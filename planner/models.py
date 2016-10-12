# planner/models.py
# Patrick W. Montgomery
# created: 10/9/2016

from django.db import models
from .code import seeding

class Lawn(models.Model):
    """
    The Lawn model contains all of the properties for a specific lawn.
    """
    user = models.ForeignKey('auth.user')
    name = models.CharField(max_length=140)
    zip_code = models.CharField(max_length=5)
    grass_type = models.CharField(max_length=140, choices=seeding.GRASS_TYPES)
    
    def __str__(self):
        return self.name
