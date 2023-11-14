from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView
from rest_framework.viewsets import ViewSet
from .serializer import CarShowRoomSerializerList,CarShowRoomSerializerCreate,CarShowRoomSerializerUpdate
from rest_framework.response import Response
from .models import CarShowRoom 
from rest_framework import status
from django.shortcuts import get_object_or_404
import datetime

class CarShowRoomAPIView(ListCreateAPIView, ViewSet):
    queryset = CarShowRoom.objects.all()
    serializer_class = CarShowRoomSerializerList

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CarShowRoomSerializerCreate
        elif self.request.method == 'PATCH':
            return CarShowRoomSerializerUpdate
        return super().get_serializer_class()

    def partial_update(self,request,pk):
        car_showroom_obj = get_object_or_404(CarShowRoom,pk = pk)   
        serializer = CarShowRoomSerializerUpdate(car_showroom_obj,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)