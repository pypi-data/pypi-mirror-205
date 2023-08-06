# Copyright (c) 2020 Adam Souzis
# SPDX-License-Identifier: MIT
"""
TOSCA implementation
"""
import functools
import copy
from .tosca_plugins import TOSCA_VERSION
from .util import (
    UnfurlError,
    UnfurlValidationError,
    get_base_dir,
    check_class_registry,
    env_var_value,
)
from .eval import Ref, RefContext, SafeRefContext, map_value
from .result import ExternalValue, ResourceRef, ResultsList
from .merge import patch_dict, merge_dicts
from .logs import get_console_log_level
from .support import is_template, ContainerImage
from toscaparser.tosca_template import ToscaTemplate
from toscaparser.entity_template import EntityTemplate
from toscaparser.properties import Property
from toscaparser.elements.entity_type import EntityType
from toscaparser.elements.statefulentitytype import StatefulEntityType
import toscaparser.workflow
import toscaparser.imports
import toscaparser.artifacts
import toscaparser.repositories
from toscaparser.common.exception import ExceptionCollector
import os
from .logs import getLogger
import logging
import re
from typing import Dict, Optional, Sequence, cast

from ruamel.yaml.comments import CommentedMap

logger = getLogger("unfurl")

from toscaparser import functions


class RefFunc(functions.Function):
    def result(self):
        return {self.name: self.args}

    def validate(self):
        pass


for func in ["eval", "ref", "get_artifact", "has_env", "get_env"]:
    functions.function_mappings[func] = RefFunc

toscaIsFunction = functions.is_function


def is_function(function):
    return toscaIsFunction(function) or Ref.is_ref(function) or is_template(function)


functions.is_function = is_function


def validate_unfurl_identifier(name):
    # should match NamedObject in unfurl json schema
    return re.match(r"^[A-Za-z._][A-Za-z0-9._:\-]*$", name) is not None


def encode_unfurl_identifier(name):
    def encode(match):
        return f"-{ord(match.group(0))}-"

    return re.sub(r"[^A-Za-z0-9._:\-]", encode, name)


def decode_unfurl_identifier(name):
    def decode(match):
        return chr(int(match.group(1)))

    return re.sub(r"-([0-9]+)-", decode, name)


def find_standard_interface(op):
    if op in StatefulEntityType.interfaces_node_lifecycle_operations:
        return "Standard"
    elif op in ["check", "discover", "revert"]:
        return "Install"
    elif op in StatefulEntityType.interfaces_relationship_configure_operations:
        return "Configure"
    else:
        return ""


__default_topology = None


def get_default_topology():
    global __default_topology
    if __default_topology is None:
        tpl = dict(
            tosca_definitions_version=TOSCA_VERSION,
            topology_template=dict(
                node_templates={"_default": {"type": "tosca.nodes.Root"}},
                relationship_templates={
                    "_default": {"type": "tosca.relationships.Root"}
                },
            ),
        )
        __default_topology = ToscaTemplate(yaml_dict_tpl=tpl)
    return __default_topology


def _patch(node, patchsrc, quote=False, tpl=None):
    if tpl is None:
        tpl = node.toscaEntityTemplate.entity_tpl
    ctx = SafeRefContext(node, dict(template=tpl))
    ctx.base_dir = getattr(patchsrc, "base_dir", ctx.base_dir)
    if quote:
        patch = copy.deepcopy(patchsrc)
    else:
        patch = map_value(patchsrc, ctx)
    logger.trace("patching node %s was %s", node.name, tpl)
    patched = patch_dict(tpl, patch, True)
    logger.trace("patched node %s: now %s", node.name, patched)
    return patched


