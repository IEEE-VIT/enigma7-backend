from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction

from .serializers import (
    QuestionSerializer,
    HintSerializer, LeaderBoardSerializers, StoryLevelSerializer
)
from .models import Question
from users.models import User
from .logging import logging
from .helpers import (
    calculate_points, is_close_answer, is_correct_answer,
    is_valid_answer, return_decoded_list
)

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_celery_beat.models import IntervalSchedule, PeriodicTask

import re
from datetime import datetime
import json
import os


CORRECT_POINTS = 10
HINT_COST = 5

HINT_XP = 50
SKIP_XP = 100
ACCEPT_CLOSE_XP = 75


class Questionview(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'order'

    def get_object(self, *args, **kwargs):
        user = self.request.user
        q_get = get_object_or_404(Question, order=user.question_id)
        return q_get


class Answerview(APIView):

    '''
    Post request of form {"answer" : string}
    '''

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @transaction.atomic
    def post(self, *args, **kwargs):
        user = self.request.user
        # get the question id in which current user is on
        ques_id = user.question_id
        user_answer = args[0].data['answer']
        question = get_object_or_404(Question, order=int(ques_id))
        time = timezone.localtime(timezone.now())
        if user.no_of_attempts == 0:
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=2, period=IntervalSchedule.MINUTES
            )
            PeriodicTask.objects.create(
                interval=schedule, name=f"XP Gen for user {user.id}",
                task='game.tasks.increase_user_xp',
                kwargs=json.dumps({'user_id': user.id})
            )
        user.no_of_attempts += 1

        if user.user_status.first_timestamp is None:
            user.user_status.first_timestamp = time

        if is_valid_answer(user_answer):
            if is_correct_answer(question, user_answer):
                question_solves = question.solves

                user.points += calculate_points(question_solves, user.user_status.hint_used)

                question_solves += 1  # number of solves for the question
                question.save()

                user.question_answered += 1

                user.user_status.hint_used = False
                user.question_id += 1
                user.user_status.hint_powerup = False
                user.user_status.skip_powerup = False
                user.user_status.accept_close_answer = False
                user.user_status.last_answered_ts = time

                user.save()
                logging(user)
                return Response(
                    {'answer': True, 'close_answer': False},
                    status=200
                )

            elif is_close_answer(question, user_answer):
                user.save()
                logging(user)
                resp = {'answer': False, 'close_answer': True,
                        'detail': "You are close to the answer !"}
                return Response(resp, status=200)

            else:
                user.save()
                resp = {'answer': False, 'close_answer': False,
                        'detail': "Keep Trying !"}  # need better wordings here
                logging(user)
                return Response(resp, status=200)
        else:
            user.save()
            resp = {"detail": "Special characters are not allowed"}
            return Response(resp, status=400)

    def _isAnswer(self, question, answer):
        decoded_answers = return_decoded_list(question.answer)
        if answer.lower() in map(lambda x: x.lower(), decoded_answers):
            return True
        return False

    def _isCloseAnswer(self, question, answer):
        decoded_answers = return_decoded_list(question.close_answers)
        if answer.lower() in map(lambda x: x.lower(), decoded_answers):
            return True
        return False

    def _isValid(self, user_response):
        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if string_check.search(user_response) is None:
            return True
        return False


class Hintview(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        if request.user.user_status.hint_powerup:
            response = dict(HintSerializer(get_object_or_404(
                Question, order=request.user.question_id)).data)
            response.update({"detail": "You are already on a hint powerup ."})
            return Response(response)
        else:
            if not request.user.user_status.hint_used:
                request.user.no_of_hints_used += 1

            request.user.user_status.hint_used = True
            request.user.save()
            serializer = HintSerializer(get_object_or_404(
                Question, order=request.user.question_id))
            logging(request.user)
            return Response(serializer.data)


class PowerupHintView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        if request.user.user_status.hint_used or request.user.user_status.hint_powerup:
            serializer = HintSerializer(get_object_or_404(
                Question, order=request.user.question_id))
            response = dict(serializer.data)
            response.update({'detail': 'You have already taken a hint .'})
            return Response(response)

        else:
            if request.user.xp >= HINT_XP:  # Hint xp

                serializer = HintSerializer(get_object_or_404(
                    Question, order=request.user.question_id))
                request.user.xp -= HINT_XP
                request.user.user_status.hint_powerup = True

                request.user.save()

                response = dict(serializer.data)
                response.update({
                    'status': request.user.user_status.hint_powerup,
                    'xp': request.user.xp}
                )
                logging(request.user)
                return Response(response, status=200)
            else:
                resp = {"detail": "Insufficient Xp",
                        'status': request.user.user_status.hint_powerup}
                logging(request.user)
                return Response(resp, status=200)


class PowerupSkipView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):

        if request.user.xp >= SKIP_XP:

            request.user.question_id += 1
            request.user.xp -= SKIP_XP

            request.user.user_status.hint_used = False
            request.user.user_status.hint_powerup = False
            request.user.user_status.skip_powerup = False
            request.user.user_status.accept_close_answer = False

            request.user.save()
            logging(request.user)
            resp = {'question_id': request.user.question_id,
                    'status': request.user.user_status.skip_powerup,
                    'xp': request.user.xp}
            return Response(resp, status=200)
        else:
            resp = {"detail": "Insufficient Xp",
                    "status": request.user.user_status.skip_powerup}
            logging(request.user)
            return Response(resp, status=200)


