from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from .serializers import QuestionSerializer , HintSerializer , LeaderBoardSerializers
from .models import Question
from users.models import User

from rest_framework import generics , mixins
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated , AllowAny
from rest_framework.response import Response

import json
import re
from datetime import datetime

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
    lookup_field = 'id'

    def get_object(self , *args , **kwargs):    
        kwargs = self.kwargs
        q_get = get_object_or_404(Question,id = self.request.user.question_id)
        return q_get



class Answerview(APIView):

    '''

    Post request of form {"answer" : string}

    '''
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self , *args , **kwargs):

        ques_id = self.request.user.question_id  # get the question id in which current user is on 
        user_answer = args[0].data['answer']
        question = get_object_or_404(Question , id = int(ques_id))
        self.request.user.no_of_attempts += 1

        if self.request.user.user_status.first_timestamp == None:
            self.request.user.user_status.first_timestamp = timezone.now()

        if self._isValid(user_answer):
            if self._isAnswer(question , user_answer):

                if self.request.user.user_status.hint_used == False:   # hint is not taken
                    self.request.user.points += CORRECT_POINTS
                else:
                    self.request.user.points += CORRECT_POINTS-HINT_COST

                self.request.user.question_answered += 1

                self.request.user.user_status.hint_used = False
                self.request.user.question_id += 1
                self.request.user.user_status.hint_powerup = False
                self.request.user.user_status.skip_powerup = False
                self.request.user.user_status.accept_close_answer = False
                self.request.user.user_status.last_answered_ts = datetime.now()

                self.request.user.save()

                return Response({'answer' : True,'close_answer' : False} , status=200)

            elif self._isCloseAnswer(question , user_answer):
                return Response({'answer' : False , 'close_answer' : True , 'detail' : "You are close to the answer !"} , status=200) # need better wordings here 

            else:
                resp = {'answer' : False , 'close_answer' : False , 'detail' : "Keep Trying !"} # need better wordings here 
                return Response(resp , status=200)
        else:
            resp = {"detail" : "Special characters are not allowed"}
            return Response(resp , status=400)

    def _isAnswer(self , question , answer):
        if answer.lower() in map(lambda x : x.lower() ,question.answer):
            return True
        return False

    def _isCloseAnswer(self,question,answer):
        if answer.lower() in map(lambda x : x.lower() ,question.close_answers):
            return True
        return False

    def _isValid(self , user_response): 
        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if string_check.search(user_response) == None: 
            return True
        return False


class Hintview(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self , request , *args , **kwargs):
        
        if not request.user.user_status.hint_used:
            request.user.no_of_hints_used += 1

        request.user.user_status.hint_used = True
        request.user.save()
        serializer = HintSerializer(get_object_or_404(Question , id = request.user.question_id))
        return Response(serializer.data)


class PowerupHintView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self , request , *args , **kwargs):

        if request.user.user_status.hint_used or request.user.user_status.hint_powerup:
            return Response({'detail' : 'You have already taken a hint .'})

        else:
            if request.user.xp >= HINT_XP: # Hint xp

                serializer = HintSerializer(get_object_or_404(Question , id = request.user.question_id))
                request.user.xp -= HINT_XP
                request.user.user_status.hint_powerup = True

                request.user.save()

                response = dict(serializer.data)
                response.update({'status' : request.user.user_status.hint_powerup  , 'xp' : request.user.xp , 'status' : request.user.user_status.hint_powerup})

                return Response(response , status=200)
            else:
                resp = {"detail" : "Insufficient Xp" , 'status' : request.user.user_status.hint_powerup}
                return Response(resp , status=200)


class PowerupSkipView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request , *args , **kwargs):

        if request.user.xp >= SKIP_XP:

            request.user.question_id += 1
            request.user.xp -= SKIP_XP

            request.user.user_status.hint_used = False
            request.user.user_status.hint_powerup = False
            request.user.user_status.skip_powerup = False
            request.user.user_status.accept_close_answer = False

            request.user.save()
            return Response({'question_id' : request.user.question_id , 'status' : request.user.user_status.skip_powerup , 'xp' : request.user.xp} , status=200)
        else:
            resp = {"detail" : "Insufficient Xp" , "status" : request.user.user_status.skip_powerup}
            return Response(resp , status=200)


class PowerupCloseAnswerView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, *args , **kwargs):

        if self.request.user.xp >= ACCEPT_CLOSE_XP:

            self.request.user.user_status.accept_close_answer = True
            
            ques_id = self.request.user.question_id 
            user_answer = args[0].data['answer']
            question = get_object_or_404(Question , id = int(ques_id))

            if self._isCloseAnswer(question , user_answer) or self._isAnswer(question , user_answer):
                
                if self.request.user.user_status.hint_used: # If user takes up both ( Close answer powerup and hint )
                    self.request.user.points += CORRECT_POINTS-HINT_COST
                    self.request.user.user_status.hint_used = False        
                else:
                    self.request.user.points += CORRECT_POINTS
            else:
                response = {'close_answer' : False , 'detail' : "The answer isn't a close answer"}
                return Response(response , status=200)
                
            self.request.user.question_id += 1
            self.request.user.question_answered += 1
            self.request.user.xp -= ACCEPT_CLOSE_XP

            self.request.user.user_status.hint_used = False
            self.request.user.user_status.hint_powerup = False
            self.request.user.user_status.skip_powerup = False
            self.request.user.user_status.accept_close_answer = False
            self.request.user.user_status.last_answered_ts = datetime.now()



            self.request.user.save()

            return Response({'question_id' : self.request.user.question_id , 'xp' : self.request.user.xp , 'status' : self.request.user.user_status.accept_close_answer} , status=200)
        else:
            resp = {"detail" : "Insufficient Xp" , "status" : self.request.user.user_status.accept_close_answer}
            return Response(resp , status=200)

    def _isCloseAnswer(self,question,answer):
        if answer.lower() in map(lambda x : x.lower() ,question.close_answers):
            return True
        return False

    def _isAnswer(self , question , answer):
        if answer.lower() in map(lambda x : x.lower() ,question.answer):
            return True
        return False

    def _isValid(self , user_response): 
        string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if string_check.search(user_response) == None: 
            return True
        return False

class LeaderBoardView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer_class = LeaderBoardSerializers

    def get_queryset(self):
        users = User.objects.order_by('-points' , 'user_status__last_answered_ts')[:25]
        return users


class XpTimeGeneration(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self , request , *args , **kwargs):
        resp = {}
        elapsed_time = (timezone.now() - request.user.user_status.first_timestamp).total_seconds()
        next_time = elapsed_time + (3600 - (elapsed_time % 3600))
        resp['time_left'] = next_time - elapsed_time
        return Response(resp)