class ToscaSpec:
    InstallerType = "unfurl.nodes.Installer"
    topology = None
    substitution_template = None

    def evaluate_imports(self, toscaDef):
        if not toscaDef.get("imports"):
            return False
        modified = []
        for import_tpl in toscaDef["imports"]:
            if not isinstance(import_tpl, dict) or "when" not in import_tpl:
                modified.append(import_tpl)
                continue

            assert self.topology
            match = Ref(import_tpl["when"]).resolve_one(
                SafeRefContext(self.topology, trace=0)
            )
            if match:
                logger.debug(
                    "include import of %s, match found for %s",
                    import_tpl["file"],
                    import_tpl["when"],
                )
                modified.append(import_tpl)
            else:
                logger.verbose(
                    "skipping import of %s, no match for %s",
                    import_tpl["file"],
                    import_tpl["when"],
                )

        if len(modified) < len(toscaDef["imports"]):
            toscaDef["imports"] = modified
            return True
        return False

    def enforce_filters(self):
        patched = False
        for nodespec in self.nodeTemplates.values():
            for req in nodespec.requirements.values():
                for prop, value in req.get_nodefilter_properties():
                    # the target already has a node so treat the node filter
                    # as coersive by annotating the target's properties
                    target = req.relationship and req.relationship.target
                    if target:
                        if isinstance(value, dict):
                            if "eval" in value:
                                if value["eval"] is None:
                                    continue
                                value.setdefault("vars", {})["SOURCE"] = dict(
                                    eval="::" + nodespec.name
                                )
                            elif "q" in value:
                                value = value["q"]
                            else:
                                # we assume this is a constraint, so don't assign the value
                                # XXX only continue if it actually looks like one
                                continue
                        patch = dict(properties={prop: value})
                        _patch(target, patch, quote=True)
                        patched = True
                for name, value in req.get_nodefilter_requirements():
                    # annotate the target's requirements
                    target = req.relationship and req.relationship.target
                    if target:
                        matching_target_req = target.requirements.get(name)
                        if matching_target_req:
                            _patch(
                                nodespec, value, tpl=matching_target_req.entity_tpl[name]
                            )
                            patched = True

        return patched

    def _overlay(self, overlays):
        def _find_matches():
            assert self.topology
            ExceptionCollector.start()  # clears previous errors
            for expression, _tpl in overlays.items():
                try:
                    match = Ref(expression).resolve_one(
                        SafeRefContext(self.topology, trace=0)
                    )
                    if not match:
                        continue
                    if isinstance(match, (list, ResultsList)):
                        for item in match:
                            yield (item, _tpl)
                    else:
                        yield (match, _tpl)
                except Exception:
                    ExceptionCollector.appendException(
                        UnfurlValidationError(
                            f'error evaluating decorator match expression "{expression}"',
                            log=True,
                        )
                    )

        matches = list(_find_matches())
        return [_patch(*m) for m in matches]

    def _parse_template(self, path, inputs, toscaDef, resolver):
        # need to set a path for the import loader
        mode = os.getenv("UNFURL_VALIDATION_MODE")
        additionalProperties = False
        if mode is not None:
            additionalProperties = "additionalProperties" in mode
            ToscaTemplate.strict = "reqcheck" in mode
        EntityTemplate.additionalProperties = additionalProperties
        self.template = ToscaTemplate(
            path=path,
            parsed_params=inputs,
            yaml_dict_tpl=toscaDef,
            import_resolver=resolver,
            verify=False,  # we display the error messages ourselves so we don't need to verify here
        )
        ExceptionCollector.collecting = True  # don't stop collecting validation errors
        ExceptionCollector.near = " while instantiating the spec"
        self.nodeTemplates = {}
        self.installers = {}
        self.relationshipTemplates = {}
        for template in self.template.nodetemplates:
            if not template.type_definition:
                continue  # invalidate template
            nodeTemplate = NodeSpec(template, self)
            if template.is_derived_from(self.InstallerType):
                self.installers[template.name] = nodeTemplate
            self.nodeTemplates[template.name] = nodeTemplate
        if hasattr(self.template, "relationship_templates"):
            # user-declared RelationshipTemplates, source and target will be None
            for template in self.template.relationship_templates:
                relTemplate = RelationshipSpec(template, self)
                self.relationshipTemplates[template.name] = relTemplate
        self.load_imported_default_templates()
        self.topology = TopologySpec(self, inputs)
        substitution_mappings = self.template.topology_template.substitution_mappings
        if substitution_mappings and substitution_mappings.node:
            self.substitution_template = self.nodeTemplates.get(
                substitution_mappings.node
            )
        self.load_workflows()
        self.groups = {
            g.name: GroupSpec(g, self) for g in self.template.topology_template.groups
        }
        self.policies = {
            p.name: PolicySpec(p, self)
            for p in self.template.topology_template.policies
        }
        ExceptionCollector.collecting = False

    def _patch(self, toscaDef, path, errorsSoFar):
        matches = None
        decorators = self.load_decorators()
        if decorators:
            logger.debug("applying decorators %s", decorators)
            matches = self._overlay(decorators)
            # overlay uses ExceptionCollector
            if ExceptionCollector.exceptionsCaught():
                # abort if overlay caused errors
                # report previously collected errors too
                ExceptionCollector.exceptions[:0] = errorsSoFar
                message = "\n".join(
                    ExceptionCollector.getExceptionsReport(
                        full=(get_console_log_level() < logging.INFO)
                    )
                )
                raise UnfurlValidationError(
                    f"TOSCA validation failed for {path}: \n{message}",
                    ExceptionCollector.getExceptions(),
                )
        modified_imports = self.evaluate_imports(toscaDef)
        annotated = self.enforce_filters()
        return matches or modified_imports or annotated

    def __init__(
        self, toscaDef, spec=None, path=None, resolver=None, skip_validation=False
    ):
        self.discovered = None
        if spec:
            inputs = spec.get("inputs")
        else:
            inputs = None

        if isinstance(toscaDef, ToscaTemplate):
            self.template = toscaDef
        else:
            self.template = None
            topology_tpl = toscaDef.get("topology_template")
            if not topology_tpl:
                toscaDef["topology_template"] = dict(
                    node_templates={}, relationship_templates={}
                )

            if spec:
                self.load_instances(toscaDef, spec)

            logger.info("Validating TOSCA template at %s", path)
            try:
                self._parse_template(path, inputs, toscaDef, resolver)
            except:
                if (
                    not ExceptionCollector.exceptionsCaught()
                    or not self.template
                    or not self.topology
                ):
                    raise  # unexpected error

            # copy errors because self._patch() might clear them
            errorsSoFar = ExceptionCollector.exceptions[:]
            patched = self._patch(toscaDef, path, errorsSoFar)
            if patched:
                # overlay and evaluate_imports modifies tosaDef in-place, try reparsing it
                self._parse_template(path, inputs, toscaDef, resolver)
            else:  # restore previously errors
                ExceptionCollector.exceptions[:0] = errorsSoFar

            if ExceptionCollector.exceptionsCaught():
                message = "\n".join(
                    ExceptionCollector.getExceptionsReport(
                        full=(get_console_log_level() < logging.INFO)
                    )
                )
                if skip_validation:
                    logger.warning("Found TOSCA validation failures: %s", message)
                else:
                    raise UnfurlValidationError(
                        f"TOSCA validation failed for {path}: \n{message}",
                        ExceptionCollector.getExceptions(),
                    )

    @property
    def base_dir(self):
        if self.template.path is None:
            return None
        return get_base_dir(self.template.path)

    def _get_project_dir(self, home=False):
        # hacky
        if self.template and self.template.import_resolver:
            manifest = self.template.import_resolver.manifest
            if manifest.localEnv:
                if home:
                    if manifest.localEnv.homeProject:
                        return manifest.localEnv.homeProject.projectRoot
                elif manifest.localEnv.project:
                    return manifest.localEnv.project.projectRoot
        return None

    def add_node_template(self, name, tpl, discovered=True):
        assert self.template
        custom_types = None
        if "custom_types" in tpl:
            custom_types = tpl.pop("custom_types")
            if custom_types:
                # XXX check for conflicts, throw error
                self.template.topology_template.custom_defs.update(custom_types)

        nodeTemplate = self.template.topology_template.add_template(name, tpl)
        nodeSpec = NodeSpec(nodeTemplate, self)
        self.nodeTemplates[name] = nodeSpec
        if discovered:
            if self.discovered is None:
                self.discovered = CommentedMap()
            self.discovered[name] = tpl
        # add custom_types back for serialization later
        if custom_types:
            tpl["custom_types"] = custom_types
        return nodeSpec

    def load_decorators(self) -> CommentedMap:
        decorators = CommentedMap()
        for path, import_tpl in self.template.nested_tosca_tpls.items():
            imported = import_tpl.get("decorators")
            if imported:
                decorators = cast(CommentedMap, merge_dicts(decorators, imported))
        decorators = cast(CommentedMap, merge_dicts(decorators, self.template.tpl.get("decorators") or {}))
        return decorators

    def load_imported_default_templates(self) -> None:
        for name, topology in self.template.nested_topologies.items():
            for nodeTemplate in topology.nodetemplates:
                if (
                    "default" in nodeTemplate.directives
                    and nodeTemplate.name not in self.nodeTemplates
                ):
                    nodeSpec = NodeSpec(nodeTemplate, self)
                    self.nodeTemplates[nodeSpec.name] = nodeSpec

    def load_workflows(self) -> None:
        # we want to let different types defining standard workflows like deploy
        # so we need to support importing workflows
        workflows = {
            name: [Workflow(w)]
            for name, w in self.template.topology_template.workflows.items()
        }
        for topology in self.template.nested_topologies.values():
            for name, w in topology.workflows.items():
                workflows.setdefault(name, []).append(Workflow(w))
        self._workflows = workflows

    def get_workflow(self, workflow: str) -> Optional["Workflow"]:
        # XXX need api to get all the workflows with the same name
        wfs = self._workflows.get(workflow)
        if wfs:
            return wfs[0]
        else:
            return None

    def get_repository_path(self, repositoryName, file=""):
        baseArtifact = ArtifactSpec(
            dict(repository=repositoryName, file=file), spec=self
        )
        if baseArtifact.repository:
            # may resolve repository url to local path (e.g. checkout a remote git repo)
            return baseArtifact.get_path()
        else:
            return None

    def get_template(self, name):
        if name == "~topology":
            return self.topology
        elif "~c~" in name:
            nodeName, capability = name.split("~c~")
            nodeTemplate = self.nodeTemplates.get(nodeName)
            if not nodeTemplate:
                return None
            return nodeTemplate.get_capability(capability)
        elif "~r~" in name:
            nodeName, requirement = name.split("~r~")
            if nodeName:
                nodeTemplate = self.nodeTemplates.get(nodeName)
                if not nodeTemplate:
                    return None
                return nodeTemplate.get_relationship(requirement)
            else:
                return self.relationshipTemplates.get(name)
        elif "~q~" in name:
            nodeName, requirement = name.split("~q~")
            nodeTemplate = self.nodeTemplates.get(nodeName)
            if not nodeTemplate:
                return None
            return nodeTemplate.get_requirement(requirement)
        elif "~a~" in name:
            nodeTemplate = None
            nodeName, artifactName = name.split("~a~")
            if nodeName:
                nodeTemplate = self.nodeTemplates.get(nodeName)
                if not nodeTemplate:
                    return None
                artifact = nodeTemplate.artifacts.get(artifactName)
                if artifact:
                    return artifact
            # its an anonymous artifact, create inline artifact
            tpl = self._get_artifact_spec_from_name(artifactName)
            # tpl is a dict or an tosca artifact
            return ArtifactSpec(tpl, nodeTemplate, spec=self)
        else:
            return self.nodeTemplates.get(name)

    def _get_artifact_declared_tpl(self, repositoryName, file):
        # see if this is declared in a repository node template with the same name
        repository = self.nodeTemplates.get(repositoryName)
        if repository:
            artifact = repository.artifacts.get(file)
            if artifact:
                return artifact.toscaEntityTemplate.entity_tpl.copy()
        return None

    def _get_artifact_spec_from_name(self, name):
        repository, sep, file = name.partition(":")
        file = decode_unfurl_identifier(file)
        artifact = self._get_artifact_declared_tpl(repository, file)
        if artifact:
            return artifact
        spec = CommentedMap(file=file)
        if repository:
            spec["repository"] = repository
        return spec

    def is_type_name(self, typeName):
        return (
            typeName in self.template.topology_template.custom_defs
            or typeName in EntityType.TOSCA_DEF
        )

    def find_matching_templates(self, typeName):
        for template in self.nodeTemplates.values():
            if template.is_compatible_type(typeName):
                yield template

    def load_instances(self, toscaDef, tpl):
        """
        Creates node templates for any instances defined in the spec

        .. code-block:: YAML

          spec:
                instances:
                  test:
                    installer: test
                installers:
                  test:
                    operations:
                      default:
                        implementation: TestConfigurator
                        inputs:"""
        node_templates = toscaDef["topology_template"]["node_templates"]
        for name, impl in tpl.get("installers", {}).items():
            if name not in node_templates:
                node_templates[name] = dict(type=self.InstallerType, properties=impl)
            else:
                raise UnfurlValidationError(
                    f'can not add installer "{name}", there is already a node template with that name'
                )

        for name, impl in tpl.get("instances", {}).items():
            if not isinstance(impl, dict):
                continue
            if name in node_templates:
                if "default" not in node_templates[name].get("directives", []):
                    continue  # allow default templates to be overridden
            # add this as a template
            if "template" not in impl:
                node_templates[name] = self.instance_to_template(impl.copy())
            elif isinstance(impl["template"], dict):
                node_templates[name] = impl["template"]

        if "discovered" in tpl:
            # node templates added dynamically by configurators
            self.discovered = tpl["discovered"]
            for name, impl in tpl["discovered"].items():
                if name not in node_templates:
                    custom_types = impl.pop("custom_types", None)
                    node_templates[name] = impl
                    if custom_types:
                        # XXX check for conflicts, throw error
                        toscaDef.setdefault("types", CommentedMap()).update(
                            custom_types
                        )

    def instance_to_template(self, impl):
        if "type" not in impl:
            impl["type"] = "unfurl.nodes.Default"
        installer = impl.pop("install", None)
        if installer:
            impl["requirements"] = [{"install": installer}]
        return impl

    def import_connections(self, importedSpec):
        # user-declared telationship templates, source and target will be None
        for template in importedSpec.template.relationship_templates:
            if not template.default_for:
                # assume its default relationship template
                template.default_for = "ANY"
            relTemplate = RelationshipSpec(template, self)
            if template.name not in self.relationshipTemplates:  # not defined yet
                self.relationshipTemplates[template.name] = relTemplate

    def get_repository(self, name: str):
        return self.template and self.template.repositories.get(name)


