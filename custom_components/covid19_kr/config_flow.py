"""Config flow for covid19_kr"""
import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, SIDO_LIST

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for covid19_kr."""

    VERSION = 1

    def __init__(self):
        """Initialize a new covid19_kr ConfigFlow."""
        self.options = {}

    async def async_step_user(self, user_input = None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            sido = user_input.get("sido", "전국")
            self.options.update({"sido": sido})

            if not SIDO_LIST[sido]["city"]: 
                self.options.update({"city": sido})
                return self.async_create_entry(
                    title=sido, data=self.options
                )

            return await self.async_step_city()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("sido"): vol.In(list(SIDO_LIST.keys()))}),
            errors=errors,
        )

    async def async_step_city(self, user_input = None):
        """Handle input of city."""
        errors = {}

        if user_input is not None:
            city = user_input.get("city", self.options["sido"])
            self.options.update({"city": city})

            await self.async_set_unique_id(city)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=city, data=self.options
            )

        CITY_LIST = [self.options["sido"]] + SIDO_LIST[self.options["sido"]]["city"]

        return self.async_show_form(
            step_id="city",
            data_schema=vol.Schema({vol.Required("city"): vol.In(CITY_LIST)}),
            errors=errors,
        )