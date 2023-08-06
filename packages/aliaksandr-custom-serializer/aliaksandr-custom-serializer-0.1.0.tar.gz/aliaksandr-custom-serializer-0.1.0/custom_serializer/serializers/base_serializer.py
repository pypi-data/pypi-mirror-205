from abc import abstractmethod
from typing import IO


class BaseSerializer:
    @staticmethod
    @abstractmethod
    def dumps(obj) -> str:
        pass

    @staticmethod
    @abstractmethod
    def dump(obj, fp: IO[str]) -> None:
        pass

    @staticmethod
    @abstractmethod
    def loads(s: str) -> object:
        pass

    @staticmethod
    @abstractmethod
    def load(fp: IO[str]) -> object:
        pass
