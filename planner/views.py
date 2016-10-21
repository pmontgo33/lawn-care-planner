# planner/views.py
# Patrick W. Montgomery
# created: 10-8-2016

# import statements
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
#from django.http import HttpResponse
from .models import Lawn
from .forms import LawnForm
from .code import seeding, mowing, planner, utils

from .code import seeding

def index(request):
    return render(request, "planner/index.html", {})
    
def lawn_detail(request, pk):
    lawn = get_object_or_404(Lawn, pk=pk)
    my_planner = planner.planner()
      
    """
    This section prepares the Seeding information
    """
    closest_station, temp_data = utils.get_closest_station_data(lawn.zip_code)
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
    print(str(my_planner))
    
    """
    This section prepares the Fertilizer information
    """
    
    
    

    
    temp_vars = {
        'lawn':lawn,
        'closest_station':seeding_info['closest_station']['name'],
        'germination_time':seeding_info['germination_time'],
        'seed_new_lb_range':seeding_info['seed_new_lb_range'],
        'seed_over_lb_range':seeding_info['seed_over_lb_range'],
        'seeding_ranges':str_ranges,
        'mowing_heights':mowing_heights,
        'planner':my_planner.tasks_by_season,
    }
    
    return render(request, 'planner/lawn_detail.html', temp_vars)
    
def lawn_new(request):

    if request.method == "POST":
        form = LawnForm(request.POST)
        if form.is_valid():
            lawn = form.save(commit=False)
            lawn.user = User.objects.get(username="guest")            #either make this User guest, or look into cookie based sessions.`
            lawn.save()
            lawn.name = "Lawn" + str(lawn.pk)
            lawn.save() 
            
            return redirect('lawn_detail', pk=lawn.pk)
    else:
        form = LawnForm()
    return render(request, 'planner/lawn_edit.html', {"form":form})