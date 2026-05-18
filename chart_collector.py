"""
한국 App Store 모바일 게임 매출 차트 일간 수집·이동평균 분석·메일 자동화.
GitHub Actions에서 매일 한국 시간 오전 7시 30분 자동 실행.

리포트 모드:
  - 평일 (월요일 제외): 일간 라이트 리포트 (1일선 단순 비교)
  - 월요일: 종합 리포트 (이동평균 기반 다중 시간축)

다중 시간축 (월요일 종합 리포트):
  - 1일선: 어제 vs 오늘 (단순 비교)
  - 1주선: 직전 7일 이동평균 vs 최근 7일 이동평균
  - 1달선: 직전 30일 이동평균 vs 최근 30일 이동평균
  - 분기선: 직전 회계분기 평균 vs 현재 회계분기 평균 (2026 Q1, Q2, Q3, Q4)
  - 1년선: 작년 평균 vs 올해 평균

데이터 소스: Apple iTunes RSS (Top Grossing → Top Free fallback)
메일 발송: Gmail SMTP
"""

import json
import os
import smtplib
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import pandas as pd
import requests
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Alignment, PatternFill
from anthropic import Anthropic

# === 환경변수 ===
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)
HISTORY_DIR = DATA_DIR / 'history'
HISTORY_DIR.mkdir(exist_ok=True)


# ============================================================
# 1. 데이터 수집
# ============================================================

def fetch_apple_chart_kr_games(limit=100):
    """Apple App Store 한국 게임 차트 수집. Top Grossing → Top Free fallback."""
    charts_to_try = [
        ('Top Grossing', f'https://itunes.apple.com/kr/rss/topgrossingapplications/limit={limit}/genre=6014/json'),
        ('Top Free', f'https://itunes.apple.com/kr/rss/topfreeapplications/limit={limit}/genre=6014/json'),
    ]
    for chart_name, url in charts_to_try:
        try:
            r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            r.raise_for_status()
            entries = r.json().get('feed', {}).get('entry', [])
            if not entries:
                print(f"[WARN] {chart_name}: 빈 데이터. fallback.")
                continue
            apps = [
                {
                    'rank': i + 1,
                    'app_id': e.get('id', {}).get('attributes', {}).get('im:bundleId', ''),
                    'title': e.get('im:name', {}).get('label', ''),
                    'developer': e.get('im:artist', {}).get('label', ''),
                    'category': e.get('category', {}).get('attributes', {}).get('label', ''),
                    'platform': 'App Store',
                    'chart': chart_name,
                }
                for i, e in enumerate(entries)
            ]
            print(f"[OK] {chart_name}: {len(apps)}개 수집")
            return apps, chart_name
        except Exception as e:
            print(f"[ERROR] {chart_name} 수집 실패: {e}")
    return [], None


# ============================================================
# 2. 데이터 저장·로드
# ============================================================

def save_current_data(data):
    today = datetime.now().strftime('%Y-%m-%d')
    f = HISTORY_DIR / f'{today}.json'
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"[OK] 데이터 저장: {f}")


def load_data_by_date(date_str):
    """특정 날짜 데이터 로드. 없으면 None."""
    f = HISTORY_DIR / f'{date_str}.json'
    if f.exists():
        return json.loads(f.read_text(encoding='utf-8'))
    return None


def find_most_recent_past_data():
    """가장 최근 과거 데이터 (1일선용)."""
    today = datetime.now().strftime('%Y-%m-%d')
    files = sorted(HISTORY_DIR.glob('*.json'))
    past = [f for f in files if f.stem < today]
    if not past:
        return None, None
    f = past[-1]
    return json.loads(f.read_text(encoding='utf-8')), f.stem


def load_window_data(today_dt, current, start_offset, end_offset):
    """[오늘-start_offset, 오늘-end_offset] 윈도우의 데이터 로드.
    
    Args:
        start_offset: 작은 값 (가까운 과거). 0이면 오늘 포함.
        end_offset: 큰 값 (먼 과거).
    
    Returns:
        실제 로드된 데이터 리스트 (없는 날은 스킵)
    """
    result = []
    for i in range(start_offset, end_offset + 1):
        if i == 0:
            result.append(current)
        else:
            target = (today_dt - timedelta(days=i)).strftime('%Y-%m-%d')
            data = load_data_by_date(target)
            if data is not None:
                result.append(data)
    return result


