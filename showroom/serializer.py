import datetime

from django_countries.fields import Country
from rest_framework import serializers

from buyer.models import Buyer
from fabric.models import Transaction

from .models import ShowRoom, ShowRoomCars


class AdditionalBuyerSerializer(serializers.ModelSerializer):
    """
    Show necessary Buyer's fields in ShowrooSerializer
    """

    class Meta:
        model = Buyer
        fields = ["id", "name", "is_active"]


class ShowRoomCarsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowRoomCars
        fields = ["id", "model", "price", "amount", "year_ofrelease", "show_room"]
        read_only_fields = ["id", "date_of_create", "date_of_latest_update", "is_active"]


class ShowRoomCarsUpdateSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["date_of_latest_update"] = datetime.datetime.now()
        return data

    class Meta:
        model = ShowRoomCars
        fields = ["model", "price", "amount", "date_of_latest_update"]
        read_only_fields = ["model", "date_of_latest_update"]


class ShowRoomListSerializer(serializers.ModelSerializer):
    show_room_cars = ShowRoomCarsCreateSerializer(many=True, read_only=True)
    buyers = AdditionalBuyerSerializer(many=True, read_only=True)

    class Meta:
        model = ShowRoom
        fields = [
            "id",
            "name",
            "is_active",
            "balance",
            "location",
            "min_price",
            "max_price",
            "min_year_of_release",
            "max_year_of_release",
            "date_of_creat",
            "date_of_latest_update",
            "buyers",
            "show_room_cars",
        ]


class ShowRoomCreateSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        if data["location"] == "":
            data["location"] = None
        return super().to_internal_value(data)

    class Meta:
        model = ShowRoom
        fields = [
            "name",
            "location",
            "min_price",
            "max_price",
            "min_year_of_release",
            "max_year_of_release",
        ]


class ShowRoomUpdateSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["date_of_latest_update"] = datetime.datetime.now()
        return data

    class Meta:
        model = ShowRoom
        fields = [
            "name",
            "location",
            "min_price",
            "max_price",
            "min_year_of_release",
            "max_year_of_release",
            "date_of_latest_update",
        ]
        read_only_fields = ["date_of_latest_update"]


class TransactionBetweenFabricAndShowroom(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["fabric", "showroom", "model", "date", "price"]
        read_only_fields = ["date"]
