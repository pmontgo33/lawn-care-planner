# lawnutils.py
# Patrick W. Montgomery
# created: 10/21/2016

# import statements
import requests
import re
import os
from bs4 import BeautifulSoup
import json
import math

from datetime import date, datetime, timedelta
from uszipcode import ZipcodeSearchEngine

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
        "datatypeid":["DLY-TMIN-NORMAL","DLY-TMAX-NORMAL"],
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
    the uszipcode package. Documentation: https://pypi.python.org/pypi/uszipcode
    """
    
    search = ZipcodeSearchEngine()
    zip_data = search.by_zipcode(zip)
    
    lat = zip_data['Latitude']
    long = zip_data['Longitude']
    
    return lat, long

def get_grass_type():
    """
    This function asks for input from the terminal for the users grass type.
    Eventually this function will be replaced by a different method of gaining
    input. ex - a form on a webpage.
    """
    
    grass_type = input("Enter your grass type (KBG, PRG, TTTF): ")
    return grass_type.upper()

def OLD_get_closest_station_data(zip_code):
    
#   Load the stations from the data file.
    file_dir = os.path.dirname(os.path.realpath(__file__)) + "/NormalDailyStations.dat"
    stations_file = open(file_dir, "r")
    stations_file_title = stations_file.readline()
    stations_file_updated = stations_file.readline()
    
    stations = json.loads(stations_file.read())
    stations_file.close()
    
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
    
    return closest_station, temp_data
    
def get_gdd_date(target_gdd, base_temp, closest_station, temp_data):
    
    """
    This function calculates the date that the target growing degree days
    are met, based on the provided base and the given temperature data set.
    """
    
    current_date = closest_station.mindate
    current_year = current_date.year
    current_gdd = 0
    
    gdd_date = None
    while (current_date.year == current_year):
        average_temp = (temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] + temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2
        
        if average_temp >= base_temp:
            daily_gdd = average_temp - base_temp
            current_gdd += daily_gdd
            
            if current_gdd >= target_gdd:
                gdd_date = current_date
                break

        current_date += timedelta(days=1)
    
    return gdd_date