def load_data_in_date_range(start_dt, end_dt, today_dt=None, current=None):
    """[start_dt, end_dt] 범위의 모든 데이터 로드. 오늘 데이터는 current로 대체."""
    result = []
    d = start_dt
    while d <= end_dt:
        date_str = d.strftime('%Y-%m-%d')
        if today_dt is not None and d.date() == today_dt.date():
            if current is not None:
                result.append(current)
        else:
            data = load_data_by_date(date_str)
            if data is not None:
                result.append(data)
        d += timedelta(days=1)
    return result


# ============================================================
# 3. 분기/연도 유틸
# ============================================================

def get_quarter(date_dt):
    """날짜의 분기. Returns (year, quarter)."""
    return date_dt.year, (date_dt.month - 1) // 3 + 1


def get_quarter_range(year, quarter):
    """분기의 시작·끝 datetime."""
    start_month = (quarter - 1) * 3 + 1
    start = datetime(year, start_month, 1)
    if quarter == 4:
        end = datetime(year, 12, 31, 23, 59, 59)
    else:
        next_start = datetime(year, start_month + 3, 1)
        end = next_start - timedelta(seconds=1)
    return start, end


def get_prior_quarter(year, quarter):
    """직전 분기."""
    if quarter == 1:
        return year - 1, 4
    return year, quarter - 1


# ============================================================
# 4. 평균 순위 계산 (이동평균의 핵심)
# ============================================================

def compute_average_ranks(window_data_list):
    """N일치 데이터에서 게임별 평균 순위 계산.
    
    Returns:
        {app_id: {avg_rank, title, developer, days_in_chart, total_days}}
    """
    if not window_data_list:
        return {}
    
    accumulator = {}
    for day_data in window_data_list:
        for app in day_data:
            app_id = app['app_id']
            if not app_id:
                continue
            if app_id not in accumulator:
                accumulator[app_id] = {
                    'rank_sum': 0,
                    'days': 0,
                    'title': app['title'],
                    'developer': app['developer'],
                }
            accumulator[app_id]['rank_sum'] += app['rank']
            accumulator[app_id]['days'] += 1
    
    total_days = len(window_data_list)
    return {
        app_id: {
            'avg_rank': info['rank_sum'] / info['days'],
            'title': info['title'],
            'developer': info['developer'],
            'days_in_chart': info['days'],
            'total_days': total_days,
        }
        for app_id, info in accumulator.items()
    }


# ============================================================
# 5. 변화 계산 (단순 비교 + 이동평균 비교)
# ============================================================

def compute_simple_changes(previous, current, threshold=10):
    """단순 두 시점 비교 (1일선용). previous가 None이면 None."""
    if not previous:
        return None
    
    prev_by_id = {item['app_id']: item for item in previous if item['app_id']}
    curr_by_id = {item['app_id']: item for item in current if item['app_id']}
    
    new_entries = [
        {'title': c['title'], 'developer': c['developer'], 'rank': c['rank']}
        for c in current if c['app_id'] and c['app_id'] not in prev_by_id
    ]
    dropped = [
        {'title': p['title'], 'developer': p['developer'], 'rank': p['rank']}
        for p in previous if p['app_id'] and p['app_id'] not in curr_by_id
    ]
    
    rank_changes = []
    for app_id, curr in curr_by_id.items():
        if app_id in prev_by_id:
            prev_rank = prev_by_id[app_id]['rank']
            curr_rank = curr['rank']
            diff = prev_rank - curr_rank
            if abs(diff) >= threshold:
                rank_changes.append({
                    'title': curr['title'],
                    'developer': curr['developer'],
                    'prev_rank': prev_rank,
                    'curr_rank': curr_rank,
                    'change': diff,
                })
    
    return {
        'new_entries': new_entries,
        'dropped': dropped,
        'rank_changes': rank_changes,
        'mode': 'simple',
    }


