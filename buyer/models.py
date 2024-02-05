from car_showroom.base_model import BaseModel
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from .manager import BuyerManager

class Buyer(AbstractBaseUser,BaseModel):
    email = models.EmailField(blank=True)
    password = models.CharField(MinLengthValidator(4),max_length=128)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email']
    objects = BuyerManager()