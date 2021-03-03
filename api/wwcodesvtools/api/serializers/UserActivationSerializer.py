from rest_framework import serializers


class UserActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    token = serializers.CharField(max_length=150)
