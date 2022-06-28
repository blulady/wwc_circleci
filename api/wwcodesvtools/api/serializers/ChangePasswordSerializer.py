from rest_framework import serializers
from ..validators.password_validator import validate_password


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        fields = ['password']

    def update(self, user_instance, validated_data):
        user_instance.set_password(validated_data['password'])
        user_instance.save()
        return user_instance
