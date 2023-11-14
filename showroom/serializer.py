from rest_framework import serializers
from .models import CarShowRoom
import datetime

class CarShowRoomSerializerList(serializers.ModelSerializer):
    class Meta:
        model = CarShowRoom
        fields = "__all__"

class CarShowRoomSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = CarShowRoom
        fields = ["name","location","min_price_of_car","max_price_of_car","min_year_of_car_realise","max_year_of_car_realise"]

class CarShowRoomSerializerUpdate(serializers.ModelSerializer):

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['date_of_latest_update'] = datetime.datetime.now()
        return data
    
    class Meta:
        model = CarShowRoom
        fields = ["name","location","min_price_of_car","max_price_of_car","min_year_of_car_realise","max_year_of_car_realise","date_of_latest_update"]