from django.http import HttpResponse, JsonResponse
from django.core import serializers
import pandas as pd
from .serializers import IngreSerializer
from .models import Ingre
from account.models import User
from firstPreference.models import Recipe
from firstPreference.serializers import RecipeSerializer
import simplejson as json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def ingre_list(request, pk):
    obj = Ingre.objects.filter(ingre_group_small__contains=pk)
    print(obj)
    if request.method == "GET":
        serializer = serializers.serialize("json", obj)
        return HttpResponse(serializer,
                            content_type="text/json-comment-filtered")
        # serializer = IngreSerializer(obj)
        # return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def ingre_combi(request):
    # 필요한 데이터
    df_best_comb_2 = pd.read_excel(
        '/Users/hwangjeong-yeon/Desktop/코딩/파이썬/종설_프로젝트/Capstone-food-recommender-system_hjy/back/server/recommend/재료별최적의궁합_glv_top5.xlsx'
    )
    df_lsts = pd.read_csv(
        '/Users/hwangjeong-yeon/Desktop/코딩/파이썬/종설_프로젝트/Capstone-food-recommender-system_hjy/back/server/recommend/재료리스트정리.csv'
    )
    df_veges = pd.read_csv(
        '/Users/hwangjeong-yeon/Desktop/코딩/파이썬/종설_프로젝트/Capstone-food-recommender-system_hjy/back/server/recommend/채식주의자종류.csv'
    )

    # 유저 아이디로 정보 가져오기
    # 리스트가 텍스트로 오므로 이것을 다시 리스트화 하기
    # obj = User.objects.get(id=pk)
    # vege_kinds_raw = obj.vegtype
    # inedible_groups_raw = obj.allergic
    # jsonDec = json.decoder.JSONDecoder()
    # vege_kinds = jsonDec.decode(vege_kinds_raw)
    # inedible_groups = jsonDec.decode(inedible_groups_raw)

    #
    if request.method == 'POST':
        # 재료들 리스트가 이리로 넘어옴{ingres:[1,2,3,4,...]}
        #data = JSONParser().parse(request)
        # 재료 리스트를 꺼내주기
        #main = data[0]
        main = ["두부"]
        vege_kinds = []
        inedible_groups = []
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
        inedible = set(inedible_groups)

        result = []
        for c in df_best_comb_2['best_combination']:
            combi = c.replace(' ', '').replace('[',
                                               '').replace(']', '').replace(
                                                   "'", "").split(',')
            # 입력된 재료(변수명: main, 형식: 리스트, '식품군별 상세분류'데이터의 ['SUBGROUP'] 원소) 각각 재료별 최적의 궁합 찾기
            if len(set(main) & set(combi)) != 0:
                for i in df_lsts.index:
                    lst_s = df_lsts.loc[i, 'SUBGROUP'].replace(
                        ' ', '').replace('[',
                                         '').replace(']',
                                                     '').replace("'",
                                                                 "").split(',')
                    # 최종적으로 제외해야 하는 재료를 제외하고 최적의 궁합에 있는 모든 재료는 포함하는 레시피 번호
                    # 결과 레시피 번호(변수명: result, 내용: 레시피 번호, 형식:리스트)는 다음 인자로 넘겨줌
                    if (len(inedible & set(lst_s)) == 0) & set(combi).issubset(
                            set(lst_s)):
                        result.append(df_lsts.loc[i, 'RECIPE_ID'])
        sample_combi_result = result
        recommendations = Recipe.objects.filter(
            recipe_id__in=sample_combi_result)
        r_serializer = RecipeSerializer(recommendations, many=True)
        return JsonResponse(r_serializer.data, safe=False)


import json
from rest_framework.parsers import JSONParser
from selectIngre.views import BestCombiGlv
from .models import *

# Create your views here.


def IngreBalance():
    best_combi_result = BestCombiGlv()


########################################################
"""컨텐츠 기반 추천 알고리즘"""
from surprise.model_selection import cross_validate
from surprise import Reader, Dataset, SVD
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.tokenize import word_tokenize
from glove import Corpus, Glove
import pandas as pd
import numpy as np
import pymysql  #pip install pymysql
from sqlalchemy import create_engine  #pip install sqlalchemy


# 문장 임베딩 함수
def sent2vec_glove(tokens, word_dict, embedding_dim=100):
    # 문장 token 리스트를 받아서 임베딩
    size = len(tokens)
    matrix = np.zeros((size, embedding_dim))
    word_table = word_dict  # glove word_dict
    for i, token in enumerate(tokens):
        vector = np.array([word_table[t] for t in token if t in word_table])
        if vector.size != 0:
            final_vector = np.mean(vector, axis=0)
            matrix[i] = final_vector
    return matrix


def content_based(inpt, df_igrds, cosine_sim):
    sim_scores_all = []
    # input값(형식: 리스트, 내용: 영양소 균형 알고리즘까지 거친 레시피 id)
    for idx in inpt:
        cos_id = df_igrds[df_igrds['RECIPE_ID'] == int(idx)].index
        # 레시피 간 유사도
        sim_scores = list(enumerate(cosine_sim[cos_id[0]]))
        # 유사도 높은 순으로 10개
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        sim_scores_all.extend(sim_scores)
    # 나열한 50개의 학습 데이터의 인덱스 리턴 (레시피 id 아님)
    recipe_indices = [i[0] for i in sim_scores_all]
    return recipe_indices


