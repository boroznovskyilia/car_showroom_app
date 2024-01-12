import datetime

from rest_framework.serializers import ModelSerializer

from fabric.model_transaction import Transaction

from .models import Buyer


class BuyerListCreateSerializer(ModelSerializer):
    class Meta:
        model = Buyer
        fields = ["name", "location", "balance", "is_active", "date_of_creat", "date_of_latest_update"]
        read_only_fields = ["is_active", "date_of_creat", "date_of_latest_update", "balance"]


class BuyerUpdateSerializer(ModelSerializer):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["date_of_latest_update"] = datetime.datetime.now()
        return data

    class Meta:
        model = Buyer
        fields = ["name", "location", "date_of_latest_update"]
        read_only_fields = ["date_of_latest_update"]


class TransactionFromShowroomAndBuyerSerializer(ModelSerializer):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data["date"] = datetime.datetime.now()
        return data

    class Meta:
        model = Transaction
        fields = ["buyer", "showroom", "date", "showroom_car"]
        read_only_fields = ["date"]
