
from rest_framework import serializers
from .models import *


class User_Serializer(serializers.ModelSerializer):
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

class Username_Serialiser(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'id', 
            'username'
        )