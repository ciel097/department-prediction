import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

####### 사이드바(한글로)
st.sidebar.page_link("app.py", label="메인")
st.sidebar.page_link("pages/department-prediction.py", label="민원 담당 부서 예측")
st.sidebar.page_link("pages/statics.py", label="민원 처리 정보 안내")
st.sidebar.page_link("pages/workload-predictions.py", label="이 달의 민원 업무량 예측")
st.sidebar.page_link("pages/chatbot.py", label="AI 챗봇")
###########################################
st.header("민원 담당부서 :blue[예측] 시스템",divider='green')
#st.subheader("이 시스템은공무원을 위한 시스템입니다.")
st.caption("이 시스템은 민원 내용을 입력하면, 자동으로 관련된 담당 부서를 예측하고 민원과 관련된 정보를 분석해 신속하고 효율적인 업무 처리를 지원합니다.")

st.title(':green[예측]')

if st.button("민원 담당 부서 예측"):
    st.switch_page("pages/department-prediction.py")
  
if st.button("민원 처리 정보 안내"):
    st.switch_page("pages/statics.py")

if st.button("이 달의 민원 업무량 예측"):
    st.switch_page("pages/workload-predictions.py")  

if st.button("AI 챗봇"):
    st.switch_page("pages/chatbot.py")

