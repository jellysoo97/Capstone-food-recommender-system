from dataclasses import fields
from tokenize import group
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from .models import IngreGroup
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.parsers import JSONParser
from django.core import serializers
import pandas as pd
from recommend.serializers import IngreSerializer
from recommend.models import Ingre
from account.models import User
from firstPreference.models import Recipe
from firstPreference.serializers import RecipeSerializer
import simplejson as json

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


def ingre_combi(request, pk):
    # 필요한 데이터
    df_best_comb_2 = pd.read_csv('재료별최적의궁합2_new.csv')
    df_lsts = pd.read_csv('재료리스트정리.csv')
    df_veges = pd.read_csv('채식주의자종류.csv')

    # 유저 아이디로 정보 가져오기
    # 리스트가 텍스트로 오므로 이것을 다시 리스트화 하기
    obj = User.objects.get(id=pk)
    vege_kinds_raw = obj.vegtype
    inedible_groups_raw = obj.allergic
    jsonDec = json.decoder.JSONDecoder()
    vege_kinds = jsonDec.decode(vege_kinds_raw)
    inedible_groups = jsonDec.decode(inedible_groups_raw)

    #
    if request.method == 'POST':
        # 재료들 리스트가 이리로 넘어옴{ingres:[1,2,3,4,...]}
        data = JSONParser().parse(request)
        # 재료 리스트를 꺼내주기
        main = data[0]
    # 알레르기환자: 못먹는 재료가 바로 리스트(inedible_groups)로 들어옴(알레르기 없으면 빈리스트)
    # 채식주의자: 채식주의자의 종류가 리스트로 들어옴(vege_kinds) -> 종류를 받아서 채식주의자별 못먹는 재료 리스트(vege) 생성
    # 채식주의자 아니면 vege_kinds가 빈리스트 -> vege 생성하지 않음
        if vege_kinds:
            for k in vege_kinds:
                vege_idx = list(df_veges[df_veges['VEGE_KINDS'] == k].index)[0]
                vege = df_veges.loc[vege_idx, 'VEGE_INDBL'].split(',')
                # 채식주의자 종류별 못먹는 재료를 못먹는 재료 리스트(indedible_groups)에 추가
                inedible_groups.extend(vege)

        # 못먹는 재료 리스트(inedible_groups)와 대체식품 재료 리스트(alters)를 비교
        # 대체도 안되고 최종적으로 제외해야 하는 재료 리스트(indedible) = 대체식품 리스트에 들어있지 않은(대체 안되는) 못먹는 재료 리스트
        #inedible = set(inedible_groups) - set(alters)

        result = []
        for c in df_best_comb_2['best_combination']:
            combi = c.replace(' ', '').replace(
                '[', '').replace(']', '').replace("'", "").split(',')
            # 입력된 재료(변수명: main, 형식: 리스트, '식품군별 상세분류'데이터의 ['SUBGROUP'] 원소) 각각 재료별 최적의 궁합 찾기
            if len(set(main) & set(combi)) != 0:
                for i in df_lsts.index:
                    lst_s = df_lsts.loc[i, 'SUBGROUP'].replace(' ', '').replace(
                        '[', '').replace(']', '').replace("'", "").split(',')
                    # 최종적으로 제외해야 하는 재료를 제외하고 최적의 궁합에 있는 모든 재료는 포함하는 레시피 번호
                    # 결과 레시피 번호(변수명: result, 내용: 레시피 번호, 형식:리스트)는 다음 인자로 넘겨줌
                    if (len(inedible_groups & set(lst_s)) == 0) & set(combi).issubset(set(lst_s)):
                        result.append(df_lsts.loc[i, 'RECIPE_ID'])
        sample_combi_result = result
        recommendations = Recipe.objects.filter(
            recipe_id__in=sample_combi_result)
        r_serializer = RecipeSerializer(recommendations, many=True)
        return JsonResponse(r_serializer.data, safe=False)
