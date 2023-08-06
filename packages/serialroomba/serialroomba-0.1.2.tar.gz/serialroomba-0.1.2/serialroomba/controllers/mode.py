from __future__ import annotations

from serialroomba.controllers.models.sensor import Sensor

from .controller import Controller
from .models.command import Command, CommandEnum
from .models.state import State, StateEnum
from .serial import DataTypes


class Mode(CommandEnum):
    FULL = Command("Full", 132)
    PASSIVE = Command("Passive", 128)
    SAFE = Command("Safe", 131)


class ModeState(StateEnum):
    OFF = State("Off", 0)
    FULL = State("Full", 3)
    PASSIVE = State("Passive", 1)
    SAFE = State("Safe", 2)


MODE_SENSOR = Sensor("Mode", 35, DataTypes.UNSIGNED_BYTE)


class ModeController(Controller):
    @property
    def current_mode(self) -> StateEnum:
        state_id = self.get_sensor_data(MODE_SENSOR)
        return ModeState.from_state_id(state_id)

    @current_mode.setter
    def current_mode(self, mode: Mode) -> None:
        self.send_command(mode)
