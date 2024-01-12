from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Sale
from .serializer import SaleForShowRooomSerializer,SaleForFabricSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

class SaleForShowRoomViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    def get_queryset(self):
        return Sale.objects.filter(fabric_car=None)
    
    serializer_class = SaleForShowRooomSerializer
    
    def retrieve(self,request,pk):
        queryset = Sale.objects.filter(id=pk).prefetch_related("showroom_car")
        showroom_sale = get_object_or_404(queryset)
        serializer = self.serializer_class(showroom_sale)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # def destroy(self,request,pk):
    #     sale_obj = get_object_or_404(Sale, pk=pk)
    #     sale_obj.is_active = False
    #     sale_obj.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class SaleForFabricViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    def get_queryset(self):
        return Sale.objects.filter(showroom_car=None)
    
    serializer_class = SaleForFabricSerializer

    def retrieve(self,request,pk):
        queryset = Sale.objects.filter(id=pk).prefetch_related("fabric_car")
        fabric_sale = get_object_or_404(queryset)
        serializer = self.serializer_class(fabric_sale)
        return Response(serializer.data,status=status.HTTP_200_OK)
        