def compute_ma_changes(prior_avg, recent_avg, threshold=5):
    """이동평균 기반 변화 계산.
    
    Args:
        prior_avg: 직전 윈도우의 게임별 평균 순위
        recent_avg: 최근 윈도우의 게임별 평균 순위
        threshold: 평균 순위 변동 임계값
    """
    if not prior_avg and not recent_avg:
        return None
    
    new_entries = []
    for app_id, info in recent_avg.items():
        if app_id not in prior_avg:
            new_entries.append({
                'title': info['title'],
                'developer': info['developer'],
                'avg_rank': round(info['avg_rank'], 1),
                'days_in_chart': info['days_in_chart'],
                'total_days': info['total_days'],
            })
    
    dropped = []
    for app_id, info in prior_avg.items():
        if app_id not in recent_avg:
            dropped.append({
                'title': info['title'],
                'developer': info['developer'],
                'avg_rank': round(info['avg_rank'], 1),
                'days_in_chart': info['days_in_chart'],
                'total_days': info['total_days'],
            })
    
    rank_changes = []
    for app_id, recent_info in recent_avg.items():
        if app_id in prior_avg:
            prior_r = prior_avg[app_id]['avg_rank']
            recent_r = recent_info['avg_rank']
            diff = prior_r - recent_r
            if abs(diff) >= threshold:
                rank_changes.append({
                    'title': recent_info['title'],
                    'developer': recent_info['developer'],
                    'prev_rank': round(prior_r, 1),
                    'curr_rank': round(recent_r, 1),
                    'change': round(diff, 1),
                    'recent_days': recent_info['days_in_chart'],
                    'prior_days': prior_avg[app_id]['days_in_chart'],
                })
    
    return {
        'new_entries': new_entries,
        'dropped': dropped,
        'rank_changes': rank_changes,
        'mode': 'moving_average',
    }


# ============================================================
# 6. 시간축별 분석 함수
# ============================================================

def compute_daily_changes(current, threshold=10):
    """1일선: 어제 vs 오늘."""
    previous, prev_date = find_most_recent_past_data()
    if previous is None:
        return None
    changes = compute_simple_changes(previous, current, threshold=threshold)
    if changes is None:
        return None
    changes['label'] = f"{prev_date} → 오늘"
    changes['prior_label'] = prev_date
    changes['recent_label'] = '오늘'
    return changes


def compute_weekly_ma_changes(today_dt, current, threshold=5):
    """1주선: 직전 7일 vs 최근 7일."""
    recent = load_window_data(today_dt, current, 0, 6)
    prior = load_window_data(today_dt, current, 7, 13)
    
    if len(recent) < 5 or len(prior) < 5:
        return None
    
    recent_avg = compute_average_ranks(recent)
    prior_avg = compute_average_ranks(prior)
    changes = compute_ma_changes(prior_avg, recent_avg, threshold=threshold)
    if changes is None:
        return None
    
    recent_start = (today_dt - timedelta(days=6)).strftime('%Y-%m-%d')
    recent_end = today_dt.strftime('%Y-%m-%d')
    prior_start = (today_dt - timedelta(days=13)).strftime('%Y-%m-%d')
    prior_end = (today_dt - timedelta(days=7)).strftime('%Y-%m-%d')
    
    changes['label'] = f"{prior_start}~{prior_end} 평균 → {recent_start}~{recent_end} 평균"
    changes['prior_label'] = f"{prior_start}~{prior_end} 평균"
    changes['recent_label'] = f"{recent_start}~{recent_end} 평균"
    changes['recent_days_count'] = len(recent)
    changes['prior_days_count'] = len(prior)
    return changes


def compute_monthly_ma_changes(today_dt, current, threshold=5):
    """1달선: 직전 30일 vs 최근 30일."""
    recent = load_window_data(today_dt, current, 0, 29)
    prior = load_window_data(today_dt, current, 30, 59)
    
    if len(recent) < 20 or len(prior) < 20:
        return None
    
    recent_avg = compute_average_ranks(recent)
    prior_avg = compute_average_ranks(prior)
    changes = compute_ma_changes(prior_avg, recent_avg, threshold=threshold)
    if changes is None:
        return None
    
    recent_start = (today_dt - timedelta(days=29)).strftime('%Y-%m-%d')
    recent_end = today_dt.strftime('%Y-%m-%d')
    prior_start = (today_dt - timedelta(days=59)).strftime('%Y-%m-%d')
    prior_end = (today_dt - timedelta(days=30)).strftime('%Y-%m-%d')
    
    changes['label'] = f"{prior_start}~{prior_end} 평균 → {recent_start}~{recent_end} 평균"
    changes['prior_label'] = f"{prior_start}~{prior_end} 평균"
    changes['recent_label'] = f"{recent_start}~{recent_end} 평균"
    changes['recent_days_count'] = len(recent)
    changes['prior_days_count'] = len(prior)
    return changes


