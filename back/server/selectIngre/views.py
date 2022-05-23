from dataclasses import fields
from tokenize import group
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from .models import IngreGroup

# Create your views here.

# 재료군 GET
def getIngreGroup(request):
  datas = IngreGroup.objects.all()

  if request.method == "GET":
    groups = serializers.serialize("json", datas, fields="group")
    return HttpResponse(groups, content_type="text/json-comment-filtered")
  

# 재료군별 재료 GET
def getIngreSub(request, id):
  subs = IngreGroup.objects.filter(pk=id)

  if request.method == "GET":
    sub = serializers.serialize("json", subs)
    print(sub)
    return HttpResponse(sub, content_type="text/json-comment-filtered")