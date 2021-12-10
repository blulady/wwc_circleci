from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers.GetMemberForDirectorSerializer import GetMemberForDirectorSerializer
from api.serializers.GetMemberSerializer import GetMemberSerializer
from api.helper_functions import is_director_or_superuser
from api.permissions import CanGetMemberInfo
from api.models import Role
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import date, datetime, timedelta
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
    Returns a list of members.
    Search by any number of characters in first_name or last_name
    -------------------------------------------------------------
    http//example.com/api/users/?search=first_name
    http//example.com/api/users/?search=last_name
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['first_name', 'last_name', 'date_joined']
    ordering = ['-date_joined']
    search_fields = ['^first_name', '^last_name']

    status_param = openapi.Parameter('status', openapi.IN_QUERY, description="Filter on status", type=openapi.TYPE_STRING)
    role_param = openapi.Parameter('role', openapi.IN_QUERY, description="Filter on role", type=openapi.TYPE_STRING)
    created_at_param = openapi.Parameter('created_at', openapi.IN_QUERY, description="Filter on date joined", type=openapi.TYPE_STRING)



    @swagger_auto_schema(manual_parameters=[status_param, role_param, created_at_param])
    def get(self, request):
        # This get method needs to be written purely to add the swagger_auto_schema decorator
        # So that we can display and accept the query params from swagger UI
        queryset = self.get_queryset()
        filter_query_set = self.filter_queryset(queryset)
        serializer = self.get_serializer_class()(filter_query_set, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        queryset = User.objects.all()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(userprofile__status=status)
        if not is_director_or_superuser(self.request.user.id, self.request.user.is_superuser):
            queryset = User.objects.exclude(userprofile__status="PENDING")
        date_filter = self.request.query_params.get('created_at')
        todays_date = datetime.today().astimezone()
        if date_filter:
            time_joined = {'3months': todays_date - timedelta(weeks=12),
                           '6months': todays_date - timedelta(weeks=24),
                           'current_year': date(todays_date.year, 1, 1)}
            queryset = queryset.filter(date_joined__gte=time_joined[date_filter])
        role_filter = self.request.query_params.get('role')
        if role_filter:
            rfilter = Role.objects.get(name=role_filter)
            queryset = queryset.filter(user_team__role=rfilter.id)
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
