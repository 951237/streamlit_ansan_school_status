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

# 파일 패스
# PATH_DATA = 'data/20221102.csv'

# 폴더내에 파일 읽어오기
def read_csv_files():
	path = "./data"
	file_list = os.listdir(path)
	lst_csv = [file for file in file_list if file.endswith(".csv")]	# 폴더내 확장자가 엑셀파일 인것을 리스트에 담기
	return lst_csv

    

# 마지막 파일 선택하기
def get_lastest_file():
    lst_csv = read_csv_files()
    lst_csv.sort()
    return lst_csv, lst_csv[-1]

lst_csv, default_ix = get_lastest_file()	# 파일 목록과 최신 파일 선택하기

# 데이터 파일 불러오기
def get_csvfile(p_file):
	df = pd.read_csv(f'./data/{p_file}', index_col=None)
	return df

# --- 사이드바 생성하기 ---
st.sidebar.header("Please Filter Here:")	# 사이드바 헤더

# 파일 선택하기
file_csvs = st.sidebar.selectbox(
	"Select data file:",
	lst_csv,
	index=lst_csv.index(default_ix)
)

# 데이터프레임 생성
df = get_csvfile(file_csvs)
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