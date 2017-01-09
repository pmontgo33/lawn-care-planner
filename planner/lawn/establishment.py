"""
lawn\establishment.py

formerly seeding.py until warm season grasses were added.

This app takes a ZIP code and a grass type from the user, and returns the best
dates to plant grass seed.

Lat & Long of zip are pulled from:
https://www.melissadata.com/lookups/GeoCoder.asp?InData=19075&submit=Search

Station Lat & Long are pulled from NOAA:
http://www.ncdc.noaa.gov/cdo-web/webservices/v2#stations

Closest station will be located by taking the distance between two points, and
returning the smallest.
"""

#   import statements
from datetime import timedelta
from . import lawnutils

"""
with open('planner/lawn/grass_details.dat') as json_data:
    grass_details = json.load(json_data)


def output_grass_details():
    import json

    with open('planner/lawn/grass_details.dat', 'w') as outfile:
        json.dump(grass_details, outfile, sort_keys=True, indent=4)
"""


def get_establishment_info(planner, closest_station, lawn):
    """
    This function was built to take the closest_station and grass type as parameters,
    and return the expecting seeding dates for that grass type based on the
    Normal Daily temperatures (NOAA dataset) of the closest weather station.
    """

    establishment_info = {}
    if lawn.grass_type.seed:
        establishment_info['seed_ranges'] = get_seed_ranges(planner, closest_station, lawn)
    if lawn.grass_type.plugs:
        establishment_info['plugs_ranges'] = get_plugs_ranges(planner, closest_station, lawn)

    return establishment_info


def get_seed_ranges(planner, closest_station, lawn):
    seed_min_temp = lawn.grass_type.specs['seed_min_temp']
    seed_max_temp = lawn.grass_type.specs['seed_max_temp']
    germination_time = lawn.grass_type.specs['germination_time']
    seed_new_lb_range = lawn.grass_type.specs['seed_new_lb_range']
    seed_over_lb_range = lawn.grass_type.specs['seed_over_lb_range']

    """
    Below iterates through the temp_data for each date, and looks for windows of
    germination_time days or longer where the temperature is within the seeding
    threshold range.
    """

    current_date = closest_station.mindate
    current_year = current_date.year

    seed_window = 0  # This is a variable to track the length of the current seeding window
    seeding_dates = []

    while current_date.year == current_year:

        if (closest_station.temp_data[current_date.strftime('%Y-%m-%d')]["TMIN"] >= seed_min_temp and
                    closest_station.temp_data[current_date.strftime('%Y-%m-%d')]["TMAX"] <= seed_max_temp):

            seed_window += 1

            if seed_window >= germination_time:
                # add germination_time days ago to seeding_dates
                good_seeding_date = current_date - timedelta(days=germination_time)
                seeding_dates.append(good_seeding_date)
        else:
            seed_window = 0

        current_date += timedelta(days=1)

    """
    Below groups seeding date ranges.
    For example seed between 2010-04-19 and 2010-04-27 (9 days)
    """

    seed_ranges = []
    if len(seeding_dates) > 0:
        start_date = seeding_dates[0]
        for i, curr_date in enumerate(seeding_dates):
            if (curr_date - seeding_dates[i - 1]).days > 1:
                end_date = seeding_dates[i - 1]
                seed_ranges.append([start_date, end_date])
                start_date = curr_date

        # the last date in the list is the last end date.
        end_date = seeding_dates[-1]
        seed_ranges.append([start_date, end_date])

    str_ranges = []
    if len(seed_ranges) > 0:
        for first_day, last_day in seed_ranges:
            str_ranges.append(first_day.strftime("%B %d").replace(" 0", " ") +
                              " to " + last_day.strftime("%B %d").replace(" 0", " "))

            planner.add_task("First day to seed", first_day)
            planner.add_task("Last day to seed", last_day)
    else:

        """
        The WARM_COOL_LATITUDE_THRESHOLD value is used when no valid seeding ranges
        are available for the provided lawn. This is due to the temperatures in the
        lawn location being too warm to support the grass type, or too cool to support
        the grass type. If the lawn is located above this threshold it is too cool.
        If the lawn is located below this threshold it is too warm.
        """
        WARM_COOL_LATITUDE_THRESHOLD = 40  # degrees

        warm_or_cool = ""
        if closest_station.latitude >= WARM_COOL_LATITUDE_THRESHOLD:
            warm_or_cool = "cool"
        else:
            warm_or_cool = "warm"

        str_ranges.append(
            "No possible seeding dates exist! The lawn location is too %s to grow this grass type." % (warm_or_cool))

    # Amount of seed based on size of lawn, rounded to nearest quarter lb
    lawn.seed_new_lb_range = [lawnutils.round_to_quarter(x * (lawn.size / 1000)) for x in
                              seed_new_lb_range]
    lawn.seed_over_lb_range = [lawnutils.round_to_quarter(x * (lawn.size / 1000)) for x in
                               seed_over_lb_range]

    return str_ranges