def compute_quarterly_changes(today_dt, current, threshold=5):
    """분기선: 직전 회계분기 평균 vs 현재 회계분기 평균."""
    curr_year, curr_q = get_quarter(today_dt)
    prior_year, prior_q = get_prior_quarter(curr_year, curr_q)
    
    curr_q_start, _ = get_quarter_range(curr_year, curr_q)
    prior_q_start, prior_q_end = get_quarter_range(prior_year, prior_q)
    
    curr_q_data = load_data_in_date_range(curr_q_start, today_dt, today_dt=today_dt, current=current)
    prior_q_data = load_data_in_date_range(prior_q_start, prior_q_end)
    
    if len(curr_q_data) < 14 or len(prior_q_data) < 30:
        return None
    
    curr_avg = compute_average_ranks(curr_q_data)
    prior_avg = compute_average_ranks(prior_q_data)
    changes = compute_ma_changes(prior_avg, curr_avg, threshold=threshold)
    if changes is None:
        return None
    
    changes['label'] = f"{prior_year} Q{prior_q} 평균 → {curr_year} Q{curr_q} 평균"
    changes['prior_label'] = f"{prior_year} Q{prior_q} 평균 ({len(prior_q_data)}일)"
    changes['recent_label'] = f"{curr_year} Q{curr_q} 평균 ({len(curr_q_data)}일)"
    changes['current_quarter'] = f"{curr_year} Q{curr_q}"
    changes['prior_quarter'] = f"{prior_year} Q{prior_q}"
    changes['recent_days_count'] = len(curr_q_data)
    changes['prior_days_count'] = len(prior_q_data)
    return changes


def compute_yearly_changes(today_dt, current, threshold=5):
    """1년선: 작년 평균 vs 올해 평균."""
    curr_year = today_dt.year
    prior_year = curr_year - 1
    
    curr_y_start = datetime(curr_year, 1, 1)
    prior_y_start = datetime(prior_year, 1, 1)
    prior_y_end = datetime(prior_year, 12, 31, 23, 59, 59)
    
    curr_y_data = load_data_in_date_range(curr_y_start, today_dt, today_dt=today_dt, current=current)
    prior_y_data = load_data_in_date_range(prior_y_start, prior_y_end)
    
    if len(curr_y_data) < 30 or len(prior_y_data) < 60:
        return None
    
    curr_avg = compute_average_ranks(curr_y_data)
    prior_avg = compute_average_ranks(prior_y_data)
    changes = compute_ma_changes(prior_avg, curr_avg, threshold=threshold)
    if changes is None:
        return None
    
    changes['label'] = f"{prior_year}년 평균 → {curr_year}년 평균"
    changes['prior_label'] = f"{prior_year}년 평균 ({len(prior_y_data)}일)"
    changes['recent_label'] = f"{curr_year}년 평균 ({len(curr_y_data)}일)"
    changes['current_year'] = curr_year
    changes['prior_year'] = prior_year
    changes['recent_days_count'] = len(curr_y_data)
    changes['prior_days_count'] = len(prior_y_data)
    return changes


def compute_all_timeframe_changes(today_dt, current, threshold=5):
    """모든 시간축의 변화 계산. 가용하지 않은 시간축은 None."""
    return {
        '1일': compute_daily_changes(current, threshold=10),
        '1주': compute_weekly_ma_changes(today_dt, current, threshold=threshold),
        '1달': compute_monthly_ma_changes(today_dt, current, threshold=threshold),
        '분기': compute_quarterly_changes(today_dt, current, threshold=threshold),
        '1년': compute_yearly_changes(today_dt, current, threshold=threshold),
    }


# ============================================================
# 7. Claude 요약
# ============================================================

def generate_daily_summary(current, changes, chart_used, previous_date):
    """일간 라이트 리포트용 짧은 요약."""
    if changes is None:
        return (f"이번이 첫 데이터 수집입니다 (차트: {chart_used}). "
                f"다음 실행부터 1일 변동 분석이 시작됩니다.")
    
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = f"""한국 App Store 게임 {chart_used} 차트의 1일 변동을 사업PM 관점에서 짧게 분석하세요.

[비교 구간] {previous_date} → 오늘

[신규 진입]
{json.dumps(changes.get('new_entries', [])[:10], ensure_ascii=False, indent=2)}

[차트 이탈]
{json.dumps(changes.get('dropped', [])[:10], ensure_ascii=False, indent=2)}

[큰 변동 (10등 이상)]
{json.dumps(changes.get('rank_changes', [])[:15], ensure_ascii=False, indent=2)}

다음을 한국어로 짧게 (2~3문단, 각 2~3줄):
1. 가장 주목할 변동 1~2건 (이유 추정 가능하면)
2. 사업PM 한 줄 인사이트

일간은 노이즈가 많으니 진짜 시그널만. 변동 미미하면 "특이사항 없음"이라고 솔직하게."""
    
    response = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=800,
        messages=[{'role': 'user', 'content': prompt}],
    )
    return response.content[0].text


