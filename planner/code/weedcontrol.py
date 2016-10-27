# weedcontrol.py
# Patrick W. Montgomery
# created: 10/21/2016

# import statements
from datetime import datetime, date, timedelta
from . import utils

    
def get_weed_control_info(closest_station, temp_data):
    
    """
    This function uses the Growing Degree Day method of determining when the
    weeds will germinate. Information on this method can be found here:
    
    http://www.omafra.gov.on.ca/english/crops/pub811/10using.htm
    http://www.uky.edu/Ag/ukturf/4-1-14.html
    """
    
    """
    These are all static variables, and the basis for the summer annual pre-emergent
    application timing based on air temperature.
    """
    GDD_BASE_TEMP = 50.0 # degrees F
    SUMMER_GDD_TARGET = 45.0 # degree days
    APP_PRIOR_TO_GERMINATION = 10 # days
    
    weed_info = {
        
        'summer_deadline':None,
    }
    
    summer_germination_date = utils.get_gdd_date(SUMMER_GDD_TARGET, GDD_BASE_TEMP, closest_station, temp_data)
    weed_info['summer_deadline'] = summer_germination_date - timedelta(days=APP_PRIOR_TO_GERMINATION)
    
    return weed_info
    
def get_old_weed_control_info(closest_station, temp_data):
    
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
