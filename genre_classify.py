#!/usr/bin/env python3
"""게임 서브장르 분류기 — app_id 기준 1회 판정 → 전역 일관(모든 시장 동일).

설계
- 우선순위: (1) 큐레이트 맵(유명 게임) → (2) 다국어 키워드 규칙(한/영/중) →
  (3) AI 폴백(워크플로, ANTHROPIC_API_KEY 있을 때) → (4) API 장르 리맵(이상장르 정리).
- 결과는 (상위장르, 서브장르, 출처). 상위장르까지 재판정하므로 API의 오분류
  (클래시 오브 클랜→'액션' 등)·이상장르(가족·음악)를 바로잡는다.
- build_dashboard/chart_collector가 app_id별로 결과를 data/genre_class.json에 캐시 →
  같은 app_id는 어느 시장·어느 날이든 같은 장르(일관성·비결정 AI 무관).

업계 표준 택소노미(GameRefinery·Sensor Tower류) — 큰 장르만 세분, 작은 장르는 평면.
"""
import re

# 상위장르 → 서브장르(빈 리스트 = 평면, 세분 안 함)
TAXONOMY = {
    '롤플레잉': ['MMORPG', '수집형RPG', '방치형RPG', '액션RPG'],
    '전략':    ['4X·SLG', 'MOBA', '디펜스'],
    '퍼즐':    ['매치3', '머지', '기타퍼즐'],
    '시뮬레이션': ['방치형·타이쿤', '팜·샌드박스'],
    '액션':    ['슈팅', '기타액션'],
    '캐주얼': [], '어드벤처': [], '스포츠': [], '레이싱': [],
    '보드': [], '카드': [], '카지노': [],
}

# 게임차트에 안 어울리는 API 장르 → 정상 장르로 리맵(폴백 시)
REMAP = {'가족': '캐주얼', '음악': '캐주얼', '주사위': '보드',
         '교육': '캐주얼', '트리비아': '캐주얼', '단어': '퍼즐', '기타': '캐주얼'}


def _norm(s):
    return re.sub(r"[\s:·\-_,.!?'\"()\[\]/]+", '', (s or '').lower())


