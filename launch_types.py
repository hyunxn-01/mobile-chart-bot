"""신작 런칭 추이 유형 판정과 주간 브리핑용 자료 줄(2026-10-29, chart_collector._launch_digest가 부른다).
유형 기준은 2026-10-28 사용자와 정했다: 하락 기준 = 순위 구간 · 늦게 상승 = 지금도 유지 중일 때만 · 판정 시작 = D+14 ·
D+0 = 출시일, 늦은 출시는 시장마다 확인 뒤 반영. 시험과 정본 설명은 워크스페이스 견본/2026-10-28-실무활용(launch_types.py · brief_test.py ·
브리핑시험_점검기록.md)에 있고, 이 파일은 그 판정 · 자료 줄을 저장소 경로로 옮긴 것이다.

대상: 수집 시작 이후 출시, 그 시장 매출 차트에 한 번이라도 든 게임.
D+0: 앱스토어 출시일. 그 시장 인기 차트에 처음 든 날이 출시 14일 넘게 뒤이고 그날 인기 순위가 10위 안이면 '그 시장 늦은 출시'로 보고 그날을 D+0으로 한다.
순위 구간: 10위 안 · 11~30위 · 31~100위. '최근 7일'은 마지막 7일 가운데 100위 안에 든 날의 평균 순위.
판정 순서:
  1. D+14 미만, 또는 매출 차트에 처음 든 지 7일이 안 됨 → 관찰 중(첫 진입 전 날들을 '이탈'로 세지 않게, 2026-10-28 시험 중 보강 · 사용자 승인 2026-10-29)
  2. 최근 7일 가운데 4일 넘게 매출 100위 밖 → 차트 이탈
  3. 최근 7일 평균이 최고 순위보다 아래 구간 → 고점 뒤 하락
  4. 같은 구간이고, 최고 순위 30위 안을 D+21 뒤에 냈고, 첫 주(D+0~7) 최고 순위가 그보다 아래 구간이었음 → 늦게 상승
  5. 같은 구간이고 최고 순위 30위 안 → 상위권 유지
  6. 같은 구간이고 최고 순위 31~100위 → 중하위권 유지
자료: commit된 docs/markets/<시장>.json(수집 코드가 대시보드 빌드보다 먼저 돌아 전날 빌드분을 읽는다)."""
import json, datetime, statistics as st
from collections import Counter
from pathlib import Path

DOCS = Path('docs') / 'markets'
D = datetime.date.fromisoformat
OBSERVE, LATE_GAP, LATE_FREE_TOP, LATE_PEAK, NEW_DAYS = 14, 14, 10, 21, 92   # NEW_DAYS: 대시보드 '신작' 배지와 같은 기준(출시 3개월 미만)
tier = lambda r: 0 if r <= 10 else (1 if r <= 30 else 2)
TIER = ['10위 안', '11~30위', '31~100위']


def first_free(fr, aid):
    """그 시장 인기 차트에 처음 든 날과 그날 순위."""
    if not fr:
        return None, None
    L = fr['timeframes']['daily']['labels']; s = (fr['timeframes']['daily']['series'] or {}).get(aid) or []
    i = next((k for k, v in enumerate(s) if v is not None), None)
    return (L[i], s[i]) if i is not None else (None, None)


