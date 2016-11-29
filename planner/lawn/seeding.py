# seeding.py
# Patrick W. Montgomery
# created: 10/3/2016

"""
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
import os
import json
import math
import requests
from datetime import date, datetime, timedelta
from . import lawnutils

GRASS_TYPES = (
    ("KBG","Kentucky Bluegrass"),
    ("PRG","Perennial Ryegrass"),
    ("TTTF", "Turf Type Tall Fescue"),
    )
    
grass_details = {
    
                "KBG":{
                    "name":"Kentucky Bluegrass", 
                    "seed_min_temp":44.0, 
                    "seed_max_temp":76.0, 
                    "germination_time":30, 
                    "seed_new_lb_range":[2.0,3.0],
                    "seed_over_lb_range":[1.0,1.5],
                    
                },
                "PRG":{
                    "name":"Perennial Ryegrass", 
                    "seed_min_temp":44.0, 
                    "seed_max_temp":76.0, 
                    "germination_time":10,
                    "seed_new_lb_range":[4.0,5.0],
                    "seed_over_lb_range":[2.0,2.5],
                },
                "TTTF":{
                    "name":"Turf Type Tall Fescue", 
                    "seed_min_temp":44.0, 
                    "seed_max_temp":76.0, 
                    "germination_time":12,
                    "seed_new_lb_range":[6.0,8.0],
                    "seed_over_lb_range":[3.0,4.0],
                },
}

def get_seeding_info(closest_station, temp_data, grass_type):
    """
    This function was built to take the zip code and grass type as parameters,
    and return the expecting seeding dates for that grass type based on the
    Normal Daily temperatures (NOAA dataset) of the closest weather station.
    """
    
    grass_name = grass_details[grass_type]["name"]
    seed_min_temp = grass_details[grass_type]["seed_min_temp"]
    seed_max_temp = grass_details[grass_type]["seed_max_temp"]
    germination_time = grass_details[grass_type]["germination_time"]
    seed_new_lb_range = grass_details[grass_type]["seed_new_lb_range"]
    seed_over_lb_range = grass_details[grass_type]["seed_over_lb_range"]
    
    """
    Below iterates through the temp_data for each date, and looks for windows of
    germination_time days or longer where the temperature is within the seeding
    threshold range.
    
    !!!!!!!!!!!!!!!!!!!!NEED TO ADD: check the "wrap around" to see if a window exists
    from December to January.
    """
    
    current_date = closest_station.mindate
    current_year = current_date.year
    
    seed_window = 0   #   This is a variable to track the length of the current seeding window
    seeding_dates = []
    
    while (current_date.year == current_year):

        if (temp_data[current_date.strftime('%Y-%m-%d')]["TMIN"] >= seed_min_temp and
            temp_data[current_date.strftime('%Y-%m-%d')]["TMAX"] <= seed_max_temp):
                
                seed_window += 1
                
                if seed_window >= germination_time:
                    # add germination_time days ago to seeding_dates
                    good_seeding_date = current_date - timedelta(days=germination_time)
                    seeding_dates.append(good_seeding_date)
        else:
            seed_window = 0
        
        current_date += timedelta(days=1)
    
    # check the wrap around here!!
    
    """
    Below groups seeding date ranges.
    For example seed between 2010-04-19 and 2010-04-27 (9 days)
    """
    
    seed_ranges = []
    if len(seeding_dates) > 0:
        start_date = seeding_dates[0]
        for i, curr_date in enumerate(seeding_dates):
            if (curr_date - seeding_dates[i-1]).days > 1:
                end_date = seeding_dates[i-1]
                seed_ranges.append([start_date, end_date])
                start_date = curr_date
        
        # the last date in the list is the last end date.
        end_date = seeding_dates[-1]
        seed_ranges.append([start_date, end_date])
    
    seeding_info = {
        
        'closest_station':closest_station,
        'germination_time':germination_time,
        'seed_ranges':seed_ranges,
        'seed_new_lb_range':seed_new_lb_range,
        'seed_over_lb_range':seed_over_lb_range,
    }
    
    return seeding_info
    
def OLD_get_seeding_info(zip_code, grass_type):
    """
    This function was built to take the zip code and grass type as parameters,
    and return the expecting seeding dates for that grass type based on the
    Normal Daily temperatures (NOAA dataset) of the closest weather station.
    """

    #   Load the stations from the data file.
    file_dir = os.path.dirname(os.path.realpath(__file__)) + "/NormalDailyStations.dat"
    stations_file = open(file_dir, "r")
    stations_file_title = stations_file.readline()
    stations_file_updated = stations_file.readline()
    
    stations = json.loads(stations_file.read())
    stations_file.close()
    
    # get the users zip code, and look up the latitude and longitude
    my_lat, my_long = utils.get_lat_long(zip_code)
    
    """
    Below finds the closest station to the zip code by finding the distance
    between two points.
    """
    
    min_distance = 100
    closest_station = None
    for station in stations:
        delta_lat = my_lat - station['latitude']
        delta_long = my_long - station['longitude']
        distance = math.sqrt(delta_lat**2+delta_long**2)
        
        if distance < min_distance:
            min_distance = distance
            closest_station = station
            
    
    """
    Below pulls the Normal Daily date from the closest station
    """
    
    #token = "KCAsygyVaVBxjhTOgyYnMCEOjKVOnCIj" pmontgo33@gmail.com token
    token = "pRciHRBTwdPoyMKflOPcUdTKYiGEzWbn" # pmontgo.33@gmail.com token
    
    headers = {'token':token, 'User-Agent':"lawn care planner"}
    url_base = "http://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    
    payload = {
            "datasetid":"NORMAL_DLY",            #required
            "datatypeid":["DLY-TMIN-NORMAL","DLY-TMAX-NORMAL"],
            "locationid":None,
            "stationid":closest_station['id'],
            "startdate":closest_station['mindate'],       #required
            "enddate":closest_station['maxdate'],         #required
            "units":"standard",
            "sortfield":None,
            "sortorder":None,
            "limit":"1000",
            "offset":None,
            "includemetadata":None
    }
    
    response = requests.get(url_base, headers=headers, params=payload)
    station_temps = response.json()['results']
    
    grass_name = grass_details[grass_type]["name"]
    seed_min_temp = grass_details[grass_type]["seed_min_temp"]
    seed_max_temp = grass_details[grass_type]["seed_max_temp"]
    germination_time = grass_details[grass_type]["germination_time"]
    seed_new_lb_range = grass_details[grass_type]["seed_new_lb_range"]
    seed_over_lb_range = grass_details[grass_type]["seed_over_lb_range"]
    
    """
    Below takes the raw data from the closet station Normals Daily, and organizes
    it into a dictionary where the date is the key, and the value is a dictionary with
    keys TMIN and TMAX
    """
    
    temp_data = {}
    
    for day_temp in station_temps:
        my_date = datetime.strptime(day_temp['date'][:10], "%Y-%m-%d").date()
        if my_date not in temp_data.keys():
            temp_data[my_date] = {"TMIN":None, "TMAX":None}
        
        if day_temp["datatype"] == "DLY-TMIN-NORMAL":
            temp_data[my_date]["TMIN"] = day_temp["value"]
        elif day_temp["datatype"] == "DLY-TMAX-NORMAL":
            temp_data[my_date]["TMAX"] = day_temp["value"]
        else:
            print("NOT A MIN OR MAX TEMPURATURE!!!")
            # this should throw an error.
            
    """
    Below iterates through the temp_data for each date, and looks for windows of
    germination_time days or longer where the temperature is within the seeding
    threshold range.
    
    !!!!!!!!!!!!!!!!!!!!NEED TO ADD: check the "wrap around" to see if a window exists
    from December to January.
    """
    
    current_date = datetime.strptime(closest_station['mindate'], "%Y-%m-%d").date()
    current_year = current_date.year
    
    seed_window = 0   #   This is a variable to track the length of the current seeding window
    seeding_dates = []
    
    while (current_date.year == current_year):
    #    print(current_date, temp_data[current_date])
        
        if (temp_data[current_date]["TMIN"] >= seed_min_temp and
            temp_data[current_date]["TMAX"] <= seed_max_temp):
                
                seed_window += 1
                
                if seed_window >= germination_time:
                    #add germination_time days ago to seeding_dates
                    good_seeding_date = current_date - timedelta(days=germination_time)
                    seeding_dates.append(good_seeding_date)
        else:
            seed_window = 0
        
        current_date += timedelta(days=1)
    
    # check the wrap around here!!
    
    """
    Below groups seeding date ranges.
    For example seed between 2010-04-19 and 2010-04-27 (9 days)
    """
    seed_ranges = []
    
    start_date = seeding_dates[0]
    for i, curr_date in enumerate(seeding_dates):
        if (curr_date - seeding_dates[i-1]).days > 1:
            end_date = seeding_dates[i-1]
            seed_ranges.append([start_date, end_date])
            start_date = curr_date
    
    # the last date in the list is the last end date.
    end_date = seeding_dates[-1]
    seed_ranges.append([start_date, end_date])
    
    seeding_info = {
        
        'closest_station':closest_station,
        'germination_time':germination_time,
        'seed_ranges':seed_ranges,
        'seed_new_lb_range':seed_new_lb_range,
        'seed_over_lb_range':seed_over_lb_range,
    }
    
    return seeding_info

def terminal_app():
    
    #   Load the stations from the data file.
    file_dir = os.path.dirname(os.path.realpath(__file__)) + "/NormalDailyStations.dat"
    stations_file = open(file_dir, "r")
    stations_file_title = stations_file.readline()
    stations_file_updated = stations_file.readline()
    
    stations = json.loads(stations_file.read())
    
    # get the users zip code, and look up the latitude and longitude
    zip = utils.get_zip_code()
    my_lat, my_long = utils.get_lat_long(zip)
    
    
    """
    Below finds the closest station to the zip code by finding the distance
    between two points.
    """
    
    min_distance = 100
    closest_station = None
    for station in stations:
        delta_lat = my_lat - station['latitude']
        delta_long = my_long - station['longitude']
        distance = math.sqrt(delta_lat**2+delta_long**2)
        
        if distance < min_distance:
            min_distance = distance
            closest_station = station
        
    print("Your closest weather station is %s." % (closest_station["name"]))
    
    
    """
    Below pulls the Normal Daily date from the closest station
    """
    
    #token = "KCAsygyVaVBxjhTOgyYnMCEOjKVOnCIj" pmontgo33@gmail.com token
    token = "pRciHRBTwdPoyMKflOPcUdTKYiGEzWbn" # pmontgo.33@gmail.com token
    
    headers = {'token':token, 'User-Agent':"lawn care planner"}
    url_base = "http://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    
    payload = {
            "datasetid":"NORMAL_DLY",            #required
            "datatypeid":["DLY-TMIN-NORMAL","DLY-TMAX-NORMAL"],
            "locationid":None,
            "stationid":closest_station['id'],
            "startdate":closest_station['mindate'],       #required
            "enddate":closest_station['maxdate'],         #required
            "units":"standard",
            "sortfield":None,
            "sortorder":None,
            "limit":"1000",
            "offset":None,
            "includemetadata":None
    }
    
    print("retrieving data...")
    response = requests.get(url_base, headers=headers, params=payload)
    print("data retrieved!")
    print(response.status_code)
    station_temps = response.json()['results']
    
    grass_type_abv = utils.get_grass_type()
    
    grass_type = grass_details[grass_type_abv]["name"]
    seed_min_temp = grass_details[grass_type_abv]["seed_min_temp"]
    seed_max_temp = grass_details[grass_type_abv]["seed_max_temp"]
    germination_time = grass_details[grass_type_abv]["germination_time"]
    
    
    """
    Below takes the raw data from the closet station Normals Daily, and organizes
    it into a dictionary where the date is the key, and the value is a dictionary with
    keys TMIN and TMAX
    """
    
    temp_data = {}
    
    for day_temp in station_temps:
        my_date = datetime.strptime(day_temp['date'][:10], "%Y-%m-%d").date()
        if my_date not in temp_data.keys():
            temp_data[my_date] = {"TMIN":None, "TMAX":None}
        
        if day_temp["datatype"] == "DLY-TMIN-NORMAL":
            temp_data[my_date]["TMIN"] = day_temp["value"]
        elif day_temp["datatype"] == "DLY-TMAX-NORMAL":
            temp_data[my_date]["TMAX"] = day_temp["value"]
        else:
            print("NOT A MIN OR MAX TEMPURATURE!!!")
            # this should throw an error.
    
    
    """
    Below iterates through the temp_data for each date, and looks for windows of
    germination_time days or longer where the temperature is within the seeding
    threshold range.
    
    !!!!!!!!!!!!!!!!!!!!NEED TO ADD: check the "wrap around" to see if a window exists
    from December to January.
    """
    
    current_date = datetime.strptime(closest_station['mindate'], "%Y-%m-%d").date()
    current_year = current_date.year
    
    seed_window = 0   #   This is a variable to track the length of the current seeding window
    seeding_dates = []
    
    while (current_date.year == current_year):
    #    print(current_date, temp_data[current_date])
        
        if (temp_data[current_date]["TMIN"] >= seed_min_temp and
            temp_data[current_date]["TMAX"] <= seed_max_temp):
                
                seed_window += 1
                
                if seed_window >= germination_time:
                    #add germination_time days ago to seeding_dates
                    good_seeding_date = current_date - timedelta(days=germination_time)
                    seeding_dates.append(good_seeding_date)
        else:
            seed_window = 0
        
        current_date += timedelta(days=1)
    
    # check the wrap around here!!
    #print(seeding_dates)
    
    """
    Below groups seeding date ranges.
    For example seed between 2010-04-19 and 2010-04-27 (9 days)
    """
    seed_ranges = []
    
    start_date = seeding_dates[0]
    for i, curr_date in enumerate(seeding_dates):
        if (curr_date - seeding_dates[i-1]).days > 1:
            end_date = seeding_dates[i-1]
            seed_ranges.append([start_date, end_date])
            start_date = curr_date
    
    # the last date in the list is the last end date.
    end_date = seeding_dates[-1]
    seed_ranges.append([start_date, end_date])
    
    """
    Below just displays the best date ranges for seeding.
    """
    
    seed_from = seed_ranges[0][0].strftime("%m-%d")
    seed_to = seed_ranges[0][1].strftime("%m-%d")
    
    message = "The best time to seed your %s is " % (grass_type)
    message += "from %s to %s" % (seed_from, seed_to)

    for seed_range in seed_ranges[1:-2]:
        seed_from = seed_range[0].strftime("%m-%d")
        seed_to = seed_range[1].strftime("%m-%d")
        message += ", from %s to %s" % (seed_from, seed_to)

    seed_from = seed_ranges[-1][0].strftime("%m-%d")
    seed_to = seed_ranges[-1][1].strftime("%m-%d")
    message += " or from %s to %s" % (seed_from, seed_to)

    print(message)
    return message


"""
If the file is run directly, run the terminal_app.
"""
if __name__ == '__main__':
    terminal_app()