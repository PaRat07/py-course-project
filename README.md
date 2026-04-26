# Проект для курса Python "Бибилиотека для работы с excel таблицами"

### План фичей (1 этап)
- Описание структуры таблицы в терминах объектной модели Python
- Валидация таблицы (на основе Pydantic-like синтаксиса)

Пример описания структуры таблицы
```py
TaskPoints = lib.InRange(0, 100)

class Student(TableValidator):
    @alias("ФИО")
    name: str

    @alias("Задача 1")
    task1_points: TaskPoints

    @alias("Задача 2")
    task2_points: TaskPoints

with DiskTable(path="...", model=Student) as tbl:
    for student in tbl:
        student.task1_points //= 2
```

### Идеи фичей для 2й итерации
- Асинхронное взаимодействие с google docs таблицами (через async with GoogleTable(...) as tbl)
- Способ описания миграций между схемами (пример - добавление задачи)

Используемые бибилотеки
- openpyxl (для работы с файлами таблиц)
- pydrive2 (для работы с google docs)

