from rest_framework import serializers


class MailSenderSerializer(serializers.Serializer):
    email = serializers.EmailField()
