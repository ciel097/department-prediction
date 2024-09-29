import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from joblib import load
import matplotlib.font_manager as fm
import numpy as np

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

####### 사이드바(한글로)
st.sidebar.page_link("app.py", label="메인")
st.sidebar.page_link("pages/department-prediction.py", label="민원 담당 부서 예측")
st.sidebar.page_link("pages/statics.py", label="민원 처리 정보 안내")
st.sidebar.page_link("pages/workload-predictions.py", label="이 달의 민원 업무량 예측")
st.sidebar.page_link("pages/chatbot.py", label="AI 챗봇")
###########################################

complaint = st.text_area("민원 내용을 입력하시면 담당부서를 예측해 드립니다.",height=100)

# 모델 불러오기
vectorizer = load('tfidf_vectorizer.joblib')
loaded_model = load('model_mlp.joblib')

# 민원 예시
#complaint = t
if (st.button("예측")):

  # 모델 불러오기
  vectorizer = load('tfidf_vectorizer.joblib')
  loaded_model = load('model_mlp.joblib')

 # complaint = "주차 공간 부족으로 인근 도로에 불법 주차가 발생하고 있습니다. 추가 주차 공간 확보 방안이 필요합니다."
  new_complaints = [complaint]

  # TF-IDF 변환
  X_new_tfidf = vectorizer.transform(new_complaints)

  # 담당과 예측 및 확률
  predictions = loaded_model.predict(X_new_tfidf)
  probabilities = loaded_model.predict_proba(X_new_tfidf)

  # 각 민원에 대해 두 개의 담당과와 확률 출력
  for complaint, prediction, probs in zip(new_complaints, predictions, probabilities):
     # 담당과 및 확률을 정렬하여 상위 2개 추출
      top_indices = probs.argsort()[-2:][::-1]
      top_classes = [loaded_model.classes_[i] for i in top_indices]
      top_probs = [probs[i] for i in top_indices]


  ## 그래프 그리기
  fig_dept = plt.figure(figsize=(20, 6))
  plt_class = [top_classes[1], top_classes[0]]
  plt_prob = [top_probs[1], top_probs[0]] 
  plt.barh(plt_class, plt_prob, color=['#F3E2A9', '#A9E2F3'])

  # 그래프 제목과 축 라벨 추가
  plt.title('담당부서 예측', fontsize=32, loc='left', pad=20)
  plt.xlabel('확률', fontsize = 18)
  plt.ylabel('담당부서', fontsize=18, rotation=90 )
  plt.yticks(fontsize=32)

  st.pyplot(fig_dept)


