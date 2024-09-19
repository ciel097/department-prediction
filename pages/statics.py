#!apt install fonts-nanum
from matplotlib import font_manager, rc
#!sudo apt-get install -y fonts-nanum
#!sudo fc-cache -fv
#!rm ~/.cache/matplotlib -rf

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.font_manager as fm

for font in font_manager.fontManager.ttflist:
    st.write(font.name)
    if 'Nanum' in font.name:
        print(font.name, font.fname)
#    print(font.name)

#plt.rc('font', family='NanumMyeongjo')
plt.rc('font', family='NanumGothic')
plt.text(0.3, 0.3, '한글', size=100)
#Text(0.3, 0.3, '한글')

#font 
plt.rcParams['font.family'] = "NanumGothic"
plt.rcParams['axes.unicode_minus']=False


# cvs 파일 읽어오기
df = pd.read_csv("saeol_data.csv")

df['req_mon'] = pd.to_datetime(df['req_date']).dt.month # 한번 만들어지면 다음엔 주석처리할것
df['req_year'] =pd.to_datetime(df['req_date']).dt.year # 한번 만들어지면 다음엔 주석처리할 것

#############################################
num_rank = 30 
start_date = pd.to_datetime(df["req_date"]) 
end_date = pd.to_datetime(df["resp_date"])
df["work_tm"] = end_date - start_date
fig_wk = plt.figure(figsize=(20, 10))
wk_tm = df.groupby("resp_dept")["work_tm"].mean().dt.days
wk_tm = wk_tm.sort_values(ascending=False)
wk_rank = wk_tm.iloc[0:num_rank]

cmap = plt.get_cmap('prism')
colors = [cmap(i / len(wk_rank)) for i in range(len(wk_rank))]
wk_rank.plot(kind="bar",color=colors)
plt.title(f"부서별 소요시간(상위 {num_rank} 부서)",fontsize=30)
plt.xlabel("부서명",fontsize=20)
plt.ylabel("소요시간",fontsize=20)
#plt.ylim(0,250)
#plt.xticks(rotation=90)
#plt.tight_layout()

st.pyplot(fig_wk)
########################################3

# 원하는 연도의 부서별 민원 요청수

year = 2023

df_year = df[df['req_year'] == year ]

df_dept = df_year.groupby("resp_dept").size().reset_index(name="freq") # reset_index가 붙어 series가 df가 되었음

df_dept['freq'] = df_dept['freq'].astype(int)
df_dept = df_dept.sort_values(by='freq', ascending=False)

#print(df_dept.iloc[-80:,:])

df_dept_above10 = df_dept[ df_dept['freq'] > 10 ]
#print(df_dept_above10)

# Colormap 설정
#cmap = plt.get_cmap('nipy_spectral')
cmap = plt.get_cmap('prism')

# 색상 설정: colormap에서 각 카테고리마다 색을 자동으로 선택
colors = [cmap(i / len(df_dept_above10['resp_dept'])) for i in range(len(df_dept_above10['resp_dept']))]

fig_dept_above10 = plt.figure(figsize=(20, 6))
plt.bar(df_dept_above10['resp_dept'], df_dept_above10['freq'],color=colors)
plt.title(str(year)+'년 부서별 민원요청수')
plt.xlabel('담당부서')
plt.ylabel('요청수')
plt.xticks(rotation=90)
plt.tight_layout()
# 차트 보여주기
#plt.show()

#st.pyplot(fig_dept_above10)


#######################################

# 담당부서들이 많아서
# num_request 건 이상인 부서들만 추려보았음

num_request = 10

df_dept_aboveNUM = df_dept[ df_dept['freq'] > num_request ]
#print(df_dept_above100)
# 파이차트 그리기
fig_df_dept_aboveNUM = plt.figure(figsize=(20, 6))
plt.pie(df_dept_aboveNUM['freq'], labels=df_dept_aboveNUM['resp_dept'], autopct='%1.1f%%', startangle=90)

# 차트 제목 추가
plt.title(str(year)+ '년도 부서별 민원요청비율('+ str(num_request)+'건 이상)')

# 그래프를 원형으로 보이게 조정
plt.axis('equal')
#plt.show()
# 차트 보여주기
st.pyplot(fig_df_dept_aboveNUM)
###############################################

# 원하는 연도의 월별 부서별 민원 요청수 그래프들(위 결과를 월별로 세부적으로 보기위해)

df_mon = df_year.groupby("req_mon").size().reset_index(name="mon_freq") # reset_index가 붙어 series가 df가 되었음

df_mon['mon_freq'] = df_mon['mon_freq'].astype(int)
df_mon = df_mon.sort_values(by='mon_freq', ascending=False)

fig_mon_dept = plt.figure(figsize=(20, 6))
plt.bar( df_mon['req_mon'], df_mon['mon_freq'],color=colors )
plt.xlim(0,13)
plt.margins(x=0)
# 차트 제목 추가
plt.title('월별 전체 민원 요청수('+ str(year) + '년기준)')

# 차트 보여주기
#plt.show()
st.pyplot(fig_mon_dept)
############################################################
# 월별 부서별 민원요청수

f, ax = plt.subplots(6, 2, figsize=(24,66))
df_month = [0]*12
df_mongrp = [0]*12

for i in range(12):
  df_month[i] = df_year[df_year['req_mon']==i+1]
  df_mongrp[i] = df_month[i].groupby("resp_dept").size().reset_index(name="mon_freq")
  plt.subplot(12,1,i+1)
  str_mon = str(i+1)
  plt.title(str_mon+'월')

  plt.bar(df_mongrp[i]['resp_dept'], df_mongrp[i]['mon_freq'],color=colors )
  plt.xticks(rotation=90)
  plt.margins(x=0)


plt.tight_layout()
# 차트 제목 추가
plt.suptitle('월별 부서별 민원요청수(' +str(year) +'년기준)',fontsize=35)
# 차트 보여주기
#plt.show()
st.pyplot(f)
################################################################