def generate_comprehensive_summary(current, multi_changes, chart_used):
    """월요일 종합 리포트: 다중 시간축 이동평균 분석."""
    active = [(name, ch) for name, ch in multi_changes.items() if ch is not None]
    if not active:
        return (f"비교 가능한 과거 데이터가 아직 없습니다 (차트: {chart_used}). "
                f"데이터가 누적되면 시간축이 자동 활성화됩니다.")
    
    sections = []
    for name, ch in active:
        mode_desc = "단순 비교" if ch.get('mode') == 'simple' else "이동평균"
        sections.append(f"""
[{name}선] ({mode_desc}) {ch['label']}
- 신규 진입: {len(ch.get('new_entries', []))}개
- 이탈: {len(ch.get('dropped', []))}개
- 큰 변동: {len(ch.get('rank_changes', []))}개

상위 변동 (최대 8개):
{json.dumps(sorted(ch.get('rank_changes', []), key=lambda x: -abs(x['change']))[:8], ensure_ascii=False, indent=2)}
""")
    
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = f"""한국 App Store 게임 {chart_used} 차트의 다중 시간축 이동평균 변화를 사업PM 관점에서 분석하세요.

[이번 측정 Top 30]
{json.dumps(current[:30], ensure_ascii=False, indent=2)}

{"".join(sections)}

**핵심 분석 관점**: 단기 vs 중장기 추세의 일치/불일치를 비교해서 진짜 시그널을 식별하세요.
- 단기(1일·1주)만 변동, 중장기(1달·분기·1년)는 안정 → 일시적 노이즈
- 단기·중장기 모두 변동 → 진짜 추세
- 중장기 변동 크고 단기는 안정 → 추세 안착 단계

**이동평균 해석 팁**:
- "평균 순위"는 윈도우 내 일관성을 반영. 같은 8위라도 평균 8위면 안정 거주자, 평균 30위면 가끔 진입하는 게임
- "직전 평균 30위 → 최근 평균 8위" = 진짜 상승 추세

한국어 5~8문단 (각 2~4줄):
1. 활성 시간축 요약
2. 단기 시그널 (1일선)
3. 중기 시그널 (1주·1달선)
4. 장기 시그널 (분기·1년선, 가용 시)
5. 단기 vs 중장기 비교 → 진짜 추세 식별
6. 사업PM 액션 포인트

군더더기 없이."""
    
    response = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=2500,
        messages=[{'role': 'user', 'content': prompt}],
    )
    return response.content[0].text


# ============================================================
# 8. 엑셀
# ============================================================

