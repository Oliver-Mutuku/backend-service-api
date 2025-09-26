from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet, OrderViewSet, google_auth



router = DefaultRouter()
router.register(r"customers", CustomerViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("auth/google/", google_auth, name="google_auth")
]

