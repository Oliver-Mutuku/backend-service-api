import json
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.core.models import Customer, Order

User = get_user_model()


class CustomerViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="Test Customer", code="CUST001")

    def test_list_customers(self):
        url = reverse("customer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_customer(self):
        url = reverse("customer-list")
        data = {"name": "Another Customer", "code": "CUST002"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)


class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test", email="t@test.com", password="pass1234")
        self.customer = Customer.objects.create(name="Test Customer", code="CUST001")

    def test_unauthenticated_cannot_list_orders(self):
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_can_create_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("order-list")
        data = {"customer": self.customer.id, "item": "Laptop", "amount": "1999.99"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)