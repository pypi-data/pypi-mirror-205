from dataclasses import dataclass
import typing
from provider import namespace, resources
from common_fate_schema.provider import v1alpha1


class ParseError(Exception):
    """Raised if Provider arguments cannot be parsed"""


@dataclass
class Option:
    value: str
    label: str
    description: typing.Optional[str] = None


_T = typing.TypeVar("_T")


def _initialise(cls: type[_T], raw_targets: dict) -> _T:
    # initialise an instance of the Target class 'cls'
    instance = cls()

    # assign each variable in the class based on the 'raw_targets' dict
    all_vars = [k for k in vars(cls).keys() if not k.startswith("__")]
    for k in all_vars:
        if k not in raw_targets:
            raise ParseError(f"{k} argument is required")
        val = raw_targets[k]
        setattr(instance, k, val)

    return instance


@dataclass
class Field:
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None


class String(Field):
    pass


@dataclass
class Resource(Field):
    resource: typing.Optional[resources.Resource] = None


def export_schema() -> typing.Dict[str, v1alpha1.Target]:
    """
    Exports the target schema defined in an Target class
    to a dictionary.

    For example, if Target is defined as:
    ```
    class Target(target.Target):
        group = target.String(title="Group", description="group to grant access to")
    ```

    this method will produce a dictionary in the form:
    ```json
    {
        "group": {
            "id": "group",
            "description": "group to grant access to",
            "title": "Group",
            "type": "string"
        }
    }
    ```
    """
    all_targets: typing.Dict[str, v1alpha1.Target] = {}

    for kind, registered_target in namespace.get_target_classes().items():
        target_class = registered_target.cls
        target_schema: typing.Dict[str, v1alpha1.TargetField] = {}
        all_vars = [
            (k, v) for (k, v) in vars(target_class).items() if not k.startswith("__")
        ]
        for k, v in all_vars:
            if type(v) == String:
                val: String = v
                schema = v1alpha1.TargetField(
                    title=val.title,
                    type="string",
                    resource=None,
                    description=val.description,
                )

                target_schema[k] = schema
            if type(v) == Resource:
                val: Resource = v
                schema = {
                    "id": k,
                    "type": "string",
                    "title": val.title,
                    "resourceName": val.resource.__name__,
                }

                schema = v1alpha1.TargetField(
                    title=val.title,
                    type="string",
                    resource=val.resource.__name__,
                    description=val.description,
                )

                target_schema[k] = schema

        all_targets[kind] = v1alpha1.Target(type="object", properties=target_schema)

    return all_targets
