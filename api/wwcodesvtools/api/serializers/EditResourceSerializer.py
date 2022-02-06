from api.models import Resource
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class EditResourceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Resource
        fields = ['edit_link', 'published_link']

    def validate_edit_link(self, value):
        return self.validate_link(value, 'edit_link')

    def validate_published_link(self, value):
        return self.validate_link(value, 'published_link')

    def validate_link(self, value, field_name):
        try:
            validator = URLValidator()
            validator(value)
        except ValidationError:
            raise serializers.ValidationError(f'{field_name} is invalid. Enter a valid url')
        return value
