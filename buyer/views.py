from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from fabric.models import Transaction
from showroom.models import ShowRoom

from .models import Buyer
from .serializer import (BuyerListCreateSerializer, BuyerUpdateSerializer,
                         TransactionFromShowroomAndBuyerSerializer)


class BuyerListCreateAPIView(ListModelMixin, CreateModelMixin, GenericViewSet):
    def to_internal_value(self, data):
        if data["location"] == "":
            data["location"] = None
        return super().to_internal_value(data)

    def get_queryset(self):
        return Buyer.objects.get_active().all()

    serializer_class = BuyerListCreateSerializer


class BuyerUpdateAPIView(GenericViewSet):
    def get_queryset(self):
        return Buyer.objects.get_active().all()

    serializer_class = BuyerUpdateSerializer

    def partial_update(self, request, pk):
        producer_obj = get_object_or_404(Buyer, pk=pk)
        if producer_obj.is_active:
            serializer = self.get_serializer(producer_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class BuyerDeleteAPIView(GenericViewSet):
    def get_queryset(self):
        return Buyer.objects.get_active().all()

    def destroy(self, request, pk):
        producer_obj = get_object_or_404(Buyer, pk=pk)
        producer_obj.is_active = False
        producer_obj.save()
        return Response(status=status.HTTP_200_OK)


class TransactionShowroomToBuyerAPIView(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        return Transaction.objects.filter(fabric=None).all()

    serializer_class = TransactionFromShowroomAndBuyerSerializer

    def create(self, request):
        serializer = TransactionFromShowroomAndBuyerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        showroom_obj = serializer.validated_data["showroom"]
        showroom = get_object_or_404(ShowRoom.objects.get_active(), pk=showroom_obj.id)
        buyer_obj = serializer.validated_data["buyer"]
        buyer = get_object_or_404(Buyer.objects.get_active(), pk=buyer_obj.id)
        showroom.buyers.add(buyer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
