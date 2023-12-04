import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from buyer.models import Buyer
from car_showroom.base_model import BaseModel, InitialModel
from showroom.models import ShowRoom


class Fabric(BaseModel):
    showrooms = models.ManyToManyField(ShowRoom, related_name="showrooms")


class FabricCars(InitialModel):
    model = models.CharField()
    price = models.IntegerField()
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name="fabric_cars")
    year_of_release = models.IntegerField(
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)],
    )


class Transaction(models.Model):
    """
    Transaction Model that used for transaction: Fabric->Showroom and Showroom->Buyer
    if fabric == None(null) -> this is Showroom->Buyer transaction
    if buyer == None(null) -> this is Fabric->Showroom transaction
    """

    showroom = models.ForeignKey(ShowRoom, on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=datetime.datetime.now())
    model = models.CharField()
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ["-date"]
