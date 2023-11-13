from rest_framework import serializers
from .models import CarShowRoom

class CarShowRoomSerializerList(serializers.ModelSerializer):
    class Meta:
        model = CarShowRoom
        fields = "__all__"

class CarShowRoomSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = CarShowRoom
        fields = ["name","location","min_price_of_car","max_price_of_car","min_year_of_car_realise","max_year_of_car_realise"]