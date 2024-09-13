import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

t = st.text_area("민원 내용을 입력하세요",height=100)

if st.button("예측"):
  st.write('문의주신 내용으로 예측되는 담당부서는' )
#  st.write('1. 보건소 (90%)')
#  st.write('2. 경찰청(10%)')
  df = pd.DataFrame(
    {
      '예측 담당 부서':['보건소','경찰청'],
      "확률":["95%",'5%']
    }
  )
#  st.write(df)

  fig_prd = plt.figure(figsize=(4,3))
  df = pd.DataFrame( {"담당부서": ["보건소","경찰청"],"확률":[80,20]})
  plt.pie(df["확률"],labels=df["담당부서"],autopct="%.1f%%")
  st.pyplot(fig_prd)


