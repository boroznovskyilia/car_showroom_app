from django.db import models
from django.core.validators import MaxValueValidator
import datetime
from django_countries.fields import CountryField

# Create your models here.
class BaseModel(models.Model):
    name = models.CharField()   
    is_active = models.BooleanField(default=True)
    date_of_creat = models.DateTimeField(default = datetime.datetime.now())
    date_of_latest_update = models.DateTimeField(default = datetime.datetime.now())
    balance = models.IntegerField(default=0)
    location = CountryField(blank=True)
    class Meta:
        abstract = True

class CarShowRoom(BaseModel):
    min_price_of_car = models.IntegerField()
    max_price_of_car = models.IntegerField()  
    min_year_of_car_realise = models.IntegerField(default=datetime.datetime.now().year,validators=[MaxValueValidator(datetime.datetime.now().year)])
    max_year_of_car_realise = models.IntegerField(default=datetime.datetime.now().year,validators=[MaxValueValidator(datetime.datetime.now().year)])
    
class CarShowRoomStock(models.Model):
    car_model = models.CharField()
    car_price = models.IntegerField()
    amount_of_cars_of_this_model = models.IntegerField()
    show_room = models.OneToOneField(CarShowRoom,on_delete=models.CASCADE)
    year_of_car_realise = models.IntegerField(default = datetime.datetime.now().year)