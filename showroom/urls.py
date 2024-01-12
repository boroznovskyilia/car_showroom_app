from django.urls import include, path
from rest_framework.routers import DefaultRouter

from showroom.views import (
    # ShowRoomCarsCreateViewSet,
    ShowRoomCarsDeleteViewSet,
    # ShowRoomCarsUpdateViewSet,
    ShowRoomCreateViewSet,
    ShowRoomDeleteViewSet,
    ShowRoomListViewSet,
    ShowRoomUpdateViewSet,
    TransactionFabricToShowroomViewSet,
    SutableCarsView,
    MakeTransactionsView,
)
from sales.views import SaleForShowRoomViewSet

router = DefaultRouter()

app_name = "showrooms"

urlpatterns = [
    path("showrooms/", ShowRoomListViewSet.as_view({"get": "list"}), name="showrooms-list"),
    path("showrooms/create/", ShowRoomCreateViewSet.as_view({"post": "create"}), name="showrooms-create"),
    path(
        "showrooms/update/<int:pk>/",
        ShowRoomUpdateViewSet.as_view({"put": "update"}),
        name="showrooms-update",
    ),
    path(
        "showrooms/delete/<int:pk>/",
        ShowRoomDeleteViewSet.as_view({"delete": "destroy"}),
        name="showrooms-delete",
    ),
    path(
        "showrooms/transaction/",
        TransactionFabricToShowroomViewSet.as_view({"get": "list", "post": "create"}),
        name="showrooms-transaction",
    ),
    path("showrooms/sutable_cars/", SutableCarsView.as_view({"get": "list"}), name="showrooms-sutable-cars"),
    path(
        "showrooms/make_transactions/",
        MakeTransactionsView.as_view({"get": "list"}),
        name="showrooms-make-transactions",
    ),
    path(
        "showrooms/cars/delete/<int:pk>/",
        ShowRoomCarsDeleteViewSet.as_view({"delete": "destroy"}),
        name="showrooms-cars-delete",
    ),
    path(
        "showrooms/sales/",
        SaleForShowRoomViewSet.as_view({"get":"list"}),name="showrooms-sale-list"
    ),
    path(
        "showrooms/sales/create/",
        SaleForShowRoomViewSet.as_view({"post":"create"}),name="showrooms-sale-create"
    ),
    path(
        "showrooms/sales/<int:pk>/",
        SaleForShowRoomViewSet.as_view({"get":"retrieve"}),name="showrooms-sales-get"
    )
]
