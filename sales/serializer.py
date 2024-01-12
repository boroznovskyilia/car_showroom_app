from rest_framework import serializers
from .models import Sale

class SaleForShowRooomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ["showroom_car","percent","date_of_start","date_of_end"]

class SaleForFabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ["fabric_car","percent","date_of_start","date_of_end"]