import streamlit as st
import random
import time

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="💰 인생 역전! 운명의 로또",
    page_icon="🎱",
    layout="centered"
)

# --- 2. 디자인 & 헤더 ---
st.title("🎱 오늘의 운명 로또")
st.subheader("우주의 기운을 모아 번호를 뽑아드립니다.")
st.markdown("---")

# --- 3. 사용자 입력 ---
name = st.text_input("당신의 이름을 알려주세요", placeholder="예: 손지호")

# 운세 멘트 리스트 (랜덤 출력용)
fortunes = [
    "오늘 동쪽에서 귀인을 만날 운세입니다! 🏃",
    "황금빛 기운이 당신을 감싸고 있습니다. ✨",
    "지나가던 강아지도 당신을 보고 웃을 좋은 날입니다. 🐶",
    "지금 당장 복권방으로 달려가야 할 타이밍! ⏱️",
    "뜻밖의 횡재수가 보입니다. 주머니를 비워두세요. 💸",
    "솔직히 말하면, 오늘 감이 아주 좋습니다. 😎"
]

# 행운의 색상 리스트
colors = ["빨강 (Red)", "파랑 (Blue)", "노랑 (Yellow)", "초록 (Green)", "보라 (Purple)", "황금색 (Gold)"]

# --- 4. 로직 실행 (버튼 클릭) ---
if st.button("🔮 운명의 번호 추출하기"):
    if name == "":
        st.warning("이름을 입력해야 우주의 기운을 모을 수 있어요!")
    else:
        # (1) 분석하는 척 애니메이션 (신뢰감 상승 요소)
        with st.spinner(f'{name}님의 바이오리듬과 우주 에너지를 분석 중...'):
            time.sleep(2) # 2초 뜸들이기
        
        # (2) 운세 & 행운의 색 보여주기
        today_fortune = random.choice(fortunes)
        today_color = random.choice(colors)
        
        st.success("분석 완료!")
        
        st.markdown(f"### 📜 {name}님의 오늘의 운세")
        st.info(f"💌 {today_fortune}")
        st.caption(f"🎨 행운의 색: **{today_color}**")
        
        st.markdown("---")
        
        # (3) 로또 번호 생성 (가중치 없이 순수 랜덤이지만, 뭔가 있어보이게)
        lotto_numbers = sorted(random.sample(range(1, 46), 6))
        
        st.markdown("### 🎱 당신을 위한 운명의 번호")
        
        # 번호를 예쁘게 보여주기 위한 컬럼 나누기
        cols = st.columns(6)
        for i, number in enumerate(lotto_numbers):
            # 각 번호를 카드처럼 표시
            cols[i].metric(label=f"{i+1}구", value=str(number))
            
        st.balloons() # 풍선 날리기 효과 (축하)
        st.markdown("#### 이 번호가 당첨되면 저(비서) 잊지 마세요! 😉")