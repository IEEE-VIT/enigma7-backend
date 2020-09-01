
from rest_framework import serializers
from .models import *


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
        model = User
        fields = (
            'id', 
            'username'
        )
        
        