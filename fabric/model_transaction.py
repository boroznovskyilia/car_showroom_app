import datetime

from django.db import models

from buyer.models import Buyer

from showroom.models import ShowRoom
from showroom.model_cars import ShowRoomCars
from .models import Fabric
from .model_cars import FabricCars


class Transaction(models.Model):
    """
    Transaction Model that used for transaction: Fabric->Showroom and Showroom->Buyer
    if fabric == None(null) -> this is Showroom->Buyer transaction
    if buyer == None(null) -> this is Fabric->Showroom transaction
    """
    
    showroom = models.ForeignKey(ShowRoom, on_delete=models.PROTECT, null=True, related_name="transactions")
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, null=True, related_name="transactions")
    fabric = models.ForeignKey(Fabric, on_delete=models.PROTECT, null=True, related_name="transactions")
    date = models.DateTimeField(default=datetime.datetime.now())
    fabric_car = models.ForeignKey(
        FabricCars, on_delete=models.PROTECT, null=True, related_name="transactions"
    )
    showroom_car = models.ForeignKey(
        ShowRoomCars, on_delete=models.PROTECT, null=True, related_name="transactions"
    )

    class Meta:
        ordering = ["-date"]
