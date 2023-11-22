from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ViewSet,GenericViewSet
from .serializer import BuyerSerializerListCreate,BuyerSerializerUpdate,\
    TransactionFromShowroomAndBuyerSerializer
from .models import Buyer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from showroom.models import CarShowRoom,TransactionFromShowroomToBuyer

class BuyerAPIViewListCreate(ListCreateAPIView,ViewSet):
    queryset = Buyer.objects.filter(is_active = True).all()
    serializer_class = BuyerSerializerListCreate

class BuyerAPIViewUpdate(GenericViewSet):
    queryset = Buyer.objects.filter(is_active = True).all()
    serializer_class = BuyerSerializerUpdate
    def partial_update(self,request,pk):
        producer_obj = get_object_or_404(Buyer,pk = pk)
        if producer_obj.is_active:
            serializer = self.get_serializer\
                (producer_obj,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

class BuyerApiVeiwDelete(GenericViewSet):
    queryset = Buyer.objects.filter(is_active = True).all()
    def destroy(self,request,pk):
        producer_obj = get_object_or_404(Buyer,pk = pk)   
        producer_obj.is_active = False
        producer_obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TransactionShowroomToBuyerAPIView(ListCreateAPIView,ViewSet):
    queryset = TransactionFromShowroomToBuyer.objects.all()
    serializer_class = TransactionFromShowroomAndBuyerSerializer
    def create(self,request):
        serializer = TransactionFromShowroomAndBuyerSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        showroom_obj = serializer.validated_data["showroom"]
        showroom = get_object_or_404(CarShowRoom.objects.filter(is_active = True)\
                                    ,pk = showroom_obj.id)
        buyer_obj = serializer.validated_data["buyer"]
        buyer = get_object_or_404(Buyer.objects.filter(is_active = True),\
                                    pk = buyer_obj.id)
        showroom.buyers_from_showroom.add(buyer)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
