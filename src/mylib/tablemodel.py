from mylib.common import exception as mylib_exc
from typing import Protocol, Dict, Any


class ValidationError(mylib_exc.MylibException): ...

class InRange:
    min_value: int | float
    max_value: int | float

    def __init__(self, min_value: int | float, max_value: int | float):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int | float) -> None:
        if value < self.min_value or self.max_value < value:
            raise ValidationError(f"Value {value} is out of range [{self.min_value}, {self.max_value}]")



class Rename:
    new_name: str

    def __init__(self, new_name: str):
        self.new_name = new_name

    def header(self, _: str) -> str:
        return self.new_name

class Renamer(Protocol):
    def header(self, old_header: str) -> str: ...

class Validator[T](Protocol):
    def validate(self, value: T) -> None: ...







class Field[T]:
    renamer: Renamer | None
    validators: list[Validator[T]]
    name: str
    
    def __init__(self, *annotations) -> None:
        renamer: Renamer | None = None
        self.validators = []
        for annot in annotations:
            usable = False
            if hasattr(annot, "header"):
                if renamer is not None:
                    raise TypeError(f"Field has multiple renamers ({renamer} and {annot})")
                renamer = annot
                usable = True

            if hasattr(annot, "validate"):
                self.validators.append(annot)
                usable = True

            if not usable:
                raise TypeError(f"Field annotation {annot} is not valid")
        self.renamer = renamer

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, f"_{self.name}", None)

    def __set__(self, instance, value):
        for validator in self.validators:
            validator.validate(value)
        setattr(instance, f"_{self.name}", value)


class TableValidatorMeta(type):
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: Dict[str, Any]):
        fields = {}
        annotations: Dict[str, type] = attrs.get('__annotations__', {})
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = annotations[attr_name]()
        attrs['__fields__'] = fields
        return super().__new__(mcs, name, bases, attrs)

class TableValidator(metaclass=TableValidatorMeta): ...
