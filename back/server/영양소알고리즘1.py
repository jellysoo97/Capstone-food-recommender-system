#!/usr/bin/env python
# coding: utf-8

# In[148]:


import pandas as pd
import numpy as np


# In[149]:


# 데이터 불러오기

source_data = pd.read_csv('C:/Users/dkfzk/Desktop/재료 영양소.csv', encoding = 'euc-kr') #재료 영양성분 데이터
menu_data = pd.read_csv('C:/Users/dkfzk/Desktop/레시피영양정보_취합_2.csv') # 메뉴 영양성분 데이터


# In[150]:


menu_data


# In[151]:


source_data


# In[152]:


sample = ['id', 'password', 1, 30, 180, 70, '저활동적', 'vegetarian', ['땅콩', '복숭아']] # 들어오는 유저 데이터

# 궁합 데이터 처리 결과 나오는 레시피 id(RECIPE_ID)
compat = [10,
 292,
 477,
 627980,
 841542,
 1562405,
 3188369,
 427,
 3,
 55,
 113,
 212,
 223,
 264,
 274,
 396,
 429,
 431,
 426,
 2461334,
 5245842,
 990147,
 90980,
 5423581,
 311,
 445,
 1387951,
 526037,
 3903471,
 7000211,
 6869960,
 1364193,
 1393131,
 174,
 492,
 841542,
 1562405,
 3364816,
 6837447,
 6864600,
 16,
 53,
 54,
 55,
 58,
 78,
 114,
 274,
 396,
 399,
 983950,
 145,
 227,
 1005520,
 6861732,
 7000115,
 161,
 383,
 1034604,
 237,
 181,
 311,
 445,
 1095605,
 2380465,
 6880753,
 6932578,
 6934885,
 494,
 6869960,
 263,
 6925166,
 475,
 477,
 627980,
 153,
 3,
 15,
 16,
 32,
 33,
 43,
 76,
 78,
 118,
 177,
 248,
 279,
 88,
 227,
 6386578,
 7000305,
 50,
 409,
 6861732,
 161,
 380,
 726413,
 782262,
 5423581,
 6837524,
 237,
 119,
 181,
 311,
 445,
 308,
 481,
 2430673,
 6867089,
 7000156,
 427,
 76,
 6901155,
 2461334,
 409,
 7000156,
 6842385,
 1364193,
 1608749]  

# 리스트 중복 제거(list to set, set to list)
compat = set(compat)

compat = list(compat)


# In[153]:


# compat(궁합 처리 후 들어오는 RECIPE_ID)를 가진 데이터 뽑기, 데이터 결측치 0으로 합산

menu = menu_data[menu_data['RECIPE_ID'].isin(compat)] 
menu = menu.fillna(0)


# In[154]:


# 권장섭취량 계산 -  데이터 [이름, 성별(true, false), 키,  나이, 몸무게, 신체활동], 나이별 열량 데이터 필요
# 신체활동 데이터는 1.0(비활동적), 1.11(저활동적), 1.25(활동적), 1,48(매우활동적)
# 2020 한국인 영양섭취 기준, 권장영양소 작성

if sample[6] == '비활동적' :
    sample[6] = 1.0
elif sample[6] == '저활동적' :
    sample[6] = 1.11
elif sample[6] == '활동적' :
    sample[6] = 1.25
else : sample[6] = 1.48

def caculate(sex, age, height, weight, activity) :
    if sex == 1 :
        cal = 662 - 9.53 * age + activity * (15.91 * weight + 539.6 * height / 100 )
        tan = cal * 0.6 /4
        dan = cal * 0.14 / 4
        ji = cal * 0.26 / 9
        
    
    else :
        cal = 354 - 6.91 * age + activity * (9.36 * weight + 726 * height / 100 )
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

reco = caculate(sample[2], sample[3], sample[4], sample[5], sample[6])

for i in range(0, len(reco)) :
    reco[i] = reco[i] / 3

reco


# In[155]:


# 메뉴 데이터에서 한국인 영양섭취 기준에 나열되어 있는 영양분 열만 뽑아내기

menu = menu[['RECIPE_ID', '에너지', '단백질', '지방',
       '탄수화물', '총 식이섬유', '칼슘', '철', '마그네슘', '인', '칼륨', '나트륨', '아연', '구리',
       '셀레늄',  '비타민 D3', '엽산(DFE)', '비타민 B12', '비타민 C', '트레오닌', '발린', '히스티딘',  '티로신', '시스테인']]
menu


# In[156]:


# 부족 영양소 확인하기 위한 재료 데이터 추출

source_df = source_data.loc[:, ['식품', '에너지', '단백질', '지방',
       '탄수화물', '총 식이섬유', '칼슘', '철', '마그네슘', '인', '칼륨', '나트륨', '아연', '구리',
       '셀레늄',  '비타민 D3', '엽산(DFE)', '비타민 B12', '비타민 C', '트레오닌', '발린', '히스티딘',  '티로신', '시스테인']]

source_df = source_df.fillna(0)

source_df


