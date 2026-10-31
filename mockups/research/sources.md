# KPI 지표형 대시보드 조사 출처

조사일: 2026-10-31 · 조사한 사람: Claude (이 저장소의 견본 작업 세션)

## 표기 규칙

- **열람**: 이 세션에서 페이지(또는 그 페이지의 원문 파일)를 실제로 받아 읽었다. 이번 조사에서 열람한 출처는 모두 GitHub(`github.com`, `raw.githubusercontent.com`)에 공개된 오픈소스 도구의 문서 · 예제 원문이다.
- **검색 결과만**: 웹 검색 결과(제목 · 주소 · 검색 엔진이 보여 준 요약)만 봤고 페이지는 열지 못했다. 이 경우 적은 내용은 검색 결과 요약에 나온 범위를 넘지 않는다.
- 각 항목의 `ID`는 `taxonomy.json`의 `dashboards[].id`와 같다.

## 막힌 주소 (네트워크 설정)

이 세션의 네트워크 정책이 GitHub 밖의 웹페이지 대부분을 막았다. 실제로 열기를 시도했다가 막힌 주소는 아래와 같다(모두 `getaddrinfo ENOTFOUND` 또는 연결 실패).

| 막힌 주소 | 시도한 도구 |
|---|---|
| https://help.tableau.com/current/pro/desktop/en-us/dashboard-narratives.htm | WebFetch |
| https://docs.holistics.io/release-notes/ai-dashboard-summaries | WebFetch |
| https://help.databox.com/understanding-the-ai-summary-visualization | WebFetch |
| https://www.strategysoftware.com/strategyone/whats-new/auto-narratives-ai-powered-dashboard-summaries | WebFetch |
| https://domo-webflow.domo.com/ai/agents/executive-performance-briefing-ai-agent | WebFetch |
| https://sensortower.com/blog/sensor-tower-introduces-app-analytics-metrics-and-a-sleek-new-ui | WebFetch |
| https://amplitude.com/docs/agents/dashboard-agent | WebFetch |
| https://www.geckoboard.com , https://en.wikipedia.org , https://sensortower.com | curl |
| https://cdn.jsdelivr.net , https://cdnjs.cloudflare.com (견본용 CDN 확인) | curl |

같은 이유로 다른 상용 도구 페이지는 열기를 더 시도하지 않고 검색 결과로 조사를 이어 갔다. 환경 설정의 Network access에서 해당 도메인을 허용하면 다시 열어 볼 수 있다.

GitHub API(`api.github.com`)의 저장소 목록 조회는 세션 범위 밖이라 거절됐고, 공개 저장소의 원문 파일(`raw.githubusercontent.com`)은 읽을 수 있었다(공개 저장소 읽기는 세션 프록시가 허용한다고 확인함).

## A. 열람한 출처 (25)

