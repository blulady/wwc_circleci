from django.contrib.auth.models import User
import django_filters


class UserProfileFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['userprofile__role','userprofile__status',]

