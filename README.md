# 📱 모바일 게임 차트 자동 분석 봇

한국 App Store 게임 차트를 **매일 자동 수집**하고, **다중 시간축(1일/1주/1달/분기/1년) 분석**과 **Claude AI 시장 인사이트**를 거쳐 **이메일 리포트**와 **인터랙티브 웹 대시보드**로 전달하는 봇입니다.

**🔗 라이브 대시보드:** https://hyunxn-01.github.io/mobile-chart-bot/

## 핵심 기능

- **두 개의 차트 수집**: Apple iTunes RSS로 한국 게임 **매출(Top Grossing)** 차트와 **인기(Top Free)** 차트를 매일 Top 100까지 수집합니다.
- **다중 시간축 분석**: 일별 순위와 주·월·분기·년 기간 평균을 함께 제공합니다.
- **AI 인사이트(Opus 4.8)**: Claude Opus 4.8(적응형 사고 + effort=max)이 차트 추세를 분석합니다. 같은 기간 차트의 인사이트는 일관되게 유지됩니다.
- **자동 리포트**: 매일 시간축별 엑셀 첨부 + 이메일 발송, 대시보드 바로가기 버튼 포함.
- **웹 대시보드**: 시간축 탭 + 게임 선택 강조 + 순위 이력 표 + **매출/인기 토글** + **퍼블리셔별 차트 장악력** 뷰. 확대·드래그 이동 지원.

## 웹 대시보드

GitHub Pages로 호스팅되는 단일 페이지(`docs/`)입니다. 워크플로가 매일 `data/history*`를 집계해 `docs/data.json`을 갱신하면 자동으로 최신화됩니다.

- **순위 추이 그래프**: 전체 게임은 흐린 회색, 선택한 게임만 색으로 강조(순위축은 위가 1위).
- **시간축 탭**: 일·주·월·분기·년 전환. 데이터가 부족한 시간축은 안내 배너 표시.
- **순위 이력 표**: 선택 게임의 시간축별 순위를 표로(상승=초록·하락=빨강), 그래프 색 구분칸 포함.
- **매출/인기 토글**: Top Grossing ↔ Top Free 차트를 한 번에 전환.
- **퍼블리셔별 차트 장악력**: 최근 차트 기준 개발사별 등장 게임 수·최고/평균 순위 집계. 행을 누르면 그 퍼블리셔의 게임이 그래프에 강조됩니다.

## 빠른 시작

1. `requirements.txt` 의존성 설치
2. GitHub Secrets 4개 등록 (`ANTHROPIC_API_KEY`, `GMAIL_USER`, `GMAIL_APP_PASSWORD`, `RECIPIENT_EMAIL`)
3. cron-job.org에서 워크플로 트리거 설정(매일)
4. Settings → Pages → Deploy from a branch → `main` `/docs`로 대시보드 켜기
5. Actions 탭에서 수동 실행으로 동작 확인

대시보드 배포·운영 가이드는 **`DASHBOARD_SETUP.md`** 를 참고하세요.

## 파일 구조

```
mobile-chart-bot/
├── chart_collector.py          # 메인 로직 (수집·분석·AI 인사이트·이메일)
├── build_dashboard.py          # data/history* → docs/data.json 집계(매출·인기·퍼블리셔)
├── requirements.txt            # Python 의존성 (anthropic 등)
├── README.md                   # 이 파일
├── DASHBOARD_SETUP.md          # 대시보드 배포·설정 가이드
├── .github/workflows/
│   └── daily_chart.yml         # GitHub Actions 워크플로 (수집→집계→커밋→발송)
├── docs/                       # GitHub Pages 대시보드
│   ├── index.html              # 대시보드 단일 페이지
│   └── data.json               # 집계 결과(워크플로가 자동 생성)
└── data/
    ├── history/                # 매출(Top Grossing) 일별 스냅샷
    │   └── YYYY-MM-DD.json
    └── history_free/           # 인기(Top Free) 일별 스냅샷
        └── YYYY-MM-DD.json
```

## 기술 스택

- **Python 3.11**
- **Claude API** (`claude-opus-4-8`, 적응형 사고 + effort=max, 스트리밍 호출) — AI 인사이트 생성
- **Chart.js + chartjs-plugin-zoom** — 대시보드 시각화
- **GitHub Pages** — 대시보드 호스팅
- **GitHub Actions** — 실행 환경 + 데이터 커밋
- **cron-job.org** — 외부 스케줄 트리거
- **Gmail SMTP** — 리포트 발송
