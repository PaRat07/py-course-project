from mylib.tablemodel import InRange, Rename, Field, TableValidator
from mylib.disktable import DiskTable

class Student(TableValidator):
    name: str = Field(Rename("ФИО"))

    task1_points: int = Field(Rename("Задача 1"), InRange(0, 100))
    task2_points: int = Field(Rename("Задача 2"), InRange(0, 100))

with DiskTable(path="/tmp/test/test.xlsx", model=Student) as tbl:
    for student in tbl:
        student.task1_points //= 2

print('Succeed')