from django.urls import path, include
from .views import CustomerViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"customers", CustomerViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