def get_plugs_ranges(planner, closest_station, lawn):
    return None

def OLD_get_seeding_info(planner, closest_station, lawn):
    """
    This function was built to take the closest_station and grass type as parameters,
    and return the expecting seeding dates for that grass type based on the
    Normal Daily temperatures (NOAA dataset) of the closest weather station.
    """

    seed_min_temp = lawn.grass_type.specs['seed_min_temp']
    seed_max_temp = lawn.grass_type.specs['seed_max_temp']
    germination_time = lawn.grass_type.specs['germination_time']
    seed_new_lb_range = lawn.grass_type.specs['seed_new_lb_range']
    seed_over_lb_range = lawn.grass_type.specs['seed_over_lb_range']

    """
    Below iterates through the temp_data for each date, and looks for windows of
    germination_time days or longer where the temperature is within the seeding
    threshold range.
    """

    current_date = closest_station.mindate
    current_year = current_date.year

    seed_window = 0  # This is a variable to track the length of the current seeding window
    seeding_dates = []

    while current_date.year == current_year:

        if (closest_station.temp_data[current_date.strftime('%Y-%m-%d')]["TMIN"] >= seed_min_temp and
                    closest_station.temp_data[current_date.strftime('%Y-%m-%d')]["TMAX"] <= seed_max_temp):

            seed_window += 1

            if seed_window >= germination_time:
                # add germination_time days ago to seeding_dates
                good_seeding_date = current_date - timedelta(days=germination_time)
                seeding_dates.append(good_seeding_date)
        else:
            seed_window = 0

        current_date += timedelta(days=1)

    """
    Below groups seeding date ranges.
    For example seed between 2010-04-19 and 2010-04-27 (9 days)
    """

    seed_ranges = []
    if len(seeding_dates) > 0:
        start_date = seeding_dates[0]
        for i, curr_date in enumerate(seeding_dates):
            if (curr_date - seeding_dates[i - 1]).days > 1:
                end_date = seeding_dates[i - 1]
                seed_ranges.append([start_date, end_date])
                start_date = curr_date

        # the last date in the list is the last end date.
        end_date = seeding_dates[-1]
        seed_ranges.append([start_date, end_date])

    str_ranges = []
    if len(seed_ranges) > 0:
        for first_day, last_day in seed_ranges:
            str_ranges.append(first_day.strftime("%B %d").replace(" 0", " ") +
                              " to " + last_day.strftime("%B %d").replace(" 0", " "))

            planner.add_task("First day to seed", first_day)
            planner.add_task("Last day to seed", last_day)
    else:

        """
        The WARM_COOL_LATITUDE_THRESHOLD value is used when no valid seeding ranges
        are available for the provided lawn. This is due to the temperatures in the
        lawn location being too warm to support the grass type, or too cool to support
        the grass type. If the lawn is located above this threshold it is too cool.
        If the lawn is located below this threshold it is too warm.
        """
        WARM_COOL_LATITUDE_THRESHOLD = 40  # degrees

        warm_or_cool = ""
        if closest_station.latitude >= WARM_COOL_LATITUDE_THRESHOLD:
            warm_or_cool = "cool"
        else:
            warm_or_cool = "warm"

        str_ranges.append(
            "No possible seeding dates exist! The lawn location is too %s to grow this grass type." % (warm_or_cool))

    # Amount of seed based on size of lawn, rounded to nearest quarter lb
    lawn.seed_new_lb_range = [lawnutils.round_to_quarter(x * (lawn.size / 1000)) for x in
                              seed_new_lb_range]
    lawn.seed_over_lb_range = [lawnutils.round_to_quarter(x * (lawn.size / 1000)) for x in
                               seed_over_lb_range]

    seeding_info = {

        'germination_time': germination_time,
        'seed_ranges': str_ranges,
    }

    return seeding_info