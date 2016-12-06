"""
planner/views.py

This file contains the views for the planner app.
"""

# import statements
from datetime import date
import math
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from planner.models import Lawn, WeatherStation, LawnProduct
from planner.forms import LawnForm
from planner.lawn import lawnutils, seeding, mowing, lawnplanner, weedcontrol, insectcontrol, fertilizer
from planner import plannerutils

from .lawn import seeding

def index(request):
    return render(request, "planner/index.html", {})
    
def lawn_detail(request, pk):
    lawn = get_object_or_404(Lawn, pk=pk)
    my_planner = lawnplanner.planner()
    
    # Get the closest station and min/max temperature data for that station based on the ZIP code 
    closest_station, temp_data = plannerutils.get_closest_station_data(lawn.zip_code)

    """
    This section prepares the Seeding information
    """
    
    seeding_info = seeding.get_seeding_info(closest_station, temp_data, lawn.grass_type)
    
    str_ranges = []
    if len(seeding_info['seed_ranges']) > 0:
        for range in seeding_info['seed_ranges']:
            str_ranges.append(range[0].strftime("%B %d").replace(" 0", " ") +
                " to " + range[1].strftime("%B %d").replace(" 0", " "))
            
            my_planner.add_task("First day to seed", range[0])
            my_planner.add_task("Last day to seed", range[1])
    else:
        
        """
        The WARM_COOL_LATITUDE_THRESHOLD value is used when no valid seeding ranges
        are available for the provided lawn. This is due to the temperatures in the
        lawn location being too warm to support the grass type, or too cool to support
        the grass type. If the lawn is located above this threshold it is too cool. 
        If the lawn is located below this threshold it is too warm.
        """
        WARM_COOL_LATITUDE_THRESHOLD = 40 #degrees
        
        warm_or_cool = ""
        if closest_station.latitude >= WARM_COOL_LATITUDE_THRESHOLD:
            warm_or_cool = "cool"
        else:
            warm_or_cool = "warm"
        
        str_ranges.append("No possible seeding dates exist! The lawn location is too %s to grow this grass type." % (warm_or_cool))
    
    grass_abv = lawn.grass_type
    lawn.grass_type = seeding.grass_details[lawn.grass_type]['name']
    
    # Amount of seed based on size of lawn, rounded to nearest quarter lb
    lawn.seed_new_lb_range = [plannerutils.round_to_quarter(x*(lawn.size / 1000)) for x in seeding_info['seed_new_lb_range']]
    lawn.seed_over_lb_range = [plannerutils.round_to_quarter(x*(lawn.size / 1000)) for x in seeding_info['seed_over_lb_range']]
    
    # # Round these figures to the nearest quarter lb
    # lawn.seed_new_lb_range = plannerutils.round_to_quarter(lawn.seed_new_lb_range)
    # lawn.seed_over_lb_range = plannerutils.round_to_quarter(lawn.seed_over_lb_range)
    
    """
    This section prepares the Mowing information
    """
    
    mowing_heights = mowing.heights[grass_abv]
    
    for key in mowing_heights.keys():
        my_season = key
        my_task_name = 'Mow at height of %s"' % (str(mowing_heights[key]['height']))
        if '-' in key:
            my_season = key.split('-')[0]
            my_task_name = 'Mow at height of %s" for %s' % (str(mowing_heights[key]['height']), mowing_heights[key]['title'].lower())
        my_planner.add_task(my_task_name, my_season)

    """
    This section prepares the Fertilizer information
    """
    
    fertilizer_info = fertilizer.get_fertilizer_info(closest_station, temp_data)

    # Fertilizer Applications
    total_fert_lb = 0
    for season in fertilizer_info['apps']:
        for app in fertilizer_info['apps'][season]:
            app['total_lbs'] = plannerutils.round_to_quarter((lawn.size / 1000) * app['rate'])

            if app['end_date'] == None:
                task_name = "Fertilize with %s lbs of Nitrogen" % (str(app['total_lbs']))
                app['title'] = task_name
            else:
                task_name = "%s - Fertilize with %s lbs of Nitrogen" % \
                            (app['end_date'].strftime("%B %d").replace(" 0", " "), str(app['total_lbs']))
                app['title'] = task_name
                app['end_date'] = app['end_date'].strftime("%B %d").replace(" 0", " ")
            
            my_planner.add_task(task_name, app['date'])
            app['date'] = app['date'].strftime("%B %d").replace(" 0", " ")

    # Fertilizer Products
    fert_products = LawnProduct.objects.filter(type='Fertilizer')
    for product in fert_products:
        first_app_total = fertilizer_info['apps']['spring'][0]['total_lbs']
        product_nitrogen = product.specs['npk'][0] / 100

        product.weight = plannerutils.round_to_quarter(first_app_total / product_nitrogen)
        product.specs['npk'] = "(%s-%s-%s)" % \
                                  (product.specs['npk'][0], product.specs['npk'][1], product.specs['npk'][2])

    """
    This section prepares the Weed Control information
    """
    
    weed_info = weedcontrol.get_weed_control_info(closest_station, temp_data)
    summer_weed_deadline = weed_info['summer_deadline'].strftime("%B %d").replace(" 0", " ")
    my_task_name = "Summer annual weed pre-emergent herbicide application deadline."
    my_planner.add_task(my_task_name, weed_info['summer_deadline'])
    
    """
    This section prepares the Insect Control information
    """
    
    insect_info = insectcontrol.get_insect_control_info(closest_station, temp_data)
    grub_deadline = insect_info['grub_deadline'].strftime("%B %d").replace(" 0", " ")
    my_task_name = "Grub worm preventer application deadline."
    my_planner.add_task(my_task_name, insect_info['grub_deadline'])
    
    """
    Take out any months in the planner that have no tasks
    """
    months_to_del = []
    for season in my_planner.tasks_by_season:
        for month in my_planner.tasks_by_season[season]:
            if not my_planner.tasks_by_season[season][month]: # if list is empty
                months_to_del.append((season,month))
    for s_m in months_to_del:
        del my_planner.tasks_by_season[s_m[0]][s_m[1]]
    
    template_vars = {
        'lawn':lawn,
        'closest_station':closest_station.name,
        'germination_time':seeding_info['germination_time'],
        'seed_new_lb_range':seeding_info['seed_new_lb_range'],
        'seed_over_lb_range':seeding_info['seed_over_lb_range'],
        'seeding_ranges':str_ranges,
        'mowing_heights':mowing_heights,
        'summer_weed_deadline':summer_weed_deadline,
        'grub_deadline':grub_deadline,
        'fertilizer_apps':fertilizer_info['apps'],
        'fertilizer_products':fert_products,
        
        'planner':my_planner.tasks_by_season,
    }
    
    return render(request, 'planner/lawn_detail.html', template_vars)
    
def lawn_new(request):

    if request.method == "POST":
        form = LawnForm(request.POST)
        if form.is_valid():
            lawn = form.save(commit=False)
            lawn.user = User.objects.get(username="guest")            #either make this User guest, or look into cookie based sessions.`
            lawn.save()
            lawn.name = "Lawn " + str(lawn.zip_code)
            lawn.save() 
            
            return redirect('lawn_detail', pk=lawn.pk)
    else:
        form = LawnForm()
    return render(request, 'planner/lawn_edit.html', {"form":form})