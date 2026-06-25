#!/usr/bin/env python3
"""AppMagic 기반 장르 라벨러 — 업계표준 분류를 trackId로 1회 조회 → 캐시 고정.

방침(사용자 결정): 자체 분류는 폐기하고 AppMagic 분류기준을 그대로 따른다.
- 소스: AppMagic 공개 검색 API `/api/v2/search?name={trackId}`.
  반환 tags[] 중 type=='games'(장르 계층) · 'meta'(미드코어/하드코어) ·
  'themes'/'settings'/'artstyles'를 사용한다.
- 키: trackId(=앱스토어 숫자ID, RSS im:id). 게임당 1회 조회 → data/genre_appmagic.json 캐시(영구).
- 라벨은 한글 매핑(KOR_*). 미매핑 라벨은 영문 유지(차후 확장).
- 매칭은 store_application_ids에 trackId가 들어있는 후보를 정확히 고른다(동명 게임 오인 방지).
"""
import datetime as _dt
import json
import re
import time

try:
    import requests
except Exception:  # 빌드 외 환경 보호
    requests = None

AM_SEARCH = 'https://appmagic.rocks/api/v2/search'

# AppMagic 상위 게임장르(영문) → 한글
KOR_TOP = {
    'RPG': '롤플레잉', 'Strategy': '전략', 'Puzzle': '퍼즐', 'Action': '액션',
    'Simulation': '시뮬레이션', 'Casual': '캐주얼', 'Adventure': '어드벤처',
    'Sports': '스포츠', 'Racing': '레이싱', 'Card': '카드', 'Board': '보드',
    'Casino': '카지노', 'Arcade': '아케이드', 'Shooter': '슈팅', 'Tabletop': '테이블탑',
    'Music': '음악·리듬', 'Educational': '교육', 'Trivia': '퀴즈', 'Word': '워드',
    'Lifestyle': '라이프스타일', 'Hypercasual': '하이퍼캐주얼', 'Platformer': '플랫포머',
    'Fighting': '대전격투', 'Sandbox': '샌드박스', 'Geolocation': '위치기반', 'Rhythm': '리듬',
}

# AppMagic 서브장르(영문) → 한글(통용 표기). 없으면 영문 유지.
KOR_SUB = {
    'Roguelike': '로그라이크', 'Action Roguelike': '액션 로그라이크',
    'MMORPG': 'MMORPG', 'Open World': '오픈월드', 'Turn-Based RPG': '턴제RPG',
    'Action RPG': '액션RPG', 'Puzzle RPG': '퍼즐RPG', 'Idle RPG': '방치형RPG',
    'Survival RPG': '서바이벌RPG', 'Gacha': '수집형', 'Survival': '서바이벌',
    '4X': '4X', 'MOBA': 'MOBA', 'Auto Battler': '오토배틀러',
    'Tower Defense': '타워디펜스', 'Build & Battle': '건설·배틀',
    'Match-3': '매치3', 'Match 3': '매치3', 'Bubble Shooter': '버블슈터',
    'Merge': '머지', 'Block Puzzle': '블록퍼즐', 'Word Puzzle': '워드퍼즐',
    'Idle': '방치형', 'Tycoon': '타이쿤', 'Farming': '팜', 'Sandbox': '샌드박스',
    'Battle Royale': '배틀로얄', 'FPS': 'FPS', 'Shoot \'em Up': '슈팅',
    'Hypercasual': '하이퍼캐주얼', 'Solitaire': '솔리테어', 'Slots': '슬롯',
    'Card Battler': '카드배틀러', 'CCG': '수집형카드', 'Platformer': '플랫포머',
    'Party': '파티', 'Runner': '러너', 'Io': 'IO',
}

# 게임 난이도/타깃(AppMagic meta) → 한글
KOR_TIER = {'Casual': '캐주얼', 'Midcore': '미드코어', 'Hardcore': '하드코어'}


