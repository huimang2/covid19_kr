"""Config flow for covid19_kr"""
import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, SIDO_LIST


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for covid19_kr."""

    VERSION = 1

    def __init__(self):
        """Initialize a new covid19_kr ConfigFlow."""
        self.data = {}

    async def async_step_user(self, user_input = None):
        """Handle the initial step."""
        
        if user_input is not None:
            self.data.update(sido=user_input.get("sido"))

        if (sido := self.data.get("sido")) is not None and sido in SIDO_LIST:

            if not SIDO_LIST[sido]["city"]:

                self.data.update(sido=sido, city=sido)
                return self.async_create_entry(title=sido, data=self.data)

            self.data.update(sido=sido)
            return await self.async_step_city()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("sido"): vol.In(list(SIDO_LIST.keys()))
            })
        )

    async def async_step_city(self, user_input = None):
        """Handle input of city."""

        if user_input is not None:
            self.data.update(city=user_input.get("city"))

        if (sido := self.data.get("sido")) is None or sido not in SIDO_LIST:
            self.data = {}
            return await self.async_step_user()

        if (city := self.data.get("city")) is not None and city in SIDO_LIST[sido]["city"] or sido == city:

            await self.async_set_unique_id(city)
            self._abort_if_unique_id_configured()

            self.data.update(sido=sido, city=city)
            return self.async_create_entry(title=city, data=self.data)
        
        CITY_LIST = [sido] + SIDO_LIST[sido]["city"]

        return self.async_show_form(
            step_id="city",
            data_schema=vol.Schema({
                vol.Required("sido"): sido,
                vol.Required("city"): vol.In(CITY_LIST)
            })
        )