# 큐레이트: 정규화 타이틀 → (상위, 서브). 차트 상위 유명 게임(전역 일관 보장의 핵심).
CURATED = {
    # MMORPG
    '리니지m': ('롤플레잉', 'MMORPG'), '리니지w': ('롤플레잉', 'MMORPG'),
    '오딘발할라라이징': ('롤플레잉', 'MMORPG'), '오딘': ('롤플레잉', 'MMORPG'),
    '나이트크로우': ('롤플레잉', 'MMORPG'), '로한m': ('롤플레잉', 'MMORPG'),
    '아키에이지워': ('롤플레잉', 'MMORPG'), '뮤모나크': ('롤플레잉', 'MMORPG'),
    '천녀유혼': ('롤플레잉', 'MMORPG'), '연운십육성': ('롤플레잉', 'MMORPG'),
    '문도': ('롤플레잉', 'MMORPG'), '몽환서유': ('롤플레잉', 'MMORPG'),
    # 수집형RPG(가챠)
    '승리의여신니케': ('롤플레잉', '수집형RPG'), '니케': ('롤플레잉', '수집형RPG'),
    '블루아카이브': ('롤플레잉', '수집형RPG'), '우마무스메프리티더비': ('롤플레잉', '수집형RPG'),
    '우마무스메': ('롤플레잉', '수집형RPG'), '명일방주': ('롤플레잉', '수집형RPG'),
    '원신': ('롤플레잉', '수집형RPG'), '원신공월지가': ('롤플레잉', '수집형RPG'),
    '명조': ('롤플레잉', '수집형RPG'), '붕괴스타레일': ('롤플레잉', '수집형RPG'),
    '젠레스존제로': ('롤플레잉', '수집형RPG'), '절구영': ('롤플레잉', '수집형RPG'),
    '예무지샤': ('롤플레잉', '수집형RPG'), '페이트그랜드오더': ('롤플레잉', '수집형RPG'),
    # 방치형RPG
    '버섯커키우기': ('롤플레잉', '방치형RPG'), 'afk저니': ('롤플레잉', '방치형RPG'),
    '레전드오브슬라임': ('롤플레잉', '방치형RPG'), '세븐나이츠키우기': ('롤플레잉', '방치형RPG'),
    # 액션RPG
    '던전앤파이터모바일': ('롤플레잉', '액션RPG'), '던전앤파이터오리진': ('롤플레잉', '액션RPG'),
    '디아블로이모탈': ('롤플레잉', '액션RPG'),
    # MOBA
    '왕자영요': ('전략', 'MOBA'), '리그오브레전드와일드리프트': ('전략', 'MOBA'),
    '펜타스톰': ('전략', 'MOBA'), '모바일레전드뱅뱅': ('전략', 'MOBA'),
    # 슈팅
    '배틀그라운드모바일': ('액션', '슈팅'), '화평정영': ('액션', '슈팅'),
    '콜오브듀티모바일': ('액션', '슈팅'), '발로란트소스액션': ('액션', '슈팅'),
    '발로란트모바일': ('액션', '슈팅'), '크로스파이어': ('액션', '슈팅'),
    '삼각주작전': ('액션', '슈팅'), '브롤스타즈': ('액션', '기타액션'),
    # 4X·SLG
    '라스트워서바이벌': ('전략', '4X·SLG'), '화이트아웃서바이벌': ('전략', '4X·SLG'),
    '라이즈오브킹덤즈': ('전략', '4X·SLG'), '클래시오브클랜': ('전략', '4X·SLG'),
    '콜오브드래곤즈': ('전략', '4X·SLG'), '삼국지전략판': ('전략', '4X·SLG'),
    '솔토지빈': ('전략', '4X·SLG'), '삼국빙하시대': ('전략', '4X·SLG'),
    '삼국모정천하': ('전략', '4X·SLG'), '버섯커': ('롤플레잉', '방치형RPG'),
    # 매치3 / 퍼즐
    '로얄매치': ('퍼즐', '매치3'), '캔디크러시사가': ('퍼즐', '매치3'),
    '가든스케이프': ('퍼즐', '매치3'), '홈스케이프': ('퍼즐', '매치3'),
    '몽환화원': ('퍼즐', '매치3'), '카이신샤오샤오러': ('퍼즐', '매치3'),
    '애니팡': ('퍼즐', '매치3'), '토온블라스트': ('퍼즐', '기타퍼즐'),
    '머지맨션': ('퍼즐', '머지'),
    # 보드/카드(중국 두디주·마작)
    '텐센트환러두디주': ('카드', ''), 'jj두디주': ('카드', ''), '투유두디주': ('카드', ''),
    '즈젠쓰촨마작': ('보드', ''), '삼국살': ('전략', '4X·SLG'),
    # 캐주얼/파티(가족 오분류 교정)
    '에그파티': ('캐주얼', ''), '거위거위오리': ('캐주얼', ''), '쿠키런킹덤': ('롤플레잉', '수집형RPG'),
    # 스포츠
    'fc축구세계': ('스포츠', ''), '위닝일레븐': ('스포츠', ''), 'fc모바일': ('스포츠', ''),
    # 어드벤처/기타
    'sky빛의아이들': ('어드벤처', ''), '제5인격': ('어드벤처', ''),
    '러브앤딥스페이스': ('시뮬레이션', ''), '광여야지련': ('시뮬레이션', ''),
    '포켓몬고': ('어드벤처', ''), '모노폴리고': ('보드', ''),
    '피파모바일': ('스포츠', ''), '쿠키런': ('액션', '기타액션'), '쿠키런오븐브레이크': ('액션', '기타액션'),
    # 영문 타이틀(미국 등 시장은 원제 영문) — 같은 게임의 타이틀 변형도 동일 장르로
    'clashofclans': ('전략', '4X·SLG'), 'clashroyale': ('전략', '디펜스'),
    'monopolygo': ('보드', ''), 'coinmaster': ('카지노', ''),
    'royalmatch': ('퍼즐', '매치3'), 'candycrushsaga': ('퍼즐', '매치3'), 'candycrush': ('퍼즐', '매치3'),
    'gardenscapes': ('퍼즐', '매치3'), 'homescapes': ('퍼즐', '매치3'),
    'roblox': ('시뮬레이션', '팜·샌드박스'), 'minecraft': ('시뮬레이션', '팜·샌드박스'),
    'brawlstars': ('액션', '기타액션'), 'pokemongo': ('어드벤처', ''),
    'pubgmobile': ('액션', '슈팅'), 'callofdutymobile': ('액션', '슈팅'),
    'genshinimpact': ('롤플레잉', '수집형RPG'), 'honkaistarrail': ('롤플레잉', '수집형RPG'),
    'whiteoutsurvival': ('전략', '4X·SLG'), 'lastwarsurvival': ('전략', '4X·SLG'), 'lastwar': ('전략', '4X·SLG'),
    'riseofkingdoms': ('전략', '4X·SLG'), 'eafcmobile': ('스포츠', ''), 'fifamobile': ('스포츠', ''),
    'cookierunkingdom': ('롤플레잉', '수집형RPG'), 'pokmonunite': ('전략', 'MOBA'),
}

