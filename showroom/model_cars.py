import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from car_showroom.base_model import InitialModel
from .models import ShowRoom
from fabric.model_cars import FabricCars


class ShowRoomCars(InitialModel):
    amount = models.PositiveIntegerField()
    show_room = models.ForeignKey(ShowRoom, on_delete=models.CASCADE, related_name="show_room_cars")
    fabric_car = models.ForeignKey(
        FabricCars, null=True, related_name="showroom_cars", on_delete=models.CASCADE
    )
