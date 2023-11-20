from rest_framework.viewsets import ViewSet,GenericViewSet
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView
from .models import Producer,ProducerStock,TransactionProducerToShowRoom
from .serializer import ProducerSerializerCreate,ProducerSerializerList,ProducerSerializeUpdate,\
ProducerStockSerializerCreate,ProducerStockSerializerUpdate,TransactionBetweenProducerAndShowroom,\
TransactionBetweenProducerAndShowroomList
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from showroom.models import CarShowRoom

class ProducerAPIVeiwCreate(CreateAPIView,ViewSet):
    serializer_class = ProducerSerializerCreate

class ProducerAPIVeiwList(ListAPIView,ViewSet):
    queryset = Producer.objects.filter(is_active = True).all().\
        prefetch_related(Prefetch("producer_stock",queryset=ProducerStock.objects.\
                                  filter(is_active = True).all()))
    serializer_class = ProducerSerializerList

class ProducerAPIVeiwUpdate(GenericViewSet):
    serializer_class = ProducerSerializeUpdate
    queryset = Producer.objects.filter(is_active = True).all()
    def partial_update(self,request,pk):
        producer_obj = get_object_or_404(Producer,pk = pk)
        if producer_obj.is_active:
            serializer = self.get_serializer\
                (producer_obj,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

class ProducerApiVeiwDelete(ViewSet):
    queryset = Producer.objects.filter(is_active = True).all()
    def destroy(self,request,pk):
        producer_obj = get_object_or_404(Producer,pk = pk)   
        producer_obj.is_active = False
        producer_obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProducerStockAPIVeiwCreate(CreateAPIView,ViewSet):
    queryset = ProducerStock.objects.filter(is_active = True).all()
    serializer_class = ProducerStockSerializerCreate

class ProducerStockAPIVeiwUpdate(GenericViewSet):
    queryset = ProducerStock.objects.filter(is_active = True).all()
    serializer_class = ProducerStockSerializerUpdate

    def partial_update(self,request,pk):
        stock_obj = get_object_or_404(ProducerStock,pk = pk)
        if stock_obj.is_active:
            serializer = self.get_serializer\
                (stock_obj,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

class ProducerStockAPIVeiwDelete(GenericViewSet):
    queryset = ProducerStock.objects.filter(is_active = True).all()
    def destroy(self,request,pk):
        show_room_stock_obj = get_object_or_404(ProducerStock,pk = pk)
        show_room_stock_obj.is_active = False
        show_room_stock_obj.save()
        return Response(status=status.HTTP_200_OK)
    
class ProducerToShowroomTransaction(ListCreateAPIView,ViewSet):
    queryset = TransactionProducerToShowRoom.objects.all()
    serializer_class = TransactionBetweenProducerAndShowroom
    def create(self,request):
        serializer = TransactionBetweenProducerAndShowroom(data = request.data)
        serializer.is_valid(raise_exception=True)
        showroom_obj = serializer.validated_data["showroom"]
        showroom = get_object_or_404(CarShowRoom.objects.filter(is_active = True)\
                                    ,pk = showroom_obj.id)
        producer_obj = serializer.validated_data["producer"]
        producer = get_object_or_404(Producer.objects.filter(is_active = True),\
                                    pk = producer_obj.id)
        producer.buyers_from_producer.add(showroom)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    