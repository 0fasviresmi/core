"""The dwd_weather_warnings component."""

from __future__ import annotations

from dwdwfsapi import DwdWeatherWarningsAPI

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_REGION_IDENTIFIER, DOMAIN, PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    region_identifier: str = entry.data[CONF_REGION_IDENTIFIER]

    # Initialize the API.
    api = await hass.async_add_executor_job(DwdWeatherWarningsAPI, region_identifier)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = api

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
