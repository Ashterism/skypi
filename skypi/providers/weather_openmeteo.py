import requests

from ..models import HourlyWeather
from ..utils.time_util import get_today, get_tomorrow

"""
python -m skypi.providers.weather_openmeteo

"""

base_url = "https://api.open-meteo.com/v1/forecast"
hourly = "cloud_cover,cloud_cover_low,cloud_cover_mid,cloud_cover_high,visibility,precipitation_probability,temperature_2m,relative_humidity_2m,dew_point_2m,wind_speed_10m,wind_gusts_10m"
temperature_unit = "celsius"
wind_speed_unit = "kmh"

latitude = 23.55053952123817
longitude = 54.74569584563267
timezone = "Asia%2FDubai"
start_time = "19:00"
end_time = "01:00"


def get_hourly_forecast() -> list[HourlyWeather]:

    # reminder this is here to ensure computed each time, not only first time
    start_hour = f"{get_today()}T{start_time}"
    end_hour = f"{get_tomorrow()}T{end_time}"

    api_url = (
        f"{base_url}?"
        f"latitude={latitude}&"
        f"longitude={longitude}&"
        f"hourly={hourly}&"
        f"temperature_unit={temperature_unit}&"
        f"wind_speed_unit={wind_speed_unit}&"
        f"timezone={timezone}&"
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
    hours = get_hourly_forecast()
    print(f"Fetched {len(hours)} hours")
    print(hours[0])
    print("\n")
