from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from showroom.models import ShowRoom

from .models import Fabric, FabricCars, Transaction
from .serializer import (FabricCarsSerializerCreate,
                         FabricCarsSerializerUpdate, FabricSerializerCreate,
                         FabricSerializerList, FabricSerializeUpdate)


class FabricCreateAPIView(CreateModelMixin, GenericViewSet):
    def to_internal_value(self, data):
        if data["location"] == "":
            data["location"] = None
        return super().to_internal_value(data)

    serializer_class = FabricSerializerCreate


class FabricListAPIView(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        return (
            Fabric.objects.get_active()
            .all()
            .prefetch_related(Prefetch("fabric_cars", queryset=FabricCars.objects.get_active().all()))
        )

    serializer_class = FabricSerializerList


class FabricUpdateAPIView(GenericViewSet):
    serializer_class = FabricSerializeUpdate

    def get_queryset(self):
        return Fabric.objects.get_active().all()

    def partial_update(self, request, pk):
        Fabric_obj = get_object_or_404(Fabric, pk=pk)
        if Fabric_obj.is_active:
            serializer = self.get_serializer(Fabric_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FabricDeleteAPIView(GenericViewSet):
    def get_queryset(self):
        return Fabric.objects.get_active().all()

    def destroy(self, request, pk):
        Fabric_obj = get_object_or_404(Fabric, pk=pk)
        Fabric_obj.is_active = False
        Fabric_obj.save()
        return Response(status=status.HTTP_200_OK)


class FabricCarsCreateAPIView(CreateModelMixin, GenericViewSet):
    def get_queryset(self):
        return FabricCars.objects.get_active().all()

    serializer_class = FabricCarsSerializerCreate


class FabricCarsUpdateAPIView(GenericViewSet):
    def get_queryset(self):
        return FabricCars.objects.get_active().all()

    serializer_class = FabricCarsSerializerUpdate

    def partial_update(self, request, pk):
        stock_obj = get_object_or_404(FabricCars, pk=pk)
        if stock_obj.is_active:
            serializer = self.get_serializer(stock_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FabricCarsDeleteAPIView(GenericViewSet):
    def get_queryset(self):
        return FabricCars.objects.get_active().all()

    def destroy(self, request, pk):
        show_room_stock_obj = get_object_or_404(FabricCars, pk=pk)
        show_room_stock_obj.is_active = False
        show_room_stock_obj.save()
        return Response(status=status.HTTP_200_OK)
