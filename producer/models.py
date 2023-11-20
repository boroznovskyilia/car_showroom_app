from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
import datetime
from showroom.models import CarShowRoom
from car_showroom.base_model import BaseModel

class Producer(BaseModel):
    buyers_from_producer = models.ManyToManyField(CarShowRoom)

class ProducerStock(models.Model):
    is_active = models.BooleanField(default=True)
    date_of_creat = models.DateTimeField(default = datetime.datetime.now())
    date_of_latest_update = models.DateTimeField(default = datetime.datetime.now())
    car_model = models.CharField()
    car_price = models.IntegerField()
    producer = models.ForeignKey(Producer,on_delete=models.CASCADE,related_name="producer_stock")
    year_of_car_release = models.IntegerField(default=datetime.datetime.now().year,
                                        validators=[MinValueValidator(1900),\
                                            MaxValueValidator(datetime.datetime.now().year)])

class Car(models.Model):
    model = models.CharField()
    year_of_release = models.DateTimeField()
    
class TransactionProducerToShowRoom(models.Model):
    producer = models.ForeignKey(Producer,on_delete=models.CASCADE)
    showroom = models.ForeignKey(CarShowRoom,on_delete=models.CASCADE,default = None)
    date_of_transaction = models.DateTimeField(default = datetime.datetime.now())
    car_model = models.CharField()
    price_of_transactions = models.PositiveIntegerField()

    class Meta:
        ordering = ['-date_of_transaction']