# app_id 기준 큐레이트(지역판 변형 등 타이틀이 달라도 강제 일치 — 전역 일관 보강)
CURATED_APPID = {
    'com.supercell.magic': ('전략', '4X·SLG'), 'com.supercell.magic.china': ('전략', '4X·SLG'),
    'com.supercell.clashofclans': ('전략', '4X·SLG'),
    'com.tencent.smoba': ('전략', 'MOBA'), 'com.tencent.tmgp.pubgmhd': ('액션', '슈팅'),
    'com.tencent.tmgp.cod': ('액션', '슈팅'), 'com.tencent.tmgp.cf': ('액션', '슈팅'),
    'com.miHoYo.Yuanshen': ('롤플레잉', '수집형RPG'), 'com.miHoYo.Nap': ('롤플레잉', '수집형RPG'),
    'com.netease.party': ('캐주얼', ''), 'com.seayoo.ggd': ('캐주얼', ''),
}

# 키워드 규칙(제목·개발사 기준만 — 마케팅 설명문은 노이즈라 안 봄). 첫 매치 채택 → 특정적인 것 위로.
# 애매한 일반어(전략/액션/영웅/war/idle 단독)는 규칙에서 빼고 AI 폴백에 맡긴다(과매칭 방지).
RULES = [
    # 카지노·슬롯·포커·카드·낚시 (설명문 'win/전략' 때문에 4X로 오분류되던 것)
    # 카드(솔리테어·러미·스페이드)·마작·낚시는 규칙에서 뺀다 → Opus가 카드/보드로(애매한 경계는 AI에 위임)
    ('카지노', '', ['slot', '슬롯', 'slots', 'casino', '카지노', 'poker', '포커', 'holdem', '홀덤', 'baccarat', '바카라',
                   'roulette', '룰렛', 'blackjack', '블랙잭', 'bingo', '빙고', 'jackpot', 'vegas', '슬롯머신', 'teen patti']),
    # 스포츠
    ('스포츠', '', ['soccer', 'football', '축구', 'fifa', 'efootball', '위닝', 'baseball', '야구', 'basketball',
                   '농구', 'nba', 'golf', '골프', 'tennis', '테니스', 'bowling', '볼링', 'cricket', '크리켓']),
    # 레이싱
    ('레이싱', '', ['racing', '레이싱', '카트', 'kart', 'asphalt', '아스팔트', 'drift', '드리프트']),
    # 슈팅
    # 'shooter/shooting/슈팅' 일반어는 뺀다(버블슈터·아케이드 오매칭) → 명확한 FPS/배틀로얄 브랜드 + fps/sniper만
    ('액션', '슈팅', ['배틀그라운드', 'pubg', '吃鸡', '和平精英', '화평정영', 'call of duty', '콜 오브 듀티', '使命召唤',
                    'valorant', '발로란트', 'crossfire', '穿越火线', '크로스파이어', 'battlefield', '배틀필드', ' fps',
                    'sniper 3d', '스나이퍼', 'war robots', '三角洲', '삼각주', 'delta force', 'free fire', '프리파이어']),
    # MOBA / 오토배틀러
    ('전략', 'MOBA', ['moba', '왕자영요', '王者荣耀', 'penta', '펜타스톰', '전설대결', 'arena of valor', 'wild rift',
                     '와일드리프트', 'mobile legends', '모바일 레전드', '英雄联盟', '金铲铲', '금삽삽', 'auto chess', '오토체스']),
    # 머지
    ('퍼즐', '머지', ['merge', '머지', '合成', '合并']),
    # 매치3
    ('퍼즐', '매치3', ['match', '매치', '消消', '三消', '캔디', 'candy', 'royal match', '로얄 매치', 'gardenscape',
                     '가든스케이프', 'homescape', '홈스케이프', '애니팡', 'blast', '블라스트', 'bubble', '버블']),
    # 타이쿤/방치형 비즈니스(시뮬) — RPG보다 먼저
    ('시뮬레이션', '방치형·타이쿤', ['tycoon', '타이쿤', 'miner', 'mining', '채굴', 'factory', '공장', 'airport', '공항',
                              'planet', 'restaurant', '레스토랑', 'cafe', '카페', '경영', '商店', '자본주의', 'capitalist']),
    # 팜/샌드박스(시뮬)
    ('시뮬레이션', '팜·샌드박스', ['farm', '팜', '농장', 'sandbox', '샌드박스', 'minecraft', '마인크래프트', 'roblox',
                            '로블록스', '我的世界', 'craft', '크래프트', 'garden', '정원']),
    # MMORPG(제목 신호)
    ('롤플레잉', 'MMORPG', ['mmorpg', 'mmo', '오픈월드', 'open world', '开放世界', '리니지', 'lineage', '오딘', 'odin',
                         '검은사막', 'black desert', '로한', 'rohan', '天堂', '천하', '천녀', '연운', 'maplestory', '메이플',
                         'traha', 'tera', '아이온', 'aion', 'perfect world', '완미']),
    # 방치형RPG(idle + RPG 신호만, 단독 idle 금지)
    ('롤플레잉', '방치형RPG', ['idle rpg', 'idle hero', 'idle legend', 'idle sword', 'afk', '버섯커', 'slime master', '放置']),
    # 수집형RPG(가챠 신호)
    ('롤플레잉', '수집형RPG', ['gacha', '가챠', '니케', 'nikke', '블루 아카이브', 'blue archive', '우마무스메', '명일방주',
                          'arknights', '원신', 'genshin', '명조', 'wuthering', '붕괴', 'honkai', 'star rail', '스타레일',
                          'zenless', '젠레스', 'fgo', 'seven knights', '세븐나이츠', 'epic seven', '에픽세븐', '소녀전선']),
    # 액션RPG
    ('롤플레잉', '액션RPG', ['action rpg', '액션 rpg', '던전앤파이터', 'dnf', '地下城', '디아블로', 'diablo']),
    # 4X·SLG(제목의 강한 SLG 신호만)
    # 강한 SLG 신호만(survival/dynasty/conquer 등 일반어는 빼서 Opus에 위임)
    ('전략', '4X·SLG', ['kingdom', '킹덤', 'empire', '제국', '삼국', '3 kingdoms', 'warpath', 'last war', '라스트워',
                       'top war', 'whiteout', '화이트아웃', 'clash of', '클래시 오브', 'rise of kingdoms', 'age of empires',
                       'age of origins', 'civilization', '문명', '率土', 'evony', 'state of survival', 'puzzles & survival']),
    # 디펜스
    ('전략', '디펜스', ['tower defense', '타워 디펜스', '타워디펜스', '디펜스', 'defense', 'random dice', '랜덤 디펜스', '塔防']),
]


