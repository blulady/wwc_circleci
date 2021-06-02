from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from api.serializers.GetMemberForDirectorSerializer import GetMemberForDirectorSerializer
from api.serializers.GetMemberSerializer import GetMemberSerializer
from api.helper_functions import is_director_or_superuser
from api.permissions import CanGetMemberInfo
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date
from dateutil.relativedelta import relativedelta
from .filters import UserProfileFilter
import logging


logger = logging.getLogger('django')


class GetMembersView(ListAPIView):
    """
    Returns a list of all members.
    Ordering by first_name, last_name or date_joined
    ------------------------------------------------
    You may also specify reverse orderings by prefixing the field name with '-', like so:
    http//example.com/api/users/?ordering=first_name
    http//example.com/api/users/?ordering=-first_name

    Filter by Role, Status or Date Joined
    ------------------------------------------------

    You may also filter results based on user role and user status like so:
    http//example.com/api/users/?role=volunteer&status=pending
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['first_name', 'last_name', 'date_joined']
    ordering = ['-date_joined']
    filterset_class = UserProfileFilter

    def get_queryset(self):
        if is_director_or_superuser(self.request.user.id, self.request.user.is_superuser):
            queryset = User.objects.all()
        else:
            queryset = User.objects.exclude(userprofile__status='PENDING')
        return queryset

    def get_serializer_class(self):
        if is_director_or_superuser(self.request.user.id, self.request.user.is_superuser):
            return GetMemberForDirectorSerializer
        return GetMemberSerializer


class GetMemberInfoView(RetrieveAPIView):
    """
    Takes the user id as a parameter and gives back the information about the member.
    """
    permission_classes = [IsAuthenticated & CanGetMemberInfo]
    queryset = User.objects.all()
    serializer_class = GetMemberForDirectorSerializer
    lookup_field = 'id'
