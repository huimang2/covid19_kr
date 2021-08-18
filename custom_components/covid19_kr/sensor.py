"""Sensor platform for the Corona virus."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import get_coordinator
from .const import DOMAIN, BRAND, MODEL, ATTRIBUTION, SW_VERSION, SENSORS


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Defer sensor setup to the shared sensor module."""

    coordinator = await get_coordinator(hass, config_entry)

    city = config_entry.data.get("city")
    
    async_add_entities(
        CoronavirusSensor(coordinator, config_entry, info_type)
        for info_type in SENSORS
        if info_type in coordinator.data
    )


class CoronavirusSensor(CoordinatorEntity, SensorEntity):
    """Sensor representing corona virus data."""

    _attr_unit_of_measurement = "명"

    def __init__(self, coordinator, config_entry, info_type):
        """Initialize coronavirus sensor."""
        super().__init__(coordinator)

        self.city = config_entry.data.get("city")
        self.info_type = info_type

        self._attr_extra_state_attributes = {ATTR_ATTRIBUTION: ATTRIBUTION}
        self._attr_icon = SENSORS[info_type]
        self._attr_unique_id = f"{self.city}-{info_type}"
        self._attr_name = f"{self.city} 코로나 {info_type}"

    @property
    def device_info(self):
        """Return device registry information for this entity."""
        return {
            "connections": {(self.city, self.unique_id)},
            "identifiers": {
                (
                    DOMAIN,
                    self.city,
                )
            },
            "manufacturer": BRAND,
            "model": f"{MODEL} {SW_VERSION}",
            "name": f"{self.city} 확진자 현황",
            "sw_version": SW_VERSION,
            "via_device": (DOMAIN, self.city),
            "entry_type": "service",
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data[self.info_type]

    @property
    def extra_state_attributes(self):
        """Return device specific state attributes."""

        attr = self.coordinator.data.get("attribute", {})
        attr = {x: attr[x] for x in attr if x and x not in SENSORS or x == self.info_type}

        if self.info_type in attr:
            _attr = attr.pop(self.info_type)
            _attr.update(attr)
            attr = _attr

        return attr
