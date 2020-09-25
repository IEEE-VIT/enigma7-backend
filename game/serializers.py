from rest_framework import serializers
from .models import Question
from users.models import User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "img_url",
            "text",
        )


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            "hint",
        )

class LeaderBoardSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "points",
            "question_answered",
        )