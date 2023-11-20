from rest_framework.serializers import ModelSerializer
from .models import Buyer
import datetime
from showroom.models import TransactionFromShowroomToBuyer

class BuyerSerializerListCreate(ModelSerializer):
    class Meta:
        model = Buyer
        fields = "__all__"

class BuyerSerializerUpdate(ModelSerializer):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['date_of_latest_update'] = datetime.datetime.now()
        return data
    class Meta:
        model = Buyer
        fields = ["name","location","date_of_latest_update"]
        read_only_fields = ["date_of_latest_update"]

class TransactionFromShowroomAndBuyerSerializer(ModelSerializer):
    class Meta:
        model = TransactionFromShowroomToBuyer
        fields = "__all__"
        read_only_fields = ["date_of_transaction"]