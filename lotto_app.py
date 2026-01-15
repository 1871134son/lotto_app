import streamlit as st
import random
import time
from datetime import datetime

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="미숙이 & 영숙이네 로또",
    page_icon="🧧",
    layout="centered"
)

# --- 2. 상태 관리 ---
if 'step' not in st.session_state:
    st.session_state.step = 'input'

# --- 3. CSS (타이틀 밝기 수정 완료!) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&family=Noto+Sans+KR:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nanum Myeongjo', serif;
        background-color: #0f0f0f;
        color: #f0e6d2;
    }

    .stApp {
        background: radial-gradient(circle, #222, #000);
        background-image: url('https://www.transparenttextures.com/patterns/black-linen.png');
    }

    /* 헤더 박스 */
    .header-box {
        border: 4px double #d4af37;
        background-color: rgba(20, 20, 20, 0.8);
        padding: 30px; text-align: center; margin-bottom: 30px;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.15);
    }
    
    /* ★★★ [수정됨] 메인 타이틀: 눈부시게 밝은 황금 그라데이션 적용 ★★★ */
    .main-title {
        font-size: 42px; /* 크기도 살짝 키움 */
        font-weight: 900; /* 더 두껍게 */
        margin: 0;
        /* 흰색 -> 밝은 금색 -> 진한 금색으로 이어지는 그라데이션 */
        background: linear-gradient(to bottom, #ffffff 0%, #fceabb 30%, #d4af37 70%, #aa771c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        /* 밝은 금색 발광 효과 */
        filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.8));
        letter-spacing: -2px;
    }
    .sub-title { color: #fceabb; font-size: 16px; margin-top: 15px; font-family: 'Noto Sans KR'; font-weight:bold;}

    /* 입력 프레임 */
    .input-frame {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #554400; padding: 40px 30px; border-radius: 10px;
    }
    .gold-label { 
        color: #f0e6d2; font-size: 16px; font-weight: bold; margin-bottom: 8px; display: block; 
        border-left: 3px solid #d4af37; padding-left: 10px;
    }
    
    /* 입력창 가독성 */
    .stTextInput input, .stDateInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #f4e4bc !important; 
        color: #000 !important; 
        border: 2px solid #b8860b !important;
        font-weight: bold !important;
        border-radius: 5px !important;
    }
    .stSelectbox div[data-baseweb="select"] span { color: #000 !important; }

    /* 결과 카드 */
    .result-card {
        background: rgba(0, 0, 0, 0.9);
        border: 4px double #d4af37;
        padding: 30px; margin-top: 20px;
        box-shadow: 0 10px 50px rgba(0,0,0,0.8);
        text-align: center;
    }

    /* 사주 테이블 */
    table.saju-table {
        width: 100%; text-align: center; border-collapse: collapse; margin: 25px 0;
        border: 2px solid #d4af37; color: #000;
    }
    td.saju-header { 
        background-color: #3e2702; color: #d4af37; padding: 10px; font-weight: bold; border: 1px solid #d4af37;
    }
    td.saju-cell { 
        background-color: #fffcf0; color: #000; padding: 15px; font-size: 22px; font-weight: 900; border: 1px solid #d4af37; 
    }
    div.saju-desc { font-size: 12px; color: #555; margin-top: 5px; font-weight: normal; }
    
    /* 로또 공 */
    .ball-wrapper {
        display: flex; justify-content: center; align-items: center; gap: 10px; margin: 30px 0; flex-wrap: wrap;
    }
    .lotto-ball {
        width: 55px; height: 55px; border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        font-size: 22px; font-weight: 900; color: white;
        box-shadow: inset -2px -2px 5px rgba(0,0,0,0.5);
        border: 2px solid rgba(255,255,255,0.4);
        font-family: 'Noto Sans KR'; text-shadow: 1px 1px 2px black;
    }
    .plus-sign { color: #d4af37; font-size: 24px; margin: 0 5px; }

    /* 결과 풀이 박스 */
    .solution-box {
        text-align: left; background: rgba(255, 255, 255, 0.1); padding: 25px; 
        border-radius: 10px; margin-top: 20px; border: 1px solid rgba(212, 175, 55, 0.5);
    }
    .solution-text {
        font-size: 16px; line-height: 1.8; color: #FFFFFF; margin: 0;
    }
    .highlight { color: #ff6b6b; font-weight: bold; font-size: 18px; }

    /* 지분 확보 텍스트 스타일 */
    .jiho-tax {
        margin-top: 30px;
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: #f4e4bc; /* 밝은 금색 */
        font-weight: bold;
        font-size: 16px;
        border: 1px dashed #d4af37;
        animation: blink 2s infinite;
    }
    @keyframes blink {
        0% { border-color: #d4af37; }
        50% { border-color: #fff; }
        100% { border-color: #d4af37; }
    }

    /* 버튼 */
    div.stButton > button {
        background: linear-gradient(to bottom, #d4af37 0%, #8a6e2f 100%);
        color: #fff; font-size: 22px; font-weight: bold;
        padding: 18px 0; width: 100%; border-radius: 8px; border: 1px solid #ffd700;
        margin-top: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    div.stButton > button:hover { transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# --- 4. 로직 함수 ---

def get_ball_style(n):
    if n <= 10: return "background-color: #fbc400;" 
    elif n <= 20: return "background-color: #69c8f2;" 
    elif n <= 30: return "background-color: #ff7272;" 
    elif n <= 40: return "background-color: #aaaaaa;" 
    else: return "background-color: #b0d840;"

def get_ganji(year):
    cheongan = ["경", "신", "임", "계", "갑", "을", "병", "정", "무", "기"]
    jiji = ["신", "유", "술", "해", "자", "축", "인", "묘", "진", "사", "오", "미"]
    return f"{cheongan[year % 10]}{jiji[year % 12]}"

time_data = {
    "자시 (23:30~01:29)": "子", "축시 (01:30~03:29)": "丑", "인시 (03:30~05:29)": "寅", 
    "묘시 (05:30~07:29)": "卯", "진시 (07:30~09:29)": "辰", "사시 (09:30~11:29)": "巳",
    "오시 (11:30~13:29)": "午", "미시 (13:30~15:29)": "未", "신시 (15:30~17:29)": "申", 
    "유시 (17:30~19:29)": "酉", "술시 (19:30~21:29)": "戌", "해시 (21:30~23:29)": "亥"
}

# --- 5. UI 구성 ---

st.markdown("""
<div class="header-box">
    <h1 class="main-title">미숙이 & 영숙이네<br>로또추첨기!</h1>
    <div class="sub-title">정통 명리학(命理學) 기반 운세 분석</div>
</div>
""", unsafe_allow_html=True)

# [STEP 1] 입력
if st.session_state.step == 'input':
    st.markdown('<div class="input-frame">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="gold-label">성함 (한글)</span>', unsafe_allow_html=True)
        name = st.text_input("name", placeholder="예: 손지호", label_visibility="collapsed")
    with col2:
        st.markdown('<span class="gold-label">성함 (漢子 - 선택)</span>', unsafe_allow_html=True)
        name_hanja = st.text_input("name_hanja", placeholder="예: 孫志浩", label_visibility="collapsed")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<span class="gold-label" style="margin-top:20px;">생년월일 (양력)</span>', unsafe_allow_html=True)
        birth = st.date_input("birth", min_value=datetime(1940, 1, 1), label_visibility="collapsed")
    with col4:
        st.markdown('<span class="gold-label" style="margin-top:20px;">태어난 시 (時)</span>', unsafe_allow_html=True)
        time_slot = st.selectbox("time", list(time_data.keys()), label_visibility="collapsed")

    st.markdown("---")
    
    st.markdown('<span class="gold-label">✋ 주로 사용하시는 손은?</span>', unsafe_allow_html=True)
    hand = st.radio("hand", ["오른손", "왼손", "양손"], horizontal=True, label_visibility="collapsed")
    
    col5, col6 = st.columns(2)
    with col5:
        st.markdown('<span class="gold-label" style="margin-top:20px;">👤 얼굴형은?</span>', unsafe_allow_html=True)
        face = st.selectbox("face", ["둥근형", "각진형", "계란형", "역삼각형"], label_visibility="collapsed")
    with col6:
        st.markdown('<span class="gold-label" style="margin-top:20px;">🌸 좋아하는 계절?</span>', unsafe_allow_html=True)
        season = st.selectbox("season", ["봄", "여름", "가을", "겨울"], label_visibility="collapsed")

    col7, col8 = st.columns(2)
    with col7:
        st.markdown('<span class="gold-label" style="margin-top:20px;">🌈 가장 끌리는 색상은?</span>', unsafe_allow_html=True)
        color_choice = st.selectbox("color", ["붉은색", "푸른색", "노란색", "흰색", "검은색"], label_visibility="collapsed")
    with col8:
        st.markdown('<span class="gold-label" style="margin-top:20px;">🛌 주로 주무시는 자세는?</span>', unsafe_allow_html=True)
        sleep_pose = st.selectbox("sleep", ["똑바로 누움", "옆으로 누움", "엎드려 누움"], label_visibility="collapsed")


    if st.button("신점(神占) 풀이 시작하기"):
        if name:
            st.session_state.name = name
            st.session_state.name_hanja = name_hanja if name_hanja else ""
            st.session_state.birth = birth
            st.session_state.time_hanja = time_data[time_slot]
            st.session_state.hand = hand
            st.session_state.face = face
            st.session_state.season = season
            st.session_state.color_choice = color_choice
            st.session_state.sleep_pose = sleep_pose
            st.session_state.step = 'loading'
            st.rerun()
        else:
            st.warning("성함을 입력해주셔야 운세를 볼 수 있습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

# [STEP 2] 로딩
elif st.session_state.step == 'loading':
    st.markdown('<div class="input-frame" style="text-align:center; padding: 80px 20px;">', unsafe_allow_html=True)
    msg = st.empty()
    bar = st.progress(0)
    
    steps = [
        f"「{st.session_state.name}」님의 사주팔자(四柱八字) 세우는 중...",
        f"관상({st.session_state.face})과 심리 상태 분석 중...",
        "부족한 오행의 기운을 파악하는 중...",
        "천지신명께 올릴 축문(祝文) 작성 중...",
        "점괘가 나왔습니다."
    ]
    for i, s in enumerate(steps):
        msg.markdown(f"<h3 style='color:#f0e6d2;'>🐢 {s}</h3>", unsafe_allow_html=True)
        time.sleep(1.2)
        bar.progress((i + 1) * 20)
        
    all_nums = random.sample(range(1, 46), 7)
    st.session_state.main_nums = sorted(all_nums[:6])
    st.session_state.bonus_num = all_nums[6]
    
    st.session_state.step = 'result'
    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# [STEP 3] 결과
elif st.session_state.step == 'result':
    st.balloons()
    
    ganjis = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    jijis = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    year_ganji = get_ganji(st.session_state.birth.year)
    month_h = random.choice(ganjis) + random.choice(jijis)
    day_h = random.choice(ganjis) + random.choice(jijis)
    time_h = random.choice(ganjis) + st.session_state.time_hanja
    
    display_name = f"{st.session_state.name}"
    if st.session_state.name_hanja:
        display_name += f"({st.session_state.name_hanja})"

    table_html = f"""
    <table class="saju-table">
        <tr>
            <td class="saju-header">시주 (時)</td>
            <td class="saju-header">일주 (日)</td>
            <td class="saju-header">월주 (月)</td>
            <td class="saju-header">년주 (年)</td>
        </tr>
        <tr>
            <td class="saju-cell">{time_h}<div class="saju-desc">자식/말년</div></td>
            <td class="saju-cell">{day_h}<div class="saju-desc">나/배우자</div></td>
            <td class="saju-cell">{month_h}<div class="saju-desc">부모/형제</div></td>
            <td class="saju-cell">{year_ganji}<div class="saju-desc">조상/초년</div></td>
        </tr>
    </table>
    """

    st.markdown(f"""
    <div class="result-card">
        <h2 style="color:#d4af37; margin-bottom:10px;">천기누설(天機漏洩) 결과</h2>
        <p style="color:#aaa; font-size:14px;">{display_name}님의 운세와 기운을 분석한 결과입니다.</p>
        {table_html}
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="solution-box">
        <p class="solution-text">
            🕊️ <strong>[신점 요약]</strong><br><br>
            귀하의 관상은 <strong>{st.session_state.face}</strong>이며, 
            주로 <strong>{st.session_state.hand}</strong>을 사용하십니다.<br><br>
            선호하시는 색상은 <strong>{st.session_state.color_choice}</strong>,
            수면 자세는 <strong>{st.session_state.sleep_pose}</strong>입니다.<br>
            또한, <strong>{st.session_state.season}</strong>의 기운이 함께하고 있습니다.<br><br>
            이러한 귀하의 기운을 바탕으로 천지신명이 점지한 숫자를 공개합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    balls_html = '<div class="ball-wrapper">'
    for num in st.session_state.main_nums:
        style = get_ball_style(num)
        balls_html += f'<div class="lotto-ball" style="{style}">{num}</div>'
    
    bonus_style = get_ball_style(st.session_state.bonus_num)
    balls_html += f'''
        <div class="plus-sign">+</div>
        <div style="text-align:center;">
            <div class="lotto-ball" style="{bonus_style} border:3px solid #d4af37;">{st.session_state.bonus_num}</div>
            <span style="font-size:12px; color:#d4af37; margin-top:5px;">보너스</span>
        </div>
    </div>
    '''
    st.markdown(balls_html, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="jiho-tax">
            "당첨되면 지호에게 10프로 나눠주기~!" 💸
        </div>
        <hr style="border:1px solid #333; margin:20px 0;">
        <p style="font-size:14px; color:#f4e4bc; font-weight:bold;">
            "운명은 준비된 자에게 미소 짓습니다."<br>
            - 미숙 & 영숙 드림 -
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 다른 가족도 봐주기"):
        st.session_state.step = 'input'
        st.rerun()