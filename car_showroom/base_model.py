from django.db import models
import datetime
from django_countries.fields import CountryField

class BaseModel(models.Model):
    name = models.CharField()   
    is_active = models.BooleanField(default=True)
    date_of_creat = models.DateTimeField(default = datetime.datetime.now())
    date_of_latest_update = models.DateTimeField(default = datetime.datetime.now())
    balance = models.IntegerField(default=0)
    location = CountryField(blank=True)
    class Meta:
        abstract = True