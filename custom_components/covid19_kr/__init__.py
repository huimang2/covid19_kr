"""The COVID-19 KR integration."""
from datetime import datetime, timedelta
import re
import logging

import async_timeout
from bs4 import BeautifulSoup

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import update_coordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, SIDO_LIST

PLATFORMS = ["sensor"]
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the covid19_kr component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up covid19_kr from a config entry."""

    if not entry.unique_id:
        hass.config_entries.async_update_entry(entry, unique_id=entry.data.get("city"))

    coordinator = await get_coordinator(hass, entry)

    if not coordinator.last_update_success:
        await coordinator.async_config_entry_first_refresh()

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def get_coordinator(
    hass: HomeAssistant, entry: ConfigEntry
) -> update_coordinator.DataUpdateCoordinator:
    """Get the data update coordinator."""

    sido = entry.data.get("sido")
    city = entry.data.get("city")

    if hass.data[DOMAIN].get(city): 
        return hass.data[DOMAIN][city]

    async def async_get_data():
        with async_timeout.timeout(20):

            if sido is None or city is None or sido not in SIDO_LIST or \
            (city not in SIDO_LIST and city not in SIDO_LIST[sido]['city']): return {}

            _sido = list(SIDO_LIST)[0] if city in SIDO_LIST else sido

            try:
                hdr = {
                    "User-Agent": (
                        "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36"
                    )
                }

                session = async_get_clientsession(hass)

                response = await session.get(SIDO_LIST[_sido]['url'], headers=hdr, timeout=30)
                response.raise_for_status()

                cr = BeautifulSoup(await response.text(), "html.parser")

            except Exception as ex:
                _LOGGER.error("Failed to crawling Error: %s", ex)
                raise

            idx = list(SIDO_LIST).index(city) if city in SIDO_LIST else SIDO_LIST[sido]['city'].index(city)
            selector = lambda x: ''.join(re.split('[^0-9]', cr.select(SIDO_LIST[_sido]['selector'].format(x))[idx].text)) or 0
            attribute = SIDO_LIST[_sido].get('attribute',{})

            data = (lambda x: { x[0][n]: selector(x[1][n]) for n in range(len(x[0])) })(SIDO_LIST[_sido]['sensor'])

            data.update({
                "attribute": { s: (lambda x: { attribute[x][0][n]: selector(attribute[x][1][n]) for n in range(len(attribute[x][0])) })(s) for s in attribute },
                "last_update": datetime.strptime(str(datetime.now().year) if _sido in ["부산", "울산"] else "" + \
                    ''.join(str(format(int(x), '02' if i or _sido in ["부산", "울산", "경북"] else '04')) \
                    for i, x in enumerate(re.split('[^0-9]', cr.select_one(SIDO_LIST[_sido]['last_update']).text)) if x), "%Y%m%d%H" + ("%M" if _sido in ["인천", "경기", "경북"] else ""))
            })

            return data

    hass.data[DOMAIN][city] = update_coordinator.DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name=DOMAIN,
        update_method=async_get_data,
        update_interval=timedelta(minutes=30),
    )
    await hass.data[DOMAIN][city].async_refresh()
    return hass.data[DOMAIN][city]
