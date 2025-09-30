from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch


class GoogleAuthTests(APITestCase):

    @patch("apps.core.views.requests.get")
    def test_google_auth_returns_jwts(self, mock_get):
        """
        Ensure that posting a valid Google ID token returns JWT access + refresh tokens.
        """
        # Mock Google response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "email": "testuser@example.com",
            "name": "Test User",
        }

        # Fake ID token (could be any string since we mock Google)
        payload = {"id_token": "FAKE_GOOGLE_ID_TOKEN"}

        url = reverse("google_auth")  # name="google_auth" in urls.py
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["email"], "testuser@example.com")
