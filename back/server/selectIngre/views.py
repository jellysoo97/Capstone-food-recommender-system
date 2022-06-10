from django.http import HttpResponse, JsonResponse
from django.core import serializers
from rest_framework.parsers import JSONParser
import json

from recommend.views import IngreBalance, PreferReco
from .models import *
from account.models import User

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
        return HttpResponse(sub, content_type="text/json-comment-filtered")

# 못먹는 재료 GET
def getInedible(request, pk):
    if request.method == "GET":
        obj = User.objects.get(id=pk)
        user_vege = obj.vegtype
        inedible_groups_raw = obj.allergic
        inedible_groups = inedible_groups_raw.split(",")
        if user_vege:
            get_vege_data = VegeType.objects.filter(vege_kinds__contains=user_vege)
            vege_data = serializers.serialize("json", get_vege_data)
            vege_data_json = json.loads(vege_data)
            vege_indbl = vege_data_json[0]["fields"]["vege_indbl"].split(",")
            inedible_groups.extend(vege_indbl)
        return JsonResponse(inedible_groups, safe=False)


#################################궁합모듈############################################

def BestCombi(request, cate, pk):
    # 유저 아이디로 정보 가져오기
    # 리스트가 텍스트로 오므로 이것을 다시 리스트화 하기
    obj = User.objects.get(id=pk)
    user_vege = obj.vegtype
    inedible_groups_raw = obj.allergic
    inedible_groups = inedible_groups_raw.split(",")

    if request.method == 'POST':
        # 재료들 리스트가 이리로 넘어옴{ingres:[1,2,3,4,...]}
        data = JSONParser().parse(request)
        # 재료 리스트를 꺼내주기
        main = data["selected_ingre"]
    # 알레르기환자: 못먹는 재료가 바로 리스트(inedible_groups)로 들어옴(알레르기 없으면 빈리스트)
    # 채식주의자: 채식주의자의 종류가 리스트로 들어옴(vege_kinds) -> 종류를 받아서 채식주의자별 못먹는 재료 리스트(vege) 생성
    # 채식주의자 아니면 vege_kinds가 빈리스트 -> vege 생성하지 않음
    if user_vege:
        get_vege_data = VegeType.objects.filter(vege_kinds__contains=user_vege)
        vege_data = serializers.serialize("json", get_vege_data)
        vege_data_json = json.loads(vege_data)
        # vege_data = json.dumps(vege_data_json[0])
        vege_indbl = vege_data_json[0]["fields"]["vege_indbl"].split(",")
        inedible_groups.extend(vege_indbl)
    
    # 대체식품 inedible_groups에서 제외
    for elem in main:
        if elem in inedible_groups:
            inedible_groups.remove(elem)

    result, best_combi = [], []
    # bestcombiglv 테이블에서 모든 데이터 가져옴
    best_combi_raw = BestCombiGlv.objects.all()
    # json 변환
    best_combi_data = serializers.serialize("json", best_combi_raw)
    best_combi_json = json.loads(best_combi_data)
    # best_combi에 하나씩 넣어줌 -> best_combi = ["['삼치','달걀']", "['파','감자']",....]
    for elem in best_combi_json:
        best_combi.append(elem["fields"]["best_combination"])

    # c = best_combi의 요소 -> ex) "['삼치','달걀']"
    for c in best_combi:
        # combi = c 형식 바꾼 리스트 -> ex) ['삼치', '달걀']
        combi = c.replace(' ', '').replace('[', '').replace(']', '').replace("'", "").split(',')
        # main과 combi 집합의 교집합이 하나라도 있으면
        if len(set(main) & set(combi)) != 0:
            # ingre_list 테이블? 길이만큼 for문 돌려서
            for i in range(0, 834):
                # ingre_list의 각 행
                lst_s_raw = IngreList.objects.filter(id=i)
                lst_s_data = serializers.serialize("json", lst_s_raw)
                lst_s_json = json.loads(lst_s_data)
                # 각 행의 subgroup
                lst_s = lst_s_json[0]["fields"]["subgroup"]
                # 각 행의 subgroup 형식 바꾸기 -> ['~~', '~~']
                lst_s = lst_s_json[0]["fields"]["subgroup"].replace('"','').replace(' ', '').replace('[', '').replace(']', '').replace("'", "").replace('"', '').split(",")
                if(len(set(inedible_groups) & set(lst_s)) == 0 & set(combi).issubset(set(lst_s))):
                    # 각 행의 recipe_id를 result에 삽입
                    result.append(lst_s_json[0]["fields"]["recipe_id"])
    sample_combi_result = list(set(result))

