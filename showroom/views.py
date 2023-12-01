from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from fabric.models import Transaction
from fabric.models import Fabric
from .serializer import (
    ShowRoomListSerializer,
    ShowRoomCreateSerializer,
    ShowRoomUpdateSerializer,
    ShowRoomCarsCreateSerializer,
    ShowRoomCarsUpdateSerializer,
    TransactionBetweenFabricAndShowroom,
)
from rest_framework.response import Response
from .models import ShowRoom, ShowRoomCars
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch


class ShowRoomListAPIView(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        return (
            ShowRoom.objects.get_active()
            .all()
            .prefetch_related(Prefetch("show_room_cars", queryset=ShowRoomCars.objects.get_active().all()))
        )

    serializer_class = ShowRoomListSerializer


class ShowRoomCreateAPIView(CreateModelMixin, GenericViewSet):
    serializer_class = ShowRoomCreateSerializer


class ShowRoomUpdateAPIView(GenericViewSet):
    serializer_class = ShowRoomUpdateSerializer

    def get_queryset(self):
        return ShowRoom.objects.get_active().all()

    def partial_update(self, request, pk):
        car_showroom_obj = get_object_or_404(ShowRoom, pk=pk)
        if car_showroom_obj.is_active:
            serializer = self.get_serializer(car_showroom_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ShowRoomDeleteAPIView(GenericViewSet):
    def get_queryset(self):
        return ShowRoom.objects.get_active().all()

    def destroy(self, request, pk):
        car_showroom_obj = get_object_or_404(ShowRoom, pk=pk)
        car_showroom_obj.is_active = False
        car_showroom_obj.save()
        return Response(status=status.HTTP_200_OK)


class ShowRoomCarsCreateAPIView(GenericViewSet):
    serializer_class = ShowRoomCarsCreateSerializer

    def create(self, request):
        serializer = ShowRoomCarsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        showroom_obj = serializer.validated_data.get("show_room")
        showroom = get_object_or_404(ShowRoom, pk=showroom_obj.id)
        if showroom.is_active:
            stock_data = serializer.validated_data
            stock_data["show_room"] = showroom.id

            stock_serializer = ShowRoomCarsCreateSerializer(data=stock_data)
            stock_serializer.is_valid(raise_exception=True)
            stock_serializer.save()

            return Response(stock_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ShowRoomCarsUpdateAPIView(GenericViewSet):
    serializer_class = ShowRoomCarsUpdateSerializer

    def get_queryset(self):
        return ShowRoom.objects.get_active().all()

    def partial_update(self, request, pk):
        show_room_stock_obj = get_object_or_404(ShowRoomCars, pk=pk, **{"is_active": True})
        serializer = ShowRoomCarsUpdateSerializer(show_room_stock_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowRoomCarsDeleteAPIView(GenericViewSet):
    def get_queryset(self):
        return ShowRoom.objects.get_active().all()

    def destroy(self, request, pk):
        show_room_stock_obj = get_object_or_404(ShowRoomCars, pk=pk)
        show_room_stock_obj.is_active = False
        show_room_stock_obj.save()
        return Response(status=status.HTTP_200_OK)


class TransactionFabricToShowroomAPIView(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        return Transaction.objects.get_active().all()

    serializer_class = TransactionBetweenFabricAndShowroom

    def create(self, request):
        serializer = TransactionBetweenFabricAndShowroom(data=request.data)
        serializer.is_valid(raise_exception=True)
        showroom_obj = serializer.validated_data["showroom"]
        showroom = get_object_or_404(ShowRoom.objects.filter(is_active=True), pk=showroom_obj.id)
        fabric_obj = serializer.validated_data["fabric"]
        fabric = get_object_or_404(Fabric.objects.filter(is_active=True), pk=fabric_obj.id)
        fabric.showrooms.add(showroom)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