def find_env_vars(props_iter):
    for propdef, value in props_iter:
        datatype = propdef.entity
        if (
            datatype.type == "map"
            and propdef.entry_schema_entity
            and propdef.entry_schema_entity.type == "unfurl.datatypes.EnvVar"
        ):
            if value:
                for key, item in value.items():
                    yield key, env_var_value(item)
        else:
            if datatype.type == "unfurl.datatypes.EnvVar":
                yield propdef.name, env_var_value(value)
            metadata = propdef.schema.get("metadata", {})
            if metadata.get("env_vars"):
                for name in metadata["env_vars"]:
                    yield name, env_var_value(value)


def find_props(attributes, propertyDefs, flatten=False):
    if not attributes:
        return
    for propdef in propertyDefs.values():
        if propdef.name not in attributes:
            continue
        if propdef.entity.properties:
            # it's complex datatype
            value = attributes[propdef.name]
            if value:
                # descend into its properties
                yield from find_props(value, propdef.entity.properties, flatten)
            else:
                yield propdef, value
        elif not flatten or not propdef.entry_schema:
            yield propdef, attributes[propdef.name]
        else:
            # its a list or map
            assert propdef.entry_schema
            properties = propdef.entry_schema_entity.properties
            value = attributes[propdef.name]
            if not value:
                yield propdef, value
                continue
            if propdef.type == "map":
                for key, val in value.items():
                    if properties:
                        # descend into its properties
                        yield from find_props(val, properties, flatten)
                    else:
                        yield propdef, (key, val)
            elif propdef.type == "list":
                for val in value:
                    if properties:
                        # descend into its properties
                        yield from find_props(val, properties, flatten)
                    else:
                        yield propdef, val


