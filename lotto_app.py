import streamlit as st
import random
import time
from datetime import datetime

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="미숙이 & 영숙이네 로또",
    page_icon="🐢",
    layout="centered"
)

# --- 2. 상태 관리 ---
if 'step' not in st.session_state:
    st.session_state.step = 'input'

# --- 3. CSS (버튼 여백 & 배경 패턴 수정) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&family=Noto+Sans+KR:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nanum Myeongjo', serif;
        background-color: #0b1021;
        color: #f4e4bc;
    }

    /* ★ 배경 패턴 변경: 거북이 등껍질 느낌의 중후한 패턴 ★ */
    .stApp {
        background: radial-gradient(circle at 50% 30%, #1a253a, #090c14);
        background-image: url('https://www.transparenttextures.com/patterns/black-scales.png');
    }

    /* 간판 */
    .gold-plate {
        border: 3px double #d4af37;
        border-radius: 8px;
        padding: 5px;
        margin-bottom: 30px;
        background-color: rgba(15, 23, 42, 0.95); /* 배경 덜 비치게 수정 */
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.2);
    }
    .inner-plate { border: 1px solid #b8860b; padding: 30px 20px; text-align: center; }
    .main-title {
        font-size: 38px; font-weight: 800; margin: 0;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { color: #d4af37; font-size: 14px; margin-top: 10px; letter-spacing: 2px; }

    /* 입력창 컨테이너 */
    .input-frame {
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid #554400;
        padding: 35px;
        border-radius: 15px;
    }
    .gold-label { color: #fcf6ba; font-size: 15px; margin-bottom: 8px; display: block; font-weight: bold; }
    
    /* 입력 위젯 (가독성 유지) */
    .stTextInput input {
        background-color: #f4e4bc !important;
        color: #000000 !important;
        border: 2px solid #b8860b !important;
        font-weight: bold !important;
    }
    .stDateInput input {
        background-color: #f4e4bc !important;
        color: #000000 !important;
        border: 2px solid #b8860b !important;
        font-weight: bold !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #f4e4bc !important;
        color: #000000 !important;
        border: 2px solid #b8860b !important;
    }
    .stSelectbox div[data-baseweb="select"] span {
        color: #000000 !important;
        font-weight: bold !important;
    }

    /* 결과 카드 */
    .certificate-box {
        background-color: rgba(0, 0, 0, 0.8);
        color: #f4e4bc;
        padding: 30px;
        border: 4px double #d4af37;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 10px 50px rgba(0,0,0,0.8);
    }
    
    /* 로또 공 */
    .ball-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
        margin: 40px 0;
    }
    .gem-ball {
        width: 55px; height: 55px; border-radius: 50%;
        display: inline-flex; justify-content: center; align-items: center;
        font-size: 22px; font-weight: 900; color: white;
        box-shadow: inset -3px -3px 8px rgba(0,0,0,0.6), inset 3px 3px 8px rgba(255,255,255,0.4);
        border: 1px solid rgba(255,255,255,0.3);
        text-shadow: 1px 1px 2px black;
    }
    .plus-sign {
        color: #d4af37; font-size: 24px; font-weight: bold; margin: 0 5px;
        padding-bottom: 5px;
    }
    
    /* 정보 그리드 */
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-top: 30px;
        text-align: left;
    }
    .info-item {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #554400;
    }
    .info-title { color: #888; font-size: 12px; margin-bottom: 5px; }
    .info-content { color: #fcf6ba; font-size: 16px; font-weight: bold; }

    /* ★ 버튼 스타일 (숨통 트임!) ★ */
    div.stButton > button {
        background: linear-gradient(to bottom, #fcf6ba 0%, #d4af37 100%);
        color: #2c2000; 
        font-weight: 800; 
        font-size: 22px; /* 글자 크기 키움 */
        border: 1px solid #fff; 
        padding: 20px 0; /* ★ 패딩 대폭 증가 (숨막힘 해결) ★ */
        margin-top: 20px; /* 위쪽 여백 추가 */
        width: 100%;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
        line-height: 1.0; /* 줄 간격 조정 */
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5); }
</style>
""", unsafe_allow_html=True)

# --- 4. 로직 함수 ---
def get_gem_style(n):
    if n <= 10: return "background: radial-gradient(circle at 30% 30%, #ffd700, #b8860b);"
    elif n <= 20: return "background: radial-gradient(circle at 30% 30%, #00bfff, #005f99);"
    elif n <= 30: return "background: radial-gradient(circle at 30% 30%, #ff6347, #8b0000);"
    elif n <= 40: return "background: radial-gradient(circle at 30% 30%, #a9a9a9, #444444);"
    else: return "background: radial-gradient(circle at 30% 30%, #32cd32, #006400);"

time_list = [
    "자시 (밤 11:30 ~ 새벽 1:29)", "축시 (새벽 1:30 ~ 3:29)", "인시 (새벽 3:30 ~ 5:29)", 
    "묘시 (아침 5:30 ~ 7:29)", "진시 (아침 7:30 ~ 9:29)", "사시 (오전 9:30 ~ 11:29)",
    "오시 (낮 11:30 ~ 1:29)", "미시 (오후 1:30 ~ 3:29)", "신시 (오후 3:30 ~ 5:29)", 
    "유시 (저녁 5:30 ~ 7:29)", "술시 (밤 7:30 ~ 9:29)", "해시 (밤 9:30 ~ 11:29)"
]

# --- 5. UI 구성 ---

# [헤더]
st.markdown("""
<div class="gold-plate">
    <div class="inner-plate">
        <h1 class="main-title">미숙이 & 영숙이네<br>로또추첨기!</h1>
        <div class="sub-title">천지신명(天地神明)의 기운을 담은 명품 번호</div>
    </div>
</div>
""", unsafe_allow_html=True)

# [STEP 1] 입력 화면
if st.session_state.step == 'input':
    st.markdown('<div class="input-frame">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="gold-label">성명 (姓名)</span>', unsafe_allow_html=True)
        name = st.text_input("name", placeholder="이름 입력", label_visibility="collapsed")
        
        st.markdown('<span class="gold-label" style="margin-top:20px;">생년월일</span>', unsafe_allow_html=True)
        birth = st.date_input("birth", min_value=datetime(1950, 1, 1), label_visibility="collapsed")

    with col2:
        st.markdown('<span class="gold-label">태어난 시 (時)</span>', unsafe_allow_html=True)
        time_slot = st.selectbox("time", time_list, label_visibility="collapsed")
        
        st.markdown('<span class="gold-label" style="margin-top:20px;">간절한 소원</span>', unsafe_allow_html=True)
        wish = st.selectbox("wish", ["금전재물 (로또당첨)", "만사형통 (운수대통)", "무병장수 (건강기원)"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("천기누설(天機漏洩) 번호 받기"):
        if name:
            st.session_state.name = name
            st.session_state.step = 'loading'
            st.rerun()
        else:
            st.warning("성명을 입력해주셔야 기운을 모을 수 있습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

# [STEP 2] 로딩
elif st.session_state.step == 'loading':
    st.markdown('<div class="input-frame" style="text-align:center; padding: 80px 20px;">', unsafe_allow_html=True)
    
    msg_box = st.empty()
    bar = st.progress(0)
    
    msgs = [
        f"「{st.session_state.name}」님의 사주를 풀이합니다...",
        "오행(五行) 기운과 조화를 이루는 숫자 탐색...",
        "황금 거북이가 길(吉)한 방위를 살피는 중...",
        "강력한 재물운을 숫자에 불어넣는 중...",
        "운명의 점지 준비 완료."
    ]
    
    for i, msg in enumerate(msgs):
        msg_box.markdown(f"<h3 style='color:#fcf6ba;'>🐢 {msg}</h3>", unsafe_allow_html=True)
        time.sleep(1.0)
        bar.progress((i + 1) * 20)
        
    # 데이터 생성
    all_nums = random.sample(range(1, 46), 7)
    st.session_state.main_nums = sorted(all_nums[:6])
    st.session_state.bonus_num = all_nums[6]
    
    # ★ 핵심 수정: 점수 범위를 40~99로 넓혀서 리얼리티 부여 ★
    st.session_state.wealth_score = random.randint(40, 99)
    
    colors = ["황금색 (Gold)", "붉은색 (Red)", "청색 (Blue)", "백색 (White)", "흑색 (Black)"]
    st.session_state.lucky_color = random.choice(colors)
    
    directions = ["동쪽 (East)", "서쪽 (West)", "남쪽 (South)", "북쪽 (North)"]
    st.session_state.direction = random.choice(directions)
    
    spots = ["은행 근처 명당", "버스 정류장 앞", "사람 많은 편의점", "시장 입구 복권방", "강가/물가 근처", "동네 오래된 슈퍼"]
    st.session_state.lucky_spot = random.choice(spots)
    
    st.session_state.step = 'result'
    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [STEP 3] 결과
elif st.session_state.step == 'result':
    # 점수가 80점 이상일 때만 풍선 효과 (희소성)
    if st.session_state.wealth_score >= 80:
        st.balloons()
    
    st.markdown(f"""
    <div class="certificate-box">
        <h2 style="font-family:'Nanum Myeongjo'; font-weight:800; color:#fcf6ba; margin-bottom:10px;">운 명 증 서</h2>
        <p style="font-size:14px; color:#aaa; margin-bottom:30px;">
            {st.session_state.name}님의 기운을 분석하여 점지한<br>
            <strong>운명(運命)</strong>의 숫자입니다.
        </p>
    """, unsafe_allow_html=True)
    
    # 번호 출력
    balls_html = '<div class="ball-wrapper">'
    for num in st.session_state.main_nums:
        style = get_gem_style(num)
        balls_html += f'<div class="gem-ball" style="{style}">{num}</div>'
    
    # 보너스
    bonus_style = get_gem_style(st.session_state.bonus_num)
    balls_html += f'''
        <div class="plus-sign">+</div>
        <div style="display:flex; flex-direction:column; align-items:center;">
            <div class="gem-ball" style="{bonus_style} border:2px solid #d4af37;">{st.session_state.bonus_num}</div>
            <span style="font-size:11px; color:#d4af37; margin-top:3px;">보너스</span>
        </div>
    </div>
    '''
    st.markdown(balls_html, unsafe_allow_html=True)
    
    # 점수에 따른 멘트 및 색상 처리
    score = st.session_state.wealth_score
    score_color = "#ff6b6b" if score >= 80 else "#feca57" if score >= 60 else "#a4b0be"
    score_comment = "대박 기운이 가득합니다! 🚀" if score >= 80 else "소소한 행운이 따릅니다. 🙂" if score >= 60 else "욕심은 금물! 재미로만 하세요. 🤔"

    # 상세 정보
    st.markdown(f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-title">💰 오늘의 재물운</div>
            <div class="info-content" style="color:{score_color};">{score}점 <span style="font-size:12px; color:#aaa;">({score_comment})</span></div>
        </div>
        <div class="info-item">
            <div class="info-title">🎨 행운의 색상</div>
            <div class="info-content" style="color:#4ecdc4;">{st.session_state.lucky_color}</div>
        </div>
        <div class="info-item">
            <div class="info-title">🧭 구매 추천 방위</div>
            <div class="info-content">{st.session_state.direction}</div>
        </div>
        <div class="info-item">
            <div class="info-title">🏪 행운의 명당</div>
            <div class="info-content">{st.session_state.lucky_spot}</div>
        </div>
    </div>
    
    <div style="margin-top:30px; border-top:1px solid rgba(255,255,255,0.1); padding-top:20px;">
        <p style="font-size:15px; line-height:1.6; color:#e2e2e2;">
            "귀하의 간절한 염원이 하늘에 닿았습니다.<br>
            이 번호와 함께 큰 행운이 깃들기를 기원합니다."
        </p>
        <p style="font-size:12px; color:#888; margin-top:20px;">미숙 & 영숙 드림</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔄 처음으로 돌아가기"):
        st.session_state.step = 'input'
        st.rerun()