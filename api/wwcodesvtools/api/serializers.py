from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import RegistrationToken, UserProfile
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
        if len(value) > 50:
            raise serializers.ValidationError("First name should not be more than 50 characters long")
        return value

    def validate_last_name(self, value):
        """
        Check that the last_name is not None or empty.
        """
        if not value:
            raise serializers.ValidationError("Last name should not be empty or None")
        if len(value) > 50:
            raise serializers.ValidationError("Last name should not be more than 50 characters long")
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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('status', 'role')

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class RegistrationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationToken
        fields = ('token', 'used')

    def update(self, instance, validated_data):
        instance.used = validated_data.get('used', instance.used)
        instance.token = validated_data.get('token', instance.token)
        instance.save()
        return instance


class AddMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.CharField(max_length=20)
    message = serializers.CharField(max_length=2000, allow_blank=True)

    def validate_role(self, value):
        valid_roles = [UserProfile.DIRECTOR, UserProfile.LEADER, UserProfile.VOLUNTEER]
        if value not in valid_roles:
            raise serializers.ValidationError("Invalid Role: accepted values are 'VOLUNTEER','LEADER','DIRECTOR'")
        return value

    def validate_email(self, value):
        # email and username  fields store same value
        # Validate for username field's regex pattern - UnicodeUsernameValidator
        regex = r'^[\w.@+-]+\Z'
        if not re.match(regex, value):
            raise serializers.ValidationError("Enter valid email. This value may contain only letters, numbers, and @/./+/-/_ characters.")
        # Validate for username field's char size 150
        if len(value) > 150:
            raise serializers.ValidationError("Email should be less than 150 characters")
        return value


class GetMemberForDirectorSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta(object):
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'userprofile', 'date_joined']


class GetMemberSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta(object):
        model = User
        fields = ['id', 'first_name', 'last_name', 'userprofile', 'date_joined']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        user_profile = UserProfile.objects.get(user_id=self.user.id)
        if user_profile.status == 'PENDING':
            error_message = "Not an active user, status is pending"
            raise exceptions.AuthenticationFailed(error_message)
        data.update({'id': self.user.id})
        data.update({'email': self.user.email})
        data.update({'first_name': self.user.first_name})
        data.update({'last_name': self.user.last_name})
        data.update({'role': user_profile.role})
        return data


class LogoutSerializer(serializers.Serializer):
    username = serializers.CharField()
