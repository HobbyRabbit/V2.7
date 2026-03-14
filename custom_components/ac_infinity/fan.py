from homeassistant.components.fan import FanEntity

from .const import DOMAIN, DEVICE_TYPE_OUTLET


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for port in range(1,9):

        device_type = coordinator.data["ports"][port]["device_type"]

        if device_type not in DEVICE_TYPE_OUTLET:

            entities.append(
                ACInfinityFan(coordinator, port)
            )

    async_add_entities(entities)


class ACInfinityFan(FanEntity):

    def __init__(self, coordinator, port):

        self.coordinator = coordinator
        self.port = port

        self._attr_name = f"AC Infinity Fan {port}"

    @property
    def percentage(self):

        return self.coordinator.data["ports"][self.port]["speed"]

    async def async_set_percentage(self, percentage):

        await self.coordinator.set_speed(
            self.port,
            percentage
        )
