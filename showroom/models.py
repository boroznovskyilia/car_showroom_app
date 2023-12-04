import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from buyer.models import Buyer
from car_showroom.base_model import BaseModel, InitialModel


class ShowRoom(BaseModel):
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    min_year_of_release = models.IntegerField(
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)],
    )
    max_year_of_release = models.IntegerField(
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)],
    )
    buyers = models.ManyToManyField(Buyer, related_name="buyers")


class ShowRoomCars(InitialModel):
    model = models.CharField()
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    show_room = models.ForeignKey(ShowRoom, on_delete=models.CASCADE, related_name="show_room_cars")
    year_ofrelease = models.IntegerField(
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)],
    )
