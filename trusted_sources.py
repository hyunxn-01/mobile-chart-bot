# -*- coding: utf-8 -*-
"""신뢰 출처 화이트리스트 (#11 AI 브리핑 '왜 움직였나' 근거용).
원칙: 편집 뉴스 섹션만 채택 — 게시판·댓글·소셜·위키는 제외(루머/2차).
- TRUSTED_DOMAINS: 웹검색 allowed_domains로 그대로 사용(도메인 단위 1차 필터).
- BLOCK_PATH_PATTERNS: 혼합 사이트(뉴스+커뮤니티)의 커뮤니티 경로를 인용에서 제외(경로 단위 2차 필터).
- BLOCK_DOMAINS: 순수 커뮤니티·소셜·위키 — 절대 인용 금지.
사용자 승인 2026-06-25.
"""

# Tier B(글로벌 정론지) + Tier C(모바일/시장 데이터 분석) + 국내 게임 정론지.
TRUSTED_DOMAINS = [
    # 글로벌 업계 정론지(B2B·뉴스)
    'gamesindustry.biz', 'gamesbeat.com', 'gamedeveloper.com',
    'pocketgamer.biz', 'mobilegamer.biz', 'videogameschronicle.com',
    'eurogamer.net', 'gamespot.com', 'ign.com',
    # 모바일/시장 데이터 분석사(수치 근거)
    'sensortower.com', 'nikopartners.com', 'gamerefinery.com',
    'naavik.co', 'deconstructoroffun.com', 'wnhub.io',
    # 국내 게임 전문 정론지(혼합 사이트는 경로 필터로 게시판 제외)
    'inven.co.kr', 'thisisgame.com', 'gamemeca.com', 'gamefocus.co.kr',
    'tgdaily.co.kr', 'khgames.co.kr', 'dailygame.co.kr', 'dailyesports.com',
    'gametoc.co.kr', 'game.donga.com', 'gameshot.net', 'gamechosun.co.kr',
]

# 커뮤니티/게시판/댓글 경로 패턴 — URL에 포함되면 출처에서 제외(혼합 사이트 안전망).
BLOCK_PATH_PATTERNS = [
    '/board', '/bbs', '/community', '/forum', '/talk', '/comment',
    '/free', '/lounge', '/dataninfo', 'board=', '/maniadb', '/userpan',
]

# 순수 커뮤니티·소셜·편집가능 위키 — 도메인째 제외(근거로 인용 불가, 단서로만).
BLOCK_DOMAINS = [
    'ruliweb.com', 'dcinside.com', 'fmkorea.com', 'arca.live', 'clien.net',
    'reddit.com', 'namu.wiki', 'wikipedia.org', 'quora.com',
    'youtube.com', 'youtu.be', 'twitch.tv', 'x.com', 'twitter.com',
    'facebook.com', 'instagram.com', 'tiktok.com', 'threads.net',
]


def _host(url):
    """URL → 호스트(소문자, 'www.' 제거)."""
    try:
        from urllib.parse import urlparse
        h = (urlparse(url).hostname or '').lower()
        return h[4:] if h.startswith('www.') else h
    except Exception:
        return ''


def is_trusted_source(url):
    """신뢰 출처 여부: 화이트리스트 도메인 + 차단도메인 아님 + 커뮤니티 경로 아님."""
    if not url or not isinstance(url, str):
        return False
    u = url.strip()
    if not u.lower().startswith(('http://', 'https://')):
        return False
    host = _host(u)
    if not host:
        return False
    # 차단 도메인(서브도메인 포함)
    for bd in BLOCK_DOMAINS:
        if host == bd or host.endswith('.' + bd):
            return False
    # 화이트리스트 도메인(서브도메인 포함)에 속해야 함
    ok = any(host == d or host.endswith('.' + d) for d in TRUSTED_DOMAINS)
    if not ok:
        return False
    # 커뮤니티/게시판 경로 차단
    low = u.lower()
    if any(p in low for p in BLOCK_PATH_PATTERNS):
        return False
    return True
