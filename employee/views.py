from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from employee.seralizers import EmployeeSeralizer, LoginSeralizer
from .import models
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

# Create your views hereHttpResponseSessionAuthentication
def poll(request):
    if request.method=='GET':
        question = models.Question.objects.all()
        seralizer= EmployeeSeralizer(question, many=True)
        return JsonResponse(seralizer.data, safe=False)
    
    elif request.method=='POST':
        json_parser = JSONParser()
        data = json_parser.parse(request)
        seralizer = EmployeeSeralizer(data=data)
        if seralizer.is_valid():
            seralizer.save()
            return JsonResponse(seralizer.data, status=200)
        return JsonResponse(seralizer.errors, status=400)

@csrf_exempt
def detail(request, id):
    try:
        instance= models.Question.objects.get(id=id)
    except models.Question.DoesNotExist as error:
        return JsonResponse({'error':'object not found'}, status=400)
    if request.method=='GET':
        question = models.Question.objects.all()
        seralizer= EmployeeSeralizer(question, many=True)
        return JsonResponse(seralizer.data, safe=False)
    
    elif request.method=='PUT':
        json_parser = JSONParser()
        data = json_parser.parse(request)
        seralizer = EmployeeSeralizer(instance, data=data)
        if seralizer.is_valid():
            seralizer.save()
            return JsonResponse(seralizer.data, status=200)
        return JsonResponse(seralizer.errors, status=400)
    
    elif request.method=='DELETE':
        instance.delete()
        return HttpResponse(status=204)


class PollApiView(APIView):
    authentication_classes=[SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        question=models.Question.objects.all()
        seralizer = EmployeeSeralizer(question, many=True)
        return Response(seralizer.data)

    def post(self, request):
        data=request.data
        seralizer=EmployeeSeralizer(data=data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data, status=200)
        return Response(seralizer.errors, status=400)

class PollApiDetail(APIView):

    authentication_classes=[SessionAuthentication, BasicAuthentication]
    permission_classes = IsAuthenticated

    def get_object(self, id):
        try:
            return models.Question.objects.get(id=id)
        except models.Question.DoesNotExist as e:
            return Response({'error':'given object not found'}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        seralizer = EmployeeSeralizer(instance)
        return Response(seralizer.data)

    def put(self, request, id):
        data = request.data
        instance = self.get_object(id)
        seralizer = EmployeeSeralizer(instance, data=data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data, status=200)
        return Response(seralizer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return Response(status=204)

from rest_framework.authtoken.models import Token

class LoginView(APIView):
    def post(self, request):
        seralizer=LoginSeralizer(data=request.data)
        seralizer.is_valid(raise_exception=True)
        user = seralizer.validate["user"]
        django_login(request, user)
        token, created= Token.objects.get_or_create(user=user)
        return Response({"token": Token.key}, status=200)
         
