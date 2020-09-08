
from rest_framework import serializers
from .models import *

import re


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
            "question_answered",
        )

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'username'
        )

    def validate_username(self , response):
        if not self._isValid(response):
            raise serializers.ValidationError("Incorrect string type for field 'username'")
        return response
    
    
    def _isValid(self , user_response): 
        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if string_check.search(user_response) == None: 
            return True
        return False
        