from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
import datetime
from showroom.models import CarShowRoom,BaseModel

class Producer(BaseModel):
    buyers_from_producer = models.ManyToManyField(CarShowRoom)

class ProducerStock(models.Model):
    car_model = models.CharField()
    car_price = models.IntegerField()
    producer = models.OneToOneField(Producer,on_delete=models.CASCADE)
    year_of_car_release = models.IntegerField(default=datetime.datetime.now().year,
                                        validators=[MinValueValidator(1900),\
                                            MaxValueValidator(datetime.datetime.now().year)])

class Car(models.Model):
    model = models.CharField()
    year_of_release = models.DateTimeField()
    
class TransactionProducerToShowRoom(models.Model):
    producer = models.ForeignKey(Producer,on_delete=models.CASCADE)
    showroom = models.ForeignKey(CarShowRoom,on_delete=models.CASCADE)
    date_of_transaction = models.DateTimeField(default = datetime.datetime.now().\
                                               strftime('%d/%m/%Y'))
    car_model = models.CharField()
    price_of_transactions = models.PositiveIntegerField()

    class Meta:
        ordering = ['-date_of_transaction']

