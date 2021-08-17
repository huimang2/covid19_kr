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

from .const import DOMAIN, SIDO_LIST, DEFAULT_URL, SENSORS, ATTRIBUTE

PLATFORMS = ["sensor"]
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the covid19_kr component."""
    await get_coordinator(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up covid19_kr from a config entry."""

    if not entry.unique_id:
        hass.config_entries.async_update_entry(entry, unique_id=entry.data["city"])

    coordinator = await get_coordinator(hass, sido=entry.data["sido"], city=entry.data["city"])

    if not coordinator.last_update_success:
        await coordinator.async_config_entry_first_refresh()

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def get_coordinator(
    hass: HomeAssistant, sido=None, city=None
) -> update_coordinator.DataUpdateCoordinator:
    """Get the data update coordinator."""

    if DOMAIN in hass.data and hass.data[DOMAIN].data and city is not None and city in hass.data[DOMAIN].data:
        return hass.data[DOMAIN]

    async def async_get_data():
        with async_timeout.timeout(20):

            data = hass.data[DOMAIN].data if DOMAIN in hass.data and hass.data[DOMAIN].data else {}   
            if sido is None or city is None or sido not in SIDO_LIST: return data
            
            sensor = list(SENSORS)
            idx = list(SIDO_LIST.keys()).index(city) if sido == city else SIDO_LIST[sido]['city'].index(city)
            
            if city in SIDO_LIST or SIDO_LIST[sido]['url']: 
                cr = await crawling(hass, DEFAULT_URL if city in SIDO_LIST else SIDO_LIST[sido]['url'])
                selector = lambda x: ''.join(re.split('[^0-9]', cr.select(SIDO_LIST['전국' if city in SIDO_LIST else sido]['selector'].format(x))[idx].text)) or 0

            if city in SIDO_LIST:
                
                data[city] = {
                    sensor[0]: selector(2),
                    sensor[1]: selector(5),
                    sensor[2]: selector(6),
                    sensor[3]: selector(7),
                    sensor[4]: selector(8),
                    "attribute": {
                        sensor[0]: {
                            ATTRIBUTE[0]: selector(3),
                            ATTRIBUTE[1]: selector(4),
                            ATTRIBUTE[2]: selector(2),
                        },
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#content > div > div.timetable > p > span').text)) if x), "%Y%m%d%H")
                    },
                }

            elif sido == "서울":
                data[city] = {
                    sensor[0]: selector('3n'),
                    sensor[1]: selector('3n+2'),
                    "attribute": {
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#move-cont1 > p > strong').text)) if x), "%Y%m%d%H")
                    }
                }

            elif sido == "부산":
                data[city] = {
                    sensor[0]: selector(1),
                    sensor[1]: selector(2),
                    "attribute": {
                        "last_update": datetime.strptime(''.join([str(datetime.now().year)] + [str(format(int(x), '02')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#covid-state-area > div > div.covid-state-prevent > p > span').text)) if x]), "%Y%m%d%H")
                    }
                }

            elif sido == "인천":
                data[city] = {
                    sensor[0]: selector(4),
                    sensor[1]: selector(3),
                    "attribute": {
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#content > div > div > div > div > div:nth-child(1) > p.covid-contents__data > b').text)) if x), "%Y%m%d%H%M")
                    }
                }

            elif sido == "울산":
                data[city] = {
                    sensor[0]:  selector(1),
                    sensor[1]:  selector(2),
                    "attribute": {
                        "last_update": datetime.strptime(''.join([str(datetime.now().year)] + [str(format(int(x), '02')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('body > div.corona_wrap > div > div > div:nth-child(1) > div.top_area > p').text)) if x]), "%Y%m%d%H")
                    }
                }

            elif sido == "경기":
                data[city] = {

                    sensor[0]: selector(2),
                    sensor[1]: selector(1),
                    "attribute": {
                        sensor[1]: {
                            ATTRIBUTE[0]: selector(3),
                            ATTRIBUTE[1]: selector(4),
                            ATTRIBUTE[2]: selector(1),
                        },
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#result > div.s-w-covid19 > section > h3 > small').text)) if x), "%Y%m%d%H%M")
                    },
                } 
            elif sido == "강원":
                data[city] = {
                    sensor[1]: selector(0),
                    "attribute": {
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#main > div.inner > div.condition > h3 > span').text)) if x), "%Y%m%d%H")
                    }
                }
            elif sido == "경북":
                data[city] = {
                    sensor[0]: selector('span'),
                    sensor[1]: selector('strong'),
                    "attribute": {
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#contents > div.status > div:nth-child(1) > div.status_tit > dl > dd').text)) if x), "%y%m%d%H%M")
                    }
                }
            elif sido == "경남":
                data[city] = {
                    sensor[0]: selector(2),
                    sensor[1]: selector(1),
                    "attribute": {
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#subCnt > div:nth-child(3) > a > div > div.top_area > p.exp').text)) if x), "%Y%m%d%H")
                    }
                }

            return data

    hass.data[DOMAIN] = update_coordinator.DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name=DOMAIN,
        update_method=async_get_data,
        update_interval=timedelta(minutes=30),
    )
    await hass.data[DOMAIN].async_refresh()
    return hass.data[DOMAIN]


async def crawling(hass: HomeAssistant, url) -> BeautifulSoup:
    """Update function for updating api information."""
    try:
        hdr = {
            "User-Agent": (
                "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36"
            )
        }

        session = async_get_clientsession(hass)

        response = await session.get(url, headers=hdr, timeout=30)
        response.raise_for_status()

        return BeautifulSoup(await response.text(), "html.parser")

    except Exception as ex:
        _LOGGER.error("Failed to crawling Error: %s", ex)
        raise

        return False
