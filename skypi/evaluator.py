from .models import HourlyRating, HourlyMoon

"""
python -m skypi.evaluator

Does various evaluations on aspects of weather.  
Rates by hour, and by aspect
Also rates overall for the "day"

Data required for surfacing return via get_evaluations() wrapper def

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


def evaluate_hours(hourlyweather, hourlymoon):

    hours = []

    for i in range(len(hourlyweather)):

        cloud_rating = eval_cloud_pct(hourlyweather[i].cloud_pct)
        dew_rating = eval_dew(hourlyweather[i].temp_c, hourlyweather[i].dew_point_c)
        wind_rating = eval_wind(hourlyweather[i].wind_kmh, hourlyweather[i].gust_kmh)
        visibility_rating = eval_visibility(hourlyweather[i].visibility_m)
        moon_rating = eval_moonlight(hourlymoon[i].phase, hourlymoon[i].el)

        overall_rating = overall_hour_rating(
            cloud_rating,
            dew_rating,
            wind_rating,
            visibility_rating,
            moon_rating,
        )

        hour = HourlyRating(
            time=hourlyweather[i].time,
            cloud_rating=cloud_rating,
            dew_rating=dew_rating,
            wind_rating=wind_rating,
            visibility_rating=visibility_rating,
            moon_rating=moon_rating,
            overall_rating=overall_rating,
        )

        hours.append(hour)

    return hours


def evaluate_day(hours):
    good_hours = 0

    for i in range(len(hours)):
        if hours[i].overall_rating == "G":
            good_hours += 1
        
    if good_hours >= 4:
        gng = {"rag": "G", "result": "GO"}
    elif good_hours >= 2:
        gng = {"rag": "A", "result": "NO-GO"}
    else:
        gng = {"rag": "R", "result": "NO-GO"}
    
    return gng
    

def get_evaluations(hourlyweather, hourlymoon):
    hours = evaluate_hours(hourlyweather, hourlymoon)
    go_no_go = evaluate_day(hours)
    return go_no_go, hours


if __name__ == "__main__":
    ...
    # hours = evaluate_hours()
    # for h in hours:
    #     print(
    #         f"{h.time} - Overall: {h.overall_rating} | Cloud: {h.cloud_rating}, Dew: {h.dew_rating}, "
    #         f"Wind: {h.wind_rating}, Moon: {h.moon_rating}, Visibility: {h.visibility_rating}"
    #     )
    # print(f"Overall tonight: {evaluate_day(hours)}")




"""
	•	Overall: GREEN / AMBER / RED
	•	Best window: 21:00-23:00
	•	1-line reasons (max 2-3), e.g.:
	•	“Cloud max 0%”
	•	“Wind max 9 km/h”
	•	“Dew spread min 8.8°C”
    
    """
