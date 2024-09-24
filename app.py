import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.header("민원 담당부서 :blue[예측] 시스템",divider='green')
#st.subheader("이 시스템은공무원을 위한 시스템입니다.")
st.caption("이것은 :blue[공무원]을 위한 시스템입니다.")

st.title(':green[예측]')

if st.button("담당 부서 예측"):
    st.switch_page("pages/department-prediction.py")
  
if st.button("민원 현황"):
    st.switch_page("pages/statics.py")

if st.button("업무량 예측"):
    st.switch_page("pages/workload-predictions.py")  

