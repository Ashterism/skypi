from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HourlyWeather:
    """One hour of weather conditions"""

    time: str
    cloud_pct: float
    temp_c: float
    dew_point_c: float
    wind_kmh: float
    gust_kmh: float
    visibility_m: float
    rain_pct: float


@dataclass
class HourlyMoon:
    """One hour of moon conditions"""
    time: str
    phase: float
    el: float
    

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