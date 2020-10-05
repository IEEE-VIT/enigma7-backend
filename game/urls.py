from django.urls import path
from .views import (
    Questionview,
    Answerview,
    Hintview,
    PowerupHintView,
    PowerupSkipView,
    PowerupCloseAnswerView,
    LeaderBoardView,
    XpTimeGeneration
)

urlpatterns = [
    path('question/', Questionview.as_view()),
    path('answer/', Answerview.as_view()),
    path('hint/', Hintview.as_view()),
    path('xp-time/', XpTimeGeneration.as_view()),
    path('leaderboard/', LeaderBoardView.as_view()),
    path('powerup/hint/', PowerupHintView.as_view()),
    path('powerup/skip/', PowerupSkipView.as_view()),
    path('powerup/close-answer/', PowerupCloseAnswerView.as_view()),
]
