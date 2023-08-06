import types
from enum import StrEnum, auto


class TYPE(StrEnum):
    BYTES = auto()
    FUNCTION = auto()
    CELL = auto()
    CLASS = auto()
    ITERATOR = auto()
    CODE = auto()
    OBJECT = auto()
    MODULE = auto()
    TUPLE = auto()
    SET = auto()


UNSERIALIZABLE_DUNDER = (
    "__mro__",
    "__base__",
    "__basicsize__",
    "__class__",
    "__dictoffset__",
    "__name__",
    "__qualname__",
    "__text_signature__",
    "__itemsize__",
    "__flags__",
    "__weakrefoffset__",
    "__objclass__",
)

UNSERIALIZABLE_TYPES = (
    types.WrapperDescriptorType,
    types.MethodDescriptorType,
    types.BuiltinFunctionType,
    types.MappingProxyType,
    types.GetSetDescriptorType,
)

UNSERIALIZABLE_CODE_TYPES = (
    "co_positions",
    "co_lines",
    "co_exceptiontable",
    "co_lnotab",
)
