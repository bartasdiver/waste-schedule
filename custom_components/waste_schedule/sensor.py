"""Sensor platform for Waste Schedule integration."""
from datetime import date, datetime, timedelta
from typing import List

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    WASTE_SCHEDULES,
    WasteSchedule,
    SENSOR_CALENDAR,
    SENSOR_DAYS_UNTIL,
    SENSOR_NEXT_DATE,
)


def calculate_next_collection(start_date: date, frequency_weeks: int, today: date) -> date:
    """Calculate next waste collection date."""
    # If start date is in the future, return it
    if start_date > today:
        return start_date

    # Calculate weeks since start date
    days_since_start = (today - start_date).days
    weeks_since_start = days_since_start // 7

    # Find next collection
    next_collection_num = (weeks_since_start // frequency_weeks) + 1
    next_collection = start_date + timedelta(weeks=next_collection_num * frequency_weeks)

    return next_collection


def get_all_collection_dates(
    start_date: date, frequency_weeks: int, from_date: date, months_ahead: int = 12
) -> List[date]:
    """Get all collection dates for the next N months."""
    dates = []
    current = calculate_next_collection(start_date, frequency_weeks, from_date)
    end_date = from_date + timedelta(days=months_ahead * 30)

    while current <= end_date:
        dates.append(current)
        current = current + timedelta(weeks=frequency_weeks)

    return dates


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    entities = []

    for schedule in WASTE_SCHEDULES:
        # Create next date sensor
        entities.append(WasteNextDateSensor(schedule))

        # Create days until sensor
        entities.append(WasteDaysUntilSensor(schedule))

        # Create calendar events sensor
        entities.append(WasteCalendarSensor(schedule))

    async_add_entities(entities)


class WasteNextDateSensor(SensorEntity):
    """Sensor for next waste collection date."""

    def __init__(self, schedule: WasteSchedule) -> None:
        """Initialize the sensor."""
        self.schedule = schedule
        self._attr_unique_id = f"{DOMAIN}_{schedule.waste_type.value}_{SENSOR_NEXT_DATE}"
        self._attr_name = f"{schedule.name} - następna data"
        self._attr_icon = schedule.icon
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> str:
        """Return the next collection date."""
        today = date.today()
        next_date = calculate_next_collection(
            self.schedule.start_date, self.schedule.frequency_weeks, today
        )
        return next_date.isoformat()

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        today = date.today()
        next_date = calculate_next_collection(
            self.schedule.start_date, self.schedule.frequency_weeks, today
        )
        return {
            "start_date": self.schedule.start_date.isoformat(),
            "frequency_weeks": self.schedule.frequency_weeks,
            "days_until": (next_date - today).days,
        }


class WasteDaysUntilSensor(SensorEntity):
    """Sensor for days until next waste collection."""

    def __init__(self, schedule: WasteSchedule) -> None:
        """Initialize the sensor."""
        self.schedule = schedule
        self._attr_unique_id = f"{DOMAIN}_{schedule.waste_type.value}_{SENSOR_DAYS_UNTIL}"
        self._attr_name = f"{schedule.name} - dni do wywozu"
        self._attr_icon = schedule.icon
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> int:
        """Return days until next collection."""
        today = date.today()
        next_date = calculate_next_collection(
            self.schedule.start_date, self.schedule.frequency_weeks, today
        )
        return (next_date - today).days

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        today = date.today()
        next_date = calculate_next_collection(
            self.schedule.start_date, self.schedule.frequency_weeks, today
        )
        return {
            "next_date": next_date.isoformat(),
            "start_date": self.schedule.start_date.isoformat(),
            "frequency_weeks": self.schedule.frequency_weeks,
        }


class WasteCalendarSensor(SensorEntity):
    """Sensor providing calendar events for waste collection."""

    def __init__(self, schedule: WasteSchedule) -> None:
        """Initialize the sensor."""
        self.schedule = schedule
        self._attr_unique_id = f"{DOMAIN}_{schedule.waste_type.value}_{SENSOR_CALENDAR}"
        self._attr_name = f"{schedule.name} - kalendarz"
        self._attr_icon = "mdi:calendar"

    @property
    def native_value(self) -> str:
        """Return the number of upcoming collections."""
        today = date.today()
        dates = get_all_collection_dates(
            self.schedule.start_date, self.schedule.frequency_weeks, today
        )
        return str(len(dates))

    @property
    def extra_state_attributes(self):
        """Return calendar events as attributes."""
        today = date.today()
        dates = get_all_collection_dates(
            self.schedule.start_date, self.schedule.frequency_weeks, today
        )

        events = []
        for collection_date in dates:
            events.append({
                "start": collection_date.isoformat(),
                "end": collection_date.isoformat(),
                "summary": f"Wywóz: {self.schedule.name}",
            })

        return {
            "events": events,
        }