# represents a node, capability or relationship
class EntitySpec(ResourceRef):
    # XXX need to define __eq__ for spec changes
    def __init__(self, toscaNodeTemplate: Optional[EntityTemplate], spec: ToscaSpec):
        if not toscaNodeTemplate:
            toscaNodeTemplate = next(
                iter(get_default_topology().topology_template.nodetemplates)
            )
        self.toscaEntityTemplate = toscaNodeTemplate
        self.spec = spec
        self.name = toscaNodeTemplate.name
        if not validate_unfurl_identifier(self.name):
            ExceptionCollector.appendException(
                UnfurlValidationError(
                    f'"{self.name}" is not a valid TOSCA template name',
                    log=True,
                )
            )

        self.type = toscaNodeTemplate.type
        self._isReferencedBy: Sequence[
            EntitySpec
        ] = []  # this is referenced by another template or via property traversal
        # nodes have both properties and attributes
        # as do capability properties and relationships
        # but only property values are declared
        # XXX user should be able to declare default attribute values
        self.propertyDefs = toscaNodeTemplate.get_properties()
        self.attributeDefs = {}
        self.properties = CommentedMap(
            [(prop.name, prop.value) for prop in self.propertyDefs.values()]
        )
        if toscaNodeTemplate.type_definition:
            # add attributes definitions
            attrDefs = toscaNodeTemplate.type_definition.get_attributes_def()
            self.defaultAttributes = {
                prop.name: prop.default
                for prop in attrDefs.values()
                if prop.name not in ["tosca_id", "state", "tosca_name"]
            }
            for name, aDef in attrDefs.items():
                prop = Property(
                    name, aDef.default, aDef.schema, toscaNodeTemplate.custom_def
                )
                self.propertyDefs[name] = prop
                self.attributeDefs[name] = prop
            # now add any property definitions that haven't been defined yet
            # i.e. missing properties without a default and not required
            props_def = toscaNodeTemplate.type_definition.get_properties_def()
            for pDef in props_def.values():
                if pDef.schema and pDef.name not in self.propertyDefs:
                    self.propertyDefs[pDef.name] = Property(
                        pDef.name,
                        pDef.default,
                        pDef.schema,
                        toscaNodeTemplate.custom_def,
                    )
        else:
            self.defaultAttributes = {}

    def _resolve(self, key):
        """Make attributes available to expressions"""
        if key in ["name", "type", "uri", "groups", "policies"]:
            return getattr(self, key)
        raise KeyError(key)

    def get_interfaces(self):
        return self.toscaEntityTemplate.interfaces

    @property
    def groups(self):
        if not self.spec:
            return
        for g in self.spec.groups.values():
            if self.name in g.members:
                yield g

    @property
    def policies(self):
        return []

    def is_compatible_target(self, targetStr):
        if self.name == targetStr:
            return True
        return self.toscaEntityTemplate.is_derived_from(targetStr)

    def is_compatible_type(self, typeStr):
        return self.toscaEntityTemplate.is_derived_from(typeStr)

    @property
    def uri(self):
        return self.get_uri()

    def get_uri(self):
        return self.name  # XXX

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    @property
    def artifacts(self):
        return {}

    @staticmethod
    def get_name_from_artifact_spec(artifact_tpl):
        name = artifact_tpl.get(
            "name", encode_unfurl_identifier(artifact_tpl.get("file", ""))
        )
        repository_name = artifact_tpl.get("repository", "")
        if repository_name:
            return repository_name + "--" + name
        else:
            return name

    def find_or_create_artifact(self, nameOrTpl, path=None, predefined=False):
        if not nameOrTpl:
            return None
        if isinstance(nameOrTpl, str):
            name = nameOrTpl
            artifact = self.artifacts.get(nameOrTpl)
            if artifact:
                return artifact
            repositoryName = ""
        else:
            # inline, anonymous templates can only specify a file and repository
            # because ArtifactInstance don't have way to refer to the inline template
            # and only encode the file and repository in get_name_from_artifact_spec()
            tpl = nameOrTpl
            name = nameOrTpl["file"]
            repositoryName = nameOrTpl.get("repository")

        # if the artifact is defined in a repository, make a copy of it
        if not repositoryName:
            # see if artifact is declared in local repository
            for localStore in self.spec.find_matching_templates(
                "unfurl.nodes.LocalRepository"
            ):
                artifact = localStore.artifacts.get(name)
                if artifact:
                    # found, make a inline copy
                    tpl = artifact.toscaEntityTemplate.entity_tpl.copy()
                    tpl["name"] = name
                    tpl["repository"] = localStore.name
                    break
            else:
                if predefined and not check_class_registry(name):
                    logger.warning(f"no artifact named {name} found")
                    return None

                # otherwise name not found, assume it's a file path or URL
                tpl = dict(file=name)
        else:
            # see if this is declared in a repository node template with the same name
            artifact_tpl = self.spec._get_artifact_declared_tpl(repositoryName, name)
            if artifact_tpl:
                tpl = artifact_tpl
                tpl["repository"] = repositoryName

        # create an anonymous, inline artifact
        return ArtifactSpec(tpl, self, path=path)

    @property
    def abstract(self):
        return None

    @property
    def directives(self):
        return []

    @property
    def tpl(self):
        return self.toscaEntityTemplate.entity_tpl

    def find_props(self, attributes):
        yield from find_props(attributes, self.propertyDefs)

    @property
    def base_dir(self):
        if self.toscaEntityTemplate._source:
            return self.toscaEntityTemplate._source
        elif self.spec:
            return self.spec.base_dir
        else:
            return None

    def aggregate_only(self):
        "The template is only the sum of its parts."
        for iDef in self.get_interfaces():
            if iDef.interfacename in ("Standard", "Configure"):
                return False
            if iDef.interfacename == "Install" and iDef.name == "discover":
                return False
        # no implementations found
        return True

    def validate(self) -> None:
        """
        Raises UnfurlValidationError on failure.
        """
        pass

    @property
    def required(self) -> bool:
        # check if this template is required by another template
        for root in _get_roots(self):
            if self.spec.substitution_template:
                if self.spec.substitution_template is root:
                    # require if a root of this template is the substitution_template
                    return True
            elif "default" not in root.directives:
                # otherwise require when there is a root that isn't a defaults template
                return True
        return False

    @property
    def environ(self):
        return os.environ


