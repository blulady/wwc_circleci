from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from ..validators.FirstAndLastNameValidator import validate_first_name, validate_last_name
import re


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False, validators=[validate_first_name])
    last_name = serializers.CharField(write_only=True, validators=[validate_last_name])

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

# TODO Use the password_validator
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
