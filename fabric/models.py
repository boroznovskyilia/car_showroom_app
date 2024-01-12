from django.db import models

from car_showroom.base_model import BaseModel
from showroom.models import ShowRoom


class Fabric(BaseModel):
    showrooms = models.ManyToManyField(ShowRoom, related_name="fabrics")
