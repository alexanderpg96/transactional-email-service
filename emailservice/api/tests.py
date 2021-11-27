from django.test import TestCase
from rest_framework.test import APIClient
from unittest import mock
from api import utils


def mocked_request_post(*args, **kwargs):
    """Used for unittest mock.patch to mock requests package."""

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse({"message": "Test message", "errors": "Hello world"}, args[0])


class EmailMessageTestCase(TestCase):
    """Tests for /email endpoint."""

    def setUp(self):
        """Set up client."""
        self.client = APIClient()

    @mock.patch("api.views.send_email")
    def test_send_email_passing(self, mock_send_email):
        """Send a successful email message."""
        mock_send_email.return_value = {
            "message": "Pass",
            "status_code": 200,
            "type": "MAILGUN",
        }
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Pass", "service": "MAILGUN"})

    @mock.patch("api.views.send_email")
    def test_send_email_passing_sendgrid(self, mock_send_email):
        """Send a successful email message with sendgrid."""
        mock_send_email.return_value = {
            "message": "Pass",
            "status_code": 204,
            "type": "SENDGRID",
        }
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
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {"message": "Pass", "service": "SENDGRID"})

    @mock.patch("api.views.send_email")
    def test_send_email_fail(self, mock_send_email):
        """Send a successful email message with sendgrid."""
        mock_send_email.return_value = {
            "message": "Fail",
            "status_code": 403,
            "type": "MAILGUN",
        }
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
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"message": "Fail", "service": "MAILGUN"})

    @mock.patch("api.utils.send_to_mailgun")
    def test_send_email(self, mock_send_to_mailgun):
        """Test send_email util function."""
        email_data = {
            "to_email": "pearsongoulart@gmail.com",
            "to_name": "Alexander",
            "from_email": "pearsongoulart@icloud.com",
            "from_name": "Alexander",
            "subject": "Testing v2",
            "body": "<h1>Testing</h1><p>Hello</p>",
        }
        utils.send_email(email_data)
        mock_send_to_mailgun.assert_called_with(email_data)

    def test_html_to_plain_text(self):
        """Test html_to_plain_text util function."""
        html = "<h1>Hello</h1><p>world</p>"
        resp = utils.html_to_plain_text(html)
        self.assertEqual(resp, "Hello\n\nworld")

    @mock.patch("api.utils.send_to_sendgrid")
    def test_send_email_sendgrid_override(self, mock_send_to_sendgrid):
        """Test send_email util function with override."""
        email_data = {
            "to_email": "pearsongoulart@gmail.com",
            "to_name": "Alexander",
            "from_email": "pearsongoulart@icloud.com",
            "from_name": "Alexander",
            "subject": "Testing v2",
            "body": "<h1>Testing</h1><p>Hello</p>",
        }
        utils.send_email(email_data, True)
        mock_send_to_sendgrid.assert_called_with(email_data)

    @mock.patch("api.utils.requests")
    def test_send_email_mailgun(self, mock_requests):
        """Test send_to_mailgun util function."""
        mock_requests.post.return_value = mocked_request_post(200)
        email_data = {
            "to_email": "pearsongoulart@gmail.com",
            "to_name": "Alexander",
            "from_email": "pearsongoulart@icloud.com",
            "from_name": "Alexander",
            "subject": "Testing v2",
            "body": "<h1>Testing</h1><p>Hello</p>",
        }
        resp = utils.send_to_mailgun(email_data)
        self.assertEqual(resp["status_code"], 200)
        self.assertEqual(resp["message"], "Test message")
        self.assertEqual(resp["type"], "MAILGUN")

    @mock.patch("api.utils.requests")
    def test_send_email_sendgrid(self, mock_requests):
        """Test send_to_sendgrid util function."""
        mock_requests.post.return_value = mocked_request_post(202)
        email_data = {
            "to_email": "pearsongoulart@gmail.com",
            "to_name": "Alexander",
            "from_email": "pearsongoulart@icloud.com",
            "from_name": "Alexander",
            "subject": "Testing v2",
            "body": "<h1>Testing</h1><p>Hello</p>",
        }
        resp = utils.send_to_sendgrid(email_data)
        self.assertEqual(resp["status_code"], 202)
        self.assertEqual(resp["message"], "Your message has been sent")
        self.assertEqual(resp["type"], "SENDGRID")

    @mock.patch("api.utils.requests")
    def test_send_email_sendgrid_error(self, mock_requests):
        """Test send_to_sendgrid util function - ERRORED."""
        mock_requests.post.return_value = mocked_request_post(403)
        email_data = {
            "to_email": "pearsongoulart@gmail.com",
            "to_name": "Alexander",
            "from_email": "pearsongoulart@icloud.com",
            "from_name": "Alexander",
            "subject": "Testing v2",
            "body": "<h1>Testing</h1><p>Hello</p>",
        }
        resp = utils.send_to_sendgrid(email_data)
        self.assertEqual(resp["status_code"], 403)
        self.assertEqual(resp["message"], "Hello world")
        self.assertEqual(resp["type"], "SENDGRID")