def user_preference(user_id, igrds_id, df_igrds, md_idx, svd):
    # input값(형식: 리스트, 내용: 영양소 균형 알고리즘까지 거친 후 각각의 레시피와 유사한 레시피 10개씩. 레시피 id가 아니라 학습 데이터의 인덱스)
    # input값이 인덱스이므로 각 인덱스에 해당하는 레시피 id 추출
    recipes_id = df_igrds.iloc[igrds_id]['RECIPE_ID']
    recipes = md_idx.loc[list(recipes_id)][['RECIPE_NM_KO', 'RECIPE_ID']]
    # 각 레시피에 대한 유저의 선호도 예측
    recipes['est'] = list(
        map(lambda x: svd.predict(user_id, x).est, list(recipes['RECIPE_ID'])))
    # 선호도 예측점수 높은 순으로 정렬
    recipes = recipes.sort_values('est', ascending=False, ignore_index=True)
    return recipes.head(10)


# 영양소 균형 이후 레시피 id들의 리스트가 inpt 으로 들어감.
def recommendation(inpt):
    # 레시피 정보
    df_recipes = pd.read_csv(
        '~/Desktop/코딩/파이썬/종설_프로젝트/Capstone-food-recommender-system_hjy/레시피기본정보_취합_2 .csv'
    )
    # 각 레시피 마다 필요한 재료 정보
    df_igrds = pd.read_csv(
        '~/Desktop/코딩/파이썬/종설_프로젝트/Capstone-food-recommender-system_hjy/재료리스트정리.csv'
    )
    # 유저 평점 정보
    # 평점 정보는 아래와 같이 구성되어 있음을 전제로 하였습니다.
    '''   user_id	recipe_id	ratings'''
    '''0	100	    2	        5.0'''
    '''1	100	    3	        4.0'''
    db_connection_str = 'mysql+pymysql://root:wangkibbum97@localhost/food_recommender_system'
    db_connection = create_engine(db_connection_str)
    df_ratings = pd.read_sql(
        'SELECT * FROM food_recommender_system.firstPreference_preference',
        con=db_connection)

    # 컨텐츠 기반 추천 알고리즘에서 레시피(메뉴) 간 유사도 추출하는 알고리즘에 필요한 학습 데이터
    train_data = df_igrds['SUBGROUP'].apply(lambda x: x.replace(
        '[', '').replace(']', '').replace("'", '').replace(' ', '').split(','))

    # 유사도 추출 알고리즘 모델 학습
    corpus = Corpus()
    corpus.fit(train_data, window=8)
    glove = Glove(no_components=100, learning_rate=0.05)
    glove.fit(corpus.matrix, epochs=20, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)

    # 단어 사전 -> 문장 임베딩 시 단어 사전의 단어를 기준으로 임베딩
    word_dict = {}
    for word in glove.dictionary.keys():
        word_dict[word] = glove.word_vectors[glove.dictionary[word]]

    # 문장 임베딩
    sentence_glove = sent2vec_glove(train_data, word_dict)
    # 문장 임베딩 결과를 바탕으로 레시피(메뉴)간 유사도 측정
    cosine_sim = cosine_similarity(sentence_glove, sentence_glove)

    # 레시피 기본정보에 레시피 별 필요한 재료 attribute 추가
    md = pd.merge(df_recipes,
                  df_igrds[['RECIPE_ID', 'SUBGROUP']],
                  on='RECIPE_ID')
    """유저 기반 협업 필터링"""

    # 유저 기반 협업 필터링 모델 학습
    reader = Reader()
    # 유저 평점 정보 df_ratings의 컬럼명: 'user_id', 'recipe_id', 'ratings' (변경하려면 아래 코드에서도 변경)
    data = Dataset.load_from_df(
        df_ratings[['user_index', 'recipe_id', 'recipe_score']], reader)
    svd = SVD()
    cross_validate(svd, data, measures=['rmse', 'mae'], cv=4)
    trainset = data.build_full_trainset()
    svd.fit(trainset)

    # 레시피 기본 정보에 레시피 별 필요한 재료 추가한 데이터 인덱스를 레시피 id로 변경
    md_idx = md.copy()
    md_idx.index = md['RECIPE_ID']
    md_idx

    #inpt: input 데이터. 영양소 균형 알고리즘 거친 결과 레시피 id(형식: 리스트, 내용: 레시피 id)
    # 컨텐트 기반으로 받아온 결과(형식: 리스트) 각각 10개씩을 하나의 리스트로 합침 -> 총 50개의 df_igrds의 인덱스(레시피 id아님)
    #inpt 값 가져오기
    content_based_recipes = content_based(inpt, df_igrds, cosine_sim)
    # 모여진 컨텐트 기반 결과(형식: 리스트, 내용: 영양소 균형까지 맞춰진 레시피 각각에 대해 유사한 레시피 id, 총 50개) -> 유저 성향 예측으로 재정렬
    recommend_df = user_preference(100, content_based_recipes, df_igrds,
                                   md_idx, svd)
    # 결과: 데이터프레임(column: 메뉴 이름, 레시피 id, 예측 유저 선호도 평가 점수) - 높은 순으로 10개 정렬
    recommend_json = recommend_df.to_json(orient='columns')
    #json으로 변환한 데이터프레임 통신
    return HttpResponse(recommend_json,
                        content_type="text/json-comment-filtered")
