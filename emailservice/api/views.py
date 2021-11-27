from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import EmailMessageSerializer


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
            # TODO: Email service code request goes here
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