def classify(app, api_genre=''):
    """app(dict: title, title_kr, developer, notes, app_id) → (상위, 서브, 출처).
    출처 ∈ curated|rule|remap|fallback. AI 폴백은 워크플로에서 fallback 자리에 주입."""
    aid = app.get('app_id') or app.get('track_id') or ''
    if aid in CURATED_APPID:
        top, sub = CURATED_APPID[aid]
        return top, sub, 'curated'
    # 타이틀(한국어 또는 원제 영문) 정규화 매칭 — 시장 무관 동일 결과
    for title in (app.get('title_kr'), app.get('title')):
        key = _norm(title)
        if key and key in CURATED:
            top, sub = CURATED[key]
            return top, sub, 'curated'
    # 키워드는 제목·개발사에서만 찾는다(설명문은 흔한 단어가 많아 과매칭 → 제외).
    hay = ' '.join([app.get('title', ''), app.get('title_kr', ''), app.get('developer', '')]).lower()
    for top, sub, kws in RULES:
        if any(k.lower() in hay for k in kws):
            return top, sub, 'rule'
    g = (api_genre or app.get('genre') or '').strip()
    if g in REMAP:
        return REMAP[g], '', 'remap'
    if g in TAXONOMY:
        return g, '', 'fallback'
    return (REMAP.get(g, '캐주얼') or '캐주얼'), '', 'fallback'


