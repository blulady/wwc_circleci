from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from api.serializers import GetMemberForDirectorSerializer, GetMemberSerializer
from api.helper_functions import is_director_or_superuser


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
