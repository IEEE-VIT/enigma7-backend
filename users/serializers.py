from rest_framework import serializers
from .models import *
import re

class UserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = (
            "hint_used",
            "hint_powerup",
            "skip_powerup",
            "accept_close_answer"
        )


class Userserializer(serializers.ModelSerializer):
    user_status = UserStatusSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "points",
            "question_answered",
            "xp",
            "no_of_hints_used",
            "user_status"
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
