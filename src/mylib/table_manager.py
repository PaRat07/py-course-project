from types import TracebackType
from typing import Type, Iterator, Any, Generator, AsyncGenerator

from mylib._internal.model_serializer import Serialize, Deserialize
from mylib._internal.table_serializing import xlsx_to_matrix, matrix_to_xlsx
from mylib._internal.table_syncronization import gdoc_table_to_matrix, matrix_to_gdoc_table
from mylib.common.exception import MylibException
from contextlib import contextmanager, asynccontextmanager
from dataclasses import dataclass


@contextmanager
def DiskTable[Model](path: str, model: Type[Model]) -> Generator[list[Model], None, None]:
    input_mat = xlsx_to_matrix(path=path)
    result_table = Deserialize(mat=input_mat, model=model)
    yield result_table
    res_mat = Serialize(model=model, table=result_table)
    matrix_to_xlsx(path=path, matrix=res_mat)


@contextmanager
def GdocTable[Model](
            spreadsheet_id: str,
            credentials_path: str,
            model: Type[Model],
        ) -> Generator[list[Model], None, None]:
    input_mat = gdoc_table_to_matrix(spreadsheet_id=spreadsheet_id, credentials_path=credentials_path)
    result_table = Deserialize(mat=input_mat, model=model)
    yield result_table
    res_mat = Serialize(model=model, table=result_table)
    matrix_to_gdoc_table(spreadsheet_id=spreadsheet_id, credentials_path=credentials_path, matrix=res_mat)
