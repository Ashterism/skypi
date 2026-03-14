from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from ..providers.weather_openmeteo import get_hourly_forecast
from ..providers.moon_astral import get_hourlymoon

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


def check_data(all_w_hours, all_m_hours):
    # check length
    len_w = len(all_w_hours)
    len_m = len(all_m_hours)
    if len_w == len_m:
        len_check = "Length matches"
    else:
        len_check = f"Length mismatch by: {(len_w - len_m)}"

    # check first & last hour match (for UTC/local errors etc)
    first_w_hour = all_w_hours[0].time
    first_m_hour = all_m_hours[0].time
    last_w_hour = all_w_hours[-1].time
    last_m_hour = all_m_hours[-1].time

    if first_w_hour == first_m_hour:
        first_hour = "hr1 matches"
    else:
        first_hour = f"hr1 clash {first_w_hour} vs {first_m_hour}"

    if last_w_hour == last_m_hour:
        last_hour = "hr-1 matches"
    else:
        last_hour = f"hr-1 clash {last_w_hour} vs {last_m_hour}"


    return(f"{len_check}, {first_hour}, {last_hour}")



def get_forecast_data(days: int = DAYS):

    start_dt, end_dt = create_datetime(days)

    all_w_hours = get_hourly_forecast(start_dt, end_dt)
    all_m_hours = get_hourlymoon(start_dt, end_dt)

    # error_check = check_data(all_w_hours, all_m_hours)
    # print(error_check)
    
   # print(f"Hours: {all_w_hours}\n")
   # print(f"Hours: {all_m_hours}\n")

    # print(f"{start_dt} - {end_dt}")
    # test = start_dt.strftime('%Y-%m-%dT%H:%M')

  
    

""""""
    # fetch data for today + days(-1)

    # combine into one object of 
    # cache object

    # extra def (maybe in another file?) - class to make cached data accessible to rest of programme


if __name__ == "__main__":
    get_forecast_data()