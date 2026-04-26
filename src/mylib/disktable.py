from types import TracebackType
from typing import Type, Iterator
from mylib._internal.table_serializing import xlsx_to_matrix, matrix_to_xlsx
from mylib.common.exception import MylibException


class DiskTable[Model]:
    path: str
    table: list[Model]
    model: Type[Model]

    @staticmethod
    def _validate(obj: Model) -> None:
        for field_name, field_descriptor in getattr(self.model, '_ fields metadata').items():
            value = getattr(obj, field_name)
            for valor in field_descriptor.validators:
                valor(value)
        

    def __init__(self, path: str, model: Type[Model]):
        self.path = path
        self.table = []
        self.model = model

    def __enter__(self) -> list[Model]:
        mat = xlsx_to_matrix(path=self.path)

        headers: list[str] = [str(h) if h is not None else "" for h in mat[0]]

        header_to_field = {}
        field_to_header = {}

        # build header <-> field name mapping
        for field_name, field_descriptor in getattr(self.model, '_ fields metadata').items():
            header_name = field_descriptor.renamer.header(field_name)
            header_to_field[header_name] = field_name
            field_to_header[field_name] = header_name

        # fill list
        for row in mat[1:]:
            instance = self.model()
            for col_idx, header in enumerate(headers):
                if col_idx < len(row) and header in header_to_field:
                    field_name = header_to_field[header]
                    value = row[col_idx]
                    setattr(instance, field_name, value)
            self._validate(instance)
            self.table.append(instance)


        return self.table

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None,) -> None:
        if exc_type is not None:
            return
        
        headers = []
        field_names = []

        for field_name, field_descriptor in getattr(self.model, '_ fields metadata').items():
            header_name = field_descriptor.renamer.header(field_name)
            headers.append(header_name)
            field_names.append(field_name)

        # build matrix
        matrix = [headers]
        for instance in self.table:
            self._validate(instance)
            row = []
            for field_name in field_names:
                value = getattr(instance, field_name, None)
                row.append(value)
            matrix.append(row)

        # dump
        matrix_to_xlsx(self.path, matrix)

    def __iter__(self) -> Iterator[Model]:
        return iter(self.table)