def _write_changes_to_sheet(ws, changes, title):
    """시간축별 변화를 시트에 작성."""
    is_ma = changes.get('mode') == 'moving_average'
    rank_label = '평균 순위' if is_ma else '순위'
    
    row = 1
    ws.cell(row=row, column=1, value=title).font = Font(bold=True, size=12)
    row += 2
    
    # 신규 진입
    ws.cell(row=row, column=1, value='■ 신규 진입').font = Font(bold=True, size=11)
    row += 1
    items = changes.get('new_entries', [])[:30]
    if not items:
        ws.cell(row=row, column=1, value='  (해당 없음)').font = Font(italic=True, color='888888')
        row += 1
    else:
        for item in items:
            ws.cell(row=row, column=1, value=item['title'])
            ws.cell(row=row, column=2, value=item['developer'])
            if is_ma:
                ws.cell(row=row, column=3, value=f"{rank_label} {item['avg_rank']} ({item['days_in_chart']}/{item['total_days']}일 등장)")
            else:
                ws.cell(row=row, column=3, value=f"{item['rank']}위 진입")
            row += 1
    row += 2
    
    # 상승 / 하락
    for label, sort_key, filter_fn in [
        ('■ 큰 폭 상승', lambda x: -x['change'], lambda x: x['change'] > 0),
        ('■ 큰 폭 하락', lambda x: x['change'], lambda x: x['change'] < 0),
    ]:
        ws.cell(row=row, column=1, value=label).font = Font(bold=True, size=11)
        row += 1
        items = [c for c in sorted(changes.get('rank_changes', []), key=sort_key)[:30] if filter_fn(c)]
        if not items:
            ws.cell(row=row, column=1, value='  (해당 없음)').font = Font(italic=True, color='888888')
            row += 1
        else:
            for item in items:
                ws.cell(row=row, column=1, value=item['title'])
                ws.cell(row=row, column=2, value=item['developer'])
                arrow = '▲' if item['change'] > 0 else '▼'
                ws.cell(row=row, column=3, value=f"{rank_label} {item['prev_rank']} → {item['curr_rank']} ({arrow}{abs(item['change'])})")
                row += 1
        row += 2
    
    # 이탈
    ws.cell(row=row, column=1, value='■ 차트 이탈').font = Font(bold=True, size=11)
    row += 1
    items = changes.get('dropped', [])[:30]
    if not items:
        ws.cell(row=row, column=1, value='  (해당 없음)').font = Font(italic=True, color='888888')
        row += 1
    else:
        for item in items:
            ws.cell(row=row, column=1, value=item['title'])
            ws.cell(row=row, column=2, value=item['developer'])
            if is_ma:
                ws.cell(row=row, column=3, value=f"이전 {rank_label} {item['avg_rank']}에서 이탈")
            else:
                ws.cell(row=row, column=3, value=f"이전 {item['rank']}위에서 이탈")
            row += 1
    
    for col_letter, width in [('A', 35), ('B', 25), ('C', 40)]:
        ws.column_dimensions[col_letter].width = width


def create_comprehensive_excel_report(current, multi_changes, summary, chart_used):
    today = datetime.now().strftime('%Y%m%d')
    filename = f'mobile_chart_{today}.xlsx'
    wb = Workbook()
    
    # 시트 1: 요약
    ws = wb.active
    ws.title = '요약'
    ws['A1'] = f'한국 App Store 게임 차트 종합 보고서 ({datetime.now().strftime("%Y-%m-%d")})'
    ws['A1'].font = Font(bold=True, size=14)
    ws.merge_cells('A1:D1')
    ws['A2'] = f'사용 차트: {chart_used}'
    ws['A2'].font = Font(italic=True, size=11)
    
    active = [(name, ch) for name, ch in multi_changes.items() if ch is not None]
    ws['A4'] = '활성 분석 시간축'
    ws['A4'].font = Font(bold=True, size=12)
    if active:
        lines = [f"  · {name}선: {ch['label']}" for name, ch in active]
        ws['A5'] = "\n".join(lines)
        ws['A5'].alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[5].height = max(30, len(active) * 24)
    else:
        ws['A5'] = '  비교 가능한 데이터 없음. 누적 후 자동 활성화됩니다.'
    
    ws['A7'] = 'Claude 종합 인사이트'
    ws['A7'].font = Font(bold=True, size=12)
    ws['A8'] = summary
    ws['A8'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.column_dimensions['A'].width = 100
    ws.row_dimensions[8].height = 600
    
    # 시트 2: 이번 차트
    ws2 = wb.create_sheet('이번 차트')
    df = pd.DataFrame(current)
    if not df.empty:
        for r in dataframe_to_rows(df, index=False, header=True):
            ws2.append(r)
        for cell in ws2[1]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='DDDDDD', end_color='DDDDDD', fill_type='solid')
        for col_letter, width in [('A', 8), ('B', 30), ('C', 40), ('D', 25), ('E', 20), ('F', 15), ('G', 20)]:
            ws2.column_dimensions[col_letter].width = width
    
    # 시간축별 시트
    for name, ch in active:
        ws_t = wb.create_sheet(f'{name}선')
        title = f'■ {name}선 변화 ({ch["label"]})'
        _write_changes_to_sheet(ws_t, ch, title)
    
    wb.save(filename)
    return filename


# ============================================================
# 9. 메일 본문
# ============================================================

