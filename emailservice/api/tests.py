from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.
class EmailMessageTestCase(TestCase):
    """Tests for /email endpoint."""

    def setUp(self):
        """Set up client."""
        self.client = APIClient()

    def test_send_email_passing(self):
        """Send a successful email message."""
        response = self.client.post(
            "/email",
            {
                "to": "pearsongoulart@gmail.com",
                "to_name": "Alexander",
                "from": "pearsongoulart@icloud.com",
                "from_name": "Alexander",
                "subject": "Testing",
                "body": "Testing",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
