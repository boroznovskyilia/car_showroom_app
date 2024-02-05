from django.urls import include, path
from rest_framework.routers import DefaultRouter

from buyer.views import (
    BuyerDeleteViewSet,
    BuyerListRetrieveViewSet,
    BuyerUpdateViewSet,
    TransactionShowroomToBuyerViewSet,
    BuyerRegisterViewSet,
    BuyerLoginAPIView,
    BuyerLogoutAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "buyers"

urlpatterns = [
    path(
        "buyers/",
        BuyerListRetrieveViewSet.as_view({"get": "list"}),
        name="buyers-list",
    ),
    path(
        "buyers/register/",
        BuyerRegisterViewSet.as_view({"post": "create"}),
        name="buyers-register",
    ),
    path(
        "buyers/login/",
        BuyerLoginAPIView.as_view({"post": "create"}),
        name="buyers-login",
    ),
    path(
        "buyers/logout/",
        BuyerLogoutAPIView.as_view({"post": "create"}),
        name="buyers-logout",
    ),
    path(
        "buyers/refresh/",
        TokenRefreshView.as_view(),
        name="buyers-refresh",
    ),
    path("buyers/update/<int:pk>/", BuyerUpdateViewSet.as_view({"put": "update"}), name="buyers-update"),
    path("buyers/account/update/", BuyerUpdateViewSet.as_view({"put": "update_account"}), name="buyers-update-account"),
    path("buyers/delete/<int:pk>/", BuyerDeleteViewSet.as_view({"delete": "destroy"}), name="buyers-delete"),
    path("buyers/account/delete/", BuyerDeleteViewSet.as_view({"delete": "delete_account"}), name="buyers-delete-account"),
    path(
        "buyers/transaction/",
        TransactionShowroomToBuyerViewSet.as_view({"get": "list", "post": "create"}),
        name="buyers-transaction",
    ),
    path("buyers/account/", BuyerListRetrieveViewSet.as_view({"get": "show_account"}), name="buyers-retrieve-account"),
    path("buyers/<int:pk>/", BuyerListRetrieveViewSet.as_view({"get": "retrieve"}), name="buyers-retrieve"),
]