def _get_roots(node: EntitySpec, seen=None):
    # node can reference each other's properties, so we need to handle circular references
    if seen is None:
        seen = set()
    yield node
    for parent in node._isReferencedBy:
        if parent.name not in seen:
            seen.add(node.name)
            yield from _get_roots(parent, seen)


class NodeSpec(EntitySpec):
    # has attributes: tosca_id, tosca_name, state, (3.4.1 Node States p.61)
    def __init__(self, template=None, spec=None):
        if not template:
            template = next(
                iter(get_default_topology().topology_template.nodetemplates)
            )
            spec = ToscaSpec(get_default_topology())
        else:
            assert spec
        EntitySpec.__init__(self, template, spec)
        self._capabilities = None
        self._requirements: Optional[Dict[str, "RequirementSpec"]] = None
        self._relationships = []
        self._artifacts = None

    def _resolve(self, key):
        try:
            return super()._resolve(key)
        except KeyError:
            req = self.get_requirement(key)
            if not req:
                raise KeyError(key)
            relationship = req.relationship
            # hack!
            relationship.toscaEntityTemplate.entity_tpl = list(req.entity_tpl.values())[
                0
            ]
            return relationship

    def get_interface_requirements(self):
        return self.toscaEntityTemplate.type_definition.get_interface_requirements(
            self.toscaEntityTemplate.entity_tpl
        )

    @property
    def artifacts(self):
        if self._artifacts is None:
            self._artifacts = {
                name: ArtifactSpec(artifact, self)
                for name, artifact in self.toscaEntityTemplate.artifacts.items()
            }
        return self._artifacts

    @property
    def policies(self):
        if not self.spec:
            return
        for p in self.spec.policies.values():
            if p.toscaEntityTemplate.targets_type == "groups":
                # the policy has groups as members, see if this node's groups is one of them
                if p.members & {g.name for g in self.groups}:
                    yield p
            elif p.toscaEntityTemplate.targets_type == "node_templates":
                if self.name in p.members:
                    yield p

    @property
    def requirements(self) -> Dict[str, "RequirementSpec"]:
        if self._requirements is None:
            self._requirements = {}
            nodeTemplate = self.toscaEntityTemplate
            for (relTpl, req, req_type_def) in nodeTemplate.relationships:
                name, values = next(iter(req.items()))
                reqSpec = RequirementSpec(name, req, self, req_type_def)
                if relTpl.target:
                    nodeSpec = self.spec.get_template(relTpl.target.name)
                    if nodeSpec:
                        nodeSpec.add_relationship(reqSpec)
                    else:
                        msg = f'Missing target node "{relTpl.target.name}" for requirement "{name}" on "{self.name}"'
                        ExceptionCollector.appendException(UnfurlValidationError(msg))
                self._requirements[name] = reqSpec
        return self._requirements

    def get_requirement(self, name):
        return self.requirements.get(name)

    def get_relationship(self, name):
        req = self.requirements.get(name)
        if not req:
            return None
        return req.relationship

    @property
    def relationships(self):
        """
        returns a list of RelationshipSpecs that are targeting this node template.
        """
        for r in self.toscaEntityTemplate.get_relationship_templates():
            assert r.source
            # calling requirement property will ensure the RelationshipSpec is properly linked
            self.spec.get_template(r.source.name).requirements
        return self._get_relationship_specs()

    def _get_relationship_specs(self):
        if len(self._relationships) != len(
            self.toscaEntityTemplate.get_relationship_templates()
        ):
            # get_relationship_templates() is a list of RelationshipTemplates that target the node
            rIds = {id(r.toscaEntityTemplate) for r in self._relationships}
            for r in self.toscaEntityTemplate.get_relationship_templates():
                if id(r) not in rIds and r.capability:
                    self._relationships.append(RelationshipSpec(r, self.spec, self))
        return self._relationships

    def get_capability_interfaces(self):
        idefs = [r.get_interfaces() for r in self._get_relationship_specs()]
        return [i for elem in idefs for i in elem if i.name != "default"]

    def get_requirement_interfaces(self):
        idefs = [r.get_interfaces() for r in self.requirements.values()]
        return [i for elem in idefs for i in elem if i.name != "default"]

    @property
    def capabilities(self):
        if self._capabilities is None:
            self._capabilities = {
                c.name: CapabilitySpec(self, c)
                for c in self.toscaEntityTemplate.get_capabilities_objects()
            }
        return self._capabilities

    def get_capability(self, name):
        return self.capabilities.get(name)

    def add_relationship(self, reqSpec: "RequirementSpec"):
        # find the relationship for this requirement:
        for relSpec in self._get_relationship_specs():
            # the RelationshipTemplate should have had the source node assigned by the tosca parser
            # XXX this won't distinguish between more than one relationship between the same two nodes
            # to fix this have the RelationshipTemplate remember the name of the requirement
            if (
                relSpec.toscaEntityTemplate.source.name
                == reqSpec.parentNode.toscaEntityTemplate.name
            ):
                assert (
                    not reqSpec.relationship
                    or reqSpec.relationship.name == relSpec.name
                ), (
                    reqSpec.relationship,
                    relSpec,
                )
                reqSpec.relationship = relSpec
                assert (
                    not relSpec.requirement or relSpec.requirement.name == reqSpec.name
                ), (
                    relSpec.requirement,
                    reqSpec,
                )
                if not relSpec.requirement:
                    relSpec.requirement = reqSpec
                    relSpec._isReferencedBy.append(self)  # type: ignore
                break
        else:
            msg = f'relationship not found for requirement "{reqSpec.name}" on "{reqSpec.parentNode}" targeting "{self.name}"'
            ExceptionCollector.appendException(UnfurlValidationError(msg))

    @property
    def abstract(self):
        if self.tpl.get("imported"):
            return "select"
        for name in ("select", "substitute"):
            if name in self.toscaEntityTemplate.directives:
                return name
        return None

    @property
    def directives(self):
        return self.toscaEntityTemplate.directives

    def validate(self):
        super().validate()
        missing = self.toscaEntityTemplate.missing_requirements
        if missing:
            raise UnfurlValidationError(
                f"Node template {self.name} is missing requirements: {','.join(missing)}"
            )


