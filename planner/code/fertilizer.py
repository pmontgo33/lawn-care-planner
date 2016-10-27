# fertilizer.py
# Patrick W. Montgomery
# created: 10/25/2016

"""
See each seasons apps function for the fertilization plan.
"""

# import statements
from datetime import datetime, date, timedelta
from . import planner

def spring_apps(closest_station, temp_data):
    """
    Spring Application plan is to put down one application of .75lb Nitrogen per
    1000 sf when the average temperatures get above 60F. 
    """
    
    APPLY_ABOVE = 60 # degrees F
    APP_RATE = .75 # lb per 1000 sf
    my_apps = []
    current_date = planner.seasons_dates['spring'][0]
    current_year = current_date.year
    
    while (current_date.year == current_year): # should this be date < end of spring date??????
        """
        Iterate through the temp_data and find the first day that the average temperature
        is above the APPLY_ABOVE value. We only need the first day, so then the loop breaks
        """
        average_temp = (temp_data[current_date]['TMIN'] + temp_data[current_date]['TMAX']) / 2
        
        if average_temp >= APPLY_ABOVE:
            my_apps.append({'date':current_date, 'rate':APP_RATE, 'end_date':None})
            break
        
        current_date += timedelta(days=1)
    
    return my_apps
    
def fall_apps(closest_station, temp_data):
    """
    Fall Application plan is to put down two applications of .75 lb Nitrogen per
    1000 sf
        1. When the average temperatures are between 75 and 65.
        2. 
    """
    
    APP_RATE = .75 # lb per 1000 sf
    my_apps = []
    
    ### FIRST FALL APPLICATION ###
    
    APPLY_RANGE = [75, 65] # degrees F
    current_date = planner.seasons_dates['fall'][0]
    current_year = current_date.year
    
    ########################YOU ARE HERE!!!!!!!!!!!!!!!!!!!!!!!!
    app_dates = []
    average_temp = 0
    while (average_temp ):
        """
        Iterate through the temp_data and find the first and last day that the average temperature
        is within the APP_RANGE values.
        """
        average_temp = (temp_data[current_date]['TMIN'] + temp_data[current_date]['TMAX']) / 2
        
        if average_temp <= APPLY_RANGE[0]:
            app_dates[0] = {'date':current_date, 'rate':APP_RATE, 'end_date':}
        elif average_temp <=
        
        current_date += timedelta(days=1)
    
    return my_apps
    
APPLICATIONS = {
    
    'spring':spring_apps,
}

def get_fertilizer_info(closest_station, temp_data):
    
    """
    This function iterates through the temperature data of the closest station
    and returns the applicable fertilzier info
    """
    
    fertilizer_info = {
        
        'applications':[],
    }
    
    for season in APPLICATIONS:
        season_apps = APPLICATIONS[season](closest_station, temp_data)
        fertilizer_info['applications'].extend(season_apps)
    
    return fertilizer_info