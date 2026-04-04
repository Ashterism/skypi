from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from .evaluator import get_evaluations

from ..providers.weather_openmeteo import get_hourly_forecast
from ..providers.moon_astral import get_hourlymoon

from ..models import HourlyForecast
from ..config import DAYS, START_TIME, END_TIME, TIMEZONE


"""
python -m skypi.services.forecaster

This file calls the weather and moon providers and merges their output
into hourly forecast objects.

It also adds an astro session date so post-midnight hours, like 1am,
get grouped in with the previous night.

Hours outside the astro session window are excluded from the forecast.
"""

start_hour = int(START_TIME.split(":")[0])
end_hour = int(END_TIME.split(":")[0])

# build the datetime range used when fetching provider data
def create_datetime(days):
    start_date = datetime.now(ZoneInfo(TIMEZONE)).date()

    start_dt = datetime(
        start_date.year,
        start_date.month,
        start_date.day,
        start_hour,
        tzinfo=ZoneInfo(TIMEZONE)
    )

    end_date = start_date + timedelta(days=days)  # lookahead end date; end_dt uses the astro session end hour

    end_dt = datetime(
        end_date.year,
        end_date.month,
        end_date.day,
        end_hour,
        tzinfo=ZoneInfo(TIMEZONE)
    )

    return start_dt, end_dt


def astro_date(dt):
# check if this hour sits in the astro session window and assign its session date (or None)
    t = dt.hour

    if start_hour <= end_hour:
        if start_hour <= t <= end_hour:
            return dt.date()
        return None

    if t >= start_hour:
        return dt.date()

    if t <= end_hour:
        return dt.date() - timedelta(days=1)

    return None
        


# fetch provider data and make sure the hourly timestamps line up
def fetch_forecast_data(days: int = DAYS):

    start_dt, end_dt = create_datetime(days)

    all_w_hours = get_hourly_forecast(start_dt, end_dt)
    all_m_hours = get_hourlymoon(start_dt, end_dt)

    assert len(all_w_hours) == len(all_m_hours), "Length mismatch"

    for i in range(len(all_w_hours)):
        assert all_w_hours[i].time == all_m_hours[i].time, f"Mismatch at index {i}"

    return(all_w_hours, all_m_hours)


# build HourlyForecast objects from the matched weather and moon hours
def create_forecast(all_w_hours, all_m_hours):
    forecast_hour_data = []

    for i in range(len(all_w_hours)):
        session_date = astro_date(all_w_hours[i].time)

        # skip hours outside the astro session window
        if session_date is None:
            continue

        hour = HourlyForecast(
            astro_date=session_date,
            time=all_w_hours[i].time,
            cloud_pct=all_w_hours[i].cloud_pct,
            temp_c=all_w_hours[i].temp_c,
            dew_point_c=all_w_hours[i].dew_point_c,
            wind_kmh=all_w_hours[i].wind_kmh,
            gust_kmh=all_w_hours[i].gust_kmh,
            visibility_m=all_w_hours[i].visibility_m,
            rain_pct=all_w_hours[i].rain_pct,
            moon_phase=all_m_hours[i].phase,
            moon_elevation=all_m_hours[i].el,
        )

        forecast_hour_data.append(hour)

    return forecast_hour_data


def get_forecast():
    # fetch raw weather and moon forecast data
    all_w_hours, all_m_hours = fetch_forecast_data()
    # merge them into hourly forecast objects
    raw_forecast_hours = create_forecast(all_w_hours, all_m_hours)
    # add ratings to each hour
    rated_forecast_hours = get_evaluations(raw_forecast_hours)
    # return the finished hourly forecast list
    return rated_forecast_hours


if __name__ == "__main__":
    test = get_forecast()
    print(test)