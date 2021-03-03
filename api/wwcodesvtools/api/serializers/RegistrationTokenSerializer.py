from rest_framework import serializers
from api.models import RegistrationToken


class RegistrationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationToken
        fields = ('token', 'used')

    def update(self, instance, validated_data):
        instance.used = validated_data.get('used', instance.used)
        instance.token = validated_data.get('token', instance.token)
        instance.save()
        return instance
