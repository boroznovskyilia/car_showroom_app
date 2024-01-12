from django.urls import include, path
from rest_framework.routers import DefaultRouter

from buyer.views import (
    BuyerDeleteViewSet,
    BuyerListCreateViewSet,
    BuyerUpdateViewSet,
    TransactionShowroomToBuyerViewSet,
)

router = DefaultRouter()

router.register(r"buyers", BuyerListCreateViewSet, basename="buyers")
router.register(r"buyers/update", BuyerUpdateViewSet, basename="buyers")
router.register(r"buyers/delete", BuyerDeleteViewSet, basename="buyers")
router.register(r"buyers/transaction", TransactionShowroomToBuyerViewSet, basename="buyers")

app_name = "buyers"

urlpatterns = [
    path(
        "buyers/",
        BuyerListCreateViewSet.as_view({"get": "list", "post": "create"}),
        name="buyers-list-create",
    ),
    path("buyers/update/<int:pk>/", BuyerUpdateViewSet.as_view({"put": "update"}), name="buyers-update"),
    path("buyers/delete/<int:pk>/", BuyerDeleteViewSet.as_view({"delete": "destroy"}), name="buyers-delete"),
    path(
        "buyers/transaction/",
        TransactionShowroomToBuyerViewSet.as_view({"get": "list", "post": "create"}),
        name="buyers-transaction",
    ),
]
