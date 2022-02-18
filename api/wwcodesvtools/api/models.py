from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):
    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    REGISTERED_USER_VALID_STATUSES = [ACTIVE, INACTIVE]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=((PENDING, PENDING),
                                       (ACTIVE, ACTIVE), (INACTIVE, INACTIVE))
                              )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_pending(self):
        return self.status == self.PENDING

    def activate(self):
        self.status = self.ACTIVE


class RegistrationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150, default='#deftoken#')
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_used(self):
        self.used = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        RegistrationToken.objects.create(user=instance)


class Team(models.Model):
    name = models.CharField(max_length=150)
    members = models.ManyToManyField(User, through='User_Team')

    def __str__(self):
        return self.name


class Role(models.Model):
    VOLUNTEER = 'VOLUNTEER'
    LEADER = 'LEADER'
    DIRECTOR = 'DIRECTOR'
    VALID_ROLES = [VOLUNTEER, LEADER, DIRECTOR]

    name = models.CharField(max_length=20)
    users = models.ManyToManyField(User, through='User_Team')

    def __str__(self):
        return self.name


class User_Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'team_id', 'role_id'], name='unique user_team')
        ]

    def highest_role(user_id):
        return User_Team.objects.filter(user=user_id).order_by('-role_id').values('role__name')[0]['role__name']


class Resource(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False, unique=True)
    edit_link = models.CharField(max_length=255, null=False, blank=False)
    published_link = models.CharField(max_length=255, null=False, blank=False)
