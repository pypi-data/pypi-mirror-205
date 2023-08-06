from __future__ import annotations

from struct import Struct
from typing import TYPE_CHECKING, List

from .models.command import CommandEnum
from .models.sensor import Sensor, SensorEnum

if TYPE_CHECKING:
    from serialroomba.controllers.serial import SerialController


class Controller:
    serial_controller: SerialController

    def __init__(self, serial_controller: SerialController) -> None:
        self.serial_controller = serial_controller

    def get_sensor_data(self, sensor: Sensor | SensorEnum) -> int | bool:
        returned_bytes = self.serial_controller.get_sensor_data(
            sensor.packet_id, sensor.data_type.number_of_bytes
        )
        return Struct(sensor.data_type.struct_format).unpack(returned_bytes)[0]

    def send_command(self, command: CommandEnum, data: List[int] | int = []):
        if isinstance(data, int):
            data = [data]
        struct_formats = [data_type.struct_format for data_type in command.data_types]
        self.serial_controller.send_command(
            command.serial_command, data, struct_formats
        )

    @staticmethod
    def check_bit_is_set(data: int, bit_number: int) -> bool:
        """Checks if a specific bit is set in an integer

        Args:
            data (int): Data to check
            bit_number (int): Bit number 0-indexed

        Returns:
            bool: Whether the bit is set or not
        """
        bit = 0b1 << bit_number
        return bool(data & bit)

    @staticmethod
    def validate_input_value(value: int, name: str, min_value: int, max_value: int):
        if value < min_value or value > max_value:
            raise ValueError(
                f"{name} must be between -500 and 500. Value provided: {value}"
            )
