
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "question_answered",
            "points",
            "rank",
            "question_answered",
        )

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'id', 
            'username'
        )
        
        