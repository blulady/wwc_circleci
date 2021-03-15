from rest_framework import serializers
from api.models import UserProfile


class EditMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('status', 'role')

    def validate_role(self, value):
        valid_roles = [UserProfile.DIRECTOR, UserProfile.LEADER, UserProfile.VOLUNTEER]
        if value not in valid_roles:
            raise serializers.ValidationError("Invalid Role: accepted values are 'VOLUNTEER','LEADER','DIRECTOR'")
        return value

    def validate_status(self, value):
        valid_status = [UserProfile.ACTIVE, UserProfile.INACTIVE]
        if value not in valid_status:
            raise serializers.ValidationError("Invalid Status: accepted values are 'ACTIVE','INACTIVE'")
        return value
