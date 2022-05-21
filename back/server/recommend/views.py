from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.parsers import JSONParser
from django.core import serializers

from .serializers import IngreSerializer
from .models import Ingre

# Create your views here.

def ingre_list(request, pk):
  obj = Ingre.objects.filter(ingre_group_small__contains=pk)
  print(obj)
  if request.method == "GET":
    serializer = serializers.serialize("json", obj)
    return HttpResponse(serializer, content_type="text/json-comment-filtered")
    # serializer = IngreSerializer(obj)
    # return JsonResponse(serializer.data, safe=False)