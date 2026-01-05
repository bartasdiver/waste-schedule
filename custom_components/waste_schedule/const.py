"""Constants for the Waste Schedule integration."""
from datetime import date
from enum import Enum
from typing import NamedTuple


class WasteType(Enum):
    """Waste types."""

    RESZTKOWE = "resztkowe"
    PLASTIK = "plastik"
    PAPIER_SZKLO = "papier_szklo"


class WasteSchedule(NamedTuple):
    """Waste schedule configuration."""

    waste_type: WasteType
    start_date: date
    frequency_weeks: int
    name: str
    icon: str


# Waste collection schedules
# Format: WasteSchedule(type, start_date, frequency_weeks, display_name, icon)
WASTE_SCHEDULES = [
    WasteSchedule(
        waste_type=WasteType.RESZTKOWE,
        start_date=date(2026, 1, 7),
        frequency_weeks=1,
        name="Odpady resztkowe",
        icon="mdi:trash-can"
    ),
    WasteSchedule(
        waste_type=WasteType.PLASTIK,
        start_date=date(2026, 1, 20),
        frequency_weeks=4,
        name="Plastik",
        icon="mdi:recycle"
    ),
    WasteSchedule(
        waste_type=WasteType.PAPIER_SZKLO,
        start_date=date(2026, 1, 19),
        frequency_weeks=4,
        name="Papier i szkło",
        icon="mdi:package-variant"
    ),
]

DOMAIN = "waste_schedule"

# Sensor prefixes
SENSOR_NEXT_DATE = "next_date"
SENSOR_DAYS_UNTIL = "days_until"
SENSOR_CALENDAR = "calendar"
