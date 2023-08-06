"""Module providingFunction utilities for the runner."""
import importlib.util
from typing import List, Tuple, Optional
from core.types import Resource
from core.logger import _logger
from core.exception import GrpcPopulationException
from oak9.tython.models.shared.shared_pb2 import DesignGap, Violation, RunnerException
from google.protobuf.message import Message

log = _logger()


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validation_results(results: List[Tuple[Resource, List[Violation], List[RunnerException]]]):
    grpc_design_gaps: list = []
    grpc_exceptions: list = []
    grpc_violation: list = []

    try:

        for resource, violations, exceptions, meta_info in results:
            for exception in exceptions:
                grpc_exception = RunnerException(
                    error_code=exception.error_code,
                    error_message=exception.error_message
                )

                grpc_exceptions.append(grpc_exception)

            for violation in violations:

                grpc_violation = Violation(
                    severity=violation.severity.name,
                    capability_id=violation.capability_id,
                    capability_name=violation.capability_name,

                    resource_id=violation.resource_id,
                    resource_type=violation.resource_type,
                    config_id=violation.config_id,
                    config_value=str(violation.config_value),
                    oak9_guidance="",
                    preffered_value=violation.preferred_value,
                    config_gap=violation.config_gap,
                    config_impact=violation.config_impact,
                    config_fix=violation.config_fix
                )

                if violation.capability_id in [existing_design_gap.capability_id for existing_design_gap in
                                               grpc_design_gaps]:
                    for existing_design_gap in grpc_design_gaps:
                        if existing_design_gap.capability_id == violation.capability_id:
                            existing_design_gap.violations.append(grpc_violation)
                else:

                    new_design_gap: DesignGap = DesignGap(
                        capability_id=violation.capability_id,
                        capability_name="",
                        source='Aws' if 'aws' in meta_info.resource_type.lower() else 'Azure',
                        resource_name=meta_info.resource_name,
                        resource_id=meta_info.resource_id,
                        resource_type=meta_info.resource_type,
                        # We may be able to get the below info from the blueprint once mapped
                        resource_gap="Critical",
                        resource_impact="Critical"
                    )

                    new_design_gap.violations.append(grpc_violation)
                    grpc_design_gaps.append(new_design_gap)

    except Exception as e:

        log.warning("Error", Message="Unable To Create gRPC Design Gap Response Due Exception", ErrorType=type(e),
                    Error=e, RequestId=meta_info.request_id, Caller=meta_info.caller)

        exception = GrpcPopulationException(meta_info, e)

        grpc_exception = RunnerException(
            error_code=exception.error_code,
            error_message=exception.error_message
        )

        grpc_exceptions.append(grpc_exception)

    return grpc_design_gaps, grpc_exceptions


def get_config_id_list(
        resource_to_flatten: object,
        resource_name: str,
        config_name: str,
        sub_resource_id: Optional[int] = None) -> list[str]:
    """
    Passes The necessary information to the recursive function that will generate the list of config ids

    Args:
        resource_to_flatten: Resource that contains the configuration that is in violation
        resource_name: Name of the resource
        config_name: Name of the configuration
        sub_resource_id: ID of the subresource that contains config_name

    Returns:
        config_id_list: A list of strings is returned
    """

    config_name_list: list = []
    csp_list: list = ['azure', 'aws', 'gcp']

    def flatten(resource: object, name: str):
        """
        Recursively traverses the resource dictionary to generate the unique_id for requested resource config.
        ! Throws a recursion error if the resource passed in contains circular dependencies in it proto definition !
        Args:
            resource: Object that contains resource configuration dictionary to be parsed
            name: Current name of resource
        Returns:
            config_id
        """
        resource_properties = [
            k for k in resource.__class__.__dict__.keys()
            if not k.startswith("_") and k[0].islower() and k != "resource_info"
        ]

        for resource_property in resource_properties:
            current_name = name + '.' + resource_property
            current_property = getattr(resource, resource_property)
            current_property_type = str(type(current_property))

            # if current_property is a list then iterate through it
            if current_property_type == "<class 'google.protobuf.pyext._message.RepeatedCompositeContainer'>" or current_property_type == "<class 'google.protobuf.internal.containers.RepeatedCompositeFieldContainer'>":

                i = 0
                for item in current_property:
                    flatten(item, current_name + '[' + str(i) + ']')

                    i = i + 1

            # if current_property is an object then flatten
            elif any(csp for csp in csp_list if csp in current_property_type):
                flatten(current_property, current_name)

            # found the config name of object we want
            if config_name in current_name and sub_resource_id is None:
                config_name_list.append(current_name)

            elif config_name in current_name and id(resource) == sub_resource_id:
                config_name_list.append(current_name)

            elif config_name in str(current_property) and id(resource) == sub_resource_id:
                if type(current_property) is str:
                    config_name_list.append(current_name + "." + current_property)

        return config_name_list

    return flatten(resource_to_flatten, resource_name)


