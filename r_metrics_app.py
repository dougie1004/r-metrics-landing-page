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
    .financial-box {
        background-color: #f3f4f6;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin-top: 1.5rem;
    }
    /* 모바일 환경 최적화를 위해 일부 컬럼 레이아웃을 해제 */
    @media (max-width: 768px) {
        .stColumns > div {
            width: 100% !important;
            flex: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# --------------------
# 2. Mock 데이터 및 시뮬레이션 함수
# --------------------

MOCK_ANALYSIS_RESULTS = [
    {"rank": 1, "name": "기타 외국식 음식점", "score": 92, "reason": "높은 직장인 수요 대비 낮은 경쟁 밀집도."},
    {"rank": 2, "name": "사무/행정 지원 서비스", "score": 90, "reason": "주변 오피스 밀집 지역 특성상 안정적인 수요 및 폐업률 낮음."},
    {"rank": 3, "name": "프리미엄 미용/피부 미용", "score": 85, "reason": "고급 주거지역 배후 인구의 높은 미용 소비 지출."}
]

def simulate_net_profit(capital, rent, area_pyeong, r_score=90):
    """
    재무 변수를 기반으로 월 순이익 범위를 시뮬레이션하는 목업 함수.
    실제 서비스에서는 R-Score, 업종, 면적 등을 반영한 정교한 AI 모델이 사용됨.
    """
    if capital <= 0 or rent <= 0 or area_pyeong <= 0:
        return (0, 0)
    
    # 1. 초기 투자금 잔여율 기반 리스크 계수 (자본금 많을수록 리스크 낮음)
    # 초기 투자금 (가상): 보증금(10개월분) + 인테리어(평당 150만원)
    initial_investment_mock = (rent * 10) + (area_pyeong * 1500000)
    
    if initial_investment_mock >= capital:
        # 투자금 부족 시 수익률 하락 시뮬레이션
        risk_factor = 0.5 
    else:
        # 투자금 여유 시 안정적인 수익률 시뮬레이션
        risk_factor = 1.0 + (capital - initial_investment_mock) / capital * 0.2

    # 2. 월 매출 및 비용 계산 (R-Score는 잠재 고객 확보 능력으로 간주)
    base_revenue = 1000000 * area_pyeong * (r_score / 100) # R-Score와 면적에 비례
    
    # 월 비용 (임대료, 인건비(고정), 공과금(면적 비례), 기타)
    fixed_labor_cost = 3000000 # 가상 인건비
    utility_cost = 50000 * area_pyeong # 가상 공과금
    total_monthly_expense = rent + fixed_labor_cost + utility_cost
    
    # 3. 예상 월 순이익 범위 계산
    net_profit_center = (base_revenue * risk_factor) - total_monthly_expense
    
    # 변동폭 설정 (R-Score가 높을수록 변동폭 작아짐 = 안정적)
    volatility = 0.3 - (r_score / 100) * 0.1
    
    lower_bound = net_profit_center * (1 - volatility)
    upper_bound = net_profit_center * (1 + volatility)
    
    # 최소 순이익이 0보다 작을 수 없음
    lower_bound = max(0, lower_bound)

    return (int(lower_bound), int(upper_bound))


# --------------------
# 3. 히어로 섹션
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
        원하는 주소, 반경, 재무 변수를 입력하고 성공 시뮬레이션을 시작해보세요.
    </p>
""", unsafe_allow_html=True)


# --------------------
# 4. 실시간 데모 (시뮬레이션)
# --------------------

# 지도 시뮬레이션 Placeholder
st.markdown("<div class='map-simulator'><p style='color: #374151;'>지도 시뮬레이션 영역: 반경 기반 분석 영역 표시</p></div>", unsafe_allow_html=True)

# 입력 폼
with st.form("analysis_form"):
    
    # 상권 분석 변수
    st.subheader("1. 상권 및 위치 변수")
    # 데스크톱에서는 2:1 비율, 모바일에서는 100% 폭을 유지하도록 조정
    col1, col2 = st.columns([3, 1])
    with col1:
        address = st.text_input("창업 희망 주소 입력", value="예: 선릉로 130길 19", help="실제 데이터를 불러오지 않고 시뮬레이션됩니다.")
    
    with col2:
        radius = st.selectbox("분석 반경 (m)", ["300", "500", "1000"], index=1)

    # 재무 시뮬레이션 변수
    st.subheader("2. 재무 변수 입력 (순이익 예측)")
    # 모바일 환경에서 컬럼이 좁아지는 것을 방지하기 위해 단일 컬럼으로 변경
    # 데스크톱에서만 3개의 컬럼으로 보이게 하려면 CSS를 사용해야 하지만, Streamlit의 기본 반응형 동작을 따름
    
    initial_capital = st.number_input("초기 자본금 (만원)", min_value=0, value=7000, step=100) * 10000
    monthly_rent = st.number_input("월 임대료 (만원)", min_value=0, value=250, step=10) * 10000
    area_pyeong = st.number_input("면적 (평)", min_value=1, value=15, step=1)

    analyze_button = st.form_submit_button("AI R-Score 및 재무 시뮬레이션 시작", type="primary")


    if analyze_button:
        if not address or initial_capital <= 0 or monthly_rent <= 0 or area_pyeong <= 0:
            st.error("모든 필수 입력값을 정확히 입력해주세요.")
        else:
            # 로딩 스피너 및 시간 지연 시뮬레이션
            with st.spinner(f"'{address}' 지역의 R-Score와 재무 시뮬레이션을 진행 중입니다..."):
                time.sleep(3)  # 3초 로딩 시뮬레이션

            # --------------------
            # 5. 결과 표시 영역
            # --------------------
            st.markdown("---")
            st.markdown(f"""
                <h3 style='font-weight: 800; color: #6366f1; font-size: 1.8em;'>
                    📊 종합 분석 보고서
                </h3>
            """, unsafe_allow_html=True)

            # R-Score 결과
            st.markdown(f"""
                <h4 style='font-weight: 700; color: #3b82f6; margin-top: 1rem;'>
                    🏆 1. AI R-Score 유망 업종 TOP 3
                </h4>
                <p style='color: #6b7280; font-size: 0.9em; margin-bottom: 1rem;'>
                    '{address}' 주소 반경 {radius}m 지역에 대한 AI R-Score 분석 결과입니다.
                </p>
            """, unsafe_allow_html=True)

            for item in MOCK_ANALYSIS_RESULTS:
                st.markdown(
                    f"""
                    <div class='ranking-card'>
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div>
                                <span class='ranking-score'>{item['rank']}위</span>
                                <span style='font-size: 1.1rem; font-weight: bold; margin-left: 10px;'>{item['name']} (R-Score: {item['score']}점)</span>
                            </div>
                            <span style='color: #6b7280; font-size: 0.9em;'>{item['reason']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # 재무 시뮬레이션 결과
            lower, upper = simulate_net_profit(initial_capital, monthly_rent, area_pyeong, MOCK_ANALYSIS_RESULTS[0]['score'])
            
            st.markdown(f"""
                <h4 style='font-weight: 700; color: #3b82f6; margin-top: 2rem;'>
                    💰 2. 예상 월 순이익 시뮬레이션
                </h4>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='financial-box'>
                    <p style='font-size: 1.1em; font-weight: 600; color: #1f2937;'>
                        선택 업종 (1위: {MOCK_ANALYSIS_RESULTS[0]['name']}) 기준 예측
                    </p>
                    <div style="font-size: 2em; font-weight: 900; color: #10b981; margin-top: 0.5rem;">
                        {lower:,}원 ~ {upper:,}원
                    </div>
                    <p style='color: #6b7280; font-size: 0.8em; margin-top: 0.5rem;'>
                        (입력: 자본금 {initial_capital/10000:,}만원, 월 임대료 {monthly_rent/10000:,}만원, 면적 {area_pyeong}평)
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.success("종합 분석이 완료되었습니다. 자세한 재무 분석 리포트는 정식 출시 후 프리미엄 서비스에서 확인 가능합니다.")
            st.balloons() # 시연 효과

# --------------------
# 6. 사전 신청 섹션
# --------------------

st.markdown("---")
st.markdown("<h2 style='text-align: center; font-weight: 800; color: #3b82f6;'>✨ 지금 바로 R-메트릭스 소식을 받아보세요!</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>정식 출시 알림 신청자에게는 **첫 달 프리미엄 리포트 50% 할인 쿠폰**을 드립니다.</p>", unsafe_allow_html=True)

# 모바일에서도 입력창이 좁아지지 않도록 컬럼 비율 유지 (3:1)
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
# 7. 푸터
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
