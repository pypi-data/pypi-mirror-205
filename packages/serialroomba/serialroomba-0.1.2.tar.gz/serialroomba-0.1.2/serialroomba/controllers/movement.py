from .controller import Controller
from .models.command import Command, CommandEnum
from .models.sensor import Sensor, SensorEnum
from .serial import DataTypes, SerialController


class MovementCommand(CommandEnum):
    DRIVE = Command(
        "Drive", 137, [DataTypes.SIGNED_TWO_BYTES, DataTypes.SIGNED_TWO_BYTES]
    )
    DRIVE_DIRECT = Command(
        "Drive direct",
        145,
        [DataTypes.SIGNED_TWO_BYTES, DataTypes.SIGNED_TWO_BYTES],
    )
    DRIVE_PWM = Command(
        "Drive PWM", 146, [DataTypes.SIGNED_TWO_BYTES, DataTypes.SIGNED_TWO_BYTES]
    )


class MovementSensor(SensorEnum):
    DISTANCE = Sensor("Distance", 19, DataTypes.SIGNED_TWO_BYTES)
    ANGLE = Sensor("Angle", 20, DataTypes.SIGNED_TWO_BYTES)
    VELOCITY = Sensor("Velocity", 39, DataTypes.SIGNED_TWO_BYTES)
    RADIUS = Sensor("Radius", 40, DataTypes.SIGNED_TWO_BYTES)
    VELOCITY_RIGHT = Sensor("Velocity right", 41, DataTypes.SIGNED_TWO_BYTES)
    VELOCITY_LEFT = Sensor("Velocity left", 42, DataTypes.SIGNED_TWO_BYTES)
    ENCODER_COUNTS_LEFT = Sensor(
        "Encoder counts left", 43, DataTypes.UNSIGNED_TWO_BYTES
    )
    ENCODER_COUNTS_RIGHT = Sensor(
        "Encoder counts right", 44, DataTypes.UNSIGNED_TWO_BYTES
    )
    MOTOR_CURRENT_LEFT = Sensor("Motor current left", 54, DataTypes.SIGNED_TWO_BYTES)
    MOTOR_CURRENT_RIGHT = Sensor("Motor current right", 55, DataTypes.SIGNED_TWO_BYTES)
    STASIS = Sensor("Statis", 58, DataTypes.BOOL)


class MovementController(Controller):
    _last_set_pwm_left_wheel: int = 0
    _last_set_pwm_right_wheel: int = 0

    def __init__(
        self, serial_controller: SerialController, wheel_span_mm: float
    ) -> None:
        super().__init__(serial_controller)
        self._wheel_span_mm = wheel_span_mm

    @property
    def motor_left_current_mA(self) -> int:
        return self.get_sensor_data(MovementSensor.MOTOR_CURRENT_LEFT)

    @property
    def motor_right_current_mA(self) -> int:
        return self.get_sensor_data(MovementSensor.MOTOR_CURRENT_RIGHT)

    @property
    def is_moving(self) -> bool:
        return not self.get_sensor_data(MovementSensor.STASIS)  # type: ignore

    @property
    def velocity_total(self) -> int:
        return self.get_sensor_data(MovementSensor.VELOCITY)

    @velocity_total.setter
    def velocity_total(self, velocity: int) -> None:
        self.validate_input_value(velocity, "Velocity", -500, 500)
        self.send_command(
            MovementCommand.DRIVE,
            [
                velocity,
                self.radius,
            ],
        )

    @property
    def radius(self) -> int:
        return self.get_sensor_data(MovementSensor.RADIUS)

    @radius.setter
    def radius(self, radius: int) -> None:
        self.validate_input_value(radius, "Radius", -2000, 2000)
        self.send_command(
            MovementCommand.DRIVE,
            [
                self.velocity_total,
                radius,
            ],
        )

    @property
    def velocity_left_wheel(self) -> int:
        return self.get_sensor_data(MovementSensor.VELOCITY_LEFT)

    @velocity_left_wheel.setter
    def velocity_left_wheel(self, velocity: int) -> None:
        self.validate_input_value(velocity, "Velocity left wheel", -500, 500)
        self.send_command(
            MovementCommand.DRIVE_DIRECT,
            [
                self.velocity_right_wheel,
                velocity,
            ],
        )

    @property
    def velocity_right_wheel(self) -> int:
        return self.get_sensor_data(MovementSensor.VELOCITY_RIGHT)

    @velocity_right_wheel.setter
    def velocity_right_wheel(self, velocity: int) -> None:
        self.validate_input_value(velocity, "Velocity right wheel", -500, 500)
        self.send_command(
            MovementCommand.DRIVE_DIRECT,
            [
                velocity,
                self.velocity_left_wheel,
            ],
        )

    @property
    def pwm_left_wheel(self) -> int:
        """Last set left wheel PWM, the Roomba doesn't provide the current PWM"""
        return self._last_set_pwm_left_wheel

    @pwm_left_wheel.setter
    def pwm_left_wheel(self, pwm: int) -> None:
        self.validate_input_value(pwm, "PWM left wheel", -255, 255)
        self._last_set_pwm_left_wheel = pwm
        self.send_command(
            MovementCommand.DRIVE_PWM,
            [
                self.pwm_right_wheel,
                pwm,
            ],
        )

    @property
    def pwm_right_wheel(self) -> int:
        """Last set right wheel PWM, the Roomba doesn't provide the current PWM"""
        return self._last_set_pwm_left_wheel

    @pwm_right_wheel.setter
    def pwm_right_wheel(self, pwm: int) -> None:
        self.validate_input_value(pwm, "PWM right wheel", -255, 255)
        self._last_set_pwm_right_wheel = pwm
        self.send_command(
            MovementCommand.DRIVE_PWM,
            [
                pwm,
                self.pwm_left_wheel,
            ],
        )

    @property
    def distance_travelled(self) -> int:
        """Resets to 0 after being read.
        If the value is not polled frequently enough, it is capped at its minimum or maximum
        """
        return self.get_sensor_data(MovementSensor.DISTANCE)

    @property
    def angle_turned(self) -> int:
        """Resets to 0 after being read
        If the value is not polled frequently enough, it is capped at its minimum or maximum
        """
        return self.get_sensor_data(MovementSensor.ANGLE)

    @property
    def encoder_counts_left(self) -> int:
        """Will roll over to 0 after it passes 65535"""
        return self.get_sensor_data(MovementSensor.ENCODER_COUNTS_LEFT)

    @property
    def encoder_counts_right(self) -> int:
        """Will roll over to 0 after it passes 65535"""
        return self.get_sensor_data(MovementSensor.ENCODER_COUNTS_RIGHT)
