#!/usr/bin/env python3
"""설계 불변식 게이트 — build 산출물이 프로젝트 규칙을 지키는지 기계 검증(CI에서 build_dashboard 뒤 실행).

현재 강제하는 규칙 — '완료된 기간만':
  브리핑의 비-weekly 시간축(월/분기/년)은 그 시장의 charts.grossing.timeframes[axis]에
  완료 구간(labels)이 있을 때만 존재해야 한다. 미완료 축을 생성하면(빈 분석) 위반.
  (weekly는 당일 스냅샷 기반이라 항상 허용 — 게이트 대상 아님.)

위반 시 exit 1 → 워크플로가 잘못된 데이터를 push하기 전에 멈춘다(자가 준수가 아니라 기계 강제).
로컬에서 `python check_invariants.py --selftest`로 판정 로직을 검증할 수 있다.
"""
import json
import sys
from pathlib import Path

GATED_AXES = ['monthly', 'quarterly', 'yearly']  # weekly는 스냅샷 기반이라 항상 허용


def _load(p):
    try:
        return json.loads(Path(p).read_text(encoding='utf-8'))
    except Exception:
        return None


def _timeframe_has_data(market_json, axis):
    """시장 JSON의 grossing.timeframes[axis]에 완료 구간(labels)이 1개 이상인가."""
    try:
        tf = (((market_json or {}).get('charts') or {}).get('grossing') or {}).get('timeframes') or {}
        return bool((tf.get(axis) or {}).get('labels'))
    except Exception:
        return False


def check_brief_axes(markets_dir):
    """브리핑 비-weekly 축 ⊆ 완료 구간 있는 시간축. 위반 메시지 리스트 반환(빈 리스트=통과)."""
    markets_dir = Path(markets_dir)
    idx = _load(markets_dir / 'index.json')
    if not idx:
        return []  # index 없으면 검사 대상 없음(로컬 부분 데이터에서 무해 통과)
    targets = [('major_%s', m['key']) for m in (idx.get('majors') or [])]
    targets += [('region_%s', r['key']) for r in (idx.get('regions') or [])]
    violations = []
    for tmpl, key in targets:
        brief = _load(markets_dir / (tmpl % key + '.json'))
        market = _load(markets_dir / (key + '.json'))
        if not brief or not isinstance(brief.get('axes'), dict):
            continue
        for axis in GATED_AXES:
            ax = brief['axes'].get(axis)
            if ax and ax.get('text') and not _timeframe_has_data(market, axis):
                violations.append(
                    f"{tmpl % key}.json: '{axis}' 축이 생성됐는데 시장 '{key}' "
                    f"timeframes['{axis}']에 완료 구간이 없음 (완료된 기간만 규칙 위반)")
    return violations


def run(markets_dir):
    v = check_brief_axes(markets_dir)
    if v:
        print('[FAIL] 설계 불변식 위반 — 완료된 기간만:')
        for x in v:
            print('  -', x)
        return 1
    print(f'[OK] 설계 불변식 통과 — 완료된 기간만 ({markets_dir}).')
    return 0


def selftest():
    """판정 로직 검증: 통과 케이스는 위반 없음, 위반 케이스는 잡아내야 한다."""
    import tempfile
    cases = [
        # (이름, market, brief, 위반_기대)
        ('통과: monthly 축 + labels 있음',
         {'charts': {'grossing': {'timeframes': {'monthly': {'labels': ['2026-05']}}}}},
         {'axes': {'weekly': {'text': '## a'}, 'monthly': {'text': '## b'}}}, False),
        ('위반: monthly 축 있는데 labels 빔',
         {'charts': {'grossing': {'timeframes': {'monthly': {'labels': []}}}}},
         {'axes': {'weekly': {'text': '## a'}, 'monthly': {'text': '## b'}}}, True),
        ('통과: weekly만(게이트 대상 아님)',
         {'charts': {'grossing': {'timeframes': {'weekly': {'labels': ['2026-06-15']}}}}},
         {'axes': {'weekly': {'text': '## a'}}}, False),
    ]
    failures = []
    for name, market, brief, expect in cases:
        d = Path(tempfile.mkdtemp())
        (d / 'index.json').write_text(json.dumps({'majors': [{'key': 'kr'}], 'regions': []}), encoding='utf-8')
        (d / 'kr.json').write_text(json.dumps(market), encoding='utf-8')
        (d / 'major_kr.json').write_text(json.dumps(brief), encoding='utf-8')
        got = bool(check_brief_axes(d))
        if got != expect:
            failures.append(f"  - '{name}': 위반_기대={expect} 인데 결과={got}")
    if failures:
        print('[SELFTEST FAIL]')
        print('\n'.join(failures))
        return 1
    print('[SELFTEST OK] 통과/위반 케이스 모두 정확히 판정.')
    return 0


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    base = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else 'docs/markets'
    sys.exit(run(base))
