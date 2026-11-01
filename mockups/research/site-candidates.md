# 차트봇 대시보드 재구성 참고 후보

조사일: 2026-11-01 · 대상: 이 저장소의 앱스토어 31개국 게임 차트 + Claude 주간 시장 브리핑 대시보드

## 요약

- 찾은 곳: **245곳** (열람 48 · 검색 결과만 197)
- 등급: 강력 추천 21 · 참고 69 · 부분 참고 115 · 제외 40
- 분야: 앱·게임 시장 분석 · 차트 69 · BI 갤러리 · 공개 대시보드 · 디자인 65 · 제품 분석 · AI 인사이트 62 · 다른 분야 순위 차트 49
- **열람**은 이 세션에서 페이지(또는 원문 파일)를 실제로 받아 읽은 곳이다. 작업 환경의 네트워크 정책이 github.com · raw.githubusercontent.com 밖의 사이트를 막아, 열람한 곳은 모두 GitHub에 공개된 저장소(오픈소스 도구, 예제, 데이터 · 대시보드 소스)다. 나머지는 웹 검색 결과(제목 · 주소 · 검색 엔진 요약)만 보고 판정했다.
- 접근 조건(무료 공개 · 로그인 필요 · 유료)은 열람한 페이지나 검색 결과에 근거가 있으면 그대로 적었다. 근거 없이 서비스 성격으로 짐작한 것은 JSON의 `access_basis`를 "추정(서비스 성격)"으로 표시했다(130곳). 모르면 "확인 못함".
- 일부 항목의 주소는 검색 결과에 나온 주소가 아니라 서비스 대표 주소를 적었다. 그런 항목은 근거(evidence)에 그렇게 적혀 있다(15곳).
- 등급은 분야별로 1차 판정한 뒤 한데 모아 다시 봤다. 이때 참고 → 강력 추천으로 올린 8곳은 JSON의 `grade_note`에 이유를 적었다.
- 구성요소 이름은 이 대시보드의 것: AI 시장 브리핑 · 주간 순위 · 순위 추이 · 선택 게임 순위 이력 · 관심 게임·퍼블리셔 · 시장 비교와 장르 점유 · 장르 진입 맵 · 퍼블리셔 점유 · 매출·인기 갭 · 진입·이탈·급변.

## 강력 추천 상위 20곳