class RelationshipSpec(EntitySpec):
    """
    Links a RequirementSpec to a CapabilitySpec.
    """

    def __init__(self, template=None, spec=None, targetNode=None):
        # template is a RelationshipTemplate
        # It is a full-fledged entity with a name, type, properties, attributes, interfaces, and metadata.
        # its connected through target, source, capability
        # its RelationshipType has valid_target_types
        if not template:
            template = get_default_topology().topology_template.relationship_templates[
                0
            ]
            spec = ToscaSpec(get_default_topology())
        else:
            assert spec
        EntitySpec.__init__(self, template, spec)
        self.requirement = None
        self.capability = None
        if targetNode:
            assert targetNode.toscaEntityTemplate is template.target
            for c in targetNode.capabilities.values():
                if c.toscaEntityTemplate is template.capability:
                    self.capability = c
                    break
            else:
                raise UnfurlError(
                    "capability %s not found in %s for %s"
                    % (
                        template.capability.name,
                        [c.name for c in targetNode.capabilities.values()],
                        targetNode.name,
                    )
                )

    @property
    def source(self):
        return self.requirement.parentNode if self.requirement else None

    @property
    def target(self):
        return self.capability.parentNode if self.capability else None

    def _resolve(self, key):
        try:
            return super()._resolve(key)
        except KeyError:
            if self.capability:
                if self.capability.parentNode.is_compatible_target(key):
                    return self.capability.parentNode
                if self.capability.is_compatible_target(key):
                    return self.capability
            raise KeyError(key)

    def get_uri(self):
        suffix = "~r~" + self.name
        return self.source.name + suffix if self.source else suffix

    def matches_target(self, capability):
        defaultFor = self.toscaEntityTemplate.default_for
        if not defaultFor:
            return False
        nodeTemplate = capability.parentNode.toscaEntityTemplate
        if defaultFor == self.toscaEntityTemplate.ANY and capability.name == "feature":
            # XXX get_matching_capabilities() buggy in this case
            return True  # optimization
        if (
            defaultFor == self.toscaEntityTemplate.ANY
            or defaultFor == nodeTemplate.name
            or nodeTemplate.is_derived_from(defaultFor)
            or defaultFor == capability.name
            or capability.is_derived_from(defaultFor)
        ):
            return self.toscaEntityTemplate.get_matching_capabilities(
                nodeTemplate, capability.name
            )

        return False


