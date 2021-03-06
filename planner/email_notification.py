"""
This file contains all of the code necessary to compile and send email notifications for the planner
"""

# Import Statements
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage

from planner.lawn import lawnplanner
from planner import plannerutils
from planner.models import Lawn


def get_planner_data(lawn):
    """
    Function takes a lawn, finds its closest weather station, and generates a lawn planner.
    :param lawn: 
    :return: lawnplanner
    """
    closest_station = plannerutils.get_closest_station_data(lawn.zip_code)
    my_planner = lawnplanner.Planner(lawn, closest_station)
    return my_planner


def get_two_week_data():
    today = date.today()
    two_weeks_from_today = today + timedelta(days=14)

    # filter lawns that want notifications and are real users (not guest or examples)
    lawns = Lawn.objects.filter(weekly_notify=True).exclude(user__username__in=['guest', 'examples'])
    upcoming_lawns = []
    for lawn in lawns:
        my_planner = get_planner_data(lawn)
        my_upcoming = []
        for task in my_planner.all_tasks():
            if today <= task['date'].replace(year=today.year) <= two_weeks_from_today:
                my_upcoming.append(task)

        # if there are any upcoming tasks, add this lawn to the upcoming lawns list.
        if len(my_upcoming) > 0:
            lawn.upcoming = my_upcoming
            upcoming_lawns.append(lawn)

    return upcoming_lawns


def send_two_week_look_ahead():
    template = get_template('planner/email/two_week_look_ahead_email.txt')

    data = get_two_week_data()
    for lawn in data:
        send_to = lawn.user.email
        subject = "%s - Two Week Look Ahead" % (lawn.name)

        planner_url = "http://lawncareplanner.com/planner/lawn/%s/" % (str(lawn.pk))
        context = Context({'lawn': lawn, 'planner_url': planner_url})
        content = template.render(context)

        email = EmailMessage(subject, content, 'Lawn Care Planner <noreply@lawncareplanner.com>', [send_to])
        email.send()