def kor_top(en):
    # AppMagic은 일부 상위장르에 ' Games' 접미어를 붙임(Sports Games·Geolocation Games 등) → 정규화 후 매핑.
    en = re.sub(r'\s+Games$', '', (en or '').strip())
    return KOR_TOP.get(en, en)


def kor_sub(en):
    return KOR_SUB.get(en, en)


def parse_tags(app):
    """AppMagic application dict → {top, sub, tier, themes, settings, *_en}.
    games 태그의 parent_ids로 계층을 세워 상위(루트)·서브(가장 깊은 leaf)를 고른다."""
    tags = app.get('tags') or []
    games = [t for t in tags if t.get('type') == 'games']
    byid = {t.get('id'): t for t in games}

    def depth(t):
        d, cur, seen = 0, t, set()
        while cur and cur.get('parent_ids'):
            p = cur['parent_ids'][0]
            if p in seen:
                break
            seen.add(p)
            cur = byid.get(p)
            d += 1
        return d

    roots = [t for t in games if not t.get('parent_ids')]
    top_en = (roots[0]['name'] if roots else (games[0]['name'] if games else ''))
    # 서브: 깊이 큰 순 → priority 작은 순. 'X: Other' 류는 후순위(상위 카테고리만 의미).
    cand = sorted(games, key=lambda t: (-depth(t), t.get('priority', 9)))
    sub_en = ''
    for t in cand:
        nm = t.get('name', '')
        if nm == top_en:
            continue
        if nm.endswith(': Other') or nm.endswith('Other'):
            if not sub_en:
                sub_en = nm.replace(': Other', '').replace('Other', '').strip()
            continue
        sub_en = nm
        break
    if not sub_en and cand:
        sub_en = cand[0].get('name', '').replace(': Other', '').strip()

    tier_en = next((t.get('name') for t in tags
                    if t.get('type') == 'meta' and t.get('name') in KOR_TIER), '')
    themes = [t.get('name') for t in tags if t.get('type') == 'themes']
    settings = [t.get('name') for t in tags if t.get('type') == 'settings']
    return {
        'top_en': top_en, 'sub_en': sub_en, 'tier_en': tier_en,
        'top': kor_top(top_en), 'sub': kor_sub(sub_en), 'tier': KOR_TIER.get(tier_en, tier_en),
        'themes': themes, 'settings': settings,
    }


