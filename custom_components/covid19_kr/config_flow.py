"""Config flow for covid19_kr"""
import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, SIDO_LIST

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for covid19_kr."""

    VERSION = 1

    async def async_step_user(self, user_input = None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None and (sido := user_input.get("sido")) is not None and sido in SIDO_LIST:

            if not SIDO_LIST[sido]["city"]: 
                user_input["city"] = sido
                return self.async_create_entry(
                    title=sido, data=user_input
                )

            return await self.async_step_city(user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("sido"): vol.In(list(SIDO_LIST.keys()))
            }),
            errors=errors,
        )

    async def async_step_city(self, user_input = None):
        """Handle input of city."""
        errors = {}

        if user_input is not None and (sido := user_input.get("sido")) is not None and (city := user_input.get("city")) is not None and city in SIDO_LIST[sido]["city"]:

            await self.async_set_unique_id(city)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=city, data=user_input
            )
        
        CITY_LIST = [sido] + SIDO_LIST[sido]["city"] if user_input is not None and sido is not None else []

        return self.async_show_form(
            step_id="city",
            data_schema=vol.Schema({
                vol.Required("sido"): sido,
                vol.Required("city"): vol.In(CITY_LIST)
            }),
            errors=errors,
        )