class RequirementSpec:
    """
    A Requirement shares a Relationship with a Capability.
    """

    # XXX need __eq__ since this doesn't derive from EntitySpec
    def __init__(self, name: str, req: dict, parent: NodeSpec, type_tpl: dict):
        self.source = self.parentNode = parent
        self.spec = parent.spec
        self.name = name
        self.entity_tpl = req
        self.relationship: Optional[RelationshipSpec] = None
        self.type_tpl = type_tpl
        # entity_tpl may specify:
        # capability (definition name or type name), node (template name or type name), and node_filter,
        # relationship (template name or type name or inline relationship template)
        # occurrences

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}'):{self.entity_tpl}"

    @property
    def artifacts(self):
        return self.parentNode.artifacts

    def get_uri(self):
        return self.parentNode.name + "~q~" + self.name

    def get_interfaces(self):
        return self.relationship.get_interfaces() if self.relationship else []

    def get_nodefilter_properties(self):
        # XXX should merge type_tpl with entity_tpl
        return get_nodefilters(self.type_tpl, "properties")

    def get_nodefilter_requirements(self):
        # XXX should merge type_tpl with entity_tpl
        return get_nodefilters(self.type_tpl, "requirements")


def get_nodefilters(entity_tpl, key):
    if not isinstance(entity_tpl, dict):
        return
    nodefilter = entity_tpl.get("node_filter")
    if nodefilter and nodefilter.get(key):
        for filter in nodefilter[key]:
            name, value = next(iter(filter.items()))
            yield name, value


class CapabilitySpec(EntitySpec):
    def __init__(self, parent=None, capability=None):
        if not parent:
            parent = NodeSpec()
            capability = parent.toscaEntityTemplate.get_capabilities_objects()[0]
        self.parentNode = parent
        assert capability
        # capabilities.Capability isn't an EntityTemplate but duck types with it
        EntitySpec.__init__(self, capability, parent.spec)
        self._relationships = None
        self._defaultRelationships = None

    @property
    def parent(self):
        return self.parentNode

    @property
    def artifacts(self):
        return self.parentNode.artifacts

    def get_interfaces(self):
        # capabilities don't have their own interfaces
        return self.parentNode.get_interfaces()

    def get_uri(self):
        # capabilities aren't standalone templates
        # this is demanagled by getTemplate()
        return self.parentNode.name + "~c~" + self.name

    @property
    def relationships(self):
        return [r for r in self.parentNode.relationships if r.capability is self]

    @property
    def default_relationships(self):
        if self._defaultRelationships is None:
            self._defaultRelationships = [
                relSpec
                for relSpec in self.spec.relationshipTemplates.values()
                if relSpec.matches_target(self)
            ]
        return self._defaultRelationships

    def get_default_relationships(self, relation=None):
        if not relation:
            return self.default_relationships
        return [
            relSpec
            for relSpec in self.default_relationships
            if relSpec.is_compatible_type(relation)
        ]


class TopologySpec(EntitySpec):
    # has attributes: tosca_id, tosca_name, state, (3.4.1 Node States p.61)
    def __init__(self, spec=None, inputs=None):
        if spec:
            self.spec = spec
            template = spec.template.topology_template
        else:
            template = get_default_topology().topology_template
            self.spec = ToscaSpec(get_default_topology())
            self.spec.topology = self

        inputs = inputs or {}
        self.toscaEntityTemplate = template
        self.name = "~topology"
        self.type = "~topology"
        self.inputs = {
            input.name: inputs.get(input.name, input.default)
            for input in template.inputs
        }
        self.outputs = {output.name: output.value for output in template.outputs}
        self.properties = CommentedMap()  # XXX implement substitution_mappings
        self.defaultAttributes = {}
        self.propertyDefs = {}
        self.attributeDefs = {}
        self.capabilities = []
        self._defaultRelationships = None
        self._isReferencedBy = []

    def get_interfaces(self):
        # doesn't have any interfaces
        return []

    def is_compatible_target(self, targetStr):
        if self.name == targetStr:
            return True
        return False

    def is_compatible_type(self, typeStr):
        return False

    @property
    def primary_provider(self):
        return self.spec.relationshipTemplates.get("primary_provider")

    @property
    def default_relationships(self):
        if self._defaultRelationships is None:
            self._defaultRelationships = [
                relSpec
                for relSpec in self.spec.relationshipTemplates.values()
                if relSpec.toscaEntityTemplate.default_for
            ]
        return self._defaultRelationships

    @property
    def base_dir(self):
        return self.spec.base_dir

    def _resolve(self, key):
        """Make attributes available to expressions"""
        try:
            return super()._resolve(key)
        except KeyError:
            nodeTemplates = self.spec.nodeTemplates
            nodeSpec = nodeTemplates.get(key)
            if nodeSpec:
                return nodeSpec
            matches = [n for n in nodeTemplates.values() if n.is_compatible_type(key)]
            if not matches:
                raise KeyError(key)
            return matches

    @property
    def tpl(self):
        return self.toscaEntityTemplate.tpl


