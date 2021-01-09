from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from api.serializers import GetMemberForDirectorSerializer, GetMemberSerializer
from api.helper_functions import is_director_or_superuser
from api.permissions import CanGetMemberInfo


class GetMembersView(ListAPIView):
    """
    Returns a list of all members.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if is_director_or_superuser(self.request.user.id, self.request.user.is_superuser):
            queryset = User.objects.all().order_by('-date_joined')
            return queryset
        queryset = User.objects.exclude(userprofile__status='PENDING').order_by('-date_joined')
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
