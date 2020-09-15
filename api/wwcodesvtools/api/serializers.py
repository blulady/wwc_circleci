from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile#, RegistrationToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile

# class RegistrationTokenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RegistrationToken