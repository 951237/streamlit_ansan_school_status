import os
import pandas as pd
import datetime
import warnings


def read_html():
	URL  = 'https://www.goeas.kr/goeas/cm/cntnts/cntntsView.do?mi=11528&cntntsId=1514'
	print("Start to working. . .")
	
	# SSL 경고 무시
	warnings.filterwarnings('ignore')
	
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}
	
	try:
		import requests
		response = requests.get(URL, headers=headers, verify=False, timeout=30)
		response.raise_for_status()
		df = pd.read_html(response.text, header=1)[0]
		print(f"✅ Data fetched successfully: {len(df)} rows")
	except Exception as e:
		print(f"❌ Error fetching data: {e}")
		raise
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
print("Save file. . .")
df.to_csv(f'data/{DATE}.csv')	# 파일저장하기