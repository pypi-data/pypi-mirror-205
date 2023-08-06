from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .validator_enum import _ValidatorEnumMeta


class _StateEnumMeta(_ValidatorEnumMeta):
    def __new__(cls, name, bases, classdict):
        cls._validate_types(classdict, desired_type=State)
        return super().__new__(metacls=cls, cls=name, bases=bases, classdict=classdict)


@dataclass
class State:
    name: str
    state_id: int


class StateEnum(Enum, metaclass=_StateEnumMeta):
    @property
    def name(self):
        return self.value.name

    @property
    def state_id(self):
        return self.value.state_id

    @classmethod
    def from_state_id(cls, state_id) -> StateEnum:
        for state in cls:
            if state.state_id == state_id:
                return cls(state)

        raise KeyError(f"State with ID {state_id} not defined")
