from rest_framework import serializers
from .models import Question


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