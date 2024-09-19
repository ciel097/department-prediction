import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from joblib import load


complaint = st.text_area("민원 내용을 입력하세요",height=100)




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

  st.write(complaint)
  st.write(top_classes[0])
  st.write(top_probs[0])
  st.write(top_classes[1])
  st.write(top_probs[1])


