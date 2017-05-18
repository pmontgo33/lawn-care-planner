# fertilizer.py
# Patrick W. Montgomery
# created: 10/25/2016

"""
See each seasons apps function for the fertilization plan.
"""

# import statements
from datetime import datetime, date, timedelta
from collections import OrderedDict
from . import lawnplanner, lawnutils

import logging
logger = logging.getLogger(__name__)

COOL_SPRING_APPLY_ABOVE = 60 # degrees F
WARM_SPRING_APPLY_ABOVE = 80 # degrees F


def spring_apps(closest_station, lawn):
    """
    Spring Application plan is to put down one application of .75lb Nitrogen per
    1000 sf when the average temperatures get above COOL_SPRING_APPLY_ABOVE or WARM_SPRING_APPLY_ABOVE.
    """

    if lawn.grass_type.season == "Cool Season":
        APPLY_ABOVE = COOL_SPRING_APPLY_ABOVE
    else:
        APPLY_ABOVE = WARM_SPRING_APPLY_ABOVE

    APP_RATE = .75 # lb per 1000 sf
    my_apps = []
    current_date = lawnplanner.seasons_dates['spring'][0]
    current_year = current_date.year
    
    while current_date.year == current_year: # should this be date < end of spring date??????
        """
        Iterate through the temp_data and find the first day that the average temperature
        is above the APPLY_ABOVE value. We only need the first day, so then the loop breaks
        """
        average_temp = (closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] +
                        closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2
        
        if average_temp >= APPLY_ABOVE:
            my_apps.append({'date':current_date, 'rate':APP_RATE, 'end_date':None})
            break
        
        current_date += timedelta(days=1)
    
    return my_apps


def cool_fall_apps(closest_station):
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
    current_date = lawnplanner.seasons_dates['fall'][0]
    current_year = current_date.year
    
    average_temp = (closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] +
                    closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2
    
    while (average_temp > APPLY_RANGE[0]):
        """
        Iterate through the temp_data and find the first day that the average temperature
        is within the APP_RANGE values.
        """
        current_date += timedelta(days=1)
        average_temp = (closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] +
                        closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2
    
    my_apps[-1] = {'date':current_date, 'rate':APP_RATE, 'end_date':None}
    
    while (average_temp > APPLY_RANGE[1]):
        """
        Iterate through the temp_data and find the last day that the average temperature
        is within the APP_RANGE values.
        """
        current_date += timedelta(days=1)
        average_temp = (closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] +
                        closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2
    
    my_apps[-1]['end_date'] = current_date
    
    
    ### SECOND FALL APPLICATION ###
    APPLY_ABOVE = 32 # degrees F
    APPLY_DAYS_BEFORE_TEMP = 14 # days before average temp is 32 degrees F
    my_apps.append(None)

    app_date = None
    while current_date < lawnplanner.seasons_dates['fall'][1]:
        """
        Iterate through the temp_data and find the first day that the TMIN temperature
        is above the APP_ABOVE value. If none is found, than use the last day of fall.
        """
        low_temp = closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMIN']
        if low_temp <= APPLY_ABOVE:
            app_date = current_date - timedelta(days=APPLY_DAYS_BEFORE_TEMP)
            break
        
        current_date += timedelta(days=1)
    
    if app_date is None:
        """
        If this weather station temps never reach the APPLY_ABOVE threshold, then
        the app_date will be APPLY_DAYS_BEFORE_TEMP days before the last day of fall
        """
        app_date = lawnplanner.seasons_dates['fall'][1] - timedelta(days=APPLY_DAYS_BEFORE_TEMP)

    my_apps[-1] = {'date':app_date, 'rate':APP_RATE, 'end_date':None}
    
    return my_apps


def cool_summer_apps(between_dates):
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


def warm_summer_apps(first_app_date, last_app_date):
    """
    Warm Season Summer Application plan is to put down an application of .75lb Nitrogen per
    1000 sf every RANGE_BETWEEN_APPS two times.
    """

    APP_RATE = .75  # lb per 1000 sf
    RANGE_BETWEEN_APPS = (28, 56)
    my_apps = []

    days_btwn_apps = int((last_app_date - first_app_date).days / 3)

    if days_btwn_apps < RANGE_BETWEEN_APPS[0]:
        # One application if there is not time for two
        days_btwn_apps = int((last_app_date - first_app_date).days / 2)
        start_app_date = first_app_date + timedelta(days=days_btwn_apps)
        my_apps.append({'date': start_app_date, 'rate': APP_RATE, 'end_date': None})
    else:
        # Two applications
        start_app_date = first_app_date + timedelta(days=days_btwn_apps)
        my_apps.append({'date': start_app_date, 'rate': APP_RATE, 'end_date': None})

        start_app_date += timedelta(days=days_btwn_apps)
        my_apps.append({'date': start_app_date, 'rate': APP_RATE, 'end_date': None})

    return my_apps