AI_MODEL = 'claude-opus-4-8'


def ai_classify(items, client, model=AI_MODEL):
    """규칙으로 못 잡은 게임들을 Opus로 배치 분류 → {app_id: (top, sub)}.
    items: [{app_id,title,developer,notes}]. 택소노미 밖 응답은 버린다. 캐시·게이팅은 호출측."""
    if not items:
        return {}
    taxo = '\n'.join(f"- {t}: {'/'.join(subs) if subs else '(서브 없음)'}" for t, subs in TAXONOMY.items())
    lines = []
    for i, g in enumerate(items):
        desc = (g.get('notes') or '')[:300].replace('\n', ' ').replace('\t', ' ')
        lines.append(f"{i}\t{(g.get('title') or '')[:45]}\t{(g.get('developer') or '')[:30]}\t앱스토어:{g.get('api') or '-'}\t{desc}")
    prompt = (
        "다음 모바일 게임들을 아래 택소노미의 (상위장르, 서브장르)로 분류해라. "
        "업계 통용 기준이며, 서브가 없는 상위장르는 서브를 비워라. 확실치 않으면 가장 근접한 상위장르만. "
        "'앱스토어:'는 애플 분류로 참고만 하되(부정확할 수 있음) 실제 게임성으로 판단해라.\n\n"
        f"[택소노미]\n{taxo}\n\n[게임] (인덱스\\t제목\\t개발사\\t앱스토어장르\\t설명)\n" + '\n'.join(lines) +
        "\n\n[출력] 각 줄 '인덱스|상위|서브'만(서브 없으면 '인덱스|상위|'). 설명·머리말 금지.")
    try:
        msg = client.messages.create(model=model, max_tokens=3000,
                                     messages=[{'role': 'user', 'content': prompt}])
        text = ''.join(getattr(b, 'text', '') for b in msg.content)
    except Exception as e:
        print('[WARN] AI 분류 호출 실패:', e)
        return {}
    res, valid_tops = {}, set(TAXONOMY.keys())
    for ln in text.splitlines():
        p = ln.split('|')
        if len(p) < 2:
            continue
        try:
            idx = int(p[0].strip())
        except ValueError:
            continue
        if not (0 <= idx < len(items)):
            continue
        top = p[1].strip()
        sub = p[2].strip() if len(p) > 2 else ''
        if top not in valid_tops:
            continue
        if sub and sub not in TAXONOMY.get(top, []):
            sub = ''
        res[items[idx].get('app_id')] = (top, sub)
    return res


