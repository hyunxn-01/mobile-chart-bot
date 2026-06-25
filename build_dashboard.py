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

# AppMagic 업계표준 장르 라벨(trackId → {top, sub, tier, ...}). 게임당 1회 조회·영구 캐시.
# canon_genre가 최우선 참조 → 점유율·히트맵·범례·기회맵이 전부 AppMagic 기준이 된다.
AM_CACHE_PATH = Path('data') / 'genre_appmagic.json'
AM_CACHE = {}


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


def period_end(key, tf):
    """기간 키의 마지막 날짜(완료 판정용). datetime 반환."""
    if tf == 'weekly':
        return datetime.strptime(key, '%Y-%m-%d') + timedelta(days=6)
    if tf == 'monthly':
        y, m = int(key[:4]), int(key[5:7])
        nxt = datetime(y + 1, 1, 1) if m == 12 else datetime(y, m + 1, 1)
        return nxt - timedelta(days=1)
    if tf == 'quarterly':
        y = int(key[:4]); q = int(key.split('-Q')[1]); em = q * 3
        nxt = datetime(y + 1, 1, 1) if em == 12 else datetime(y, em + 1, 1)
        return nxt - timedelta(days=1)
    if tf == 'yearly':
        return datetime(int(key), 12, 31)
    return datetime.strptime(key, '%Y-%m-%d')


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


def build_genres(days, dates):
    """가장 최근 차트일 기준 장르별 집계(봇이 lookup으로 붙인 genre 사용). 게임 수 desc, 최고 순위 asc."""
    if not dates:
        return {'as_of': None, 'list': []}
    latest = dates[-1]
    by = {}
    for app in days[latest]:
        g = (app.get('genre') or '').strip() or '미상'
        r = app.get('rank')
        e = by.setdefault(g, {'genre': g, 'num_games': 0, 'ranks': [], 'games': []})
        e['num_games'] += 1
        if r is not None:
            e['ranks'].append(r)
        e['games'].append({'title': app.get('title', ''), 'rank': r, 'app_id': app.get('app_id', '')})
    out = []
    for g, e in by.items():
        ranks = e['ranks']
        e['best_rank'] = min(ranks) if ranks else None
        e['avg_rank'] = round(sum(ranks) / len(ranks), 1) if ranks else None
        e['games'].sort(key=lambda x: (x['rank'] is None, x['rank'] if x['rank'] is not None else 9999))
        del e['ranks']
        out.append(e)
    out.sort(key=lambda e: (-e['num_games'], e['best_rank'] if e['best_rank'] is not None else 9999))
    return {'as_of': latest, 'list': out}


def build_chart(history_dir):
    """한 차트(grossing 또는 free)의 집계 묶음을 만든다(디렉터리에서 로드)."""
    return build_chart_from_days(load_history(history_dir))


def build_chart_from_days(days):
    """한 차트(grossing 또는 free)의 집계 묶음을 days({date:[apps]})에서 만든다.
    출력 구조 = data.json의 charts[kind]와 동일(timeframes·publishers·genres·games)."""
    dates = sorted(days.keys())

    games = {}
    for date_str in dates:
        for app in days[date_str]:
            aid = app.get('app_id')
            if not aid:
                continue
            games[aid] = {'title': app.get('title', ''), 'developer': app.get('developer', ''), 'genre': app.get('genre', ''), 'sub': app.get('am_sub', ''), 'tier': app.get('am_tier', ''), 'release': app.get('release', ''), 'rating': app.get('rating'), 'icon': app.get('icon', ''), 'updated': app.get('updated', ''), 'ratings': app.get('ratings'), 'notes': app.get('notes', ''), 'artist_id': app.get('artist_id'), 'cv_rating': app.get('cv_rating'), 'cv_ratings': app.get('cv_ratings'), 'track_id': app.get('track_id', ''), 'version': app.get('version', '')}

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
        # 진행 중(미완료) 기간 제외: 마지막 기간의 끝날이 최신 수집일보다 미래면 드롭(완료된 기간만 표시)
        if dates:
            latest_dt = datetime.strptime(dates[-1], '%Y-%m-%d')
            while labels and period_end(labels[-1], tf) > latest_dt:
                labels.pop()
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
        'genres': build_genres(days, dates),
    }


