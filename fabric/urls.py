from django.urls import include, path
from rest_framework.routers import DefaultRouter

from fabric.views import (
    FabricCarsCreateViewSet,
    FabricCarsDeleteViewSet,
    FabricCarsUpdateViewSet,
    FabricCreateViewSet,
    FabricDeleteViewSet,
    FabricListViewSet,
    FabricUpdateViewSet,
)
from sales.views import SaleForFabricViewSet

app_name = "fabrics"

urlpatterns = [
    path("fabrics/", FabricListViewSet.as_view({"get": "list"}), name="fabrics-list"),
    path("fabrics/create/", FabricCreateViewSet.as_view({"post": "create"}), name="fabrics-create"),
    path("fabrics/update/<int:pk>/", FabricUpdateViewSet.as_view({"put": "update"}), name="fabrics-update"),
    path(
        "fabrics/delete/<int:pk>/", FabricDeleteViewSet.as_view({"delete": "destroy"}), name="fabrics-delete"
    ),
    path(
        "fabrics/cars/create/",
        FabricCarsCreateViewSet.as_view({"post": "create"}),
        name="fabrics-cars-create",
    ),
    path(
        "fabrics/cars/update/<int:pk>/",
        FabricCarsUpdateViewSet.as_view({"put": "update"}),
        name="fabrics-cars-update",
    ),
    path(
        "fabrics/cars/delete/<int:pk>/",
        FabricCarsDeleteViewSet.as_view({"delete": "destroy"}),
        name="fabrics-cars-delete",
    ),
        path(
        "fabrics/sales/",
        SaleForFabricViewSet.as_view({"get":"list"}),name="fabrics-sale-list"
    ),
    path(
        "fabrics/sales/create/",
        SaleForFabricViewSet.as_view({"post":"create"}),name="fabrics-sale-create"
    ),
    path(
        "fabrics/sales/<int:pk>/",
        SaleForFabricViewSet.as_view({"get":"retrieve"}),name="fabrics-sales-get"
    )
]
