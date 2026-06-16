# 차트 대시보드 추가 — 설정 가이드

이 봇에 **GitHub Pages 인터랙티브 대시보드**가 추가됐습니다. 매일 자동 갱신되는 웹페이지에서
일·주·월·분기·년 시간축으로 100여 개 게임의 순위 추이를 보고, 보고 싶은 게임만 선택해 강조할 수
있습니다. 매일 발송되는 메일(평일 라이트 포함)에 대시보드 링크 버튼이 들어갑니다.

## 새 파일 / 변경 파일

| 구분 | 파일 | 내용 |
|---|---|---|
| 신규 | `build_dashboard.py` | `data/history/*.json` 전체 → `docs/data.json` 집계 (표준 라이브러리만) |
| 신규 | `docs/index.html` | 대시보드 페이지(정적). `data.json`을 읽어 그래프를 그림 |
| 변경 | `chart_collector.py` | `DASHBOARD_URL` 상수 추가 + 모든 메일에 대시보드 버튼 |
| 변경 | `.github/workflows/daily_chart.yml` | 매일 실행 끝에 `build_dashboard.py` 실행 + `docs/` 커밋 |

> `docs/data.json`은 봇이 만드는 **자동 생성물**입니다. 직접 편집하지 않습니다. 첫 실행 때 생성됩니다.

## 데이터 산출 방식 (확인용)

- **일별** = 그날의 실제 순위(원본, 평균 아님).
- **주·월·분기·년** = 그 기간에 **차트에 든 날의 순위만 평균**(봇의 기존 `compute_average_ranks`와 동일 규칙).
  그 기간에 한 번도 안 들었으면 빈칸(null)으로 둡니다.

## 설정 순서 (최초 1회)

1. **파일 반영** — 위 신규·변경 파일을 레포에 커밋·푸시.
2. **레포 공개 전환** — `Settings → General → 맨 아래 Danger Zone → Change repository visibility → Public`.
   - 노출되는 건 봇 코드와 공개 차트 순위뿐입니다. **API키·Gmail 앱비번 등 시크릿은 `Settings → Secrets`에 있어 공개되지 않습니다.**
3. **Pages 켜기** — `Settings → Pages → Build and deployment → Source: "Deploy from a branch" → Branch: main / 폴더: /docs → Save`.
   - 잠시 뒤 상단에 사이트 주소가 뜹니다: `https://<사용자명>.github.io/<레포명>/`
4. **주소 확인** — `chart_collector.py`의 `DASHBOARD_URL`은 이미 `https://hyunxn-01.github.io/mobile-chart-bot/`로 채워져 있습니다. 위에서 뜬 Pages 주소가 같은지 확인만 하면 됩니다(다르면 그 줄만 교체).
5. **첫 데이터 생성** — `Actions 탭 → Daily Mobile Chart Report → Run workflow`(수동 1회 실행).
   - `build_dashboard.py`가 `docs/data.json`을 만들어 커밋 → 대시보드가 살아납니다.
   - 이 실행 전까지 페이지는 "데이터를 불러오지 못했습니다"로 보이는 게 정상입니다.

이후부터는 매일 자동입니다: 차트 수집 → `data.json` 갱신 → 커밋 → Pages 자동 반영 → 메일에 링크.

## 알아둘 점

- **분기·년 탭**은 데이터가 충분히 쌓일 때까지 "데이터 부족"으로 표시됩니다(정상). 일·주·월은 곧바로 의미가 생깁니다.
- 대시보드는 **공개 URL**이라 링크를 아는 사람은 볼 수 있습니다(검색 노출은 거의 없음). 민감 정보는 담기지 않습니다.
- **의존성 추가 없음** — `requirements.txt`는 그대로입니다.
- `data.json`은 매 실행 통째로 다시 생성됩니다. 수년 뒤 레포가 커지면 일별 시리즈를 최근 N일로 제한하는 옵션을 추가하면 됩니다.

## 미리보기

같은 폴더의 결과물을 배포 전에 보고 싶으면, 제공된 `dashboard_preview.html`(예시 데이터 내장)을
브라우저로 열어보세요. 실제 페이지와 동일한 동작(시간축 탭·게임 검색·선택 강조)을 오프라인에서 확인할 수 있습니다.
