import datetime

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from fabric.model_transaction import Transaction
from django.contrib.auth import get_user_model
from .models import Buyer
from django.db.models import Q

class BuyerRegisterSerializer(ModelSerializer):
    def to_internal_value(self,data):
        name = data.get('name')
        email = data.get('email')
        if not name and not email:
            raise serializers.ValidationError("Please provide either 'name' or 'email'.")
        buyer =  get_user_model().objects.filter(
            Q(name=name) & Q(email=email) & Q(is_active=True)
        ).first()
        if buyer is None:
            return data
        else:
            raise serializers.ValidationError("Account with this name or email is already exist")

    class Meta:
        model = Buyer
        fields = ("name", "email", "password","location")
        extra_kwargs = {"password": {"write_only": True}}


class BuyerLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        if not name and not email:
            raise serializers.ValidationError("Please provide either 'name' or 'email'.")
        buyer =  get_user_model().objects.filter(
            Q(name=name) & Q(email=email)
        ).first()

        if buyer and buyer.password==password and buyer.is_active:
            return buyer

        raise serializers.ValidationError("Incorrect Credentials")

class BuyerListSerializer(ModelSerializer):
    class Meta:
        model = Buyer
        fields = ["id","name","email", "balance", "is_active", "date_of_creat", "date_of_latest_update"]
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
