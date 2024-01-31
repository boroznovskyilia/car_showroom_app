from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from showroom.models import ShowRoom

from .models import Fabric
from .model_cars import FabricCars
from .model_transaction import Transaction
from .serializer import (
    FabricCarsSerializerCreate,
    FabricCarsSerializerUpdate,
    FabricSerializerCreate,
    FabricSerializerList,
    FabricSerializeUpdate,
)


class FabricCreateViewSet(CreateModelMixin, GenericViewSet):
    def to_internal_value(self, data):
        if data["location"] == "":
            data["location"] = None
        return super().to_internal_value(data)

    serializer_class = FabricSerializerCreate


class FabricListViewSet(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        return (
            Fabric.objects.filter(is_active=True)
            .all()
            .prefetch_related(Prefetch("fabric_cars", queryset=FabricCars.objects.filter(is_active=True)))
        )

    serializer_class = FabricSerializerList


class FabricUpdateViewSet(GenericViewSet):
    serializer_class = FabricSerializeUpdate

    def get_queryset(self):
        return Fabric.objects.filter(is_active=True)

    def partial_update(self, request, pk):
        Fabric_obj = get_object_or_404(Fabric, pk=pk)
        if Fabric_obj.is_active:
            serializer = self.get_serializer(Fabric_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class FabricDeleteViewSet(GenericViewSet):
    def get_queryset(self):
        return Fabric.objects.filter(is_active=True)

    def destroy(self, request, pk):
        Fabric_obj = get_object_or_404(Fabric, pk=pk)
        Fabric_obj.is_active = False
        Fabric_obj.save()
        return Response(status=status.HTTP_200_OK)


class FabricCarsCreateViewSet(CreateModelMixin, GenericViewSet):
    def get_queryset(self):
        return FabricCars.objects.filter(is_active=True)

    serializer_class = FabricCarsSerializerCreate


class FabricCarsUpdateViewSet(GenericViewSet):
    def get_queryset(self):
        return FabricCars.objects.filter(is_active=True)

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


class FabricCarsDeleteViewSet(GenericViewSet):
    def get_queryset(self):
        return FabricCars.objects.filter(is_active=True)

    def destroy(self, request, pk):
        show_room_stock_obj = get_object_or_404(FabricCars, pk=pk)
        show_room_stock_obj.is_active = False
        show_room_stock_obj.save()
        return Response(status=status.HTTP_200_OK)
