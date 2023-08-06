from typing import IO

from .base_serializer import BaseSerializer


class JsonSerializer(BaseSerializer):
    @classmethod
    def dumps(cls, obj) -> str:
        if isinstance(obj, bool):
            return str(obj).lower()

        if isinstance(obj, (int, float)):
            return str(obj)

        if isinstance(obj, str):
            return f'"{obj}"'

        if isinstance(obj, type(None)):
            return "null"

        if isinstance(obj, (list, tuple)):
            return f"[{','.join(list(map(cls.dumps, obj)))}]"

        if isinstance(obj, dict):
            data = ",".join(
                [f'"{key}": {cls.dumps(value)}' for (key, value) in obj.items()]
            )
            return f"""{{{data}}}"""

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
        if s[start_index] == '"':
            return cls._loads_str(s, start_index)
        if s[start_index] == "[":
            return cls._loads_list(s, start_index)

        if s[start_index].isdigit():
            return cls._loads_num(s, start_index)

        if s[start_index] == "t":
            return True, start_index + 4

        if s[start_index] == "f":
            return False, start_index + 5

        if s[start_index] == "n":
            return None, start_index + 4

        if s[start_index] == "{":
            return cls._loads_dict(s, start_index)

    @classmethod
    def _loads_list(cls, s: str, start_index: int) -> tuple[list, int]:
        end_index = start_index + 1
        braces = 1
        while braces:
            if s[end_index] == "[":
                braces += 1
            if s[end_index] == "]":
                braces -= 1

            end_index += 1

        arr = []
        index = start_index + 1
        while index < end_index - 2:
            while s[index] in (" ", ",", "\n"):
                index += 1
            res, index = cls._loads(s, index)
            arr.append(res)

        return arr, end_index

    @classmethod
    def _loads_dict(cls, s: str, start_index: int) -> tuple[dict, int]:
        end_index = start_index + 1
        braces = 1
        while braces:
            if s[end_index] == "{":
                braces += 1
            if s[end_index] == "}":
                braces -= 1

            end_index += 1

        index = start_index + 1
        result = {}
        while index < end_index - 2:
            while s[index] in (" ", ",", "\n"):
                index += 1
            key, index = cls._loads_str(s, index)

            while s[index] in (" ", ",", "\n", ":"):
                index += 1

            value, index = cls._loads(s, index)
            result[key] = value

        return result, end_index + 1

    @classmethod
    def _loads_str(cls, s: str, start_index: int) -> tuple[str, int]:
        end_index = start_index + 1
        while s[end_index] != '"':
            end_index += 1

        return s[start_index + 1 : end_index], end_index + 1

    @classmethod
    def _loads_num(cls, s: str, start_index: int) -> tuple[int | float, int]:
        end_index = start_index + 1
        while len(s) > end_index and (s[end_index].isdigit() or s[end_index] == "."):
            end_index += 1

        num = s[start_index:end_index]

        if num.count("."):
            return float(num), end_index

        return int(num), end_index
