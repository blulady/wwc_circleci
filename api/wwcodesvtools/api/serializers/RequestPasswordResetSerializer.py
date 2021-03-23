from rest_framework import serializers
from django.contrib.auth.models import User


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        user_queryset = User.objects.filter(email=email).exists()
        if not user_queryset:
            raise serializers.ValidationError({'error': 'Email does not exist'})
        return email
