"""
lawn/mowing.py

This script is used to extract the mowing information from the lawn object.

"""

# import statements
import logging
logger = logging.getLogger(__name__)


def get_mowing_info(planner, closest_station, lawn):
    """
    :param planner: The planner to which the mowing information will be added
    :param closest_station: The station closest to the location provided by the user
    :param lawn: This is the users lawn.
    :return: a dictionary containing all of the mowing information
    """
    logger.debug("get_mowing_info - Lawn: %s, Station: %s" % (lawn, closest_station))
    mowing_heights = lawn.grass_type.mowing

    for key in mowing_heights.keys():
        my_season = key
        my_task_name = 'Mow at height of %s"' % (str(mowing_heights[key]['height']))
        if '-' in key:
            my_season = key.split('-')[0]
            my_task_name = 'Mow at height of %s" for %s' % (str(mowing_heights[key]['height']), mowing_heights[key]['title'].lower())
        planner.add_task(my_task_name, my_season)

    mowing_info = {
        'heights': mowing_heights,
    }
    return mowing_info
