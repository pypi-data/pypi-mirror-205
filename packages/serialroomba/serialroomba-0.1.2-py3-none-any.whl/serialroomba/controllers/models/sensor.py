from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..serial import DataTypes
from .validator_enum import _ValidatorEnumMeta


class _SensorEnumMeta(_ValidatorEnumMeta):
    def __new__(cls, name, bases, classdict):
        cls._validate_types(classdict, desired_type=Sensor)
        return super().__new__(metacls=cls, cls=name, bases=bases, classdict=classdict)


@dataclass
class Sensor:
    name: str
    packet_id: int
    data_type: DataTypes


class SensorEnum(Enum, metaclass=_SensorEnumMeta):
    @property
    def name(self):
        return self.value.name

    @property
    def data_type(self):
        return self.value.data_type

    @property
    def packet_id(self):
        return self.value.packet_id
