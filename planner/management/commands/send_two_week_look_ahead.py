"""
This is a management command to be called by Heroku Scheduler. When it is executed, it will check if it is
Wednesday. If it is Wednesday, it will send out the Two Week Look Ahead email notifications.
"""

# Import Statements
from django.core.management.base import BaseCommand, CommandError
from datetime import date
from planner import email_notification


class Command(BaseCommand):
    help = 'Sends out two week look aheads to users that have upcoming tasks. Only sends on Wednesday'

    def handle(self, *args, **options):
        # if today is Wednesday, send out two week look ahead
        if date.today().weekday() == 2:
            email_notification.send_two_week_look_ahead()