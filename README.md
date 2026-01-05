# Waste Schedule - Home Assistant Integration

Custom integration do Home Assistant do śledzenia harmonogramu wywozu odpadów.

## Funkcje

- Sensory z następną datą wywozu dla każdego typu odpadów
- Sensory pokazujące liczbę dni do następnego wywozu
- Kalendarze ze wszystkimi przyszłymi terminami wywozu
- Automatyczne obliczanie dat na podstawie częstotliwości

## Skonfigurowane typy odpadów

| Typ | Data początkowa | Częstotliwość |
|-----|-----------------|---------------|
| Resztkowe | 07.01.2026 | Co tydzień |
| Plastik | 20.01.2026 | Co 4 tygodnie |
| Papier i szkło | 19.01.2026 | Co 4 tygodnie |

## Instalacja

### Metoda 1: Manualna (zalecana do developmentu)

1. Skopiuj katalog `custom_components/waste_schedule` do katalogu `custom_components` w Twojej instalacji Home Assistant.
2. Zrestartuj Home Assistant.
3. Dodaj do `configuration.yaml`:

```yaml
# configuration.yaml
waste_schedule:
```

4. Zrestartuj Home Assistant ponownie.

### Metoda 2: HACS

Aby dodać to do HACS, musisz:
1. Utworzyć repozytorium GitHub
2. Dodać je jako custom repository w HACS

## Dostępne encje

### Sensory

Dla każdego typu odpadów dostępne są następujące sensory:

1. **Sensor następnej daty** (np. `sensor.odpady_resztkowe_nastepna_data`)
   - Pokazuje datę następnego wywozu w formacie ISO (np. `2026-01-07`)
   - Atrybuty:
     - `start_date`: Data początkowa harmonogramu
     - `frequency_weeks`: Częstotliwość w tygodniach
     - `days_until`: Liczba dni do wywozu

2. **Sensor dni do wywozu** (np. `sensor.odpady_resztkowe_dni_do_wywozu`)
   - Pokazuje liczbę dni do następnego wywozu
   - Atrybuty:
     - `next_date`: Data następnego wywozu
     - `start_date`: Data początkowa harmonogramu
     - `frequency_weeks`: Częstotliwość w tygodniach

3. **Sensor kalendarza** (np. `sensor.odpady_resztkowe_kalendarz`)
   - Pokazuje liczbę nadchodzących zbiórek
   - Atrybuty:
     - `events`: Lista wszystkich nadchodzących wydarzeń z datami

### Kalendarze

Dla każdego typu odpadów dostępny jest kalendarz (np. `calendar.odpady_resztkowe_harmonogram`), który można użyć w dashboardach z kalendarzem.

## Przykłady automatyzacji

### Powiadomienie dzień przed wywozem

```yaml
automation:
  - alias: "Powiadomienie o wywozie odpadów resztkowych"
    trigger:
      - platform: numeric_state
        entity_id: sensor.odpady_resztkowe_dni_do_wywozu
        below: 2
    action:
      - service: notify.mobile_app_your_device
        data:
          title: "Wywóz odpadów"
          message: "Jutro odbiór odpadów resztkowych! Wystaw pojemniki."
```

### Grupa wszystkich sensorów wywozu

```yaml
group:
  waste_schedule:
    name: Harmonogram wywozu odpadów
    entities:
      - sensor.odpady_resztkowe_nastepna_data
      - sensor.odpady_resztkowe_dni_do_wywozu
      - sensor.plastik_nastepna_data
      - sensor.plastik_dni_do_wywozu
      - sensor.papier_i_szklo_nastepna_data
      - sensor.papier_i_szklo_dni_do_wywozu
```

### Karta na dashboard

```yaml
type: entities
title: Harmonogram wywozu odpadów
entities:
  - entity: sensor.odpady_resztkowe_nastepna_data
    icon: mdi:trash-can
  - entity: sensor.odpady_resztkowe_dni_do_wywozu
    icon: mdi:calendar-clock
  - entity: sensor.plastik_nastepna_data
    icon: mdi:recycle
  - entity: sensor.plastik_dni_do_wywozu
    icon: mdi:calendar-clock
  - entity: sensor.papier_i_szklo_nastepna_data
    icon: mdi:package-variant
  - entity: sensor.papier_i_szklo_dni_do_wywozu
    icon: mdi:calendar-clock
```

## Modyfikacja harmonogramu

Aby zmienić daty lub częstotliwość wywozu, edytuj plik:
`custom_components/waste_schedule/const.py`

Znajdź sekcję `WASTE_SCHEDULES` i zmień odpowiednie wartości:

```python
WASTE_SCHEDULES = [
    WasteSchedule(
        waste_type=WasteType.RESZTKOWE,
        start_date=date(2026, 1, 7),  # Rok, miesiąc, dzień
        frequency_weeks=1,             # Co ile tygodni
        name="Odpady resztkowe",
        icon="mdi:trash-can"
    ),
    # Dodaj więcej typów odpadów...
]
```

Po zmianach zrestartuj Home Assistant.

## Rozwiązywanie problemów

### Sensory nie pokazują się

1. Sprawdź czy pliki są we właściwym miejscu: `<config>/custom_components/waste_schedule/`
2. Sprawdź logi Home Assistant (Settings > System > Logs) pod kątem błędów
3. Upewnij się, że Home Assistant został zrestartowany

### Błędne daty

1. Sprawdź czy daty początkowe w `const.py` są poprawne
2. Upewnij się, że częstotliwość (frequency_weeks) jest prawidłowa
3. Zrestartuj Home Assistant po zmianach

## Licencja

MIT
