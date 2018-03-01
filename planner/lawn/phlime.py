"""
Calculates the pH and lime information for the given lawn
"""

# import statements
from datetime import timedelta
from collections import OrderedDict
from . import lawnplanner, lawnutils

import logging
logger = logging.getLogger(__name__)


def lime_apps(closest_station, lawn, fert_apps):
    """
    :param closest_station: the station to pull the weather data from
    :param lawn: will use the needed lime lbs
    :return: a list of lime applications
    """
    logger.debug("lime_apps - Lawn: %s, Station: %s" % (lawn, closest_station))
    my_apps = []
    if lawn.lime == 0:
        return my_apps

    # First application in spring halfway between spring N app and next N app.
    # Second application in fall, between both fall N apps.

    first_n_date = fert_apps['spring'][0]['date']
    if len(fert_apps['spring']) > 1:
        second_n_date = fert_apps['spring'][1]['date']
    else:
        second_n_date = fert_apps['summer'][0]['date']

    days_btwn_n_apps = second_n_date - first_n_date
    first_lime_date = first_n_date + (days_btwn_n_apps / 2)

    first_n_date = fert_apps['fall'][0]['date']
    second_n_date = fert_apps['fall'][1]['date']
    days_btwn_n_apps = second_n_date - first_n_date
    second_lime_date = first_n_date + (days_btwn_n_apps / 2)

    lime_rate = lawn.lime
    if lime_rate > 100:
        lime_rate = 100
    if lime_rate > 50:
        first_lime_rate = 50
    else:
        first_lime_rate = lime_rate
    second_lime_rate = lime_rate - first_lime_rate

    my_apps.append({'date': first_lime_date, 'rate': first_lime_rate, 'nutrient': 'Lime', 'end_date': None})
    if second_lime_rate > 0:
        my_apps.append({'date': second_lime_date, 'rate': second_lime_rate, 'nutrient': 'Lime', 'end_date': None})

    return my_apps


def get_phlime_info(planner, closest_station, lawn):
    """
    This function iterates through the temperature data of the closest station and uses the fertilizer application
    schedule to return the applicable pH & Lime info
    """
    logger.debug("get_phlime_info - Lawn: %s, Station: %s" % (lawn, closest_station))

    phlime_info = {
        'apps': None,
        'description': None
    }

    # Fertilizer Applications
    phlime_info['apps'] = OrderedDict([

        ('spring', []),
        ('summer', []),
        ('fall', []),
    ])

    # Add lime applications
    lime_applications = lime_apps(closest_station, lawn, planner.fertilizer_info['apps'])
    for app in lime_applications:
        season = lawnplanner.season_of_date(app['date'])
        phlime_info['apps'][season].append(app)

    # Finalize applications and add to planner
    for season in phlime_info['apps']:
        for app in phlime_info['apps'][season]:
            app['total_lbs'] = lawnutils.round_to_quarter((lawn.size / 1000) * app['rate'])

            if app['end_date'] is None:
                task_name = "Amend Soil with %s lbs of %s" % (str(app['total_lbs']), app['nutrient'])
                app['title'] = task_name
            else:
                task_name = "%s - Amend Soil with %s lbs of %s" % \
                            (app['end_date'].strftime("%B %d").replace(" 0", " "), str(app['total_lbs']),
                             app['nutrient'])
                app['title'] = task_name

            planner.add_task(task_name, app['date'])

    # Generate the PH Lime Description to be displayed on the detail page.
    phlime_info['description'] = (
        "Lime application rates assume a CCE of 100. Read the label of your specific product for your CCE. "
        "If your lime source is close to 100 CCE, you do not need to adjust the recommended amount. "
        "In the event that you use a lime source with a CCE well below or above 100, use the following formula "
        "to adjust the required amount: Actual Lime to Apply = Planner recommendation * 100 / CCE of your product. "
    )

    return phlime_info
