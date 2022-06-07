import pandas as pd

from .models import *
from account.models import User

# Create your views here.

def IngreBalance(pk, inedible, combi):
    # 메뉴별 영양소 데이터
    recipe_ingre_data = pd.DataFrame(RecipeIngre.objects.all().values())
    # 데이터 결측치 = 0
    recipe_ingre_data = recipe_ingre_data.fillna(0)
    # 재료별 영양소 데이터
    ingre_nut = pd.DataFrame(IngreNut.objects.all().values())
    # 데이터 결측치 = 0
    ingre_nut = ingre_nut.fillna(0)

    # 유저 인덱스
    user_idx = pk
    # 궁합 알고리즘 결과값: recipe_id 리스트
    best_combi_result = combi
    # 유저 못 먹는 재료 리스트
    inedible_list = inedible

    # 해당 idx의 유저 정보 불러오기
    user = User.objects.get(id=user_idx)
    # recipe_id에 해당하는 데이터 -> 레시피영양정보 모델에서 불러오기
    combi_menu_ingre = recipe_ingre_data[recipe_ingre_data["recipe_id"].isin(best_combi_result)]
    
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
            carbo = cal * 0.6 /4
            protein = cal * 0.14 / 4
            fat = cal * 0.26 / 9
        else :
            cal = 354 - 6.91 * age + health * (9.36 * weight + 726 * height / 100 )
            carbo = cal * 0.6 /4
            protein = cal * 0.14 / 4
            fat = cal * 0.26 / 9
        fiber = 30
        calcium = 800
        steel = 12
        magne = 320
        phos = 700
        calrium = 3500
        natrium = 1500
        zinc = 9
        copper = 750
        selenium = 60
        vita_d3 = 10
        dfe = 400
        vita_b12 = 2.4
        vita_c = 100
        threo = 1200
        valine = 1500
        histi = 900
        tyrosine = 3000
        cysteine = 1200
        return [cal, protein, fat, carbo, fiber, calcium, steel, magne, phos, calrium, natrium, zinc, copper, selenium, vita_d3, dfe, vita_b12,
            vita_c, threo, valine, histi, tyrosine, cysteine]

    # 유저의 하루 권장 섭취량
    user_recommend = calculate(user.sex, user.age, user.height, user.weight, health_data)
    # 유저의 한끼 권장 섭취량
    for i in range(0, len(user_recommend)) :
        user_recommend[i] = user_recommend[i] / 3
    
    # 부족 영양소 확인하기 위한 재료 데이터 추출
    source_df = ingre_nut.loc[:, ["name", "energy", "protein", "fat", "carbo", "fiber", "calcium", "steel", "magne", "phos", "calrium", "natrium", "zinc", "copper", "selenium", "vita_d3", "dfe", "vita_b12",
            "vita_c", "threo", "valine", "histi", "tyrosine", "cysteine"]]
    # 부족한 영양소 추출 - 못먹는 메뉴에서 권장 섭취량 대비 비율이 가장 높은 영양소(가장 풍부한 영양소) 추출
    nut_list = ["energy", "protein", "fat", "carbo", "fiber", "calcium", "steel", "magne", "phos", "calrium", "natrium", "zinc", "copper", "selenium", "vita_d3", "dfe", "vita_b12",
            "vita_c", "threo", "valine", "histi", "tyrosine", "cysteine"]
    short_nut = []
    # user db 에서 못먹는 재료 데이터 하나하나 추출
    for elem in inedible_list :
        te = []
        # 재료 하나에 해당하는 재료 영양성분 데이터 추출
        print(elem)
        nut = list(source_df[source_df["name"] == elem].iloc[0])
        # 식품 이름을 제외하고, 영양성분 데이터만 추출
        nut = nut[1:]
        # 문자열로 되어있을 수 있는 데이터 float 형으로 변환
        nut = list(map(float, nut))

        # 각 영양성분 권장섭취량과 비교(절대 양이 아닌, 비율로 계산)
        # 가장 비율이 높은 것을 뽑을 것임(권장섭취량 대비 가장 높은 영양 비율을 가진 재료)
        for i in range(0, len(user_recommend)) :
            # 비율로 나타내기
            te.append((nut[i] - user_recommend[i]) / user_recommend[i])
        # 비율 중 가장 큰 것을 부족 영양소로 추가(menu_list에는 식품 이름이 포함되어 있으므로 가장 큰 영양소를 뽑으려면 +1 해주어야함)
        short_nut.append(nut_list[te.index(max(te))])

    # 영양소 균형 알고리즘 : 가중평균방법
    location = []

    for i in short_nut :
        location.append(nut_list.index(i))

    def nutrient(i) :  
        tem = []
        short_nutri = 0
        
        for j in range(0, len(user_recommend)) :
            tem.append(combi_menu_ingre.iloc[i][j+1] - user_recommend[j])
        
        for k in location :    
            short_nutri += tem[k]
        
        not_short_nutri = sum(tem) - short_nutri
        
        difference = not_short_nutri - short_nutri
        
        total = short_nutri * difference * not_short_nutri / sum(tem)
        
        return [abs(total), combi_menu_ingre.iloc[i]['RECIPE_ID']]

    total_list = []
    for i in range(0, len(combi_menu_ingre)) :
        total_list.append(nutrient(i))
    total_list.sort(key=lambda x:x[0])

    result = []
    for i in range(0, len(total_list)) :
        result.append(total_list[i][1])
    return_result = result[:5]

    # recipe_id에 해당하는 기본정보, 과정정보 가져오기
    def getRecipeInfo(id_list):
        return_result = {}
        for elem in id_list:
            basic_info = RecipeBasic.objects.get(recipe_id=elem)
            order_info = RecipeOrder.objects.get(recipe_id=elem)
            return_result[elem] = {basic_info: basic_info, order_info: order_info}
        return return_result
    last_result = getRecipeInfo(return_result)

    return last_result