| ID | 대시보드 · 기능 | 주소 | 읽은 내용 요약 |
|---|---|---|---|
| O01 | Metabase X-rays (자동 인사이트) | https://github.com/metabase/metabase/blob/master/docs/exploration-and-organization/x-rays.md | 차트의 점을 눌러 '자동 인사이트' → 필드 유형에 맞는 차트 자동 생성, 확대 · 축소 · 관련 항목 제안, 대시보드로 저장 |
| O02 | Metabase Number 차트 | https://github.com/metabase/metabase/blob/master/docs/questions/visualizations/numbers.md | 숫자 하나를 크게, 접두 · 접미 · 소수점, 구간별 조건부 색 |
| O03 | Metabase Trend 차트 | https://github.com/metabase/metabase/blob/master/docs/questions/visualizations/trend.md | 최근 기간 값 + 이전 기간 대비 증감, 비교 최대 3개(이전 기간 · 이전 값 · 목표값 · 다른 열), 좋음/나쁨 색 뒤집기 |
| O04 | Metabase Metabot | https://github.com/metabase/metabase/blob/master/docs/ai/metabot.md | 채팅 사이드바(cmd+e), 차트 분석 요청, 응답 메뉴(복사 · 피드백 · 다시 실행), "결과를 다시 확인하라"는 안내 |
| O05 | Metabase Research | https://github.com/metabase/metabase/blob/master/docs/ai/research.md | 질문 → 계획 → 차트 여러 개 생성, '흥미도(Interestingness)' 순 정렬(AI 또는 결정적 점수), 별표 · 댓글 · 숨김, 사이드바 맨 위 요약(Summary)에 차트 추가, 데이터 점에서 '더 탐색' |
| O06 | Metabase Documents | https://github.com/metabase/metabase/blob/master/docs/documents/introduction.md | 글과 차트를 섞은 긴 분석 문서, `/`로 차트 · Metabot 삽입, 차트 옆 보조 글, `@` 언급 |
| O07 | Metabase 대시보드 소개 | https://github.com/metabase/metabase/blob/master/docs/dashboards/introduction.md | 섹션 틀: KPI 격자 / 큰 차트+오른쪽 KPI / KPI+아래 큰 차트, 변수가 들어가는 글 카드, 탭, "중요한 것을 위 · 크게, 카드 10개 이하" |
| O08 | Grafana Stat 패널 | https://github.com/grafana/grafana/blob/main/docs/sources/visualizations/panels-visualizations/visualizations/stat/index.md | 값 하나 + 선택적 스파크라인 + 변화율, 임계값 색, 계산 방식(평균 · 최근값 등) |
| O09 | Grafana Bar gauge | https://github.com/grafana/grafana/blob/main/docs/sources/visualizations/panels-visualizations/visualizations/bar-gauge/index.md | 필드마다 값 하나로 줄여 범위 안 막대로 표시 |
| O10 | Grafana State timeline | https://github.com/grafana/grafana/blob/main/docs/sources/visualizations/panels-visualizations/visualizations/state-timeline/index.md | 상태(LOW/NORMAL/HIGH…)가 시간에 따라 바뀌는 띠 |
| O11 | Grafana 대시보드 모범 사례 | https://github.com/grafana/grafana/blob/main/docs/sources/visualizations/dashboards/build-dashboards/best-practices/index.md | USE · RED · 4대 신호 같은 지표 선택 틀, 계층형 대시보드와 드릴다운, 같은 것끼리 비교, 의미 있는 색, 축 정규화 |
| O12 | Grafana 저장소 소개 | https://github.com/grafana/grafana | 위쪽 드롭다운 템플릿 변수, 시간 범위 나란히 비교 |
| O13 | Observable Framework 예제 목록 | https://github.com/observablehq/framework/blob/main/examples/README.md | 대시보드 · 리포트 예제 모음 |
| O14 | Observable 예제: 미국 전력망(eia) | https://github.com/observablehq/framework/blob/main/examples/eia/src/index.md | 4열 격자, 지도 카드(2열×3행) + 상위 5 막대 + 수요 대 예측 + 국가 간 교류, 아래 출처 메모 |
| O15 | Observable 예제: Plot 다운로드(plot) | https://github.com/observablehq/framework/blob/main/examples/plot/src/index.md | KPI 카드 4개(최신 버전 · 별 · 일간 · 누적) 줄, 큰 숫자, 28일 · 7일 이동평균 선, 두 번째 KPI 줄 |
| O16 | Observable 예제: 웹 로그(api) | https://github.com/observablehq/framework/blob/main/examples/api/src/index.md | 한 줄 흐름 리포트, 차트마다 아래 작은 설명 메모, 상위 경로 2열 |
| O17 | Observable 예제: 호텔 예약(hotel-bookings) | https://github.com/observablehq/framework/blob/main/examples/hotel-bookings/src/index.md | 세그먼트 선택이 제목 문구까지 바꿈, 행 병합 KPI 카드 |
| O18 | Observable 예제: 모기지 금리(mortgage-rates) | https://github.com/observablehq/framework/blob/main/examples/mortgage-rates/src/index.md | 금리 카드 2개 + 큰 차트(2열×2행), 확대 가능한 전체 기간 차트 |
| O19 | Observable Framework 마크다운 · 격자 문서 | https://github.com/observablehq/framework/blob/main/docs/markdown.md | grid-cols-2~4, colspan · rowspan, 좁은 화면에서 열 수 자동 감소, card · tip 블록 |
| O20 | Streamlit `st.metric` | https://github.com/streamlit/streamlit/blob/develop/lib/streamlit/elements/metric.py | 라벨 · 값 · 증감, 증감 색 정상/반대/끔, 테두리, 값 아래 미니 차트(line/bar/area) |
| O21 | PostHog 웹 분석 대시보드 | https://github.com/PostHog/posthog.com/blob/master/contents/docs/web-analytics/dashboard.mdx | 맨 위 방문자 · 조회 · 세션 등 지표와 이전 기간 비교, 경로 표 클릭 시 대시보드 전체 필터 |
| O22 | PostHog AI | https://github.com/PostHog/posthog.com/blob/master/contents/docs/posthog-ai/index.mdx | 채팅 사이드바 + 화면 곳곳 인라인 진입점, 분석 후 설명, 대시보드 · 알림 생성까지 수행 |
| O23 | Plausible Analytics | https://github.com/plausible/analytics | 핵심 지표를 한 페이지에, 주간 · 월간 메일 리포트와 급등 · 급락 알림 |
| O24 | Tremor 대시보드 템플릿(OSS) | https://github.com/tremorlabs/template-dashboard-oss | SaaS 대시보드 템플릿(README만 읽음, 화면 배치는 README에 설명이 없어 분류에 쓰지 않음) |
| O25 | Lightdash · Rill · Redash 소개 | https://github.com/lightdash/lightdash , https://github.com/rilldata/rill , https://github.com/getredash/redash | 에이전트형 BI(근거 쿼리를 볼 수 있는 답, 검증된 답 재사용), 대화형 BI, 예약 갱신 · 알림 (README만 읽음, 화면 배치 정보가 적어 분류에서는 Lightdash만 씀) |

