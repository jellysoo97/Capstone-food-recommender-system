from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from rest_framework.parsers import JSONParser

from selectIngre.views import BestCombiGlv
from .models import *
from account.models import User

# Create your views here.

def IngreBalance():
    # 유저 인덱스
    user_idx = BestCombiGlv().pk
    # 궁합 알고리즘 결과값: recipe_id 리스트
    best_combi_result = BestCombiGlv().combi
    # 유저 못 먹는 재료 리스트
    inedible_list = BestCombiGlv().inedible
    combi_menu_list = []

    # 해당 idx의 유저 정보 불러오기
    user = User.objects.get(id=user_idx)
    print("user: ", user)

    # recipe_id에 해당하는 데이터 레시피영양정보 모델에서 불러오기
    for elem in best_combi_result:
        combi_menu_data = RecipeIngre.objects.filter(recipe_id=elem).values()
        combi_menu_list.append(combi_menu_data)
        # NaN은 0으로
    
    # 권장섭취량 계산 -  데이터 [이름, 성별(true, false), 키,  나이, 몸무게, 신체활동], 나이별 열량 데이터 필요
    # 신체활동 데이터는 1.0(비활동적), 1.11(저활동적), 1.25(활동적), 1,48(매우활동적)
    # 2020 한국인 영양섭취 기준, 권장영양소 작성
    if user.health == "비활동적":
        health_data = 1.0
    elif user.health == "저활동적":
        health_data = 1.11
    elif user.health == "활동적":
        health_data = 1.25
    else: health_data = 1.48

    def calculate(sex, age, height, weight, health):
        if sex == 1 :
            cal = 662 - 9.53 * age + health * (15.91 * weight + 539.6 * height / 100 )
            tan = cal * 0.6 /4
            dan = cal * 0.14 / 4
            ji = cal * 0.26 / 9
        else :
            cal = 354 - 6.91 * age + health * (9.36 * weight + 726 * height / 100 )
            tan = cal * 0.6 /4
            dan = cal * 0.14 / 4
            ji = cal * 0.26 / 9
        sik = 30
        cals = 800
        chel = 12
        mag = 320
        inn = 700
        calu = 3500
        nat = 1500
        ahyeon = 9
        guri = 750
        cel = 60
        vit_d = 10
        yeup = 400
        vit_b = 2.4
        vit_c = 100
        tre = 1200
        vallin = 1500
        hist = 900
        ti = 3000
        siste = 1200
        return [cal, dan, ji, tan, sik, cals, chel, mag, inn, calu, nat, ahyeon, guri, cel, vit_d, yeup, vit_b,
            vit_c, tre, vallin, hist, ti, siste]

    # 유저의 하루 권장 섭취량
    user_recommend = calculate(user.sex, user.age, user.height, user.weight, health_data)
    # 유저의 한끼 권장 섭취량
    for i in range(0, len(user_recommend)) :
        user_recommend[i] = user_recommend[i] / 3
    
    # 부족 영양소 확인하기 위한 재료 데이터 추출
    # 부족한 영양소 추출 - 못먹는 메뉴에서 권장 섭취량 대비 비율이 가장 높은 영양소(가장 풍부한 영양소) 추출
    short_nut = []

    for elem in inedible_list :
        te = []
        # a = list(source_df[source_df['식품'] == j].iloc[0])
        # a = a[1:]
        # a = list(map(float, a))

        # for i in range(0, len(user_recommend)) :
        #     te.append((a[i] - user_recommend[i]) / user_recommend[i])

        # te.index(max(te))

        # short_nut.append(menu_list[te.index(max(te))+1])

    # 영양소 균형 알고리즘 : 가중평균방법