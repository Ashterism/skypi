from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from skypi.config import TIMEZONE, START_TIME
from skypi.models import HourlyForecast
from skypi.services.astro_sessions import best_astro_window, astro_session_rating

"""
python -m pytest tests/test_astro_session_rating.py
"""

def mock_data(ratings: list[str]) -> list[HourlyForecast]:
    start_hour = int(START_TIME.split(":")[0])
    test_date = datetime.now(ZoneInfo(TIMEZONE)).date()
    start_dt = datetime(
        test_date.year,
        test_date.month,
        test_date.day,
        start_hour,
        tzinfo=ZoneInfo(TIMEZONE),
    )

    hours = []

    i = 0
    for rating in ratings:
        dt = start_dt + timedelta(hours=i)

        hours.append(
            HourlyForecast(
                astro_date=test_date,
                time=dt,
                cloud_pct=0,
                temp_c=20,
                dew_point_c=10,
                wind_kmh=5,
                gust_kmh=8,
                visibility_m=20000,
                rain_pct=0,
                moon_phase=0,
                moon_elevation=-10,
                cloud_rating=None,
                dew_rating=None,
                wind_rating=None,
                visibility_rating=None,
                moon_rating=None,
                overall_rating=rating,
            )
        )
        i += 1

    return hours


def test_three_consecutive_g_is_green_go():
    hours = mock_data(["G", "G", "G"])

    window = best_astro_window(hours)
    result = astro_session_rating(window)

    assert result["rag"] == "G"
    assert result["result"] == "GO"
    assert window["best_window_hours"] == hours
    assert window["best_window_length"] == 3


def test_two_consecutive_g_is_amber_maybe():
    hours = mock_data(["G", "G"])

    window = best_astro_window(hours)
    result = astro_session_rating(window)

    assert result["rag"] == "A"
    assert result["result"] == "MAYBE"
    assert window["best_window_hours"] == hours
    assert window["best_window_length"] == 2


def test_split_g_hours_is_red_no_go():
    hours = mock_data(["G", "R", "G"])

    window = best_astro_window(hours)
    result = astro_session_rating(window)

    assert result["rag"] == "R"
    assert result["result"] == "NO-GO"
    assert window["best_window_hours"] == [hours[2]]
    assert window["best_window_length"] == 1


def test_middle_two_g_hours_is_amber_maybe():
    hours = mock_data(["R", "G", "G", "R"])

    window = best_astro_window(hours)
    result = astro_session_rating(window)

    assert result["rag"] == "A"
    assert result["result"] == "MAYBE"
    assert window["best_window_hours"] == [hours[1], hours[2]]
    assert window["best_window_length"] == 2


def test_longest_window_wins():
    hours = mock_data(["G", "G", "G", "R", "G"])

    window = best_astro_window(hours)
    result = astro_session_rating(window)

    assert result["rag"] == "G"
    assert result["result"] == "GO"
    assert window["best_window_hours"] == [hours[0], hours[1], hours[2]]
    assert window["best_window_length"] == 3