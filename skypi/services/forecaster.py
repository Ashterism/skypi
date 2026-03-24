from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from ..providers.weather_openmeteo import get_hourly_forecast
from ..providers.moon_astral import get_hourlymoon
from ..evaluator import get_evaluations

from ..models import HourlyForecast
from ..config import DAYS, START_TIME, END_TIME, TIMEZONE


"""
python -m skypi.services.forecaster

This file calls the Moon and Weather data providers, and merges the output
into a single "forecast hour" object.

It adds an astro viewing session "date" to allow logical grouping e.g., 1am 
in with the previous night.

None "astro session" hours are excluded from the forecast.

"""

start_hour = int(START_TIME.split(":")[0])
end_hour = int(END_TIME.split(":")[0])

# create start and end datetimes to use with providers
def create_datetime(days):
    start_date = datetime.now(ZoneInfo(TIMEZONE)).date()

    start_dt = datetime(
        start_date.year,
        start_date.month,
        start_date.day,
        start_hour,
        tzinfo=ZoneInfo(TIMEZONE)
    )

    end_date = start_date + timedelta(days=days) # reminder - day ends at 1am

    end_dt = datetime(
        end_date.year,
        end_date.month,
        end_date.day,
        end_hour,
        tzinfo=ZoneInfo(TIMEZONE)
    )

    return start_dt, end_dt


def astro_date(dt):
# check if hour is in "astro period" and assign viewing session date (or none)
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
        


# fetch data from providers and validate matches
def fetch_forecast_data(days: int = DAYS):

    start_dt, end_dt = create_datetime(days)

    all_w_hours = get_hourly_forecast(start_dt, end_dt)
    all_m_hours = get_hourlymoon(start_dt, end_dt)

    assert len(all_w_hours) == len(all_m_hours), "Length mismatch"

    for i in range(len(all_w_hours)):
        assert all_w_hours[i].time == all_m_hours[i].time, f"Mismatch at index {i}"

    return(all_w_hours, all_m_hours)


# create hourly object (classes) from hours
def create_forecast(all_w_hours, all_m_hours):
    forecast_hour_data = []

    for i in range(len(all_w_hours)):
        session_date = astro_date(all_w_hours[i].time)

        # skips hours not in astro_range
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
    # fetch weather / moon forecasts
    all_w_hours, all_m_hours = fetch_forecast_data()
    # create hourly forecast objects
    raw_forecast_hours = create_forecast(all_w_hours, all_m_hours)
    # add ratings to the hours
    rated_forecast_hours = get_evaluations(raw_forecast_hours)
    # return complete hourly forecasts
    return rated_forecast_hours


if __name__ == "__main__":
    test = get_forecast()
    print(test)