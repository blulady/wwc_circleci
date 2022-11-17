from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from api.serializers.CompleteMemberInfoSerializer import CompleteMemberInfoSerializer
from api.serializers.NonSensitiveMemberInfoSerializer import NonSensitiveMemberInfoSerializer
from api.helper_functions import is_director_or_superuser
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import date, datetime, timedelta
import logging

from ..models import UserProfile, Role


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
    -------------------------------------------------------------
    Search by any number of characters in first_name or last_name, like so:
    http//example.com/api/users/?search=first_name
    http//example.com/api/users/?search=last_name
    Returns a list of members.
    ---------------------------------------------------------------
    You may also filter results based on user status, creation date, role and team, like so:
    http//example.com/api/users/?role=VOLUNTEER&status=ACTIVE
    http//example.com/api/users/?status=ACTIVE&created_at=3months
    http//example.com/api/users/?role=VOLUNTEER&team=4
    http//example.com/api/users/?status=ACTIVE&status=PENDING&role=LEADER&role=DIRECTOR
    Returns a list of members.

    """
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['first_name', 'last_name', 'date_joined']
    ordering = ['-date_joined']
    search_fields = ['^first_name', '^last_name']

    item = openapi.Items(type=openapi.TYPE_STRING)
    status_param = openapi.Parameter('status', openapi.IN_QUERY, description="Filter on status", type=openapi.TYPE_ARRAY, collectionFormat='multi', items=item)
    role_param = openapi.Parameter('role', openapi.IN_QUERY, description="Filter on role", type=openapi.TYPE_ARRAY, collectionFormat='multi', items=item)
    created_at_param = openapi.Parameter('created_at', openapi.IN_QUERY, description="Filter on date joined", type=openapi.TYPE_STRING)
    team_param = openapi.Parameter('team', openapi.IN_QUERY, description="Filter on team", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[status_param, role_param, created_at_param, team_param])
    def get(self, request):
        # This get method needs to be written purely to add the swagger_auto_schema decorator
        # So that we can display and accept the query params from swagger UI
        self.is_user_director_or_superuser = is_director_or_superuser(request.user.id, request.user.is_superuser)
        queryset = self.get_queryset()
        filter_query_set = self.filter_queryset(queryset)
        serializer = self.get_serializer_class()(filter_query_set, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = User.objects.all()
        # get the ordering fields for the queryset
        order_fields = OrderingFilter().get_ordering(self.request, queryset, self)
        # remove the prefix '-' for distinct clause
        distinct_fields = [field.strip('-') for field in order_fields]
        order_fields.append('id')
        distinct_fields.append('id')
        # add distinct clause on user id to eliminate duplicate rows from the query results.
        # DISTINCT ON expression matches the ORDER BY clause
        queryset = User.objects.order_by(*order_fields).distinct(*distinct_fields).exclude(userprofile__status="PENDING")

        status_filter = set(self.request.query_params.getlist('status'))
        if status_filter and status_filter.issubset(UserProfile.ALL_STATUS_VALUES):
            queryset = queryset.filter(userprofile__status__in=status_filter)

        date_filter = self.request.query_params.get('created_at')
        todays_date = datetime.today().astimezone()
        time_joined = {'3months': todays_date - timedelta(weeks=12),
                       '6months': todays_date - timedelta(weeks=24),
                       'current_year': date(todays_date.year, 1, 1)}
        if date_filter and (date_filter in time_joined):
            queryset = queryset.filter(date_joined__gte=time_joined[date_filter])

        role_filter = set(self.request.query_params.getlist('role'))
        team_filter = self.request.query_params.get('team')
        role_team_filter = {}
        if role_filter and role_filter.issubset(Role.VALID_ROLES):
            role_team_filter['user_team__role__name__in'] = role_filter
        if team_filter and team_filter.isnumeric():
            role_team_filter['user_team__team__id'] = team_filter
        if role_team_filter:
            queryset = queryset.filter(**role_team_filter)
        return queryset

    def get_serializer_class(self):
        if self.is_user_director_or_superuser:
            return CompleteMemberInfoSerializer
        return NonSensitiveMemberInfoSerializer


class GetMemberInfoView(RetrieveAPIView):
    """
    Takes the user id as a parameter and gives back the information about the member.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        try:
            if is_director_or_superuser(self.request.user.id, self.request.user.is_superuser):
                return CompleteMemberInfoSerializer
            else:
                return NonSensitiveMemberInfoSerializer
        except AttributeError:
            return "Attribute Exception: user id not found"


class GetMemberProfileView(RetrieveAPIView):
    """
    Get current logged in user's id. If valid, display profile information for that user. Return an error
    message if there is no id match in the DB
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CompleteMemberInfoSerializer
    queryset = None
    lookup_field = 'id'

    def get_serializer_class(self):
        try:
            return CompleteMemberInfoSerializer
        except Exception:
            current_user = self.request.user
            return ("Exception: ", current_user, "not found.")

    def retrieve(self, request):
        current_user = self.request.user
        curr_id = current_user.id
        instance = User.objects.get(pk=curr_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
