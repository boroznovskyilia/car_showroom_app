from django.urls import include, path
from rest_framework.routers import DefaultRouter

from fabric.views import (FabricCarsCreateAPIView, FabricCarsDeleteAPIView,
                          FabricCarsUpdateAPIView, FabricCreateAPIView,
                          FabricDeleteAPIView, FabricListAPIView,
                          FabricUpdateAPIView)

router = DefaultRouter()

router.register(r"fabrics", FabricListAPIView, basename="fabrics")
router.register(r"fabrics/create", FabricCreateAPIView, basename="fabrics")
router.register(r"fabrics/update", FabricUpdateAPIView, basename="fabrics")
router.register(r"fabrics/delete", FabricDeleteAPIView, basename="fabrics")

router.register(r"fabrics_cars/create", FabricCarsCreateAPIView, basename="fabrics_cars")
router.register(r"fabrics_cars/update", FabricCarsUpdateAPIView, basename="fabrics_cars")
router.register(r"fabrics_cars/delete", FabricCarsDeleteAPIView, basename="fabrics_cars")
app_name = "fabrics"

urlpatterns = [
    path("", include(router.urls)),
]
