from rest_framework.generics import ListCreateAPIView,CreateAPIView
from rest_framework.viewsets import ViewSet,GenericViewSet
from .serializer import CarShowRoomSerializerList,CarShowRoomSerializerCreate,\
    CarShowRoomSerializerUpdate,CarShowRoomStockSerializerCreate,CarShowRoomStockSerializserUpdate
from rest_framework.response import Response
from .models import CarShowRoom,CarShowRoomStock
from rest_framework import status
from django.shortcuts import get_object_or_404


class CarShowRoomAPIView(ListCreateAPIView, ViewSet):
    queryset = CarShowRoom.objects.filter(is_active = True)
    serializer_class = CarShowRoomSerializerList

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarShowRoomSerializerCreate
        elif self.request.method == 'PATCH':
            return CarShowRoomSerializerUpdate
        return super().get_serializer_class()

    def destroy(self,request,pk):
        car_showroom_obj = get_object_or_404(CarShowRoom,pk = pk)   
        car_showroom_obj.is_active = False
        car_showroom_obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self,request,pk):
        car_showroom_obj = get_object_or_404(CarShowRoom,pk = pk)
        if car_showroom_obj.is_active:
            serializer = self.get_serializer\
                (car_showroom_obj,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class CarShowRoomStockAPIViewCreate(GenericViewSet):
    queryset = CarShowRoomStock.objects.all()
    serializer_class = CarShowRoomStockSerializerCreate

    def create(self, request):
        serializer = CarShowRoomStockSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        showroom_obj = serializer.validated_data.get('show_room')
        showroom = get_object_or_404(CarShowRoom, pk=showroom_obj.id)
        if showroom.is_active:
            stock_data = serializer.validated_data  
            stock_data["show_room"] = showroom.id
            
            stock_serializer = CarShowRoomStockSerializerCreate(data=stock_data)
            stock_serializer.is_valid(raise_exception=True)
            stock_serializer.save()

            return Response(stock_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
class CarShowRoomStockAPIViewUpdate(GenericViewSet): 
    queryset = CarShowRoomStock.objects.all()
    serializer_class = CarShowRoomStockSerializserUpdate

    def partial_update(self,request,pk):
        show_room_stock_obj = get_object_or_404(CarShowRoomStock,pk = pk)
        serializer = CarShowRoomStockSerializserUpdate(show_room_stock_obj,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)