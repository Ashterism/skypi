from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from ..providers.weather_openmeteo import get_hourly_forecast
from ..providers.moon_astral import get_hourlymoon

from ..models import HourlyForecast
from ..config import DAYS, START_TIME, END_TIME, TIMEZONE


"""
python -m skypi.services.forecaster

"""

# create start and end datetimes to use with providers
def create_datetime(days):
    start_date = date.today()

    start_dt = datetime(
        start_date.year,
        start_date.month,
        start_date.day,
        int(START_TIME.split(":")[0]),
        0,
        tzinfo=ZoneInfo(TIMEZONE)
    )

    end_date = start_date + timedelta(days=days - 1)

    end_dt = datetime(
        end_date.year,
        end_date.month,
        end_date.day,
        int(END_TIME.split(":")[0]),
        0,
        tzinfo=ZoneInfo(TIMEZONE)
    )

    return start_dt, end_dt

# test function to ensure data from both providers aligns (time stamps)
def check_data(all_w_hours, all_m_hours):
    # check length
    assert len(all_w_hours) == len(all_m_hours), "Length mismatch"

    for i in range(len(all_w_hours)):
        assert all_w_hours[i].time == all_m_hours[i].time, f"Mismatch at index {i}"


# main / runner script
def get_forecast_data(days: int = DAYS):

    start_dt, end_dt = create_datetime(days)

    all_w_hours = get_hourly_forecast(start_dt, end_dt)
    all_m_hours = get_hourlymoon(start_dt, end_dt)

    check_data(all_w_hours, all_m_hours)

    forecast_hours = []
    for i in range(len(all_w_hours)):
        hour = HourlyForecast(
            # weather data
            time=all_w_hours[i].time,
            cloud_pct=all_w_hours[i].cloud_pct,
            temp_c=all_w_hours[i].temp_c,
            dew_point_c=all_w_hours[i].dew_point_c,
            wind_kmh=all_w_hours[i].wind_kmh,
            gust_kmh=all_w_hours[i].gust_kmh,
            visibility_m=all_w_hours[i].visibility_m,
            rain_pct=all_w_hours[i].rain_pct,
            # moon data
            moon_phase=all_m_hours[i].phase,
            moon_elevation=all_m_hours[i].el
        )

        # add each hourly forecast object to a list of hour objects
        forecast_hours.append(hour)

    return forecast_hours



if __name__ == "__main__":
    test = get_forecast_data()
    print(test)