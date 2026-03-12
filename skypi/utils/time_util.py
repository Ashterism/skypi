from datetime import datetime, date, timedelta

def get_today():
    today = date.today()
    return(today.isoformat())

def get_tomorrow():
    tomorrow = date.today() + timedelta(days=1)
    return(tomorrow.isoformat())

if __name__ == "__main__":
    get_today()
    
