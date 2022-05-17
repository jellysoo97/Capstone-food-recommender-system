# -*- coding: utf-8 -*-
"""재료궁합모듈.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y-Y5_6brLqnARsNO3rFHLD34P-btG4lA
"""

#데이터 받아오기
df_best_comb_2 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/재료별최적의궁합2수정.csv')
df_lsts = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/재료별리스트정리.csv')

result = []
#입력된 재료 input (변수명: main, 형식: 리스트)
for m in ['두부', '애호박', '소고기']:
  #못먹는 재료 (변수명: inedible, 형식: 리스트) 필터링
  for ex in ['소고기']:
    if m == ex:
      continue
  for combi in df_best_comb_2['best combination']:
    if m in combi:
      combi = combi.replace("'", '').replace('[', '').replace(']', '').replace(' ','').split(',')
    #재료 조합이 들어있는 레시피 번호 저장 -> 다음으로 넘김
      for i in df_lsts.index:
        if (combi[0] in df_lsts.loc[i, 'IRDNT_NM']) & (combi[1] in df_lsts.loc[i, 'IRDNT_NM']):
          #print(df_lsts.loc[i, 'RECIPE_ID'])
          result.append(df_lsts.loc[i, 'RECIPE_ID'])
#print(result)

#결과 (형식: 리스트)
sample_combi_result = result