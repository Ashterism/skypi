
"""
    python -m skypi.services.astro_sessions
"""

from ..models import AstroSession
from .forecaster import get_forecast


def astro_session_rating(astro_date_hours):
    consec_hours_g = 0
    consec_g_dts = []
    max_consec_g = 0
    max_consec_g_dts = []
   

    for hour in astro_date_hours:
        if hour.overall_rating == "G":
            consec_hours_g += 1
            consec_g_dts.append(hour.time)
            max_consec_g = max(max_consec_g, consec_hours_g)
            if max_consec_g == consec_hours_g:
                max_consec_g_dts = consec_g_dts

        else:
            consec_hours_g = 0
            consec_g_dts = []        
    
    if max_consec_g >= 3:
        gng = {"rag": "G", "result": "GO", "window": max_consec_g_dts}
    elif max_consec_g == 2:
        gng = {"rag": "A", "result": "MAYBE", "window": max_consec_g_dts}
    else:
        gng = {"rag": "R", "result": "NO-GO", "window": "na"}
    
    return gng


def create_astro_sessions():
    forecast_hours = get_forecast()
    astro_date_list = []
    for hour in forecast_hours:
        if (
            hour.astro_date == None or 
            hour.astro_date in astro_date_list
        ):
            pass

        else:
            astro_date_list.append(hour.astro_date)

    
    astro_session_data = []
    for date in astro_date_list:
        astro_date_hours = []
        for hour in forecast_hours:
            if hour.astro_date == date:
                astro_date_hours.append(hour)

        astro_day = AstroSession(
                astro_date=date,
                astro_hours=astro_date_hours,
                astro_rating=astro_session_rating(astro_date_hours)
            )         
        
        astro_session_data.append(astro_day)

    return astro_session_data
            
   # print(astro_session_data[0])


def get_astro_sessions():
    astro_session_data = create_astro_sessions()
    return astro_session_data


if __name__ == "__main__":
    astro_session_data = create_astro_sessions()
    print(astro_session_data)
    print("ran")



