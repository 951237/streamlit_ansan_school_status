import os
import pandas as pd
import lxml
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import datetime


def read_html():
	URL  = 'https://www.goeas.kr/USR/ORG/MNU13/SchoolList.do?orgType=Z'
	df = pd.read_html(URL, header=1)[0]
	df = df[:5]   # '계' 열 삭제
 
	# 공립, 사립 칼럼의 '-' 없애기
	def remove_str(col):
		return col.strip().replace("-","0")

	df['국립'] = df['국립'].apply(remove_str)
	df['공립'] = df['공립'].apply(remove_str)
	df['사립'] = df['사립'].apply(remove_str)
 
	# 공립, 사립 칼럼 숫자로 바꾸기
	# df_spc['가점_기타'] = df_spc['가점_기타'].astype(str)
	df['국립'] = df['국립'].astype(int)
	df['공립'] = df['공립'].astype(int)
	df['사립'] = df['사립'].astype(int)
	return df 

# 파일이름 생성 - 년 월 일
DATE = datetime.datetime.now().strftime ("%Y%m%d")
df = read_html()
df.to_csv(f'data/{DATE}.csv')	# 파일저장하기