# In[157]:


sample[8]


# In[163]:


# 부족한 영양소 추출 - 못먹는 메뉴에서 권장 섭취량 대비 비율이 가장 높은 영양소(가장 풍부한 영양소) 추출

menu_list = ['RECIPE_ID', '에너지', '단백질', '지방',
       '탄수화물', '총 식이섬유', '칼슘', '철', '마그네슘', '인', '칼륨', '나트륨', '아연', '구리',
       '셀레늄',  '비타민 D3', '엽산(DFE)', '비타민 B12', '비타민 C', '트레오닌', '발린', '히스티딘',  '티로신', '시스테인']

short_nut = []


for j in sample[8] : # user db 에서 못먹는 재료 데이터 하나하나 추출
    te = []
    a = list(source_df[source_df['식품'] == j].iloc[0]) # 재료 하나에 해당하는 재료 영양성분 데이터 추출
    a = a[1:] # 식품 이름을 제외하고, 영양성분 데이터만 추출
    a = list(map(float, a)) # 문자열로 되어있을 수 있는 데이터 float 형으로 변환

    for i in range(0, len(reco)) : # 각 영양성분 권장섭취량과 비교(절대 양이 아닌, 비율로 계산), 가장 비율이 높은 것을 뽑을 것임(권장섭취량 대비 가장 높은 영양 비율을 가진 재료)
        te.append((a[i] - reco[i]) / reco[i]) # 비율로 나타내기

    te

    te.index(max(te))

    short_nut.append(menu_list[te.index(max(te))+1]) # 비율 중 가장 큰 것을 부족 영양소로 추가(menu_list에는 식품 이름이 포함되어 있으므로 가장 큰 영양소를 뽑으려면 +1 해주어야함)

short_nut


# In[168]:


# 영양소 균형 알고리즘 : 가중평균방법

location = []

for i in short_nut : # 부족한 영양소의 인덱스 위치를 찾아냄( 예> 발린 -> 18번째)
    location.append(menu_list.index(i))

# 가중평균 방법 -> 부족 영양소의 합에 부족하지 않은 영양소와 부족한 영양소의 차이의 비율만큼 곱해줌 

def nutrient(i) :  
    tem = []
    short_nutri = 0
    
    for j in range(0, len(reco)) : # 영양소 차이 계산
        tem.append(menu.iloc[i][j+1] - reco[j])
    
    for k in location :    # 부족 영양소 얼마만큼인지 파악
        short_nutri += tem[k]
    
    not_short_nutri = sum(tem) - short_nutri
    
    difference = not_short_nutri - short_nutri
    
    total = short_nutri * difference * not_short_nutri / sum(tem)  # 부족한 영양소에 부족하지 않은 영양소와의 비율만큼 
    
    return [abs(total), menu.iloc[i]['RECIPE_ID']]
    
    #calorie = float(menu.iloc[i]['에너지']) - reco[0]
    #protein = float(menu.iloc[i]['단백질']) - reco[1]
    #fat = float(menu.iloc[i]['지방']) - reco[2]
    #carbon = float(menu.iloc[i]['탄수화물']) - reco[3]
    #vitamin_c = float(menu.iloc[i]['비타민 C']) - reco[4]
    #calcium = float(menu.iloc[i]['칼슘']) - reco[5]
    #potassium = float(menu.iloc[i]['칼륨']) - reco[6]
    #magnesium = float(menu.iloc[i]['마그네슘']) - reco[7]
    #pho = float(menu.iloc[i]['인']) - reco[8]
    #zinc = float(menu.iloc[i]['아연']) - reco[9]
    #celenium = float(menu.iloc[i]['셀레늄']) - reco[10]
    #vitamin_b = float(menu.iloc[i]['비타민 B12']) - reco[11]
    
    #tem = [calorie, protein, fat, carbon, vitamin_c, calcium, potassium, magnesium, pho, zinc, celenium, vitamin_b]
    
    #weigh = []
    
    #for j in range(0, len(tem)) :
        #a = abs(tem[j]) / reco[j] * 100
        #weigh.append(a)
    
    #weigh_source = tem[weigh.index(max(weigh))]
    #weigh_quantity = max(weigh)
    #weigh_sum = sum(weigh) - weigh_quantity
    
    #source_sum = sum(tem)
    
    #total = (weigh_source * (weigh_sum-weigh_quantity) * weigh_sum / sum(weigh))  + weigh_sum * (weigh_sum-weigh_quantity) * weigh_quantity / sum(weigh)
    
    #total = calorie + protein + fat + carbon + vitamin_c + calcium + potassium + magnesium + pho + zinc + celenium + vitamin_b
    #return [abs(total), menu.iloc[i]['RECIPE_NM_KO']]


# In[169]:


total_list = []

for i in range(0, len(menu)) :
    total_list.append(nutrient(i))

total_list.sort(key=lambda x:x[0])


# In[170]:


total_list


# In[171]:


list_a = []

for i in range(0, len(total_list)) :
    list_a.append(total_list[i][1])

list_a

list_a[:5]

