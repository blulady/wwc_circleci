from rest_framework import serializers
from api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('status', 'role')

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance
