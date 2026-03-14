from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_MAC

from .const import DOMAIN
from .coordinator import ACInfinityCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):

    mac = entry.data.get(CONF_MAC)

    if not mac:
        raise ValueError("MAC address missing from config entry")

    coordinator = ACInfinityCoordinator(
        hass,
        mac,
        entry.title,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        ["fan", "switch", "sensor"],
    )

    return True
