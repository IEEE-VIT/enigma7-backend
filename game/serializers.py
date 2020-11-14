from rest_framework import serializers
from .models import Question, StoryBlock
from users.models import User


class StoryBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryBlock
        fields = (
            "story_text",
        )


class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = (
            "id",
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

class StoryLevelSerializer(serializers.ModelSerializer):
    question_story = StoryBlockSerializer() 
    class Meta:
        model = Question
        fields = (
            "id",
            "question_story",
        )
