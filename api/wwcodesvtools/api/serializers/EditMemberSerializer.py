import re
from rest_framework import serializers
from api.models import UserProfile


class EditMemberSerializer(serializers.ModelSerializer):
    #status = serializers.SerializerMethodField('validate_old_status')
    class Meta:
        model = UserProfile
        fields = ('status', 'role')

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance

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

    # def validate_old_status(self, attrs):
    #     user_status = attrs.get('status')
    #     valid_status = [UserProfile.ACTIVE, UserProfile.INACTIVE]
    #     if user_status not in valid_status:
    #         raise serializers.ValidationError({'error':"Invalid Status: accepted values are 'ACTIVE','INACTIVE'. Can not edit user with 'PENDING' status"})
    #     return user_status