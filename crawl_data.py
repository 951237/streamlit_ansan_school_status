import os
import pandas as pd
import datetime
import warnings
import ssl
import requests
from urllib3 import PoolManager


class LegacySSLAdapter(requests.adapters.HTTPAdapter):
    """구형 TLS 스택을 사용하는 서버와의 핸드셰이크를 허용하는 어댑터."""
    CIPHERS = "DEFAULT:@SECLEVEL=1"

    def __init__(self, *args, **kwargs):
        self._ciphers = kwargs.pop("ciphers", self.CIPHERS)
        super().__init__(*args, **kwargs)

    def _build_ssl_context(self):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.set_ciphers(self._ciphers)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        if hasattr(ssl, "OP_LEGACY_SERVER_CONNECT"):
            ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT
        if hasattr(ssl, "TLSVersion"):
            ctx.minimum_version = ssl.TLSVersion.TLSv1
        return ctx

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        ctx = self._build_ssl_context()
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=ctx,
            **pool_kwargs,
        )

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        ctx = self._build_ssl_context()
        proxy_kwargs["ssl_context"] = ctx
        return super().proxy_manager_for(proxy, **proxy_kwargs)


def read_html():
	URL  = 'https://www.goeas.kr/goeas/cm/cntnts/cntntsView.do?mi=11528&cntntsId=1514'
	print("Start to working. . .")
	
	# SSL 경고 무시
	warnings.filterwarnings('ignore')
	
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}
	
	try:
		session = requests.Session()
		session.mount('https://', LegacySSLAdapter())

		response = session.get(URL, headers=headers, verify=False, timeout=30)
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
