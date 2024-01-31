import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .models import Fabric
from car_showroom.base_model import InitialModel


class FabricCars(InitialModel):
    model = models.CharField()
    price = models.IntegerField()
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name="fabric_cars")
    year_of_release = models.IntegerField(
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)],
    )
    
    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.id},{self.model},{self.price})"


