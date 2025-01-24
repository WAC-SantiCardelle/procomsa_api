from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderInfoViewSet, OrderDataViewSet, StatusTypeViewSet

router = DefaultRouter()
router.register(r'pedidos', OrderInfoViewSet)
router.register(r'lineas', OrderDataViewSet)
router.register(r'estados', StatusTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
