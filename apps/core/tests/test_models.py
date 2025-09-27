from django.test import TestCase
from apps.core.models import Customer, Order

class ModelStrTests(TestCase):
    def test_customer_str(self):
        c = Customer.objects.create(name="John Doe", code="C123")
        self.assertEqual(str(c), "John Doe - (C123)")

    def test_order_str(self):
        c = Customer.objects.create(name="John Doe", code="C123")
        o = Order.objects.create(customer=c, item="Phone", amount=500)
        self.assertIn("Order #", str(o))
        self.assertIn("Phone", str(o))
