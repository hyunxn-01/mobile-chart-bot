"""
한국 모바일 게임 차트 주간 수집·분석·메일 발송 자동화.
GitHub Actions에서 매주 월요일 한국 시간 오전 9시 자동 실행.
메일 발송: Gmail SMTP.
"""

import json
import os
import smtplib
from datetime import datetime
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
from google_play_scraper import list as gp_list
from anthropic import Anthropic

# === 환경변수 (GitHub Secrets에서 주입) ===
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)


def fetch_google_play_top_grossing_kr_games(limit=100):
    """Google Play 한국 게임 카테고리 매출(Top Grossing) 차트 수집."""
    try:
        results = gp_list(
            collection='TOP_GROSSING',
            category='GAME',
            country='kr',
            lang='ko',
        )
        results = results[:limit]
        return [
            {
                'rank': i + 1,
                'app_id': r.get('appId', ''),
                'title': r.get('title', ''),
                'developer': r.get('developer', ''),
                'score': r.get('score'),
                'platform': 'Google Play',
                'chart': 'Top Grossing',
            }
            for i, r in enumerate(results)
        ]
    except Exception as e:
        print(f"[ERROR] Google Play 차트 수집 실패: {e}")
        return []


def fetch_apple_top_charts_kr_games(limit=100):
    """Apple App Store 한국 게임 카테고리 인기(Top Free) 차트.
    
    Apple은 Top Grossing RSS를 deprecated 시켰으므로 인기(무료) 차트로 대체.
    genre=6014 = Games 카테고리.
    """
    url = f'https://itunes.apple.com/kr/rss/topfreeapplications/limit={limit}/genre=6014/json'
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        r.raise_for_status()
        data = r.json()
        entries = data.get('feed', {}).get('entry', [])
        return [
            {
                'rank': i + 1,
                'app_id': e.get('id', {}).get('attributes', {}).get('im:bundleId', ''),
                'title': e.get('im:name', {}).get('label', ''),
                'developer': e.get('im:artist', {}).get('label', ''),
                'score': None,
                'platform': 'App Store',
                'chart': 'Top Free Games',
            }
            for i, e in enumerate(entries)
        ]
    except Exception as e:
        print(f"[ERROR] App Store 차트 수집 실패: {e}")
        return []


def load_previous_data():
    """이전 주 데이터 로드. 첫 실행 시 None 반환."""
    f = DATA_DIR / 'last_week.json'
    if f.exists():
        return json.loads(f.read_text(encoding='utf-8'))
    return None


def save_current_data(data):
    """이번 주 데이터를 다음 주 비교용으로 저장."""
    f = DATA_DIR / 'last_week.json'
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def compute_changes(previous, current):
    """전주 대비 변화 계산."""
    if not previous:
        return {'is_first_week': True}
    
    prev_by_id = {item['app_id']: item for item in previous if item['app_id']}
    curr_by_id = {item['app_id']: item for item in current if item['app_id']}
    
    new_entries = [c for c in current if c['app_id'] and c['app_id'] not in prev_by_id]
    dropped = [p for p in previous if p['app_id'] and p['app_id'] not in curr_by_id]
    
    rank_changes = []
    for app_id, curr in curr_by_id.items():
        if app_id in prev_by_id and curr['platform'] == prev_by_id[app_id]['platform']:
            prev_rank = prev_by_id[app_id]['rank']
            curr_rank = curr['rank']
            diff = prev_rank - curr_rank  # 양수=상승, 음수=하락
            if abs(diff) >= 5:
                rank_changes.append({
                    'title': curr['title'],
                    'platform': curr['platform'],
                    'prev_rank': prev_rank,
                    'curr_rank': curr_rank,
                    'change': diff,
                })
    
    return {
        'is_first_week': False,
        'new_entries': new_entries,
        'dropped': dropped,
        'rank_changes': rank_changes,
    }


