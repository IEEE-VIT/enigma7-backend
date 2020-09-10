from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
 BaseUserManager,AbstractUser,PermissionsMixin
)
from .managers import *


class User(AbstractUser):
    username=models.CharField(max_length=255, null= False)
    email=models.EmailField(max_length=255,unique=True)
    points=models.IntegerField(default=0)
    rank=models.IntegerField(null=True)
    question_answered=models.IntegerField(default=0)    
    no_of_hints_used=models.IntegerField(default=0)
    no_of_attempts=models.IntegerField(default=0)
    question_id=models.IntegerField(default=1)
    xp = models.IntegerField(default = 0 , null = False , blank = False)
    first_attempt = models.DateTimeField(null = True)
    objects = UserManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



    def __str__(self):
	    return self.email


class UserStatus(models.Model):

    user = models.OneToOneField(User , on_delete=models.CASCADE)
    hint_used = models.BooleanField(default=False)
    hint_powerup = models.BooleanField(default=False)
    skip_powerup = models.BooleanField(default=False)
    accept_close_answer = models.BooleanField(default=False)


    def __str__(self):
	    return self.user.username
    

