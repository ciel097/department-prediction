from matplotlib import font_manager, rc
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
#colors_5 = ['#F5A9A9','#F5BCA9', '#F5D0A9', '#F3E2A9'  ,'#D0F5A9' ,'#A9F5BC'  ,'#A9E2F3' ,'#A9D0F5' ,'#A9BCF5', '#A9A9F5']
colors_pie= ['#F78181', '#F79F81', '#F7BE81', '#BEF781', '#81F7BE', '#81DAF5', '#81BEF7', '#819FF7', '#9F81F7']
colors_total = ['#F5BCA9', '#F6D8CE', '#F8E6E0', '#F5D0A9', '#F6E3CE', '#FFDAB9', '#FFE4B5', '#FFEFD5', '#FAFAD2', '#EEE8AA', '#E1F5A9', '#ECF6CE', '#F1F8E0', '#D0F5A9', '#E3F6CE', '#ECF8E0','#CEECF5', '#E0F8F7', '#CEE3F6', '#EFF5FB', '#CED8F6']
colors_blue=['#A9E2F3']
colors_5=['#F5BCA9','#F5BCA9','#F5BCA9','#F5BCA9','#F5BCA9','#FFEFD5','#FFEFD5','#FFEFD5','#FFEFD5','#FFEFD5','#ECF6CE','#ECF6CE','#ECF6CE','#ECF6CE','#ECF6CE', '#E0F8F7', '#E0F8F7', '#E0F8F7', '#E0F8F7', '#E0F8F7', '#CECEF6', '#CECEF6', '#CECEF6', '#CECEF6', '#CECEF6',  '#E6E6E6', '#E6E6E6', '#E6E6E6', '#E6E6E6', '#E6E6E6','#BDBDBD','#BDBDBD','#BDBDBD','#BDBDBD','#BDBDBD']

####### 사이드바(한글로)
st.sidebar.page_link("app.py", label="메인")
st.sidebar.page_link("pages/department-prediction.py", label="민원 담당 부서 예측")
st.sidebar.page_link("pages/statics.py", label="민원 처리 정보 안내")
st.sidebar.page_link("pages/workload-predictions.py", label="이 달의 민원 업무량 예측")
#st.sidebar.page_link("pages/chatbot.py", label="AI 챗봇")
###########################################

# csv 파일 읽어오기
df = pd.read_csv("saeol_data_all.csv")

df['req_mon'] = pd.to_datetime(df['작성일']).dt.month # 한번 만들어지면 다음엔 주석처리할것
df['req_year'] =pd.to_datetime(df['작성일']).dt.year # 한번 만들어지면 다음엔 주석처리할 것

####### 부서별 민원 처리 소요시간(업무량 예측 페이지와 겹치는 정보라 생략)
#num_dep = [10,30,50]
#num_rank = st.selectbox("부서수 선택", num_dep)

#fig_wk_y = 6
#if (num_rank == 10) :
#  fig_wk_y = 6
#elif(num_rank == 30):
#  fig_wk_y = 12
#elif(num_rank == 50):
#  fig_wk_y = 18
#else :
#  fig_wk_y = 6

#start_date = pd.to_datetime(df["작성일"]) 
#end_date = pd.to_datetime(df["답변일자"])
#df["work_tm"] = end_date - start_date
#fig_wk = plt.figure(figsize=(20, fig_wk_y))
#wk_tm = df.groupby("담당과")["work_tm"].mean().dt.days
#wk_tm = wk_tm.sort_values(ascending=False)
#wk_rank = wk_tm.iloc[0:num_rank]
###################################################

#wk_rank.plot.barh(color=colors_5)
#plt.title(f"부서별 소요시간(상위 {num_rank} 부서)",fontsize=30,pad=20)
#plt.ylabel("부서명",fontsize=20)
#plt.xlabel("소요시간",fontsize=20)
#plt.xticks(fontsize=20)
#plt.yticks(fontsize=20)

#st.pyplot(fig_wk)
#st.caption("민원 처리 시간 데이터를 분석하여 부서별 평균 민원시간 예측")
########################################3
    

