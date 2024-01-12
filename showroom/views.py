from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from buyer.models import Buyer
from datetime import datetime,timezone
from fabric.model_transaction import Transaction
from fabric.models import Fabric
from fabric.model_cars import FabricCars
from .serializer import (
    ShowRoomCarWithPopularitySerializer,
    ShowRoomListSerializer,
    ShowRoomCreateSerializer,
    ShowRoomUpdateSerializer,
    # ShowRoomCarsCreateSerializer,
    # ShowRoomCarsUpdateSerializer,
    TransactionBetweenFabricAndShowroom,
    SutableCarsSerializer,
    MakeTransactionsSerializer,
)
from rest_framework.response import Response
from .models import ShowRoom
from .model_cars import ShowRoomCars
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.db.models import (
    Count,
    F,
    Value,
    Case,
    When,
    IntegerField,
    Min,
    Max,
    OuterRef,
    Subquery,
    Exists,
    ExpressionWrapper,
)
from django.db.models.functions import Coalesce
from django.db import transaction


class ShowRoomListViewSet(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        return (
            ShowRoom.objects.filter(is_active=True)
            .all()
            .prefetch_related(
                Prefetch(
                    "show_room_cars",
                    queryset=ShowRoomCars.objects.filter(is_active=True).prefetch_related(
                        Prefetch("fabric_car", queryset=FabricCars.objects.filter(is_active=True))
                    ).annotate(popularity=Count("fabric_car__transactions__id", distinct=True))
                    .order_by("-popularity"),
                ),
                Prefetch(
                    "buyers",
                    queryset=Buyer.objects.annotate(
                        num_of_transaction=Count(
                            Case(
                                When(
                                    transactions__showroom=F("showroom"),
                                    transactions__buyer=F("pk"),
                                    then=Value(1),
                                ),
                                default=None,
                            ),
                            output_field=IntegerField(),
                        )
                    ),
                ),
            )
        )

    serializer_class = ShowRoomListSerializer


class ShowRoomCreateViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = ShowRoomCreateSerializer


class ShowRoomUpdateViewSet(GenericViewSet):
    serializer_class = ShowRoomUpdateSerializer

    def get_queryset(self):
        return ShowRoom.objects.get_active().all()

    def update(self, request, pk):
        car_showroom_obj = get_object_or_404(ShowRoom, pk=pk)
        if car_showroom_obj.is_active:
            serializer = self.get_serializer(car_showroom_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ShowRoomDeleteViewSet(GenericViewSet):
    def get_queryset(self):
        return ShowRoom.objects.get_active().all()

    def destroy(self, request, pk):
        car_showroom_obj = get_object_or_404(ShowRoom, pk=pk)
        car_showroom_obj.is_active = False
        car_showroom_obj.save()
        return Response(status=status.HTTP_200_OK)


# class ShowRoomCarsCreateViewSet(GenericViewSet):
#     serializer_class = ShowRoomCarsCreateSerializer

#     def create(self, request):
#         serializer = ShowRoomCarsCreateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         showroom_obj = serializer.validated_data.get("show_room")
#         showroom = get_object_or_404(ShowRoom, pk=showroom_obj.id)
#         if showroom.is_active:
#             stock_data = serializer.validated_data
#             stock_data["show_room"] = showroom.id

#             stock_serializer = ShowRoomCarsCreateSerializer(data=stock_data)
#             stock_serializer.is_valid(raise_exception=True)
#             stock_serializer.save()

#             return Response(stock_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)


# class ShowRoomCarsUpdateViewSet(GenericViewSet):
#     serializer_class = ShowRoomCarsUpdateSerializer

#     def get_queryset(self):
#         return ShowRoom.objects.get_active().all()

#     def partial_update(self, request, pk):
#         show_room_stock_obj = get_object_or_404(ShowRoomCars, pk=pk, **{"is_active": True})
#         serializer = ShowRoomCarsUpdateSerializer(show_room_stock_obj, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ShowRoomCarsDeleteViewSet(GenericViewSet):
    def get_queryset(self):
        return ShowRoom.objects.get_active().all()

    def destroy(self, request, pk):
        show_room_stock_obj = get_object_or_404(ShowRoomCars, pk=pk)
        show_room_stock_obj.is_active = False
        # showroom_cars = ShowRoomCars.objects.filter(is_active = True,id__gt = pk).update(is_active = False)
        show_room_stock_obj.save()
        return Response(status=status.HTTP_200_OK)


class TransactionFabricToShowroomViewSet(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        return Transaction.objects.filter(buyer=None).all()

    serializer_class = TransactionBetweenFabricAndShowroom

    def create(self, request):
        serializer = TransactionBetweenFabricAndShowroom(data=request.data)
        serializer.is_valid(raise_exception=True)
        showroom_obj = serializer.validated_data["showroom"]
        showroom = get_object_or_404(
            ShowRoom.objects.filter(is_active=True).prefetch_related(
                Prefetch("show_room_cars", queryset=ShowRoomCars.objects.filter(is_active=True))
            ),
            pk=showroom_obj.id,
        )
        fabric_obj = serializer.validated_data["fabric"]
        fabric = get_object_or_404(Fabric.objects.filter(is_active=True), pk=fabric_obj.id)
        fabric_car_obj = serializer.validated_data["fabric_car"]
        fabric_car = get_object_or_404(
            FabricCars.objects.filter(is_active=True), pk=fabric_car_obj.id, fabric=fabric_obj.id
        )
        showroom_car_exist = ShowRoomCars.objects.filter(fabric_car=fabric_car, show_room=showroom).exists()

        if not showroom_car_exist:
            showroom_car = ShowRoomCars.objects.get(fabric_car=fabric_car, show_room=showroom)
            showroom_car.amount += 1
            showroom_car.save()
        else:
            showroom_car = ShowRoomCars.objects.create(show_room=showroom, amount=1)
            fabric_car.showroom_cars = showroom_car
            fabric_car.save()
            showroom_car.save()

        fabric.showrooms.add(showroom)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SutableCarsView(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        showrooms = ShowRoom.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "show_room_cars",
                ShowRoomCars.objects.filter(is_active=True).prefetch_related(
                    Prefetch("fabric_car", FabricCars.objects.filter(is_active=True))
                ),
            )
        )
        with transaction.atomic():
            for showroom in showrooms:
                min_price, max_price = showroom.min_price, showroom.max_price

                min_price_subquery = (
                    FabricCars.objects.filter(
                        is_active=True, model=OuterRef("model"), price__range=(min_price, max_price)
                    )
                    .order_by("price")
                    .values("price")[:1]
                )

                sutable_cars = FabricCars.objects.filter(is_active=True, price=Subquery(min_price_subquery))
                for sutable_car in sutable_cars:
                    showroom_car = showroom.show_room_cars.filter(
                        is_active=True, fabric_car__model=sutable_car.model, fabric_car__price=sutable_car.price
                    )
                    if not showroom_car.exists():
                        showroom.show_room_cars.filter(
                            is_active=True, fabric_car__model=sutable_car.model
                        ).update(is_active=False)
                        new_car = ShowRoomCars.objects.create(
                            show_room=showroom,
                            amount=0,
                        )
                        sutable_car.showroom_cars.add(new_car)

        return showrooms

    serializer_class = SutableCarsSerializer


class MakeTransactionsView(ListModelMixin, GenericViewSet):
    def get_queryset(self):
        showrooms = ShowRoom.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "show_room_cars",
                ShowRoomCars.objects.filter(is_active=True)
                .prefetch_related(Prefetch(
                        "fabric_car",FabricCars.objects.filter(is_active=True).prefetch_related("sale")
                    )              
                )
                .annotate(popularity=Count("fabric_car__transactions__id", distinct=True))
                .order_by("-popularity"),
            )
        )
        return showrooms

    serializer_class = MakeTransactionsSerializer

    def list(self, request):
        showrooms = self.get_queryset()
        with transaction.atomic():
            for showroom in showrooms:
                for showroom_car in showroom.show_room_cars.all():
                    sale = 0
                    #calculate price with sale (can be implemented as separate function)
                    if showroom_car.fabric_car.sale.filter().exists():  
                        sale_obj = showroom_car.fabric_car.sale.first()
                        if (sale_obj.date_of_start <= datetime.now(timezone.utc) and 
                            sale_obj.date_of_end >= datetime.now(timezone.utc)):
                            sale = sale_obj.percent
                    price_with_sale = showroom_car.fabric_car.price*(1-sale/100)
                    if showroom.balance >= price_with_sale:
                        # find cars with the same model in other showrooms
                        other_showroom_cars = (ShowRoomCars.objects.filter(
                            is_active=True,
                            fabric_car__model=showroom_car.fabric_car.model,
                            fabric_car__price__range=(showroom.min_price, showroom.max_price),
                        ).prefetch_related("fabric_car").exclude(show_room__id=showroom.id)
                        .order_by("fabric_car__price"))
                        #find the most sutable variant
                        result_price = float("inf") 
                        if other_showroom_cars.exists():
                            result_car = other_showroom_cars.first()
                            result_price = result_car.fabric_car.price
                            for other_car in other_showroom_cars:
                                sale = 0
                                if other_car.fabric_car.sale.filter().exists():  
                                    sale_obj = other_car.fabric_car.sale.first()
                                    if (sale_obj.date_of_start <= datetime.now(timezone.utc) and 
                                        sale_obj.date_of_end >= datetime.now(timezone.utc)):
                                        sale = sale_obj.percent
                                other_price_with_sale = other_car.fabric_car.price*(1-sale/100)
                                if(other_price_with_sale<result_price):
                                    result_car=other_car
                                    result_price=other_price_with_sale
                        # showroom_car price less than minimar price of car from other showrooms
                        if(price_with_sale<=result_price):
                            showroom.balance -= showroom_car.fabric_car.price
                            showroom_car.amount += 1
                            Transaction.objects.create(
                                showroom=showroom,
                                fabric=showroom_car.fabric_car.fabric,
                                fabric_car=showroom_car.fabric_car,
                            )
                            showroom_car.fabric_car.fabric.showrooms.add(showroom)
                            showroom_car.save()
                            showroom.save()
                        else:
                            showroom.balance-=result_price
                            if showroom.show_room_cars.filter(
                                    fabric_car__model=result_car.fabric_car.model,
                                    fabric_car__fabric=result_car.fabric_car.fabric,
                                    fabric_car__price=result_car.fabric_car.price,
                                ).exists():
                                result_car.amount+=1
                                result_car.save()
                            else:
                                new_car = ShowRoomCars.objects.create(
                                    fabric_car=result_car.fabric_car,
                                    show_room=showroom,
                                    amount=1,
                                )
                                Transaction.objects.create(
                                    showroom=showroom,
                                    fabric=showroom_car.fabric_car.fabric,
                                    fabric_car=showroom_car.fabric_car,
                                )
                                # showroom.show_room_cars.add(new_car)    
        # with transaction.atomic():
        #     for showroom in showrooms:
        #         for showroom_car in showroom.show_room_cars.all():
        #             sale = 0
        #             if showroom_car.fabric_car.sale.exists():          #can be implemented as separate function
        #                 sale_obj = showroom_car.fabric_car.sale.first()
        #                 if (sale_obj.date_of_start <= datetime.now(timezone.utc) and 
        #                         sale_obj.date_of_end >= datetime.now(timezone.utc)):
        #                     sale = sale_obj.percent
        #             if showroom.balance >= showroom_car.fabric_car.price:
        #                 showroom.balance -= int(showroom_car.fabric_car.price*(1-sale/100))
        #                 showroom_car.amount += 1
        #                 Transaction.objects.create(
        #                     showroom=showroom,
        #                     fabric=showroom_car.fabric_car.fabric,
        #                     fabric_car=showroom_car.fabric_car,
        #                 )
        #                 showroom_car.fabric_car.fabric.showrooms.add(showroom)
        #                 showroom_car.save()
        #                 showroom.save()
        return super().list(request)
