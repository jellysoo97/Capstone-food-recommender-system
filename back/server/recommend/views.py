import pandas as pd
import numpy as np
import json

# from glove import Glove, Corpus
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

from firstPreference.views import getCosine
from .models import *
from account.models import User
from firstPreference.models import Preference
from selectIngre.models import *

# Create your views here.

# recipe_id에 해당하는 기본정보, 과정정보 가져오기
# def getRecipeInfo(id_list):
#     return_result = {}
#     for elem in id_list:
#         elem = int(elem)
#         basic_info = RecipeBasic.objects.get(recipe_id=elem)
#         order_info = RecipeOrder.objects.filter(recipe_id=elem).values()
#         what_info = RecipeWhat.objects.filter(recipe_id=elem).values()
#         return_result[elem] = {"basic_info": 
#         {"recipe_nm_ko": basic_info.recipe_nm_ko, "sumry": basic_info.sumry, 
#         "cooking_time": basic_info.cooking_time, "qnt": basic_info.qnt, 
#         "level_nm": basic_info.level_nm, "img_url": basic_info.img_url}, 
#         "order_info": list(order_info), "what_info": list(what_info)}
#     return json.dumps(return_result, ensure_ascii=False)

# 보내지는 recipe 정보 index 수정
def getRecipeInfo(id_list):
    return_result = {}
    for i in range(0, len(id_list)):
        elem = int(id_list[i])
        basic_info = RecipeBasic.objects.get(recipe_id=elem)
        order_info = RecipeOrder.objects.filter(recipe_id=elem).values()
        what_info = RecipeWhat.objects.filter(recipe_id=elem).values()
        ingre_info = RecipeIngre.objects.filter(recipe_id=elem).values()
        return_result[i] = {"basic_info": 
        {"recipe_nm_ko": basic_info.recipe_nm_ko, "sumry": basic_info.sumry, 
        "cooking_time": basic_info.cooking_time, "qnt": basic_info.qnt, 
        "level_nm": basic_info.level_nm, "img_url": basic_info.img_url}, 
        "order_info": list(order_info), "what_info": list(what_info), "ingre_info": list(ingre_info)}
    return json.dumps(return_result, ensure_ascii=False)

#####################################영양소 균형 알고리즘#####################################################

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
    combi_menu_ingre = combi_menu_ingre.fillna(0)
    
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
    # print(source_df[source_df["name"] == "땅콩"])
    # 부족한 영양소 추출 - 못먹는 메뉴에서 권장 섭취량 대비 비율이 가장 높은 영양소(가장 풍부한 영양소) 추출
    nut_list = ["energy", "protein", "fat", "carbo", "fiber", "calcium", "steel", "magne", "phos", "calrium", "natrium", "zinc", "copper", "selenium", "vita_d3", "dfe", "vita_b12",
            "vita_c", "threo", "valine", "histi", "tyrosine", "cysteine"]
    short_nut = []
    # user db 에서 못먹는 재료 데이터 하나하나 추출
    for elem in inedible_list :
        te = []
        # 재료 하나에 해당하는 재료 영양성분 데이터 추출
        nut = list(source_df[source_df["name"].str.contains(elem)].iloc[0])
        # nut = list(source_df[source_df["name"] == elem].iloc[0])
        # 식품 이름을 제외하고, 영양성분 데이터만 추출
        nut = nut[1:]
        try:
            # 문자열로 되어있을 수 있는 데이터 float 형으로 변환
            nut = list(map(float, nut))  
        except:
            a_new = []
            for ingre in nut:
                if type(ingre) == str:
                    ingre = ingre.replace(",", "")
                a_new.append(ingre)
            nut = list(map(float, a_new))

        # 각 영양성분 권장섭취량과 비교(절대 양이 아닌, 비율로 계산)
        # 가장 비율이 높은 것을 뽑을 것임(권장섭취량 대비 가장 높은 영양 비율을 가진 재료)
        for i in range(0, len(user_recommend)) :
            # 비율로 나타내기
            te.append((float(nut[i]) - float(user_recommend[i])) / float(user_recommend[i]))
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
            if combi_menu_ingre.iloc[i][j+3] == "" :
                tem.append(float(0) - float(user_recommend[j]))
            else:
                elem = str(combi_menu_ingre.iloc[i][j+3])
                elem = elem.replace(",", "")
                tem.append(float(elem) - float(user_recommend[j]))

        for k in location :    
            short_nutri += tem[k]
        
        not_short_nutri = sum(tem) - short_nutri
        
        difference = not_short_nutri - short_nutri
        
        total = short_nutri * difference * not_short_nutri / sum(tem)
        
        return [abs(total), combi_menu_ingre.iloc[i]["recipe_id"]]

    total_list = []
    for i in range(0, len(combi_menu_ingre)) :
        total_list.append(nutrient(i))
    total_list.sort(key=lambda x:x[0])

    result = []
    for i in range(0, len(total_list)) :
        result.append(total_list[i][1])
    return_result = result[:5]
    last_result = getRecipeInfo(return_result)

    return last_result


