from django.contrib import admin
from .models import Question, StoryBlock


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['order', 'text', 'solves']
    ordering = (('order'), )


@admin.register(StoryBlock)
class StorAdmin(admin.ModelAdmin):
    list_display = ['story_id', 'story_text']
    ordering = (('story_id'), )
