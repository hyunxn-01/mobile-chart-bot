"""
한국 App Store 모바일 게임 매출 차트 일간 수집·캘린더 기반 이동평균 분석·메일 자동화.
GitHub Actions / cron-job.org 트리거로 매일 한국 시간 오전 7시 37분 실행.

활성 시간축 (그날 추가되는 분석):
  - 매일: 1일선 (어제 vs 오늘)
  - 월요일: + 1주선 (전전주 vs 전주, 월~일 단위)
  - 매월 1일: + 1달선 (전전월 vs 전월, 캘린더 월)
  - 분기 시작일(1/1, 4/1, 7/1, 10/1): + 분기선 (전전분기 vs 전분기)
  - 1월 1일: + 1년선 (재작년 vs 작년)

Claude API 호출은 529 과부하 등 일시 오류 시 자동 재시도. 최종 실패해도 메일은 발송.
AI 분석 모델은 파일 상단 CLAUDE_MODEL 상수로 관리.
"""

import json
import os
import smtplib
import time
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

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

# === AI 분석 모델 (변경 시 이 한 줄만 수정) ===
CLAUDE_MODEL = 'claude-opus-4-7'

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)
HISTORY_DIR = DATA_DIR / 'history'
HISTORY_DIR.mkdir(exist_ok=True)


# ============================================================
# 1. 데이터 수집·저장·로드
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


def save_current_data(data):
    today = datetime.now().strftime('%Y-%m-%d')
    f = HISTORY_DIR / f'{today}.json'
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"[OK] 데이터 저장: {f}")


def load_data_by_date(date_str):
    f = HISTORY_DIR / f'{date_str}.json'
    if f.exists():
        return json.loads(f.read_text(encoding='utf-8'))
    return None


def find_most_recent_past_data():
    today = datetime.now().strftime('%Y-%m-%d')
    files = sorted(HISTORY_DIR.glob('*.json'))
    past = [f for f in files if f.stem < today]
    if not past:
        return None, None
    f = past[-1]
    return json.loads(f.read_text(encoding='utf-8')), f.stem


def load_data_in_date_range(start_dt, end_dt, today_dt=None, current=None):
    """[start_dt, end_dt] 범위 데이터 로드. today_dt와 current 주어지면 그날은 current로 대체."""
    result = []
    d = start_dt
    while d.date() <= end_dt.date():
        if today_dt is not None and d.date() == today_dt.date():
            if current is not None:
                result.append(current)
        else:
            data = load_data_by_date(d.strftime('%Y-%m-%d'))
            if data is not None:
                result.append(data)
        d += timedelta(days=1)
    return result


# ============================================================
# 2. 분기 유틸
# ============================================================

def get_quarter(date_dt):
    return date_dt.year, (date_dt.month - 1) // 3 + 1


def get_quarter_range(year, quarter):
    start_month = (quarter - 1) * 3 + 1
    start = datetime(year, start_month, 1)
    if quarter == 4:
        end = datetime(year, 12, 31, 23, 59, 59)
    else:
        end = datetime(year, start_month + 3, 1) - timedelta(seconds=1)
    return start, end


def get_prior_quarter(year, quarter):
    if quarter == 1:
        return year - 1, 4
    return year, quarter - 1


# ============================================================
# 3. 평균 순위 + 비교 계산
# ============================================================

def compute_average_ranks(window_data_list):
    """N일치 데이터에서 게임별 평균 순위. 빈 리스트면 빈 dict."""
    if not window_data_list:
        return {}
    accumulator = {}
    for day_data in window_data_list:
        for app in day_data:
            app_id = app['app_id']
            if not app_id:
                continue
            if app_id not in accumulator:
                accumulator[app_id] = {'rank_sum': 0, 'days': 0,
                                       'title': app['title'], 'developer': app['developer']}
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


def compute_simple_changes(previous, current, threshold=10):
    """1일선용 단순 두 시점 비교."""
    if not previous:
        return {'mode': 'simple', 'new_entries': [], 'dropped': [], 'rank_changes': [],
                'past_days': 0, 'recent_days': 1, 'comparable': False}
    
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
                    'title': curr['title'], 'developer': curr['developer'],
                    'prev_rank': prev_rank, 'curr_rank': curr_rank, 'change': diff,
                })
    return {'mode': 'simple', 'new_entries': new_entries, 'dropped': dropped,
            'rank_changes': rank_changes, 'past_days': 1, 'recent_days': 1, 'comparable': True}


