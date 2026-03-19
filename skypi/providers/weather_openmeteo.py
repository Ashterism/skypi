import requests

from ..models import HourlyWeather
from ..config import LATITUDE, LONGITUDE, TIMEZONE

"""
python -m skypi.providers.weather_openmeteo

"""

base_url = "https://api.open-meteo.com/v1/forecast"
hourly = "cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility,precipitation_probability,temperature_2m,relative_humidity_2m,dew_point_2m,wind_speed_10m,wind_gusts_10m"
temperature_unit = "celsius"
wind_speed_unit = "kmh"


def get_hourly_forecast(start_dt, end_dt) -> list[HourlyWeather]:

    # convert time to string format used by open meteo
    start_hour = start_dt.strftime('%Y-%m-%dT%H:%M')
    end_hour = end_dt.strftime('%Y-%m-%dT%H:%M')

    api_url = (
        f"{base_url}?"
        f"latitude={LATITUDE}&"
        f"longitude={LONGITUDE}&"
        f"hourly={hourly}&"
        f"temperature_unit={temperature_unit}&"
        f"wind_speed_unit={wind_speed_unit}&"
        f"timezone={TIMEZONE}&"
        f"start_hour={start_hour}&"
        f"end_hour={end_hour}"
    )

    # fetch the weather forecast per hour, for a set of hours
    response = requests.get(api_url, timeout=15)
    response.raise_for_status()

    content = response.json()
    hourly_block = content["hourly"] # data section in json

    # split the forecasts into hourly objects
    hours = []

    for i in range(len(hourly_block["time"])):
        hour = HourlyWeather(
            time=hourly_block["time"][i],
            cloud_pct=hourly_block["cloud_cover"][i],
            temp_c=hourly_block["temperature_2m"][i],
            dew_point_c=hourly_block["dew_point_2m"][i],
            wind_kmh=hourly_block["wind_speed_10m"][i],
            gust_kmh=hourly_block["wind_gusts_10m"][i],
            visibility_m=hourly_block["visibility"][i],
            rain_pct=hourly_block["precipitation_probability"][i]
        )

        # add each hourly forecast object to a list "hours"
        hours.append(hour)

    return hours



if __name__ == "__main__":

    # test print
    ...