# ============================================================
# 다국가 집계 (Phase 2) — data/charts/{country}/{kind} → docs/markets/{country}.json
# ============================================================

CHARTS_DIR = Path('data') / 'charts'
MARKETS_OUT = DOCS_DIR / 'markets'

# Apple 게임 장르 ID(숫자) → 정규 장르(한글). 언어 독립이라 전 국가 통일에 사용.
GENRE_ID_KR = {
    '7001': '액션', '7002': '어드벤처', '7003': '캐주얼', '7004': '보드', '7005': '카드',
    '7006': '카지노', '7007': '주사위', '7008': '교육', '7009': '가족', '7011': '음악',
    '7012': '퍼즐', '7013': '레이싱', '7014': '롤플레잉', '7015': '시뮬레이션', '7016': '스포츠',
    '7017': '전략', '7018': '트리비아', '7019': '단어',
}

# 한 게임에 장르ID가 여러 개일 때 '게임 성격'을 더 잘 나타내는 것을 우선(어드벤처·캐주얼·가족은 후순위).
# 예: 밤탈출 = 어드벤처+롤플레잉 → 롤플레잉. AppMagic 라벨이 없을 때 폴백 품질을 끌어올린다.
GENRE_PRIORITY = ['7014', '7017', '7015', '7016', '7013', '7006', '7012', '7001',
                  '7004', '7005', '7019', '7011', '7002', '7003', '7008', '7018', '7009', '7007']


GENRE_NONE = '장르 없음'   # AppMagic 게임 장르 태그가 없는 경우(Apple/현지 폴백 미사용)


def canon_genre(app):
    """장르는 AppMagic 분류 안에서만 유지한다. L2(직계 서브) 우선 → 없으면 L1(둘 다 AppMagic 유래).
    AppMagic이 게임 장르 태그를 주지 않으면 '장르 없음'으로 분류(Apple genre_ids·현지 장르 폴백 제거)."""
    am = AM_CACHE.get(str(app.get('track_id') or ''))
    if am:
        if am.get('genre'):      # ← 우리 모든 장르의 디폴트 = L2(직계 서브)
            return am['genre']
        if am.get('top'):        # L2가 비면 L1(역시 AppMagic 택소노미 유래)
            return am['top']
    return GENRE_NONE


def load_country_charts(country, kind):
    """data/charts/{country}/{kind}/*.json → {date: [apps]} 날짜순."""
    d = CHARTS_DIR / country / kind
    days = {}
    if not d.exists():
        return days
    for f in sorted(d.glob('*.json')):
        try:
            datetime.strptime(f.stem, '%Y-%m-%d')
        except ValueError:
            continue
        try:
            data = json.loads(f.read_text(encoding='utf-8'))
            if isinstance(data, list):
                days[f.stem] = data
        except Exception as e:
            print(f"[WARN] {f} 로드 실패: {e}")
    return days


def build_genre_series(days, dates):
    """일별 장르 점유율 시계열(누적영역 차트용): {labels, genres:{genre:[count per date]}}."""
    all_g = set()
    per_day = {}
    for dt in dates:
        c = {}
        for app in days[dt]:
            g = canon_genre(app)
            c[g] = c.get(g, 0) + 1
            all_g.add(g)
        per_day[dt] = c
    genres = {g: [per_day[dt].get(g, 0) for dt in dates] for g in sorted(all_g)}
    return {'labels': dates, 'genres': genres}


