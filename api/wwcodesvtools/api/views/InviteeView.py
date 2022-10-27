from api.models import Invitee
from api.serializers.InviteeSerializer import InviteeSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.permissions import CanAccessInvitee


class InviteeViewSet(viewsets.ModelViewSet):
    # Exclude the invitees that has been accepted
    queryset = Invitee.objects.exclude(accepted=True)
    serializer_class = InviteeSerializer
    permission_classes = [IsAuthenticated & CanAccessInvitee]