def fetch_one(track_id, session=None, timeout=15):
    """trackId로 AppMagic 조회 → 라벨 dict 또는 None(미발견). 네트워크 오류는 예외 전파(캐시 안 함)."""
    s = session or requests
    r = s.get(AM_SEARCH, params={'name': str(track_id), 'limit': 5}, timeout=timeout,
              headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
    r.raise_for_status()
    apps = (r.json() or {}).get('applications') or []
    tid = str(track_id)
    app = next((a for a in apps
                if tid in [str(x) for x in (a.get('store_application_ids') or [])]), None)
    if app is None:
        app = apps[0] if apps else None
    if app is None:
        return None
    res = parse_tags(app)
    res['am_id'] = app.get('id')
    return res


def label_all(track_ids, cache, sleep=2.0, max_new=60, abort_after=3, cooldown_h=48, log=print):
    """캐시에 없는 trackId만 AppMagic을 '아주 정중하게' 조회 → cache 채움(in-place).
    AppMagic은 대량 자동조회를 차단(410 Gone)하고, 반복하면 영구차단 위험이 있으므로 발자국 최소화:
      · 런당 max_new개 소량만, 느리게(sleep초)
      · 연속 abort_after회 실패=차단으로 보고 즉시 중단 + cooldown_h시간 '쿨다운'(그동안 AppMagic 안 두드림)
      · 쿨다운/캐시는 영구 → 며칠~몇 주에 걸쳐 안전하게 누적. 미발견은 {'miss':1}로 1회만.
    cache['__meta']['blocked_until']에 쿨다운 만료시각 저장. 반환: (신규 라벨, 미발견)."""
    if requests is None:
        log('[WARN] requests 없음 — AppMagic 라벨 건너뜀')
        return 0, 0
    meta = cache.get('__meta') or {}
    now = _dt.datetime.utcnow()
    bu = meta.get('blocked_until')
    if bu:
        try:
            if now < _dt.datetime.fromisoformat(bu):
                log(f'[INFO] AppMagic 차단 쿨다운 중(~{bu}Z) — 이번 실행 라벨 건너뜀(영구차단 회피)')
                return 0, 0
        except Exception:
            pass
    sess = requests.Session()
    new = miss = consec = 0
    todo = [str(t) for t in track_ids if str(t or '') and str(t) not in cache and str(t) != '__meta']
    for tid in todo:
        if new + miss >= max_new:
            log(f'[INFO] AppMagic 런당 상한({max_new}) — 나머지 {len(todo) - new - miss}개는 다음 실행에서')
            break
        try:
            r = fetch_one(tid, sess)
            consec = 0
            if r and r.get('top'):
                cache[tid] = r
                new += 1
            else:
                cache[tid] = {'miss': 1}
                miss += 1
        except Exception as e:
            consec += 1
            log(f'[WARN] AppMagic 조회 실패 {tid}: {e}')
            if consec >= abort_after:
                until = (now + _dt.timedelta(hours=cooldown_h)).isoformat()
                meta['blocked_until'] = until
                cache['__meta'] = meta
                log(f'[WARN] 연속 {consec}회 실패 — 차단 판단. {cooldown_h}h 쿨다운(~{until}Z) 후 재시도')
                break
        time.sleep(sleep)
    log(f'[OK] AppMagic 라벨: 신규 {new} · 미발견 {miss} · 남은 {max(0, len(todo) - new - miss)} · 캐시 {len([k for k in cache if k != "__meta"])}')
    return new, miss


# 밤탈출-49일 실제 응답(요약)으로 파싱 검증 — 네트워크 없이.
_SAMPLE = {'tags': [
    {'id': 243582, 'name': 'Roguelike', 'priority': 0, 'parent_ids': [89], 'type': 'games'},
    {'id': 243425, 'name': 'Stylized', 'priority': 3, 'parent_ids': [], 'type': 'artstyles'},
    {'id': 243941, 'name': 'Action Roguelike: Other', 'priority': 0, 'parent_ids': [243991], 'type': 'games'},
    {'id': 89, 'name': 'RPG', 'priority': 0, 'parent_ids': [], 'type': 'games'},
    {'id': 3, 'name': 'Games', 'priority': 0, 'parent_ids': [], 'type': 'domain'},
    {'id': 243242, 'name': 'Fantasy', 'priority': 0, 'parent_ids': [], 'type': 'settings'},
    {'id': 243250, 'name': 'Horror', 'priority': 0, 'parent_ids': [], 'type': 'themes'},
    {'id': 243571, 'name': 'Midcore', 'priority': 0, 'parent_ids': [], 'type': 'meta'},
    {'id': 243991, 'name': 'Action Roguelike', 'priority': 0, 'parent_ids': [243582], 'type': 'games'},
    {'id': 244485, 'name': 'Urban Fantasy', 'priority': 0, 'parent_ids': [], 'type': 'settings'},
]}


def _selftest():
    r = parse_tags(_SAMPLE)
    exp = {'top': '롤플레잉', 'sub': '액션 로그라이크', 'tier': '미드코어'}
    bad = {k: (r.get(k), v) for k, v in exp.items() if r.get(k) != v}
    if bad or 'Horror' not in r['themes'] or 'Fantasy' not in r['settings']:
        print('[SELFTEST FAIL]', bad, '| themes', r['themes'], '| settings', r['settings'])
        return 1
    print('[SELFTEST OK] 밤탈출 → 롤플레잉/액션 로그라이크/미드코어 + 테마 Horror·배경 Fantasy')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(_selftest())
