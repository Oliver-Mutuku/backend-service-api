import json
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Customer, Order

User = get_user_model()


class CustomerViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="John Doe", code="C001")
        self.url = reverse("customer-list")  # DRF router name

    def test_list_customers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_customer(self):
        data = {"name": "Jane Smith", "code": "C002"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)


class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="Oliver", code="C123")
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="pass123")
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        self.url = reverse("order-list")

    def test_list_orders_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_authenticated(self):
        data = {"customer": self.customer.id, "item": "Laptop", "amount": "2500.00"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_unauthenticated_access_denied(self):
        client = APIClient()  # no token
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GoogleAuthTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("google_auth")  # add this name in urls.py

    @patch("apps.core.views.requests.get")
    def test_google_auth_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "email": "test@example.com",
            "name": "Test User"
        }

        response = self.client.post(self.url, {"id_token": "valid_token"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_google_auth_missing_token(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "ID token is required")

    @patch("apps.core.views.requests.get")
    def test_google_auth_invalid_token(self, mock_get):
        mock_get.return_value.status_code = 400
        response = self.client.post(self.url, {"id_token": "bad_token"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid ID token")
