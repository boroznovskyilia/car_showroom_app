import datetime

from django_countries.fields import Country
from django.core.validators import MinValueValidator
from rest_framework import serializers

from buyer.models import Buyer
from fabric.model_cars import FabricCars
from fabric.model_transaction import Transaction
from fabric.models import Fabric

from .models import ShowRoom
from .model_cars import ShowRoomCars
from sales.serializer import SaleForFabricSerializer


class AdditionalBuyerSerializer(serializers.ModelSerializer):
    """
    Show necessary Buyer's fields in ShowrooSerializer
    """

    num_of_transaction = serializers.SerializerMethodField()

    class Meta:
        model = Buyer
        fields = ["id", "name", "is_active", "num_of_transaction"]

    def get_num_of_transaction(self, obj):
        return obj.num_of_transaction


# class ShowRoomCarsCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ShowRoomCars
#         fields = ["id", "model", "price", "amount", "year_ofrelease", "show_room"]
#         read_only_fields = ["id", "date_of_create", "date_of_latest_update", "is_active"]


# class ShowRoomCarsUpdateSerializer(serializers.ModelSerializer):
#     def to_internal_value(self, data):
#         data = super().to_internal_value(data)
#         data["date_of_latest_update"] = datetime.datetime.now()
#         return data

#     class Meta:
#         model = ShowRoomCars
#         fields = ["model", "price", "amount", "date_of_latest_update"]
#         read_only_fields = ["model", "date_of_latest_update"]


class FabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabric()
        fields = ["id", "name"]


class FabricCarsSerializer(serializers.ModelSerializer):
    fabric = FabricSerializer()
    sale = SaleForFabricSerializer(many=True,read_only=True)
    class Meta:
        model = FabricCars
        fields = ["id", "model", "fabric", "price", "year_of_release","sale"]


class ShowRoomCarWithPopularitySerializer(serializers.ModelSerializer):
    popularity = serializers.SerializerMethodField()
    fabric_car = FabricCarsSerializer()

    class Meta:
        model = ShowRoomCars
        fields = ["id", "fabric_car", "amount", "popularity"]

    def get_popularity(self, obj):
        return obj.popularity


class ShowRoomCarSerializer(serializers.ModelSerializer):
    fabric_car = FabricCarsSerializer()

    class Meta:
        model = ShowRoomCars
        fields = ["id", "fabric_car", "amount"]


class ShowRoomListSerializer(serializers.ModelSerializer):
    # show_room_cars = ShowRoomCarSerializer(many=True, read_only=True)
    show_room_cars = ShowRoomCarWithPopularitySerializer(many=True,read_only=True)
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
    def get_num_of_transaction(self, obj):
        return obj.num_of_transaction

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

    balance = serializers.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        model = ShowRoom
        fields = [
            "name",
            "location",
            "balance",
            # "min_price",
            # "max_price",
            # "min_year_of_release",
            # "max_year_of_release",
            "date_of_latest_update",
        ]
        read_only_fields = ["date_of_latest_update"]


class TransactionBetweenFabricAndShowroom(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["fabric", "showroom", "date", "fabric_car"]
        read_only_fields = ["date"]


class FabricsSerializer(serializers.ModelSerializer):
    fabric_cars = FabricCarsSerializer(many=True)

    class Meta:
        model = Fabric
        fields = ["id", "name", "fabric_cars"]


class SutableCarsSerializer(serializers.ModelSerializer):
    show_room_cars = ShowRoomCarSerializer(many=True)

    # sutable_cars = serializers.SerializerMethodField
    class Meta:
        model = ShowRoom
        fields = ["id", "name", "min_price", "max_price", "show_room_cars"]


class MakeTransactionsSerializer(serializers.ModelSerializer):
    show_room_cars = ShowRoomCarWithPopularitySerializer(many=True)

    class Meta:
        model = ShowRoom
        fields = ["id", "name", "balance", "min_price", "max_price", "show_room_cars"]
