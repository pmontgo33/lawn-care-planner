# fertilizer.py
# Patrick W. Montgomery
# created: 10/25/2016

"""
See each seasons apps function for the fertilization plan.
"""

# import statements
from datetime import datetime, date, timedelta
from collections import OrderedDict
from . import lawnplanner as planner


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
        average_temp = (temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] + temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2
        
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
        2. Two weeks before the low temperature reaches 32
    """
    
    APP_RATE = .75 # lb per 1000 sf
    my_apps = []
    
    ### FIRST FALL APPLICATION ###
    my_apps.append(None)
    APPLY_RANGE = [75, 65] # degrees F
    current_date = planner.seasons_dates['fall'][0]
    current_year = current_date.year
    
    average_temp = (temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] + temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2
    
    while (average_temp > APPLY_RANGE[0]):
        """
        Iterate through the temp_data and find the first day that the average temperature
        is within the APP_RANGE values.
        """
        current_date += timedelta(days=1)
        average_temp = (temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] + temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2
    
    my_apps[-1] = {'date':current_date, 'rate':APP_RATE, 'end_date':None}
    
    while (average_temp > APPLY_RANGE[1]):
        """
        Iterate through the temp_data and find the last day that the average temperature
        is within the APP_RANGE values.
        """
        current_date += timedelta(days=1)
        average_temp = (temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] + temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2
    
    my_apps[-1]['end_date'] = current_date
    
    
    ### SECOND FALL APPLICATION ###
    APPLY_ABOVE = 32 # degrees F
    APPLY_DAYS_BEFORE_TEMP = 14 # days before average temp is 32 degrees F
    my_apps.append(None)
    print(closest_station.name)
    
    low_temp = None
    app_date = None
    while (current_date < planner.seasons_dates['fall'][1]):
        """
        Iterate through the temp_data and find the first day that the TMIN temperature
        is above the APP_ABOVE value. If none is found, than use the last day of fall.
        """
        low_temp = temp_data[current_date.strftime('%Y-%m-%d')]['TMIN']
        if (low_temp <= APPLY_ABOVE):
            app_date = current_date - timedelta(days=APPLY_DAYS_BEFORE_TEMP)
            break
        
        current_date += timedelta(days=1)
    
    if app_date == None:
        """
        If this weather station temps never reach the APPLY_ABOVE threshold, then
        the app_date will be APPLY_DAYS_BEFORE_TEMP days before the last day of fall
        """
        app_date = planner.seasons_dates['fall'][1] - timedelta(days=APPLY_DAYS_BEFORE_TEMP)
    
    # low_temp = APPLY_ABOVE + 1
    # while (low_temp > APPLY_ABOVE):
    #     """
    #     Iterate through the temp_data and find the first day that the TMIN temperature
    #     is above the APP_ABOVE value.
    #     """
    #     current_date += timedelta(days=1)
    #     print(low_temp, current_date)
    #     low_temp = temp_data[current_date.strftime('%Y-%m-%d')]['TMIN']

    app_date = current_date - timedelta(days=APPLY_DAYS_BEFORE_TEMP)
    my_apps[-1] = {'date':app_date, 'rate':APP_RATE, 'end_date':None}
    
    return my_apps

def summer_apps(closest_station, temp_data, between_dates):
    """
    Summer Application plan is to put down one application of .75lb Nitrogen per
    1000 sf right between the Fall and Spring applications. 
    """
    
    APP_RATE = .75 # lb per 1000 sf
    
    my_apps = []
    
    days_between_apps = between_dates[1] - between_dates[0]
    
    mid_app_date = between_dates[0] + (days_between_apps / 2)
    start_app_date = mid_app_date - timedelta(days=7)
    end_app_date = mid_app_date + timedelta(days=7)
    
    my_apps.append({'date':start_app_date, 'rate':APP_RATE, 'end_date':end_app_date})
    
    return my_apps
    

def get_fertilizer_info(closest_station, temp_data):
    
    """
    This function iterates through the temperature data of the closest station
    and returns the applicable fertilzier info
    """
    
    fertilizer_info = OrderedDict([
        
        ('spring',[]),
        ('summer',[]),
        ('fall',[]),
    ])
    
    # Add spring applications
    spring_applications = spring_apps(closest_station, temp_data)
    fertilizer_info['spring'].extend(spring_applications)
    
    # Add fall applications
    fall_applications = fall_apps(closest_station, temp_data)
    fertilizer_info['fall'].extend(fall_applications)
    
    # Add summer applications
    between_dates = [spring_applications[0]['date'], fall_applications[0]['date']]
    summer_applications = summer_apps(closest_station, temp_data, between_dates)
    fertilizer_info['summer'].extend(summer_applications)
    
    return fertilizer_info