from __future__ import annotations

from .controller import Controller
from .serial import DataTypes
from .models.sensor import Sensor, SensorEnum
from enum import Enum


class EnvironmentSensors(SensorEnum):
    BUMPS_AND_WHEEL_DROP_FLAGS = Sensor(
        "Bumps and wheel drop flags", 7, DataTypes.UNSIGNED_BYTE
    )
    WALL_FLAG = Sensor("Wall flag", 8, DataTypes.BOOL)
    CLIFF_LEFT_FLAG = Sensor("Cliff Left flag", 9, DataTypes.BOOL)
    CLIFF_FRONT_LEFT_FLAG = Sensor("Cliff Front Left flag", 10, DataTypes.BOOL)
    CLIFF_FRONT_RIGHT_FLAG = Sensor("Cliff Front Right flag", 11, DataTypes.BOOL)
    CLIFF_RIGHT_FLAG = Sensor("Cliff Right flag", 12, DataTypes.BOOL)
    VIRTUAL_WALL_FLAG = Sensor("Virtual wall flag", 13, DataTypes.BOOL)
    WALL_SIGNAL = Sensor("Wall signal", 27, DataTypes.UNSIGNED_TWO_BYTES)
    CLIFF_LEFT_SIGNAL = Sensor("Cliff Left signal", 28, DataTypes.UNSIGNED_TWO_BYTES)
    CLIFF_FRONT_LEFT_SIGNAL = Sensor(
        "Cliff Front Left signal", 29, DataTypes.UNSIGNED_TWO_BYTES
    )
    CLIFF_FRONT_RIGHT_SIGNAL = Sensor(
        "Cliff Front Right signal", 30, DataTypes.UNSIGNED_TWO_BYTES
    )
    CLIFF_RIGHT_SIGNAL = Sensor("Cliff Right signal", 31, DataTypes.UNSIGNED_TWO_BYTES)
    LIGHT_BUMPER_FLAGS = Sensor("Light bumper flags", 45, DataTypes.UNSIGNED_BYTE)
    LIGHT_BUMPER_LEFT_SIGNAL = Sensor(
        "Light bumper Left signal", 46, DataTypes.UNSIGNED_TWO_BYTES
    )
    LIGHT_BUMPER_FRONT_LEFT_SIGNAL = Sensor(
        "Light bumper Front Left signal", 47, DataTypes.UNSIGNED_TWO_BYTES
    )
    LIGHT_BUMPER_CENTER_LEFT_SIGNAL = Sensor(
        "Light bumper Center Left signal", 48, DataTypes.UNSIGNED_TWO_BYTES
    )
    LIGHT_BUMPER_CENTER_RIGHT_SIGNAL = Sensor(
        "Light bumper Center Right signal", 49, DataTypes.UNSIGNED_TWO_BYTES
    )
    LIGHT_BUMPER_FRONT_RIGHT_SIGNAL = Sensor(
        "Light bumper Front Right signal", 50, DataTypes.UNSIGNED_TWO_BYTES
    )
    LIGHT_BUMPER_RIGHT_SIGNAL = Sensor(
        "Light bumper Right signal", 51, DataTypes.UNSIGNED_TWO_BYTES
    )
    INFRARED_OPCODE_LEFT = Sensor("Infrared opcode Left", 52, DataTypes.UNSIGNED_BYTE)
    INFRARED_OPCODE_RIGHT = Sensor("Infrared opcode Right", 52, DataTypes.UNSIGNED_BYTE)


class InfraredOpCodes(Enum):
    IR_REMOTE_LEFT = 129
    IR_REMOTE_FORWARD = 130
    IR_REMOTE_RIGHT = 131
    IR_REMOTE_SPOT = 132
    IR_REMOTE_MAX = 133
    IR_REMOTE_SMALL = 134
    IR_REMOTE_MEDIUM = 135
    IR_REMOTE_LARGE_OR_CLEAN = 136
    IR_REMOTE_STOP = 137
    IR_REMOTE_POWER = 138
    IR_REMOTE_ARC_LEFT = 139
    IR_REMOTE_ARC_RIGH = 140
    IR_REMOTE_STOP2 = 141
    SCHEDULING_REMOTE_DOWNLOAD = 142
    SCHEDULING_REMOTE_SEEK_DOCK = 143
    DOCK_RESERVED = 160
    DOCK_FORCE_FIELD = 161
    DOCK_GREEN_BUOY = 164
    DOCK_GREEN_BUOY_AND_FORCE_FIELD = 165
    DOCK_RED_BUOY = 168
    DOCK_RED_BUOY_AND_FORCE_FIELD = 169
    DOCK_RED_BUOY_AND_GREEN_BUOY = 172
    DOCK_RED_BUOY_AND_GREEN_BUOY_AND_FORCE_FIELD = 173


