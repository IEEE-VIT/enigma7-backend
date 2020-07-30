from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
 AbstractBaseUser
)

class Users(AbstractBaseUser):
    username=models.CharField(max_length=255,unique=True,null=False)
    email=models.EmailField(max_length=255,unique=True)
    points=models.IntegerField(default=0)
    rank=models.IntegerField()
    question_answered=models.IntegerField(default=0)    
    hints_used=models.IntegerField(default=0)
    no_of_attempts=models.IntegerField(default=0)
    question_id=models.IntegerField()
    
    def __str__(self):
	    return self.username 