| # | 이름 | 무엇이 왜 맞는가 | 맞는 구성요소 | 열람 여부 | 접근 |
|---|---|---|---|---|---|
| 1 | [AppRankNavi (tomoto0/app-ranking)](https://github.com/tomoto0/app-ranking) | 5개국 앱스토어 순위를 나란히 놓고 AI가 상위 앱 · 카테고리 · 신규 진입 · 나라 비교 해설을 붙인다. 우리 'AI 브리핑 + 다국가 주간 순위'와 가장 가까운 실제 구현(소스 열람). | AI 시장 브리핑, 주간 순위, 시장 비교와 장르 점유, 진입·이탈·급변, 관심 게임·퍼블리셔 | 열람 | 무료 공개 |
| 2 | [Netflix Top 10 (Tudum) — 나라별 주간 Top 10](https://www.netflix.com/tudum/top10) | 나라별 주간 Top 10 + 'Top 10에 머문 주 수' + 매주 고정 발행. 우리 31개국 주간 순위와 데이터 모양 · 발행 주기가 같다. | 주간 순위, 시장 비교와 장르 점유, 진입·이탈·급변, 순위 추이 | 검색 결과만 | 무료 공개 |
| 3 | [AppMagic](https://appmagic.rocks/tool-descriptions/essentials-new) | 시장 세그먼트 대시보드(선두 · 분산도 · 진입 장벽), 퍼블리셔 순위, 우리 장르 라벨의 출처. 장르 진입 맵과 퍼블리셔 점유의 직접 기준. | 장르 진입 맵, 퍼블리셔 점유, 주간 순위, 진입·이탈·급변, 시장 비교와 장르 점유 | 검색 결과만 | 확인 못함 |
| 4 | [AppTweak Top Charts](https://help.apptweak.com/en/articles/4202346-compare-different-top-charts-across-countries) | 나라별 차트 최대 9개 나란히, 상위 10 순위 이력, 높은 순위에 가중을 둔 '두 날짜 사이 상승' 정렬. 시장 비교 · 순위 추이 · 급변 지표에 바로 쓴다. | 시장 비교와 장르 점유, 순위 추이, 진입·이탈·급변, 주간 순위 | 검색 결과만 | 유료 |
| 5 | [FlixPatrol](https://flixpatrol.com/top10/) | 나라 × 플랫폼 일간 Top 10을 순위 점수로 합쳐 세계 순위를 만들고 작품별 나라 이력을 보여 준다. 다국가 종합 순위와 선택 게임 이력의 모델. | 주간 순위, 시장 비교와 장르 점유, 순위 추이, 선택 게임 순위 이력, 진입·이탈·급변 | 검색 결과만 | 무료 공개 |
| 6 | [Kworb (Spotify · Apple Music · iTunes 차트 집계)](https://kworb.net/spotify/) | 행=날짜, 열=전 세계 + 나라, 칸=순위인 곡별 이력 표. 선택 게임의 31개국 순위 이력 표로 거의 그대로 옮길 수 있다. | 선택 게임 순위 이력, 순위 추이, 시장 비교와 장르 점유, 주간 순위 | 검색 결과만 | 무료 공개 |
| 7 | [Tableau Pulse (지표 다이제스트)](https://www.salesforce.com/products/tableau-pulse/) | AI가 고른 가장 큰 변화를 다이제스트 맨 위에, 그 아래 관심 지표마다 썸네일 + 한 줄 인사이트 카드. 브리핑 헤드라인 + 관심 게임 KPI 카드 구성 그대로. | AI 시장 브리핑, 주간 순위, 진입·이탈·급변, 관심 게임·퍼블리셔 | 검색 결과만 | 로그인 필요 |
| 8 | [Steam Charts (Valve 공식 — Top Sellers · Most Played)](https://store.steampowered.com/charts/) | 게임 플랫폼의 매출 순위(나라 필터)와 이용자 순위를 두 탭으로, 줄마다 지난주 변화 · 머문 기간. 매출 · 인기 2탭과 갭 화면의 직접 모델. | 주간 순위, 매출·인기 갭, 진입·이탈·급변, 시장 비교와 장르 점유 | 검색 결과만 | 무료 공개 |
| 9 | [PocketGamer.biz 주간 글로벌 모바일 게임 차트](https://www.pocketgamer.biz/weekly-global-mobile-games-charts/) | 나라별 매출 · 무료 순위에 신규 진입 · 순위 이동 · 퍼블리셔 해설을 붙인 주간 칼럼. AI 시장 브리핑의 섹션 구성과 문장 형식의 선례. | AI 시장 브리핑, 주간 순위, 진입·이탈·급변, 퍼블리셔 점유 | 검색 결과만 | 무료 공개 |
| 10 | [Perplexity Finance (종목 페이지 · 시장 요약)](https://www.perplexity.ai/finance) | 가격 차트 위 사건 주석 + 매일 AI 서술 + 출처 단 3줄 시장 요약. 선택 게임 순위 이력에 브리핑 문장을 주석으로 꽂는 방식에 맞는다. | AI 시장 브리핑, 선택 게임 순위 이력, 순위 추이, 진입·이탈·급변 | 검색 결과만 | 무료 공개 |
| 11 | [Amazon QuickSight 경영 요약 (Amazon Q, Generative BI)](https://docs.aws.amazon.com/quick/latest/userguide/quicksight-gen-bi.html) | 요약 문장을 누르면 근거 시각화가 열린다. 브리핑 문장 → 근거 차트 연결의 가장 직접적인 사례. | AI 시장 브리핑, 진입·이탈·급변, 순위 추이 | 검색 결과만 | 유료 |
| 12 | [Power BI · Fabric Copilot 서술(Narrative with Copilot)](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-create-narrative) | 요약 속 각주가 인용한 시각화를 강조하고, 필터를 바꾸면 요약도 따라간다. 브리핑 각주와 시장 탭 전환 설계에 맞는다. | AI 시장 브리핑, 시장 비교와 장르 점유, 진입·이탈·급변 | 검색 결과만 | 유료 |
| 13 | [ThoughtSpot AI Highlights · Spotter](https://docs.thoughtspot.com/cloud/latest/liveboard-ai-highlights) | KPI 변화를 신뢰 구간으로 '예상 / 예상 밖'으로 나누고 최대 기여 요인을 붙인다. 급변 카드에 AI 해석을 묶는 방식. | 진입·이탈·급변, 순위 추이, AI 시장 브리핑 | 검색 결과만 | 로그인 필요 |
| 14 | [Apache ECharts 예제: Bump Chart (Ranking)](https://github.com/apache/echarts-examples/blob/gh-pages/public/examples/ts/bump-chart.ts) | 뒤집힌 순위 축, 선 끝 이름표, 호버 강조를 갖춘 순위 추이 차트 예제(소스 열람). 순위 추이 · 선택 게임 순위 이력 차트의 구현 기준. | 순위 추이, 선택 게임 순위 이력 | 열람 | 무료 공개 |
| 15 | [Box Office Mojo — 나라별 주말 · 주간 박스오피스](https://www.boxofficemojo.com/) | 나라마다 같은 형식의 주간 순위표(지난주 · 변화율 · 주차 · 배급사). 31개국 주간 순위표와 퍼블리셔 열 구성에 그대로 쓴다. | 주간 순위, 진입·이탈·급변, 시장 비교와 장르 점유, 선택 게임 순위 이력 | 검색 결과만 | 무료 공개 |
| 16 | [Billboard Charts (Hot 100 · Global 200 · Artist Chart History)](https://www.billboard.com/charts/) | 지난주 · 최고 순위 · 머문 주 · NEW/RE-ENTRY와 항목별 Chart History. 주간 순위표와 게임 상세 이력의 표준 표기. | 주간 순위, 선택 게임 순위 이력, 진입·이탈·급변 | 검색 결과만 | 무료 공개 |
| 17 | [Spotify Charts](https://charts.spotify.com/) | 나라별 주간 차트에 '최고 신규 진입 · 최대 상승 · 최장 유지' 헤드라인 묶음. 진입 · 이탈 · 급변 요약 카드 3종으로 옮긴다. | 주간 순위, 진입·이탈·급변, 시장 비교와 장르 점유 | 검색 결과만 | 로그인 필요 |
| 18 | [모바일인덱스 (IGAWorks) 주간 통합 매출 순위 · 리포트](https://www.mobileindex.com/) | 주간 통합 매출 순위 · 연속 1위 · 장르별 · 퍼블리셔별 매출 정리. 한국 독자에게 익숙한 지표 표현과 '추정치' 주의 문구의 기준. | 주간 순위, 퍼블리셔 점유, 시장 비교와 장르 점유, AI 시장 브리핑 | 검색 결과만 | 확인 못함 |
| 19 | [The Economist Big Mac 지수 인터랙티브](https://source.opennews.org/articles/how-we-made-new-big-mac-index-interactive/) | 왼쪽 정렬 표에서 행을 고르면 오른쪽 시계열에서 강조된다. 주간 순위표 → 선택 게임 순위 이력 연결 구조와 같다. | 주간 순위, 선택 게임 순위 이력, 시장 비교와 장르 점유 | 검색 결과만 | 확인 못함 |
| 20 | [PLAYFIELD v2 (JinCoy/mobile-game-market-research)](https://github.com/JinCoy/mobile-game-market-research) | 모바일 게임 시장 조사 대시보드(무료 · 매출 순위, 장르 비교, 관심 게임, 매출-다운로드 비교, 소스 열람). 칸 색으로 추정 · 확인 · 가정을 나누는 근거 표기가 AI 브리핑 근거 표시에 쓸 만하다. | 주간 순위, 시장 비교와 장르 점유, 관심 게임·퍼블리셔, 매출·인기 갭 | 열람 | 무료 공개 |

### 상위 20곳에서 무엇을 가져올지

**1. AppRankNavi (tomoto0/app-ranking)** (열람) — 5개국(일본·미국·영국·중국·한국) App Store 순위를 나란히 놓는 다국가 비교 화면과, 선택한 나라·카테고리·날짜의 순위를 AI가 상위 앱 경향·카테고리 동향·주목할 신규 진입·국제 비교 네 관점으로 해설하는 구성을 우리 "AI 시장 브리핑 + 주요 시장 주간 순위" 첫 화면에 그대로 대응시킬 수 있다. 앱 이름 검색으로 나라별 순위를 바로 보는 기능은 "관심 게임" 검색에 참고.  
AI · 해설을 지표와 묶는 방식: 순위 데이터(나라·카테고리·날짜 선택)를 입력으로 OpenAI가 4개 관점의 트렌드 분석 글을 생성해 같은 화면에 붙인다(README 기준).  
근거: README: "世界5カ国（日本、アメリカ、イギリス、中国、韓国）のApp Storeランキングをリアルタイムで比較", "AIトレンド分析… 上位アプリの傾向と特徴 / カテゴリ別の市場動向 / 注目すべき新規参入アプリ / 国際比較における特徴", 매일 JST 7:00 자동 수집.

**2. Netflix Top 10 (Tudum) — 나라별 주간 Top 10** (검색 결과만) — 나라 선택 → 그 나라 주간 Top 10 표 + 'Weeks in Top 10' 열 구조를 우리 '주요 시장 주간 순위'에 그대로 차용(나라 탭 + 순위 + 머문 주 수). 전 세계 4개 목록(영어/비영어 × 영화/TV)을 매주 화요일 발행하는 '발행 주기 + 지난 주 넘기기'는 주간 브리핑 보관 화면에, 국가별 TSV 내려받기는 데이터 공개 방식에 참고  
AI · 해설을 지표와 묶는 방식: 없음(편집 기사 Tudum과 별도 페이지로 연결되는 정도로 보임 — 확인 못함)  
근거: 검색 결과: top10.netflix.com 국가 페이지에 'Weeks in Top 10' 필드, 매주 화요일 4개 글로벌 목록, 국가별 TSV 제공

**3. AppMagic** (검색 결과만) — "Market Segment Dashboard"(장르 동향 비교·선두 식별·분산도와 진입 장벽 평가)는 우리 "장르 진입 맵"의 축(경쟁 강도 대 보상) 설계에, 앱과 퍼블리셔를 함께 매기는 순위와 "Top Trending"·"Top Soft Launches" 목록은 "퍼블리셔 점유"와 "진입·급변"에, 최대 100개 앱·퍼블리셔 비교 대시보드는 관심 게임 비교에 참고. 사람이 직접 붙인 장르·세팅·아트 태그는 우리 장르 분류(AppMagic 라벨)와 같은 계열이라 용어를 맞추기 쉽다.  
AI · 해설을 지표와 묶는 방식: 없음(사람이 붙인 장르 태그가 해석의 기반)  
근거: 검색 요약: 매출·무료 차트 + Top Trending·Top Soft Launches, Market Segment Dashboard "compare genre dynamics, identify market leaders, and assess fragmentation and entry barriers", 상위 차트 신규 앱 수동 태깅(500+ 태그), 최대 100개 비교. 우리 저장소도 AppMagic 장르 라벨을 쓴다(genre_appmagic.py).

**4. AppTweak Top Charts** (검색 결과만) — "My Top Charts"에서 나라·스토어·카테고리·유형(무료/매출)별 차트를 최대 9개 나란히 두는 화면은 우리 31개국·5대 시장 비교에, 그래프 아이콘의 "Top Chart Trends"(차트 상위 10의 순위 이력)는 "순위 추이"에, 두 날짜 사이 상승폭으로 정렬하되 높은 순위의 상승에 가중을 주는 정렬은 "급변" 지표 계산식에 바로 참고할 수 있다. 시계 아이콘의 과거 날짜 차트(Top 200)는 주간 순위 아카이브에 대응.  
AI · 해설을 지표와 묶는 방식: 없음  
근거: 검색 요약: 최대 9개 커스텀 차트(나라·카테고리·유형), Top Chart Trends(상위 10 순위 이력), Top Chart History(과거 날짜 Top 200), 두 날짜 순위로 성장 계산(높은 순위 가중), 7일 무료 체험으로 과거 데이터 열람.

**5. FlixPatrol** (검색 결과만) — 나라 × 플랫폼별 일별 Top 10을 모아 순위 점수(1위=10점…10위=1점)를 합산해 '전 세계' 순위를 만드는 방식을, 우리 31개국 순위를 합친 '다국가 종합 순위'·장르 점유 계산에 차용. 작품 페이지의 나라별 순위 이력은 '선택 게임 순위 이력'의 나라별 칸 배치에 참고  
AI · 해설을 지표와 묶는 방식: 없음  
근거: 검색 결과: FAQ에 순위별 점수(10~1점) 합산, 국가별 Top 10과 작품별 이력, 아카이브·API는 유료(월 $49)

**6. Kworb (Spotify · Apple Music · iTunes 차트 집계)** (검색 결과만) — 곡 한 개 페이지가 '행=날짜/주, 열=Global+나라별, 칸=순위(스트림 수)'인 표 — 우리 '선택 게임 순위 이력'을 31개국 열 × 주간 행 표(칸=순위, 색=등락)로 만드는 데 거의 그대로 차용 가능. 일간/주간·순위/수치 전환 버튼도 참고  
AI · 해설을 지표와 묶는 방식: 없음  
근거: 검색 결과: 곡별 Spotify Chart History 페이지에 Global + 나라별 열, Weekly/Daily, Positions/Streams/Both 전환

**7. Tableau Pulse (지표 다이제스트)** (검색 결과만) — 다이제스트 화면: 맨 위 'AI가 고른 가장 큰 변화' 요약 → 아래 팔로우한 지표마다 썸네일 차트 + 한 줄 인사이트 + 상세 링크 + 후속 질문 칩. 우리 AI 시장 브리핑 상단(전 시장 헤드라인)과 그 아래 '관심 게임 · 시장' KPI 카드(카드마다 브리핑 한 줄)로 그대로 옮길 수 있다. 주간 메일 · 슬랙 발송 형식도 우리 주간 브리핑 발행에 맞음.  
AI · 해설을 지표와 묶는 방식: 여러 지표를 가로질러 가장 큰 변화만 AI가 요약해 맨 위에 두고, 지표 카드마다 그 지표 전용 인사이트 문장을 붙임. 후속 질문을 클릭 가능한 질문으로 제시.  
근거: Tableau 도움말·O'Reilly 장: 다이제스트 = 지표별 요약 시각화 + 상위 인사이트 글 + 상세 링크 + 후속 질문, 여러 지표 팔로우 시 맨 위 AI 요약

**8. Steam Charts (Valve 공식 — Top Sellers · Most Played)** (검색 결과만) — 매출 기준 Top Sellers(나라 필터, 주간)와 동접 기준 Most Played를 같은 허브의 두 탭으로 두고, 줄마다 '지난주 대비 순위 변화 · 차트에 머문 기간'을 붙이는 구조 — 우리 매출 순위/인기 순위 2탭 + 지난주 변화 + 머문 주 수와 거의 같은 데이터 모양. 두 탭을 나란히 놓으면 '매출·인기 갭' 화면이 됨  
AI · 해설을 지표와 묶는 방식: 없음  
근거: 검색 결과: 2022년 9월 출시, Top 100 매출 순위(지역 필터, 전주 대비 순위 변화 · 차트 기간 표시), Most Played Top 100, 국가별 top sellers

**9. PocketGamer.biz 주간 글로벌 모바일 게임 차트** (검색 결과만) — 나라별(미국·영국·중국) 무료·매출 순위 + 기간 머리말 + 신규 진입·순위 이동·퍼블리셔 성과 해설(예: 한 퍼블리셔가 상위 5 중 4자리) 구성은 우리 다국가 주간 브리핑의 섹션 순서와 "퍼블리셔가 상위 N 중 몇 자리" 지표에 참고. 다만 2019~2020년 글 위주.  
AI · 해설을 지표와 묶는 방식: 기자 해설(AI 아님)  
근거: 검색 요약: Sensor Tower 데이터, "Rankings from August 12th to 18th" 머리말, "Tencent picked up six spots… four of them in the top five".

**10. Perplexity Finance (종목 페이지 · 시장 요약)** (검색 결과만) — 종목 페이지: 추세 차트 + 핵심 지표 + 매일 쓰는 AI 서술, 차트 위에 촉매(공시 · 등급 변경)를 표시한 주석 차트, 시장 요약 3줄 + 하단 인용 출처. 우리 '선택 게임 순위 이력'에 브리핑 언급 · 업데이트 날짜를 주석으로 찍고, '전 시장 3줄 요약 + 출처 목록'을 AI 브리핑 머리에 쓰는 데 직접 참고.  
AI · 해설을 지표와 묶는 방식: 차트에 사건 주석을 겹치고, 시장 요약 3줄 아래 인용 출처를 나열. 종목별 일일 서술.  
근거: 리뷰·기사: 티커 검색 시 작은 차트 + 핵심 지표, 무료 등급에 촉매 주석 차트, 3줄 시장 요약과 하단 출처

**11. Amazon QuickSight 경영 요약 (Amazon Q, Generative BI)** (검색 결과만) — 대시보드 경영 요약(Executive summary): 주요 인사이트와 기간 대비 변화를 글로 요약하고, 요약 문장을 누르면 그 문장의 근거 시각화가 열린다. 우리 브리핑 문장 → 해당 순위 추이 · 급변 차트로 이동하는 '문장-근거 연결'에 그대로 참고. 데이터 스토리는 주간 브리핑 아카이브 형식에 참고.  
AI · 해설을 지표와 묶는 방식: 요약 문장마다 출처 시각화에 링크(문장 클릭 → 근거 차트). 기간 대비 변화 중심.  
근거: AWS 문서·블로그: Reader Pro/Author Pro가 Build 메뉴로 경영 요약 생성, 요약 문장 클릭 시 해당 시각화로 이동

**12. Power BI · Fabric Copilot 서술(Narrative with Copilot)** (검색 결과만) — 페이지 위 서술 시각화 + 각주: 요약 문장 끝 각주를 누르면 그 문장이 가리키는 시각화가 강조된다. 우리 AI 시장 브리핑의 근거 표기(문장마다 [순위표] [장르 점유] 각주 → 해당 카드 하이라이트)로 옮기기 좋다. 필터 · 슬라이서를 따라 요약이 바뀌는 점은 시장 탭 전환 시 브리핑 교체와 같은 구조.  
AI · 해설을 지표와 묶는 방식: 보이는 시각화 데이터만 요약, 각주로 근거 시각화 강조, 필터를 따름(교차 강조는 미반영), 갱신 필요 표시.  
근거: Microsoft Learn: 각주를 선택하면 요약이 참조한 시각화를 Power BI가 강조; 페이지 · 보고서 · 선택 시각화 범위 요약

**13. ThoughtSpot AI Highlights · Spotter** (검색 결과만) — Liveboard AI Highlights: KPI 변화를 신뢰 구간으로 '예상된 변화 / 예상 밖 변화'로 나누고 최대 기여 요인을 붙인다. 우리 급변 카드에 '예상 밖' 라벨과 기여 요인(장르 · 시장) 한 줄을 붙이는 방식으로 참고. KPI 관심 목록(watchlist)은 관심 게임 목록에 대응.  
AI · 해설을 지표와 묶는 방식: 이상 탐지 신뢰 구간으로 변화 분류 + 변화 분석 엔진의 기여 요인 서술 + 차트로 대화 시작.  
근거: ThoughtSpot 문서: 앞 5개 시계열 KPI, 신뢰 구간 밖이면 예상 밖, SpotIQ 변화 분석으로 최대 기여 요인

**14. Apache ECharts 예제: Bump Chart (Ranking)** (열람) — y축을 뒤집은(inverse) 순위 선 + 선 끝 이름표(endLabel) + 마우스를 올린 선만 강조(emphasis focus) 구성을 '순위 추이'의 주간 평균 순위 선 그래프와 '선택 게임 순위 이력'에 그대로 옮긴다.  
AI · 해설을 지표와 묶는 방식: 없음  
근거: 예제 원문(bump-chart.ts)에서 inverse·endLabel·emphasis 설정 확인

**15. Box Office Mojo — 나라별 주말 · 주간 박스오피스** (검색 결과만) — 나라(area) 코드별 같은 형식 순위표: Rank · LW · 전주 대비 % · 상영관 · 상영관 변화 · 누적 · 상영 주차 · 배급사 열을 우리 주간 순위 표의 열 구성(지난주 · 변화 · 머문 주 · 퍼블리셔)에 차용. 작품별 주차 표는 게임 순위 이력에 참고  
AI · 해설을 지표와 묶는 방식: 없음  
근거: 검색 결과: weekend/{주차}/?area=GB 형식 나라별 페이지, Rank·LW·%±LW·Theaters·Weeks·Distributor 열

**16. Billboard Charts (Hot 100 · Global 200 · Artist Chart History)** (검색 결과만) — 순위 줄마다 지난주 · 최고 순위 · 차트 주 수 · NEW/RE-ENTRY 표기, 아티스트 'Chart History' 페이지(피크 위치·피크 날짜·차트 주 수)를 우리 주간 순위 표와 게임 상세의 '최고 순위 · 머문 주 수 · 재진입' 표기에 차용(견본 09에서 이미 시험)  
AI · 해설을 지표와 묶는 방식: 차트 옆 'Chart Beat' 기사로 해설을 따로 붙임(같은 화면 결합은 확인 못함)  
근거: 검색 결과: Hot 100 Peak Position · Peak Date · Weeks On Chart 형식, Artist 100 등 아티스트별 Chart History

**17. Spotify Charts** (검색 결과만) — 차트 화면의 'Highest new entries · Biggest gainers · Longest streaks' 같은 헤드라인 묶음을 우리 '진입 · 이탈 · 급변' 요약 카드 3종(신규 최고 진입, 최대 상승, 최장 유지)에 차용. 나라 선택 + 주간 Top 50/200 구조는 주간 순위에 참고  
AI · 해설을 지표와 묶는 방식: 없음  
근거: 검색 결과: 헤드라인 보기에 최고 신규 진입·최대 상승·최장 유지, 익명 접근은 Global Weekly만 가능하다는 제3자 설명

**18. 모바일인덱스 (IGAWorks) 주간 통합 매출 순위 · 리포트** (검색 결과만) — 구글플레이·앱스토어·원스토어 3사 합산 "주간 통합 매출 순위"와 몇 주 연속 1위인지를 언론이 인용하는 구조는 우리 주간 순위 KPI(연속 1위 주)에, 연말 리포트의 장르별 매출 분석·퍼블리셔 매출 순위·"추정치 차이 가능" 주석은 장르 점유와 퍼블리셔 점유 화면, 데이터 주의 문구에 참고.  
AI · 해설을 지표와 묶는 방식: 없음(리포트는 사람이 쓴 해설)  
근거: 검색 요약: 주간 통합 매출 순위 매주 발표(예: "5주 연속 1위"), 게임어워즈 리포트에 평균 MAU·누적 매출·장르별 매출 분석, "추정치가 반영돼 있으며 실제 수치… 차이가 있을 수 있다". (주소는 서비스 대표 주소로 적었고, 검색 결과에서 그대로 본 주소는 아님)

**19. The Economist Big Mac 지수 인터랙티브** (검색 결과만) — 왼쪽 정렬 가능한 표에서 항목(통화)을 고르면 오른쪽 시계열에서 그 항목이 강조되는 구조를 '주간 순위 표 → 선택 게임 순위 이력' 연결과 나라 고르기에 그대로 쓴다.  
AI · 해설을 지표와 묶는 방식: 없음  
근거: 검색 요약: 지도 대신 왼쪽 정렬 표 + 오른쪽 시계열 강조로 재설계, 비교·탐색 중심 대시보드

**20. PLAYFIELD v2 (JinCoy/mobile-game-market-research)** (열람) — Top 10/20/100·스토어·무료/매출·장르 필터, 스토어 간 장르 비교, 최대 6개 게임 비교, 관심 게임 보존, 그리고 칸 색으로 "추정·판독값 / 확인됨 / 분석자 가정"을 구분하는 근거 표기는 우리 대시보드의 데이터 신뢰 표시와 매출-다운로드 비교 화면에 참고.  
AI · 해설을 지표와 묶는 방식: 없음(전략 분석 글은 원자료 시트와 연결해 근거 행까지 추적)  
근거: README: "Top 10 / 20 / 100 목록… 무료·매출 순위, 장르", "최대 6개 게임 비교, 관심 게임", "노란 칸 = 추정·판독값·확인 필요, 초록 칸 = 확인됨, 파란 글씨 = 분석자 입력·가정값", "매출-다운로드 비교 172개 게임".

## 나머지 후보 전체

등급 · 분야 순. 각 줄의 "참고할 점"은 상대 화면의 무엇을 이 대시보드의 어느 구성요소에 쓸지다.

### 강력 추천 (1)

#### 앱·게임 시장 분석 · 차트 (1)

| 이름 | 종류 | 맞는 구성요소 | 참고할 점 | AI · 해설 결합 | 열람 | 접근 |
|---|---|---|---|---|---|---|
| [app-chart-rank-tracker (PeekPanda 기반)](https://github.com/fdarkaou/app-chart-rank-tracker) | 오픈소스 순위 추적 도구 | 관심 게임·퍼블리셔, 선택 게임 순위 이력, 진입·이탈·급변 | 관심 앱마다 "최신 순위 · 전일 대비 · 7일 변화 · 최고 · 최저 · 처음 잡힌 날 · 빠진 날 수"를 한 줄로 두는 표와 "N계단 이상 움직인 앱만" 알림 옵션은 우리 관심 게임 표의 열 구성과 급변 알림 기준에 바로 참고. | 없음 | 열람 | 무료 공개 |

### 참고 (69)

#### 앱·게임 시장 분석 · 차트 (19)

| 이름 | 종류 | 맞는 구성요소 | 참고할 점 | AI · 해설 결합 | 열람 | 접근 |
|---|---|---|---|---|---|---|
| [4Gamer「スマホゲームのセルラン分析」](https://www.4gamer.net/games/633/G063395/20260427006/) | 게임 매체 주간 연재(일본) | AI 시장 브리핑, 주간 순위, 진입·이탈·급변 | Sensor Tower 데이터로 매주 일본 국내 수익 순위를 정리하며 "전주 10위 → 1위" 같은 순위 이동과 "최근 늘 Top5" 같은 지속성 평가를 붙이는 형식은 우리 일본 시장 주간 브리핑의 문장 형식과 "지속 상승·연속 상위" 표현에 참고. "App Store·Google Play만, PC/콘솔 제외" 같은 범위 주석도. | 기자가 쓴 주간 해설(AI 아님)이 순위표와 함께 실린다. | 검색 결과만 | 무료 공개 |
| [Appfigures Top Charts · Store Performance](https://appfigures.com/products/store-performance) | 앱 시장 분석 도구(순위) | 주간 순위, 관심 게임·퍼블리셔, 시장 비교와 장르 점유 | 나라·카테고리를 한 번에 건너뛰며 목록을 나란히 비교하고, 특정 앱을 "watch"해 두는 흐름은 우리 "관심 게임" 목록과 시장 간 비교 화면에, 매시간 순위의 증감·이력 표기는 순위표 증감 칸에 참고. | 없음 | 검색 결과만 | 로그인 필요 |
| [FoxData Top Charts (최근 7일 모니터)](https://foxdata.com/en/blogs/how-to-use-top-charts-to-discover-mobile-app-market-opportunities-and-optimize-your-app) | 앱 시장 분석 도구(순위) | 진입·이탈·급변, 순위 추이, 주간 순위 | "Last 7 Days Charts Monitor"의 "New" 표시(지난 1주 높은 순위에 새로 든 앱)와 "Competitive Trend"(긴 기간 상위 10 추적)는 우리 주간 순위표의 NEW 배지와 상위 10 추이 그래프에 참고. | 없음 | 검색 결과만 | 확인 못함 |
| [FoxData 주간 리포트 · 월간 전 세계 매출 상위](https://foxdata.com/cn/blogs/foxdata-weekly-report-clash-royale-leads-ios-rpgs-power-revenue-growth/) | 시장 데이터 블로그(주간) | AI 시장 브리핑, 주간 순위, 진입·이탈·급변 | "2주 연속 1위", "매출 1위 복귀" 같은 연속·복귀 표현을 헤드라인으로 쓰는 주간 리포트 형식은 우리 브리핑 헤드라인과 "연속 1위 주 수" KPI 문구에 참고. | 사람이 쓴 주간 해설(AI 여부 확인 못함) | 검색 결과만 | 무료 공개 |
| [GameAnalytics MarketIQ Store Intelligence](https://docs.gameanalytics.com/products-and-features/marketIQ/store-intelligence) | 게임 시장 분석 도구 | 관심 게임·퍼블리셔, 진입·이탈·급변, 주간 순위 | 상위 차트·뜨는 게임·최근 출시·소프트런칭과 "좋아하는 타이틀·스튜디오 추적"을 한 도구에 묶은 구성은 우리 "관심 게임과 퍼블리셔" 저장 + 신규 진입 목록 묶음에 참고. | 없음 | 검색 결과만 | 로그인 필요 |
| [Ludo.ai Market Trends · Top Charts Blender](https://ludo.ai/features/top-charts) | 게임 기획 AI 도구(시장 동향) | 장르 진입 맵, 주간 순위, AI 시장 브리핑 | AI가 비슷한 게임을 묶은 "Game Topics"를 "Top-200에 든 게임 수가 많은 순"·"독특함" 순으로 정렬하는 화면은 우리 장르 진입 맵에서 장르 칸의 크기(상위 진입 수)와 희소성을 함께 보여 주는 정렬에 참고. 위쪽 출처·장르·지역 필터는 시장 필터 배치에. | AI가 차트 게임들을 주제(Game Topic)로 묶고, 묶음마다 상위 차트 진입 수로 정렬해 해석과 지표를 결합한다. | 검색 결과만 | 확인 못함 |
| [Sensor Tower Category Rankings 모듈](https://sensortower.com/blog/new-and-improved-sensor-towers-category-rankings-module) | 앱 시장 분석 도구(순위 이력) | 선택 게임 순위 이력, 순위 추이, 시장 비교와 장르 점유 | 앱 하나의 모든 카테고리 순위를 한 화면에 모으고, 카테고리를 고르면 순위 이력 그래프에 업데이트 시점(초록 + 표시)을 겹치는 방식은 "선택 게임 순위 이력"에서 게임 업데이트일(우리 데이터의 updated 필드)과 순위 변화를 겹쳐 보여 주는 데 참고. Multi-Country View는 나라별 순위 비교 칸에. | 없음(업데이트 표시를 그래프에 겹쳐 맥락을 줌) | 검색 결과만 | 확인 못함 |
| [Tech Dev Notes 앱 Insights 페이지](https://techdevnotes.com/apps/ios/1640745955/insights) | 앱 순위 추적 사이트 | 선택 게임 순위 이력, 진입·이탈·급변, AI 시장 브리핑 | 앱마다 자동 계산한 한 줄 인사이트(미국 순위·리뷰 변화)를 30일 스파크라인·7일 변화·같은 카테고리 비교와 함께 두고, "이 숫자는 우리 추적값으로 계산했다"고 밝히는 방식은 우리 게임 상세 창의 자동 요약 문장 + 근거 숫자 + 계산 출처 표기에 참고. | 자동 계산된 인사이트 문장(규칙 기반으로 보임)이 스파크라인·7일 델타와 같은 카드에 묶이고, 계산 주체를 명시한다. | 검색 결과만 | 무료 공개 |
| [AppBrain 개발사 차트 집계](https://www.appbrain.com/dev/RobTop+Games/) | 앱 순위 사이트(Android) | 퍼블리셔 점유, 관심 게임·퍼블리셔 | 개발사 페이지에서 그 회사 앱들의 나라별 순위를 Top 10 / Top 100 / Top 500 구간으로 세어 "Top 10 28곳"처럼 보여 주는 방식은 우리 "퍼블리셔별 차트 점유"를 31개국 구간별 진입 수로 요약하는 KPI에 그대로 참고(xmarket_lite로 계산 가능). "Recent Ranking Changes"는 퍼블리셔 상세의 변동 목록에. | 없음 | 검색 결과만 | 무료 공개 |
| [AppTweak Publisher Insights](https://www.apptweak.com/en/market-intelligence/publisher-insights) | 앱 시장 분석 도구(퍼블리셔) | 퍼블리셔 점유, 시장 비교와 장르 점유 | 나라·카테고리별 상위 10개 퍼블리셔가 시장의 몇 %를 차지하는지 보여 주는 화면은 우리 "퍼블리셔별 차트 점유"(나라 파일의 publishers 목록)를 나라별 상위 10 점유 막대로 그리는 데 참고. 게임 카테고리·하위 세그먼트 필터도 같은 구조. | 없음 | 검색 결과만 | 유료 |
| [gamebiz App Store 세일즈 랭킹 1주 돌아보기](https://gamebiz.jp/news/371557) | 게임 매체 주간 기사(일본) | 주간 순위, AI 시장 브리핑 | 한 주 동안 각 게임이 1위를 며칠 했는지(예: 4일·2일·1일)로 정리하는 방식은 우리 일간 데이터(daily)로 "주간 1위 일수" KPI를 만들고 브리핑 첫 줄로 쓰는 데 참고. | 기자 해설(AI 아님) | 검색 결과만 | 무료 공개 |
| [GameDev Reports × AppMagic 월간 상위 게임](https://gamedevreports.substack.com/p/appmagic-top-mobile-games-by-revenue-7d7) | 게임 업계 뉴스레터(월간) | AI 시장 브리핑, 주간 순위 | "헤드라인 한 줄 + 방법론 주석(수수료·세금 제외, 중국 안드로이드 제외) + 매출 섹션 + 다운로드 섹션 + 신규 진입" 고정 틀은 우리 브리핑에 매출 순위/인기 순위 두 섹션과 계산 주석을 고정 배치하는 데 참고. | 사람이 쓴 요약(AI 아님) | 검색 결과만 | 무료 공개 |
| [GameDiscoverCo 뉴스레터 · Steam Hype 차트](https://newsletter.gamediscover.co/p/video-game-charts-a-series-of-lenses) | 게임 업계 뉴스레터 | AI 시장 브리핑, 진입·이탈·급변 | "차트는 렌즈"라는 관점(같은 데이터라도 차트 정의가 보이는 것을 바꾼다)은 우리 매출 순위 대 인기 순위 갭 화면의 해설 문구에, 출시 전 관심도 차트 + 주간 해설 뉴스레터 결합은 브리핑과 지표 연결 방식에 참고. | 사람이 쓴 해설이 차트 데이터를 읽어 준다(AI 아님). | 검색 결과만 | 무료 공개 |
| [GameRefinery (Liftoff) 월간 시장 리뷰](https://www.gamedeveloper.com/press-release/gamerefinery-a-liftoff-company-mobile-game-market-review-march-2024) | 게임 시장 분석(월간 리뷰) | AI 시장 브리핑, 시장 비교와 장르 점유 | 미국·중국·일본 시장을 나눠 월간으로 해설하는 리뷰 형식(시장별 섹션 + 장르·기능 관점)은 우리 다국가 브리핑의 "시장별 차이" 섹션 구성에 참고. | 분석가가 쓴 월간 해설(AI 아님) | 검색 결과만 | 유료 |
| [Global EdTech App Category Trends (basakbozkurt/dashboard)](https://github.com/basakbozkurt/dashboard) | 오픈소스 순위 기반 카테고리 추이 대시보드 | 시장 비교와 장르 점유, 순위 추이 | 순위 목록을 Borda 점수로 모아 카테고리 구성의 시간 변화(누적 막대)와 나라별 카테고리 추이를 보여 주고, 집계 방법(Borda·평균·중앙값)을 바꿔 비교하는 화면은 우리 "순위 가중 추정 점유"(genre_matrix rev)의 계산 가정을 화면에서 바꿔 보게 하는 아이디어에 참고. 미분류 비율 탐색기도 장르 미상 처리 표시에. | 없음 | 열람 | 무료 공개 |
| [MobileAction Top Charts · Biggest Movers](https://www.mobileaction.co/aso-tools/discover-market-leaders/) | 앱 시장 분석 도구(ASO) | 진입·이탈·급변, 주간 순위 | "Biggest Movers / Biggest Losers" 목록과 최신 무료·유료 앱 차트는 우리 "급변"(급상승·급하락)과 "진입" 목록을 순위표 옆 두 칸으로 나누는 배치에 참고. | 없음 | 검색 결과만 | 로그인 필요 |
| [Sensor Tower Game Intelligence (Game IQ)](https://sensortower.com/ko/product/game-intelligence) | 게임 시장 분석 도구(장르) | 시장 비교와 장르 점유, 장르 진입 맵 | 하위 장르·테마·아트·BM 축으로 나눈 장르 대시보드는 장르 점유 화면에서 장르를 상위/하위 두 단계로 펼치는 방식(우리 genre·sub 필드)에 참고. | 없음 | 검색 결과만 | 유료 |
| [Sensor Tower 월간 전 세계 매출 상위 게임 글](https://sensortower.com/blog/top-mobile-games-by-worldwide-revenue-june-2021) | 시장 데이터 블로그(월간) | AI 시장 브리핑, 주간 순위 | 순위표 이미지를 먼저 두고 그 아래 1위 게임·매출·나라 구성 해설, 방법론 한 줄, 전월·다음 달 링크를 두는 형식은 우리 브리핑의 "순위 → 해설 → 데이터 출처 → 지난 회차" 배치에 참고. | 사람이 쓴 해설이 순위표 이미지 아래 붙는다(AI 아님). | 검색 결과만 | 무료 공개 |
| [Video Game Insights (VG Insights)](https://vginsights.com) | 게임 시장 분석 도구(Steam) | 장르 진입 맵, 시장 비교와 장르 점유 | 장르·하위 장르 수준의 성과·판매·"공급과 수요"를 함께 보는 Genre Analytics는 우리 장르 진입 맵의 두 축(게임 수 점유=공급, 매출 가중 점유=수요/보상)을 설명하는 틀로 참고. | 없음 | 검색 결과만 | 확인 못함 |

#### BI 갤러리 · 공개 대시보드 · 디자인 (18)

| 이름 | 종류 | 맞는 구성요소 | 참고할 점 | AI · 해설 결합 | 열람 | 접근 |
|---|---|---|---|---|---|---|
| [Apache ECharts 예제 갤러리](https://echarts.apache.org/examples) | 차트 갤러리 | 순위 추이, 시장 비교와 장르 점유, 장르 진입 맵 | Bump Chart(순위 추이), Treemap(장르 점유), 이산 색 Heatmap(장르×시장 진입 맵) 예제를 각각 해당 구성요소의 시각화 후보로. | 없음 | 검색 결과만 | 무료 공개 |
| [Dashboard Design Patterns](https://github.com/dashboarddesignpatterns/dashboarddesignpatterns.github.io) | 대시보드 디자인 패턴 연구 | 주간 순위, 진입·이탈·급변, AI 시장 브리핑 | Thresholds·Trend-arrows·Annotations·Filtered 같은 구성 패턴과 화면 구성 패턴을 KPI·급변 표시·브리핑 주석 설계 점검표로. | Annotations(작성자가 변화 지점에 덧붙이는 설명) 패턴 | 열람 | 무료 공개 |
| [FT 시각 어휘(Visual Vocabulary)](https://github.com/Financial-Times/chart-doctor/blob/main/visual-vocabulary/README.md) | 차트 선택 가이드 | 순위 추이, 시장 비교와 장르 점유, 매출·인기 갭 | '순위(Ranking)'·'변화(Change over time)'·'상관(Correlation)' 분류로 구성요소마다 차트 형식을 고르는 기준표 — 매출·인기 갭은 산점도/기울기, 순위 추이는 범프 차트 등. | 없음 | 열람 | 무료 공개 |
| [Observable Framework 예제](https://github.com/observablehq/framework/tree/main/examples) | 오픈소스 대시보드 예제 | 주간 순위, 시장 비교와 장르 점유, AI 시장 브리핑 | KPI 카드 줄+이동평균 선(plot), 세그먼트 선택이 제목 문장까지 바꾸는 방식(hotel-bookings), 차트 아래 설명 메모(api)를 각각 KPI 줄·시장 탭·브리핑 근거 메모에. | 차트마다 아래 짧은 설명 메모, 선택에 따라 제목 문장 변경 | 열람 | 무료 공개 |
| [Our World in Data 데이터 인사이트·핵심 인사이트](https://ourworldindata.org/) | 데이터 저널리즘 사이트 | AI 시장 브리핑, 순위 추이, 시장 비교와 장르 점유 | '결론을 담은 제목 + 차트 + 짧은 글' 구성을 AI 브리핑 문장마다 근거 차트를 붙이는 카드로, 주제 페이지 맨 위 핵심 인사이트를 브리핑 요약 띠로. | 사람이 쓴 결론 문장을 차트 제목으로 써 문장과 차트를 한 몸으로 묶음 | 검색 결과만 | 무료 공개 |
| [AppRankly](https://github.com/zmsp/AppRankly) | 오픈소스 앱 분석 대시보드 | 순위 추이, AI 시장 브리핑 | 추세 위에 메모(캠페인·기능 추가)와 출시(업데이트) 표시를 겹치는 방식을 '선택 게임 순위 이력'의 업데이트일·브리핑 언급 표시에. | AI로 리뷰·키워드를 요약하고, 앱별 메모를 데이터 추세 위에 인라인으로 저장 | 열람 | 무료 공개 |
| [Big Book of Dashboards(6장 Ranking by Now, Comparing with Then)](https://oreilly.com/library/view/the-big-book/9781119282716) | 대시보드 사례집(책) | 주간 순위, 순위 추이 | '지금 순위 + 과거와 비교' 장의 사례를 주간 순위 표(이번 주·지난주·변동) 설계에. | 없음 | 검색 결과만 | 유료 |
| [Datawrapper 표 속 미니 차트](https://www.datawrapper.de/academy/how-to-add-bar-charts-line-charts-to-tables) | 차트 도구 문서 | 주간 순위, 순위 추이 | 표의 연속 열을 작은 선으로 바꾸고 모든 칸의 y축을 맞추는 설정을 '주간 순위' 표의 8주 미니 순위선에. | 없음 | 검색 결과만 | 무료 공개 |
| [Evidence](https://github.com/evidence-dev/evidence) | 코드형 BI(마크다운+SQL) | AI 시장 브리핑, 주간 순위 | 마크다운 글 속에 숫자(Value)·BigValue(비교+스파크라인)를 끼우는 보고서 방식 — AI 브리핑 문장 안 숫자를 실제 데이터 값으로 바인딩하는 화면에. | 글 안에 데이터 값을 인라인으로 삽입(Value 컴포넌트), BigValue로 헤드라인 숫자 | 열람 | 무료 공개 |
| [FT 코로나·백신 트래커](https://www.ft.com/) | 데이터 저널리즘 트래커 | 시장 비교와 장르 점유, 순위 추이 | 나라별 추이를 같은 축으로 겹치고 강조색 하나로 한 나라를 띄우는 트래커 페이지 방식을 31개국 시장 비교 선에. | 기자가 매일 차트를 갱신하며 해설을 덧붙이는 트래커 형식(검색 요약) | 검색 결과만 | 유료 |
| [Gapminder Tools (Ranks · Trends · Bubbles)](https://www.gapminder.org/tools/) | 공개 데이터 탐색 도구 | 순위 추이, 시장 비교와 장르 점유 | Ranks 도구(상위·하위 나라와 시간에 따른 순위 변화)를 '시장 비교'에서 나라별 장르 점유 순위 변화로, Trends의 나라 여럿 겹친 선을 시장 비교 선으로. | 없음 | 검색 결과만 | 무료 공개 |
| [Geckoboard 리더보드 위젯](https://support.geckoboard.com/en/articles/6055782-guide-to-the-leaderboard-visualization) | KPI 대시보드 도구 문서 | 주간 순위, 진입·이탈·급변 | 화살표로 오른 항목·내린 항목을 바로 보이고, 주간·월간·범주별로 자르는 리더보드를 '주간 순위'와 급변 표시에. | 없음 | 검색 결과만 | 로그인 필요 |
| [IMF DataMapper](https://www.imf.org/external/datamapper/) | 공공 데이터 포털 | 시장 비교와 장르 점유, 순위 추이 | 지도 · 시계열 선 · 순위표를 한 화면에서 같은 지표로 전환하는 구성을 31개국 '시장 비교'(나라별 1위 장르, 점유)에 참고, 화면 상태를 주소로 공유하는 방식도. | 없음 | 검색 결과만 | 무료 공개 |
| [Metabase](https://github.com/metabase/metabase) | 오픈소스 BI | AI 시장 브리핑, 주간 순위 | KPI 격자/큰 차트+KPI 섹션 틀, Trend 카드(최대 3개 비교), Documents(글+차트) — AI 브리핑 문서형 화면과 KPI 줄에. | Metabot이 차트를 분석하고 Documents에서 글과 차트를 섞음(앞 조사에서 문서 열람) | 열람 | 무료 공개 |
| [AI UX Playground 패턴](https://www.aiuxplayground.com/patterns) | AI UX 패턴 갤러리 | AI 시장 브리핑 | 인용(citations)·신뢰도(confidence)·사람 검토 같은 신뢰 패턴을 브리핑 문장의 근거·확실성 표시에. | 인용·신뢰도 표시 패턴 | 검색 결과만 | 무료 공개 |
| [FT 영국 경제 대시보드(2015)](https://www.niemanlab.org/2015/07/the-financial-times-built-a-handy-dashboard-that-gives-you-a-snapshot-of-the-u-k-economy/) | 데이터 저널리즘 대시보드 | AI 시장 브리핑 | 지표가 자동 갱신되고 각 지표 옆에 원자료와 관련 기사 링크를 다는 방식을 브리핑 문장 ↔ 근거 지표 ↔ 외부 기사 링크 연결에. | 지표마다 해당 FT 기사 링크를 붙여 해설과 숫자를 연결 | 검색 결과만 | 확인 못함 |
| [Our World in Data Data Explorer](https://ourworldindata.org/explorers) | 데이터 탐색기 | 시장 비교와 장르 점유 | 나라 선택(지역 집계 포함)을 유지한 채 선·막대·기울기 차트·지도·표 보기를 바꾸는 방식을 '시장 비교와 장르 점유'의 보기 전환에. | 없음 | 검색 결과만 | 무료 공개 |
| [Shape of AI (AI UX 패턴 목록)](https://www.shapeof.ai) | AI UX 패턴 갤러리 | AI 시장 브리핑 | AI임을 알리는 표지(identifiers)·근거로 안내(wayfinders) 패턴을 'Claude 작성' 표시와 근거 링크 설계에. | AI 존재 표시·출처 안내 패턴(검색 요약) | 검색 결과만 | 무료 공개 |

#### 제품 분석 · AI 인사이트 (20)

| 이름 | 종류 | 맞는 구성요소 | 참고할 점 | AI · 해설 결합 | 열람 | 접근 |
|---|---|---|---|---|---|---|
| [Domo 경영 성과 브리핑 에이전트](https://domo-webflow.domo.com/ai/agents/executive-performance-briefing-ai-agent) | BI · KPI 옆 생성 서술 | AI 시장 브리핑, 주간 순위, 진입·이탈·급변 | 생성 서술을 해당 차트 · KPI 카드 바로 옆에 두어 별도 보고서로 갈 필요 없게 함. 우리 시장 카드 옆에 그 시장 브리핑 문단을 붙이는 배치 참고. | KPI 카드와 서술을 한 앱에 나란히, 주석 대시보드. | 검색 결과만 | 로그인 필요 |
| [Metabase Research · Metabot](https://github.com/metabase/metabase/blob/master/docs/ai/research.md) | BI(오픈소스) · AI 조사 · 채팅 | AI 시장 브리핑, 순위 추이, 시장 비교와 장르 점유 | Research: 질문 → 차트 여러 개를 흥미도 순으로 생성, 사이드바 맨 위 Summary에 메모와 차트를 모음, 데이터 점에서 '더 탐색'. 우리 브리핑 아래 '근거 차트 묶음'을 흥미도 순으로 깔고 요약 칸에 핵심 차트를 고정하는 구성 참고. | 흥미도 정렬 + 요약 영역에 차트 고정 + 차트별 댓글. | 열람 | 무료 공개 |
| [OpenBB Workspace 에이전트(위젯 데이터 인용)](https://github.com/OpenBB-finance/agents-for-openbb) | 금융 워크스페이스 · AI 에이전트 예제 | AI 시장 브리핑, 주간 순위, 순위 추이 | 에이전트가 워크스페이스 위젯 데이터를 읽고 인용(citations)을 단 답과 차트를 낸다. 우리 브리핑 문장이 대시보드 위젯(순위표 · 장르 점유)을 인용 각주로 가리키는 구조의 구현 예로 참고. | 위젯 원자료를 읽어 답하고 위젯 인용을 붙임, 추론 단계 표시. | 열람 | 무료 공개 |
| [PostHog 웹 분석 · 대시보드 · PostHog AI](https://github.com/PostHog/posthog.com/blob/master/contents/docs/web-analytics/dashboard.mdx) | 제품 분석(오픈소스) | 주간 순위, 진입·이탈·급변, AI 시장 브리핑 | 맨 위 방문자 · 조회 · 세션 지표와 이전 기간 비교, 경로 표를 누르면 대시보드 전체 필터, 오른쪽 AI 사이드패널, 빈 대시보드의 AI 시작 질문. 우리 상단 KPI 줄(이전 주 대비) + 순위표 행 클릭 → 화면 전체가 그 게임으로 걸러지는 상호작용 참고. | AI는 사이드패널에서 인사이트를 만들어 대시보드에 추가; 지표 자체에는 서술 없음. | 열람 | 무료 공개 |
| [Sisense Narratives · KPI Card](https://docs.sisense.com/main/SisenseLinux/sisense-narratives.htm) | BI · 위젯별 AI 서술 | AI 시장 브리핑, 순위 추이, 주간 순위 | 위젯마다 서술 토글 → 그 위젯의 핵심을 요약하는 패널. KPI Card 플러그인은 여러 지표 + 추세 + 스파크라인을 한 카드에. 우리 순위표 · 추이 차트마다 '해설 펼치기' 토글을 두는 데 참고. | 위젯 단위 서술 패널(토글). | 검색 결과만 | 로그인 필요 |
| [Tellius 자동 인사이트(추세 요인)](https://www.tellius.com/product/auto-insights) | AI 분석 · 변화 요인 순위 | 진입·이탈·급변, 시장 비교와 장르 점유, 장르 진입 맵 | KPI 변화의 요인을 유의성으로 순위화하고 자연어 요약 + 시각화 + 통계 + 세그먼트로 보여 줌. 우리 '장르 점유 변화'를 장르 · 시장별 기여로 쪼개 폭포/막대로 보여 주는 데 참고. | 요인 순위 + 자연어 요약 + 근거 통계. | 검색 결과만 | 로그인 필요 |
| [Zoho Analytics Zia Insights](https://www.zoho.com/analytics/help/zia/zia-insights-dashboard.html) | BI · 대시보드 인사이트 패널 | AI 시장 브리핑, 진입·이탈·급변, 시장 비교와 장르 점유 | 오른쪽 위 버튼으로 대시보드 전체 인사이트 패널, 구성요소마다 Zia 아이콘, 패널 안 '글 보기 / 차트 보기' 전환. 우리 AI 브리핑 패널에 '글 / 근거 차트' 토글을 두고, 카드마다 AI 아이콘으로 그 카드 해설만 여는 구조 참고. | 대시보드 전체 + 구성요소별 진입점, 같은 인사이트를 글과 차트 두 보기로. | 검색 결과만 | 로그인 필요 |
| [Amplitude Dashboard Agent](https://amplitude.com/docs/agents/dashboard-agent) | 제품 분석 · 대시보드 반복 분석 에이전트 | AI 시장 브리핑, 진입·이탈·급변 | 기존 대시보드 차트들을 분석해 추세 · 이상 · 차트 간 상관을 찾아 우선순위 인사이트와 권고를 반복 생성. 우리 주간 브리핑의 '핵심 시사점'(권고)과 '눈여겨볼 게임'을 대시보드 차트와 연결하는 모델. | 대시보드 단위 반복 분석, 우선순위 + 권고. | 검색 결과만 | 로그인 필요 |
| [Bloomberg AI 뉴스 요약 · Company News 요약](https://www.bloomberg.com/company/press/bloomberg-launches-gen-ai-summarization-for-news-content) | 금융 터미널 · AI 요약 | AI 시장 브리핑, 선택 게임 순위 이력 | 기사 맨 위 AI 3줄 요약, 기업 뉴스(CN)의 시간순 요약. 우리 브리핑 섹션 머리 3줄과 '게임별 AI 언급 연표'(선택 게임 순위 이력 옆)에 참고. | 글 맨 위 3줄, 시간 도장 붙은 요약, 전문가 평가. | 검색 결과만 | 유료 |
| [Databox AI Summary](https://help.databox.com/understanding-the-ai-summary-visualization) | KPI 대시보드 · AI 요약 블록 | AI 시장 브리핑, 주간 순위 | AI 요약이 KPI 격자 안의 블록 하나로 들어간다(자동 갱신 · 편집 가능 · 길이 선택). 우리 KPI 줄 옆에 'Claude 한 줄' 블록을 같은 크기 카드로 끼우는 배치 참고. | 대시보드 블록형 요약, 자동 갱신, 사후 편집. | 검색 결과만 | 로그인 필요 |
| [Datadog 대시보드 이상 탐지 · Watchdog](https://docs.datadoghq.com/dashboards/graph_insights/investigate_anomalies/) | 관측 · 대시보드 이상 이슈 | 진입·이탈·급변, 순위 추이 | 여러 위젯에서 동시에 일어난 이상을 '이슈' 하나로 묶고 기여 태그를 붙이며, 이슈를 누르면 해당 위젯으로 스크롤. 우리 '여러 시장 동시 급상승'(예: 한 게임이 5개 시장 동시 ▲)을 이슈 카드 하나로 묶고 누르면 시장별 순위 추이로 이동하는 방식에 참고. | 동시 이상 묶음 + 기여 태그 + 위젯 스크롤. | 검색 결과만 | 로그인 필요 |
| [Google Analytics 4 홈 인사이트 카드](https://support.google.com/analytics/answer/10388660?hl=en) | 제품 · 웹 분석 · 자동 인사이트 카드 | 진입·이탈·급변, AI 시장 브리핑 | 홈의 인사이트 카드(자동 생성 + 맞춤 조건), '모든 인사이트 보기', 상호작용으로 카드 순서 조정, 기여도 분석. 우리 '진입 · 이탈 · 급변'을 카드 피드로 만들고 사용자가 고정한 조건(예: 관심 게임 10계단 이상 변동)을 맞춤 인사이트로 두는 데 참고. | 이상 변화를 카드 한 장 = 발견 하나로, 상세는 기여도 분석으로 연결. | 검색 결과만 | 로그인 필요 |
| [Google Finance (AI 리서치판)](https://blog.google/products/search/new-google-finance-ai-deep-search/) | 금융 · AI 리서치 + 차트 | AI 시장 브리핑, 순위 추이 | 종목 · 시장 질문에 AI 답 + 근거 링크, 고급 차트 · 실적 실시간. 우리 '브리핑에 묻기'(질문 → 브리핑 문장 + 링크) 화면과 순위 추이 차트를 한 화면에 두는 구성 참고. | 질문 답에 출처 링크, 차트와 같은 화면. | 검색 결과만 | 무료 공개 |
| [Metabase Documents](https://github.com/metabase/metabase/blob/master/docs/documents/introduction.md) | BI(오픈소스) · 글+차트 문서 | AI 시장 브리핑, 순위 추이 | 글 사이에 차트를 넣고 차트 옆 보조 글을 다는 문서. 우리 주간 브리핑을 글 흐름 사이에 해당 순위 차트를 끼운 '주간 호'로 내는 데 참고. | 문서 안 차트 삽입, 차트 옆 보조 글, AI 호출. | 열람 | 무료 공개 |
| [Plausible Analytics](https://github.com/plausible/analytics) | 웹 분석(오픈소스) | 주간 순위, 진입·이탈·급변 | 핵심 지표를 한 페이지에, 주간 · 월간 메일 리포트에 급등 · 급락 알림. 우리 주간 브리핑 메일 + '이번 주 급등 · 급락' 알림 형식 참고. | AI 없음, 정기 리포트 + 급변 알림으로 해석을 대신. | 열람 | 무료 공개 |
| [Seeking Alpha 분석 페이지 AI 핵심 요약 · 퀀트 등급](https://seekingalpha.com/article/4754392-redesigned-analysis-page-with-ai-insights) | 금융 · AI 요약 + 요인 등급 | AI 시장 브리핑, 관심 게임·퍼블리셔 | 분석 글마다 AI 핵심 요약(전문 보기 링크), 종목마다 가치 · 성장 · 수익성 · 모멘텀 요인 등급. 우리 관심 게임 카드에 '브리핑 요약 + 요인 칩(순위 · 추세 · 시장 수 · 매출/인기 갭)'을 함께 두는 데 참고. | 글 요약은 원문 링크와 함께, 정량 등급은 별도 칩. | 검색 결과만 | 유료 |
| [Sigma Computing 'Explain this chart'](https://help.sigmacomputing.com/docs/explain-visualizations-with-ai) | BI · 차트별 AI 설명 | 순위 추이, 시장 비교와 장르 점유 | 차트 메뉴 → 차트 이미지 + 기반 데이터로 핵심 · 관찰 · 분포 설명을 실시간 생성, 피드백 버튼. 우리 각 차트(순위 추이 · 장르 점유)에 '이 차트 해설' 메뉴를 두고, 미리 쓴 브리핑 문장 중 관련 것을 보여 주는 방식으로 참고. | 차트 단위 설명 모달 + 피드백. | 검색 결과만 | 로그인 필요 |
| [Stripe 대시보드 홈](https://docs.stripe.com/dashboard/basics) | 결제 · 홈 지표 | 주간 순위, 진입·이탈·급변 | 핵심 숫자 몇 개 + 스파크라인 + 기간 비교 + 처리할 알림. 우리 상단 KPI 줄을 5개 이하로 줄이고 숫자 아래 스파크라인을 두는 데 참고. | 없음(알림만). | 검색 결과만 | 로그인 필요 |
| [Tableau Dashboard Narratives (Tableau Agent)](https://help.tableau.com/current/pro/desktop/en-us/dashboard-narratives.htm) | BI · 대시보드 요약 + 차트별 인사이트 | AI 시장 브리핑, 시장 비교와 장르 점유 | 대시보드 전체 요약 + 차트별 인사이트를 함께 생성, 작성자가 대상 워크시트를 제한. 우리 브리핑을 '전체 요약 + 구성요소별 한 줄(순위표 · 장르 점유 · 갭)'로 나눌 때 참고. | 전체 요약과 차트별 인사이트 2층 구조, 데이터 갱신 시 재생성. | 검색 결과만 | 로그인 필요 |
| [Looker 대시보드 요약 (Conversational Analytics)](https://docs.cloud.google.com/looker/docs/conversational-analytics-looker-data-agents-dashboards) | BI · 대시보드 맨 위 AI 요약 | AI 시장 브리핑 | 대시보드 대화를 열면 맨 위에 '무엇을 보여 주는지 · 핵심 하이라이트 · 의미' 3단 요약. 우리 브리핑 머리말을 '이 화면이 다루는 것 / 이번 주 핵심 / 시사점' 3단으로 짜는 데 참고. 예약 발송에 요약 포함은 주간 발행에 대응. | 대시보드 상단 3단 요약 + 대시보드와 채팅. | 검색 결과만 | 로그인 필요 |

#### 다른 분야 순위 차트 (12)

| 이름 | 종류 | 맞는 구성요소 | 참고할 점 | AI · 해설 결합 | 열람 | 접근 |
|---|---|---|---|---|---|---|
| [FIFA 남자 세계 랭킹](https://inside.fifa.com/fifa-world-ranking/men) | 국가대표 세계 순위(월별) | 주간 순위, 순위 추이, 시장 비교와 장르 점유, 진입·이탈·급변, AI 시장 브리핑 | 순위표의 '이전 순위 · 순위 변동 · 이전 점수 · 점수 변화' 열과 대륙연맹 필터, 발표마다 '가장 많이 오른 팀' 해설 기사를 함께 내는 형식을 우리 주간 순위(이전 순위 · 변동 · 권역 필터) + 급상승 해설에 참고 | 발표 때마다 '가장 큰 상승' 등 변동 해설 기사(별도 글) | 검색 결과만 | 무료 공개 |
| [FiveThirtyEight — Global Club Soccer Rankings · NBA Elo (데이터 저장소)](https://github.com/fivethirtyeight/data/tree/master/soccer-spi) | 스포츠 순위 모델 + 공개 데이터 | 순위 추이, 선택 게임 순위 이력, 시장 비교와 장르 점유, AI 시장 브리핑 | 전 세계 클럽 SPI 순위(리그 열 + 현재 순위 + 이전 순위)와 경기별 등급 추이 파일 구성을 우리 '다국가 종합 순위 + 지난 순위' 표와 데이터 공개 방식(최신 파일 + 전체 이력 파일 분리)에 참고. 방법론 글을 별도로 두는 방식은 브리핑 계산식 공개에 참고 | 기사(해설)와 인터랙티브 순위를 같은 사이트에서 연결(대시보드 안 결합은 확인 못함) | 열람 | 무료 공개 |
| [JustWatch Streaming Charts · 시장 점유 리포트](https://www.justwatch.com/us/streaming-charts) | OTT 인기 순위 + 분기 점유 리포트 | 주간 순위, 퍼블리셔 점유, 시장 비교와 장르 점유, AI 시장 브리핑 | 15개국 일·주·월 Top 10 차트와 '플랫폼별 점유(%p 증감)' 분기 리포트를 함께 내는 구조를, 우리 순위 화면 + 퍼블리셔 점유 변화(분기 %p) + 사람이 쓴 분기 해설 묶음에 참고 | 분기 리포트에서 점유 수치 + 증감 해설을 글로 발표(대시보드 안 결합은 확인 못함) | 검색 결과만 | 무료 공개 |
| [SteamDB Charts](https://steamdb.info/charts/) | 게임 플랫폼 비공식 통계(동접·최고치) | 주간 순위, 순위 추이, 선택 게임 순위 이력, 진입·이탈·급변 | 현재 동접 순위 + 24시간 최고 + 역대 최고, 게임별 장기 추이 그래프를 '선택 게임 순위 이력'의 최고치 · 장기 그래프 표기에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [CoinMarketCap](https://coinmarketcap.com/) | 가상자산 순위(시가총액) | 주간 순위, 진입·이탈·급변, 퍼블리셔 점유 | 맨 위 시장 요약 띠(전체 규모 · 1·2위 점유율 'dominance') + 기간별(1h/24h/7d/30d) 상승·하락 상위 + 'Trending' 목록 구조를 우리 화면 맨 위 KPI 띠(상위 퍼블리셔 점유) + 급상승/급하락 상위 목록에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [Google Trends](https://trends.google.com/trends/explore) | 검색 관심도 비교(나라·지역) | 시장 비교와 장르 점유, 순위 추이, 진입·이탈·급변 | 키워드 최대 5개 비교 시계열 + '지역별 관심도'(0~100 정규화 지도·표) + '급상승(Breakout)' 관련 검색어 구조를 우리 장르·게임의 나라별 비교(정규화 막대)와 급상승 표시에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [Hanteo Chart (한터차트)](https://www.hanteochart.com/) | K-pop 판매 집계(실시간 · 주간 · 나라별) | 주간 순위, 시장 비교와 장르 점유, AI 시장 브리핑 | 같은 K-pop 판매를 '나라별 차트 TOP 30(미국 · 일본 · 중국)'으로 나눠 매주 발표하고 자체 뉴스(한터뉴스)가 순위를 해설하는 구조 — 우리 나라별 주간 순위 + 주간 해설 묶음과 데이터 모양이 비슷 | 자체 뉴스 사이트가 순위 발표를 기사로 해설(편집 결합) | 검색 결과만 | 무료 공개 |
| [Kworb iTunes · Apple Music 전 세계 차트 / 아티스트별 나라 목록](https://kworb.net/itunes/) | 음악 다국가 종합 차트 | 시장 비교와 장르 점유, 선택 게임 순위 이력, 관심 게임·퍼블리셔 | 곡 · 앨범이 '지금 몇 개 나라에서 몇 위인지'를 나라 행으로 한눈에 나열하는 아티스트 페이지를, 우리 '게임 한 개가 31개국 중 어디에서 몇 위인지'(xmarket) 칸 표 + 퍼블리셔별 게임 묶음에 차용. 나라 순위를 점수로 합친 전 세계 차트는 다국가 종합 순위에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [Opta Analyst Power Rankings](https://theanalyst.com/articles/power-rankings-your-club-ranked/) | 스포츠 전 세계 클럽 순위(0~100 점수) | 시장 비교와 장르 점유, AI 시장 브리핑, 순위 추이 | 전 세계 1만여 팀을 0~100 점수 하나로 줄 세우고 리그 평균으로 '가장 강한 리그' 순위를 따로 내는 구조 — 우리 게임 순위를 장르 · 시장 단위 평균으로 묶어 '가장 경쟁이 센 장르/시장' 순위를 만드는 데 참고. 순위표 + 해설 기사를 한 글에 묶는 형식은 브리핑에 참고 | 기사 본문에 순위표를 넣고 그 아래 해설(편집 기사형 결합) | 검색 결과만 | 무료 공개 |
| [Similarweb Top Websites Ranking](https://www.similarweb.com/top-websites/) | 웹사이트 순위(나라 × 카테고리) | 주간 순위, 시장 비교와 장르 점유, 진입·이탈·급변 | 나라 × 카테고리 조합으로 같은 순위표(순위 · 카테고리 · 순위 변화)를 바꿔 보는 필터 구조를 우리 '나라 × 장르' 순위 필터에 참고 | 없음 | 검색 결과만 | 로그인 필요 |
| [Finviz Map (트리맵)](https://finviz.com/map.ashx) | 주식 시장 트리맵 | 시장 비교와 장르 점유, 퍼블리셔 점유 | 섹터 → 산업 → 종목 계층 트리맵(면적=시가총액, 색=등락)을 '장르 → 하위 장르 → 게임'(면적=순위 가중 매출 점유, 색=주간 순위 변동) 지도에 차용(견본 10에서 장르 단위로 시험) | 없음 | 검색 결과만 | 무료 공개 |
| [The Numbers — Market Charts (배급사 · 장르 점유)](https://www.the-numbers.com/market/) | 영화 시장 점유 통계(연간) | 퍼블리셔 점유, 시장 비교와 장르 점유 | 연도별 '배급사 점유'·'장르 점유' 표(순위, 작품 수, 매출, 점유율)를 우리 '퍼블리셔별 차트 점유'와 '장르 점유' 표의 열 구성(게임 수 · 순위 가중 점유 · 점유율)에 차용 | 없음 | 검색 결과만 | 무료 공개 |

### 부분 참고 (115)

#### 앱·게임 시장 분석 · 차트 (28)

| 이름 | 종류 | 맞는 구성요소 | 참고할 점 | AI · 해설 결합 | 열람 | 접근 |
|---|---|---|---|---|---|---|
| [Appark.ai](https://appark.ai/en/guide) | 앱 시장 분석 도구 | 주간 순위, 퍼블리셔 점유, 관심 게임·퍼블리셔 | 다운로드/매출 순위 전환과 퍼블리셔 순위, 게임 팀용 모니터링 목록은 부분 참고. AI 분석 주장은 구체 화면이 확인되지 않음. | "AI powered analysis"라는 제3자 소개뿐, 화면 확인 못함 | 검색 결과만 | 확인 못함 |
| [app-analytics-dash (VizViper)](https://github.com/VizViper/app-analytics-dash) | 오픈소스 앱 순위 대시보드 | 퍼블리셔 점유, 순위 추이 | 플랫폼·퍼블리셔 드롭다운으로 그 퍼블리셔 앱 전체의 순위 추이를 한 그래프에 그리는 화면은 "퍼블리셔 상세" 추이 그래프에 부분 참고. | 없음 | 열람 | 무료 공개 |
| [Apple App Store 공식 Top Charts](https://apps.apple.com/) | 플랫폼 공식 차트 | 주간 순위, 매출·인기 갭 | 우리 데이터의 원천. 무료(다운로드)와 매출 차트가 서로 다른 것을 잰다는 점(한 분석: 미국 매출 상위 20 중 14개가 무료 상위 50에 없음)은 매출·인기 갭 화면 해설 근거로만 참고. | 없음 | 검색 결과만 | 무료 공개 |
| [Apptica Top Charts · Top History](https://apptica.com/blog/introducing-top-apps/) | 앱 시장 분석 도구 | 선택 게임 순위 이력, 진입·이탈·급변 | 앱 프로필의 "Top History" 순위 이력 + 비슷한 앱 묶음, Trending Apps 섹션은 게임 상세 창 구성에 부분 참고. | 없음 | 검색 결과만 | 확인 못함 |
| [Apptopia](https://apptopia.com/) | 앱 시장 분석 도구 | 퍼블리셔 점유, 시장 비교와 장르 점유 | Market Explorer와 340여 분류 태그(X-Ray Intelligence)는 장르 세분화 아이디어 정도로만 참고. | 없음 | 검색 결과만 | 유료 |
| [i-boss 월간 모바일 게임 인기·매출 정리 (모바일인덱스 데이터)](https://www.i-boss.co.kr/ab-3208-1801) | 마케팅 커뮤니티 월간 정리 글(한국) | AI 시장 브리핑, 주간 순위 | 월간 매출 1위와 "네 단계 상승" 같은 순위 이동, 인기(이용자) 순위를 한 글에 나란히 두는 형식은 매출 대 인기 비교 문단에 부분 참고. | 사람이 쓴 정리(AI 아님) | 검색 결과만 | 무료 공개 |
| [Liquid & Grit](https://www.liquidandgrit.com/) | 게임 시장 리서치(구독) | AI 시장 브리핑, 시장 비교와 장르 점유 | 매출 상위 게임의 수익 요인을 장르(캐주얼·코어·카지노)별 월간 리포트로 나누는 방식은 장르별 브리핑 묶음에 부분 참고. | 분석가 리포트(AI 아님) | 검색 결과만 | 유료 |
| [Newzoo 상위 20 게임(매출·MAU)](https://newzoo.com/) | 게임 시장 리서치 | 주간 순위, AI 시장 브리핑 | "이번 달 매출 상위 20에 신작 6개, MAU 차트는 정체" 같은 매출 순위 대 이용자 순위 대비 해설은 매출·인기 갭 브리핑 문장에 부분 참고. | 분석가 해설(AI 아님) | 검색 결과만 | 유료 |
| [Roblox Charts · RoMonitor Stats](https://www.roblox.com/charts/top-playing-now) | 플랫폼 공식 차트·통계 | 주간 순위, 순위 추이 | 동시 접속(CCU) 실시간 순위와 RoMonitor의 장기 이력·마일스톤 표기는 순위 이력의 "기록 경신" 표시에 부분 참고. | 없음 | 검색 결과만 | 무료 공개 |
| [Similarweb App Top Charts · Rankings](https://support.similarweb.com/hc/en-us/articles/27737321931677-Using-App-Top-Charts) | 웹·앱 분석 도구 | 주간 순위, 선택 게임 순위 이력 | 오른쪽 위 날짜·나라 선택 + 무료/유료/매출 전환, 앱 클릭 시 분석 모듈로 이동하는 흐름은 순위표 → 게임 상세 연결에 부분 참고. | 없음 | 검색 결과만 | 유료 |
| [SteamPulse (Girard-Labs)](https://github.com/Girard-Labs/SteamPulse) | 오픈소스 Steam 동접 대시보드 | 진입·이탈·급변, 주간 순위 | 주간 순위 이동·모멘텀 배지와 동접·24시간 최고·역대 최고 표기는 순위표 배지 디자인에 부분 참고. | 없음 | 열람 | 무료 공개 |
| [TapTap 排行榜](https://www.taptap.cn/) | 게임 플랫폼 순위(중국) | 진입·이탈·급변, 주간 순위 | 热门榜·热玩榜·新品榜·预约榜·热卖榜·独家榜 + 장르별 17개 보드로 나누는 구조는 우리 "진입"(신규) 목록을 별도 보드로 떼는 분류에 부분 참고. | 없음 | 검색 결과만 | 확인 못함 |
| [七麦数据 (Qimai)](https://www.qimai.cn/) | 앱 시장 분석 도구(중국) | 주간 순위, 시장 비교와 장르 점유 | 중국 App Store 순위 원천 후보. 화면 구성은 확인하지 못해 부분 참고로만 둔다. | 없음 | 검색 결과만 | 확인 못함 |
| [게임트릭스 (PC방 점유율)](https://www.gametrics.com/) | PC방 게임 점유율 순위(한국) | 주간 순위, 시장 비교와 장르 점유 | 순위를 "점유율 %"로 표기하는 방식은 우리 순위 가중 점유 표기에 부분 참고. 데이터 종류(PC방 이용시간)는 다르다. | 없음 | 검색 결과만 | 확인 못함 |
| [42matters 국가별 매출 상위 게임](https://42matters.com/top-grossing-mobile-games-us) | 앱 순위 공개 페이지 | 주간 순위 | 나라별로 같은 틀의 공개 순위 페이지를 만든 구성은 우리 나라별 정적 페이지(공유용) 아이디어에 부분 참고. | 없음 | 검색 결과만 | 무료 공개 |
| [App Ape (일본)](https://ja.appa.pe/) | 앱 이용 분석 도구(일본) | 주간 순위 | MAU·실행 횟수·이용 시간 기준 순위는 데이터가 달라 "급성장 앱" 순위 구성 정도만 부분 참고. | 없음 | 검색 결과만 | 확인 못함 |
| [Deconstructor of Fun · Terminal](https://www.deconstructoroffun.com/terminal) | 게임 분석 매체·도구 | AI 시장 브리핑 | 게임 분석 글과 시장 데이터를 묶어 경영진 질문에 답하게 하겠다는 Terminal 구상은 "브리핑에 묻기"류 기능의 방향 참고. 라이브 데이터 연동은 "예정" 상태. | 분석 콘텐츠 + (예정) 라이브 시장 데이터로 요청형 답변 | 검색 결과만 | 확인 못함 |
| [Esports Charts · Esports Map](https://escharts.com/) | e스포츠 시청 통계 | 시장 비교와 장르 점유 | 나라·게임·지역별 최고 시청 기록을 히트맵과 시간축으로 보여 주는 지도는 31개국 지도 시각화 아이디어에 부분 참고. | 없음 | 검색 결과만 | 확인 못함 |
| [Fortnite.gg 플레이어 수](https://fortnite.gg/) | 게임 통계 사이트 | 선택 게임 순위 이력 | 맵 페이지의 현재·24시간 최고·역대 최고 3단 숫자는 게임 상세의 "현재 순위·19주 최고·역대" KPI 묶음에 부분 참고. | 없음 | 검색 결과만 | 무료 공개 |
| [Gamalytic](https://gamalytic.com/) | Steam 매출 추정 도구 | 시장 비교와 장르 점유 | 추정 정확도를 "77%가 오차 30% 안"처럼 공개하는 방식은 우리 추정 점유의 신뢰 범위 표기에 부분 참고. | 없음 | 검색 결과만 | 확인 못함 |
| [Google Play 공식 Top charts](https://play.google.com/store/games) | 플랫폼 공식 차트 | 주간 순위 | 안드로이드 차트 원천. 화면 구성 참고점은 적다. | 없음 | 검색 결과만 | 무료 공개 |
| [RoWatcher](https://www.rowatcher.com/) | Roblox 게임 분석 | 주간 순위 | 전체 동접과 추적 중인 경험 수를 맨 위 KPI로 두는 배치는 "추적 나라 수·게임 수" KPI 줄에 부분 참고. | 없음 | 검색 결과만 | 확인 못함 |
| [SteamCharts.com](https://steamcharts.com/app/1448030) | PC 게임 접속자 추이 사이트 | 선택 게임 순위 이력 | 게임별 월간 표(평균·증감·증감%·최고)와 "최근 30일" 행은 선택 게임 순위 이력을 표로 보여 줄 때의 열 구성에 부분 참고. | 없음 | 검색 결과만 | 무료 공개 |
| [SteamSpy](https://steamspy.com/) | Steam 보유자 추정 사이트 | 시장 비교와 장르 점유 | 보유자를 범위("2,000,000 .. 5,000,000")로 표기하고 태그별 탐색을 제공하는 방식은 추정치 범위 표기에 부분 참고. | 없음 | 검색 결과만 | 확인 못함 |
| [Streams Charts 게임 · 트렌드](https://streamscharts.com/trends/games) | 스트리밍 분석 | 진입·이탈·급변 | "빠르게 성장하는 게임" 트렌드 목록은 급상승 목록 화면에 부분 참고. | 없음 | 검색 결과만 | 무료 공개 |
| [TwitchTracker 게임 순위](https://twitchtracker.com/games) | 스트리밍 시청 순위 | 주간 순위 | 최근 7일 평균 시청자·채널·시청 시간·최고 시청자 열 구성은 주간 순위 표의 보조 지표 열 배치에 부분 참고. | 없음 | 검색 결과만 | 무료 공개 |
| [Valve 무관 Steam 대시보드: steam-live-charts](https://github.com/Mocas-12/steam-live-charts) | 오픈소스 Steam 순위 대시보드 | 주간 순위 | 최다 플레이·판매·할인·신작 탭을 60초마다 갱신하는 단순 탭 구성은 순위 탭 묶음 참고 정도. | 없음 | 열람 | 무료 공개 |
| [昴 주간 세일즈 랭킹 (일본, 추정 매출)](https://www.dreamnews.jp/press/0000256854) | 공략 사이트 운영사 주간 발표 | 주간 순위 | 순위와 추정 매출을 함께 싣고 "공식 매출이 아닌 추정"임을 밝히는 방식은 우리 추정 점유 주석에 부분 참고. | 없음 | 검색 결과만 | 무료 공개 |

#### BI 갤러리 · 공개 대시보드 · 디자인 (37)

| 이름 | 종류 | 맞는 구성요소 | 참고할 점 | AI · 해설 결합 | 열람 | 접근 |
|---|---|---|---|---|---|---|
| [Apache ECharts 예제: Bar Race(나라별)](https://github.com/apache/echarts-examples/blob/gh-pages/public/examples/ts/bar-race-country.ts) | 차트 라이브러리 예제 | 주간 순위, 순위 추이 | realtimeSort로 막대 순서가 주마다 바뀌는 재생형 순위 — 19주 주간 순위를 '재생'하는 보조 화면 정도로만 참고(대시보드 본화면엔 과함). | 없음 | 열람 | 무료 공개 |
| [Apache Superset 대시보드](https://github.com/apache/superset) | 오픈소스 BI | 주간 순위, 시장 비교와 장르 점유 | Big Number with Trendline(최근 값+추세선) 카드와 네이티브 필터 바를 KPI 줄·시장 필터에. | 없음 | 열람 | 무료 공개 |
| [Grafana Play](https://play.grafana.org/) | 공개 대시보드 샌드박스 | 진입·이탈·급변, 순위 추이 | Stat 패널(값+스파크라인+임계값 색)과 State timeline을 '급변'·'지속 상승' 상태 띠에 참고, 키오스크 재생 목록은 TV형 화면에. | 없음 | 검색 결과만 | 무료 공개 |
| [Tableau Public 오늘의 시각화(VOTD)](https://public.tableau.com/app/discover/viz-of-the-day) | BI 공개 갤러리 | 주간 순위, 시장 비교와 장르 점유 | KPI 카드·랭킹형 대시보드 사례를 검색해 카드 배치 아이디어를 얻는 용도. 게임 차트 사례는 검색으로 찾지 못함. | 없음 | 검색 결과만 | 무료 공개 |
| [The Pudding 빌보드 차트 비주얼 에세이](https://pudding.cool/) | 데이터 저널리즘(음악 차트) | 순위 추이, AI 시장 브리핑 | Top 10 머문 기간을 거품 크기로, 시대별 흐름을 스크롤 이야기로 — 포트폴리오용 '주간 신문판'형 브리핑 연출에 부분 참고. | 글이 차트 사이를 이끄는 스크롤 서사 | 검색 결과만 | 무료 공개 |
| [awesome-dashboard 목록](https://github.com/obazoud/awesome-dashboard) | 대시보드 도구 목록 | 주간 순위 | 오픈소스 대시보드 도구 색인 — 추가 후보 탐색용. | 없음 | 열람 | 무료 공개 |
| [best-of-streamlit](https://github.com/jrieke/best-of-streamlit) | 앱 목록(GitHub) | 주간 순위 | 별 수 순으로 정리된 앱 목록에서 금융 차트 앱 등 순위·추이 앱을 찾는 색인. | 없음 | 열람 | 무료 공개 |
| [CDC COVE 범프 차트 안내](https://www.cdc.gov/cove/data-visualization-types/bump-chart.html) | 차트 사용 안내 | 순위 추이 | 범프 차트 = 시간에 따른 순위 변화 추적이라는 정의와 사용 지침을 순위 추이 화면 설명 문구에. | 없음 | 검색 결과만 | 무료 공개 |
| [Data Viz Project](https://datavizproject.com/) | 차트 종류 목록 | 순위 추이 | 기울기·범프 차트 등 형식 비교 — 2주 비교(기울기)와 19주 추이(범프) 선택에. | 없음 | 검색 결과만 | 무료 공개 |
| [Databox 앱 스토어 대시보드 템플릿](https://databox.com/dashboard-examples/app-store) | KPI 템플릿 | 주간 순위 | 순위·매출·리뷰·설치를 한 화면에 모은 앱 스토어 템플릿 — 단, 자기 앱 지표 중심이라 시장 순위와는 다름. | 없음 | 검색 결과만 | 로그인 필요 |
| [Datawrapper River](https://www.datawrapper.de/docs/how-to-use-the-river) | 재사용 차트 갤러리 | 순위 추이 | 다른 사용자가 공개한 차트를 골라 재사용하는 갤러리 — 기자용 차트 형식 탐색에. | 없음 | 검색 결과만 | 무료 공개 |
| [Datawrapper 블로그: 닌텐도 판매 스파크라인](https://blog.datawrapper.de/weekly-chart-nintendo-console-sales-as-sparklines) | 차트 사례 글 | 주간 순위 | 여러 항목을 스파크라인 표로 비교하고 y축을 맞추라는 원칙을 게임 순위 표에. | 없음 | 검색 결과만 | 무료 공개 |
| [Flourish 바 차트 레이스](https://flourish.studio/visualisations/bar-chart-race/) | 차트 도구 템플릿 | 순위 추이 | 타임라인 선 차트 결합·시점별 자막 기능을 '순위 추이' 재생 보조 화면에(자막=브리핑 문장). | 시점에 맞춰 자막(캡션)으로 핵심 순간 설명 | 검색 결과만 | 로그인 필요 |
| [Gapminder Vizabi / tools-page](https://github.com/Gapminder/tools-page) | 오픈소스 탐색 도구 틀 | 시장 비교와 장르 점유 | 같은 데이터 틀 위에 도구(차트 종류)만 갈아 끼우는 구조 — 견본 간 공통 데이터 계층 설계 참고. | 없음 | 열람 | 무료 공개 |
| [Hex 데이터 앱](https://hex.tech/product/data-apps/) | 노트북형 데이터 앱 | AI 시장 브리핑 | 노트북 분석을 대시보드·보고서형 앱으로 발행 — 분석 글과 차트를 함께 공개하는 형식. | 없음 | 검색 결과만 | 로그인 필요 |
| [Keen IO Dashboards 템플릿](https://github.com/keen/dashboards) | 대시보드 레이아웃 템플릿 | AI 시장 브리핑 | 차트 칸마다 '제목 + 차트 + 메모' 틀이 있는 CSS 격자 레이아웃 — 위젯별 AI 한 줄 자리 설계에. | 차트 칸마다 선택적 메모(notes) 영역 | 열람 | 무료 공개 |
| [Looker Studio 템플릿 갤러리](https://lookerstudio.google.com/navigation/templates) | BI 템플릿 갤러리 | 주간 순위 | 점수 카드 + 시계열 + 표의 기본 템플릿 배치 — 무료 포트폴리오 대시보드 구현 수단 비교용. | 없음 | 검색 결과만 | 로그인 필요 |
| [Lux](https://github.com/lux-org/lux) | 자동 시각화 추천 | AI 시장 브리핑 | 데이터프레임을 보면 차트를 자동 추천 — 브리핑 문장에 맞는 근거 차트 자동 선택 아이디어. | 데이터 특성으로 차트 자동 추천 | 열람 | 무료 공개 |
| [Mobbin(웹 대시보드 화면)](https://mobbin.com/) | UI 사례 갤러리 | 주간 순위 | 실서비스 화면 라이브러리에서 대시보드 범주를 찾아 모바일 레이아웃 참고. | 없음 | 검색 결과만 | 유료 |
| [owid-grapher 저장소](https://github.com/owid/owid-grapher) | 오픈소스 차트 도구 | 순위 추이 | 차트를 삽입 가능한 단위로 만들어 기사 · 페이지에 재사용하는 구조 참고(코드 재사용은 라이선스상 불가). | 없음 | 열람 | 무료 공개 |
| [PatternBase(AI UX React 패턴)](https://blog.stackademic.com/patternbase-54-ai-ux-patterns-for-react-developers-7a26b3707c10) | AI UX 컴포넌트 | AI 시장 브리핑 | 인용 컴포넌트 등 AI UX 패턴 구현 예 — 브리핑 인용 표시 구현에. | 인용(citations) 컴포넌트 | 검색 결과만 | 확인 못함 |
| [Perceptual Edge 대시보드 디자인 대회](https://www.perceptualedge.com/blog/?p=1308) | 대시보드 디자인 비평 | 주간 순위 | 작은 공간에 많은 지표를 담는 Few식 설계·비평을 KPI 줄 밀도 조정에. | 없음 | 검색 결과만 | 무료 공개 |
| [Plotly Dash 샘플 앱](https://github.com/plotly/dash-sample-apps) | 공개 앱 모음 | 시장 비교와 장르 점유 | 100여 개 예제 중 금융·운영 대시보드의 필터+그래프 배치 참고. | 없음 | 열람 | 무료 공개 |
| [Power BI Data Stories Gallery](https://community.fabric.microsoft.com/t5/Data-Stories-Gallery/bd-p/DataStoriesGallery) | BI 공개 갤러리 | 주간 순위 | 월간 선정작(이야기성·창의성 기준)에서 보고서형 배치 참고. 검색·정렬 기능은 약함. | 없음 | 검색 결과만 | 무료 공개 |
| [Qlik 데모 사이트·Qlik Gallery](https://explore.qlik.com/) | BI 데모 갤러리 | 시장 비교와 장르 점유 | 로그인 없이 쓰는 연관 탐색 데모 — 선택이 모든 차트를 걸러 주는 상호작용 참고. | 없음 | 검색 결과만 | 무료 공개 |
| [ReUI · Creative Tim shadcn KPI 블록](https://www.creative-tim.com/ui/block/kpi-sparkline-cards) | UI 컴포넌트 블록 | 주간 순위 | 스파크라인+증감 배지 KPI 카드(지표에 따라 색 논리 반전)를 KPI 줄 구현에. | 없음 | 검색 결과만 | 무료 공개 |
| [Reuters 데이터 섹션(자동 차트)](https://palewi.re/posts/2025/09/05/100-automated-charts-on-reuters-com/) | 데이터 저널리즘 | AI 시장 브리핑 | 자동 생성 차트 100개를 기사 흐름에 끼우는 방식 — 브리핑 문장마다 자동 차트를 붙이는 파이프라인 참고. | 자동 차트를 기사 본문에 배치 | 검색 결과만 | 무료 공개 |
| [SaaSFrame 대시보드·분석 화면 모음](https://www.saasframe.io/categories/dashboard) | UI 사례 갤러리 | 주간 순위 | 실제 SaaS 대시보드 166개·분석 화면 67개에서 KPI 카드 여백·사이드바 배치 참고. | 없음 | 검색 결과만 | 유료 |
| [Smashing(TV 대시보드)](https://github.com/Smashing/smashing) | TV 대시보드 프레임워크 | 주간 순위 | TV용 큰 숫자 위젯 격자 — 벽걸이 화면형 요약에. | 없음 | 열람 | 무료 공개 |
| [Statista 차트](https://www.statista.com/chart/26324/average-time-per-day-spent-on-mobile-games-on-android) | 통계 차트 사이트 | 시장 비교와 장르 점유 | 장르별 다운로드 같은 단일 차트 + 출처 표기 형식 — 장르 점유 차트 캡션 참고. | 없음 | 검색 결과만 | 유료 |
| [Streamlit 앱 갤러리](https://streamlit.io/gallery) | 공개 앱 갤러리 | 주간 순위 | 금융·스포츠 통계 앱 사례에서 st.metric(값+증감+미니 차트) 카드 배치 참고. | 없음 | 검색 결과만 | 무료 공개 |
| [Tableau Exchange Bump Chart 확장](https://exchange.tableau.com/products/1029) | BI 확장 | 순위 추이 | BI 도구에서도 범프 차트를 따로 확장으로 제공 — 순위 추이 시각화 선택 근거. | 없음 | 검색 결과만 | 확인 못함 |
| [Tableau Public #GamesNightViz](https://www.thedataschool.co.uk/takhmina-pirmahmadova/starte-mit-tableau-public) | 커뮤니티 프로젝트 | 관심 게임·퍼블리셔 | 게임 데이터 주제 커뮤니티 시각화 — 게임 소재 표현 아이디어 정도. | 없음 | 검색 결과만 | 무료 공개 |
| [Tableau 대시보드 예제 페이지](https://www.tableau.com/dashboard-examples) | BI 공식 예제 | 주간 순위 | 부서별 예제 묶음 — 경영 요약형 배치 참고. 공식 페이지 내용은 확인 못함. | 없음 | 검색 결과만 | 무료 공개 |
| [The Economist big-mac-data 저장소](https://github.com/TheEconomist/big-mac-data) | 공개 데이터·계산 코드 | 시장 비교와 장르 점유 | 지표 계산 방법과 원자료를 함께 공개하는 방식 — 우리 '순위 가중 추정 점유' 같은 계산식 공개 메모의 본보기. | 없음 | 열람 | 무료 공개 |
| [Tremor 대시보드 템플릿](https://github.com/tremorlabs/template-dashboard) | UI 템플릿 | 주간 순위 | SaaS 대시보드 템플릿 구성(README에 배치 설명 없음) — React 구현 시 참고. | 없음 | 열람 | 확인 못함 |
| [World Bank 세계개발지표(WDI)](https://datatopics.worldbank.org/world-development-indicators/) | 공공 데이터 포털 | 시장 비교와 장르 점유 | 여러 나라를 입력해 한 그래프에 비교, 지역 묶음(집계) 포함 — 지역(유럽·동남아) 묶음과 개별 나라를 같이 보여 주는 방식 참고. | 없음 | 검색 결과만 | 무료 공개 |

#### 제품 분석 · AI 인사이트 (26)

| 이름 | 종류 | 맞는 구성요소 | 참고할 점 | AI · 해설 결합 | 열람 | 접근 |
|---|---|---|---|---|---|---|
| [Microsoft LIDA](https://github.com/microsoft/lida) | AI 시각화 생성 라이브러리 | AI 시장 브리핑, 순위 추이 | 데이터 요약 → 목표 생성 → 시각화 생성 · 설명 · 평가 — 브리핑 문장에 맞는 근거 차트를 자동 고르는 파이프라인 아이디어(화면은 없음). | 시각화 설명 · 추천. | 열람 | 무료 공개 |
| [Narrative BI](https://narrative.bi/platform/) | AI · 예약 서술 리포트 | AI 시장 브리핑, 진입·이탈·급변 | 일 · 주 · 월 예약 서술 리포트 + 이상 알림 — 글 중심이라 시각화 참고는 적음; 주간 발행 주기 참고. | 예약 서술(텍스트 위주). | 검색 결과만 | 무료 공개 |
| [Pendo AI Insights](https://www.pendo.io/pendo-blog/introducing-pendo-insights) | 제품 분석 · AI 인사이트 | AI 시장 브리핑, 진입·이탈·급변 | 인사이트마다 근거 · AI 다음 단계 · 영향 맥락을 붙임 — 브리핑 시사점 카드에 '근거 / 다음 행동' 칸을 두는 데 참고. | 인사이트 = 근거 + 다음 단계 + 영향. | 검색 결과만 | 유료 |
| [Pyramid Analytics Smart Insights](https://community.pyramidanalytics.com/t/m1htx9z/smart-insights-on-any-data-source) | BI · AI 서술 | AI 시장 브리핑, 순위 추이 | 차트 · 대시보드 · 모델 단위 서술(파레토 · 추세 · 이상치) — 서술 범위를 차트/화면/전체로 나누는 개념 참고. | 범위별 서술. | 검색 결과만 | 로그인 필요 |
| [SAP Analytics Cloud Smart Insights](https://www.sap.com/germany/products/data-cloud/analytics-cloud-smart-insights.html) | BI · 데이터 점 설명 | 순위 추이, 진입·이탈·급변 | 데이터 점을 누르면 영향 요인을 글과 시각으로 설명 — 순위 추이 점 클릭 시 그 주 브리핑 문장 표시에 참고. | 점 클릭 → 요인 설명. | 검색 결과만 | 로그인 필요 |
| [Shopify Sidekick · Sidekick Pulse](https://www.shopify.com/nz/enterprise/blog/sidekick-ai-enterprise) | 커머스 · AI 비서 | AI 시장 브리핑, 진입·이탈·급변 | 주간 성과 요약 요청, 묻지 않아도 제안하는 Pulse — 브리핑을 '먼저 알려 주는 카드'로 홈에 두는 아이디어. | 선제 인사이트 + 대화형 요약. | 검색 결과만 | 로그인 필요 |
| [Vercel Web Analytics](https://vercel.com/docs/analytics) | 웹 분석 | 주간 순위, 퍼블리셔 점유 | 패널마다 상위 항목을 방문자 순 목록으로 — 퍼블리셔 · 장르 상위 목록 패널 배치 참고. | 없음. | 검색 결과만 | 로그인 필요 |
| [Yahoo 주식 앱(대만) 관심종목 AI 요약(계획)](https://wantrich.chinatimes.com/news/20260610900426-420101) | 금융 앱 · 관심 목록 AI 요약 | 관심 게임·퍼블리셔, AI 시장 브리핑 | 관심 종목 묶음에 AI 요약(VIP, 대만 앱 계획) — 관심 게임 목록 전체를 요약하는 카드 아이디어. 주 사이트 기능은 미확인. | 관심 목록 단위 요약. | 검색 결과만 | 유료 |
| [Yellowfin Signals · Stories](https://www.yellowfinbi.com/blog/industrys-first-automated-analysis-and-cross-vendor-storytelling) | BI · 변화 감지 + 이야기 | AI 시장 브리핑, 진입·이탈·급변 | Signals(의미 있는 변화 자동 감지)와 Stories(글+시각화)를 대시보드에 붙임 — 급변 감지와 주간 이야기 분리 구조 참고. | 신호와 이야기 분리. | 검색 결과만 | 로그인 필요 |
| [Akkio Chat Explore · Generative Reports](https://www.akkio.com/post/generative-reports-in-action) | AI BI | AI 시장 브리핑 | 채팅으로 차트를 만들어 리포트 탭에 추가 — 직접 대응 화면은 적음. | 채팅 → 리포트. | 검색 결과만 | 유료 |
| [Fathom Analytics](https://usefathom.com/docs/start/dashboard) | 웹 분석 | 주간 순위 | 단순 한 화면 지표 + 메일 리포트 — 밀도 낮은 요약 화면 참고. | 없음. | 검색 결과만 | 유료 |
| [GoodData Key Driver Analysis](https://www.gooddata.com/docs/cloud/experimental-features/key-driver-analysis) | BI · 핵심 요인 분석 | 진입·이탈·급변 | KPI에 영향이 큰 요인 순위 — 급변 설명 보조로만 참고(베타). | 요인 순위. | 검색 결과만 | 로그인 필요 |
| [Heap AI CoPilot · Illuminate](https://www.heap.io/blog/ai-copilot-announcement) | 제품 분석 · AI | AI 시장 브리핑 | 자연어 질문 → 차트 자동 선택, Illuminate 선제 알림 — 직접 맞는 화면은 적음. | 질문 → 차트. | 검색 결과만 | 유료 |
| [Hex (Notebook Agent · Chat with App)](https://learn.hex.tech/docs/getting-started/ai-overview) | 데이터 노트북 · 앱 | AI 시장 브리핑 | 게시된 앱(대시보드)에 대해 AI가 요약 · 로직 설명 · 필터 변경 — 견본 해설 기능 참고 정도. | 앱 단위 요약 채팅. | 검색 결과만 | 유료 |
| [Holistics AI 대시보드 요약](https://docs.holistics.io/release-notes/ai-dashboard-summaries) | BI · 대시보드 요약 | AI 시장 브리핑 | 대시보드 옆에 짧은 서술을 자동 생성 · 저장 — 브리핑 저장 · 버전 개념 참고. | 대시보드 옆 저장형 요약. | 검색 결과만 | 로그인 필요 |
| [Klipfolio PowerMetrics AI](https://klipfolio.com/blog/powermetrics-ai) | KPI 플랫폼 · AI | 주간 순위 | 관리되는 지표 목록 위 AI 질문 · 지표 개요 · 목표 알림 — 지표 정의 목록 화면 참고. | 지표 카탈로그 기반 답. | 검색 결과만 | 로그인 필요 |
| [Lightdash AI 에이전트](https://github.com/lightdash/lightdash) | 에이전트형 BI(오픈소스) | AI 시장 브리핑 | 답의 근거 쿼리를 열어 보고 검증된 답을 재사용 — 브리핑 문장 옆 '계산 보기'(어떤 데이터로 셌나) 링크 참고. | 검사 가능한 쿼리, 검증 답. | 열람 | 무료 공개 |
| [Linear Insights](https://linear.app/docs/insights) | 업무 도구 · 측정 × 기준 패널 | 시장 비교와 장르 점유 | 측정값 × 나누는 기준 × 세그먼트 선택 → 그래프 + 표 — 장르 점유 비교 화면의 축 선택 UI 참고. | 없음. | 검색 결과만 | 유료 |
| [Luzmo IQ](https://www.luzmo.com/iq) | 임베디드 분석 · AI 답 | AI 시장 브리핑 | 답 컴포넌트가 차트 + 글 요약을 함께, AI 경영 요약 — '브리핑에 묻기' 답 카드 형식 참고. | 차트 + 글 답 컴포넌트. | 검색 결과만 | 유료 |
| [Mixpanel Agent(구 Spark)](https://docs.mixpanel.com/docs/mixpanel-agent) | 제품 분석 · AI 에이전트 | AI 시장 브리핑 | 질문 → 차트를 보드에 저장, 보드 해석 — '브리핑에 묻기' 결과를 보드에 고정하는 흐름 참고. | 질문 결과를 보드로. | 검색 결과만 | 로그인 필요 |
| [Qlik Insight Advisor](https://help.qlik.com/en-US/cloud-services/Subsystems/Hub/Content/Sense_Hub/Insights/insight-advisor-natural-language.htm) | BI · 자연어 인사이트 | AI 시장 브리핑 | 질문 → 맞는 차트 + '추가 인사이트 보기', 대시보드용 자연어 인사이트 개체(클릭마다 갱신) — 시장 · 게임 선택 시 브리핑 문장 목록 갱신에 참고. | 선택에 따라 인사이트 목록 갱신. | 검색 결과만 | 로그인 필요 |
| [Rows AI Analyst](https://rows.com/ai) | 스프레드시트 · AI | 주간 순위 | 표마다 묻기 전에 자동 인사이트를 보여 줌 — 우리 순위표 위에 '이 표에서 볼 것' 한 줄을 미리 띄우는 아이디어. | 표 단위 선제 인사이트. | 검색 결과만 | 유료 |
| [Salesforce CRM Analytics · Einstein Discovery](https://trailhead.salesforce.com/content/learn/modules/einstein-discovery-quick-look/meet-einstein-discovery) | BI · 서술형 인사이트 | AI 시장 브리핑 | 인사이트를 서술형(무엇) · 진단형(왜) · 비교형으로 나눔 — 우리 브리핑 섹션 분류를 화면 라벨로 쓰는 데 참고. | 인사이트 유형 분류. | 검색 결과만 | 유료 |
| [Slack AI 일일 리캡](https://www.salesforce.com/news/stories/slack-ai-news-update/) | 협업 · AI 다이제스트 | AI 시장 브리핑 | 고른 채널의 아침 요약, '더 보기'로 출처 확인 — 주간 브리핑 배포 채널과 출처 열기 UX 참고. | 요약 + 출처 펼치기. | 검색 결과만 | 유료 |
| [Strategy(MicroStrategy) Auto Narratives](https://www.strategysoftware.com/strategyone/whats-new/auto-narratives-ai-powered-dashboard-summaries) | BI · 자동 서술 | AI 시장 브리핑 | 대시보드 AI 요약 기능 — 세부 화면 정보 부족, 존재 확인 수준. | 대시보드 요약. | 검색 결과만 | 로그인 필요 |
| [Umami](https://github.com/umami-software/umami) | 웹 분석(오픈소스) | 주간 순위 | 트래픽 · 캠페인 · 전환을 한곳에 — README에 화면 정보가 적어 개념 참고만. | 없음(MCP 옵션). | 열람 | 무료 공개 |

#### 다른 분야 순위 차트 (24)

| 이름 | 종류 | 맞는 구성요소 | 참고할 점 | AI · 해설 결합 | 열람 | 접근 |
|---|---|---|---|---|---|---|
| [Chartmetric](https://chartmetric.com/products/dashboard) | 음악 데이터 분석 도구 | 관심 게임·퍼블리셔, 순위 추이, 선택 게임 순위 이력 | 아티스트별로 여러 플랫폼 지표·차트 순위를 한 작업 공간에 모으는 대시보드와 자체 종합 순위(16개 플랫폼 지표)를 '관심 게임·퍼블리셔' 관찰 목록과 게임별 종합 점수에 참고 | 없음(확인 못함) | 검색 결과만 | 유료 |
| [Netflix Top 10 Power BI 대시보드 (GitHub 개인 프로젝트)](https://github.com/Filometer/Netflix-Top10-PowerBI) | 공개 데이터로 만든 BI 대시보드 | 순위 추이, 시장 비교와 장르 점유, 주간 순위 | Netflix 국가별 Top 10 공개 데이터로 '나라별 순위 · 주간 추이 · 누적 주 수 최다 · 순위 진행' 화면을 짠 구성 목록을 우리 화면 목록 점검표로 참고 | README에 'Key Insights' 목록을 사람이 정리 | 열람 | 무료 공개 |
| [Apple Music Top Charts (Daily Top 100 · City Charts)](https://music.apple.com/us/browse/top-charts) | 음악 공식 차트(약 116개국 일간) | 주간 순위, 시장 비교와 장르 점유 | 같은 형식의 Top 100 목록을 나라마다 두고 나라 선택기로 바꾸는 구조, 도시 단위 Top 25까지 내려가는 계층을 '권역 → 나라' 드릴다운에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [ATP 랭킹 (No.1 주 수 · 순위 이력)](https://www.atptour.com/en/rankings/singles) | 테니스 세계 순위(주간) | 선택 게임 순위 이력, 주간 순위 | '1위 누적 주 수 · 연속 주 수' 같은 기록 지표를 우리 '연속 1위 주 수 · 누적 1위 주 수' KPI 정의에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [Billboard Hot 100 Power BI 대시보드 (GitHub 개인 프로젝트)](https://github.com/AmalenduR841/billboard-hot-100-powerbi-dashboard) | 공개 데이터로 만든 BI 대시보드 | 선택 게임 순위 이력, 진입·이탈·급변 | 6쪽 구성(명예의 전당 · 연대별 · 아티스트 깊이 보기 · 곡 탐색 · 추세와 인사이트 · 재진입과 컴백) 중 '재진입과 컴백' 쪽을 우리 '재진입 · 지속 상승' 화면 아이디어로 참고 | 'Trends & Insights' 쪽에 사람이 쓴 해설 | 열람 | 무료 공개 |
| [ClubElo](http://clubelo.com/) | 스포츠 Elo 순위(유럽 클럽) | 순위 추이, 선택 게임 순위 이력 | 클럽별 장기 순위 이력 그래프를 게임 순위 이력 장기 그래프에 참고(검색 결과에 직접 정보 없음) | 없음 | 검색 결과만 | 확인 못함 |
| [CoinGecko](https://www.coingecko.com/) | 가상자산 순위(시가총액) | 진입·이탈·급변, 시장 비교와 장르 점유 | 상승·하락 상위를 '상위 1,000개 안에서만' 계산하는 하한 규칙과 카테고리별 시가총액 묶음을, 우리 급상승 계산의 순위 하한(예: 100위 안)과 장르 묶음 표에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [ESPN BPI / Power Rankings](https://www.espn.com/nba/bpi) | 스포츠 팀 강도 지표·파워 랭킹 | 주간 순위, AI 시장 브리핑 | 주간 파워 랭킹 기사 형식(순위 + 지난주 순위 + 팀마다 2~3줄 해설)을 '주간 순위 줄마다 AI 한 줄' 형식에 참고 | 순위 줄마다 기자의 짧은 해설(검색 결과에서는 BPI 정의만 확인) | 검색 결과만 | 무료 공개 |
| [IMDb STARmeter · MOVIEmeter](https://help.imdb.com/article/imdbpro/industry-research/faq-for-starmeter-moviemeter-and-companymeter/GSPB7HDNPKVT5VHC) | 인기 순위(주간, 조회 기반) | 주간 순위, 진입·이탈·급변 | '하위 순위일수록 변동이 크게 보인다'는 안내를 순위 변동 표기 옆에 두는 방식 — 우리 급상승 목록에 '하위권의 큰 변동은 과장될 수 있음' 주석을 붙이는 데 참고 | 도움말에 변동 해석 주의 문구 | 검색 결과만 | 유료 |
| [KOBIS 박스오피스 (영화관입장권통합전산망)](https://www.kobis.or.kr/kobis/business/stat/boxs/findDailyBoxOfficeList.do) | 국내 영화 공식 순위(일별) | 주간 순위, 진입·이탈·급변 | 일별 순위에 '신규 진입 여부(NEW/OLD)'와 '순위 증감' 필드를 표준으로 두는 점을 우리 데이터 사전(진입 · 이탈 정의)과 순위 표 표기에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [Nielsen Streaming Top 10](https://www.nielsen.com/data-center/top-10/) | 미국 스트리밍 주간 Top 10 | 주간 순위, 퍼블리셔 점유 | 플랫폼 · 작품 단위 주간 Top 10(분 단위 시청량)에 플랫폼 이름을 같이 적는 표를 '게임 + 퍼블리셔' 주간 순위 표기에 참고. 연말 'ARTEY' 연간 순위는 연간 결산 화면 아이디어 | 없음(언론이 받아 해설) | 검색 결과만 | 무료 공개 |
| [Oricon Ranking](https://www.oricon.co.jp/rank/) | 일본 음악 공식 차트(주간) | 주간 순위, 진입·이탈·급변 | 주간 판매량 + 전주 순위 + NEW/RE-ENTRY + 누적 판매 표기를 우리 주간 순위의 '재진입' 표기와 누적 지표에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [Shazam Charts (나라 · 도시)](https://www.shazam.com/charts/top-200/world) | 음악 인식 순위(약 70개 나라 · 1,500개 도시) | 시장 비교와 장르 점유, 진입·이탈·급변 | '발견(Discovery) 차트'처럼 순위 상위가 아니라 '막 뜨기 시작한 곡'을 별도 차트로 두는 개념을 우리 '급상승 · 신규 진입' 별도 목록에 참고. 나라 → 도시 계층은 권역 → 나라 계층에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [Soundcharts](https://soundcharts.com/) | 음악 데이터 분석 도구(차트 · 방송) | 진입·이탈·급변, 관심 게임·퍼블리셔 | 차트 알림(새 최고 순위, 나라 · 플랫폼 · 차트 종류로 거르기)과 주간 리포트 메일을 '관심 게임' 알림·주간 브리핑 메일 설계에 참고 | 주간 리포트 메일에 하이라이트를 모아 보냄(AI 여부 확인 못함) | 검색 결과만 | 유료 |
| [YouTube Charts](https://charts.youtube.com/) | 음악 영상 공식 차트(약 57개국 주간) | 주간 순위, 시장 비교와 장르 점유 | 같은 형식 주간 Top 목록을 나라마다 두고(일요일 갱신) 전 세계 차트와 오가는 구조를 31개국 주간 순위 탭에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [멜론 차트](https://www.melon.com/chart/) | 국내 음원 차트(실시간·일간·주간) | 주간 순위, 진입·이탈·급변 | 순위 옆 등락 화살표와 숫자, 신규(NEW) 표시를 한 줄에 압축하는 국내 사용자에게 익숙한 표기 방식을 주간 순위 줄 디자인에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [써클차트 (Circle Chart)](https://circlechart.kr/) | 국내 음악 공식 차트(주간) | 주간 순위, 진입·이탈·급변 | 주차별 종합 순위와 '신규 진입' 표기, 큰 순위 상승(예: 88위→7위)을 기사가 받아 쓰는 형식을 우리 주간 순위의 신규 진입·급상승 강조에 참고 | 없음(언론이 순위표를 받아 해설 기사로 재가공) | 검색 결과만 | 무료 공개 |
| [Koyfin](https://www.koyfin.com/) | 금융 데이터 대시보드 | 관심 게임·퍼블리셔 | 관심 종목 목록(Watchlist) + 맞춤 대시보드 개념을 '관심 게임·퍼블리셔' 관찰 목록에 참고(화면 세부는 확인 못함) | 없음 | 검색 결과만 | 확인 못함 |
| [Luminate Streaming Charts (Variety 게재)](https://support.luminatedata.com/portal/en/kb/articles/svm-charts-film-tv) | 스트리밍 주간 Top 50 | 주간 순위 | 주간 Top 50 + 시즌을 별도 항목으로 세는 규칙처럼 '항목 단위 정의'를 차트 머리에 밝히는 방식을 우리 순위 기준(게임 단위, 주간 평균 순위) 표기에 참고 | Variety 기사로 해설 | 검색 결과만 | 유료 |
| [Morningstar Market Barometer · Sector Heatmap](https://advisor.morningstar.com/documentation_component_usmarketbarometer.htm) | 시장 스타일 박스 · 섹터 열지도 | 시장 비교와 장르 점유 | 3×3 스타일 박스(크기 × 성향) 칸을 등락 색으로 칠하는 압축 표기를 '장르 계열 × 시장 권역' 소형 열지도에 참고 | 없음 | 검색 결과만 | 로그인 필요 |
| [Netflix 'What We Watched' 시청 리포트](https://about.netflix.com/news/what-we-watched-the-second-half-of-2024) | OTT 반기 시청 리포트(글 + 표) | AI 시장 브리핑 | 반기마다 전체 규모(총 시청 시간) → 상위 작품 → 해설 순으로 쓰는 '리포트 글 + 내려받는 표' 묶음을, 우리 월간 · 분기 브리핑의 발행 형식(글 + 근거 표 내려받기)에 참고 | 사람이 쓴 해설 글과 전체 데이터 표를 함께 공개 | 검색 결과만 | 무료 공개 |
| [StockAnalysis — Market Movers](https://stockanalysis.com/markets/gainers/) | 주식 상승·하락 순위 | 진입·이탈·급변 | 일간 상승·하락·거래 상위를 탭으로 나눈 간단한 목록을 '급변' 목록 탭 구성에 참고(화면 세부 확인 못함) | 없음 | 검색 결과만 | 확인 못함 |
| [TradingView Heatmaps (주식 · ETF · 코인)](https://www.tradingview.com/heatmap/stock/) | 시장 트리맵(지역·지수 필터) | 시장 비교와 장르 점유 | 트리맵에 거래소 · 지역 · 지수 필터를 붙이고 색 척도를 그날 범위로 자동 조정하는 방식 — 장르 지도에 '나라 필터' 붙이는 설계와 색 척도 고정 여부 판단에 참고 | 없음 | 검색 결과만 | 무료 공개 |
| [Transfermarkt — 시장 가치 순위](https://www.transfermarkt.com/) | 스포츠 선수 시장 가치 순위 | 선택 게임 순위 이력 | 선수 페이지의 '시장 가치 변화 그래프'(시점마다 점 · 최고치 표시)를 게임 상세의 순위 이력 그래프 표기에 참고 | 없음 | 검색 결과만 | 무료 공개 |

## 뺀 곳과 이유 (40)

- [Apify 앱스토어 차트 스크레이퍼들](https://apify.com/scrapemint/app-store-top-charts-tracker) (검색 결과만) — 수집 도구라 화면 참고 대상이 아님.
- [Business of Apps 매출 상위 통계](https://www.businessofapps.com/data/top-grossing-apps/) (검색 결과만) — 통계 기사라 화면 참고점이 적음.
- [data.ai (구 App Annie) Top Charts](https://www.data.ai/) (검색 결과만) — Sensor Tower 인수(2024) 후 서비스가 사라졌다는 2026년 글이 있어 현재 화면을 참고할 수 없음.
- [game-i (일본)](https://game-i.daa.jp/) (검색 결과만) — 검색으로 화면을 확인하지 못함.
- [mobilegamer.biz](https://mobilegamer.biz/) (검색 결과만) — 이 사이트의 차트 화면을 찾지 못함.
- [Naavik](https://naavik.co/) (검색 결과만) — 대시보드 · 차트 도구를 찾지 못함.
- [Segwise](https://segwise.ai/) (검색 결과만) — 광고 소재 분석이라 우리 데이터(차트 순위)와 맞지 않음.
- [TwitchMetrics](https://www.twitchmetrics.net/games/played) (검색 결과만) — TwitchTracker와 겹치고 참고점이 적음.
- [ファミ通App](https://app.famitsu.com/) (검색 결과만) — 사이트 갱신이 중단됨.
- [游戏葡萄](https://youxiputao.com/) (검색 결과만) — 주간 순위 화면을 확인하지 못함.
- [点点数据 (Diandian)](https://www.diandian.com/) (검색 결과만) — 검색 결과에 화면 · 기능 정보가 없어 판정 불가.
- [蝉大师 (Chandashi)](https://www.chandashi.com/) (검색 결과만) — 순위 화면 정보를 찾지 못함.
- [게볼루션](https://www.gevolution.co.kr/) (검색 결과만) — 검색으로 화면을 확인할 수 없고 직접 열기도 막혀 판정 불가(네트워크 허용 후 재확인 권장).
- [게임메카 순위](https://www.gamemeca.com/) (검색 결과만) — 현재 모바일 순위 화면을 확인하지 못함(오래된 PC 온라인 순위 기사뿐).
- [인벤 순위](https://www.inven.co.kr/) (검색 결과만) — 순위 페이지를 찾지 못함.
- [Datawrapper 저장소](https://github.com/datawrapper/datawrapper) (열람) — 저장소에 화면 사례가 없음(문서 링크만)
- [Dribbble 대시보드 샷](https://dribbble.com/) (검색 결과만) — 검색으로 관련 사례를 특정하지 못했고 실데이터 화면이 아님
- [Flourish SDK](https://github.com/kiln/flourish-sdk) (열람) — 대시보드 화면 사례가 아님
- [HoloViz Panel / Vega-Lite](https://github.com/holoviz/panel) (열람) — 대시보드 사례가 아니라 범용 라이브러리
- [Information is Beautiful](https://informationisbeautiful.net/) (검색 결과만) — 우리 구성요소에 맞는 화면을 찾지 못함
- [Observable 노트북: Billboard Hot 100](https://observablehq.com/@khaos2) (검색 결과만) — 내용을 확인할 수 없음
- [Turnilo](https://github.com/allegro/turnilo) (열람) — 보관된 프로젝트이고 Druid 전용, 화면 정보 부족
- [Visual Capitalist](https://www.visualcapitalist.com/) (검색 결과만) — 관련 페이지를 찾지 못함
- [Chartbrew](https://github.com/chartbrew/chartbrew) (열람) — 일반 차트 빌더이고 AI 해석 결합이 없음
- [Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/) (검색 결과만) — 검색으로 화면 정보를 찾지 못함
- [Julius AI](https://julius.ai) (검색 결과만) — 파일 업로드형 일회성 분석이라 상시 대시보드 화면 참고점이 없음
- [Matomo](https://github.com/matomo-org/matomo) (열람) — README에 대시보드 · AI 화면 정보가 없어 참고점 확인 불가
- [Oracle EPM GenAI 인사이트 요약](https://docs.oracle.com/en/cloud/saas/readiness/epm/2025/splan-apr25/25apr-sales-planning-wn-f38307.htm) (검색 결과만) — 기업 계획 도구라 화면 정보가 없고 순위 · 시장 데이터와 맞는 화면이 없음
- [PandasAI](https://github.com/sinaptik-ai/pandas-ai) (열람) — 라이브러리라 화면 구성 참고점이 없음
- [Rill](https://github.com/rilldata/rill) (열람) — README에 화면 구성 정보가 적어 참고점 확인 불가
- [Similarweb AI 트래픽 지표](https://support.similarweb.com/hc/en-us/articles/6092440668445-Similarweb-Extension) (검색 결과만) — 'AI'가 해석 기능이 아니라 AI 챗봇 유입 측정이라 이 분류(C)에 맞지 않음(순위 화면은 시장 분석 분류에서 볼 대상)
- [Vanna](https://github.com/vanna-ai/vanna) (열람) — 채팅 컴포넌트 외 대시보드 화면이 없음
- [WrenAI](https://github.com/Canner/WrenAI) (열람) — 에이전트용 백엔드라 화면 참고점이 없음
- [Zenlytic (Zoë)](https://www.zenlytic.com) (검색 결과만) — 채팅 우선 제품이라 지표+해설 배치 사례가 확인되지 않음
- [Deezer Charts](https://www.deezer.com/explore/charts) (검색 결과만) — 다른 음악 차트(Spotify · Apple Music)와 같은 구조이고 따로 참고할 화면 정보가 없음
- [FBref](https://fbref.com/) (검색 결과만) — 선수·경기 단위 통계표 위주라 나라별 순위 추이 · 점유 화면으로 옮길 요소가 거의 없음
- [GitHub Trending](https://github.com/trending) (검색 결과만) — 순위 근거가 비공개이고 이력 · 나라 비교가 없어 참고할 화면이 없음
- [Product Hunt Leaderboard](https://www.producthunt.com/leaderboard) (검색 결과만) — 순위가 하루짜리 투표 경쟁이라 나라별 순위 추이 · 장르 점유 같은 우리 데이터 모양과 맞지 않음
- [Spotify Charts BI Pipeline (GitHub 개인 프로젝트)](https://github.com/kirbydoo10/Spotify-Charts-Pipeline-Dashboard) (열람) — 실제 데이터가 아닌 시뮬레이션 데이터 기반이라 참고 근거로 약함
- [지니 차트](https://www.genie.co.kr/chart/top200) (검색 결과만) — 멜론과 같은 형식의 국내 음원 순위라 별도로 참고할 점이 없음

## 막힌 주소

열기를 시도했다가 네트워크 정책으로 막힌 주소(같은 이유로 다른 사이트는 검색 결과로 판정했다). 환경 설정의 Network access에서 도메인을 허용하면 열어 볼 수 있다.

- https://appmagic.rocks/top-charts/apps — WebFetch — getaddrinfo ENOTFOUND
- https://www.qimai.cn/rank — WebFetch — getaddrinfo ENOTFOUND
- https://www.gevolution.co.kr/rank/ — WebFetch — getaddrinfo ENOTFOUND
- https://public.tableau.com/app/discover/viz-of-the-day — WebFetch
- https://dashboarddesignpatterns.github.io/ — WebFetch
- https://ourworldindata.org/grapher/life-expectancy — WebFetch
- https://github.com/plotly/dash-sample-apps/tree/main/apps — curl (403)
- https://www.tableau.com/products/tableau-pulse — WebFetch — getaddrinfo ENOTFOUND
- https://posthog.com/docs/web-analytics/dashboard — WebFetch — getaddrinfo ENOTFOUND
- https://www.netflix.com/tudum/top10 WebFetch
- https://kworb.net/spotify/ WebFetch
- https://flixpatrol.com/top10/ WebFetch
- https://store.steampowered.com/charts/ WebFetch
- https://www.billboard.com/charts/hot-100/ WebFetch
