from rest_framework import serializers
from django.contrib.auth.models import User
from ..validators.FirstAndLastNameValidator import validate_first_name, validate_last_name


class NameChangeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, validators=[validate_first_name])
    last_name = serializers.CharField(write_only=True, validators=[validate_last_name])

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
