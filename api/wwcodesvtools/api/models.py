from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):
    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    VOLUNTEER = 'VOLUNTEER'
    LEADER = 'LEADER'
    DIRECTOR = 'DIRECTOR'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=((PENDING, PENDING),
                                       (ACTIVE, ACTIVE), (INACTIVE, INACTIVE))
                              )
    role = models.CharField(max_length=20,
                            choices=((VOLUNTEER, VOLUNTEER),
                                     (LEADER, LEADER), (DIRECTOR, DIRECTOR))
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
