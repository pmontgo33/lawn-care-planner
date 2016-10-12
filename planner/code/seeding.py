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
import requests
import re
import os
from bs4 import BeautifulSoup
import json
import math
from datetime import date, datetime, timedelta


GRASS_TYPES = (
    ("KBG","Kentucky Bluegrass"),
    ("PRG","Perennial Ryegrass"),
    ("TTTF", "Turf Type Tall Fescue"),
    )
    
grass_details = {
                "KBG":{"name":"Kentucky Bluegrass", "seed_min_temp":44.0, "seed_max_temp":76.0, "germination_time":30},
                "PRG":{"name":"Perennial Ryegrass", "seed_min_temp":44.0, "seed_max_temp":76.0, "germination_time":10},
                "TTTF":{"name":"Turf Type Tall Fescue", "seed_min_temp":44.0, "seed_max_temp":76.0, "germination_time":12},
                }

def update_normal_daily_stations():
    """
    This function updates the data file NormalDailyStations.dat (or creates it 
    if it does not exist) with the latest NOAA stations that support the 
    Normals Daily dataset.
    """
    
    token = "KCAsygyVaVBxjhTOgyYnMCEOjKVOnCIj"
    headers = {'token':token, 'User-Agent':"lawn-care-planner"}
    
    station_url = "http://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
    payload = {
        "datasetid": "NORMAL_DLY",  #   return list of stations that have Normal Daily data
        "limit": "1000",
        "offset": None,
    }
    
    response = requests.get(station_url, headers=headers, params=payload)
    
    stations = response.json()['results']
    
    count = response.json()['metadata']['resultset']['count']
    limit = response.json()['metadata']['resultset']['limit']
    offset = response.json()['metadata']['resultset']['offset']
    
    while (limit+offset < count):
        payload['offset'] = limit+offset
        response = requests.get(station_url, headers=headers, params=payload)
        stations.extend(response.json()['results'])
        
        count = response.json()['metadata']['resultset']['count']
        limit = response.json()['metadata']['resultset']['limit']
        offset = response.json()['metadata']['resultset']['offset']
    
    file_dir = os.path.dirname(os.path.realpath(__file__)) + "/NormalDailyStations.dat"
    view_data = open(file_dir, "w")
    view_data.write("Normal Daily Stations List\nUpdated: %s\n" % date.today())
    view_data.write(json.dumps(stations, sort_keys=True, indent=4))
    view_data.close()
    
def get_zip_code():
    """
    This function asks for input from the terminal for the users zip code.
    Eventually this function will be replaced by a different method of gaining
    input. ex - a form on a webpage.
    """
    zip = input("Enter ZIP code: ")
    return int(zip)
    
def get_lat_long(zip):
    """
    This function takes a zip code and looks up the latitude and longitude using
    this website: https://www.melissadata.com/lookups/GeoCoder.asp?InData=19075&submit=Search
    """
    
    zip_url = "https://www.melissadata.com/lookups/GeoCoder.asp"
    headers = {'User-Agent':"lawn-care-planner"}
    payload = {
        "InData":zip,
        "submit":"Search",
    }
    
    response = requests.get(zip_url, headers=headers, params=payload)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Check to make sure zip code exists. If so return None, None
    if (len(soup.find_all(text=re.compile("Lat & Long for  was not found."))) > 0
        or len(soup.find_all(text=re.compile("Invalid address."))) > 0):
        return None, None
    
    results = soup.find_all("td", attrs={"class":"padd"})
    
    lat = float(results[0].text)
    long = float(results[1].text)
    
    return lat, long

def get_grass_type():
    """
    This function asks for input from the terminal for the users grass type.
    Eventually this function will be replaced by a different method of gaining
    input. ex - a form on a webpage.
    """
    
    grass_type = input("Enter your grass type (KBG, PRG, TTTF): ")
    return grass_type.upper()

def get_seeding_info(zip_code, grass_type):
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
    
    # get the users zip code, and look up the latitude and longitude
    my_lat, my_long = get_lat_long(zip_code)
    
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
    
    token = "KCAsygyVaVBxjhTOgyYnMCEOjKVOnCIj"
    headers = {'token':token, 'User-Agent':"noaa api test"}
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
    zip = get_zip_code()
    my_lat, my_long = get_lat_long(zip)
    
    
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
    
    token = "KCAsygyVaVBxjhTOgyYnMCEOjKVOnCIj"
    headers = {'token':token, 'User-Agent':"noaa api test"}
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
    
    station_temps = response.json()['results']
    
    grass_type_abv = get_grass_type()
    
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
#    print("The best time to seed your %s is " % (grass_type), end="")
#    print("from %s to %s" % (seed_from, seed_to), end="")
    
    for seed_range in seed_ranges[1:-2]:
        seed_from = seed_range[0].strftime("%m-%d")
        seed_to = seed_range[1].strftime("%m-%d")
        message += ", from %s to %s" % (seed_from, seed_to)
#        print(", from %s to %s" % (seed_from, seed_to), end="")
    
    seed_from = seed_ranges[-1][0].strftime("%m-%d")
    seed_to = seed_ranges[-1][1].strftime("%m-%d")
    message += " or from %s to %s" % (seed_from, seed_to)
#    print(" or from %s to %s" % (seed_from, seed_to))
    
    print(message)
    return message
    """
    view_data = open("ViewData.txt", "w")
    view_data.write(json.dumps(response.json(), sort_keys=True, indent=4))
    view_data.close()
    """
