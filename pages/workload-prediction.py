

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

## cmap  설정
from matplotlib.colors import LinearSegmentedColormap
data = np.random.rand(35) * 100

sorted_indices = np.argsort(data)[::-1]
sorted_data = data[sorted_indices]

cmap = LinearSegmentedColormap.from_list('red_to_blue', ['red', 'blue'], N=35)
sorted_colors_custom = cmap(np.linspace(0, 1, 35))

# Generate 35 distinct colors using a colormap that spans a wide range of colors
distinct_colors = plt.cm.get_cmap('tab20c', 35)  # tab20c provides a diverse color palette

# Plot the bar graph with distinct colors for each bar
#fig, ax = plt.subplots(figsize=(10, 6))
#bars = ax.bar(range(35), sorted_data, color=distinct_colors(range(35)))
#### cmap 끝


st.header("이달의 업무량 예측",divider='green')
#st.subheader("이 시스템은공무원을 위한 시스템입니다.")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

# 데이터 불러오기
data = pd.read_csv('saeol_data_copy.csv')

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

predicted_counts = predict_all_departments(month_input)

# 차트
#colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFC300', '#DAF7A6', '#900C3F', '#581845', '#C70039', '#FF5733']

figure1 = plt.figure(figsize=(25, 10))
plt.bar(predicted_counts['담당과'], predicted_counts['민원'], color=distinct_colors(range(35)))
plt.title(f"{month_input}월 민원 비중 예측")
plt.xlabel("담당과")
plt.ylabel("민원 비중")
plt.xticks(rotation=90)

for index, value in enumerate(predicted_counts['민원']):
    plt.text(index, value, f"{value:.2%}", ha='center', va='bottom')

st.pyplot(figure1)