def generate_summary_with_claude(current, changes):
    """Claude API로 사업PM 시각의 주간 변화 요약 생성."""
    if changes.get('is_first_week'):
        return ("이번 주가 첫 데이터 수집입니다. 다음 주부터 전주 대비 변화 분석이 시작됩니다.\n\n"
                f"이번 주 수집된 차트: 총 {len(current)}개 (Google Play 매출 + App Store 인기)")
    
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
    prompt = f"""한국 모바일 게임 차트의 주간 변화를 사업PM 관점에서 요약해 주세요.

[이번 주 Google Play 매출 Top 20]
{json.dumps([c for c in current if c['platform']=='Google Play'][:20], ensure_ascii=False, indent=2)}

[이번 주 App Store 인기 Top 20]
{json.dumps([c for c in current if c['platform']=='App Store'][:20], ensure_ascii=False, indent=2)}

[새로 진입한 앱]
{json.dumps(changes.get('new_entries', [])[:15], ensure_ascii=False, indent=2)}

[차트에서 떨어진 앱]
{json.dumps(changes.get('dropped', [])[:15], ensure_ascii=False, indent=2)}

[순위 변동 (5등 이상)]
{json.dumps(changes.get('rank_changes', [])[:20], ensure_ascii=False, indent=2)}

다음을 한국어로 요약 (5~7문단, 각 문단 2~4줄):
1. 주목할 신규 진입작 (장르·개발사·진입 순위 짚기)
2. 큰 폭 상승작 (가능하면 이유 추정 — 신규 콘텐츠·이벤트·시즌 등)
3. 큰 폭 하락작
4. 전체 차트 트렌드 (장르 분포·개발사 변화)
5. 사업PM이 주목할 신호 1~2가지

군더더기 없이 간결하게."""
    
    response = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=2000,
        messages=[{'role': 'user', 'content': prompt}],
    )
    return response.content[0].text


def create_excel_report(current, changes, summary):
    """엑셀 보고서 생성 (요약 / 이번 주 차트 / 변화 시트)."""
    today = datetime.now().strftime('%Y%m%d')
    filename = f'mobile_chart_{today}.xlsx'
    
    wb = Workbook()
    
    # 시트 1: 주간 요약
    ws = wb.active
    ws.title = '주간 요약'
    ws['A1'] = f'한국 모바일 게임 차트 주간 보고서 ({datetime.now().strftime("%Y-%m-%d")})'
    ws['A1'].font = Font(bold=True, size=14)
    ws.merge_cells('A1:D1')
    
    ws['A3'] = 'Claude 분석 요약'
    ws['A3'].font = Font(bold=True, size=12)
    ws['A4'] = summary
    ws['A4'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.column_dimensions['A'].width = 100
    ws.row_dimensions[4].height = 500
    
    # 시트 2: 이번 주 전체 차트
    ws2 = wb.create_sheet('이번 주 차트')
    df = pd.DataFrame(current)
    if not df.empty:
        for r in dataframe_to_rows(df, index=False, header=True):
            ws2.append(r)
        for cell in ws2[1]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color='DDDDDD', end_color='DDDDDD', fill_type='solid')
        for col_letter, width in [('A', 8), ('B', 30), ('C', 40), ('D', 25), ('E', 8), ('F', 15), ('G', 20)]:
            ws2.column_dimensions[col_letter].width = width
    
    # 시트 3: 주간 변화
    if not changes.get('is_first_week'):
        ws3 = wb.create_sheet('주간 변화')
        row = 1
        
        ws3.cell(row=row, column=1, value='■ 신규 진입').font = Font(bold=True, size=12)
        row += 1
        for item in changes.get('new_entries', []):
            ws3.cell(row=row, column=1, value=item['title'])
            ws3.cell(row=row, column=2, value=item['platform'])
            ws3.cell(row=row, column=3, value=f"{item['rank']}위 진입")
            row += 1
        
        row += 2
        ws3.cell(row=row, column=1, value='■ 큰 폭 상승 (5등 이상)').font = Font(bold=True, size=12)
        row += 1
        for item in sorted(changes.get('rank_changes', []), key=lambda x: -x['change'])[:15]:
            if item['change'] > 0:
                ws3.cell(row=row, column=1, value=item['title'])
                ws3.cell(row=row, column=2, value=item['platform'])
                ws3.cell(row=row, column=3, value=f"{item['prev_rank']}위 → {item['curr_rank']}위 (▲{item['change']})")
                row += 1
        
        row += 2
        ws3.cell(row=row, column=1, value='■ 큰 폭 하락 (5등 이상)').font = Font(bold=True, size=12)
        row += 1
        for item in sorted(changes.get('rank_changes', []), key=lambda x: x['change'])[:15]:
            if item['change'] < 0:
                ws3.cell(row=row, column=1, value=item['title'])
                ws3.cell(row=row, column=2, value=item['platform'])
                ws3.cell(row=row, column=3, value=f"{item['prev_rank']}위 → {item['curr_rank']}위 (▼{abs(item['change'])})")
                row += 1
        
        row += 2
        ws3.cell(row=row, column=1, value='■ 차트 이탈').font = Font(bold=True, size=12)
        row += 1
        for item in changes.get('dropped', [])[:15]:
            ws3.cell(row=row, column=1, value=item['title'])
            ws3.cell(row=row, column=2, value=item['platform'])
            ws3.cell(row=row, column=3, value=f"이전 {item['rank']}위에서 이탈")
            row += 1
        
        for col_letter, width in [('A', 35), ('B', 15), ('C', 30)]:
            ws3.column_dimensions[col_letter].width = width
    
    wb.save(filename)
    return filename


