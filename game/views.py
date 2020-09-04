from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .serializers import QuestionSerializer , HintSerializer
from .models import Question 

from rest_framework import generics , mixins
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated , AllowAny
from rest_framework.response import Response

import json


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
    
        if self._isAnswer(question , user_answer):

            if self.request.user.userstatus.hint_used == False:   # hint is not taken
                self.request.user.points += CORRECT_POINTS
            else:
                self.request.user.points += CORRECT_POINTS-HINT_COST

            self.request.user.userstatus.hint_used = False
            self.request.user.question_answered += 1
            self.request.user.save()

            return Response({'answer' : True} , status=200)

        elif self._isCloseAnswer(question , user_answer):
            return Response({'answer' : False , 'detail' : "You are close to the answer !"} , status=200) # need better wordings here 

        else:
            resp = {'answer' : False , 'detail' : "Keep Trying !"} # need better wordings here 
            return Response(resp , status=200)

    def _isAnswer(self , question , answer):
        if answer.lower() in map(lambda x : x.lower() ,question.answer):
            return True
        return False

    def _isCloseAnswer(self,question,answer):
        if answer.lower() in map(lambda x : x.lower() ,question.close_answers):
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
