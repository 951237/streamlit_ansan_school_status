# UptimeRobot 설정 가이드

## 목적
Streamlit Cloud 무료 티어는 일정 시간 접속이 없으면 휴면 상태로 전환됩니다. UptimeRobot을 사용하여 주기적으로 앱을 호출함으로써 휴면 방지를 할 수 있습니다.

## 설정 단계

### 1. UptimeRobot 계정 생성
1. https://uptimerobot.com 에 접속
2. 무료 계정으로 가입 (이메일 인증 필요)

### 2. HTTP 모니터 생성
1. Dashboard → "Add New Monitor" 클릭
2. Monitor Type: **HTTP(s)** 선택
3. Friendly Name: `안산 학교 현황판` 또는 원하는 이름
4. URL: Streamlit Cloud 배포 URL 입력
   - 예: `https://your-app-name.streamlit.app/`
5. Monitoring Interval: **5 minutes** (무료 플랜 최소 간격)
6. "Create Monitor" 클릭

### 3. 알림 설정 (선택사항)
1. "My Settings" → "Alert Contacts"
2. 이메일, Slack, Discord 등 원하는 알림 채널 추가
3. 모니터 설정에서 알림 대상 연결

### 4. Heartbeat 모니터 설정 (GitHub Actions용)
1. "Add New Monitor" → Monitor Type: **Heartbeat**
2. Friendly Name: `Daily Data Crawl`
3. Heartbeat Interval: **24 hours**
4. Heartbeat URL이 생성됨 (예: `https://heartbeat.uptimerobot.com/ABC123`)
5. GitHub Actions 워크플로우 파일(`.github/workflows/daily_data_crawl.yml`)에서 해당 URL 활성화:
   ```yaml
   - name: Notify via UptimeRobot Heartbeat
     if: always()
     run: |
       curl -X POST "https://heartbeat.uptimerobot.com/YOUR_HEARTBEAT_KEY"
   ```

### 5. 상태 페이지 생성 (선택사항)
1. "Status Pages" → "Add Status Page"
2. 모니터 선택 및 공개 URL 생성
3. 이해관계자와 공유 가능

## 기대 효과
- ✅ Streamlit Cloud 앱 휴면 방지
- ✅ 장애 발생 시 즉시 알림
- ✅ 데이터 수집 작업 실행 확인
- ✅ 서비스 가용성 모니터링

## 참고사항
- 무료 플랜: 최대 50개 모니터, 5분 간격 체크
- 로그는 24시간만 보관
- 자세한 내용은 `HELP/UptimeRobot.md` 참조
