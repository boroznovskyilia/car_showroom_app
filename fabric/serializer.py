import datetime

from rest_framework import serializers

from fabric.model_transaction import Transaction
from showroom.models import ShowRoom

from .models import Fabric
from .model_cars import FabricCars


class AdditionalShowRoomSerializer(serializers.ModelSerializer):
    """
    Show necessary ShowRoom's fields in Fabric serializer
    """

    class Meta:
        model = ShowRoom
        fields = ["id", "name", "location", "is_active"]


class FabricCarsSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = FabricCars
        fields = [
            "id",
            "model",
            "price",
            "year_of_release",
            "fabric",
            "is_active",
            "date_of_creat",
            "date_of_latest_update",
        ]
        read_only_fields = ["id", "is_active", "date_of_creat", "date_of_latest_update"]


class FabricSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Fabric
        fields = ["name", "location", "is_active", "date_of_creat", "date_of_latest_update"]
        read_only_fields = ["is_active", "date_of_creat", "date_of_latest_update"]


class FabricSerializerList(serializers.ModelSerializer):
    fabric_cars = FabricCarsSerializerCreate(many=True, read_only=True)
    showrooms = AdditionalShowRoomSerializer(many=True, read_only=True)

    class Meta:
        model = Fabric
        fields = ["id", "name", "location", "showrooms", "fabric_cars"]


class FabricSerializeUpdate(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["date_of_latest_update"] = datetime.datetime.now()
        return data

    class Meta:
        model = Fabric
        fields = ["name", "date_of_latest_update", "location"]
        read_only_fields = ["date_of_latest_update"]


class FabricCarsSerializerUpdate(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["date_of_latest_update"] = datetime.datetime.now()
        return data

    class Meta:
        model = FabricCars
        fields = ["model", "year_of_release", "price", "date_of_latest_update"]
        read_only_fields = ["date_of_latest_update"]
