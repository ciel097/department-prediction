import openai
from openai import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
#from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
### by Ju 240929 start
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
st.sidebar.page_link("pages/chatbot.py", label="AI 챗봇")
###########################################
### Ju 240929  end

api_key = st.secrets["openai_key"]

embeddings = OpenAIEmbeddings(openai_api_key=api_key)

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

import openai

from openai import OpenAI

client = OpenAI(api_key=api_key)

def get_response_from_gpt(query, docs):
    context = "\n\n".join([doc.page_content for doc in docs])

    openai.api_key = api_key
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"{context}\n\n질문: {query}\n\n답변:"}
        ]
    )
    return response.choices[0].message.content

prompt = "서초구 민원 내용을 안내하는 친절한 챗봇 역할 수행:"
user_input = "사용자 입력"
input = prompt + user_input
docs = db.similarity_search(user_input)
if docs:
    response = get_response_from_gpt(input, docs)
    print("챗봇 응답:", response)
else:
    print("관련 정보를 찾을 수 없습니다.")
