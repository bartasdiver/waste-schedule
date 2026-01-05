"""Calendar platform for Waste Schedule integration."""
import logging
from datetime import date, datetime, timedelta
from typing import List

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN, WASTE_SCHEDULES, WasteSchedule
from .sensor import get_all_collection_dates

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the calendar platform."""
    entities = []

    for schedule in WASTE_SCHEDULES:
        entities.append(WasteCalendarEntity(schedule))

    async_add_entities(entities)


class WasteCalendarEntity(CalendarEntity):
    """Calendar entity for waste collection schedule."""

    def __init__(self, schedule: WasteSchedule) -> None:
        """Initialize the calendar entity."""
        self.schedule = schedule
        self._attr_unique_id = f"{DOMAIN}_calendar_{schedule.waste_type.value}"
        self._attr_name = f"{schedule.name} - Harmonogram"
        self._attr_icon = "mdi:calendar"

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        try:
            today = date.today()
            next_date = get_all_collection_dates(
                self.schedule.start_date, self.schedule.frequency_weeks, today, months_ahead=1
            )

            if next_date:
                next_collection = next_date[0]
                # All-day events use date objects (not datetime)
                return CalendarEvent(
                    start=next_collection,
                    end=next_collection,
                    summary=f"Wywóz: {self.schedule.name}",
                )
        except Exception:
            return None
        return None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> List[CalendarEvent]:
        """Return calendar events within date range."""
        try:
            today = date.today()
            all_dates = get_all_collection_dates(
                self.schedule.start_date, self.schedule.frequency_weeks, today, months_ahead=12
            )

            events = []
            for collection_date in all_dates:
                # Convert datetime to date for comparison
                start = start_date.date() if hasattr(start_date, 'date') else start_date
                end = end_date.date() if hasattr(end_date, 'date') else end_date

                # Check if event is within the requested range
                if start <= collection_date <= end:
                    events.append(
                        CalendarEvent(
                            start=collection_date,
                            end=collection_date,
                            summary=f"Wywóz: {self.schedule.name}",
                        )
                    )

            return events
        except Exception as e:
            _LOGGER.error(f"Error getting events for {self.schedule.name}: {e}")
            return []