def build_country(country):
    """국가별 집계를 data.json의 charts[kind]와 '동일한 구조'로 생성(index 대시보드 그대로 재사용).
    + 장르 차트 스왑용 genre_series 동봉. 게임명은 한국어(title_kr), 장르는 표준화(canon_genre)."""
    out = {'country': country, 'generated': datetime.now().strftime('%Y-%m-%d %H:%M'), 'charts': {}}
    for kind in ('grossing', 'free'):
        days = load_country_charts(country, kind)
        if not days:
            continue
        # 정규화: 한국어 게임명 + 표준 장르(genre_ids 기반) + app_id 보강
        for dt in days:
            for app in days[dt]:
                app['title'] = app.get('title_kr') or app.get('title', '')
                app['genre'] = canon_genre(app)
                _am = AM_CACHE.get(str(app.get('track_id') or '')) or {}
                app['am_sub'] = _am.get('sub', '')
                app['am_tier'] = _am.get('tier', '')
                if not app.get('app_id'):
                    app['app_id'] = app.get('track_id')
        ch = build_chart_from_days(days)
        ch['genre_series'] = build_genre_series(days, sorted(days.keys()))
        out['charts'][kind] = ch
    return out


# --- 시장 그룹(브리핑과 동일) + 합산 가중치 ---
MAJOR_MARKETS = ['kr', 'us', 'jp', 'cn', 'tw']
REGIONS = {
    'europe':      ('유럽',           ['gb', 'de', 'fr', 'it', 'es', 'nl', 'ru', 'se']),
    'na_oceania':  ('북미·오세아니아', ['ca', 'au']),
    'middle_east': ('중동',           ['sa', 'ae', 'eg', 'tr']),
    'latam':       ('중남미',         ['br', 'mx', 'ar', 'co']),
    'sea':         ('동남아',         ['id', 'th', 'vn', 'ph', 'my', 'sg']),
    'south_asia':  ('남아시아',       ['in', 'pk', 'bd']),
}
REV_ALPHA = 1.1   # 매출 멱법칙(프론트 revWeight와 동일)
DL_ALPHA = 0.8    # 다운로드는 더 완만
# 국가별 상대 시장규모(미국=100). 지역 합산 시 큰 시장이 더 기여하도록 가중. 공개 매출/다운로드 국가순위 근사.
MARKET_WEIGHT = {  # 매출(grossing)
    'us': 100, 'jp': 90, 'cn': 95, 'kr': 45, 'tw': 22, 'gb': 30, 'de': 32, 'fr': 24, 'ca': 20, 'au': 18,
    'it': 16, 'es': 15, 'nl': 10, 'ru': 14, 'se': 8, 'sa': 12, 'ae': 9, 'eg': 4, 'tr': 7,
    'br': 14, 'mx': 12, 'ar': 5, 'co': 4, 'id': 10, 'th': 9, 'vn': 7, 'ph': 6, 'my': 7, 'sg': 8, 'in': 12, 'pk': 3, 'bd': 2,
}
DL_WEIGHT = {      # 다운로드(free) — 인구·설치 규모 경향
    'us': 100, 'cn': 120, 'jp': 45, 'kr': 18, 'tw': 10, 'gb': 22, 'de': 28, 'fr': 24, 'ca': 16, 'au': 12,
    'it': 18, 'es': 18, 'nl': 7, 'ru': 40, 'se': 5, 'sa': 10, 'ae': 6, 'eg': 22, 'tr': 28,
    'br': 70, 'mx': 45, 'ar': 16, 'co': 16, 'id': 75, 'th': 30, 'vn': 35, 'ph': 35, 'my': 16, 'sg': 5, 'in': 150, 'pk': 30, 'bd': 20,
}


