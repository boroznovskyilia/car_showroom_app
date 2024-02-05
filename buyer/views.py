from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin,RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from fabric.model_transaction import Transaction
from showroom.models import ShowRoom
from showroom.model_cars import ShowRoomCars
from .models import Buyer
from .serializer import (
    BuyerListSerializer,
    BuyerUpdateSerializer,
    BuyerLoginSerializer,
    BuyerRegisterSerializer,
    TransactionFromShowroomAndBuyerSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .utils import set_token_header

class BuyerRegisterViewSet(GenericViewSet):    
    serializer_class = BuyerRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        response = set_token_header(data,token)
        return response

class BuyerLoginAPIView(GenericViewSet):
    serializer_class = BuyerLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = RefreshToken.for_user(user)
        data = serializer.data
        response = set_token_header(data,token)
        return response

class BuyerLogoutAPIView(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BuyerListRetrieveViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerListSerializer

    def to_internal_value(self, data):
        if data["location"] == "":
            data["location"] = None
        return super().to_internal_value(data)  

    def get_queryset(self):
        return Buyer.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        JWTAuthentication().authenticate(request)
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        JWTAuthentication().authenticate(request)
        return super().retrieve(request, *args, **kwargs)
    
    @action(methods=['get'],detail=True,permission_classes=[IsAuthenticated])
    def show_account(self, request, *args, **kwargs):
        current_buyer = JWTAuthentication().authenticate(request)[0]
        serializer = self.get_serializer(current_buyer)
        return Response(serializer.data)

class BuyerUpdateViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerUpdateSerializer

    def get_queryset(self):
        return Buyer.objects.filter(is_active=True)

    def partial_update(self, request, pk):
        buyer_obj = get_object_or_404(Buyer, pk=pk)
        if buyer_obj.is_active:
            serializer = self.get_serializer(buyer_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['patch'],detail=True,permission_classes=[IsAuthenticated])
    def update_account(self, request, *args, **kwargs):
        current_buyer = JWTAuthentication().authenticate(request)[0]
        serializer = self.get_serializer(current_buyer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class BuyerDeleteViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Buyer.objects.filter(is_active=True)

    def destroy(self, request, pk):
        buyer_obj = get_object_or_404(Buyer, pk=pk)
        buyer_obj.is_active = False
        buyer_obj.save()
        return Response(status=status.HTTP_200_OK)
    
    @action(methods=['delete'],detail=True,permission_classes=[IsAuthenticated])
    def delete_account(self,request):
        current_buyer = JWTAuthentication().authenticate(request)[0]
        current_buyer.is_active = False
        current_buyer.save()
        return Response(status=status.HTTP_200_OK)


class TransactionShowroomToBuyerViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionFromShowroomAndBuyerSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(fabric=None).all()

    def create(self, request):
        serializer = TransactionFromShowroomAndBuyerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        showroom_obj = serializer.validated_data["showroom"]
        showroom = get_object_or_404(ShowRoom.objects.get_active(), pk=showroom_obj.id)
        buyer_obj = serializer.validated_data["buyer"]
        buyer = get_object_or_404(Buyer.objects.get_active(), pk=buyer_obj.id)
        showroom_car_obj = serializer.validated_data["showroom_car"]
        showroom_car = get_object_or_404(ShowRoomCars.objects.filter(is_active=True), pk=showroom_car_obj.id)
        showroom.buyers.add(buyer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    