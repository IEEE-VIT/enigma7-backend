
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "question_answered",
            "points",
            "auth_token",
        )

class Username_change(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'id', 
            'username'
        )