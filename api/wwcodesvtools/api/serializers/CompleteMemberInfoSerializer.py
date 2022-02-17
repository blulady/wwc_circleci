from django.contrib.auth.models import User
from api.serializers.NonSensitiveMemberInfoSerializer import NonSensitiveMemberInfoSerializer


class CompleteMemberInfoSerializer(NonSensitiveMemberInfoSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'status', 'highest_role', 'date_joined', 'role_teams']