def judge(L, s, rl, fr, aid):
    """한 게임의 판정. 반환 dict(유형 · 근거 수치)."""
    last = D(L[-1]); d0 = D(rl); late = None
    fd, frk = first_free(fr, aid)
    if fd and (D(fd) - d0).days > LATE_GAP and frk is not None and frk <= LATE_FREE_TOP:
        late = (D(fd) - d0).days; d0 = D(fd)   # 그 시장 늦은 출시로 확인 → 그날을 D+0
    c = {}
    for i, v in enumerate(s):
        if v is not None and D(L[i]) >= d0:
            c[(D(L[i]) - d0).days] = v
    days = (last - d0).days
    w7 = s[-7:]; inn = [v for v in w7 if v is not None]; out7 = len(w7) - len(inn)
    f = dict(days=days, late=late, out7=out7, avg7=(st.mean(inn) if inn else None))
    if not c:
        f.update(peak=None, pd=None, type='차트 이탈' if days >= OBSERVE else '관찰 중'); return f
    peak = min(c.values()); pd = min(d for d, v in c.items() if v == peak)
    p7 = [v for v in s[-14:-7] if v is not None]
    f.update(peak=peak, pd=pd, d7=c.get(7), d14=c.get(14), d30=c.get(30), now=s[-1], first=min(c),
             prev7=(st.mean(p7) if p7 else None), top10=sum(1 for v in c.values() if v <= 10), charted=len(c))
    wk1 = [v for d, v in c.items() if d <= 7]; f['wk1'] = min(wk1) if wk1 else None
    if days < OBSERVE or days - f['first'] < 7: t = '관찰 중'
    elif out7 > 3 or not inn: t = '차트 이탈'
    elif tier(f['avg7']) > tier(peak): t = '고점 뒤 하락'
    elif peak <= 30 and pd > LATE_PEAK and (f['wk1'] is None or tier(f['wk1']) > tier(peak)): t = '늦게 상승'
    elif peak <= 30: t = '상위권 유지'
    else: t = '중하위권 유지'
    f['type'] = t; return f


def market_rows(cc):
    """그 시장의 수집 시작 이후 출시작 판정 목록과 수집 시작일."""
    x = json.loads((DOCS / f'{cc}.json').read_text(encoding='utf-8'))['charts']
    g, fr = x['grossing'], x.get('free')
    L = g['timeframes']['daily']['labels']; S = g['timeframes']['daily']['series']; start = L[0]
    rows = []
    for aid, m in g['games'].items():
        rl = m.get('release') or ''; s = S.get(aid) or []
        if not rl or rl < start or not any(v is not None for v in s):
            continue
        f = judge(L, s, rl, fr, aid)
        f.update(aid=aid, t=m.get('title_kr') or m.get('title') or aid, g=m.get('genre', ''), rl=rl, dev=m.get('developer') or '')
        rows.append(f)
    return rows, start


