# plannerutils.py
# Patrick W. Montgomery
# created: 11-17-2016

# import statements
from django.db.models import Min, F
import math

from planner.models import WeatherStation
from planner.lawn import lawnutils


def get_closest_station_data(zip_code):
    

    # get the users zip code, and look up the latitude and longitude
    my_lat, my_long = lawnutils.get_lat_long(zip_code)
    
    """
    Below finds the closest station to the zip code by finding the distance
    between two points.
    """
    
    delta_lat = my_lat - F('latitude')
    delta_long = my_long - F('longitude')
    distance_equation = (delta_lat**2+delta_long**2)**0.5
    
    """
    This statement queries the database to sort the stations by their distance
    from the zip_code. Then calling query[0] gives the closest station to the zip
    code.
    """
    query = WeatherStation.objects.all().annotate(distance=distance_equation).order_by('distance')
    closest_station = query[0]
    
    return closest_station, closest_station.temp_data

def OLD_get_closest_station_data(zip_code):
    
    stations = WeatherStation.objects.all().iterator()
    
    # get the users zip code, and look up the latitude and longitude
    my_lat, my_long = lawnutils.get_lat_long(zip_code)
    
    """
    Below finds the closest station to the zip code by finding the distance
    between two points.
    """
    
    min_distance = 100
    closest_station = None
    for station in stations:
        delta_lat = my_lat - station.latitude
        delta_long = my_long - station.longitude
        distance = math.sqrt(delta_lat**2+delta_long**2)
        
        if distance < min_distance:
            min_distance = distance
            closest_station = station
            
    
    return closest_station, closest_station.temp_data