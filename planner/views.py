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

    # Get the closest station and min/max temperature data for that station based on the ZIP code
    closest_station = plannerutils.get_closest_station_data(lawn.zip_code)

    my_planner = lawnplanner.Planner(lawn, closest_station)

    # Separate the Products by type
    fert_products = LawnProduct.objects.filter(type='Fertilizer')
    # Add the application weight to the fertilizer products
    for product in fert_products:
        first_app_total = my_planner.fertilizer_info['apps']['spring'][0]['total_lbs']
        product_nitrogen = product.specs['npk'][0] / 100

        product.weight = plannerutils.round_to_quarter(first_app_total / product_nitrogen)
        product.specs['npk'] = "(%s-%s-%s)" % \
                               (product.specs['npk'][0], product.specs['npk'][1], product.specs['npk'][2])

    seed_products = LawnProduct.objects.filter(type='Grass Seed')
    weed_products = LawnProduct.objects.filter(type='Weed Control')
    insect_products = LawnProduct.objects.filter(type='Insect Control')

    template_vars = {
        'lawn': lawn,
        'closest_station': closest_station,
        'planner': my_planner,
        'fertilizer_products': fert_products,
        'seed_products':seed_products,
        "weed_products":weed_products,
        'insect_products':insect_products,

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