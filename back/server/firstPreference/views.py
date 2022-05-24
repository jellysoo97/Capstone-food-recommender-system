from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.parsers import JSONParser
from django.core import serializers

from .serializers import RecipeSerializer, PreferenceSerializer
from .models import Recipe, Preference

# GET으로 레시피 데이터 불러오기 , POST로 선호정보 저장하기


@csrf_exempt
def check_preference(request):
    obj = Recipe.objects.all().order_by('id')[:10]
    if request.method == 'GET':
        serializer = PreferenceSerializer(obj, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PreferenceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