def _selftest():
    cases = [
        # API 상위장르 오분류 교정
        ({'title_kr': '클래시 오브 클랜'}, '액션', ('전략', '4X·SLG')),
        ({'title': 'Clash of Clans'}, '게임', ('전략', '4X·SLG')),                 # 영문 타이틀도 동일
        ({'app_id': 'com.supercell.magic.china', 'title_kr': '클래시 오브 클랜'}, '액션', ('전략', '4X·SLG')),  # 중국판 app_id
        ({'title_kr': '콜 오브 듀티 모바일'}, '전략', ('액션', '슈팅')),
        ({'title_kr': '원신'}, '어드벤처', ('롤플레잉', '수집형RPG')),
        ({'title': 'Genshin Impact'}, '어드벤처', ('롤플레잉', '수집형RPG')),
        ({'title_kr': '왕자영요', 'app_id': 'com.tencent.smoba'}, '액션', ('전략', 'MOBA')),
        ({'title_kr': '에그파티'}, '가족', ('캐주얼', '')),
        ({'title_kr': 'QQ 댄스'}, '음악', ('캐주얼', '')),       # 음악 리맵
        # 서브장르
        ({'title_kr': '리니지M'}, '롤플레잉', ('롤플레잉', 'MMORPG')),
        ({'title_kr': '버섯커 키우기'}, '롤플레잉', ('롤플레잉', '방치형RPG')),
        ({'title': 'Royal Match'}, '게임', ('퍼즐', '매치3')),
        ({'title': 'Monopoly Go!'}, '게임', ('보드', '')),
        # 혼동 교정(제목 기준) — 설명문 안 보므로 오발동 방지
        ({'title': '88 Fortunes Casino Slots'}, '전략', ('카지노', '')),     # 4X로 오분류되던 카지노
        ({'title': 'Dream League Soccer 2026'}, '액션', ('스포츠', '')),       # 축구
        ({'title': 'Idle Miner Tycoon'}, '캐주얼', ('시뮬레이션', '방치형·타이쿤')),  # 방치형RPG 아님
        ({'title': 'Merge Dragons!'}, '어드벤처', ('퍼즐', '머지')),
        ({'title': 'Last War: Survival'}, '게임', ('전략', '4X·SLG')),         # 제목 신호로 SLG
    ]
    fails = []
    for app, api, exp in cases:
        got = classify(app, api)[:2]
        if got != exp:
            fails.append(f"  {app.get('title_kr') or app.get('title')}: api={api} 기대={exp} 결과={got}")
    # 시장 무관 일관성: 같은 게임이 시장별로 타이틀이 달라도 동일 결과
    kr = classify({'title_kr': '클래시 오브 클랜'}, '액션')[:2]
    us = classify({'title': 'Clash of Clans'}, '게임')[:2]
    cn = classify({'app_id': 'com.supercell.magic.china', 'title_kr': '클래시 오브 클랜'}, '액션')[:2]
    if not (kr == us == cn):
        fails.append(f"  [일관성] KR={kr} US={us} CN={cn} 불일치")
    if fails:
        print('[SELFTEST FAIL]'); print('\n'.join(fails)); return 1
    print('[SELFTEST OK] 14케이스 + 시장 일관성 통과(오분류 교정·이상장르 리맵·다국어·app_id)'); return 0


if __name__ == '__main__':
    import sys
    sys.exit(_selftest())
