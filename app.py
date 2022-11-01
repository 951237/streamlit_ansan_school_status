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

PATH_DATA = 'data/20221102.csv'

df = pd.read_csv(PATH_DATA)
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

# 공립, 사립, 국립 학교숫자 시각화
fig = px.bar(
	df,
	x = '구분',
	y = ['공립', '사립','국립'],
	template = 'plotly_white'
)

# 막대그래프 : 값을 한꺼번에 나타내기
fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig, use_container_width=True)