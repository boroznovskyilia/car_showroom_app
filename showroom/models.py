from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
import datetime
from car_showroom.base_model import BaseModel

# Create your models here.

class CarShowRoom(BaseModel):
    min_price_of_car = models.IntegerField()
    max_price_of_car = models.IntegerField()  
    min_year_of_car_release = models.IntegerField(default=datetime.datetime.now().year,
                                validators=[MinValueValidator(1900),\
                                            MaxValueValidator(datetime.datetime.now().year)])
    max_year_of_car_release = models.IntegerField(default=datetime.datetime.now().year,\
                                validators=[MinValueValidator(1900),\
                                            MaxValueValidator(datetime.datetime.now().year)])
    buyers_from_showroom = models.ManyToManyField('buyer.Buyer')
    
class CarShowRoomStock(models.Model):
    is_active = models.BooleanField(default=True)
    date_of_creat = models.DateTimeField(default = datetime.datetime.now())
    date_of_latest_update = models.DateTimeField(default = datetime.datetime.now())
    car_model = models.CharField()
    car_price = models.PositiveIntegerField()
    amount_of_cars_of_this_model = models.PositiveIntegerField()
    show_room = models.ForeignKey(CarShowRoom,on_delete=models.CASCADE,\
                                related_name="show_room_stocks")
    year_of_car_release = models.IntegerField(default=datetime.datetime.now().year,
                                validators=[MinValueValidator(1900),\
                                            MaxValueValidator(datetime.datetime.now().year)])

class TransactionFromShowroomToBuyer(models.Model):
    showroom = models.ForeignKey(CarShowRoom,on_delete=models.CASCADE)
    buyer = models.ForeignKey('buyer.Buyer',on_delete=models.CASCADE)
    date_of_transaction = models.DateTimeField(default = datetime.datetime.now())
    car_model = models.CharField()
    price_of_transactions = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['-date_of_transaction']