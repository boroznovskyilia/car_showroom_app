from django.db import models
import datetime
from showroom.models import CarShowRoom,BaseModel


class Buyer(BaseModel):
    pass

class TransactionFromShowroomToBuyer(models.Model):
    showroom = models.ForeignKey(CarShowRoom,on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    date_of_transaction = models.DateField(default = datetime.datetime.now().strftime('%d/%m/%Y'))
    car_model = models.CharField()
    price_of_transactions = models.PositiveIntegerField()
    class Meta:
        ordering = ['-date_of_transaction']

