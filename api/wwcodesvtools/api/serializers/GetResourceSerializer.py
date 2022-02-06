from api.models import Resource
from rest_framework import serializers


class CompleteResourceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Resource
        fields = ['edit_link', 'published_link']


class NonSensitiveResourceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Resource
        fields = ['published_link']
