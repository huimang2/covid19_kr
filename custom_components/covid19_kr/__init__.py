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

from .const import DOMAIN, SIDO_LIST, DEFAULT_URL

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

            if city in SIDO_LIST:
                cr = await crawling(hass, DEFAULT_URL)

                data[city] = {
                    "신규확진자": cr.select('#content > div > div.data_table.midd.mgt24 > table > tbody > tr > td:nth-child(2)')[list(SIDO_LIST.keys()).index(city)].text.replace(',',''),
                    "누적확진자": cr.select('#content > div > div.data_table.midd.mgt24 > table > tbody > tr > td:nth-child(5)')[list(SIDO_LIST.keys()).index(city)].text.replace(',',''),
                    "격리자": cr.select('#content > div > div.data_table.midd.mgt24 > table > tbody > tr > td:nth-child(6)')[list(SIDO_LIST.keys()).index(city)].text.replace(',',''),
                    "격리해제": cr.select('#content > div > div.data_table.midd.mgt24 > table > tbody > tr > td:nth-child(7)')[list(SIDO_LIST.keys()).index(city)].text.replace(',',''),
                    "사망자": cr.select('#content > div > div.data_table.midd.mgt24 > table > tbody > tr > td:nth-child(8)')[list(SIDO_LIST.keys()).index(city)].text.replace(',',''),
                    "attribute": {
                        "신규확진자": {
                            "국내발생": cr.select('#content > div > div.data_table.midd.mgt24 > table > tbody > tr > td:nth-child(3)')[list(SIDO_LIST.keys()).index(city)].text.replace(',',''),
                            "해외유입": cr.select('#content > div > div.data_table.midd.mgt24 > table > tbody > tr > td:nth-child(4)')[list(SIDO_LIST.keys()).index(city)].text.replace(',',''),
                            "합계": cr.select('#content > div > div.data_table.midd.mgt24 > table > tbody > tr > td:nth-child(2)')[list(SIDO_LIST.keys()).index(city)].text.replace(',',''),
                        },
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#content > div > div.timetable > p > span').text)) if x), "%Y%m%d%H")
                    },
                }

                return data

            if SIDO_LIST[sido]['url']:
                cr = await crawling(hass, SIDO_LIST[sido]['url'])

            if sido == "서울":
                data[city] = {
                    "신규확진자": cr.select('#move-cont1 > div:nth-child(3) > table.tstyle-status.pc.pc-table > tbody > tr:nth-child(3n) > td')[SIDO_LIST[sido]['city'].index(city)].text.replace(',','').replace('+',''),
                    "누적확진자": cr.select('#move-cont1 > div:nth-child(3) > table.tstyle-status.pc.pc-table > tbody > tr:nth-child(3n+2) > td')[SIDO_LIST[sido]['city'].index(city)].text.replace(',',''),
                    "attribute": {
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#move-cont1 > p > strong').text)) if x), "%Y%m%d%H")
                    }
                }
            elif sido == "부산":
                data[city] = {
                    "신규확진자": cr.select('#covid-state-area > div > div.covid-state-table > table:nth-child(1) > tbody > tr:nth-child(1) > td')[1:][SIDO_LIST[sido]['city'].index(city)].text.replace('-','0'),
                    "누적확진자": cr.select('#covid-state-area > div > div.covid-state-table > table:nth-child(1) > tbody > tr:nth-child(2) > td')[1:][SIDO_LIST[sido]['city'].index(city)].text,
                    "attribute": {
                        "last_update": datetime.strptime(''.join([str(datetime.now().year)] + [str(format(int(x), '02')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#covid-state-area > div > div.covid-state-prevent > p > span').text)) if x]), "%Y%m%d%H")
                    }
                }
            elif sido == "인천":
                data[city] = {
                    "신규확진자": cr.select('#content > div > div > div > div > div:nth-child(2) > div > table > tr')[2].select('td')[1:][SIDO_LIST[sido]['city'].index(city)].text.replace(',','').replace('+',''),
                    "누적확진자": cr.select('#content > div > div > div > div > div:nth-child(2) > div > table > tr')[1].select('td')[1:][SIDO_LIST[sido]['city'].index(city)].text.replace(',',''),
                    "attribute": {
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#content > div > div > div > div > div:nth-child(1) > p.covid-contents__data > b').text)) if x), "%Y%m%d%H%M")
                    }
                }
            elif sido == "울산":
                data[city] = {
                    "신규확진자": cr.select('body > div.corona_wrap > div > div > div.localarea_box > table > tbody > tr:nth-child(1) > td')[SIDO_LIST[sido]['city'].index(city)].text.replace(',',''),
                    "누적확진자": cr.select('body > div.corona_wrap > div > div > div.localarea_box > table > tbody > tr:nth-child(2) > td')[SIDO_LIST[sido]['city'].index(city)].text.replace(',',''),
                    "attribute": {
                        "last_update": datetime.strptime(''.join([str(datetime.now().year)] + [str(format(int(x), '02')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('body > div.corona_wrap > div > div > div:nth-child(1) > div.top_area > p').text)) if x]), "%Y%m%d%H")
                    }
                }
            if sido == "경기":
                data[city] = {
                    "신규확진자": ''.join(x for x in re.split('[^0-9]', cr.select('#result > div.mt-4.py-4.w-100 > div > div > dl:nth-child(n+2) > dd > small:nth-child(2)')[SIDO_LIST[sido]['city'].index(city)].text) if x),
                    "누적확진자": cr.select('#result > div.mt-4.py-4.w-100 > div > div > dl:nth-child(n+2) > dd > strong')[SIDO_LIST[sido]['city'].index(city)].text.replace(',',''),
                    "attribute": {
                        "누적확진자": {
                            "국내발생": ''.join(x for x in re.split('[^0-9]', cr.select('#result > div.mt-4.py-4.w-100 > div > div > dl:nth-child(n+2) > dd > small:nth-child(3)')[SIDO_LIST[sido]['city'].index(city)].text) if x),
                            "해외유입": ''.join(x for x in re.split('[^0-9]', cr.select('#result > div.mt-4.py-4.w-100 > div > div > dl:nth-child(n+2) > dd > small:nth-child(4)')[SIDO_LIST[sido]['city'].index(city)].text) if x),
                            "합계": cr.select('#result > div.mt-4.py-4.w-100 > div > div > dl:nth-child(n+2) > dd > strong')[SIDO_LIST[sido]['city'].index(city)].text.replace(',',''),
                        },
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#result > div.s-w-covid19 > section > h3 > small').text)) if x), "%Y%m%d%H%M")
                    },
                } 
            elif sido == "강원":
                data[city] = {
                    "누적확진자": [x.text for x in cr.select('#main > div.inner > div.condition > div > table > tbody > tr:nth-child(2) > td:nth-child(n+2)') + cr.select('#main > div.inner > div.condition > div > table > tbody > tr:nth-child(4) > td')][SIDO_LIST[sido]['city'].index(city)].replace(',',''),
                    "attribute": {
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02' if i else '04')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#main > div.inner > div.condition > h3 > span').text)) if x), "%Y%m%d%H")
                    }
                }
            elif sido == "경북":
                data[city] = {
                    "신규확진자": cr.select('#contents > div.status > div:nth-child(2) > div > dl:nth-child(n+3) > dd > span')[SIDO_LIST[sido]['city'].index(city)].text.replace(',','').replace('+','').replace('-','0'),
                    "누적확진자": cr.select('#contents > div.status > div:nth-child(2) > div > dl:nth-child(n+3) > dd > strong')[SIDO_LIST[sido]['city'].index(city)].text.replace(',',''),
                    "attribute": {
                        "last_update": datetime.strptime(''.join(str(format(int(x), '02')) for i, x in enumerate(re.split('[^0-9]', cr.select_one('#contents > div.status > div:nth-child(1) > div.status_tit > dl > dd').text)) if x), "%y%m%d%H%M")
                    }
                }
            elif sido == "경남":
                data[city] = {
                    "신규확진자": cr.select('#subCnt > div.cont.corona_map > div.city_board > div > div.table.type1.pt10 > table > tbody > tr:nth-child(2) > td:nth-child(n+3)')[SIDO_LIST[sido]['city'].index(city)].text,
                    "누적확진자": cr.select('#subCnt > div.cont.corona_map > div.city_board > div > div.table.type1.pt10 > table > tbody > tr:nth-child(1) > td:nth-child(n+3)')[SIDO_LIST[sido]['city'].index(city)].text,
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
