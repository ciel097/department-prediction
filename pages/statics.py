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

######## 한글폰트 우리것으로 추가
def unique(list):
    x = np.array(list)
    return np.unique(x)
@st.cache_data
def fontRegistered():
    font_dirs = './customFonts'
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)   
    fm._load_fontmanager(try_read_cache=False)

fontRegistered()
fontNames = [f.name for f in fm.fontManager.ttflist]
unique(fontNames)
fontname = 'NanumGothic'
plt.rc('font', family=fontname)
##########
# color를 보기 좋은 색으로 설정
colors5 = ['#F5A9A9','#F5BCA9', '#F5D0A9', '#F3E2A9'  ,'#D0F5A9' ,'#A9F5BC'  ,'#A9E2F3' ,'#A9D0F5' ,'#A9BCF5', '#A9A9F5']
colors_pie= ['#F78181', '#F79F81', '#F7BE81', '#BEF781', '#81F7BE', '#81DAF5', '#81BEF7', '#819FF7', '#9F81F7']
###################
# csv 파일 읽어오기
df = pd.read_csv("saeol_data.csv")

df['req_mon'] = pd.to_datetime(df['req_date']).dt.month # 한번 만들어지면 다음엔 주석처리할것
df['req_year'] =pd.to_datetime(df['req_date']).dt.year # 한번 만들어지면 다음엔 주석처리할 것

####### 부서별 민원 처리 소요시간
num_dep = [10,30,50]
num_rank = st.selectbox("부서수 선택", num_dep)

start_date = pd.to_datetime(df["req_date"]) 
end_date = pd.to_datetime(df["resp_date"])
df["work_tm"] = end_date - start_date
fig_wk = plt.figure(figsize=(20, 6))
wk_tm = df.groupby("resp_dept")["work_tm"].mean().dt.days
wk_tm = wk_tm.sort_values(ascending=False)
wk_rank = wk_tm.iloc[0:num_rank]

wk_rank.plot.barh(color=colors5)
plt.title(f"부서별 소요시간(상위 {num_rank} 부서)",fontsize=30,pad=20)
plt.xlabel("부서명",fontsize=20)
plt.ylabel("소요시간",fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

st.pyplot(fig_wk)
########################################3
    
# 원하는 연도의 부서별 민원 요청수

searching_year = [2023,2022,2021,2020,2019,2018,2017,2016,2015,2014]
year = st.selectbox("연도 선택", searching_year)

df_year = df[df['req_year'] == year ]

df_dept = df_year.groupby("resp_dept").size().reset_index(name="freq") # reset_index가 붙어 series가 df가 되었음

df_dept['freq'] = df_dept['freq'].astype(int)
df_dept = df_dept.sort_values(by='freq', ascending=False)
df_dept_above10 = df_dept[ df_dept['freq'] > 10 ]

fig_dept_above10 = plt.figure(figsize=(20, 6))
plt.barh(df_dept_above10['resp_dept'], df_dept_above10['freq'],color=colors5)
plt.title('부서별 민원요청수('+str(year)+'년 기준)',fontsize=30,pad=20)
plt.xlabel('담당부서',fontsize=20)
plt.ylabel('요청수',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
# 차트 보여주기
#plt.show()

st.pyplot(fig_dept_above10)
#########################################3



#######################################

# 담당부서들이 많아서 num_request 건 이상인 부서들만 추려보았음
# pie 차트
num_request = 10

df_dept_aboveNUM = df_dept[ df_dept['freq'] > num_request ]
#print(df_dept_above100)
# 파이차트 그리기

fig_df_dept_aboveNUM = plt.figure(figsize=(20, 10))
textprops = {"fontsize":15} 
plt.pie(df_dept_aboveNUM['freq'], labels=df_dept_aboveNUM['resp_dept'],colors=colors_pie, autopct='%1.1f%%', startangle=90,textprops=textprops)

# 차트 제목 추가
plt.title('부서별 민원요청비율('+str(year)+'년 기준,'+ str(num_request)+'건 이상)',fontsize=30,pad=20)

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
plt.bar( df_mon['req_mon'], df_mon['mon_freq'],color=colors5 )
plt.xlim(0,13)
plt.margins(x=0)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# 차트 제목 추가
plt.title('월별 전체 민원 요청수('+ str(year) + '년기준)',fontsize=30,pad=20)

# 차트 보여주기
#plt.show()
st.pyplot(fig_mon_dept)
############################################################
# 월별 부서별 민원요청수
searching_month = [1,2,3,4,5,6,7,8,9,10,11,12]
cur_mon = 9
str_select_mon = '해당 연도('+str(year)+'년)의 월 선택'
selected_mon = st.selectbox(str_select_mon, searching_month,index=cur_mon-1)

fig_selected_mon = plt.figure( figsize=(20,6))
df_month = [0]
df_mongrp = [0]

df_month = df_year[df_year['req_mon']==selected_mon]
df_mongrp = df_month.groupby("resp_dept").size().reset_index(name="mon_freq")
df_mongrp = df_mongrp.sort_values(by='mon_freq',ascending=False)  


plt.title(str(selected_mon)+'월')
plt.barh(df_mongrp['resp_dept'], df_mongrp['mon_freq'],color=colors5 )
plt.xticks(fontsize=20)
plt.yticks( fontsize=20)
plt.margins(x=0)
plt.tight_layout()

plt.title('해당연월('+str(year)+'년 '+str(selected_mon)+'월)의 부서별 민원요청수',fontsize=30,pad=20)
st.pyplot(fig_selected_mon)
################################################################
