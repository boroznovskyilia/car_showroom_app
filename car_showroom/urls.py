"""
URL configuration for car_showroom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from showroom.views import CarShowRoomAPIViewList,CarShowRoomStockAPIViewCreate,\
    CarShowRoomStockAPIViewUpdate,CarShowRoomAPIViewUpdate,CarShowRoomAPIViewDelete,\
    CarShowRoomAPIViewCreate,CarShowRoomStockAPIViewDelete
from producer.views import ProducerAPIVeiwCreate,ProducerAPIVeiwList,ProducerAPIVeiwUpdate,\
    ProducerApiVeiwDelete,ProducerStockAPIVeiwCreate,ProducerStockAPIVeiwUpdate,\
        ProducerStockAPIVeiwDelete,ProducerToShowroomTransaction
from buyer.views import BuyerAPIViewListCreate,BuyerAPIViewUpdate,BuyerApiVeiwDelete,\
TransactionShowroomToBuyerAPIView
schema_view = get_schema_view(
    openapi.Info(
        title="REST APIs",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

router.register(r'showroom',CarShowRoomAPIViewList,basename='showroom')
router.register(r'showroom/create',CarShowRoomAPIViewCreate,\
                basename='showroom')
router.register(r'showroom/update',CarShowRoomAPIViewUpdate,\
                basename='showroom')
router.register(r'showroom/delete',CarShowRoomAPIViewDelete,\
                basename='showroom')

router.register(r'showroom_stock/create',CarShowRoomStockAPIViewCreate,\
                basename='showroom_stock')
router.register(r'showroom_stock/update',CarShowRoomStockAPIViewUpdate,\
                basename='showroom_stock')
router.register(r'showroom_stock/delete',CarShowRoomStockAPIViewDelete,\
                basename='showroom_stock')

router.register(r'producer/list',ProducerAPIVeiwList,basename='producer')
router.register(r'producer/create',ProducerAPIVeiwCreate,basename='producer')
router.register(r'producer/update',ProducerAPIVeiwUpdate,basename='producer')
router.register(r'producer/delete',ProducerApiVeiwDelete,basename='producer')

router.register(r'producer_stock/create',ProducerStockAPIVeiwCreate,\
    basename='producer_stock')
router.register(r'producer_stock/update',ProducerStockAPIVeiwUpdate,\
    basename='producer_stock')
router.register(r'producer_stock/delete',ProducerStockAPIVeiwDelete,\
    basename='producer_stock')
router.register(r'producer_stock/transaction',ProducerToShowroomTransaction,\
    basename='producer_stock')

router.register(r'buyer',BuyerAPIViewListCreate,basename="buyer")
router.register(r'buyer/update',BuyerAPIViewUpdate,basename="buyer")
router.register(r'buyer/delete',BuyerApiVeiwDelete,basename="buyer")
router.register(r'buyer/transaction',TransactionShowroomToBuyerAPIView,basename="buyer")


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
]
urlpatterns+=router.urls