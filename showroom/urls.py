from django.urls import include, path
from rest_framework.routers import DefaultRouter

from showroom.views import (ShowRoomCarsCreateAPIView,
                            ShowRoomCarsDeleteAPIView,
                            ShowRoomCarsUpdateAPIView, ShowRoomCreateAPIView,
                            ShowRoomDeleteAPIView, ShowRoomListAPIView,
                            ShowRoomUpdateAPIView,
                            TransactionFabricToShowroomAPIView)

router = DefaultRouter()

router.register(r"showrooms", ShowRoomListAPIView, basename="showrooms")
router.register(r"showrooms/create", ShowRoomCreateAPIView, basename="showrooms")
router.register(r"showrooms/update", ShowRoomUpdateAPIView, basename="showrooms")
router.register(r"showrooms/delete", ShowRoomDeleteAPIView, basename="showrooms")
router.register(r"showrooms/transaction", TransactionFabricToShowroomAPIView, basename="showrooms")

router.register(r"showrooms_cars/create", ShowRoomCarsCreateAPIView, basename="showrooms_cars")
router.register(r"showrooms_cars/update", ShowRoomCarsUpdateAPIView, basename="showrooms_cars")
router.register(r"showrooms_cars/delete", ShowRoomCarsDeleteAPIView, basename="showrooms_cars")

app_name = "showrooms"

urlpatterns = [
    path("", include(router.urls)),
]
