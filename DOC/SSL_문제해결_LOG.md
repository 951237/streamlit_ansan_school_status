# SSL 핸드셰이크 문제 해결 로그

## 문제 상황
GitHub Actions 환경에서 경기도교육청 웹사이트 크롤링 시 SSL 핸드셰이크 실패:
```
ssl.SSLError: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure
```

## 원인 분석
1. 대상 서버(`www.goeas.kr`)가 오래된 TLS 버전(TLS 1.0/1.1) 사용
2. Python 3.11의 기본 SSL 컨텍스트는 TLS 1.2 이상만 지원
3. 서버와 클라이언트 간 TLS 버전 불일치로 핸드셰이크 실패

## 해결 방법

### 시도 1: URL 수정 ❌
- 기존 URL이 400 에러 반환
- 개선사항 문서의 올바른 URL로 변경
- 결과: URL은 수정되었으나 SSL 에러 지속

### 시도 2: requests 라이브러리 + verify=False ❌
- urllib에서 requests로 변경
- SSL 검증 비활성화 (`verify=False`)
- 결과: 로컬에서는 성공, GitHub Actions에서는 실패

### 시도 3: CustomHttpAdapter (최종 해결) ✅
```python
class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        ctx = create_urllib3_context()
        ctx.load_default_certs()
        ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=ctx
        )
```

#### 핵심 포인트
- `OP_LEGACY_SERVER_CONNECT` (0x4): OpenSSL 3.0의 레거시 서버 연결 허용
- `create_urllib3_context()`: urllib3의 SSL 컨텍스트 생성
- `session.mount()`: HTTPS 요청에 커스텀 어댑터 적용

## 테스트 결과
```bash
Start to working. . .
✅ Data fetched successfully: 6 rows
Save file. . .
```

## 관련 커밋
1. `38ad47a` - URL 수정 및 requests 라이브러리 도입
2. `9fec96e` - CustomHttpAdapter로 레거시 서버 호환성 확보

## 참고 자료
- [OpenSSL 3.0 Breaking Changes](https://www.openssl.org/docs/man3.0/man7/migration_guide.html)
- [urllib3 SSL Context](https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings)
- [Python SSL Module](https://docs.python.org/3/library/ssl.html)

## 추가 권장사항
대상 서버 관리자에게 TLS 1.2+ 업그레이드 요청 권장 (보안 취약점)
