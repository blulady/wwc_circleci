from rest_framework import serializers
from django.contrib.auth.models import User


class GetMemberForDirectorSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')
    role = serializers.SerializerMethodField('get_role')

    class Meta(object):
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'status', 'role', 'date_joined']

    def get_status(self, obj):
        return obj.userprofile.status

    def get_role(self, obj):
        return obj.userprofile.role
