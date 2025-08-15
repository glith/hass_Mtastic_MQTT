from homeassistant.components import sensor
from homeassistant.helpers.entity import EntityCategory

from .coordinator import BaseEntity
from .constants import DOMAIN

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_setup_entities):
    coordinator = entry.runtime_data
    async_setup_entities([
        _LastUpdate(coordinator),
        _TelemetryBattery(coordinator),
        _TelemetryVoltage(coordinator),
        _TelemetryAirtimelUtil(coordinator),
        _TelemetryChannelUtil(coordinator),
        _Neighbors(coordinator),
        _TelemetryTemperature(coordinator),
        _TelemetryRelativeHumidity(coordinator),
        _TelemetryBarometricPressure(coordinator),
        _TelemetryGasResistance(coordinator),
        _TelemetryLux(coordinator),
        _PowerChannel1Voltage(coordinator),
        _PowerChannel1Current(coordinator),
        _PowerChannel2Voltage(coordinator),
        _PowerChannel2Current(coordinator),
        _PowerChannel3Voltage(coordinator),
        _PowerChannel3Current(coordinator)
    ])

class _TelemetryBattery(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_battery_level", "Battery")
        self._attr_device_class = sensor.SensorDeviceClass.BATTERY
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "%"
        self._attr_entity_registry_enabled_default = False
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("device_metrics"):
            if (value := tel.get("battery_level")) > 0:
                return 100 if value > 100 else value
        return None

class _TelemetryVoltage(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_voltage", "Voltage")
        self._attr_device_class = sensor.SensorDeviceClass.VOLTAGE
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "V"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("device_metrics"):
            if (value := tel.get("voltage")) > 0:
                return value
        return None

class _TelemetryAirtimelUtil(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_air_util_tx", "Tx Airtime Utilization")
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "%"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False
        self._attr_icon = "mdi:cloud-percent"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("device_metrics"):
            if value := tel.get("air_util_tx"):
                return value
        return None

class _TelemetryChannelUtil(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_channel_utilization", "Channel Utilization")
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "%"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False
        self._attr_icon = "mdi:gauge"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("device_metrics"):
            if value := tel.get("channel_utilization"):
                return value
        return None

class _TelemetryChannelUtil(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_channel_utilization", "Channel Utilization")
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "%"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False
        self._attr_icon = "mdi:gauge"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("device_metrics"):
            if value := tel.get("channel_utilization"):
                return value
        return None

class _LastUpdate(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"last_update", "Last Update")

        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_class = sensor.SensorDeviceClass.TIMESTAMP

    @property
    def native_value(self):
        return self.coordinator.last_update

    @property
    def extra_state_attributes(self):
        result = dict()
        if pos := self.coordinator.data.get("nodeinfo"):
            for attr in ("id", "longname", "shortname"):
                if value := pos.get(attr):
                    result[attr] = value
        return result

class _Neighbors(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"nn_neighbors", "Neighbors Count")
        self._attr_state_class = "measurement"
        self._attr_suggested_display_precision = 0
        self._attr_entity_registry_enabled_default = False
        self._attr_icon = "mdi:map-marker-multiple-outline"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> float | None:
        if nn := self.coordinator.data.get("neighborinfo"):
            if (value := nn.get("neighbors_count")) >= 0:
                return value
        return None


class _TelemetryTemperature(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_temperature", "Temperature")
        self._attr_device_class = sensor.SensorDeviceClass.TEMPERATURE
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "°C"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("environment_metrics"):
            if (value := tel.get("temperature")) > 0:
                return value
        return None


class _TelemetryRelativeHumidity(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_relativehumidity", "Relative Humidity")
        self._attr_device_class = sensor.SensorDeviceClass.HUMIDITY
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "%"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("environment_metrics"):
            if (value := tel.get("relative_humidity")) > 0:
                return value
        return None


class _TelemetryBarometricPressure(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_barometric_pressure", "Barometric Pressure")
        self._attr_device_class = sensor.SensorDeviceClass.ATMOSPHERIC_PRESSURE
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "hPa"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("environment_metrics"):
            if (value := tel.get("barometric_pressure")) > 0:
                return value
        return None

class _TelemetryGasResistance(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_gas_resistance", "Gas Resistance (AQI)")
        self._attr_device_class = sensor.SensorDeviceClass.AQI
        self._attr_state_class = "measurement"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("environment_metrics"):
            if (value := tel.get("gas_resistance")) > 0:
                return value
        return None

class _TelemetryLux(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"tel_lux", "Illuminance")
        self._attr_device_class = sensor.SensorDeviceClass.ILLUMINANCE
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "lx"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("environment_metrics"):
            if (value := tel.get("lux")) > 0:
                return value
        return None
        
class _PowerChannel1Voltage(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"power_ch1_voltage", "Channel 1 Voltage")
        self._attr_device_class = sensor.SensorDeviceClass.VOLTAGE
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "V"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("power_metrics"):
            if (value := tel.get("ch1_voltage")) > 0:
                return value
        return None
        
class _PowerChannel1Current(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"power_ch1_current", "Channel 1 Current")
        self._attr_device_class = sensor.SensorDeviceClass.CURRENT
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "mA"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("power_metrics"):
            if (value := tel.get("ch1_current")) > 0:
                return value
        return None

class _PowerChannel2Voltage(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"power_ch2_voltage", "Channel 2 Voltage")
        self._attr_device_class = sensor.SensorDeviceClass.VOLTAGE
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "V"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("power_metrics"):
            if (value := tel.get("ch2_voltage")) > 0:
                return value
        return None
        
class _PowerChannel2Current(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"power_ch2_current", "Channel 2 Current")
        self._attr_device_class = sensor.SensorDeviceClass.CURRENT
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "mA"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("power_metrics"):
            if (value := tel.get("ch2_current")) > 0:
                return value
        return None
        
class _PowerChannel3Voltage(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"power_ch3_voltage", "Channel 3 Voltage")
        self._attr_device_class = sensor.SensorDeviceClass.VOLTAGE
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "V"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("power_metrics"):
            if (value := tel.get("ch3_voltage")) > 0:
                return value
        return None
        
class _PowerChannel3Current(BaseEntity, sensor.SensorEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.with_name(f"power_ch3_current", "Channel 3 Current")
        self._attr_device_class = sensor.SensorDeviceClass.CURRENT
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "mA"
        self._attr_suggested_display_precision = 1
        self._attr_entity_registry_enabled_default = False

    @property
    def native_value(self) -> float | None:
        if tel := self.coordinator.data.get("power_metrics"):
            if (value := tel.get("ch3_current")) > 0:
                return value
        return None
