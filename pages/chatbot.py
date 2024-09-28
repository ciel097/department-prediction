import openai
import streamlit as st
from openai import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

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