def build_region_days(member_ccs, kind):
    """멤버국 차트를 점유율 가중 합산 → 지역 단일 차트용 {date:[apps(지역순위)]}.
    게임별 지역가치 = Σ(국가 시장가중 × rank^-alpha). 그 값으로 지역 순위(1=최상위) 매김."""
    cc_days, all_dates, meta = {}, set(), {}
    for cc in member_ccs:
        d = load_country_charts(cc, kind)
        if not d:
            continue
        for dt in d:
            for app in d[dt]:
                app['title'] = app.get('title_kr') or app.get('title', '')
                app['genre'] = canon_genre(app)
                _am = AM_CACHE.get(str(app.get('track_id') or '')) or {}
                app['am_sub'] = _am.get('sub', '')
                app['am_tier'] = _am.get('tier', '')
                if not app.get('app_id'):
                    app['app_id'] = app.get('track_id')
                aid = app.get('app_id')
                if aid and aid not in meta:
                    meta[aid] = app
        cc_days[cc] = d
        all_dates |= set(d.keys())
    if not cc_days:
        return {}
    W = MARKET_WEIGHT if kind == 'grossing' else DL_WEIGHT
    alpha = REV_ALPHA if kind == 'grossing' else DL_ALPHA
    region_days = {}
    for dt in sorted(all_dates):
        val = {}
        for cc, d in cc_days.items():
            apps = d.get(dt)
            if not apps:
                continue
            cw = W.get(cc, 5)
            for app in apps:
                aid, r = app.get('app_id'), app.get('rank')
                if not aid or not r:
                    continue
                val[aid] = val.get(aid, 0) + cw * (float(r) ** (-alpha))
        if not val:
            continue
        ordered = sorted(val.items(), key=lambda kv: -kv[1])
        apps_out = []
        for i, (aid, v) in enumerate(ordered[:100], start=1):
            a = dict(meta.get(aid, {}))
            a['app_id'] = aid
            a['rank'] = i
            apps_out.append(a)
        region_days[dt] = apps_out
    return region_days


def build_region_market(region_key, name, member_ccs):
    """지역 합산 마켓을 index 구조(charts.{grossing,free}+genre_series)로 생성."""
    out = {'market': region_key, 'name': name, 'type': 'region', 'members': member_ccs,
           'generated': datetime.now().strftime('%Y-%m-%d %H:%M'), 'charts': {}}
    for kind in ('grossing', 'free'):
        days = build_region_days(member_ccs, kind)
        if not days:
            continue
        ch = build_chart_from_days(days)
        ch['genre_series'] = build_genre_series(days, sorted(days.keys()))
        out['charts'][kind] = ch
    return out


CC_NAMES = {'kr': '한국', 'us': '미국', 'jp': '일본', 'cn': '중국', 'tw': '대만'}


def _market_genre_shares(market_obj):
    """그 시장 grossing 최신 기준 장르별 {매출 점유%, 게임수 점유%}(미상 제외).
    매출 점유 = Σ rank^-REV_ALPHA(프론트 revShare와 동일 모델)를 시장 내 정규화."""
    lst = ((((market_obj or {}).get('charts') or {}).get('grossing') or {}).get('genres') or {}).get('list') or []
    rows = {}
    for e in lst:
        g = (e.get('genre') or '').strip()
        if not g or g == '미상':
            continue
        revw = 0.0
        for gm in (e.get('games') or []):
            r = gm.get('rank')
            if r:
                revw += float(r) ** (-REV_ALPHA)
        rows[g] = {'rev_w': revw, 'n': e.get('num_games', 0) or 0}
    totrev = sum(v['rev_w'] for v in rows.values()) or 1.0
    totn = sum(v['n'] for v in rows.values()) or 1
    return {g: {'rev': round(v['rev_w'] / totrev * 1000) / 10,
                'pre': round(v['n'] / totn * 1000) / 10} for g, v in rows.items()}