def build_daily_email_html(today, chart_used, current, changes, summary, previous_date):
    """일간 라이트 리포트 본문."""
    if changes is None:
        body = "<p>이번이 첫 데이터 수집입니다. 다음 실행부터 1일 변동 분석이 시작됩니다.</p>"
    else:
        new_html = "".join([
            f"<li>{e['title']} <span style='color:#888'>({e['developer']}, {e['rank']}위 진입)</span></li>"
            for e in changes.get('new_entries', [])[:10]
        ]) or "<li style='color:#888'>없음</li>"
        
        dropped_html = "".join([
            f"<li>{e['title']} <span style='color:#888'>(이전 {e['rank']}위 → 이탈)</span></li>"
            for e in changes.get('dropped', [])[:10]
        ]) or "<li style='color:#888'>없음</li>"
        
        rank_sorted = sorted(changes.get('rank_changes', []), key=lambda x: -abs(x['change']))[:10]
        changes_html = "".join([
            f"<li>{c['title']} <span style='color:{'#16a34a' if c['change']>0 else '#dc2626'}'>"
            f"{c['prev_rank']}위 → {c['curr_rank']}위 "
            f"({'▲' if c['change']>0 else '▼'}{abs(c['change'])})</span></li>"
            for c in rank_sorted
        ]) or "<li style='color:#888'>없음</li>"
        
        body = f"""
        <p><strong>비교:</strong> {previous_date} → {today}</p>
        <h3 style="margin-top:24px;">📈 신규 진입</h3>
        <ul>{new_html}</ul>
        <h3 style="margin-top:24px;">📉 차트 이탈</h3>
        <ul>{dropped_html}</ul>
        <h3 style="margin-top:24px;">📊 큰 폭 변동 (10등 이상)</h3>
        <ul>{changes_html}</ul>
        <h3 style="margin-top:24px;">💡 인사이트</h3>
        <pre style="white-space: pre-wrap; font-family: 'Malgun Gothic', sans-serif; line-height: 1.7; background: #f8f8f8; padding: 16px; border-radius: 4px;">{summary}</pre>
        """
    
    return f"""
    <div style="font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; max-width: 700px;">
      <h2>📱 한국 App Store 게임 차트 일간 변동</h2>
      <p><strong>수집일:</strong> {today} | <strong>차트:</strong> {chart_used} ({len(current)}개)</p>
      <hr/>
      {body}
      <hr style="margin-top: 30px;"/>
      <p style="color: #888; font-size: 12px;">월요일에는 이동평균 기반 다중 시간축 종합 리포트가 별도 발송됩니다.</p>
    </div>
    """


def build_comprehensive_email_html(today, chart_used, current, multi_changes, summary):
    """종합 리포트 본문."""
    active = [(name, ch) for name, ch in multi_changes.items() if ch is not None]
    
    if not active:
        body = """
        <p style="color: #888;">비교 가능한 과거 데이터가 아직 없습니다. 데이터가 쌓이면 시간축별 분석이 자동 활성화됩니다.</p>
        <ul style="color: #666; font-size: 13px;">
          <li>어제 데이터 → 1일선 활성</li>
          <li>각 윈도우 5일 이상 → 1주선 활성 (약 2주 후)</li>
          <li>각 윈도우 20일 이상 → 1달선 활성 (약 2달 후)</li>
          <li>현재 분기 14일 + 직전 분기 30일 → 분기선 활성</li>
          <li>올해 30일 + 작년 60일 → 1년선 활성</li>
        </ul>
        """
    else:
        tf_html = "<ul>"
        for name, ch in active:
            mode_label = "단순 비교" if ch.get('mode') == 'simple' else "이동평균"
            n_new = len(ch.get('new_entries', []))
            n_dropped = len(ch.get('dropped', []))
            n_changes = len(ch.get('rank_changes', []))
            tf_html += (
                f"<li><strong>{name}선</strong> <span style='color:#888;font-size:12px'>({mode_label})</span><br>"
                f"<span style='color:#666'>{ch['label']}</span><br>"
                f"신규 {n_new}, 이탈 {n_dropped}, 큰 변동 {n_changes}</li>"
            )
        tf_html += "</ul>"
        
        body = f"""
        <h3 style="margin-top:24px;">📊 활성 분석 시간축</h3>
        {tf_html}
        <h3 style="margin-top:24px;">💡 Claude 종합 인사이트</h3>
        <pre style="white-space: pre-wrap; font-family: 'Malgun Gothic', sans-serif; line-height: 1.7; background: #f8f8f8; padding: 16px; border-radius: 4px;">{summary}</pre>
        <p style="color: #666; margin-top: 24px;">시간축별 상세 변화는 첨부 엑셀의 각 시트에서 확인하세요.</p>
        """
    
    return f"""
    <div style="font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; max-width: 800px;">
      <h2>📱 한국 App Store 게임 차트 종합 보고서</h2>
      <p><strong>수집일:</strong> {today} | <strong>차트:</strong> {chart_used} ({len(current)}개)</p>
      <hr/>
      {body}
    </div>
    """


