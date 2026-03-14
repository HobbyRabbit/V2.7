import logging
from datetime import timedelta

from bleak import BleakClient
from bleak_retry_connector import establish_connection

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.components.bluetooth import async_ble_device_from_address

from .const import (
    PORT_COUNT,
    UPDATE_INTERVAL,
    DEFAULT_PORT_STATE,
)

_LOGGER = logging.getLogger(__name__)


class ACInfinityCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, mac, name):

        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

        self.mac = mac
        self.client = None

        self.data = {
            "ports": {
                p: DEFAULT_PORT_STATE.copy()
                for p in range(1, PORT_COUNT + 1)
            }
        }

    async def _ensure_connected(self):

        if self.client and self.client.is_connected:
            return

        device = async_ble_device_from_address(
            self.hass,
            self.mac,
        )

        if not device:
            raise UpdateFailed("BLE device not found")

        self.client = await establish_connection(
            BleakClient,
            device,
            self.name,
        )

    async def set_port(self, port, state):

        _LOGGER.debug("Set port %s -> %s", port, state)

        self.data["ports"][port]["power"] = state

        self.async_set_updated_data(self.data)

    async def set_speed(self, port, speed):

        _LOGGER.debug("Set speed %s -> %s", port, speed)

        self.data["ports"][port]["speed"] = speed

        self.async_set_updated_data(self.data)

    async def _async_update_data(self):

        await self._ensure_connected()

        return self.data
