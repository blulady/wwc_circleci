from rest_framework import serializers
from django.contrib.auth.models import User


class NameChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

# TODO create a separate validator like password_validator. Use that here and in UserRegistrationSerializer
    def validate(self, data):
        min = 1
        max = 50
        new_fn = data.get('first_name')
        new_ln = data.get('last_name')
        fn_len = len(new_fn)
        ln_len = len(new_ln)
        if not data:
            raise serializers.ValidationError("Name cannot be empty")
        if min > fn_len or fn_len > max:
            raise serializers.ValidationError("Length of firstname not in range of 1 to 50 characters")
        if min > ln_len or ln_len > max:
            raise serializers.ValidationError("Length of lastname not in range of 1 to 50 characters")
        return data