#####################################선호도 알고리즘#####################################################

# """컨텐츠 기반 추천 알고리즘"""
def PreferReco(pk, combi, main, inedible):
    # 궁합 모듈 결과
    inpt = combi
    # 레시피 정보
    df_recipes = pd.DataFrame(RecipeBasic.objects.all().values())
    # 각 레시피마다 필요한 재료 정보
    df_igrds = pd.DataFrame(IngreList.objects.all().values())

    # 유저 평점 정보
    # 평점 정보는 아래와 같이 구성되어 있음을 전제로 하였습니다.
    # '''   user_id	recipe_id	ratings'''
    # '''0	100	    2	        5.0'''
    # '''1	100	    3	        4.0'''
    df_ratings = pd.DataFrame(Preference.objects.all().values())

    # 컨텐츠 기반 추천 알고리즘에서 레시피(메뉴) 간 유사도 추출하는 알고리즘에 필요한 학습 데이터
    # train_data = df_igrds['SUBGROUP'].apply(lambda x: x.replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(','))

    # # 유사도 추출 알고리즘 모델 학습
    cosine_sim = getCosine()
    # corpus = Corpus()
    # corpus.fit(train_data, window=8)
    # glove = Glove(no_components=100, learning_rate=0.05)
    # glove.fit(corpus.matrix, epochs=20, no_threads=4, verbose=True)
    # glove.add_dictionary(corpus.dictionary)

    # # 단어 사전 -> 문장 임베딩 시 단어 사전의 단어를 기준으로 임베딩
    # word_dict = {}
    # for word in  glove.dictionary.keys():
    #     word_dict[word] = glove.word_vectors[glove.dictionary[word]]

    # # 문장 임베딩 함수
    # def sent2vec_glove(tokens, word_dict, embedding_dim=100):
    #     #문장 token 리스트를 받아서 임베딩  
    #     size = len(tokens)
    #     matrix = np.zeros((size, embedding_dim))
    #     word_table = word_dict     # glove word_dict
    #     for i, token in enumerate(tokens):
    #         vector = np.array([
    #             word_table[t] for t in token
    #             if t in word_table
    #         ])
    #         if vector.size != 0:
    #             final_vector = np.mean(vector, axis=0)
    #             matrix[i] = final_vector
    #     return matrix

    # 컨텐츠 기반
    def content_based(inpt, df_igrds, cosine_sim):
        sim_scores_all = []
        #input값(형식: 리스트, 내용: 궁합 알고리즘까지 거친 레시피 id)
        for idx in inpt:
            cos_id = df_igrds[df_igrds['recipe_id'] == int(idx)].index
            #레시피 간 유사도
            sim_scores = list(enumerate(cosine_sim[cos_id[0]]))
            # print(sim_scores)
            #유사도 높은 순으로 10개
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]
            sim_scores_all.extend(sim_scores)
        #나열한 50개의 학습 데이터의 인덱스 리턴 (레시피 id 아님)
        recipe_indices = [i[0] for i in sim_scores_all]
        recipe_indices = list(set(recipe_indices))
        return recipe_indices

    # 유저 기반
    def user_preference(user_id, igrds_id, df_igrds, md_idx, svd):
        #input값(형식: 리스트, 내용: 궁합 알고리즘까지 거친 후 각각의 레시피와 유사한 레시피 10개씩. 레시피 id가 아니라 학습 데이터의 인덱스)
        #input값이 인덱스이므로 각 인덱스에 해당하는 레시피 id 추출
        recipes_id = df_igrds.iloc[igrds_id]["recipe_id"]
        # recipes = md_idx.loc[list(recipes_id)][['recipe_nm_ko', 'recipe_id']]
        recipes_raw = md_idx.loc[list(recipes_id)][['recipe_nm_ko', 'subgroup']]
        # recipes_nm = md_idx.loc[list(recipes_id)]['recipe_nm_ko']
        # recipes_idx = md_idx.loc[list(recipes_id)].index
        #전체 recipes의 SUBGROUP에서
        recipes = pd.DataFrame()
        # recipes['recipe_id'] = recipes_idx
        # recipes['recipe_nm_ko'] = recipes_nm
        for i in recipes_raw.index:
            lst_s = recipes_raw.loc[i, 'subgroup'].replace(' ', '').replace('[', '').replace(']', '').replace("'", "").split(',')
            #입력된 재료(변수명: main)는 포함하고 최종적으로 제외해야 하는 재료를 제외하는 레시피 번호
            if (len(set(main) & set(lst_s)) != 0) & (len(set(inedible) & set(lst_s)) == 0):
                recipes = recipes.append(recipes_raw.loc[i][['recipe_nm_ko']])
        #각 레시피에 대한 유저의 선호도 예측
        recipes['est'] = list(map(lambda x: svd.predict(user_id, x).est, list(recipes.index)))
        #선호도 예측점수 높은 순으로 정렬
        recipes = recipes.sort_values('est', ascending=False)
        return recipes.head(10)

    # # 문장 임베딩
    # sentence_glove = sent2vec_glove(train_data, word_dict)
    # # 문장 임베딩 결과를 바탕으로 레시피(메뉴)간 유사도 측정
    # cosine_sim = cosine_similarity(sentence_glove, sentence_glove)

    # 레시피 기본정보에 레시피 별 필요한 재료 attribute 추가
    md = pd.merge(df_recipes, df_igrds, left_on = 'recipe_id', right_on = 'recipe_id')

    ################ """유저 기반 협업 필터링""" ##################

    # 유저 기반 협업 필터링 모델 학습
    reader = Reader()
    #유저 평점 정보 df_ratings의 컬럼명: 'user_id', 'recipe_id', 'ratings' (변경하려면 아래 코드에서도 변경)
    data = Dataset.load_from_df(df_ratings[['user_id', 'recipe_id', 'ratings']], reader)
    svd = SVD()
    cross_validate(svd, data, measures=['rmse', 'mae'], cv=4)
    trainset = data.build_full_trainset()
    svd.fit(trainset)

    # 레시피 기본 정보에 레시피 별 필요한 재료 추가한 데이터 인덱스를 레시피 id로 변경
    md_idx = md.copy()
    md_idx = md_idx.set_index("recipe_id")

    # inpt: input 데이터. 식재료 궁합 알고리즘 거친 결과 레시피 id(형식: 리스트, 내용: 레시피 id)
    # 컨텐트 기반으로 받아온 결과(형식: 리스트) 각각 10개씩을 하나의 리스트로 합침 -> 총 50개의 df_igrds의 인덱스(레시피 id아님)
    content_based_recipes = content_based(inpt, df_igrds, cosine_sim)
    #모여진 컨텐트 기반 결과(형식: 리스트, 내용: 영양소 균형까지 맞춰진 레시피 각각에 대해 유사한 레시피 id, 총 50개) -> 유저 성향 예측으로 재정렬
    result = user_preference(pk, content_based_recipes, df_igrds, md_idx, svd)
    #결과: 데이터프레임(column: 메뉴 이름, 레시피 id, 예측 유저 선호도 평가 점수) - 높은 순으로 10개 정렬
    result_tolist = list(result.index)
    last_result = getRecipeInfo(result_tolist)
    return last_result