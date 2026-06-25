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

# AppMagic L2 서브장르(영문) → 한글(통용 표기). 표준약어(MMORPG·MOBA·4X·FPS 등)는 영문 유지. 미매핑은 영문 그대로.
KOR_SUB = {
    # 롤플레잉
    'Idle RPG': '방치형RPG', 'MMORPG': 'MMORPG', 'Team Battler': '팀배틀러', 'Roguelike': '로그라이크',
    'Action Roguelike': '액션 로그라이크', 'Action RPG (ARPG)': '액션RPG', 'Action RPG': '액션RPG',
    'Puzzle RPG': '퍼즐RPG', 'Tactical RPG': '택틱스RPG', 'Empire Building': '제국건설',
    'Open World RPG': '오픈월드RPG', 'Open World': '오픈월드', 'Action RPG/MMORPG': '액션RPG',
    'Text-Based RPG': '텍스트RPG', 'Turn-Based RPG': '턴제RPG', 'Survival RPG': '서바이벌RPG',
    'Survival Roguelike': '서바이벌 로그라이크', 'Gacha': '수집형',
    # 퍼즐
    'Match-3': '매치3', 'Match 3': '매치3', 'Match-3: Tile': '매치3 타일', 'Match 3D': '매치3D',
    'Match-3 PvP': '매치3 PvP', 'Merge': '머지', 'Block Puzzle': '블록퍼즐', 'Word Puzzle': '워드퍼즐',
    'Bubble Shooter': '버블슈터', 'Sudoku': '스도쿠', 'Trivia': '퀴즈', 'Physics Puzzle': '물리퍼즐',
    'Logic Puzzle': '로직퍼즐', 'Jigsaw Puzzle': '직소퍼즐', 'Brick Breaker': '벽돌깨기',
    'Match-2 Blast': '매치2 블라스트', 'Coloring': '컬러링', 'Sort Puzzle': '소트퍼즐',
    'Connect Puzzle': '커넥트퍼즐', 'Nonogram': '노노그램', 'Minesweeper': '지뢰찾기', 'Maze': '미로',
    'Find The Difference': '틀린그림찾기', 'Draw Line Puzzle': '라인퍼즐', 'Math Puzzle': '수학퍼즐',
    'Fill & Organize': '정리퍼즐', 'Chain Puzzle': '체인퍼즐', 'Jam Puzzle': '잼퍼즐',
    'Power Level Puzzle': '파워퍼즐', 'Puzzle: Coloring': '컬러링퍼즐', 'Swipe-To-Move': '스와이프퍼즐',
    'Rope Puzzle': '로프퍼즐',
    # 전략
    '4X Strategy': '4X', '4X': '4X', 'Real Time Strategy (RTS)': 'RTS', 'MOBA': 'MOBA',
    'Card Battler': '카드배틀러', 'Tactics': '택틱스', 'Turn-Based Strategy (TBS)': 'TBS',
    'Tower Defense': '타워디펜스', 'Build & Battle': '건설·배틀', 'Auto Battler': '오토배틀러',
    'Auto Chess': '오토체스', 'CCG (Collectible Card Games)': '수집형카드(CCG)', 'CCG': '수집형카드(CCG)',
    'Real Time Tactics (RTT)': 'RTT', 'Turn-Based Tactics (TBT)': 'TBT', 'Takeover': '점령전',
    # 카지노
    'Slots': '슬롯', 'Casino Card Games': '카지노 카드', 'Bingo': '빙고', 'Poker': '포커',
    'Mahjong': '마작', 'Roulette': '룰렛', 'Fish Hunter': '피쉬헌터', 'Plinko': '플린코',
    'Crash': '크래시', 'Coin Looter': '코인루터', 'Pachinko': '파친코', 'Scratch Cards': '스크래치카드',
    'Casino Domino': '카지노 도미노', 'Coin Pusher': '코인푸셔', 'Claw Machine': '인형뽑기', 'Keno': '키노',
    'Teen Patti': '틴파티', 'Okey': '오케이', 'Rummy': '러미', 'Baloot': '발롯', 'Durak': '두락',
    # 시뮬레이션
    'Tycoon/Management': '타이쿤·경영', 'Tycoon': '타이쿤', 'Vehicle Simulator': '차량 시뮬',
    'Sandbox': '샌드박스', 'Farming': '팜', 'Life Sim': '인생 시뮬', 'Fashion & Dress Up': '드레스업',
    'Time Management': '타임매니지먼트', 'Dating Sim': '연애 시뮬', 'Job Simulator': '직업 시뮬',
    'Animal Simulator': '동물 시뮬', 'Virtual Pet': '가상펫', 'Citybuilder': '도시건설',
    'Home Design': '홈디자인', 'Fishing Simulator': '낚시 시뮬', 'Idol Training': '아이돌 육성',
    'Breeding': '육성', 'Satisfaction': '힐링', 'Simulator: Dance': '댄스 시뮬', 'Idle': '방치형',
    # 액션
    'Platformer': '플랫포머', 'Action-Adventure': '액션 어드벤처', 'Fighting': '대전격투',
    'Survival Horror': '서바이벌 호러', "Shoot 'em Up": '슈팅', 'Stealth': '스텔스',
    "Beat 'em Up": '비트앰업', 'Brawl': '브롤', 'Artillery Shooter': '포격 슈팅',
    'Asymmetric Battle': '비대칭 대전', 'Melee Battle Royale': '근접 배틀로얄',
    # 아케이드
    'Clicker/Idle': '클리커·방치형', 'Idle Arcade': '방치형 아케이드', 'Rhythm': '리듬',
    '.io': 'IO', 'Pinball': '핀볼', 'Eat & Grow': '잡아먹기', 'Slicing': '슬라이싱',
    'Destruction': '파괴', 'Arcade Fishing': '아케이드 낚시', 'Melee Arena': '근접 아레나',
    'Timing': '타이밍', 'Ballz-like': '볼즈류',
    # 슈팅
    'First-Person Shooter (FPS)': 'FPS', 'Third-Person Shooter (TPS)': 'TPS', 'Battle Royale': '배틀로얄',
    'Tactical Shooter': '택티컬 슈터', 'Sniper': '스나이퍼', 'Hero Shooter': '히어로 슈터',
    'Looter Shooter': '루터 슈터', 'Cover Shooter': '커버 슈터', 'Survival Shooter': '서바이벌 슈터',
    'Extraction Shooter': '익스트랙션 슈터', 'Vehicle Shooter': '차량 슈팅', 'Hunting': '헌팅',
    'Top-Down Shooter (TDS)': 'TDS',
    # 테이블탑
    'Card Games': '카드', 'Board Games': '보드', 'Dice': '주사위', 'Mahjong Solitaire': '마작 솔리테어',
    'Domino': '도미노', 'Carrom': '캐롬', 'Sea Battle': '해전', 'Solitaire': '솔리테어',
    'Chess': '체스', 'Ludo': '루도', 'Backgammon': '백개먼',
    # 어드벤처
    'Quest': '퀘스트', 'Hidden Object': '히든오브젝트', 'Interactive Story': '인터랙티브 스토리',
    'Survival': '서바이벌',
    # 레이싱
    'Arcade Racing': '아케이드 레이싱', 'Simulation Racing': '시뮬 레이싱',
    'Racing: Mixed/Other Vehicles': '레이싱(기타)', 'Driving School': '운전 연수',
    # 스포츠
    'Arcade Sports': '아케이드 스포츠', 'Simulation Sports': '시뮬 스포츠', 'Sports Manager': '스포츠 경영',
    # 키즈
    'Kids: Educational': '키즈 교육', 'Kids: Simulator': '키즈 시뮬', 'Kids: Coloring & Drawing': '키즈 색칠',
    'Kids: Fashion & Beauty': '키즈 패션', 'Kids: Activity': '키즈 액티비티', 'Kids: Cooking & DIY': '키즈 요리',
    # 파티
    'Truth or Dare': '진실게임', 'Mafia/Betrayal': '마피아', 'Mini Games': '미니게임',
    'Interactive Guessing': '추측게임', 'Party Royale': '파티 로얄', 'Party': '파티',
    # 기타 공통
    'Hypercasual': '하이퍼캐주얼', 'Runner': '러너', 'Io': 'IO',
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


AM_TAGS = 'https://appmagic.rocks/api/v2/tags'


def fetch_taxonomy(session=None, timeout=20):
    """AppMagic 전체 games 장르 택소노미 → {id: {'name', 'parent'}}. 한 번 호출로 전 트리. 실패 시 {}."""
    if requests is None:
        return {}
    s = session or requests
    try:
        r = s.get(AM_TAGS, params={'type': 'games'}, timeout=timeout,
                  headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        r.raise_for_status()
        data = (r.json() or {}).get('data') or []
        return {t['id']: {'name': t.get('name', ''), 'parent': (t.get('parent_ids') or [None])[0]}
                for t in data if t.get('type') == 'games' and 'id' in t}
    except Exception as e:
        print('[WARN] AppMagic 택소노미 조회 실패:', e)
        return {}


def _path_of(leaf_name, taxo, byname):
    """리프 이름 → (top_en, l2_en, path_en[루트→리프]). 택소노미에서 부모를 거슬러 올라가 경로 복원."""
    tid = byname.get(leaf_name)
    if tid is None:
        return leaf_name, leaf_name, [leaf_name]
    ch, seen = [], set()
    while tid is not None and tid in taxo and tid not in seen:
        seen.add(tid)
        ch.append(taxo[tid]['name'])
        tid = taxo[tid]['parent']
    ch.reverse()
    if not ch:
        return leaf_name, leaf_name, [leaf_name]
    return ch[0], (ch[1] if len(ch) > 1 else ch[0]), ch


def apply_l2(cache, taxo, log=print):
    """캐시 각 항목의 저장 리프(sub_en/leaf_en)에서 L2(루트의 직계 자식)와 전체 경로를 도출,
    genre·sub = L2(우리 모든 장르의 디폴트), top = L1, path_en = 전체 경로로 세팅. 택소노미 기반 → 재조회 0.
    신규·기존(deepest leaf 저장분) 모두 통일 처리. 반환: 갱신 항목 수."""
    if not taxo:
        log('[WARN] 택소노미 없음 — L2 적용 건너뜀(top 유지)')
        return 0
    byname = {}
    for tid, v in taxo.items():
        byname.setdefault(v['name'], tid)
    n = 0
    for k, e in cache.items():
        if k == '__meta' or not isinstance(e, dict) or not e.get('top'):
            continue
        leaf = e.get('leaf_en') or e.get('sub_en') or ''
        if not leaf:
            continue
        top_en, l2_en, path = _path_of(leaf, taxo, byname)
        e['top'] = kor_top(top_en)
        e['genre'] = kor_sub(l2_en)   # ← 메인 장르 = L2
        e['sub'] = kor_sub(l2_en)
        e['l2_en'] = l2_en
        e['path_en'] = path
        n += 1
    log(f'[OK] L2 적용: {n}개 항목 genre=L2로 매핑(전체 경로 보존)')
    return n


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
