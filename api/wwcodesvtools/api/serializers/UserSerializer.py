from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        data = super().validate(attrs)
        email = data['email']
        username = data['username']
        if (email is not None and username is not None and email != username):
            raise serializers.ValidationError({"email_username":
                                               "Email and Username should be same"})
        return data

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
