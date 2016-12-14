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


def zip_is_valid(zip):
    """
    This function takes a zip code and returns True if it is a valid zip code,
    otherwise it returns False
    """
    search = ZipcodeSearchEngine()
    zip_data = search.by_zipcode(zip)
    
    lat = zip_data['Latitude']
    
    if lat != None:
        return True
    
    return False


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


def get_gdd_date(target_gdd, base_temp, closest_station):
    
    """
    This function calculates the date that the target growing degree days
    are met, based on the provided base and the given temperature data set.
    """
    
    current_date = closest_station.mindate
    current_year = current_date.year
    current_gdd = 0
    
    gdd_date = None
    while current_date.year == current_year:
        average_temp = (closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMIN'] +
                        closest_station.temp_data[current_date.strftime('%Y-%m-%d')]['TMAX']) / 2

        if average_temp >= base_temp:
            daily_gdd = average_temp - base_temp
            current_gdd += daily_gdd
            
            if current_gdd >= target_gdd:
                gdd_date = current_date
                break

        current_date += timedelta(days=1)
    
    return gdd_date


def round_to_quarter(value):
    """
    This function is used to round a value to the nearest quarter.
    Examples:
    3.82 >> 3.75
    6.91 >> 7.0
    5.23 >> 5.25
    2.11 >> 2.0
    """
    return round(value*4)/4