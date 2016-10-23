# weedcontrol.py
# Patrick W. Montgomery
# created: 10/21/2016

# import statements
from datetime import datetime, date, timedelta

def get_weed_control_info(closest_station, temp_data):
    
    """
    These are all static variables, and the basis for the summer annual pre-emergent
    application timing based on air temperature.
    """
    SUMMER_GERMINATION_TEMP = 55.0 # degrees F
    SUMMER_GERMINATION_TIME = 5 # days
    APP_PRIOR_TO_GERMINATION = 10 # days
    
    weed_info = {
        
        'summer_deadline':None,
    }
    
    current_date = datetime.strptime(closest_station['mindate'], "%Y-%m-%d").date()
    current_year = current_date.year
    
    days_at_temp = 0
    while (current_date.year == current_year):
        average_temp = (temp_data[current_date]['TMIN'] + temp_data[current_date]['TMAX']) / 2
        
        if average_temp >= SUMMER_GERMINATION_TEMP:
            days_at_temp += 1
            
            if days_at_temp >= SUMMER_GERMINATION_TIME:
                weed_info['summer_deadline'] = current_date - timedelta(days=APP_PRIOR_TO_GERMINATION)
                break
        else:
            days_at_temp = 0
        
        current_date += timedelta(days=1)    
    
    return weed_info
    