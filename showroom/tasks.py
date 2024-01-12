from celery import shared_task

import logging

from datetime import datetime,timezone
from fabric.model_cars import FabricCars
from fabric.model_transaction import Transaction

from .models import ShowRoom
from .model_cars import ShowRoomCars
from django.db.models import Prefetch
from django.db.models import (
    Count,
    OuterRef,
    Subquery,
)
from django.db import transaction


logger = logging.getLogger(__name__)

@shared_task
def sutable_cars():
    try:
        showrooms = ShowRoom.objects.filter(is_active=True).prefetch_related(
                Prefetch(
                    "show_room_cars",
                    ShowRoomCars.objects.filter(is_active=True).prefetch_related(
                        Prefetch("fabric_car", FabricCars.objects.filter(is_active=True))
                    ),
                )
            )
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
            with transaction.atomic():
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
    except Exception as e:
        logger.exception("An error occurred during task execution")
        raise e


@shared_task
def make_transactions():
    try:
        showrooms = ShowRoom.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "show_room_cars",
                ShowRoomCars.objects.filter(is_active=True)
                .prefetch_related("fabric_car")
                .annotate(popularity=Count("fabric_car__transactions__id", distinct=True))
                .order_by("-popularity"),
            )
        )
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
                        other_showroom_cars = ShowRoomCars.objects.filter(
                            is_active=True,
                            fabric_car__model=showroom_car.fabric_car.model,
                            fabric_car__price__range=(showroom.min_price,showroom.max_price),
                            show_room__id__ne=showroom.id,  
                        ).order_by("fabric_car__price")
                        #find the most sutable variant
                        result_car = other_showroom_cars.first()
                        result_price = result_car.price
                        for other_car in other_showroom_cars:
                            sale = 0
                            if other_car.fabric_car.sale.filter().exists():  
                                sale_obj = other_car.fabric_car.sale.first()
                                if (sale_obj.date_of_start <= datetime.now(timezone.utc) and 
                                    sale_obj.date_of_end >= datetime.now(timezone.utc)):
                                    sale = sale_obj.percent
                            price_with_sale = other_car.fabric_car.price*(1-sale/100)
                            if(price_with_sale<result_price):
                                result_price=other_car
                                result_price=price_with_sale
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
                            if showroom.show_room_cars.filter(id = result_car.id).exists():
                                result_car.amount+=1
                                result_car.save()
                            else:
                                new_car = ShowRoomCars.objects.create(
                                    show_room=showroom,
                                    amount=1,
                                )
                                showroom.show_room_cars.add(new_car)        
        return showrooms
    except Exception as e:
        logger.exception("An error occurred during task execution")
        raise e