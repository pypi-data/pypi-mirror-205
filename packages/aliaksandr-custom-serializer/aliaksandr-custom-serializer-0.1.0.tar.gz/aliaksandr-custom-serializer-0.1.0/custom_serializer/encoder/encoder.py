import base64
import builtins
import inspect
import types

from .constants import (
    TYPE,
    UNSERIALIZABLE_DUNDER,
    UNSERIALIZABLE_TYPES,
    UNSERIALIZABLE_CODE_TYPES,
)
from .helpers import is_iterable, get_class_that_defined_method

PRIMITIVES = (int, str, bool, float, types.NoneType)


class Encoder:
    @classmethod
    def encode(cls, obj):
        if isinstance(obj, PRIMITIVES):
            return obj

        if isinstance(obj, types.ModuleType):
            return cls._encode_module(obj)

        if isinstance(obj, types.CellType):
            return cls._encode_cell(obj)

        if isinstance(obj, bytes):
            return cls._encode_bytes(obj)

        if isinstance(obj, list):
            return type(obj)((cls.encode(item) for item in obj))

        if isinstance(obj, (tuple, set)):
            return cls._encode_collection(obj)

        if isinstance(obj, dict):
            return {key: cls.encode(value) for key, value in obj.items()}

        if isinstance(obj, (types.FunctionType, types.MethodType)):
            return cls._encode_function(obj)

        if isinstance(obj, type):
            return cls._encode_class(obj)

        if isinstance(obj, types.CodeType):
            return cls._encode_code(obj)

        if is_iterable(obj):
            return cls._encode_iterator(obj)

        if isinstance(obj, object):
            return cls._encode_object(obj)

    @classmethod
    def decode(cls, obj) -> any:
        if isinstance(obj, PRIMITIVES):
            return obj

        if isinstance(obj, list):
            return type(obj)((cls.decode(item) for item in obj))

        if isinstance(obj, dict):
            type_to_decode = cls._get_type(obj)

            if type_to_decode is None:
                return {key: cls.decode(value) for key, value in obj.items()}

            if type_to_decode == TYPE.BYTES:
                return cls._decode_bytes(obj)

            if type_to_decode == TYPE.FUNCTION:
                return cls._decode_function(obj)

            if type_to_decode == TYPE.CELL:
                return cls._decode_cell(obj)

            if type_to_decode == TYPE.CLASS:
                return cls._decode_class(obj)

            if type_to_decode == TYPE.ITERATOR:
                return cls._decode_iterator(obj)

            if type_to_decode == TYPE.CODE:
                return cls._decode_code(obj)

            if type_to_decode == TYPE.OBJECT:
                return cls._decode_object(obj)

            if type_to_decode == TYPE.MODULE:
                return cls._decode_module(obj)

            if type_to_decode in (TYPE.TUPLE, TYPE.SET):
                return cls._decode_collection(obj)

        return obj

    @classmethod
    def _encode_bytes(cls, bytes_obj: bytes):
        data = base64.b64encode(bytes_obj).decode("ascii")
        return cls._mark_data(data, TYPE.BYTES)

    @classmethod
    def _decode_bytes(cls, encoded):
        return base64.b64decode(cls._get_data(encoded).encode("ascii"))

    @classmethod
    def _encode_module(cls, obj):
        return cls._mark_data(obj.__name__, TYPE.MODULE)

    @classmethod
    def _decode_module(cls, encoded):
        return __import__(cls._get_data(encoded))

    @classmethod
    def _encode_collection(cls, obj):
        data = [cls.encode(item) for item in obj]
        return cls._mark_data(data, type(obj).__name__.lower())

    @classmethod
    def _decode_collection(cls, obj):
        data = cls._get_data(obj)
        collection = getattr(builtins, cls._get_type(obj).lower())
        return collection((cls.decode(item) for item in data))

    @classmethod
    def _encode_code(cls, code):
        attrs = [attr for attr in dir(code) if attr.startswith("co")]

        code_dict = {
            attr: cls.encode(getattr(code, attr))
            for attr in attrs
            if attr not in UNSERIALIZABLE_CODE_TYPES
        }

        return cls._mark_data(code_dict, TYPE.CODE)

    @classmethod
    def _decode_code(cls, obj):
        data = cls._get_data(obj)

        def f():
            pass

        code_dict = cls.decode(data)

        return f.__code__.replace(**code_dict)

    @classmethod
    def _encode_function(cls, func):
        fcode = func.__code__
        fname = func.__name__
        fdefaults = func.__defaults__
        fdict = func.__dict__
        fclass = get_class_that_defined_method(func)
        fclosure = (
            tuple(cell for cell in func.__closure__ if cell.cell_contents is not fclass)
            if func.__closure__ is not None
            else tuple()
        )

        fglobs = {
            key: cls.encode(value)
            for (key, value) in func.__globals__.items()
            if key in func.__code__.co_names
            and value is not fclass
            and key != func.__code__.co_name
        }

        encoded_function = cls.encode(
            dict(
                code=fcode,
                name=fname,
                argdefs=fdefaults,
                closure=fclosure,
                fdict=fdict,
                globals=fglobs,
            )
        )

        return cls._mark_data(
            encoded_function,
            TYPE.FUNCTION,
            is_method=isinstance(func, types.MethodType),
        )

    @classmethod
    def _decode_function(cls, encoded):
        encoded_function = cls.decode(cls._get_data(encoded))

        fdict = encoded_function.pop("fdict")

        new_func = types.FunctionType(**encoded_function)
        new_func.__dict__.update(fdict)
        new_func.__globals__.update({new_func.__name__: new_func})
        return new_func

    @classmethod
    def _encode_cell(cls, obj):
        data = cls.encode(obj.cell_contents)
        return cls._mark_data(data, TYPE.CELL)

    @classmethod
    def _decode_cell(cls, obj):
        return cls._create_cell(cls.decode(cls._get_data(obj)))

    @classmethod
    def _encode_class(cls, obj):
        data = {
            attr: cls.encode(getattr(obj, attr))
            for attr, value in inspect.getmembers(obj)
            if attr not in UNSERIALIZABLE_DUNDER
            and type(value) not in UNSERIALIZABLE_TYPES
        }

        data["__bases__"] = [
            cls.encode(base) for base in obj.__bases__ if base != object
        ]

        data["__name__"] = obj.__name__

        return cls._mark_data(data, TYPE.CLASS)

    @classmethod
    def _decode_class(cls, obj):
        data = cls._get_data(obj)

        class_bases = tuple(cls.decode(base) for base in data.pop("__bases__"))
        class_dict = {
            attr: cls.decode(value)
            for (attr, value) in data.items()
            if not (isinstance(value, dict) and cls._get_type(value) == TYPE.FUNCTION)
        }

        result = type(data["__name__"], class_bases, class_dict)

        for key, value in data.items():
            if isinstance(value, dict) and cls._get_type(value) == TYPE.FUNCTION:
                try:
                    func = cls.decode(value)
                except ValueError:
                    closure = cls._get_data(value)["closure"]
                    cls._get_data(closure).append(cls._create_cell(result))
                    func = cls.decode(value)

                func.__globals__.update({result.__name__: result})

                if value.get("is_method"):
                    func = types.MethodType(func, result)

                setattr(result, key, func)

        return result

    @classmethod
    def _encode_iterator(cls, obj):
        data = list(map(cls.encode, obj))
        return cls._mark_data(data, TYPE.ITERATOR)

    @classmethod
    def _decode_iterator(cls, obj):
        data = cls._get_data(obj)
        return iter(cls.decode(value) for value in data)

    @classmethod
    def _encode_object(cls, obj):
        data = {
            "__class__": cls.encode(obj.__class__),
            "attrs": {
                attr: cls.encode(value)
                for (attr, value) in inspect.getmembers(obj)
                if not attr.startswith("__")
                and not isinstance(value, types.FunctionType)
                and not isinstance(value, types.MethodType)
            },
        }

        return cls._mark_data(data, TYPE.OBJECT)

    @classmethod
    def _decode_object(cls, obj):
        data = cls._get_data(obj)
        obj_class = cls.decode(data["__class__"])

        result = object.__new__(obj_class)
        result.__dict__ = {
            key: cls.decode(value) for key, value in data["attrs"].items()
        }

        return result

    @staticmethod
    def _mark_data(data, _type: TYPE, **additional_props):
        return dict(__type=_type, data=data, **additional_props)

    @staticmethod
    def _get_type(encoded):
        if isinstance(encoded, dict):
            return encoded.get("__type")

    @staticmethod
    def _get_data(encoded):
        if isinstance(encoded, dict):
            return encoded.get("data")

    @staticmethod
    def _create_cell(value):
        return (lambda: value).__closure__[0]
