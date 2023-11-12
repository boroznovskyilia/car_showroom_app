from rest_framework import serializers
from .models import CarShowRoom

class CarShowRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarShowRoom
        fields = "__all__"