#################################영양소 균형 & 선호도 알고리즘 따로 실행############################################
    if cate == "balance":
        return_result = IngreBalance(pk, inedible_groups, sample_combi_result)
    else:
        return_result = PreferReco(pk, sample_combi_result)
    
    return JsonResponse(return_result, safe=False)


    # for c in df_best_comb_2['best_combination']:
    #     combi = c.replace(' ', '').replace(
    #         '[', '').replace(']', '').replace("'", "").split(',')
    #     print("combi", combi)
    #     # 입력된 재료(변수명: main, 형식: 리스트, '식품군별 상세분류'데이터의 ['SUBGROUP'] 원소) 각각 재료별 최적의 궁합 찾기
    #     if len(set(main) & set(combi)) != 0:
    #         for i in df_lsts.index:
    #             lst_s = df_lsts.loc[i, 'SUBGROUP'].replace(' ', '').replace(
    #                 '[', '').replace(']', '').replace("'", "").split(',')
    #             # 최종적으로 제외해야 하는 재료를 제외하고 최적의 궁합에 있는 모든 재료는 포함하는 레시피 번호
    #             # 결과 레시피 번호(변수명: result, 내용: 레시피 번호, 형식:리스트)는 다음 인자로 넘겨줌
    #             if (len(inedible_groups & set(lst_s)) == 0) & set(combi).issubset(set(lst_s)):
    #                 result.append(df_lsts.loc[i, 'RECIPE_ID'])
    # sample_combi_result = result
    # print(sample_combi_result)
    # recommendations = Recipe.objects.filter(recipe_id__in=sample_combi_result)
    # r_serializer = RecipeSerializer(recommendations, many=True)
    # return JsonResponse(r_serializer.data, safe=False)


# input데이터(변수명: put, 형식: 딕셔너리) 받아서 indedible_groups 리스트 생성
# inedible_groups = put['allergic'] #리스트
# vege_kinds = put['vegtype'] #문자열
# #알레르기환자: 못먹는 재료가 바로 리스트(inedible_groups)로 들어옴(알레르기 없으면 빈리스트)
# #채식주의자: 채식주의자의 종류가 문자열로 들어옴(vege_kinds) -> 종류를 받아서 채식주의자별 못먹는 재료 리스트(vege) 생성
# #채식주의자 아니면 vege_kinds가 빈리스트 -> vege 생성하지 않음
# if vege_kinds != 'N':
#   vege_idx = list(df_veges[df_veges['VEGE_KINDS'] == vege_kinds].index)[0]
#   vege = df_veges.loc[vege_idx, 'VEGE_INDBL'].split(',')
#   #채식주의자 종류별 못먹는 재료를 못먹는 재료 리스트(indedible_groups)에 추가
#   inedible_groups.extend(vege)

# 못먹는 재료 리스트(inedible_groups)와 대체식품 재료 리스트(alters)를 비교
# 대체도 안되고 최종적으로 제외해야 하는 재료 리스트(indedible) = 대체식품 리스트에 들어있지 않은(대체 안되는) 못먹는 재료 리스트
#inedible = set(inedible_groups) - set(alters)
# result=[]
# for c in df_best_comb_2['best_combination']:
#   combi = c.replace(' ', '').replace('[', '').replace(']', '').replace("'", "").split(',')
#   #입력된 재료(변수명: main, 형식: 리스트, '식품군별 상세분류'데이터의 ['SUBGROUP'] 원소) 각각 재료별 최적의 궁합 찾기
#   if len(set(main) & set(combi)) != 0:
#     for i in df_lsts.index:
#       lst_s = df_lsts.loc[i, 'SUBGROUP'].replace(' ', '').replace('[', '').replace(']', '').replace("'", "").split(',')
#       #최종적으로 제외해야 하는 재료를 제외하고 최적의 궁합에 있는 모든 재료는 포함하는 레시피 번호
#       #결과 레시피 번호(변수명: result, 내용: 레시피 번호, 형식:리스트)는 다음 인자로 넘겨줌
#       if (len(inedible & set(lst_s)) == 0) & set(combi).issubset(set(lst_s)):
#         result.append(df_lsts.loc[i, 'RECIPE_ID'])
# sample_combi_result = list(set(result))
# sample_combi_result