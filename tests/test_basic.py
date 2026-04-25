from mylib.tablemodel import InRange, Rename, Field, TableValidator
from mylib.disktable import DiskTable
from typing import Annotated

class Student(TableValidator):
    name: Annotated[str, Field(Rename("ФИО"))]

    task1_points: Annotated[int, Field(Rename("Задача 1"), InRange(0, 100))]
    task2_points: Annotated[int, Field(Rename("Задача 2"), InRange(0, 100))]

with DiskTable(path="/tmp/test/table.xlsx", model=Student) as tbl:
    for student in tbl:
        student.task1_points //= 2