import datetime

from django.db import models

from showroom.models import ShowRoom
from showroom.model_cars import ShowRoomCars
from fabric.models import Fabric
from fabric.model_cars import FabricCars
from django.core.validators import MaxValueValidator, MinValueValidator



class Sale(models.Model):
    percent = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(100)],
                                               default = 5)
    fabric_car = models.ForeignKey(
        FabricCars, on_delete=models.PROTECT, null=True, related_name="sale"
    )
    showroom_car = models.ForeignKey(
        ShowRoomCars, on_delete=models.PROTECT, null=True, related_name="sale"
    )
    date_of_start = models.DateTimeField(default=datetime.datetime.now())
    date_of_end = models.DateTimeField(default=datetime.datetime.now())
