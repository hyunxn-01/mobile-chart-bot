"""
data/history/*.json 누적 데이터를 GitHub Pages 대시보드용 docs/data.json으로 집계한다.

- 일별(daily): 각 날짜의 실제 순위(원본). 봇의 1일선과 동일 — 평균이 아니다.
- 주/월/분기/년: 해당 기간에 '차트에 든 날'의 순위만 평균(봇 compute_average_ranks와 같은 규칙).
  그 기간에 한 번도 안 들었으면 null.

chart_collector.py와 같은 레포에서 매일 실행되어 대시보드 데이터를 갱신한다.
사용법: 레포 루트에서 `python build_dashboard.py`
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

HISTORY_DIR = Path('data') / 'history'
DOCS_DIR = Path('docs')
OUT_FILE = DOCS_DIR / 'data.json'

AVG_TIMEFRAMES = ['weekly', 'monthly', 'quarterly', 'yearly']


def load_history():
    """{YYYY-MM-DD: [app, ...]} 날짜순. 잘못된 파일은 건너뛴다."""
    days = {}
    for f in sorted(HISTORY_DIR.glob('*.json')):
        date_str = f.stem
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            continue
        try:
            data = json.loads(f.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"[WARN] {f} 로드 실패: {e}")
            continue
        if isinstance(data, list):
            days[date_str] = data
    return days


def period_key(date_str, tf):
    d = datetime.strptime(date_str, '%Y-%m-%d')
    if tf == 'weekly':
        monday = d - timedelta(days=d.weekday())
        return monday.strftime('%Y-%m-%d')
    if tf == 'monthly':
        return d.strftime('%Y-%m')
    if tf == 'quarterly':
        return f'{d.year}-Q{(d.month - 1) // 3 + 1}'
    if tf == 'yearly':
        return str(d.year)
    return date_str


def build():
    days = load_history()
    dates = sorted(days.keys())

    games = {}
    for date_str in dates:
        for app in days[date_str]:
            aid = app.get('app_id')
            if not aid:
                continue
            games[aid] = {'title': app.get('title', ''), 'developer': app.get('developer', '')}

    timeframes = {}

    # 일별: 원본 순위
    daily_series = {aid: [None] * len(dates) for aid in games}
    for i, date_str in enumerate(dates):
        for app in days[date_str]:
            aid = app.get('app_id')
            if aid in daily_series:
                daily_series[aid][i] = app.get('rank')
    timeframes['daily'] = {'labels': dates, 'series': daily_series}

    # 주/월/분기/년: 기간평균(등장한 날만)
    for tf in AVG_TIMEFRAMES:
        period_to_dates = {}
        for date_str in dates:
            period_to_dates.setdefault(period_key(date_str, tf), []).append(date_str)
        labels = list(period_to_dates.keys())  # dates가 정렬돼 있어 라벨도 시간순
        series = {aid: [None] * len(labels) for aid in games}
        for pi, k in enumerate(labels):
            acc = {}
            for date_str in period_to_dates[k]:
                for app in days[date_str]:
                    aid = app.get('app_id')
                    r = app.get('rank')
                    if aid not in series or r is None:
                        continue
                    a = acc.setdefault(aid, [0, 0])
                    a[0] += r
                    a[1] += 1
            for aid, (s, c) in acc.items():
                series[aid][pi] = round(s / c, 1)
        timeframes[tf] = {'labels': labels, 'series': series}

    chart_used = ''
    if dates and days[dates[-1]]:
        chart_used = days[dates[-1]][0].get('chart', '')

    out = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'chart_used': chart_used,
        'date_range': [dates[0], dates[-1]] if dates else [],
        'num_days': len(dates),
        'num_games': len(games),
        'games': games,
        'timeframes': timeframes,
    }
    DOCS_DIR.mkdir(exist_ok=True)
    OUT_FILE.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f"[OK] {OUT_FILE} 생성: {len(games)}게임 · {len(dates)}일 · 시간축 {list(timeframes.keys())}")
    return out


if __name__ == '__main__':
    build()
