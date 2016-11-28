# planner/views.py
# Patrick W. Montgomery
# created: 10-8-2016

# import statements
from datetime import date
import math
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from planner.models import Lawn, WeatherStation
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
    for range in seeding_info['seed_ranges']:
        str_ranges.append(range[0].strftime("%B %d") +
            " to " + range[1].strftime("%B %d"))
        
        my_planner.add_task("First day to seed", range[0])
        my_planner.add_task("Last day to seed", range[1])
    
    grass_abv = lawn.grass_type
    lawn.grass_type = seeding.grass_details[lawn.grass_type]['name']
    
    # amount of seed based on size of lawn
    lawn.seed_new_lb_range = [x*(lawn.size / 1000) for x in seeding_info['seed_new_lb_range']]
    lawn.seed_over_lb_range = [x*(lawn.size / 1000) for x in seeding_info['seed_over_lb_range']]

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
    
    for season in fertilizer_info:
        for app in fertilizer_info[season]:
            app['total_lbs'] = plannerutils.round_to_quarter((lawn.size / 1000) * app['rate'])
            
            if app['end_date'] == None:
                task_name = "Fertilize with %s lbs of Nitrogen" % (str(app['total_lbs']))
                app['title'] = task_name
            else:
                task_name = "%s - Fertilize with %s lbs of Nitrogen" % (app['end_date'].strftime("%B %-d"), str(app['total_lbs']))
                app['title'] = task_name
                app['end_date'] = app['end_date'].strftime("%B %-d")
            
            my_planner.add_task(task_name, app['date'])
            app['date'] = app['date'].strftime("%B %-d")
    
    """
    This section prepares the Weed Control information
    """
    
    weed_info = weedcontrol.get_weed_control_info(closest_station, temp_data)
    summer_weed_deadline = weed_info['summer_deadline'].strftime("%B %d")
    my_task_name = "Summer annual weed pre-emergent herbicide application deadline."
    my_planner.add_task(my_task_name, weed_info['summer_deadline'])
    
    """
    This section prepares the Insect Control information
    """
    
    insect_info = insectcontrol.get_insect_control_info(closest_station, temp_data)
    grub_deadline = insect_info['grub_deadline'].strftime("%B %d")
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
        'fertilizer_apps':fertilizer_info,
        
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