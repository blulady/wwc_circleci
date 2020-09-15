from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    NEW = 'NEW'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    VOLUNTEER = 'VOLUNTEER'
    LEADER = 'LEADER'
    DIRECTOR = 'DIRECTOR'
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    status =  models.CharField(max_length=20, 
      choices = ((NEW, NEW), (ACTIVE,ACTIVE), (INACTIVE, INACTIVE))
      )
    role = models.CharField(max_length=20, 
      choices = ((VOLUNTEER, VOLUNTEER), (LEADER, LEADER), (DIRECTOR, DIRECTOR)) 
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_new(self):
      return self.status == self.NEW


class RegistrationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    used = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)