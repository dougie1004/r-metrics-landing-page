import streamlit as st
import time

# --------------------
# 1. 페이지 설정 및 디자인
# --------------------

st.set_page_config(
    page_title="R-메트릭스 (R-Metrics)",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Tailwind CSS의 젊은 느낌을 Streamlit Markdown과 Custom CSS로 표현
st.markdown("""
<style>
    /* Vibrant Gradient Header Background */
    .vibrant-header {
        background: linear-gradient(135deg, #6366f1 0%, #3b82f6 100%);
        color: white;
        padding: 3rem 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .vibrant-header h1 {
        font-size: 2.5em;
        font-weight: 800;
    }
    .vibrant-header p {
        font-size: 1.2em;
        font-weight: 300;
        opacity: 0.9;
    }
    /* Map Simulator Placeholder */
    .map-simulator {
        height: 350px;
        background-color: #e0e7ff; 
        background-image: url('https://placehold.co/800x400/ccd5ff/374151?text=Your+Map+Simulation+Here');
        background-size: cover;
        border-radius: 12px;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    /* Result Card Styling */
    .ranking-card {
        padding: 1rem;
        border-radius: 10px;
        border-left: 8px solid #3b82f6;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
        background-color: white;
    }
    .ranking-score {
        font-size: 1.5rem;
        font-weight: bold;
        color: #6366f1;
    }
</style>
""", unsafe_allow_html=True)


# --------------------
# 2. 히어로 섹션
# --------------------

st.markdown(
    """
    <div class="vibrant-header">
        <h1>당신의 창업, 실패율 0%에 도전하세요.</h1>
        <p>R-메트릭스: AI R-Score가 당신의 잠재 상권을 초정밀 1km 반경으로 분석합니다.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <h2 style='text-align: center; font-weight: 800; color: #3b82f6;'>
        📍 내 가게 위치, 성공 점수는?
    </h2>
    <p style='text-align: center; color: #6b7280; margin-bottom: 2rem;'>
        원하는 주소와 반경을 입력하고, AI R-Score가 예측한 유망 업종을 지금 바로 확인해보세요.
    </p>
""", unsafe_allow_html=True)


# --------------------
# 3. 실시간 데모 (시뮬레이션)
# --------------------

# 가상 분석 결과 데이터 (선릉로 130길 19 기반)
MOCK_ANALYSIS_RESULTS = [
    {"rank": 1, "name": "기타 외국식 음식점", "score": 92, "reason": "높은 직장인 수요 대비 낮은 경쟁 밀집도."},
    {"rank": 2, "name": "사무/행정 지원 서비스", "score": 90, "reason": "주변 오피스 밀집 지역 특성상 안정적인 수요 및 폐업률 낮음."},
    {"rank": 3, "name": "프리미엄 미용/피부 미용", "score": 85, "reason": "고급 주거지역 배후 인구의 높은 미용 소비 지출."}
]

# 지도 시뮬레이션 Placeholder
st.markdown("<div class='map-simulator'><p style='color: #374151;'>지도 시뮬레이션 영역: 반경 기반 분석 영역 표시</p></div>", unsafe_allow_html=True)

# 입력 폼
with st.form("analysis_form"):
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        address = st.text_input("창업 희망 주소 입력", value="예: 선릉로 130길 19", help="실제 데이터를 불러오지 않고 시뮬레이션됩니다.")
    
    with col2:
        radius = st.selectbox("분석 반경 (m)", ["300", "500", "1000"], index=1)

    with col3:
        analyze_button = st.form_submit_button("AI R-Score 분석 시작", type="primary")

    if analyze_button:
        if not address:
            st.error("주소를 입력해주세요.")
        else:
            # 로딩 스피너 및 시간 지연 시뮬레이션
            with st.spinner(f"'{address}' 반경 {radius}m 상권 데이터를 분석 중입니다..."):
                time.sleep(3)  # 3초 로딩 시뮬레이션

            # --------------------
            # 4. 결과 표시 영역
            # --------------------
            st.markdown("---")
            st.markdown(f"""
                <h3 style='font-weight: 800; color: #6366f1; font-size: 1.8em;'>
                    🏆 R-메트릭스가 예측한 유망 업종 TOP 3
                </h3>
                <p style='color: #6b7280; font-size: 0.9em;'>
                    '{address}' 주소 반경 {radius}m 지역에 대한 AI R-Score 분석 결과입니다.
                </p>
            """, unsafe_allow_html=True)

            # 결과 카드 표시
            for item in MOCK_ANALYSIS_RESULTS:
                st.markdown(
                    f"""
                    <div class='ranking-card'>
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div>
                                <span class='ranking-score'>{item['rank']}위</span>
                                <span style='font-size: 1.1rem; font-weight: bold; margin-left: 10px;'>{item['name']} ({item['score']}점)</span>
                            </div>
                            <span style='color: #6b7280; font-size: 0.9em;'>{item['reason']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.success("분석이 완료되었습니다. 자세한 리포트는 정식 출시 후 프리미엄 서비스에서 확인 가능합니다.")
            st.balloons() # 시연 효과

# --------------------
# 5. 사전 신청 섹션
# --------------------

st.markdown("---")
st.markdown("<h2 style='text-align: center; font-weight: 800; color: #3b82f6;'>✨ 지금 바로 R-메트릭스 소식을 받아보세요!</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>정식 출시 알림 신청자에게는 **첫 달 프리미엄 리포트 50% 할인 쿠폰**을 드립니다.</p>", unsafe_allow_html=True)

col_email, col_btn = st.columns([3, 1])

with col_email:
    user_email = st.text_input("이메일 주소를 입력해주세요", placeholder="email@example.com", label_visibility="collapsed")

with col_btn:
    if st.button("알림 신청하고 쿠폰 받기", use_container_width=True):
        if "@" in user_email and "." in user_email:
            st.success(f"[성공!] {user_email} 주소로 정식 출시 알림이 등록되었습니다. 감사합니다!")
            # 실제 서비스에서는 이메일을 DB에 저장하는 로직이 필요함
        else:
            st.error("유효한 이메일 주소를 입력해주세요.")

# --------------------
# 6. 푸터
# --------------------

st.markdown("""
---
<p style='text-align: center; color: #9ca3af; font-size: 0.8em; margin-top: 1rem;'>
    R-메트릭스 (R-Metrics) | &copy; 2025 All Rights Reserved.
</p>
<p style='text-align: center; color: #9ca3af; font-size: 0.7em;'>
    본 서비스는 소상공인 창업 성공률 증진을 위해 빅데이터를 활용합니다.
</p>
""", unsafe_allow_html=True)
