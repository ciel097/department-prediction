#!pip install openai
#!pip install faiss-gpu
#!pip install langchain
#!pip install langchain_openai
#!pip install langchain_community

#from langchain.embeddings import OpenAIEmbeddings
#from langchain.vectorstores import FAISS
#import openai
##################################### add streamlit by Ju 240928
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
#from sklearn.model_selection import train_test_split
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics import accuracy_score
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

#complaint = st.text_area("챗봇에게 민원내용을 문의하시면 답변해 드립니다.",height=100)
# 민원 예시

#if (st.button("검색")):
#  str_result = "챗봇결과값 출력 텍스트칸"
#  st.write(str_result)
#  st.subheader(str_result)
#  st.success(str_result)
#  st.info(str_result)

#####################################

#api_key = st.secrets["openai_key"] 

#embeddings = OpenAIEmbeddings(openai_api_key=api_key)
#db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

