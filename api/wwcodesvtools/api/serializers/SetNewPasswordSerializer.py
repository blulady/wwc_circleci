from rest_framework import serializers
from ..validators.password_validator import validate_password


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    email = serializers.EmailField(max_length=150, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'email', 'token']