def get_config_id_list_simplified(
        resource: object,
        resource_name: str,
        config_name: str,
        sub_resource_id: Optional[int] = None) -> list[str]:
    name_list = []

    def print_message_fields(message, prefix="", name_list=None):
        if name_list is None:
            name_list = []

        for field_descriptor, value in message.ListFields():
            field_name = field_descriptor.name
            field_path = prefix + "." + field_name if prefix else field_name
            if field_descriptor.message_type:
                if field_descriptor.label == field_descriptor.LABEL_REPEATED:
                    for submessage in value:
                        print_message_fields(submessage, prefix=field_path, name_list=name_list)
                else:
                    print_message_fields(value, prefix=field_path, name_list=name_list)
            else:
                name_list.append(field_path)

            # found the config name of object we want
            if config_name in field_name and sub_resource_id is None:
                name_list.append(field_name)

            elif config_name in field_name and id(resource) == sub_resource_id:
                name_list.append(field_name)

            elif config_name in str(field_path) and id(resource) == sub_resource_id:
                if type(field_path) is str:
                    name_list.append(field_name + "." + field_path)

    print_message_fields(resource, prefix=resource_name, name_list=name_list)

    return name_list


def normalize_name_format(resource: Resource) -> str:
    """
    normalize_name_format returns a snake case version of the objects name
    Args:
        resource:  DESCRIPTOR Property from resource that contains the resource name.
    Returns:
        name: returns name of object in snake case
    """
    resource_name: str = resource.name[0]
    for counter, character in enumerate(resource.name):
        if character == "_" or counter == 0:
            continue
        elif character.isupper() and (resource_name[-1].islower() or resource_name[-1].isdigit()):
            resource_name += '_' + character
        else:
            resource_name += character

    return resource_name.lower()


def get_config_id(bundle: Message, config_name: str, sub_resource: Optional[Message] = None) -> str:
    """
    Generates the unique path (id) that ties the violation to the offending property.
    Args:
        bundle: Top-level (bundle) message containing the resource that failed validation.
        config_name: name of the property that caused the violation (ex. name).
        sub_resource: Full path to the Message that contains the violation. Defaults to None.
    """

    if sub_resource is not None:
        sub_resource_id = id(sub_resource)
    else:
        sub_resource_id = None

    resource_name = normalize_name_format(bundle.DESCRIPTOR)
    # config_id_list = get_config_id_list(bundle, resource_name, config_name, sub_resource_id)
    config_id_list = get_config_id_list_simplified(bundle, resource_name, config_name, sub_resource_id)

    for config_id in config_id_list:
        if config_name == config_id.split('.')[-1]:
            return config_id

    return ""
    # raise Exception(
    #     f"Failed to generate config_id for bundle: {bundle.DESCRIPTOR.name},"
    #     f" property: {config_name},"
    #     f" sub_resource: {sub_resource}")
