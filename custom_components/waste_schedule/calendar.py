"""Calendar platform for Waste Schedule integration."""
from datetime import date, datetime, timedelta
from typing import List

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN, WASTE_SCHEDULES, WasteSchedule
from .sensor import get_all_collection_dates


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
        today = date.today()
        next_date = get_all_collection_dates(
            self.schedule.start_date, self.schedule.frequency_weeks, today, months_ahead=1
        )

        if next_date:
            next_collection = next_date[0]
            # Create timezone-aware datetime using local timezone
            midnight = dt_util.now().replace(hour=0, minute=0, second=0, microsecond=0)
            event_start = midnight.replace(day=next_collection.day, month=next_collection.month, year=next_collection.year)
            event_end = event_start.replace(hour=23, minute=59, second=59)
            return CalendarEvent(
                start=dt_util.as_utc(event_start),
                end=dt_util.as_utc(event_end),
                summary=f"Wywóz: {self.schedule.name}",
            )
        return None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> List[CalendarEvent]:
        """Return calendar events within date range."""
        today = date.today()
        all_dates = get_all_collection_dates(
            self.schedule.start_date, self.schedule.frequency_weeks, today, months_ahead=12
        )

        events = []
        for collection_date in all_dates:
            # Create timezone-aware datetime using local timezone
            midnight = dt_util.now().replace(hour=0, minute=0, second=0, microsecond=0)
            event_start = midnight.replace(day=collection_date.day, month=collection_date.month, year=collection_date.year)
            event_end = event_start.replace(hour=23, minute=59, second=59)

            # Convert to UTC for comparison
            event_start_utc = dt_util.as_utc(event_start)
            event_end_utc = dt_util.as_utc(event_end)

            # Check if event is within the requested range
            if event_start_utc <= end_date and event_end_utc >= start_date:
                events.append(
                    CalendarEvent(
                        start=event_start_utc,
                        end=event_end_utc,
                        summary=f"Wywóz: {self.schedule.name}",
                    )
                )

        return events
