# SkyPi

A simple local dashboard that answers one question:

> Is tonight good for astrophotography?

Built for desert shooting (Abu Dhabi), but designed to be flexible.

---

## What it does

- Pulls hourly weather data (cloud, wind, visibility, etc.)
- Pulls moon phase + elevation
- Combines them into a single hourly model
- Scores each hour (R / A / G)
- Groups hours into astro “nights” (19:00 → 01:00)
- Finds the best continuous shooting window
- Shows:
  - Go / No-Go for tonight
  - Next usable / best window
  - 2-week lookahead
  - Moon position + mini chart

---

## Stack

- Python
- Flask (simple UI)
- Open-Meteo (weather)
- Astral (moon data)


No JS frameworks. Runs locally.
Designed primarily for a 480x320 touchscreen (Raspberry Pi), with a separate desktop layout.

---

## Project structure

```
skypi/
│
├── skypi/
│   ├── services/
│   │   ├── forecaster.py        # builds hourly forecast data
│   │   ├── astro_sessions.py    # groups into nights + finds best windows
│   │   └── daily_report.py      # shapes data for the UI
│   │
│   ├── providers/
│   │   ├── weather_openmeteo.py
│   │   └── moon_astral.py
│   │
│   ├── evaluator.py             # R/A/G scoring logic
│   ├── models.py                # dataclasses (HourlyForecast, AstroSession)
│   └── config.py                # location + time settings
│
├── web/
│   ├── app.py                   # Flask app
│   ├── templates/
│   └── static/
│
├── requirements.txt
└── README.md
```

---

## How it works (high level)

1. **Forecaster**
   - pulls weather + moon data
   - aligns timestamps
   - builds HourlyForecast objects
   - filters to astro session hours

2. **Evaluator**
   - scores each hour (cloud, wind, moon, etc.)
   - produces overall R / A / G

3. **Astro sessions**
   - groups hours into nights
   - finds longest continuous good astro window
   - assigns night rating

4. **Daily report**
   - prepares UI-friendly data
   - “Tonight at a glance”
   - moon summary + chart
   - next usable / best window

---

## Running locally

From project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m web.app
```

Then open:

```
http://127.0.0.1:5001
```

---

## Config

Edit:

```
skypi/config.py
```

Key bits:
- LAT, LON
- TIMEZONE
- START_TIME / END_TIME (astro session window)

---

## Notes

- Astro “night” runs across midnight (e.g. 19:00 → 01:00)
- Hours are grouped using an astro_date so 01:00 belongs to the previous night
- “Best window” = longest continuous run of green hours
- “Next usable” = first green (or amber fallback) night in the horizon

---

## Current state

- v1.6: working end-to-end
- 14-day horizon
- local-only dashboard
- no caching yet

---

## Next steps (rough)

- caching forecast data
- multi-location (selection) support)
- cleaner config handling
- optional cloud deploy
- refine scoring model

---

## Why

Built because:
- existing weather apps don’t answer “can I shoot here tonight” without manually entering coordinates or reading through the data
- wanted to create a permanent display using a 480x320 touchscreen (Raspberry Pi)
- need a quick, honest go/no-go + window
- wanted something simple, local, and predictable