def launch_digest(cc):
    """주간 브리핑 자료에 붙일 '신작 런칭 추이' 한 줄. 차트인 신작 = 런칭 92일 안 · 매출 차트 첫 진입 7일 안,
    상위권 신작 = 런칭 92일 안 · 지금 30위 안(차트인 신작 제외). 기준값 · 정착 현황 · D+14 구간별 잔존 · 첫 진입 시점 · 유형 기준을 함께 넘긴다."""
    rows, start = market_rows(cc)
    md = lambda s: f"{int(s[5:7])}/{int(s[8:10])}"
    rk = lambda v: f"{v}위" if v is not None else '100위 밖'

    def who(r):
        g = r['g'] if r['g'] and r['g'] != '장르 없음' else ''
        return ' · '.join(x for x in [('세부 장르 ' + g) if g else '', r['dev']] if x)

    def line(r, full):
        late = f", 이 시장 늦은 출시로 확인되어 D+0은 출시 {r['late']}일 뒤" if r['late'] else ''
        base = (f"{r['t']}({who(r)}; {md(r['rl'])} 출시{late}; 지금 D+{r['days']}, 유형 {r['type']}; 지금 {rk(r['now'])}, 최고 {r['peak']}위(D+{r['pd']})"
                f"; 매출 차트 첫 진입 D+{r['first']}")
        if full:
            base += (f"; D+7 {rk(r['d7'])} · D+14 {rk(r['d14']) if r['days'] >= 14 else '아직'} · D+30 {rk(r['d30']) if r['days'] >= 30 else '아직'}"
                     f"; 최근 7일 평균 {r['avg7']:.1f}위(직전 7일 {('%.1f위' % r['prev7']) if r['prev7'] else '자료 없음'}); 차트에 든 {r['charted']}일 중 10위 안 {r['top10']}일")
        return base + ')'
    young = [r for r in rows if r['peak'] is not None and r['days'] < NEW_DAYS]
    entered = sorted([r for r in young if r['days'] - r['first'] < 7 and r['now'] is not None], key=lambda r: r['now'])
    top = sorted([r for r in young if r not in entered and r['now'] is not None and r['now'] <= 30], key=lambda r: r['now'])

    def med(d):
        elig = [r for r in rows if r['peak'] is not None and r['days'] >= d]
        inn = sorted(r[f'd{d}'] for r in elig if r.get(f'd{d}') is not None)
        m = (inn[len(inn) // 2] if len(inn) % 2 else (inn[len(inn) // 2 - 1] + inn[len(inn) // 2]) / 2) if inn else None
        return f"D+{d} {('%g위' % m) if m is not None else '자료 없음'}({len(elig)}개 중 {len(inn)}개가 그날 차트에 남음)"
    past14 = [r for r in rows if r['days'] >= 14]
    stay = [r for r in past14 if r['type'] != '차트 이탈']
    dist = ' · '.join(f'{k} {v}' for k, v in Counter(r['type'] for r in stay).most_common()) or '없음'

    def d14_tier(r):
        v = r.get('d14')
        return '100위 밖' if v is None else TIER[tier(v)]
    by14 = ' · '.join(f"{k} {sum(1 for r in past14 if d14_tier(r) == k and r['type'] != '차트 이탈')}/{sum(1 for r in past14 if d14_tier(r) == k)}"
                      for k in TIER + ['100위 밖'])
    early = [r for r in past14 if r['peak'] is not None and r['first'] <= 14]
    early_s = (f"D+14가 지난 {len(past14)}개 중 출시 14일 안에 매출 100위에 처음 든 게임 {len(early)}개"
               f"(그중 D+14 그날에도 100위 안 {sum(1 for r in early if r.get('d14') is not None)}개, 지금 남은 {sum(1 for r in early if r['type'] != '차트 이탈')}개), "
               f"출시 15일 뒤에 처음 든 게임 {sum(1 for r in past14 if r['peak'] is not None and r['first'] > 14)}개")
    since = md(start)
    return ("신작 런칭 추이(런칭 92일 안 · 유형은 아래 기준으로 판정한 값) — "
            "차트인 신작(최근 7일 안에 매출 100위 첫 진입): " + ('; '.join(line(r, False) for r in entered) or '없음') +
            " | 상위권 신작(지금 30위 안, 위 차트인 신작 제외): " + ('; '.join(line(r, True) for r in top) or '없음') +
            f" | 기준값(이 시장 {since} 이후 출시작 중 그날 차트에 남은 게임의 순위 중앙값, 차트에서 빠진 게임은 빠짐): {med(14)}, {med(30)}"
            f" | 정착 현황: {since} 이후 출시작 {len(rows)}개 중 D+14가 지난 {len(past14)}개 가운데 지금 차트에 남은 게임 {len(stay)}개(지금 유형: {dist})"
            f" | D+14 순위 구간별 지금 차트 잔존(남은 수/그 구간 게임 수, D+14가 지난 게임): {by14}"
            f" | 첫 진입 시점: {early_s}"
            " | 유형 기준(순위 구간 10위 안 · 11~30위 · 31~100위, D+14부터 판정): 관찰 중=D+14 전이거나 매출 차트에 처음 든 지 7일 전, 차트 이탈=최근 7일 중 4일 넘게 100위 밖, "
            "고점 뒤 하락=최근 7일 평균이 최고 순위보다 아래 구간, 늦게 상승=최고 30위 안을 D+21 뒤에 냈고 첫 주보다 위 구간으로 올라와 지금도 그 구간, "
            "상위권 유지=최고 30위 안이고 지금도 같은 구간, 중하위권 유지=최고 31~100위이고 지금도 같은 구간")
