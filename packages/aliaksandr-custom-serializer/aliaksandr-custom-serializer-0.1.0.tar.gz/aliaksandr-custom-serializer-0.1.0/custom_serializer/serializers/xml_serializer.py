from typing import IO

from .base_serializer import BaseSerializer


class XmlSerializer(BaseSerializer):
    @classmethod
    def dumps(cls, obj) -> str:
        if isinstance(obj, bool):
            return f"<bool>{str(obj)}</bool>"

        if isinstance(obj, int):
            return f"<int>{str(obj)}</int>"

        if isinstance(obj, float):
            return f"<float>{str(obj)}</float>"

        if isinstance(obj, str):
            return f"<str>{obj}</str>"

        if isinstance(obj, type(None)):
            return f"<none>None</none>"

        if isinstance(obj, (list, tuple)):
            return f"<list>{''.join(list(map(cls.dumps, obj)))}</list>"

        if isinstance(obj, dict):
            data = "".join(
                [f"<{key}>{cls.dumps(value)}</{key}>" for (key, value) in obj.items()]
            )
            return f"<dict>{data}</dict>"

    @classmethod
    def dump(cls, obj, fp: IO[str]) -> None:
        fp.write(cls.dumps(obj))

    @classmethod
    def loads(cls, s: str):
        res, _ = cls._loads(s, 0)
        return res

    @classmethod
    def load(cls, fp: IO[str]):
        return cls.loads(fp.read())

    @classmethod
    def _loads(
        cls, s: str, start_index: int
    ) -> tuple[bool | str | int | float | list | dict | None, int]:
        index = start_index

        if s[index] != "<":
            raise Exception(f"Invalid symbol at position {index}")

        type_start_index = index + 1
        type_end_index = index

        while s[type_end_index] != ">":
            type_end_index += 1

        object_type = s[type_start_index:type_end_index]
        method_name = f"_loads_{object_type}"

        if not hasattr(cls, method_name):
            raise Exception("Unknown type")

        index = type_end_index + 1
        return getattr(cls, method_name)(s, index)

    @classmethod
    def _loads_str(cls, s: str, start_index: int) -> tuple[str, int]:
        end_index = start_index
        while s[end_index : end_index + 6] != "</str>":
            end_index += 1

        return s[start_index:end_index], end_index + 6

    @classmethod
    def _loads_bool(cls, s: str, start_index: int) -> tuple[bool, int]:
        end_index = start_index
        while s[end_index : end_index + 7] != "</bool>":
            end_index += 1

        bool_obj = s[start_index:end_index]
        if bool_obj == "True":
            return True, end_index + 7
        else:
            return False, end_index + 7

    @classmethod
    def _loads_int(cls, s: str, start_index: int) -> tuple[int, int]:
        end_index = start_index
        while s[end_index : end_index + 6] != "</int>":
            end_index += 1

        int_obj = s[start_index:end_index]
        return int(int_obj), end_index + 6

    @classmethod
    def _loads_float(cls, s: str, start_index: int) -> tuple[float, int]:
        end_index = start_index
        while s[end_index : end_index + 8] != "</float>":
            end_index += 1

        int_obj = s[start_index:end_index]
        return float(int_obj), end_index + 8

    @classmethod
    def _loads_none(cls, s: str, start_index: int) -> tuple[type(None), int]:
        end_index = start_index
        while s[end_index : end_index + 7] != "</none>":
            end_index += 1

        return None, end_index + 7

    @classmethod
    def _loads_list(cls, s: str, start_index: int) -> tuple[list, int]:
        end_index = start_index
        deep = 1
        while deep:
            if s[end_index : end_index + 6] == "<list>":
                deep += 1
            if s[end_index : end_index + 7] == "</list>":
                deep -= 1

            end_index += 1

        end_index -= 1
        arr = []
        index = start_index
        while index < end_index:
            res, index = cls._loads(s, index)
            arr.append(res)

        return arr, end_index + 7

    @classmethod
    def _loads_dict(cls, s: str, start_index: int) -> tuple[dict, int]:
        end_index = start_index
        deep = 1
        while deep:
            if s[end_index : end_index + 6] == "<dict>":
                deep += 1
            if s[end_index : end_index + 7] == "</dict>":
                deep -= 1

            end_index += 1

        end_index -= 1

        index = start_index
        result = {}

        while index < end_index:
            ket_start_index = index + 1
            key_end_index = index + 1

            while s[key_end_index] != ">":
                key_end_index += 1

            key = s[ket_start_index:key_end_index]

            value, index = cls._loads(s, key_end_index + 1)
            index += 3 + len(key)

            result[key] = value

        return result, end_index + 7
