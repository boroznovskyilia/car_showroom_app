import datetime

from django.db import models
from django_countries.fields import CountryField


class ActiveObjectManager(models.Manager):
    """
    Manager to get active objects from daatabase
    """

    def get_active(self):
        return self.filter(is_active=True)


class InitialModel(models.Model):
    """
    Base Model that used for FabricCars and ShowRoomCars
    """

    is_active = models.BooleanField(default=True)
    date_of_creat = models.DateTimeField(default=datetime.datetime.now())
    date_of_latest_update = models.DateTimeField(default=datetime.datetime.now())
    # objects = ActiveObjectManager()

    class Meta:
        abstract = True
    
class BaseModel(InitialModel):
    """
    Base Model that used for Fabric,ShowRoom,Buyer
    """

    name = models.CharField(unique=True)
    balance = models.IntegerField(default=0)
    location = CountryField(blank=True)

    class Meta:
        abstract = True
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.id},{self.name})"


