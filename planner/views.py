"""
planner/views.py

This file contains the views for the planner app.
"""

# import statements
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from planner.models import Lawn, LawnProduct
from planner.forms import LawnForm
from planner.lawn import lawnplanner
from planner import plannerutils

import logging
logger = logging.getLogger(__name__)


def user_can_view_lawn(lawn, user):
    """
    Tests and allows view of the specific lawn if user is superuser, user owns the lawn,
    lawn is guest, or lawn is an example.
    :return: True if access is allowed, False otherwise
    """

    if user.is_superuser:
        return True
    elif lawn.user == User.objects.get(username="guest"):
        return True
    elif lawn.user == User.objects.get(username="examples"):
        return True
    elif lawn.user == user:
        return True
    else:
        return False


def user_can_edit_lawn(lawn, user):
    """
    Tests and allows edit & delete access to the specific lawn if user is superuser, if user owns the lawn, or if
    guest owns the lawn.
    :return: True if access is allowed, False otherwise
    """

    if user.is_superuser:
        return True
    elif lawn.user == user:
        return True
    elif lawn.user == User.objects.get(username="guest"):
        return True
    else:
        return False


def index(request):
    logger.debug("Index View (homepage)")
    return render(request, "planner/index.html", {})


class LawnDetailView(UserPassesTestMixin, View):

    def __init__(self):
        self.raise_exception = True

    def get_permission_denied_message(self):
        logger.info("LawnDetailView - Access Denied")
        return "You do not have access to this Lawn! Please go back, and create your own."

    def test_func(self):
        lawn = get_object_or_404(Lawn, pk=self.kwargs.get('pk'))
        return user_can_view_lawn(lawn, self.request.user)

    def get(self, request, pk, *args, **kwargs):
        logger.debug("LawnDetailView GET")

        lawn = get_object_or_404(Lawn, pk=pk)

        # Get the closest station and min/max temperature data for that station based on the ZIP code
        closest_station = plannerutils.get_closest_station_data(lawn.zip_code)
        logger.info("Closest Staion: %s" % (closest_station))

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
        logger.debug("LawnDetailView POST (NPK Calculator submitted)")

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
        logger.debug("ProfileUpdateView GET")
        self.object = User.objects.get(username=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        logger.info("Profile Updated - User: %s" % (self.object.user))
        return redirect('user_detail')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'account/user_detail.html'

    def get_object(self):
        logger.debug("UserDetailView")
        return self.request.user


class UserLawnListView(LoginRequiredMixin, ListView):
    model = Lawn
    template_name = 'planner/user_lawn_list.html'

    def get_queryset(self):
        logger.debug("UserLawnListView")
        return Lawn.objects.filter(user=self.request.user)


class LawnDeleteView(UserPassesTestMixin, DeleteView):
    model = Lawn
    success_url = reverse_lazy('user_lawn_list')
    template_name = 'planner/lawn_confirm_delete.html'

    def __init__(self):
        logger.debug("LawnDeleteView")
        self.raise_exception = True

    def get_permission_denied_message(self):
        logger.info("LawnDeleteView - Access Denied")
        return "You do not have access to this Lawn! Please go back, and create your own."

    def test_func(self):
        lawn = get_object_or_404(Lawn, pk=self.kwargs.get('pk'))
        return user_can_edit_lawn(lawn, self.request.user)


class LawnNewView(FormView):
    form_class = LawnForm
    template_name = 'planner/lawn_edit.html'

    def form_valid(self, form):
        lawn = form.save(commit=False)

        if self.request.user.is_anonymous():
            lawn.user = User.objects.get(username="guest")
            lawn.name = "Lawn " + str(lawn.zip_code)
        else:
            lawn.user = self.request.user
        lawn.save()
        logger.info("New Lawn Created - Name: %s, User: %s" % (lawn.name, lawn.user.email))

        self.kwargs['lawn_pk'] = lawn.pk
        return super(LawnNewView, self).form_valid(form)

    def get_form_kwargs(self):
        logger.debug("LawnNewView")
        kwargs = super(LawnNewView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('lawn_detail', kwargs={'pk':self.kwargs.get('lawn_pk')})


class LawnEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lawn
    form_class = LawnForm
    template_name = 'planner/lawn_edit.html'

    # TODO add function to redirect to previous page if cancel button is clicked.

    def __init__(self):
        logger.debug("LawnEditView")
        self.raise_exception = True

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            # ref = request.GET['ref']
            # logger.debug("Cancel URL is ?%s?" % (ref))
            return HttpResponseRedirect(reverse('lawn_detail', kwargs={'pk':self.get_object().pk}))
        else:
            return super(LawnEditView, self).post(request, *args, **kwargs)

    def get_permission_denied_message(self):
        logger.info("LawnEditView - Access Denied")
        return "You do not have access to this Lawn! Please go back, and create your own."

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            lawn = form.save(commit=False)
            if lawn.user == User.objects.get(username="guest"):
                lawn.user = self.request.user
                lawn.save()
        return super(LawnEditView, self).form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(Lawn, pk=self.kwargs.get('pk'))

    def get_form_kwargs(self):
        kwargs = super(LawnEditView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        lawn = self.get_object()
        logger.info("Lawn Edited - Name: %s, User: %s" % (lawn.name, lawn.user.email))
        return reverse('lawn_detail', kwargs={'pk':self.kwargs.get('pk')})

    def test_func(self):
        lawn = get_object_or_404(Lawn, pk=self.kwargs.get('pk'))
        return user_can_edit_lawn(lawn, self.request.user)
