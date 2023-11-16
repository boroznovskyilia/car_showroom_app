from rest_framework import serializers
from .models import CarShowRoom,CarShowRoomStock
import datetime


class CarShowRoomStockSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = CarShowRoomStock
        fields = "__all__"

class CarShowRoomStockSerializserUpdate(serializers.ModelSerializer):

    class Meta:
        model = CarShowRoomStock
        fields = ["car_model","car_price","amount_of_cars_of_this_model"]
        read_only_fields = ["car_model"]
        

class CarShowRoomSerializerList(serializers.ModelSerializer):
    show_room_stocks = CarShowRoomStockSerializerCreate(many = True,read_only = True)

    class Meta:
        model = CarShowRoom
        fields = ["id","name","location","min_price_of_car","max_price_of_car",\
                  "min_year_of_car_release","max_year_of_car_release","date_of_creat",\
                    "date_of_latest_update","show_room_stocks"]
        

class CarShowRoomSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = CarShowRoom
        fields = ["name","location","min_price_of_car","max_price_of_car",\
                  "min_year_of_car_release","max_year_of_car_release"]

class CarShowRoomSerializerUpdate(serializers.ModelSerializer):

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['date_of_latest_update'] = datetime.datetime.now()
        return data
    
    class Meta:
        model = CarShowRoom
        fields = ["name","location","min_price_of_car","max_price_of_car",\
                  "min_year_of_car_release","max_year_of_car_release",\
                    "date_of_latest_update"]
        
