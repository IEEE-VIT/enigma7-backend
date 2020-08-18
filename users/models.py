from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
 BaseUserManager,AbstractUser,PermissionsMixin
)
from .managers import *

class Users(AbstractUser):
    username=models.CharField(max_length=255,unique=True,null=False)
    email=models.EmailField(max_length=255,unique=True)
    points=models.IntegerField(default=0)
    rank=models.IntegerField(null=True)
    question_answered=models.IntegerField(default=0)    
    hints_used=models.IntegerField(default=0)
    no_of_attempts=models.IntegerField(default=0)
    question_id=models.IntegerField(default=1)
    objects = UserManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']



    def __str__(self):
	    return self.username

