from .controllers import (
    CleaningController,
    EnvironmentController,
    Mode,
    ModeController,
    MovementController,
    PowerController,
    SerialController,
)


class SerialRoomba:
    def __init__(
        self,
        port: str,
        baud_rate: int = 115200,
        time_out_s: float = 1.0,
        wheel_span_mm: float = 235.0,
    ):
        self.serial_controller = SerialController(
            port=port, baud_rate=baud_rate, time_out_s=time_out_s
        )

        self.mode_controller = ModeController(self.serial_controller)
        self.cleaning_controller = CleaningController(self.serial_controller)
        self.movement_controller = MovementController(
            self.serial_controller, wheel_span_mm=wheel_span_mm
        )
        self.power_controller = PowerController(self.serial_controller)
        self.environment_controller = EnvironmentController(self.serial_controller)

        self.mode_controller.current_mode = Mode.PASSIVE
