from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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

        if self._isValid(user_answer):
            if self._isAnswer(question , user_answer):

                if self.request.user.userstatus.hint_used == False:   # hint is not taken
                    self.request.user.points += CORRECT_POINTS
                else:
                    self.request.user.points += CORRECT_POINTS-HINT_COST

                self.request.user.question_answered += 1

                self.request.user.userstatus.hint_used = False
                self.request.userstatus.hint_powerup = False
                self.request.userstatus.skip_powerup = False
                self.request.userstatus.accept_close_answer = False
                self.request.userstatus.last_answered_ts = datetime.now()

                self.request.user.save()

                return Response({'answer' : True} , status=200)

            elif self._isCloseAnswer(question , user_answer):
                return Response({'answer' : False , 'detail' : "You are close to the answer !"} , status=200) # need better wordings here 

            else:
                resp = {'answer' : False , 'detail' : "Keep Trying !"} # need better wordings here 
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
        
        if not request.user.userstatus.hint_used:
            request.user.no_of_hints_used += 1

        request.user.userstatus.hint_used = True
        request.user.save()
        serializer = HintSerializer(get_object_or_404(Question , id = request.user.question_id))
        return Response(serializer.data)


class PowerupHintView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self , request , *args , **kwargs):

        if request.user.userstatus.hint_used or request.user.userstatus.hint_powerup:
            return Response({'detail' : 'You have already taken a hint .'})

        else:
            if request.user.xp >= HINT_XP: # Hint xp

                serializer = HintSerializer(get_object_or_404(Question , id = request.user.question_id))
                request.user.xp -= HINT_XP
                request.user.userstatus.hint_powerup = True

                request.user.save()

                response = dict(serializer.data)
                response.update({'status' : request.user.userstatus.hint_powerup  , 'xp' : request.user.xp , 'status' : request.user.userstatus.hint_powerup})

                return Response(response , status=200)
            else:
                resp = {"detail" : "Insufficient Xp" , 'status' : request.user.userstatus.hint_powerup}
                return Response(resp , status=200)


class PowerupSkipView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request , *args , **kwargs):

        if request.user.xp >= SKIP_XP:

            request.user.question_id += 1
            request.user.xp -= SKIP_XP

            request.user.userstatus.hint_used = False
            request.userstatus.hint_powerup = False
            request.userstatus.skip_powerup = False
            request.userstatus.accept_close_answer = False

            request.user.save()
            return Response({'question_id' : request.user.question_id , 'status' : request.user.userstatus.skip_powerup , 'xp' : request.user.xp} , status=200)
        else:
            resp = {"detail" : "Insufficient Xp" , "status" : request.user.userstatus.skip_powerup}
            return Response(resp , status=200)


class PowerupCloseAnswerView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, *args , **kwargs):

        if self.request.user.xp >= ACCEPT_CLOSE_XP:

            self.request.user.userstatus.accept_close_answer = True
            
            ques_id = self.request.user.question_id 
            user_answer = args[0].data['answer']
            question = get_object_or_404(Question , id = int(ques_id))

            if self._isCloseAnswer(question , user_answer) or self._isAnswer(question , user_answer):
                
                if self.request.user.userstatus.hint_used: # If user takes up both ( Close answer powerup and hint )
                    self.request.user.points += CORRECT_POINTS-HINT_COST
                    self.request.user.userstatus.hint_used = False        
                else:
                    self.request.user.points += CORRECT_POINTS
            else:
                response = {'detail' : "The answer isn't a close answer"}
                return Response(response , status=200)
                
            self.request.user.question_id += 1
            self.request.user.question_answered += 1
            self.request.user.xp -= ACCEPT_CLOSE_XP

            self.request.userstatus.hint_used = False
            self.request.userstatus.hint_powerup = False
            self.request.userstatus.skip_powerup = False
            self.request.userstatus.accept_close_answer = False
            self.request.userstatus.last_answered_ts = datetime.now()



            self.request.user.save()

            return Response({'question_id' : self.request.user.question_id , 'xp' : self.request.user.xp , 'status' : self.request.user.userstatus.accept_close_answer} , status=200)
        else:
            resp = {"detail" : "Insufficient Xp" , "status" : self.request.user.userstatus.accept_close_answer}
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
        users = User.objects.order_by('-points')[:25]
        users_list = self._split(users)
        return users_list

    def _split(self ,array):
        array = list(array)
        for counter in range(0,len(array)):
            if not counter + 1 == len(array): # rule out , index exceed error
                if array[counter].points == array[counter + 1].points: # if same points
                    if array[counter + 1].userstatus.last_answered_ts < array[counter].userstatus.last_answered_ts: # if later object has reached timestamp earlier
                        array[counter + 1] , array[counter] = array[counter] , array[counter + 1] # swapping

        return array