class PowerupCloseAnswerView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @transaction.atomic
    def post(self, *args, **kwargs):
        user = self.request.user
        if user.xp >= ACCEPT_CLOSE_XP:

            user.user_status.accept_close_answer = True

            ques_id = user.question_id
            user_answer = args[0].data['answer']
            question = get_object_or_404(Question, order=int(ques_id))

            if is_correct_answer(question, user_answer) or is_close_answer(question, user_answer):

                question_solves = question.solves

                user.points += calculate_points(question_solves, user.user_status.hint_used)

                question_solves += 1  # number of solves for the question
                question.save()

                user.question_answered += 1
                user.question_id += 1
                user.question_answered += 1
                user.xp -= ACCEPT_CLOSE_XP

                user.user_status.hint_used = False
                user.user_status.hint_powerup = False
                user.user_status.skip_powerup = False
                user.user_status.accept_close_answer = False
                user.user_status.last_answered_ts = datetime.now()

                user.save()
                resp = {'question_id': user.question_id,
                        'xp': user.xp,
                        'status': user.user_status.accept_close_answer,
                        'answer': True}
                logging(user)
                return Response(resp, status=200)
            else:
                response = {'close_answer': False,
                            'detail': "The answer isn't a close answer"}
                logging(user)
                return Response(response, status=200)

        else:
            resp = {"detail": "Insufficient Xp",
                    "status": user.user_status.accept_close_answer}
            logging(user)
            return Response(resp, status=200)

    def _isCloseAnswer(self, question, answer):
        decoded_list = return_decoded_list(question.close_answers)
        if answer.lower() in map(lambda x: x.lower(), decoded_list):
            return True
        return False

    def _isAnswer(self, question, answer):
        decoded_answers = return_decoded_list(question.answer)
        if answer.lower() in map(lambda x: x.lower(), decoded_answers):
            return True
        return False

    def _isValid(self, user_response):
        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if string_check.search(user_response) is None:
            return True
        return False


class LeaderBoardView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = LeaderBoardSerializers

    def get_queryset(self):
        users = User.objects.order_by(
            '-points', 'user_status__last_answered_ts')[:25]
        return users


class XpTimeGeneration(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        resp = {}
        if request.user.user_status.first_timestamp:
            elapsed_time = (
                timezone.localtime(timezone.now()) - request.user.user_status.first_timestamp
            ).total_seconds()
            next_time = elapsed_time + (3600 - (elapsed_time % 3600))
            resp['time_left'] = next_time - elapsed_time
        else:
            resp['time_left'] = None
        return Response(resp)


class IndividualLevelStoryView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = StoryLevelSerializer
    lookup_field = 'order'

    def get_object(self):
        user = self.request.user
        story_get = get_object_or_404(Question, order=user.question_id)
        return story_get


class CompleteLevelStoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Question.objects.all()
    serializer_class = StoryLevelSerializer
    lookup_field = 'order'

    def get_queryset(self):
        user = self.request.user
        story_get = Question.objects.filter(order__range=(1, user.question_id))
        return story_get


class EnigmaStatusView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        date = datetime.strptime(os.environ['START_DATE'], '%d-%m-%Y').date()
        time = datetime.strptime(os.environ['START_TIME'], '%H:%M').time()
        started_bool = bool(int(os.environ['ENIGMA_STARTED']))
        resp = {'has_started': started_bool,
                'start_date': date, 'start_time': time}
        return Response(resp)
