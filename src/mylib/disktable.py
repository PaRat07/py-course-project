from types import TracebackType
from typing import Type, Iterator


class DiskTable[Model]:
    path: str
    table: list[Model]

    def __init__(self, path: str, model: Type[Model]):
        self.path = path
        self.table = []

    def __enter__(self) -> "DiskTable[Model]":
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None,) -> None:
        pass

    def __iter__(self) -> Iterator[Model]:
        return iter(self.table)