# ============================================================
# 10. 메일 발송
# ============================================================

def send_email_via_gmail(subject, html_body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(attachment_path)}'
        )
        msg.attach(part)
    
    app_password = GMAIL_APP_PASSWORD.replace(' ', '')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, app_password)
        server.send_message(msg)
    print(f"[OK] 메일 발송: {RECIPIENT_EMAIL}")


# ============================================================
# 11. 메인
# ============================================================

def main():
    print(f"\n=== 한국 App Store 게임 차트 수집 ({datetime.now()}) ===\n")
    
    missing = [k for k, v in {
        'ANTHROPIC_API_KEY': ANTHROPIC_API_KEY,
        'GMAIL_USER': GMAIL_USER,
        'GMAIL_APP_PASSWORD': GMAIL_APP_PASSWORD,
        'RECIPIENT_EMAIL': RECIPIENT_EMAIL,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"환경변수 누락: {missing}")
    
    today_dt = datetime.now()
    is_monday = today_dt.weekday() == 0
    report_mode = '종합 (월요일)' if is_monday else '일간'
    print(f"[INFO] 리포트 모드: {report_mode}\n")
    
    print("[1/4] App Store 차트 수집...")
    current, chart_used = fetch_apple_chart_kr_games(100)
    if not current:
        raise RuntimeError("모든 차트 수집 실패")
    print(f"      → {len(current)}개 수집, 사용 차트: {chart_used}")
    
    today = today_dt.strftime('%Y-%m-%d')
    
    if is_monday:
        # ===== 월요일: 다중 시간축 종합 리포트 =====
        print("[2/4] 다중 시간축 변화 계산...")
        multi_changes = compute_all_timeframe_changes(today_dt, current, threshold=5)
        active_names = [name for name, ch in multi_changes.items() if ch is not None]
        if active_names:
            print(f"      → 활성 시간축: {', '.join(active_names)}")
            for name in active_names:
                ch = multi_changes[name]
                mode_label = "단순" if ch.get('mode') == 'simple' else "이동평균"
                print(f"        · {name}선 ({mode_label}): 신규 {len(ch.get('new_entries', []))} / 이탈 {len(ch.get('dropped', []))} / 변동 {len(ch.get('rank_changes', []))}")
        else:
            print("      → 활성 시간축 없음 (데이터 누적 대기)")
        
        print("[3/4] Claude 종합 인사이트 생성...")
        summary = generate_comprehensive_summary(current, multi_changes, chart_used)
        print("─" * 60)
        print(summary)
        print("─" * 60)
        
        print("[4/4] 엑셀 + 메일 발송...")
        excel_path = create_comprehensive_excel_report(current, multi_changes, summary, chart_used)
        subject = f'[모바일 게임 차트] 종합 보고 {today} ({chart_used})'
        html_body = build_comprehensive_email_html(today, chart_used, current, multi_changes, summary)
        send_email_via_gmail(subject, html_body, attachment_path=excel_path)
    
    else:
        # ===== 평일: 일간 라이트 리포트 =====
        print("[2/4] 직전 데이터와 1일선 비교...")
        previous, previous_date = find_most_recent_past_data()
        changes = compute_simple_changes(previous, current, threshold=10) if previous else None
        if changes is None:
            print("      → 비교 가능한 과거 데이터 없음")
            previous_date = None
        else:
            print(f"      → 비교 기준: {previous_date}")
            print(f"      → 신규 {len(changes.get('new_entries', []))} / 이탈 {len(changes.get('dropped', []))} / 변동 {len(changes.get('rank_changes', []))} (임계값 10등)")
        
        print("[3/4] Claude 일간 요약 생성...")
        summary = generate_daily_summary(current, changes, chart_used, previous_date)
        print("─" * 60)
        print(summary)
        print("─" * 60)
        
        print("[4/4] 메일 발송 (첨부 없음)...")
        subject = f'[모바일 게임 차트] 일간 변동 {today} ({chart_used})'
        html_body = build_daily_email_html(today, chart_used, current, changes, summary, previous_date)
        send_email_via_gmail(subject, html_body, attachment_path=None)
    
    save_current_data(current)
    print("\n=== 완료 ===\n")


if __name__ == '__main__':
    main()
