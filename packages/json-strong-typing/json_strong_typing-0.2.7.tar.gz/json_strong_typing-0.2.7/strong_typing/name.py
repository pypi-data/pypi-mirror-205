"""
Type-safe data interchange for Python data classes.

:see: https://github.com/hunyadi/strong_typing
"""

import typing
from typing import Literal, Union

from .auxiliary import _auxiliary_types
from .inspection import (
    is_generic_dict,
    is_generic_list,
    is_type_optional,
    is_type_union,
    unwrap_generic_dict,
    unwrap_generic_list,
    unwrap_optional_type,
    unwrap_union_types,
)


def _python_type_to_str(data_type: type) -> str:
    "Returns the string representation of a Python type without metadata."

    origin = typing.get_origin(data_type)
    if origin is not None:
        data_type_args = typing.get_args(data_type)

        if origin is dict:  # Dict[T]
            origin_name = "Dict"
        elif origin is list:  # List[T]
            origin_name = "List"
        elif origin is set:  # Set[T]
            origin_name = "Set"
        elif origin is Union:
            if len(data_type_args) == 2 and type(None) in data_type_args:
                # Optional[T] is represented as Union[T, None]
                origin_name = "Optional"
                data_type_args = tuple(t for t in data_type_args if t is not type(None))
            else:
                origin_name = "Union"
        elif origin is Literal:
            args = ", ".join(repr(arg) for arg in data_type_args)
            return f"Literal[{args}]"
        else:
            origin_name = origin.__name__

        args = ", ".join(python_type_to_str(t) for t in data_type_args)
        return f"{origin_name}[{args}]"

    if isinstance(data_type, typing.ForwardRef):
        fwd: typing.ForwardRef = data_type
        return fwd.__forward_arg__

    return data_type.__name__


def python_type_to_str(data_type: type) -> str:
    "Returns the string representation of a Python type."

    if data_type is type(None):
        return "None"

    # use compact name for alias types
    name = _auxiliary_types.get(data_type)
    if name is not None:
        return name

    metadata = getattr(data_type, "__metadata__", None)
    if metadata is not None:
        # type is Annotated[T, ...]
        arg = typing.get_args(data_type)[0]
        s = _python_type_to_str(arg)
        args = ", ".join(repr(m) for m in metadata)
        return f"Annotated[{s}, {args}]"
    else:
        # type is a regular type
        return _python_type_to_str(data_type)


def python_type_to_name(data_type: object, force: bool = False) -> str:
    """
    Returns the short name of a Python type.

    :param force: Whether to produce a name for composite types such as generics.
    """

    # use compact name for alias types
    name = _auxiliary_types.get(data_type)
    if name is not None:
        return name

    # unwrap annotated types
    metadata = getattr(data_type, "__metadata__", None)
    if metadata is not None:
        # type is Annotated[T, ...]
        arg = typing.get_args(data_type)[0]
        return python_type_to_name(arg)

    if force:
        # generic types
        if is_type_optional(data_type, strict=True):
            inner_name = python_type_to_name(unwrap_optional_type(data_type))
            return f"Optional__{inner_name}"
        elif is_generic_list(data_type):
            item_name = python_type_to_name(unwrap_generic_list(data_type))
            return f"List__{item_name}"
        elif is_generic_dict(data_type):
            key_type, value_type = unwrap_generic_dict(data_type)
            key_name = python_type_to_name(key_type)
            value_name = python_type_to_name(value_type)
            return f"Dict__{key_name}__{value_name}"
        elif is_type_union(data_type):
            member_types = unwrap_union_types(data_type)
            member_names = "__".join(
                python_type_to_name(member_type) for member_type in member_types
            )
            return f"Union__{member_names}"

    # named system or user-defined type
    if hasattr(data_type, "__name__") and not typing.get_args(data_type):
        return data_type.__name__

    raise TypeError(f"cannot assign a simple name to type: {data_type}")
