from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.parsers import JSONParser
from django.core import serializers

import pandas as pd
import json

# from .serializers import RecipeSerializer, PreferenceSerializer
# from .models import Preference
from recommend.models import RecipeBasic

# GET으로 레시피 데이터 불러오기 , POST로 선호정보 저장하기
# @csrf_exempt
# def check_preference(request):
#     obj = Recipe.objects.all().order_by('id')[:10]
#     if request.method == 'GET':
#         serializer = PreferenceSerializer(obj, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PreferenceSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# signup - 초기 선호도 입력 페이지 get
def getFirstPrefer(request):
    data = RecipeBasic.objects.all().values()
    data_pd = pd.DataFrame(data)
    return_result = {}
    if request.method == "GET":
        menu_list = data_pd.sample(n=10).values.tolist()
        for elem in menu_list:
            return_result[int(elem[0])] = {"recipe_id": int(elem[1]),
            "recipe_nm_ko": elem[2], "img_url": elem[-1]}
        return_result = json.dumps(return_result, ensure_ascii=False)
        return JsonResponse(return_result, safe=False)

# cosine_sim_lst
def getCosine():
    with open("cosine_sim_lst.txt", encoding="utf-8") as txtfile:
        cosine_sim_lst = txtfile.read()
    return cosine_sim_lst