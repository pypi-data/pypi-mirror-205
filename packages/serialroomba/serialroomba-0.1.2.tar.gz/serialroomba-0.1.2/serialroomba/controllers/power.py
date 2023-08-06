from serialroomba.controllers.controller import Controller
from serialroomba.controllers.serial import DataTypes
from serialroomba.controllers.models.state import State, StateEnum
from .models.sensor import Sensor


class PowerSensors:
    BATTERY_CAPACITY = Sensor("Battery capacity", 26, DataTypes.UNSIGNED_TWO_BYTES)
    BATTERY_CHARGE = Sensor("Battery charge", 25, DataTypes.UNSIGNED_TWO_BYTES)
    BATTERY_TEMPERATURE = Sensor("Batery temperature", 24, DataTypes.SIGNED_BYTE)
    CHARGING_STATE = Sensor("Charging state", 21, DataTypes.UNSIGNED_BYTE)
    CURRENT = Sensor("Current", 23, DataTypes.SIGNED_TWO_BYTES)
    VOLTAGE = Sensor("Voltage", 22, DataTypes.UNSIGNED_TWO_BYTES)
    CHARGER_AVAILABLE = Sensor("Charger available", 34, DataTypes.UNSIGNED_BYTE)


class ChargingState(StateEnum):
    NOT_CHARGING = State("Not charging", 0)
    RECONDITIONING_CHARGING = State("Reconditioning charging", 1)
    FULL_CHARGING = State("Full charging", 2)
    TRICKLE_CHARGING = State("Trickle charging", 3)
    WAITING = State("Waiting", 4)
    CHARGING_FAULT_CONDITION = State("Waiting", 5)


class PowerController(Controller):
    @property
    def battery_voltage_mV(self) -> int:
        return self.get_sensor_data(PowerSensors.VOLTAGE)

    @property
    def battery_current_mA(self) -> int:
        return self.get_sensor_data(PowerSensors.CURRENT)

    @property
    def battery_charge_mAh(self) -> int:
        return self.get_sensor_data(PowerSensors.BATTERY_CHARGE)

    @property
    def battery_capacity_mAh(self) -> int:
        return self.get_sensor_data(PowerSensors.BATTERY_CAPACITY)

    @property
    def battery_temperature_deg_C(self) -> int:
        return self.get_sensor_data(PowerSensors.BATTERY_TEMPERATURE)

    @property
    def battery_charging_state(self) -> StateEnum:
        charging_state_id = self.get_sensor_data(PowerSensors.CHARGING_STATE)
        return ChargingState.from_state_id(charging_state_id)

    @property
    def battery_is_charging(self) -> bool:
        charging_state = self.get_sensor_data(PowerSensors.CHARGING_STATE)
        if charging_state in [
            ChargingState.NOT_CHARGING.state_id,
            ChargingState.CHARGING_FAULT_CONDITION.state_id,
        ]:
            return False
        return True

    @property
    def internal_charger_available(self) -> bool:
        data = self.get_sensor_data(PowerSensors.CHARGER_AVAILABLE)
        return self.check_bit_is_set(data, 0)

    @property
    def base_charger_available(self) -> bool:
        data = self.get_sensor_data(PowerSensors.CHARGER_AVAILABLE)
        return self.check_bit_is_set(data, 1)
