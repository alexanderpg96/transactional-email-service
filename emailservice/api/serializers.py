from rest_framework import serializers


class EmailMessageSerializer(serializers.Serializer):
    """Serializer for EmailMessage model.

    Used for validation of email messages sent to API prior to send to external email service.
    """

    to_email = serializers.EmailField()
    to_name = serializers.CharField(max_length=255)
    from_email = serializers.EmailField()
    from_name = serializers.CharField(max_length=255)
    subject = serializers.CharField(max_length=255)
    body = serializers.CharField()

    class Meta:
        """"""

        pass
