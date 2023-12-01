from django.urls import include, path
from rest_framework.routers import DefaultRouter

from buyer.views import (BuyerDeleteAPIView, BuyerListCreateAPIView,
                         BuyerUpdateAPIView, TransactionShowroomToBuyerAPIView)

router = DefaultRouter()

router.register(r"buyers", BuyerListCreateAPIView, basename="buyers")
router.register(r"buyers/update", BuyerUpdateAPIView, basename="buyers")
router.register(r"buyers/delete", BuyerDeleteAPIView, basename="buyers")
router.register(r"buyers/transaction", TransactionShowroomToBuyerAPIView, basename="buyers")

app_name = "buyers"
urlpatterns = [
    path("", include(router.urls)),
]
