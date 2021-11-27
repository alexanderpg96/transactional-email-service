from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import EmailMessageSerializer
from .utils import send_email


class EmailMessageView(APIView):
    """APIView class for EmailMessage API request."""

    def post(self, request):
        """Send email to configured email service."""
        data = request.data
        # Change to model field names (Python linter was not happy with 'from' as it's a protected keyword)
        data["to_email"] = data.pop("to")
        data["from_email"] = data.pop("from")

        serializer = EmailMessageSerializer(data=data)

        if serializer.is_valid():
            # Initial request with default service
            resp = send_email(serializer.data)
            # Initial service failed, use fallback
            if resp["status_code"] < 200 or resp["status_code"] > 204:
                resp = send_email(serializer.data, override_default=True)

            return Response(
                {"message": resp["message"], "service": resp["type"]},
                status=resp["status_code"],
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
