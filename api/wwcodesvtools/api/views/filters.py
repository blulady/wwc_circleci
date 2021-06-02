from django.contrib.auth.models import User
import django_filters
from django_filters import DateTimeFromToRangeFilter
from django_filters import ChoiceFilter
from datetime import date
from dateutil.relativedelta import relativedelta


class UserProfileFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['userprofile__role','userprofile__status', ]