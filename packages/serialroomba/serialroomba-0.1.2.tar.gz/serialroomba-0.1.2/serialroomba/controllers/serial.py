from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from struct import Struct
from typing import List

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE, Serial, SerialException

from ..exceptions import RoombaConnectionError


class ControlCodes:
    SENSOR = 142


@dataclass
class _DataType:
    struct_format: str
    number_of_bytes: int


class DataTypes(Enum):
    UNSIGNED_BYTE = _DataType("B", 1)
    SIGNED_BYTE = _DataType("b", 1)
    UNSIGNED_TWO_BYTES = _DataType("H", 2)
    SIGNED_TWO_BYTES = _DataType("h", 2)
    BOOL = _DataType("?", 1)

    @property
    def struct_format(self):
        return self.value.struct_format

    @property
    def number_of_bytes(self):
        return self.value.number_of_bytes


class SerialController:
    connection = Serial()

    def __init__(self, port: str, baud_rate: int, time_out_s: float) -> None:
        self.connection.port = port
        self.connection.baudrate = baud_rate
        self.connection.timeout = time_out_s

        self._connect_serial()

    def _connect_serial(self) -> None:
        self.connection.bytesize = EIGHTBITS
        self.connection.parity = PARITY_NONE
        self.connection.stopbits = STOPBITS_ONE
        self.connection.xonxoff = False  # Flow control

        try:
            self.connection.open()
        except SerialException as exception:
            raise RoombaConnectionError(repr(exception)) from exception

        if not self.connection.is_open:
            raise RoombaConnectionError("Could not open the serial port")

    @staticmethod
    def _pack_data(
        command: int, data_bytes: List[int] = [], struct_formats: List[str] = []
    ):
        return Struct("B" + "".join(struct_formats)).pack(command, *data_bytes)

    def send_command(
        self,
        command: int,
        data: List[int] = [],
        struct_formats: List[str] = [],
    ):
        if len(data) != len(struct_formats):
            raise ValueError(
                f"The number of struct formats ({len(struct_formats)}) ",
                f"must match the number of data parts ({len(data)})",
            )
        command_and_data_bytes = self._pack_data(command, data, struct_formats)
        self.connection.write(command_and_data_bytes)

    def get_sensor_data(self, packet_id: int, number_of_bytes: int) -> bytes:
        self.send_command(ControlCodes.SENSOR, [packet_id], ["B"])
        return self.connection.read(number_of_bytes)
