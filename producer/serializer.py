from rest_framework import serializers
from .models import Producer,ProducerStock,TransactionProducerToShowRoom
import datetime
from showroom.models import CarShowRoom

class HelpCarShowRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarShowRoom
        fields = ["id","name","location","is_active"]

class ProducerStockSerializerCreate(serializers.ModelSerializer):
    
    class Meta:
        model = ProducerStock
        fields = ["car_model","car_price","year_of_car_release","producer"]

class ProducerSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ["name","location"]

class ProducerSerializerList(serializers.ModelSerializer):
    producer_stock = ProducerStockSerializerCreate(many = True,read_only = True)
    buyers_from_producer = HelpCarShowRoomSerializer(many = True,read_only = True)
    class Meta:
        model = Producer
        fields = ["id","name","location","buyers_from_producer","producer_stock"]

class ProducerSerializeUpdate(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['date_of_latest_update'] = datetime.datetime.now()
        return data
    
    class Meta:
        model = Producer
        fields = ["name","date_of_latest_update","location"]
        read_only_fields = ["date_of_latest_update"]

class ProducerStockSerializerUpdate(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['date_of_latest_update'] = datetime.datetime.now()
        return data
    class Meta:
        model = ProducerStock
        fields = ["car_model","year_of_car_release","car_price","date_of_latest_update"]
        read_only_fields = ["date_of_latest_update"]

class TransactionBetweenProducerAndShowroom(serializers.ModelSerializer):
    class Meta:
        model = TransactionProducerToShowRoom
        fields = "__all__"
        read_only_fields = ["date_of_transaction"]

class TransactionBetweenProducerAndShowroomList(serializers.ModelSerializer):
    class Meta:
        model = TransactionProducerToShowRoom
        fields = "__all__"