def build_genre_matrix(built):
    """주요국+지역 × 장르 매트릭스(매출/게임수 점유%). built={key:(market_obj,name,type)}.
    열=시장(매출 가중 큰 순), 행=장르(총 매출 점유 desc). 칸 클릭·블루오션 비교용."""
    cells, gtot, cols = {}, {}, []
    for key, (obj, name, typ) in built.items():
        sh = _market_genre_shares(obj)
        if not sh:
            continue
        cells[key] = sh
        cols.append({'key': key, 'name': name, 'type': typ})
        for g, v in sh.items():
            gtot[g] = gtot.get(g, 0) + v['rev']
    genres = sorted(gtot.keys(), key=lambda g: -gtot[g])
    return {'generated': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'metric_default': 'rev', 'markets': cols, 'genres': genres, 'cells': cells}


def build_genre_audit(all_games):
    """전 시장 고유 게임을 AppMagic 라벨(AM_CACHE)로 정리 → 읽기전용 검수표 genre_audit.json.
    Opus·자체분류 폐기(AppMagic이 권위). track_id로 AM_CACHE 조회, 없으면 폴백 장르 표기."""
    from collections import Counter
    rows = []
    for aid, g in all_games.items():
        am = AM_CACHE.get(str(g.get('track_id') or '')) or {}
        if am.get('top'):
            top, sub, tier, s = am['top'], am.get('sub', ''), am.get('tier', ''), 'appmagic'
        else:
            top, sub, tier, s = (g.get('genre') or '기타'), '', '', 'fallback'
        rows.append({'app_id': aid, 'title': g.get('title'), 'api': g.get('genre', ''),
                     'top': top, 'sub': sub, 'tier': tier, 'src': s})
    src = Counter(r['src'] for r in rows)
    rows.sort(key=lambda r: (r['top'], r['sub'], r['title'] or ''))
    (MARKETS_OUT / 'genre_audit.json').write_text(
        json.dumps({'generated': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'n': len(rows), 'sources': dict(src), 'rows': rows},
                   ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f"[OK] 장르 검수표(AppMagic): {len(rows)}게임 · 출처 {dict(src)} → genre_audit.json")


def build_markets():
    """전 국가(개별) + 지역(합산) 마켓 → docs/markets/{key}.json + index.json + genre_matrix.json + genre_audit.json."""
    if not CHARTS_DIR.exists():
        print('[INFO] data/charts 없음 — 다국가 집계 건너뜀')
        return
    MARKETS_OUT.mkdir(parents=True, exist_ok=True)
    countries = sorted([d.name for d in CHARTS_DIR.iterdir() if d.is_dir()])
    # AppMagic 업계표준 장르 라벨: 신규 trackId만 조회해 캐시 채움(canon_genre가 참조하기 전에).
    try:
        AM_CACHE.clear()
        AM_CACHE.update(json.loads(AM_CACHE_PATH.read_text(encoding='utf-8')))
    except Exception:
        pass
    try:
        import genre_appmagic as gam
        _rank, _all = {}, set()
        for cc in countries:
            for kind in ('grossing', 'free'):
                _days = load_country_charts(cc, kind)
                if not _days:
                    continue
                _last = sorted(_days.keys())[-1]   # 최신 스냅샷 = 현재 차트
                for _dt, _apps in _days.items():
                    for _a in _apps:
                        _t = _a.get('track_id')
                        if not _t:
                            continue
                        _t = str(_t)
                        _all.add(_t)
                        if _dt == _last:
                            _r = _a.get('rank') or 999
                            if _t not in _rank or _r < _rank[_t]:
                                _rank[_t] = _r
        # 현재 차트 게임을 상위 랭크부터, 그 외(과거 등장) 게임은 뒤에 — '보이는 게임' 커버리지 우선
        _ordered = sorted(_rank, key=lambda t: _rank[t]) + [t for t in sorted(_all) if t not in _rank]
        gam.label_all(_ordered, AM_CACHE)
        # 전체 택소노미로 L2 도출(우리 모든 장르의 디폴트=L2) — 저장 리프→루트 거슬러 L2, 재조회 0. 신규+기존 통일.
        _taxo = gam.fetch_taxonomy()
        if _taxo:
            (Path('data') / 'appmagic_taxonomy.json').write_text(
                json.dumps(_taxo, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
            gam.apply_l2(AM_CACHE, _taxo)
        AM_CACHE_PATH.write_text(
            json.dumps(AM_CACHE, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    except Exception as e:
        print('[WARN] AppMagic 라벨 단계 실패(폴백 장르로 진행):', e)
    have = set()
    majors, regions_idx, singles = [], [], []
    built = {}   # 히트맵 매트릭스용: 주요국+지역의 market_obj 보관
    all_games = {}   # 장르 검수표용: 전 시장 고유 게임(app_id → 게임 dict)
    # 1) 개별 국가(주요 5 + 나머지)
    for cc in countries:
        co = build_country(cc)
        if not co.get('charts'):
            continue
        (MARKETS_OUT / f'{cc}.json').write_text(
            json.dumps(co, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
        have.add(cc)
        for _aid, _g in ((co.get('charts', {}).get('grossing', {}) or {}).get('games') or {}).items():
            if _aid not in all_games:
                all_games[_aid] = _g
        g = co['charts'].get('grossing', {})
        entry = {'key': cc, 'num_days': g.get('num_days', 0), 'num_games': g.get('num_games', 0)}
        if cc in MAJOR_MARKETS:
            majors.append({**entry, 'type': 'major'})
            built[cc] = (co, CC_NAMES.get(cc, cc.upper()), 'major')
        else:
            singles.append({**entry, 'type': 'country'})
    # 2) 지역(합산) — 멤버가 1개국 이상 수집된 지역만
    for key, (name, ccs) in REGIONS.items():
        members = [cc for cc in ccs if cc in have]
        if not members:
            continue
        rm = build_region_market(key, name, members)
        if not rm.get('charts'):
            continue
        (MARKETS_OUT / f'{key}.json').write_text(
            json.dumps(rm, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
        g = rm['charts'].get('grossing', {})
        regions_idx.append({'key': key, 'name': name, 'type': 'region', 'members': members,
                            'num_days': g.get('num_days', 0), 'num_games': g.get('num_games', 0)})
        built[key] = (rm, name, 'region')
    (MARKETS_OUT / 'index.json').write_text(
        json.dumps({'generated': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'majors': majors, 'regions': regions_idx, 'countries': singles,
                    # 하위호환: 옛 프론트가 읽던 평면 리스트도 유지(개별 국가 전체)
                    'countries_flat': [{'country': e['key']} for e in (majors + singles)]},
                   ensure_ascii=False), encoding='utf-8')
    # 장르×시장 비교 매트릭스(히트맵용)
    matrix = build_genre_matrix(built)
    (MARKETS_OUT / 'genre_matrix.json').write_text(
        json.dumps(matrix, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f"[OK] 다국가 집계: 주요 {len(majors)} + 지역 {len(regions_idx)} + 개별 {len(singles)}"
          f" · 매트릭스 {len(matrix['markets'])}시장×{len(matrix['genres'])}장르 → {MARKETS_OUT}")
    build_genre_audit(all_games)


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
    brief_file = Path('data') / 'ai_brief.json'
    if brief_file.exists():
        try:
            out['ai_brief'] = json.loads(brief_file.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"[WARN] ai_brief 로드 실패: {e}")
    DOCS_DIR.mkdir(exist_ok=True)
    OUT_FILE.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f"[OK] {OUT_FILE} 생성")
    print(f"     매출(grossing): {grossing['num_games']}게임 · {grossing['num_days']}일")
    print(f"     인기(free): {free['num_games']}게임 · {free['num_days']}일")
    print(f"     퍼블리셔: 매출 {len(grossing['publishers']['list'])}곳 · 인기 {len(free['publishers']['list'])}곳")
    try:
        build_markets()
    except Exception as e:
        print(f"[WARN] 다국가 집계 실패: {e}")
    return out


if __name__ == '__main__':
    build()
