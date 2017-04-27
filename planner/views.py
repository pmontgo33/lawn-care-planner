"""
planner/views.py

This file contains the views for the planner app.
"""

# import statements
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import UpdateView
from django.http import JsonResponse
from planner.models import Lawn, LawnProduct
from planner.forms import LawnForm
from planner.lawn import lawnplanner
from planner import plannerutils


class LawnDetailView(View):

    def get(self, request, pk, *args, **kwargs):
        lawn = get_object_or_404(Lawn, pk=pk)

        # Get the closest station and min/max temperature data for that station based on the ZIP code
        closest_station = plannerutils.get_closest_station_data(lawn.zip_code)

        my_planner = lawnplanner.Planner(lawn, closest_station)

        # Separate the Products by type
        fert_products = LawnProduct.objects.filter(type='Fertilizer')
        # Add the application weight to the fertilizer products

        if len(my_planner.fertilizer_info['apps']['spring']) == 0:
            first_app_total = my_planner.fertilizer_info['apps']['summer'][0]['total_lbs']
        else:
            first_app_total = my_planner.fertilizer_info['apps']['spring'][0]['total_lbs']

        for product in fert_products:
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
            'seed_products': seed_products,
            "weed_products": weed_products,
            'insect_products': insect_products,

        }
        return render(request, 'planner/lawn_detail.html', template_vars)

    def post(self, request, pk, *args, **kwargs):
        print("post")
        lawn = get_object_or_404(Lawn, pk=pk)
        # Create an empty dictionary
        response = {}

        # Save the data sent from the AJAX request
        input_n = float(request.POST.get('input_n'))
        input_p = float(request.POST.get('input_p'))
        input_k = float(request.POST.get('input_k'))
        print(input_n, input_p, input_k)
        # Do maths
        total_nitrogen = (lawn.size / 1000) * .75
        product_weight = plannerutils.round_to_quarter(total_nitrogen / (input_n / 100))

        # Save the result into the response dictionary
        response['product_weight'] = product_weight

        # Send the response as a JSON response(check the docs on how to import this)
        return JsonResponse(response)


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'account/profile_update_form.html'
    fields = ('first_name', 'last_name')

    def get(self, request, *args, **kwargs):
        self.object = User.objects.get(username=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect('index')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'account/user_detail.html'
    def get_object(self):
        return self.request.user


class UserLawnListView(LoginRequiredMixin, ListView):
    model = Lawn
    template_name = 'planner/user_lawn_list.html'

    def get_queryset(self):
        return Lawn.objects.filter(user=self.request.user)


def index(request):
    return render(request, "planner/index.html", {})


def lawn_new(request):

    if request.method == "POST":
        form = LawnForm(request.user, request.POST)
        if form.is_valid():
            lawn = form.save(commit=False)
            print(lawn.name)
            if request.user.is_anonymous():
                lawn.user = User.objects.get(username="guest")
                lawn.name = "Lawn " + str(lawn.zip_code)
            else:
                lawn.user = request.user
            lawn.save()

            return redirect('lawn_detail', pk=lawn.pk)
    else:
        form = LawnForm(request.user)
    return render(request, 'planner/lawn_edit.html', {"form": form})
