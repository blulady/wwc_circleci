from rest_framework import serializers
import re


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)
    email = serializers.EmailField(max_length=150, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'email', 'token']

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
