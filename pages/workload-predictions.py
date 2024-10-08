import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt


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

## cmap  설정
from matplotlib.colors import LinearSegmentedColormap
data = np.random.rand(35) * 100

sorted_indices = np.argsort(data)[::-1]
sorted_data = data[sorted_indices]

cmap = LinearSegmentedColormap.from_list('red_to_blue', ['red', 'blue'], N=35)
sorted_colors_custom = cmap(np.linspace(0, 1, 35))

# Generate 35 distinct colors using a colormap that spans a wide range of colors
distinct_colors = plt.cm.get_cmap('tab20c', 35)  # tab20c provides a diverse color palette

##########

####### 사이드바(한글로)
st.sidebar.page_link("app.py", label="메인")
st.sidebar.page_link("pages/department-prediction.py", label="민원 담당 부서 예측")
st.sidebar.page_link("pages/statics.py", label="민원 처리 정보 안내")
st.sidebar.page_link("pages/workload-predictions.py", label="이 달의 민원 업무량 예측")
st.sidebar.page_link("pages/chatbot.py", label="서리풀 챗봇")
###########################################

st.header("이달의 업무량 예측")
#st.subheader("이 시스템은공무원을 위한 시스템입니다.")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

# 데이터 불러오기
data = pd.read_csv('saeol_data_all.csv')

# 월 정보 추출
data['답변일자'] = pd.to_datetime(data['답변일자'])
data['월'] = data['답변일자'].dt.month

# 월별 민원 수
monthly_counts = data.groupby(['담당과', '월']).size().reset_index(name='민원수')

# 레이블 인코딩
le = LabelEncoder()
monthly_counts['담당과'] = le.fit_transform(monthly_counts['담당과'])

# 데이터 분할
X = monthly_counts[['담당과', '월']]
y = monthly_counts['민원수']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# 모델 학습
model = RandomForestRegressor()
model.fit(X_train, y_train)

# 월별 예측
def predict_all_departments(month):
    departments_encoded = le.transform(le.classes_)
    X_pred = pd.DataFrame({'담당과': departments_encoded, '월': [month] * len(departments_encoded)})
    predictions = model.predict(X_pred)

    # 데이터프레임 변환
    result = pd.DataFrame({
        '담당과': le.classes_,
        '예측 민원': predictions
    })

    # 예측 민원
    total_predictions = result['예측 민원'].sum()
    result['민원'] = result['예측 민원'] / total_predictions if total_predictions > 0 else 0
    result = result.sort_values(by='민원', ascending=False).reset_index(drop=True)

    return result[['담당과', '민원']]


from datetime import datetime

today = datetime.today()
month_input = today.month
##################################### 월 선택박스 추가 by Ju
searching_month = [1,2,3,4,5,6,7,8,9,10,11,12]
cur_mon = 9
str_select_mon = '월 선택'
month_input = st.selectbox(str_select_mon, searching_month,index=cur_mon-1)
########################################

predicted_counts = predict_all_departments(month_input)

# 차트
#colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFC300', '#DAF7A6', '#900C3F', '#581845', '#C70039', '#FF5733']

figure1 = plt.figure(figsize=(25, 10))
plt.bar(predicted_counts['담당과'], predicted_counts['민원'], color=distinct_colors(range(35)))
plt.title(f"2024년 {month_input}월 민원 비중 예측",fontsize=32,pad=20)
plt.xlabel("담당과",fontsize=20)
plt.ylabel("민원 비중",fontsize=20)
plt.xticks(rotation=90,fontsize=20)
plt.yticks(fontsize=20)

for index, value in enumerate(predicted_counts['민원']):
    plt.text(index, value, f"{value:.2%}", ha='center', va='bottom')

st.pyplot(figure1)
## str_comment f 스트링으로 위 결과값 넣어 수정할것
str_dep1 = str(predicted_counts.iloc[0]['담당과'])
str_dep2 = str(predicted_counts.iloc[1]['담당과'])
str_dep3 = str(predicted_counts.iloc[2]['담당과'])
per1 = predicted_counts.iloc[0]['민원']
per2 = predicted_counts.iloc[1]['민원']
per3 = predicted_counts.iloc[2]['민원']
str_comment = f"이번 달 민원 예측 결과, {str_dep1}가 전체 업무의 {per1:.2%}로 가장 높은 비중을 차지하며, 그 뒤를 {str_dep2}({per2:.2%})와 {str_dep3}({per3:.2%})이 따릅니다. 주요 부서들이 업무량을 크게 담당하는 가운데, 다양한 부서들이 고르게 참여할 것으로 예상됩니다."
st.caption(str_comment)