참고로 읽었지만 대시보드 화면 정보가 없어 분류에 쓰지 않은 것: Metabase Progress/Gauge 문서, Apache Superset README, Our World in Data `owid-grapher` README, WrenAI · Vanna · OpenBB · Umami README, Evidence · Tremor 저장소 첫 화면.

## B. 검색 결과만 본 출처 (55)

### AI 요약 · 해설을 KPI와 함께 보여 주는 BI

| ID | 대시보드 · 기능 | 주소 | 검색 결과에서 확인한 내용 |
|---|---|---|---|
| S01 | Tableau Dashboard Narratives (Tableau Agent) | https://help.tableau.com/current/pro/desktop/en-us/dashboard-narratives.htm | 대시보드 전체 요약 + 차트별 인사이트, 작성자가 대상 시트 제한, 데이터 갱신 시 요약도 바뀜 |
| S02 | Holistics AI dashboard summaries | https://docs.holistics.io/release-notes/ai-dashboard-summaries | 대시보드 옆에 짧은 서술을 자동 생성 · 저장, 추세와 변화 강조 |
| S03 | Databox AI Summary | https://help.databox.com/understanding-the-ai-summary-visualization | 대시보드 안의 블록 하나로 들어가는 AI 요약, 자동 갱신, 편집 가능, 길이 · 문체 선택, 횟수 제한 |
| S04 | Strategy(MicroStrategy) Auto Narratives | https://www.strategysoftware.com/strategyone/whats-new/auto-narratives-ai-powered-dashboard-summaries | AI 대시보드 요약 |
| S05 | Domo Executive performance briefing agent | https://domo-webflow.domo.com/ai/agents/executive-performance-briefing-ai-agent | 생성된 서술을 해당 차트 · KPI 카드 옆에 한 화면으로 배치 |
| S06 | Oracle EPM GenAI 인사이트 요약 | https://docs.oracle.com/en/cloud/saas/readiness/epm/2025/splan-apr25/25apr-sales-planning-wn-f38307.htm | 생성형 AI 인사이트 요약(영어만) |
| S07 | Power BI Narrative with Copilot | https://learn.microsoft.com/en-gb/power-BI/create-reports/copilot-create-narrative | 보고서 · 페이지 · 고른 시각화(KPI 카드 포함) 요약, PDF · PPT 내보내기 |
| S08 | ThoughtSpot Liveboard AI Highlights | https://docs.thoughtspot.com/cloud/latest/liveboard-ai-highlights | 신뢰 구간으로 '예상된 변화/예상 밖 변화' 구분, 탭마다 앞 5개 시계열 KPI, 변화 최대 기여 요인 |
| S09 | ThoughtSpot Monitor (KPI 이상 알림) | https://docs.thoughtspot.com/cloud/latest/monitor | KPI가 예측 범위를 벗어나면 알림 |
| S10 | Qlik Insight Advisor | https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Insights/insight-advisor-natural-language.htm | 자연어 질문 → 차트 + '추가 인사이트 보기', 대시보드용 자연어 인사이트 개체(클릭할 때마다 중요 인사이트 목록 갱신, 커뮤니티 글 https://community.qlik.com/t5/Product-Innovation/Natural-Language-Insights-Powerful-AI-on-Dashboards/bc-p/2015118) |
| S11 | Looker 대시보드 요약 (Conversational Analytics) | https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-data-agents-dashboards | 대시보드 대화를 열면 맨 위에 요약: 무엇을 보여 주는지 · 핵심 하이라이트 · 의미, 예약 발송에도 요약 포함 |
| S12 | Google Analytics 4 홈 인사이트 카드 | https://www.1clickreport.com/blog/ga4-generated-insights-2026-ai-summaries-guide | 홈의 자동 · 맞춤 인사이트 카드, '모든 인사이트 보기', 상호작용에 따라 카드 순서 조정. 기여도 분석: https://support.google.com/analytics/answer/10388660?hl=en |
| S13 | Sisense Narratives | https://docs.sisense.com/main/SisenseLinux/sisense-narratives.htm | 위젯마다 서술 토글 → 그 위젯의 핵심을 요약하는 패널. KPI Card 플러그인(여러 지표 + 추세 + 스파크라인): https://www.sisense.com/marketplace/add-on/kpi-card/ |
| S14 | Zoho Analytics Zia Insights | https://www.zoho.com/analytics/help/zia/zia-insights-dashboard.html | 오른쪽 위 버튼으로 대시보드 전체 인사이트 패널, 구성요소마다 Zia 아이콘, 글 보기 · 차트 보기, 추세 · 급등 · 급락 · 이상 · 기여 요인 |
| S15 | Amplitude Dashboard Agent | https://amplitude.com/docs/agents/dashboard-agent | 대시보드 차트를 분석해 추세 · 이상 · 차트 간 상관을 찾고 우선순위 인사이트와 권고를 반복 생성 |
| S16 | Amplitude 대시보드 표시 방식 · KPI 템플릿 | https://amplitude.com/docs/analytics/dashboard-preferences.md , https://www.amplitude.com/templates/product-kpi-dashboard.md | 차트 · 표 · KPI 표시 전환, '핵심 지표 표시' |
| S17 | Mixpanel Agent (구 Spark) | https://docs.mixpanel.com/docs/mixpanel-agent | 질문 → 차트를 보드에 저장, 보드 · 리포트 해석 |
| S18 | Datadog 대시보드 이상 탐지 · Watchdog | https://docs.datadoghq.com/dashboards/graph_insights/investigate_anomalies/ | 대시보드의 시계열에서 이상을 찾아 동시 발생한 것을 '이슈'로 묶음, 기여 태그, 이슈를 누르면 해당 위젯으로 스크롤, 인사이트 캐러셀은 우선순위 높은 것이 왼쪽 |
| S19 | Yellowfin Signals · Stories | https://www.yellowfinbi.com/blog/industrys-first-automated-analysis-and-cross-vendor-storytelling | 의미 있는 변화 자동 감지(Signals), 글과 시각화를 섞은 이야기(Stories), 대시보드에 붙는 이야기 |
| S20 | Tellius 자동 인사이트 | https://www.tellius.com/product/auto-insights | KPI 변화의 원인 요인을 통계적 유의성으로 순위화, 자연어 요약 + 시각화 + 통계 + 세그먼트 |
| S21 | Narrative BI | https://narrative.bi/platform/ | 일 · 주 · 월 예약 서술 리포트, 이상 알림, 글 중심(시각화 적음) |
| S22 | Bloomberg AI 뉴스 요약 | https://www.bloomberg.com/company/press/bloomberg-launches-gen-ai-summarization-for-news-content | 기사 맨 위 AI 요약 3줄, 기업 뉴스 시간순 요약, 전문가 평가 |
| S23 | Lightdash AI 에이전트 | https://github.com/lightdash/lightdash (README 열람, 위 O25와 같은 출처) | 근거 쿼리를 볼 수 있는 답, 검증된 답 재사용 |

### 모바일 앱 · 게임 시장 분석 도구

| ID | 대시보드 · 기능 | 주소 | 검색 결과에서 확인한 내용 |
|---|---|---|---|
| S24 | Sensor Tower Top Charts · App Intelligence | https://sensortower.com/blog/sensor-tower-introduces-app-analytics-metrics-and-a-sleek-new-ui | 실시간 상위 앱 · 퍼블리셔, 경쟁 비교, 매출 · 다운로드 추세 (제3자 리뷰 요약) |
| S25 | Sensor Tower Game Intelligence (Game IQ) | https://sensortower.com/ko/product/game-intelligence | 하위 장르 · 테마 · 아트 · BM · 메타 분류, 하위 장르 전용 대시보드, 매일 갱신 |
| S26 | Sensor Tower 게임 분류 리포트 2021 | https://sensortower.com/blog/mobile-game-taxonomy-report-2021 | 연도별 장르 점유 변화 |
| S27 | AppMagic | https://appmagic.rocks/tool-descriptions/essentials-new | 매출 · 무료 차트, 수동 장르 태그, 시장 세그먼트 대시보드(장르 동향 · 선두 · 분산도 · 진입 장벽), 최대 100개 앱 비교 |
| S28 | AppTweak Top Charts | https://help.apptweak.com/en/articles/4202346-compare-different-top-charts-across-countries | 나라별 차트 최대 9개 나란히, 상위 10 순위 이력, 과거 날짜 차트, 두 날짜 사이 상승 폭 정렬(높은 순위일수록 가중) |
| S29 | Appfigures Top Charts · Store Performance | https://appfigures.com/products/store-performance | 모든 카테고리 · 나라 순위를 매시간, 증감 · 이력, 목록 나란히 비교, 관심 앱 |
| S30 | GameAnalytics MarketIQ Store Intelligence | https://docs.gameanalytics.com/products-and-features/marketIQ/store-intelligence | 상위 차트 · 뜨는 게임 · 관심 게임과 스튜디오 추적 |
| S31 | GameAnalytics GameIntel | https://gamesbeat.com/gameanalytics-launches-gameintel-market-intelligence-platform/ | 상위 차트, 상위 게임 · 퍼블리셔, 최근 출시, 소프트런칭 |
| S32 | GameRefinery 장르 대시보드들 | https://docs.gamerefinery.com/en/articles/6632072-what-are-the-latest-trends-in-my-market-and-in-specific-segments | Genre Essentials(장르 점유 · 많이 쓰는 기능), Market Trends(기능 도입률 추이), Market Share, Market Explorer |
| S33 | Ludo.ai 시장 인텔리전스 | https://ludo.ai/market-intelligence | 위쪽 필터(출처 · 장르 · 지역) |
| S34 | 42matters 국가별 매출 상위 게임 | https://42matters.com/top-grossing-mobile-games-india | 나라별 준실시간 매출 상위 목록 |
| S35 | 모바일인덱스 GAME (IGAWorks) | https://ditoday.com/?p=90947 | 57개 세부 태그 장르 분석, 퍼블리셔 점유, 순위 통계, 출시 달력 |
| S36 | PocketGamer.biz 주간 글로벌 모바일 게임 차트 | https://www.pocketgamer.biz/weekly-global-mobile-games-charts/ | 나라별 무료 · 매출 순위 + 기간 머리말 + 신규 진입 · 순위 변동 · 퍼블리셔 해설 |
| S37 | EK Gaming 월간 매출 상위 20 리포트 | https://ekgamingllc.com/?p=9340 | 상위 20 + 추세 해설 + 인수합병 |
| S38 | SteamDB Charts | https://steamdb.com/charts | 동시 접속 상위 100, 최고치, 뜨는 게임 |

### 제품 · 웹 분석과 일반 KPI 대시보드

| ID | 대시보드 · 기능 | 주소 | 검색 결과에서 확인한 내용 |
|---|---|---|---|
| S39 | Stripe 대시보드 홈 | https://docs.stripe.com/dashboard/basics | 핵심 숫자 몇 개 + 스파크라인 + 기간 비교 + 처리할 알림 (디자인 분석: https://www.925studios.co/blog/stripe-dashboard-design-breakdown) |
| S40 | Linear Insights | https://linear.app/docs/insights | 측정값 × 나누는 기준 × 세그먼트 선택 → 그래프 + 표, 화면 옆 패널 |
| S41 | Geckoboard 고객 대시보드 · TV 대시보드 | https://www.geckoboard.com/customers/ , https://www.geckoboard.com/blog/data-visualization-for-tv-dashboards-a-teardown | 실제 회사 대시보드 70여 개, TV용 배치, 과도한 정밀도 피하기, 경고 표시 |
| S42 | Klipfolio PowerMetrics | https://klipfolio.com/lp/executive-dashboards | 관리되는 지표 목록으로 경영 대시보드 구성 |
| S43 | Bold BI KPI 예제 | https://www.boldbi.com/blog/build-your-own-kpi-examples-with-sample-data-sources/ | 산업별 예제 데이터와 KPI 위젯 |
| S44 | SimpleKPI 대시보드 예제 52개 | https://www.simplekpi.com/resources | KPI 대시보드 예제 모음 |
| S45 | Tableau Public 오늘의 시각화: 아마존 매출 KPI | https://thedataschool.co.uk/mila-kholodiy/my-first-viz-of-the-day/ | KPI 카드 5개를 이전 기간과 비교, 변화에만 주황색, 나머지는 회색 |
| S46 | Tableau 대시보드 쇼케이스(KPI 위젯 12종) | https://www.tableau.com/en-gb/data-insights/dashboard-showcase/superstore | 월간 성과용 KPI 위젯 12가지 모양 |
| S47 | Tableau Public 인기 시각화 10선 | https://tableau.com/blog/ten-most-favorited-vizzes-celebrate-ten-viz-tastic-years-tableau-public | NCAA 수익 KPI 대시보드, KPI 표현 방법 모음 |
| S48 | Billboard 차트 | https://www.billboard.com/charts/billboard-200/2024-02-17 | 줄마다 NEW · RE-ENTRY 표시, 지난주 순위 · 최고 순위 · 차트 주 수 |
| S49 | Finviz 지도 · Matrix | https://finviz.com/blog/the-finviz-matrix-market-breadth-visualized/ | 트리맵(크기=시가총액, 색=등락, 섹터로 묶음), 섹터 간 강도 매트릭스 |
| S50 | Our World in Data 데이터 인사이트 · 핵심 인사이트 | https://ourworldindata.org/redesigning-from-one-to-two-columns | 주제 페이지 맨 위 핵심 인사이트, 데이터 인사이트 = 결론을 담은 제목 + 차트 + 짧은 글 + 더 보기 |
| S51 | Stephen Few 불릿 그래프 (Domo 설명 글) | https://www.domo.com/learn/charts/bullet-graphs | 측정 막대 + 목표 표시 + 질적 구간 배경, 회색조 |
| S52 | IBCS 표준 (Zebra BI 글) | https://zebrabi.com/designing-financial-reports-dashboards-and-business-presentations/ | 실적 · 계획 · 차이를 일관된 모양 · 색으로, 차이 열을 강조, ISO 24896 |
| S53 | RAG 성과 대시보드 (Kent 의회 · ClearPoint) | https://democracy.kent.gov.uk/documents/s132000/Performance%20Dashboard%20Covering%20Report.pdf , https://www.clearpointstrategy.com/blog/why-rag-status-fails | KPI별 목표 대비 빨강 · 주황 · 초록, 목표 달성 KPI 수, 빨강을 감추는 문제 |
| S54 | NYT 선거 결과 실시간 지도 (Open News 정리) | https://source.opennews.org/articles/us-elections-roundup-november-2013/ | 실시간 결과 지도, 주요 경합 요약, 분 단위 추이 |
| S55 | Sensor Tower의 AppMagic 인수 발표 | https://sensortower.com/press/press-release-sensor-tower-acquires-appmagic-adding-dedicated-smb-solution-to-comprehensive-suite-of-digital-intelligence | 맥락 정보(시장 분석 도구 업계 동향), 화면 정보 없음 → 분류에 쓰지 않음 |

## 집계

- 열람: 25건 (모두 GitHub 공개 저장소 문서 · 예제). 이 중 화면 구성 정보가 있어 분류에 쓴 것 22건.
- 검색 결과만: 55건. 이 중 분류에 쓴 것 52건(S23은 O25와 중복, S44 · S55는 화면 정보 부족으로 제외).
- `taxonomy.json`에 넣은 대시보드: 74개 (열람 22 + 검색 결과만 52; 같은 제품의 여러 페이지는 하나로 합친 경우가 있다).

## 조사의 한계

- 상용 BI · 앱 분석 도구(Sensor Tower, AppMagic, Tableau, Power BI 등)는 페이지를 열지 못해 검색 요약에 기대었다. 실제 화면의 배치 세부(카드 크기, 순서)는 확인하지 못했고, `taxonomy.json`의 분류 값은 검색 요약에 적힌 기능에서 추론했다. 이렇게 추론한 값은 `taxonomy.json`의 `confidence: "inferred"`로 표시했다.
- 화면 사진을 직접 보지 못했으므로 색 · 글꼴 같은 시각 스타일은 분류 축에 넣지 않았다(과제 조건과도 맞는다).