class EnvironmentController(Controller):
    @property
    def wall_detected(self) -> bool:
        return self.get_sensor_data(EnvironmentSensors.WALL_FLAG)  # type: ignore

    @property
    def cliff_left_detected(self) -> bool:
        return self.get_sensor_data(EnvironmentSensors.CLIFF_LEFT_FLAG)  # type: ignore

    @property
    def cliff_front_left_detected(self) -> bool:
        return self.get_sensor_data(EnvironmentSensors.CLIFF_FRONT_LEFT_FLAG)  # type: ignore

    @property
    def cliff_front_right_detected(self) -> bool:
        return self.get_sensor_data(EnvironmentSensors.CLIFF_FRONT_RIGHT_FLAG)  # type: ignore

    @property
    def cliff_right_detected(self) -> bool:
        return self.get_sensor_data(EnvironmentSensors.CLIFF_RIGHT_FLAG)  # type: ignore

    @property
    def virtual_wall_detected(self) -> bool:
        return self.get_sensor_data(EnvironmentSensors.VIRTUAL_WALL_FLAG)  # type: ignore

    @property
    def wall_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.WALL_SIGNAL)

    @property
    def cliff_left_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.CLIFF_LEFT_SIGNAL)

    @property
    def cliff_front_left_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.CLIFF_FRONT_LEFT_SIGNAL)

    @property
    def cliff_front_right_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.CLIFF_FRONT_RIGHT_SIGNAL)

    @property
    def cliff_right_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.CLIFF_RIGHT_SIGNAL)

    @property
    def light_bumper_left_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_LEFT_SIGNAL)

    @property
    def light_bumper_front_left_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_FRONT_LEFT_SIGNAL)

    @property
    def light_bumper_center_left_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_CENTER_LEFT_SIGNAL)

    @property
    def light_bumper_center_right_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_CENTER_RIGHT_SIGNAL)

    @property
    def light_bumper_front_right_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_FRONT_RIGHT_SIGNAL)

    @property
    def light_bumper_right_signal(self) -> int:
        return self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_RIGHT_SIGNAL)

    @property
    def light_bumper_left_detected(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_FLAGS)
        return self.check_bit_is_set(data, 0)

    @property
    def light_bumper_front_left_detected(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_FLAGS)
        return self.check_bit_is_set(data, 1)

    @property
    def light_bumper_center_left_detected(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_FLAGS)
        return self.check_bit_is_set(data, 2)

    @property
    def light_bumper_center_right_detected(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_FLAGS)
        return self.check_bit_is_set(data, 3)

    @property
    def light_bumper_front_right_detected(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_FLAGS)
        return self.check_bit_is_set(data, 4)

    @property
    def light_bumper_right_detected(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.LIGHT_BUMPER_FLAGS)
        return self.check_bit_is_set(data, 5)

    @property
    def infrared_opcode_left(self) -> InfraredOpCodes:
        opcode = self.get_sensor_data(EnvironmentSensors.INFRARED_OPCODE_LEFT)
        return InfraredOpCodes(opcode)

    @property
    def infrared_opcode_right(self) -> InfraredOpCodes:
        opcode = self.get_sensor_data(EnvironmentSensors.INFRARED_OPCODE_RIGHT)
        return InfraredOpCodes(opcode)

    @property
    def bumper_left_activate(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.BUMPS_AND_WHEEL_DROP_FLAGS)
        return self.check_bit_is_set(data, 1)

    @property
    def bumper_right_activate(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.BUMPS_AND_WHEEL_DROP_FLAGS)
        return self.check_bit_is_set(data, 0)

    @property
    def wheel_left_dropped(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.BUMPS_AND_WHEEL_DROP_FLAGS)
        return self.check_bit_is_set(data, 3)

    @property
    def wheel_right_dropped(self) -> bool:
        data = self.get_sensor_data(EnvironmentSensors.BUMPS_AND_WHEEL_DROP_FLAGS)
        return self.check_bit_is_set(data, 2)
