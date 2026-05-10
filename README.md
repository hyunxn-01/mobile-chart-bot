# 한국 모바일 게임 차트 주간 자동 리포트

매주 월요일 한국 시간 오전 9시, Google Play 매출 Top 100 + App Store 인기 Top 100을 자동 수집해서, 전주 대비 변화를 Claude로 요약하고 엑셀 첨부 메일로 발송합니다.

## 동작 흐름

1. Google Play 한국 게임 카테고리 매출 Top 100 수집
2. App Store 한국 게임 카테고리 인기 Top 100 수집
3. 이전 주 데이터와 비교 (신규 진입 / 이탈 / 5등 이상 변동 추출)
4. Claude API로 사업PM 시각의 변화 요약 생성
5. 엑셀 보고서 작성 (3개 시트: 주간 요약 / 이번 주 차트 / 주간 변화)
6. Gmail SMTP로 본인 메일에 첨부 발송
7. 이번 주 데이터를 다음 주 비교용으로 저장 (git commit)

## 셋업 (한 번만)

### 1. GitHub 레포 생성

1. github.com 우측 상단 `+` → `New repository`
2. Repository name: `mobile-chart-bot`
3. **Private** 권장 (API 키 보호)
4. *Add a README file* 등 모든 체크박스 **체크 해제**
5. `Create repository`

### 2. 코드 업로드

레포 페이지에서:

1. `Add file` → `Upload files`
2. 다음 3개 파일 드래그앤드롭:
   - `chart_collector.py`
   - `requirements.txt`
   - `README.md`
3. `Commit changes`

워크플로우 파일은 폴더 구조가 필요하므로 별도:

1. `Add file` → `Create new file`
2. 파일명에 정확히 입력: `.github/workflows/weekly_chart.yml`
3. 내용에 `weekly_chart.yml` 파일 내용 복붙
4. `Commit new file`

### 3. GitHub Secrets 등록

레포 `Settings` → 좌측 `Secrets and variables` → `Actions` → `New repository secret`. 다음 4개를 등록합니다:

| Name | 값 |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic Console에서 받은 키 (`sk-ant-...`) |
| `GMAIL_USER` | 발송용 Gmail 주소 (예: `hyunxn.01@gmail.com`) |
| `GMAIL_APP_PASSWORD` | Gmail 앱 비밀번호 16자리 (공백 없이 또는 그대로) |
| `RECIPIENT_EMAIL` | 결과 받을 메일 주소 (`GMAIL_USER`와 같아도 OK) |

**⚠️ 주의**: Gmail 앱 비밀번호는 일반 Gmail 로그인 비밀번호가 **아닙니다**. `myaccount.google.com/apppasswords`에서 발급받은 16자리 코드입니다.

### 4. 첫 실행 (수동 테스트)

1. 레포 `Actions` 탭
2. 좌측에서 `Weekly Mobile Chart Report` 선택
3. 우측 `Run workflow` 버튼 클릭

성공하면 약 1~2분 후 등록한 메일로 첨부 엑셀이 도착합니다.

첫 실행 때는 *이전 주 데이터*가 없으므로 변화 분석 없이 *현재 차트*만 정리되어 옵니다. 다음 주부터 본격적으로 변화 분석이 들어갑니다.

## 자동 실행

매주 월요일 한국 시간 오전 9시 자동 실행. 별도로 손댈 필요 없습니다.

## 비용

- GitHub Actions: 무료
- Gmail SMTP: 무료 (일 500통 한도, 우리는 주 1통)
- Anthropic API: 매주 약 $0.01, 월 $0.05 이하

## 문제 발생 시

- Actions 탭에서 실행 로그 확인
- 가장 흔한 문제:
  - **Secrets 이름 오타** (대소문자 정확히)
  - **Gmail 앱 비밀번호 오입력** — 16자리 정확히, 공백 포함해도 OK
  - **2단계 인증 비활성화** — 그러면 앱 비밀번호 무효화됨
  - **Anthropic 결제 수단 미등록**
