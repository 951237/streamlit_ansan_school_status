import os
import pandas as pd
import lxml
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

# streamlit 페이지 생성
st.set_page_config(
    page_title='안산관내 초등학교 현황',		# 브라우저 탭 제목
    page_icon = ":bar_chart:",				# 브라우저 파비콘
    layout = "wide"							# 레이아웃
    )

def read_html():
	URL  = 'https://www.goeas.kr/USR/ORG/MNU13/SchoolList.do?orgType=Z'
	df = pd.read_html(URL, header=1)[0]
	df = df[:5]   # '계' 열 삭제
	return df 

df = read_html()
st.dataframe(df)

# 학교현황 막대그래프
fig_total_school_num = px.bar(
    df,
	x = df['구분'],
	y = df['계'],
	orientation='v',
	color = df['구분'],
	template="plotly_white")

st.plotly_chart(fig_total_school_num, use_container_width=True)

# 학생수현황 막대그래프
fig_total_student_num = px.bar(
    df,
	x = df['구분'],
	y = df['학생수'],
	orientation='v',
	color = df['구분'],
	template="plotly_white")

st.plotly_chart(fig_total_student_num, use_container_width=True)

# 현황 막대그래프
fig_total_teacher_num = px.bar(
    df,
	x = df['구분'],
	y = df['교원수'],
	orientation='v',
	color = df['구분'],
	template="plotly_white")

st.plotly_chart(fig_total_teacher_num, use_container_width=True)

# 공립, 사립 시각화
df_type = df[['구분','공립','사립']]
df_type = df_type.set_index('구분')
# 수평 바그래프
st.line_chart(df_type, use_container_width=True)