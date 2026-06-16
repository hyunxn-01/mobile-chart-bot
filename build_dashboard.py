"""
data/history/*.json (Top Grossing) + data/history_free/*.json (Top Free) 누적 데이터를
GitHub Pages 대시보드용 docs/data.json으로 집계한다.

- 일별(daily): 각 날짜의 실제 순위(원본). 봇의 1일선과 동일 — 평균이 아니다.
- 주/월/분기/년: 해당 기간에 '차트에 든 날'의 순위만 평균(봇 compute_average_ranks와 같은 규칙).
  그 기간에 한 번도 안 들었으면 null.
- 퍼블리셔(publishers): 가장 최근 차트일 기준, 개발사별 등장 게임 수·최고/평균 순위 집계.

차트 2종(매출=grossing, 인기=free)을 각각 집계해 data.json의 charts.{grossing,free}에 담는다.
하위호환: 최상위에 grossing 필드(chart_used/games/timeframes/num_games)를 그대로 둔다(구 대시보드 호환).

chart_collector.py와 같은 레포에서 매일 실행되어 대시보드 데이터를 갱신한다.
사용법: 레포 루트에서 `python build_dashboard.py`
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

HISTORY_DIR = Path('data') / 'history'            # Top Grossing(매출)
HISTORY_FREE_DIR = Path('data') / 'history_free'  # Top Free(인기)
DOCS_DIR = Path('docs')
OUT_FILE = DOCS_DIR / 'data.json'

AVG_TIMEFRAMES = ['weekly', 'monthly', 'quarterly', 'yearly']


def load_history(history_dir):
    """{YYYY-MM-DD: [app, ...]} 날짜순. 잘못된/없는 파일은 건너뛴다. 디렉터리가 없으면 빈 dict."""
    days = {}
    if not history_dir.exists():
        return days
    for f in sorted(history_dir.glob('*.json')):
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


def build_publishers(days, dates):
    """가장 최근 차트일 기준 개발사별 집계. 등장 게임 수 desc, 최고 순위 asc로 정렬."""
    if not dates:
        return {'as_of': None, 'list': []}
    latest = dates[-1]
    by_dev = {}
    for app in days[latest]:
        dev = (app.get('developer') or '').strip() or '(미상)'
        r = app.get('rank')
        e = by_dev.setdefault(dev, {'developer': dev, 'num_games': 0, 'ranks': [], 'games': []})
        e['num_games'] += 1
        if r is not None:
            e['ranks'].append(r)
        e['games'].append({'title': app.get('title', ''), 'rank': r, 'app_id': app.get('app_id', '')})
    out = []
    for dev, e in by_dev.items():
        ranks = e['ranks']
        e['best_rank'] = min(ranks) if ranks else None
        e['avg_rank'] = round(sum(ranks) / len(ranks), 1) if ranks else None
        e['games'].sort(key=lambda g: (g['rank'] is None, g['rank'] if g['rank'] is not None else 9999))
        del e['ranks']
        out.append(e)
    out.sort(key=lambda e: (-e['num_games'], e['best_rank'] if e['best_rank'] is not None else 9999))
    return {'as_of': latest, 'list': out}


def build_chart(history_dir):
    """한 차트(grossing 또는 free)의 집계 묶음을 만든다."""
    days = load_history(history_dir)
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

    return {
        'chart_used': chart_used,
        'date_range': [dates[0], dates[-1]] if dates else [],
        'num_days': len(dates),
        'num_games': len(games),
        'games': games,
        'timeframes': timeframes,
        'publishers': build_publishers(days, dates),
    }


def build():
    grossing = build_chart(HISTORY_DIR)
    free = build_chart(HISTORY_FREE_DIR)

    out = {
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        # --- 하위호환: 최상위 = grossing (구 대시보드가 이 필드를 직접 읽음) ---
        'chart_used': grossing['chart_used'],
        'date_range': grossing['date_range'],
        'num_days': grossing['num_days'],
        'num_games': grossing['num_games'],
        'games': grossing['games'],
        'timeframes': grossing['timeframes'],
        # --- 신규: 차트 2종 묶음 ---
        'charts': {
            'grossing': grossing,
            'free': free,
        },
    }
    DOCS_DIR.mkdir(exist_ok=True)
    OUT_FILE.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f"[OK] {OUT_FILE} 생성")
    print(f"     매출(grossing): {grossing['num_games']}게임 · {grossing['num_days']}일")
    print(f"     인기(free): {free['num_games']}게임 · {free['num_days']}일")
    print(f"     퍼블리셔: 매출 {len(grossing['publishers']['list'])}곳 · 인기 {len(free['publishers']['list'])}곳")
    return out


if __name__ == '__main__':
    build()