class Workflow:
    def __init__(self, workflow):
        self.workflow = workflow

    def __str__(self):
        return f"Workflow({self.workflow.name})"

    def initial_steps(self):
        preceeding = set()
        for step in self.workflow.steps.values():
            preceeding.update(step.on_success + step.on_failure)
        return [
            step for step in self.workflow.steps.values() if step.name not in preceeding
        ]

    def get_step(self, stepName):
        return self.workflow.steps.get(stepName)

    def match_step_filter(self, stepName, resource):
        step = self.get_step(stepName)
        if step:
            return all(filter.evaluate(resource.attributes) for filter in step.filter)
        return None

    def match_preconditions(self, resource):
        for precondition in self.workflow.preconditions:
            target = resource.root.find_resource(precondition.target)
            # XXX if precondition.target_relationship
            if not target:
                # XXX target can be a group
                return False
            if not all(
                filter.evaluate(target.attributes) for filter in precondition.condition
            ):
                return False
        return True


class ArtifactSpec(EntitySpec):
    buildin_fields = (
        "file",
        "repository",
        "deploy_path",
        "version",
        "checksum",
        "checksum_algorithm",
        "mime_type",
        "file_extensions",
    )

    def __init__(
        self,
        artifact_tpl,
        template: Optional[EntitySpec] = None,
        spec: Optional[ToscaSpec] = None,
        path=None,
    ):
        # 3.6.7 Artifact definition p. 84
        self.parentNode = template
        spec = template.spec if template else spec
        assert spec
        if isinstance(artifact_tpl, toscaparser.artifacts.Artifact):
            artifact = artifact_tpl
        else:
            # inline artifact
            name = self.get_name_from_artifact_spec(artifact_tpl)
            artifact_tpl.pop("name", None)  # "name" isn't a valid key
            custom_defs = spec and spec.template.topology_template.custom_defs or {}
            artifact = toscaparser.artifacts.Artifact(
                name, artifact_tpl, custom_defs, path
            )
        EntitySpec.__init__(self, artifact, spec)
        self.repository: Optional[toscaparser.repositories.Repository] = (
            spec
            and artifact.repository
            and spec.get_repository(artifact.repository)
            or None
        )
        # map artifacts fields into properties
        for prop in self.buildin_fields:
            self.defaultAttributes[prop] = getattr(artifact, prop)

    def get_uri(self):
        if self.parentNode:
            return self.parentNode.name + "~a~" + self.name
        else:
            return "~a~" + self.name

    @property
    def file(self):
        return self.toscaEntityTemplate.file

    @property
    def base_dir(self):
        if self.toscaEntityTemplate._source:
            return get_base_dir(self.toscaEntityTemplate._source)
        else:
            return super().base_dir

    def get_path(self, resolver=None):
        return self.get_path_and_fragment(resolver)[0]

    def get_path_and_fragment(self, resolver=None, tpl=None):
        """
        returns path, fragment
        """
        tpl = self.spec and self.spec.template.tpl or tpl
        if not resolver and self.spec:
            resolver = self.spec.template.import_resolver

        loader = toscaparser.imports.ImportsLoader(
            None, self.base_dir, repositories=tpl.get("repositories"), resolver=resolver
        )
        path, isFile, fragment = loader._resolve_import_template(
            None, self.as_import_spec()
        )
        return path, fragment

    def as_import_spec(self):
        return dict(file=self.file, repository=self.toscaEntityTemplate.repository)

    def as_value(self) -> Optional[ExternalValue]:
        if self.is_compatible_type("tosca.artifacts.Deployment.Image.Container.Docker"):
            artifactDef = self.toscaEntityTemplate
            assert not artifactDef.checksum or artifactDef.checksum_algorithm == 256
            kw = dict(tag=self.properties.get("tag"), digest=artifactDef.checksum)
            if self.repository:
                kw["registry_host"] = self.repository.hostname
                if self.repository.credential:
                    kw["username"] = self.repository.credential.get("user")
                    kw["password"] = self.repository.credential.get("token")
            return ContainerImage(artifactDef.file, **kw)
        # XXX return File or FilePath
        return None


class GroupSpec(EntitySpec):
    def __init__(self, template, spec):
        EntitySpec.__init__(self, template, spec)
        self.members = template.members

    # XXX getNodeTemplates() getInstances(), getChildren()

    @property
    def member_groups(self):
        return [self.spec.groups[m] for m in self.members if m in self.spec.groups]

    @property
    def policies(self):
        if not self.spec:
            return
        for p in self.spec.policies.values():
            if p.toscaEntityTemplate.targets_type == "groups":
                if self.name in p.members:
                    yield p


class PolicySpec(EntitySpec):
    def __init__(self, template, spec):
        EntitySpec.__init__(self, template, spec)
        self.members = set(template.targets_list)
