from rest_framework import serializers
from api.models import UserProfile
import re


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
