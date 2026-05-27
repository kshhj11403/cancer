import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import time
import random
import os

# ---------------- --- 1. 티니핑 마법 페이지 설정 --- ----------------
st.set_page_config(
    page_title="캐치! 티니핑 마법 건강 진단",
    page_icon="🏥",
    layout="centered"
)

# [초필살기] 나눔고딕 폰트를 온라인에서 강제로 다운로드하여 Matplotlib에 주입!
@st.cache_data
def load_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    return font_path

try:
    font_path = load_font()
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except Exception as e:
    plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'sans-serif']

plt.rcParams['axes.unicode_minus'] = False

# --- 2. 웹페이지 전체에 귀여운 폰트 및 스타일 적용 (CSS 마법) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gamja+Flower&family=Nanum+Gothic+Coding&display=swap');
    
    html, body, [data-testid="stWidgetLabel"], .stMarkdown p {
        font-family: 'Gamja Flower', 'Malgun Gothic', sans-serif !important;
        font-size: 1.15rem !important;
    }
    h1, h2, h3 {
        font-family: 'Gamja Flower', 'Malgun Gothic', sans-serif !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- 세션 상태 ----------------
if 'app_step' not in st.session_state:
    st.session_state.app_step = 0

if 'captcha_attempts' not in st.session_state:
    st.session_state.captcha_attempts = 0

if 'generated_code' not in st.session_state:
    st.session_state.generated_code = str(random.randint(100000, 999999))

# ---------------- 데이터 로드 ----------------
try:
    model = joblib.load('cancer_model.pkl')
    scaler = joblib.load('cancer_scaler.pkl')
    df_original = pd.read_csv('cancer.csv')

    numeric_cols = []
    for col in df_original.columns:
        try:
            pd.to_numeric(df_original[col])
            numeric_cols.append(col)
        except:
            pass

    df_original.rename(columns={
        numeric_cols[0]: '나이',
        numeric_cols[1]: '흡연여부',
        numeric_cols[2]: '음주여부'
    }, inplace=True)

except:
    st.error("서비스 초기화 중 문제가 발생했습니다.")
    st.caption("잠시 후 다시 접속해주세요. (cancer_model.pkl, cancer_scaler.pkl, cancer.csv 파일 확인)")
    st.stop()

# --- 이미지 에셋 로드 (티니핑 이미지) ---
teenieping_logo = "https://shopby-images.cdn-nhncommerce.com/20251210/193406.74593594/%EC%BA%90%EC%B9%98%ED%8B%B0%EB%8B%88%ED%95%91.png"
hachuping_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0yx11nxnIhf6fFOJHWlXaUsJZA0YqVEXzcA&s"
joaping_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeQj23ZRAGlZtuCcTMShhj1k8KeUvSLUy8VQ&s"
banglping_img = "https://cimg.cowave.kr/image/vendor_inventory/8590/4fe3c32147424c16a4d8dd8b5de5529afe5168d35115abfffaeadc6bf453.jpg"

# ---------------- 공통 사이드바 ----------------
with st.sidebar:
    st.caption("서비스 상태핑")
    st.success("정상 운영 중")

    st.caption("현재 예상 대기시간")
    st.write(f"{random.randint(3, 18)}분")

    st.caption("권장 환경")
    st.write("Chrome 120 이상")

    st.divider()

    if st.button("처음으로핑", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ---------------- 화면 0: 분석 시작 ----------------
if st.session_state.app_step == 0:
    st.markdown(
        f"""
        <div style='text-align: center; background-color: #fff0f5; padding: 25px; border-radius: 20px; border: 3px solid #ffb6c1; box-shadow: 0 4px 15px rgba(255,182,193,0.5);'>
            <img src='{teenieping_logo}' width='280'><br>
            <h1 style='color: #ff1493; margin-top: 15px; font-size: 2.5rem;'> 반짝반짝! 나의 건강 핑 찾기 </h1>
            <p style='color: #ff69b4; font-size: 1.4rem; font-weight: bold;'>마법의 비밀 포지션을 찾아줄 거야핑! ٩(ˊᗜˋ*)و</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("""
    본 서비스는 검진 데이터를 기반으로 통계적 위험도를 분석하는 참고용 서비스입니다핑.
    實際 진단 결과와 차이가 발생할 수 있습니다.
    """)

    st.info("현재 접속량 증가로 인해 일부 사용자의 분석 요청이 지연될 수 있습니다핑.")
    st.checkbox("안내사항을 확인했습니다핑.")

    if st.button("분석 시작하기핑", type="secondary"):
        st.session_state.app_step = 1
        st.rerun()

    st.stop()

# ---------------- 화면 1: 약관 동의 ----------------
if st.session_state.app_step == 1:
    st.title("서비스 이용 동의핑")

    agree1 = st.checkbox("[필수] 개인정보 수집 및 이용 동의핑")
    agree2 = st.checkbox("[필수] 민감정보 처리 동의핑")
    agree3 = st.checkbox("[필수] 서비스 이용약관 동의핑")
    agree4 = st.checkbox("[선택] 맞춤형 건강정보 수신 동의핑")

    scroll_check = st.checkbox("약관 내용을 모두 확인했습니다핑.")

    if st.button("다음핑", disabled=not (agree1 and agree2 and agree3 and scroll_check)):
        with st.spinner("마법 약관 확인 중..."):
            time.sleep(1.2)
        st.session_state.app_step = 2
        st.rerun()

    st.stop()

# ---------------- 화면 2: 자동 입력 방지 (억까 캡차) ----------------
if st.session_state.app_step == 2:
    st.title("본인 확인 및 자동입력방지핑")
    st.caption("안전한 데이터 보호를 위해 화면에 유효화된 6자리 번호를 기입하십시오핑.")

    st.code(st.session_state.generated_code)
    code = st.text_input("번호 입력핑", max_chars=6)

    if st.button("인증 확인핑"):
        st.session_state.captcha_attempts += 1

        if st.session_state.captcha_attempts == 1:
            st.error("인증 세션이 만료되었습니다핑! 실시간 재할당된 하단의 코드로 재입력해 주십시오핑.")
            st.session_state.generated_code = str(random.randint(100000, 999999))
            st.rerun()
        elif code != st.session_state.generated_code:
            st.error("번호가 일치하지 않습니다핑!")
        else:
            with st.spinner("보안 토큰 검증 중핑..."):
                time.sleep(1.0)
            st.success("본인 확인이 완료되었습니다핑!")
            st.session_state.app_step = 3
            st.rerun()

    st.stop()

# ---------------- 화면 3: 검진 정보 입력 (춤추는 버튼 무빙) ----------------
if st.session_state.app_step == 3:
    st.title("마법의 라이프 지표 입력핑")

    input_age = st.slider("내 나이핑 (세)", min_value=10, max_value=100, value=25)
    input_smokes = st.slider("주당 흡연 횟수핑 (번)", min_value=0.0, max_value=50.0, value=5.0, step=0.5)
    input_alcohol = st.slider("주당 음주 횟수핑 (번)", min_value=0.0, max_value=10.0, value=2.0, step=0.5)

    # 춤추는 CSS 타겟팅 인젝션
    st.markdown("""
    <style>
    @keyframes flyAroundTargeted {
      0% { transform: translate(0px, 0px); }
      20% { transform: translate(150px, -30px); }
      40% { transform: translate(-100px, 45px); }
      60% { transform: translate(130px, 60px); }
      80% { transform: translate(-120px, -20px); }
      100% { transform: translate(0px, 0px); }
    }
    div.element-container button[kind="secondary"] {
      animation: flyAroundTargeted 1.2s infinite alternate ease-in-out;
      position: relative;
      z-index: 999;
      cursor: crosshair;
    }
    </style>
    """, unsafe_allow_html=True)

    st.caption("※ 매크로 방지를 위해 마법 가변 좌표 인코딩이 적용되어 있습니다핑! 움직이는 버튼을 정밀 조작하십시오핑.")

    if st.button("마법 분석 요청핑", type="secondary"):
        if random.random() < 0.12:
            st.error("세션 전송 오버플로우 발생! 처음 단계로 회귀합니다핑...")
            time.sleep(1.5)
            st.session_state.app_step = 0
            st.rerun()

        st.session_state.input_age = input_age
        st.session_state.input_smokes = input_smokes
        st.session_state.input_alcohol = input_alcohol
        st.session_state.app_step = 4
        st.rerun()

    st.stop()

# ---------------- 화면 4: 지옥의 티니핑 로딩바 ----------------
if st.session_state.app_step == 4:
    st.title("임상 데이터 마법 연산 중핑")
    progress = st.progress(0)
    status = st.empty()

    dance_timeline = [
        (5, "입력 프로파일 가중치 변환 중핑...", 0.5),
        (25, "메인 클러스터 커널 스택 메모리 로드 중핑...", 0.5),
        (55, "다차원 벡터 공간 내 유클리드 거리 지표 연산 중핑...", 0.6),
        (75, "통계학적 신뢰 구간 필터 레이어 교차 검증 중핑...", 0.6),
        (99, "⚠️ 동기화 홀드: 최종 연산 노드의 서명 패킷 대기 중 (99%)...", 2.0), 
        (40, "🚨 패킷 거부: 연산 노드 거절 반응 발생! 알고리즘 롤백 조치 (-59%핑)...", 1.5),
        (65, "커널 분석 가중치 레이어 초고속 재연산 진행 중핑...", 0.4),
        (100, "✅ 연산 성공! 최종 레포트를 인출했습니다핑!", 0.5)
    ]

    for val, txt, delay in dance_timeline:
        status.text(txt)
        progress.progress(val)
        time.sleep(delay)

    st.session_state.app_step = 5
    st.rerun()

# ---------------- 화면 5: 결과 및 한글 완벽 차트 ----------------
if st.session_state.app_step == 5:
    input_age = st.session_state.input_age
    input_smokes = st.session_state.input_smokes
    input_alcohol = st.session_state.input_alcohol

    new_patient = pd.DataFrame([{
        '나이': float(input_age),
        '흡연여부': float(input_smokes),
        '음주여부': float(input_alcohol)
    }])

    new_patient_scaled = scaler.transform(new_patient)
    pred_cluster = model.predict(new_patient_scaled)

    st.title("💖 마법의 AI 종합 분석 결과 보고서핑")

    # 결과 매칭 및 이미지 분기
    if pred_cluster[0] == 0:
        cluster_desc = "참 잘했어요핑! 하츄핑이 사랑해핑! 건강한 '사랑핑' 군집이다핑!"
        alert_style = "background-color: #f0fff0; border: 3px solid #32cd32; color: #008000;"
        ping_img = hachuping_img
    elif pred_cluster[0] in [1, 2]:
        cluster_desc = "토닥토닥.. 조아핑이 응원해핑! 관리가 필요한 '조아핑' 군집이다핑!"
        alert_style = "background-color: #fffff0; border: 3px solid #ffd700; color: #daa520;"
        ping_img = joaping_img
    else:
        cluster_desc = "삐뽀삐뽀! 방글핑이 경고해핑! 조심해야 할 '위험핑' 군집이다핑!"
        alert_style = "background-color: #ffe4e1; border: 3px solid #ff4500; color: #ff0000;"
        ping_img = banglping_img

    st.markdown(
        f"""
        <div style='{alert_style} padding: 20px; border-radius: 20px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: flex; align-items: center;'>
            <img src='{ping_img}' width='150' style='border-radius: 20px; margin-right: 20px; border: 3px solid white; object-fit: cover; height: 130px;'>
            <div>
                <span style='font-size: 1.4rem; color:#333;'>🏥 {input_age}세 피험자 분석 결과:</span><br><br>
                <span style='font-size: 1.3rem; line-height: 1.5;'>귀하는 현재 통계학적으로 <b>[{pred_cluster[0]}번 군집]</b>에 배정되었으며,<br>
                <span style='font-size: 1.4rem; text-decoration: underline;'>{cluster_desc}</span></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 맷플롯립 시각화 인프라 구축
    X_original = df_original[['나이', '흡연여부', '음주여부']]
    X_scaled_original = scaler.transform(X_original)
    df_original['cluster'] = model.predict(X_scaled_original)

    colors = ['#ff69b4', '#ffd700', '#32cd32', '#ff4500']
    df_original['c'] = df_original['cluster'].map({i: colors[i % 4] for i in range(4)})

    st.write("")
    st.markdown("<h3 style='color: #ff1493; text-align: center;'>💖 환자 군집 내 실시간 포지셔닝핑</h3>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#fffafa')

    # 기존 데이터 산점도
    ax.scatter(
        df_original['음주여부'],
        df_original['흡연여부'],
        c=df_original['c'],
        alpha=0.4,
        s=40,
        label='기존 환자 마법 데이터셋'
    )

    # 유저 위치 별(Star) 마커 주입
    ax.scatter(
        input_alcohol,
        input_smokes,
        c='#ff1493',
        s=400,
        marker='*',
        label='나의 위치핑! (★)',
        edgecolor='#ffffff',
        linewidth=2,
        zorder=10
    )

    # [✨ 해결 포인트] 가져온 폰트 정보를 축과 레이블에 강제 인젝션하여 한글 출력 보장
    ax.set_xlabel('주당 음주 횟수핑 (번)', color='#ff1493', fontsize=11, fontweight='bold', fontproperties=font_prop)
    ax.set_ylabel('주당 흡연 횟수핑 (번)', color='#ff1493', fontsize=11, fontweight='bold', fontproperties=font_prop)
    ax.set_title('다차원 티니핑 군집 매핑 데이터', color='#ff1493', fontsize=13, fontweight='bold', fontproperties=font_prop)

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(font_prop)
        label.set_color('#ff69b4')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#ffb6c1')
    ax.spines['bottom'].set_color('#ffb6c1')
    ax.grid(True, color='#ffe4e1', linestyle='--', alpha=0.6)

    legend = ax.legend(loc='upper right')
    for text in legend.get_texts():
        text.set_fontproperties(font_prop)
        text.set_color('#ff1493')

    st.pyplot(fig, use_container_width=True)

    # 데이터 프레임 출력
    st.write("**알고리즘 참조용 군집 중심값 Matrix**")
    centers_df = pd.DataFrame(
        scaler.inverse_transform(model.cluster_centers_),
        columns=['나이핑', '흡연지표핑', '음주지표핑'],
        index=[f'티니핑 군집 {i}' for i in range(model.n_clusters)]
    )
    st.write(centers_df)

    if st.button("신규 피험자 데이터 재분석 요청핑"):
        st.session_state.app_step = 3
        st.rerun()

    st.stop()
