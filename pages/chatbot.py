#!pip install openai
#!pip install faiss-gpu
#!pip install langchain
#!pip install langchain_openai
#!pip install langchain_community
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

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import openai 
from openai import OpenAI

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