def compute_period_changes(past_data, recent_data, threshold=5):
    """이동평균 기반 두 기간 비교. 한쪽이라도 비면 빈 결과 반환."""
    past_avg = compute_average_ranks(past_data)
    recent_avg = compute_average_ranks(recent_data)
    
    base = {
        'mode': 'moving_average',
        'past_days': len(past_data),
        'recent_days': len(recent_data),
    }
    
    if not past_avg or not recent_avg:
        base.update({'new_entries': [], 'dropped': [], 'rank_changes': [], 'comparable': False})
        return base
    
    new_entries = [
        {'title': info['title'], 'developer': info['developer'],
         'avg_rank': round(info['avg_rank'], 1),
         'days_in_chart': info['days_in_chart'], 'total_days': info['total_days']}
        for app_id, info in recent_avg.items() if app_id not in past_avg
    ]
    dropped = [
        {'title': info['title'], 'developer': info['developer'],
         'avg_rank': round(info['avg_rank'], 1),
         'days_in_chart': info['days_in_chart'], 'total_days': info['total_days']}
        for app_id, info in past_avg.items() if app_id not in recent_avg
    ]
    rank_changes = []
    for app_id, recent_info in recent_avg.items():
        if app_id in past_avg:
            past_r = past_avg[app_id]['avg_rank']
            recent_r = recent_info['avg_rank']
            diff = past_r - recent_r
            if abs(diff) >= threshold:
                rank_changes.append({
                    'title': recent_info['title'], 'developer': recent_info['developer'],
                    'prev_rank': round(past_r, 1), 'curr_rank': round(recent_r, 1),
                    'change': round(diff, 1),
                    'recent_days': recent_info['days_in_chart'],
                    'prior_days': past_avg[app_id]['days_in_chart'],
                })
    base.update({'new_entries': new_entries, 'dropped': dropped, 'rank_changes': rank_changes,
                 'comparable': True})
    return base


# ============================================================
# 4. 유의문구 생성
# ============================================================

def generate_warning(changes, expected_past, expected_recent, past_label, recent_label):
    past_d = changes.get('past_days', 0)
    recent_d = changes.get('recent_days', 0)
    
    if past_d == 0 and recent_d == 0:
        return f"⚠️ 양쪽 기간 모두 데이터 없음 (봇 시작 이전 또는 누락). 비교 불가."
    if past_d == 0:
        return f"⚠️ {past_label} 데이터 없음. 비교 기준 부재 — 변화 분석 불가, {recent_label} 평균만 의미 있음."
    if recent_d == 0:
        return f"⚠️ {recent_label} 데이터 없음. 비교 불가."
    
    warnings = []
    if past_d < expected_past:
        warnings.append(f"{past_label}: {past_d}/{expected_past}일")
    if recent_d < expected_recent:
        warnings.append(f"{recent_label}: {recent_d}/{expected_recent}일")
    if warnings:
        return f"⚠️ 부분 데이터: {' / '.join(warnings)}"
    return None


# ============================================================
# 5. 시간축별 분석 함수
# ============================================================

def analyze_daily(today_dt, current):
    """1일선: 어제 vs 오늘."""
    previous, prev_date = find_most_recent_past_data()
    changes = compute_simple_changes(previous, current, threshold=10)
    changes['past_label'] = prev_date if prev_date else '어제 (데이터 없음)'
    changes['recent_label'] = today_dt.strftime('%Y-%m-%d')
    changes['period_label'] = f"{changes['past_label']} → {changes['recent_label']}"
    if not changes['comparable']:
        changes['warning'] = "⚠️ 어제 데이터 없음. 비교 불가 (첫 실행이거나 누락)."
    else:
        changes['warning'] = None
    return changes


def analyze_weekly(today_dt, current):
    """1주선: 전전주(월~일) vs 전주(월~일). 월요일에 호출."""
    recent_start = today_dt - timedelta(days=7)
    recent_end = today_dt - timedelta(days=1)
    past_start = today_dt - timedelta(days=14)
    past_end = today_dt - timedelta(days=8)
    
    past_data = load_data_in_date_range(past_start, past_end)
    recent_data = load_data_in_date_range(recent_start, recent_end)
    
    changes = compute_period_changes(past_data, recent_data, threshold=5)
    past_label = f"{past_start.strftime('%Y-%m-%d')}~{past_end.strftime('%m-%d')} (전전주)"
    recent_label = f"{recent_start.strftime('%Y-%m-%d')}~{recent_end.strftime('%m-%d')} (전주)"
    changes['past_label'] = past_label
    changes['recent_label'] = recent_label
    changes['period_label'] = f"{past_label} 평균 → {recent_label} 평균"
    changes['warning'] = generate_warning(changes, 7, 7, '전전주', '전주')
    return changes


def analyze_monthly(today_dt, current):
    """1달선: 전전월 vs 전월. 매월 1일에 호출."""
    last_month_end = today_dt - timedelta(days=1)
    last_month_start = datetime(last_month_end.year, last_month_end.month, 1)
    two_months_end = last_month_start - timedelta(days=1)
    two_months_start
