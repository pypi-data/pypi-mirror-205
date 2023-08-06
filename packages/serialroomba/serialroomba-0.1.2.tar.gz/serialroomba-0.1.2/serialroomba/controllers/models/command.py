from dataclasses import dataclass, field
from enum import Enum
from typing import List

from serialroomba.controllers.serial import DataTypes

from .validator_enum import _ValidatorEnumMeta


class _CommandEnumMeta(_ValidatorEnumMeta):
    def __new__(cls, name, bases, classdict):
        cls._validate_types(classdict, desired_type=Command)
        return super().__new__(metacls=cls, cls=name, bases=bases, classdict=classdict)


@dataclass
class Command:
    name: str
    serial_command: int
    data_types: List[DataTypes] | DataTypes | None = field(default_factory=list)


class CommandEnum(Enum, metaclass=_CommandEnumMeta):
    @property
    def name(self):
        return self.value.name

    @property
    def serial_command(self):
        return self.value.serial_command

    @property
    def data_types(self):
        return self.value.data_types
