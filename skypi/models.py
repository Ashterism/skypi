from __future__ import annotations
from typing import List

from datetime import date, datetime

from dataclasses import dataclass


@dataclass
class HourlyWeather:
    """One hour of weather conditions from provider"""

    time: datetime
    cloud_pct: float
    temp_c: float
    dew_point_c: float
    wind_kmh: float
    gust_kmh: float
    visibility_m: float
    rain_pct: float


@dataclass
class HourlyMoon:
    """One hour of moon conditions from provider"""
    time: datetime
    phase: float
    el: float


@dataclass
class HourlyForecast:
    """One hour of combined forecast data"""
    #meta
    astro_date: date
    #weather
    time: datetime
    cloud_pct: float
    temp_c: float
    dew_point_c: float
    wind_kmh: float
    gust_kmh: float
    visibility_m: float
    rain_pct: float
    #moon
    moon_phase: float
    moon_elevation: float
    #ratings
    cloud_rating: str | None = None
    dew_rating: str | None = None
    wind_rating: str | None = None
    visibility_rating: str | None = None
    moon_rating: str | None = None
    overall_rating: str | None = None


@dataclass
class AstroSession:
    #meta
    astro_date: date
    astro_hours: List[HourlyForecast] | None = None
    astro_rating: str | None = None


#REMOVE AFTER REFACTOR OF EVALUATOR (or keep and refactor hourlyforecast to nestle)
@dataclass
class HourlyRating:
    time: str
    cloud_rating: str
    dew_rating: str
    wind_rating: str
    visibility_rating: str
    moon_rating: str
    overall_rating: str



# @dataclass
# class RatedHour:
#     """Rating of weather - kept separate from raw weather"""

#     hour: HourlyWeather
#     rag: str  # "R", "A", or "G"