"""Config flow for Waste Schedule integration."""
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class WasteScheduleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Waste Schedule."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Check if already configured
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        # Automatically create the entry without user input
        return self.async_create_entry(
            title="Waste Schedule",
            data={},
        )
