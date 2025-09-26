import requests
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets

from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer

User = get_user_model()

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([AllowAny])
def google_auth(request):
    """
    Verify Google ID token, create/retrieve user,
    then return JWT access + refresh tokens.
    """
    id_token = request.data.get("id_token")

    if not id_token:
        return Response({"error": "ID token is required"}, status=400)

    # Verify with Google
    resp = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token})
    if resp.status_code != 200:
        return Response({"error": "Invalid ID token"}, status=400)

    user_info = resp.json()
    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        return Response({"error": "Email not found in token"}, status=400)

    # Get or create user
    user, _ = User.objects.get_or_create(
        email=email,
        defaults={"username": email.split("@")[0]}
    )

    # Issue JWT tokens
    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }
    })