def warm_fall_apps(closest_station):
    """
    Warm Season Fall Application plan is to put down an application of .75lb Nitrogen per
    1000 sf 56 days before low temp reaches 32 degrees F.
    """

    APP_RATE = .75  # lb per 1000 sf
    APPLY_ABOVE = 32  # degrees F
    APPLY_DAYS_BEFORE_TEMP = 42  # days before average temp is 32 degrees F
    my_apps = []
    print(closest_station.name)

    current_date = lawnplanner.seasons_dates['fall'][0]
    app_date = None
    while current_date < lawnplanner.seasons_dates['fall'][1]:
        """
        Iterate through the temp_data and find the first day that the TMIN temperature
        is above the APP_ABOVE value. If none is found, than use the last day of fall.
        """
        low_temp = closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMIN']
        if low_temp <= APPLY_ABOVE:
            app_date = current_date - timedelta(days=APPLY_DAYS_BEFORE_TEMP)
            break

        current_date += timedelta(days=1)

    if app_date is None:
        """
        If this weather station temps never reach the APPLY_ABOVE threshold, then
        the app_date will be APPLY_DAYS_BEFORE_TEMP days before the last day of fall
        """
        app_date = lawnplanner.seasons_dates['fall'][1] - timedelta(days=APPLY_DAYS_BEFORE_TEMP)

    my_apps.append({'date': app_date, 'rate': APP_RATE, 'end_date': None})

    return my_apps


def get_fert_weight(npk, required_nitrogen):
    """
    :param required_nitrogen: this is the required lbs of nitrogen required for the application
    :return: the amount of product required for an application

    This method calculates the required amount of product for an application.
    """
    product_nitrogen = npk['N'] / 100.0
    app_weight = required_nitrogen / product_nitrogen

    return app_weight


def get_fertilizer_info(planner, closest_station, lawn):
    """
    This function iterates through the temperature data of the closest station
    and returns the applicable fertilizer info
    """
    logger.debug("get_fertilizer_info - Lawn: %s, Station: %s" % (lawn, closest_station))

    fertilizer_info = {
        'apps':None,
        'description':None
    }

    # Fertilizer Applications
    fertilizer_info['apps'] = OrderedDict([

        ('spring',[]),
        ('summer',[]),
        ('fall',[]),
    ])

    # Add spring applications
    spring_applications = spring_apps(closest_station, lawn)
    fertilizer_info['apps']['spring'].extend(spring_applications)

    if lawn.grass_type.season == "Cool Season":
        # Add fall applications
        fall_applications = cool_fall_apps(closest_station)
        fertilizer_info['apps']['fall'].extend(fall_applications)

        # Add summer applications
        between_dates = [spring_applications[0]['date'], fall_applications[0]['date']]
        summer_applications = cool_summer_apps(between_dates)
        fertilizer_info['apps']['summer'].extend(summer_applications)
    else:
        # Add fall applications
        fall_applications = warm_fall_apps(closest_station)
        fertilizer_info['apps']['fall'].extend(fall_applications)

        # Add summer applications
        last_app_date = fall_applications[0]['date']

        if len(spring_applications) == 0:
            first_app_date = lawnplanner.seasons_dates['spring'][1]
        else:
            first_app_date = spring_applications[0]['date']
        summer_applications = warm_summer_apps(first_app_date, last_app_date)

        fertilizer_info['apps']['summer'].extend(summer_applications)

    # Finalize applications and add to planner
    for season in fertilizer_info['apps']:
        for app in fertilizer_info['apps'][season]:
            app['total_lbs'] = lawnutils.round_to_quarter((lawn.size / 1000) * app['rate'])

            if app['end_date'] is None:
                task_name = "Fertilize with %s lbs of Nitrogen" % (str(app['total_lbs']))
                app['title'] = task_name
            else:
                task_name = "%s - Fertilize with %s lbs of Nitrogen" % \
                            (app['end_date'].strftime("%B %d").replace(" 0", " "), str(app['total_lbs']))
                app['title'] = task_name
                app['end_date'] = app['end_date'].strftime("%B %d").replace(" 0", " ")

            planner.add_task(task_name, app['date'])
            app['date'] = app['date'].strftime("%B %d").replace(" 0", " ")

    # Generate the Fertilizer Description to be displayed on the detail page.
    if lawn.grass_type.season == "Cool Season":
        fertilizer_info['description'] = (
            "This fertilizer plan is based four applications per year: late Spring, mid Summer, early Fall, and late Fall. "
            "The mid Summer application should only be done if your lawn is properly irrigated. "
            "The dates listed below are based on average historic temperatures in your area. "
            "These should only be used as a guideline, and actual weather forecasts should be used to determine actual dates."
        )
    else:
        fertilizer_info['description'] = (
            "This fertilizer plan is based four applications per year: late Spring, two Summer, and late Fall. "
            "The Summer applications should only be done if your lawn is properly irrigated. "
            "The dates listed below are based on average historic temperatures in your area. "
            "These should only be used as a guideline, and actual weather forecasts should be used to determine actual dates."
        )

    return fertilizer_info
