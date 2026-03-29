"""
python -m skypi.evaluator

This file evaluates each forecast hour and writes ratings onto the
HourlyForecast objects.

It does not evaluate full astro sessions / nights.
That grouping and session-level GO / NO-GO logic belongs elsewhere.
"""


def eval_cloud_pct(cloud_pct):
    if cloud_pct >= 20:
        return "R"
    elif cloud_pct >= 5:
        return "A"
    else:
        return "G"


def eval_dew(temp_c, dew_point):
    dew_spread = temp_c - dew_point
    if dew_spread <= 2:
        return "R"
    elif dew_spread < 5:
        return "A"
    else:
        return "G"


def eval_wind(wind_kmh, gust_kmh):
    effective_wind = max(wind_kmh, gust_kmh)

    if effective_wind > 25:
        return "R"
    elif effective_wind >= 16:
        return "A"
    else:
        return "G"


def eval_moonlight(phase, elevation):
    # for DSO - for milkyway <5 and >23 is Green
    if elevation < 0:
        return "G"
    else:
        if phase < 4 or phase > 24:
            return "G"
        elif (4 <= phase < 8) or (20 <= phase <= 24):
            return "A"
        else:
            return "R"


def eval_visibility(visibility_m):
    if visibility_m < 8000:
        return "R"
    elif visibility_m < 15000:
        return "A"
    else:
        return "G"


def overall_hour_rating(cloud, dew, wind, visibility, moon):
    ratings = [cloud, dew, wind, visibility, moon]
    if "R" in ratings:
        return "R"
    if "A" in ratings:
        return "A"
    return "G"


def evaluate_hours(forecast_hours):

    for hour in forecast_hours:
        cloud_rating = eval_cloud_pct(hour.cloud_pct)
        dew_rating = eval_dew(hour.temp_c, hour.dew_point_c)
        wind_rating = eval_wind(hour.wind_kmh, hour.gust_kmh)
        visibility_rating = eval_visibility(hour.visibility_m)
        moon_rating = eval_moonlight(hour.moon_phase, hour.moon_elevation)

        hour.cloud_rating = cloud_rating
        hour.dew_rating = dew_rating
        hour.wind_rating = wind_rating
        hour.visibility_rating = visibility_rating
        hour.moon_rating = moon_rating
        hour.overall_rating = overall_hour_rating(
            cloud_rating,
            dew_rating,
            wind_rating,
            visibility_rating,
            moon_rating,
        )

    return forecast_hours

    

def get_evaluations(hourly_forecast):
    hours = evaluate_hours(hourly_forecast)
    return hours



if __name__ == "__main__":
    from .forecaster import get_forecast

    hourly_forecast = get_forecast()

    for hour in hourly_forecast:
        print(
            f"{hour.time} | "
            f"astro_date={hour.astro_date} | "
            f"overall={hour.overall_rating} | "
            f"cloud={hour.cloud_rating} | "
            f"dew={hour.dew_rating} | "
            f"wind={hour.wind_rating} | "
            f"visibility={hour.visibility_rating} | "
            f"moon={hour.moon_rating}"
        )

        

"""
	•	Overall: GREEN / AMBER / RED
	•	Best window: 21:00-23:00
	•	1-line reasons (max 2-3), e.g.:

	•	“Cloud max 0%”
	•	“Wind max 9 km/h”
	•	“Dew spread min 8.8°C”
    
    """
