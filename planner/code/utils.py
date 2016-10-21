# utils.py
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


def get_closest_station_data(zip_code):
    
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