# 원하는 연도의 부서별 민원 요청수

searching_year = [2023,2022,2021,2020,2019,2018,2017,2016,2015,2014]
year = st.selectbox("연도 선택", searching_year)

df_year = df[df['req_year'] == year ]

df_dept = df_year.groupby("담당과").size().reset_index(name="freq") # reset_index가 붙어 series가 df가 되었음


df_dept['freq'] = df_dept['freq'].astype(int)
df_dept = df_dept.sort_values(by='freq', ascending=False)
df_dept_above10 = df_dept[ df_dept['freq'] > 10 ]
df_dept_above10 = df_dept_above10.reset_index(drop=True)

fig_dept_above10 = plt.figure(figsize=(20, 12))
plt.barh(df_dept_above10['담당과'], df_dept_above10['freq'],color=colors_5)
plt.title('부서별 민원요청수('+str(year)+'년 기준)',fontsize=30,pad=20)
plt.ylabel('담당부서',fontsize=20)
plt.xlabel('요청수',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.tight_layout()
# 차트 보여주기
#plt.show()
st.pyplot(fig_dept_above10)


## 그래프 아래 코멘트 달기
dept1 = str(df_dept_above10.iloc[0]['담당과'])
dept2 =str(df_dept_above10.iloc[1]['담당과'])
str_last1 = str(df_dept_above10.iloc[-1]['담당과'])
str_last2 = str(df_dept_above10.iloc[-2]['담당과'])

def cal_app_min(val):
  ran = [200,180,150,130,100,80,50,30,10]
  near= ran[0]

  for i in range(len(ran)):
    gap = ran[i] - val
    if (gap <0) :
      continue
    elif ( gap < near - val ):
      near = ran[i]

  return near

min_freq = int(df_dept_above10.iloc[-2]['freq'])
app_min = cal_app_min(min_freq)
str_dept = f'이 그래프는 {year}년도에 각 부서별로 접수된 민원 요청 수를 보여줍니다. 부서마다 민원 처리 건수가 상이하며, {dept1}와 {dept2}가 가장 많은 민원을 처리했음을 알 수 있습니다. 상대적으로 적은 민원을 처리한 {str_last1}와 {str_last2}와 같은 부서들로, 요청 수가 {app_min}건 미만입니다. '
st.caption(str_dept)
st.write('   ')
st.write('   ')
#########################################3



#######################################

# 담당부서들이 많아서 num_request 건 이상인 부서들만 추려보았음
# pie 차트
num_request = 100

df_dept_aboveNUM = df_dept[ df_dept['freq'] > num_request ]
#print(df_dept_above100)
# 파이차트 그리기

fig_df_dept_aboveNUM = plt.figure(figsize=(20, 10))
textprops = {"fontsize":15} 
plt.pie(df_dept_aboveNUM['freq'], labels=df_dept_aboveNUM['담당과'],colors=colors_pie, autopct='%1.1f%%', startangle=90,textprops=textprops)

# 차트 제목 추가
plt.title('부서별 민원요청비율('+str(year)+'년 기준,'+ str(num_request)+'건 이상)',fontsize=25,pad=20)

# 그래프를 원형으로 보이게 조정
plt.axis('equal')
#plt.show()
# 차트 보여주기
st.pyplot(fig_df_dept_aboveNUM)

#### 그래프 아래 코멘트달기
#def make_autopct(values):
#    def my_autopct(pct):
#        total = sum(values)
#        val = int(round(pct*total/100.0))
#        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
#    return my_autopct

total=  sum(df_dept_aboveNUM['freq']) 
per = df_dept_aboveNUM.iloc[0]['freq']/ sum(df_dept_aboveNUM['freq'])    

str_pie_dept1 = str(df_dept_aboveNUM.iloc[0]['담당과'])
str_pie_dept2 = str(df_dept_aboveNUM.iloc[1]['담당과'])
str_pie_dept3 = str(df_dept_aboveNUM.iloc[2]['담당과'])
#str_pie = f'이 그래프는 {year}년 부서별 민원 요청 비율을 보여주며, {str_pie_dept1}가 {per:.2%}로 가장 많은 민원을 받았습니다. {str_pie_dept2}와 {str_pie_dept3}가 그 뒤를 잇고 있으며, 일부 부서는 상대적으로 낮은 비율을 기록했습니다.'
str_pie = f'이 그래프는 {year}년 부서별 민원 요청 비율을 보여주며, {str_pie_dept1}가 {per:.1%}로 가장 많은 민원을 받았습니다. {str_pie_dept2}와 {str_pie_dept3}가 그 뒤를 잇고 있습니다.'
st.caption(str_pie)
###############################################

# 원하는 연도의 월별 부서별 민원 요청수 그래프들(위 결과를 월별로 세부적으로 보기위해)

df_mon = df_year.groupby("req_mon").size().reset_index(name="mon_freq") # reset_index가 붙어 series가 df가 되었음

df_mon['mon_freq'] = df_mon['mon_freq'].astype(int)
df_mon = df_mon.sort_values(by='mon_freq', ascending=False)

fig_mon_dept = plt.figure(figsize=(20, 12))
plt.bar( df_mon['req_mon'], df_mon['mon_freq'],color=colors_blue )
plt.xlim(0,13)
plt.margins(x=0)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# 차트 제목 추가
plt.title('월별 전체 민원 요청수('+ str(year) + '년기준)',fontsize=30,pad=20)

# 차트 보여주기
#plt.show()
st.pyplot(fig_mon_dept)

indx_mon = df_mon['mon_freq'].idxmax()
most_mon=df_mon['req_mon'][indx_mon] 
most_req = df_mon['mon_freq'][indx_mon] 
str_comment_mon = f'이 그래프는 {year}년 월별 민원 요청 수를 나타내며, {most_mon}월에 민원이 가장 많이 발생하여 {most_req}건을 기록했습니다.'
st.caption(str_comment_mon)
st.write(' ')
############################################################
# 월별 부서별 민원요청수
searching_month = [1,2,3,4,5,6,7,8,9,10,11,12]
cur_mon = 9
str_select_mon = '해당 연도('+str(year)+'년)의 월 선택'
selected_mon = st.selectbox(str_select_mon, searching_month,index=cur_mon-1)

fig_selected_mon = plt.figure( figsize=(20,12))
df_month = [0]
df_mongrp = [0]

df_month = df_year[df_year['req_mon']==selected_mon]
df_mongrp = df_month.groupby("담당과").size().reset_index(name="mon_freq")
df_mongrp = df_mongrp.sort_values(by='mon_freq',ascending=False)  

plt.title(str(selected_mon)+'월')
plt.barh(df_mongrp['담당과'], df_mongrp['mon_freq'],color=colors_5 )
plt.xticks(fontsize=20)
plt.yticks( fontsize=20)
plt.xlim(0,150)
plt.margins(x=0)
plt.tight_layout()
plt.title('해당연월('+str(year)+'년 '+str(selected_mon)+'월)의 부서별 민원요청수',fontsize=30,pad=20)
st.pyplot(fig_selected_mon)

##그래프아래 코멘트달기
str_mon_dept1 = str(df_mongrp.iloc[0]['담당과'])
str_mon_dept2 =str(df_mongrp.iloc[1]['담당과'])
str_mon_dept3 =str(df_mongrp.iloc[2]['담당과'])
str_mon_last1 = str(df_mongrp.iloc[-1]['담당과'])
str_mon_last2 = str(df_mongrp.iloc[-2]['담당과'])
str_most_req =  str(df_mongrp.iloc[0]['mon_freq'])
str_comment_m = f'이 그래프는 {year}년 {selected_mon}월 기준 부서별 민원 요청 수를 보여줍니다. {str_mon_dept1}가 {str_most_req}건으로 가장 많은 민원을 처리했으며, 그 다음으로 {str_mon_dept2}와 {str_mon_dept3}가 높은 민원 수치를 기록했습니다. 반면, {str_mon_last1}와 {str_mon_last2}등 일부 부서는 상대적으로 적은 민원 요청을 받았습니다.'

st.caption(str_comment_m)
################################################################
