from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch


class GoogleAuthTests(APITestCase):
    @patch("apps.core.views.requests.get")
    def test_google_auth_returns_jwts(self, mock_get):
        """
        Ensure that a valid Google ID token exchange returns access + refresh tokens.
        """
        # Mock Google token verification
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "email": "testuser@example.com",
            "name": "Test User"
        }

        url = reverse("google_auth")
        response = self.client.post(url, {"id_token": "FAKE_GOOGLE_ID_TOKEN"}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], "testuser@example.com")

    @patch("apps.core.views.requests.get")
    def test_google_auth_rejects_invalid_token(self, mock_get):
        """
        Ensure that an invalid Google ID token is rejected.
        """
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {"error": "invalid_token"}

        url = reverse("google_auth")
        response = self.client.post(url, {"id_token": "INVALID"}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)


    def test_google_auth_missing_token(self):
        url = reverse("google_auth")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    @patch("apps.core.views.requests.get")
    def test_google_auth_no_email_in_token(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "No Email User"}
        url = reverse("google_auth")
        response = self.client.post(url, {"id_token": "FAKE"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
