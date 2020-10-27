from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
import re


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()
        return instance

    def validate_first_name(self, value):
        """
        Check that the first_name is not None or empty.
        """
        if not value:
            raise serializers.ValidationError("First name should not be empty or None")
        return value

    def validate_last_name(self, value):
        """
        Check that the last_name is not None or empty.
        """
        if not value:
            raise serializers.ValidationError("Last name should not be empty or None")
        return value

    def validate_password(self, value):
        """
        Check that the password is correct:
            8-50 characters.
            At least one upper case letter
            At least one lower case letter
            At least one numeric char
        """
        if not (8 <= len(value) <= 50):
            raise serializers.ValidationError("Password should be 8 to 50 characters long")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password should have at least one upper case letter")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password should have at least one lower case letter")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password should have at least one number")
        return value


class MailSenderSerializer(serializers.Serializer):
    email = serializers.EmailField()
