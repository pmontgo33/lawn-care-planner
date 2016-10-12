# planner/views.py
# Patrick W. Montgomery
# created: 10-8-2016

# import statements
from datetime import date
from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from .models import Lawn
from .code import seeding, mowing

from .code import seeding

def index(request):
    return render(request, "planner/index.html", {})
    
def lawn_detail(request, pk):
    lawn = get_object_or_404(Lawn, pk=pk)
    """    
    seasons = {
        "spring": [date(2010, 3, 1), date(2010, 5, 31)],
        "summer": [date(2010, 6, 1), date(2010, 8, 31)],
        "fall": [date(2010, 9, 1), date(2010, 11, 30)],
        "winter": [date(2010, 12, 1), date(2010, 2, 28)],
    }
    """    
    """
    This section prepares the Seeding information
    """
    seeding_info = seeding.get_seeding_info(lawn.zip_code, lawn.grass_type)
    
    str_ranges = []
    for range in seeding_info['seed_ranges']:
        str_ranges.append(range[0].strftime("%B %d") +
            " to " + range[1].strftime("%B %d"))
    
    grass_abv = lawn.grass_type
    lawn.grass_type = seeding.grass_details[lawn.grass_type]['name']  
    
    """
    This section prepares the Mowing information
    """
    
    mowing_heights = mowing.heights[grass_abv]
    
    temp_vars = {
        'lawn':lawn,
        'closest_station':seeding_info['closest_station']['name'],
        'germination_time':seeding_info['germination_time'],
        'seeding_ranges':str_ranges,
        'mowing_heights':mowing_heights,
    }
    
    return render(request, 'planner/lawn_detail.html', temp_vars)
    