def send_email_via_gmail(subject, html_body, attachment_path):
    """Gmail SMTP로 첨부파일 포함 메일 발송.
    
    인증: 2단계 인증 활성화된 Gmail의 16자리 앱 비밀번호 사용.
    포트: 465 (SSL).
    """
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    with open(attachment_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename={os.path.basename(attachment_path)}'
    )
    msg.attach(part)
    
    # 앱 비밀번호의 공백 제거 (사용자가 공백 포함 복사 경우 대비)
    app_password = GMAIL_APP_PASSWORD.replace(' ', '')
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(GMAIL_USER, app_password)
        server.send_message(msg)
    print(f"[OK] 메일 발송 완료: {RECIPIENT_EMAIL} (Gmail SMTP)")


def main():
    print(f"\n=== 한국 모바일 게임 차트 수집 ({datetime.now()}) ===\n")
    
    missing = [k for k, v in {
        'ANTHROPIC_API_KEY': ANTHROPIC_API_KEY,
        'GMAIL_USER': GMAIL_USER,
        'GMAIL_APP_PASSWORD': GMAIL_APP_PASSWORD,
        'RECIPIENT_EMAIL': RECIPIENT_EMAIL,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"환경변수 누락: {missing}")
    
    print("[1/5] Google Play 매출 차트 수집...")
    gp_data = fetch_google_play_top_grossing_kr_games(100)
    print(f"      → {len(gp_data)}개 수집 완료")
    
    print("[2/5] App Store 인기 차트 수집...")
    apple_data = fetch_apple_top_charts_kr_games(100)
    print(f"      → {len(apple_data)}개 수집 완료")
    
    current = gp_data + apple_data
    if not current:
        raise RuntimeError("데이터 수집 실패. 차트 수집 함수 점검 필요.")
    
    print("[3/5] 이전 주 데이터와 비교...")
    previous = load_previous_data()
    changes = compute_changes(previous, current)
    if changes.get('is_first_week'):
        print("      → 첫 실행. 다음 주부터 변화 분석 시작.")
    else:
        print(f"      → 신규 진입 {len(changes.get('new_entries', []))}개 / 이탈 {len(changes.get('dropped', []))}개 / 큰 폭 변동 {len(changes.get('rank_changes', []))}개")
    
    print("[4/5] Claude로 요약 생성 중...")
    summary = generate_summary_with_claude(current, changes)
    print("─" * 60)
    print(summary)
    print("─" * 60)
    
    print("[5/5] 엑셀 보고서 생성 및 메일 발송...")
    excel_path = create_excel_report(current, changes, summary)
    
    today = datetime.now().strftime('%Y-%m-%d')
    subject = f'[모바일 게임 차트] 주간 보고 {today}'
    html_body = f"""
    <div style="font-family: 'Malgun Gothic', sans-serif; line-height: 1.6;">
      <h2>한국 모바일 게임 차트 주간 보고서</h2>
      <p><strong>수집일:</strong> {today}</p>
      <p><strong>수집 항목:</strong> Google Play 매출 Top 100 + App Store 인기 Top 100</p>
      <hr/>
      <h3>📊 Claude 분석 요약</h3>
      <pre style="white-space: pre-wrap; font-family: 'Malgun Gothic', sans-serif; line-height: 1.7; background: #f8f8f8; padding: 16px; border-radius: 4px;">{summary}</pre>
      <p>전체 차트와 상세 변화는 첨부 엑셀 파일에서 확인하세요.</p>
    </div>
    """
    send_email_via_gmail(subject, html_body, excel_path)
    
    save_current_data(current)
    print("\n=== 완료 ===\n")


if __name__ == '__main__':
    main()
