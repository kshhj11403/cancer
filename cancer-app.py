import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import time
import random
import os

# ---------------- 기본 설정 ----------------
st.set_page_config(
    page_title="막장 건강검진 결과 사전 분석 서비스",
    page_icon="🏥",
    layout="centered"
)

# ---------------- 온라인에서 나눔고딕 폰트 실시간 다운로드 ----------------
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

# ---------------- 세션 상태 초기화 ----------------
if 'app_step' not in st.session_state: st.session_state.app_step = 0
if 'captcha_attempts' not in st.session_state: st.session_state.captcha_attempts = 0
if 'generated_code' not in st.session_state: st.session_state.generated_code = str(random.randint(100000, 999999))
if 'captcha_time' not in st.session_state: st.session_state.captcha_time = time.time()
if 'smokes_score' not in st.session_state: st.session_state.smokes_score = 0.0
if 'alcohol_score' not in st.session_state: st.session_state.alcohol_score = 0.0
if 'scratched' not in st.session_state: st.session_state.scratched = False

# ---------------- 데이터 로드 ----------------
try:
    # 꼼수 방지용 가짜 더미 모델/데이터 자동 생성 (파일 없을 때 에러 방지)
    if not os.path.exists('cancer.csv'):
        df_dummy = pd.DataFrame({'Age': [30,40,50,60], 'Smoking': [1,5,10,20], 'Alcohol': [0,2,5,8]})
        df_dummy.to_csv('cancer.csv', index=False)
    
    class DummyModel:
        def predict(self, X): return [random.randint(0, 3) for _ in range(len(X))]
        @property
        def n_clusters(self): return 4
        @property
        def cluster_centers_(self): return [[35, 3, 2], [45, 12, 5], [52, 6, 4], [61, 22, 7]]
        
    class DummyScaler:
        def transform(self, X): return X
        def inverse_transform(self, X): return X

    model = joblib.load('cancer_model.pkl') if os.path.exists('cancer_model.pkl') else DummyModel()
    scaler = joblib.load('cancer_scaler.pkl') if os.path.exists('cancer_scaler.pkl') else DummyScaler()
    df_original = pd.read_csv('cancer.csv')

    numeric_cols = [col for col in df_original.columns if pd.to_numeric(df_original[col], errors='coerce').notnull().all()]
    df_original.rename(columns={numeric_cols[0]: '나이', numeric_cols[1]: '흡연여부', numeric_cols[2]: '음주여부'}, inplace=True)
except Exception as e:
    st.error(f"서비스 초기화 중 문제가 발생했습니다: {e}")
    st.stop()

# ---------------- 공통 사이드바 ----------------
with st.sidebar:
    st.caption("서비스 상태")
    st.error("⚠️ 서버 과열 (디스크 스왑 가동 중)")
    st.caption("현재 예상 대기시간")
    st.write(f"⏳ {random.randint(180, 420)}분")
    st.divider()
    if st.button("처음으로 (데이터 날아가서 후회함)", type="primary"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# ---------------- 화면 0: 분석 시작 ----------------
if st.session_state.app_step == 0:
    st.title("🏥 건강검진 결과 사전 분석 서비스")
    st.caption("본 서비스는 검진 데이터를 기반으로 통계적 위험도를 분석하는 참고용 서비스입니다.")
    
    confirm = st.checkbox("동의하지 않을 시 분석 프로세스 진입이 불가함을 서약합니다.")
    st.write("")
    if st.button("분석 시작", type="secondary"):
        if confirm:
            st.session_state.app_step = 1
            st.rerun()
        else:
            st.warning("🚨 위의 서약 체크박스를 체크하지 않으면 시작 버튼이 작동하지 않는 고도의 보안 조치입니다.")
    st.stop()

# ---------------- 화면 1: 약관 동의 (억까 모멘트 1, 2) ----------------
if st.session_state.app_step == 1:
    st.title("서비스 이용 동의")
    
    agree1 = st.checkbox("[필수] 개인정보 수집 및 이용 동의")
    agree2 = st.checkbox("[필수] 민감정보 처리 동의")
    agree3 = st.checkbox("[필수] 서비스 이용약관 동의")
    # 📌 억까 1: 선택인 척하는 필수 마케팅 동의
    agree4 = st.checkbox("[선택] 야간 마케팅 및 맞춤형 보험 상품 유선 권고 연락 동의")

    # 📌 억까 2: 억지 스크롤 확인용 꼼수 슬라이더
    st.text_area("약관 전문", value="제1조... 약관을 끝까지 읽으셔야 합니다. 하단의 '스크롤 매칭 인증기'를 100%로 맞추십시오.", height=120, disabled=True)
    scroll_emulation = st.slider("📜 약관 스크롤 매칭 인증기 (맨 아래로 스크롤하듯 100까지 당기세요)", 0, 100, 0)

    if st.button("다음"):
        if not (agree1 and agree2 and agree3):
            st.error("필수 약관에 동의해주세요.")
        elif scroll_emulation < 100:
            st.error("🚨 시스템이 약관 정독을 감지하지 못했습니다. 스크롤 인증기를 100%로 완전히 밀어주십시오.")
        elif not agree4:
            # 선택 사항이라 해놓고 강제하기
            st.error("🚨 [보안 경고] [선택] 항목을 동의하지 않을 경우, 공공 망 데이터 커넥션 인출이 제한됩니다. 그냥 동의하십시오.")
        else:
            with st.spinner("약관 무결성 검증 중..."): time.sleep(1.2)
            st.session_state.app_step = 2
            st.session_state.captcha_time = time.time() # 타이머 리셋
            st.rerun()
    st.stop()

# ---------------- 화면 2: 자동 입력 방지 (억까 모멘트 3: 타임아웃 폭탄) ----------------
if st.session_state.app_step == 2:
    st.title("본인 확인 및 자동입력방지")
    
    # 📌 억까 3: 실시간 제한 시간 카운트다운 (화면 갱신될 때마다 줄어듦)
    elapsed = int(time.time() - st.session_state.captcha_time)
    time_left = max(0, 10 - elapsed)
    
    if time_left <= 0:
        st.error("⏰ [타임아웃] 입력 제한 시간(10초)이 초과되어 보안 코드가 폭파되었습니다! 번호가 재발급됩니다.")
        st.session_state.generated_code = str(random.randint(100000, 999999))
        st.session_state.captcha_time = time.time()
        time.sleep(1.5)
        st.rerun()

    st.warning(f"🚨 보안 패킷 보호를 위해 {time_left}초 내에 입력 후 [인증 확인]을 눌러야 합니다!")
    st.code(st.session_state.generated_code, language="text")
    code = st.text_input("번호 입력 (마음이 급해진다...)", max_chars=6)

    if st.button("인증 확인"):
        st.session_state.captcha_attempts += 1
        if st.session_state.captcha_attempts == 1:
            st.error("❌ [1차 시도 패배] 첫 번째 인증 세션은 원래 만료되도록 설계되어 있습니다. 재발급된 코드로 다시 시도하십시오.")
            st.session_state.generated_code = str(random.randint(100000, 999999))
            st.session_state.captcha_time = time.time() # 시간 초기화
            st.rerun()
        elif code != st.session_state.generated_code:
            st.error("번호가 일치하지 않습니다! 타이머는 멈추지 않습니다.")
        else:
            st.success("🎉 억까를 뚫고 본인 확인 성공!")
            time.sleep(1.0)
            st.session_state.app_step = 3
            st.rerun()
            
    # 트릭: 유저가 멍하니 있을 때 실시간 카운트다운을 시각적으로 유도하기 위한 리프레시 버튼
    if st.button("⏱️ 남은 시간 동기화 새로고침"): st.rerun()
    st.stop()

# ---------------- 화면 3: 검진 정보 입력 (억까 모멘트 4, 5, 6) ----------------
if st.session_state.app_step == 3:
    st.title("검진 정보 입력 및 미니게임")
    
    # 📌 억까 4: 마우스 올리면 요동치는 연령 설정 (여기서는 슬라이더 값 무작위 난수 섞기로 구현)
    st.subheader("1. 연령 입력")
    st.caption("※ 보안 매크로 방지를 위해 입력축이 가변적입니다.")
    age_seed = st.slider("연령 가변 컨트롤러 (정밀하게 조절해보세요)", 1, 100, 40)
    # 조절할 때마다 40% 확률로 오차 발생
    input_age = age_seed + random.choice([-3, 0, 2]) if random.random() < 0.4 else age_seed
    st.info(f"🎯 보정된 현재 인식 연령: 만 {input_age}세")

    st.divider()

    # 📌 억까 5: 클릭 노가다 미니게임형 음주/흡연 지표 입력
    st.subheader("2. 생활 습관 지표 게이지 빌딩")
    st.caption("직접 입력은 차단되었습니다. 증량 버튼을 눌러 본인의 지표를 달성하십시오.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("현재 흡연 지표", f"{st.session_state.smokes_score:.1f}")
        if st.button("🚬 흡연 지표 +1.5 올리기"):
            if random.random() < 0.15:
                st.error("💥 금연 패치가 작동하여 지표가 초기화되었습니다! (-3.0)")
                st.session_state.smokes_score = max(0.0, st.session_state.smokes_score - 3.0)
            else:
                st.session_state.smokes_score += 1.5
            st.rerun()
            
    with c2:
        st.metric("현재 음주 지표", f"{st.session_state.alcohol_score:.1f}")
        if st.button("🍺 음주 지표 +1.0 올리기"):
            if random.random() < 0.20:
                st.warning("🤮 과음으로 인해 맥주잔을 엎질렀습니다! 지표 대폭 하락 (-4.0)")
                st.session_state.alcohol_score = max(0.0, st.session_state.alcohol_score - 4.0)
            else:
                st.session_state.alcohol_score += 1.0
            st.rerun()

    if st.button("♻️ 지표 영점으로 초기화"):
        st.session_state.smokes_score = 0.0
        st.session_state.alcohol_score = 0.0
        st.rerun()

    # 움직이는 버튼 CSS 애니메이션 유지
    st.markdown("""
    <style>
    @keyframes flyAroundTargeted {
      0% { transform: translate(0px, 0px); }
      25% { transform: translate(140px, -25px); }
      50% { transform: translate(-100px, 45px); }
      75% { transform: translate(120px, 25px); }
      100% { transform: translate(0px, 0px); }
    }
    div.element-container button[kind="secondary"] {
      animation: flyAroundTargeted 1.1s infinite alternate ease-in-out;
      position: relative; z-index: 999; cursor: cell;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("분석 요청", type="secondary"):
        # 📌 억까 6: 뜬금없는 블루스크린 스캠 경고창 후 초기화
        if random.random() < 0.15:
            st.code("""
            A problem has been detected and Windows has been shut down to prevent damage
            to your health_matrix_system.
            
            UNEXPECTED_KERNEL_SPOOFING_ERROR
            
            Technical Information:
            *** STOP: 0x000000D1 (0x0000000C, 0x00000002, 0x00000000, 0xF73120AE)
            """, language="text")
            st.error("🚨 치명적인 세션 크래시가 발생했습니다. 보안을 위해 0단계로 긴급 사출합니다.")
            time.sleep(3.5)
            st.session_state.app_step = 0
            st.rerun()
            
        st.session_state.input_age = input_age
        st.session_state.input_smokes = st.session_state.smokes_score
        st.session_state.input_alcohol = st.session_state.alcohol_score
        st.session_state.app_step = 4
        st.rerun()
    st.stop()

# ---------------- 화면 4: 지옥의 로딩바 + 팝업 대처 미니게임 (억까 모멘트 7) ----------------
if st.session_state.app_step == 4:
    st.title("임상 데이터 초고속 가속 연산 중")
    
    # 📌 억까 7: 로딩 중에 광고/경고창 팝업이 무작위로 뜨고 제한 시간 내 안 닫으면 롤백
    progress = st.progress(0)
    status = st.empty()
    
    dance_timeline = [
        (10, "가중치 매트릭스 변환 중...", 0.5),
        (45, "커널 스택 메모리 로드 중...", 0.5),
        (99, "⚠️ 동기화 홀드: 최종 연산 노드의 서명 패킷 대기 중 (99% 고정)...", 2.0)
    ]
    
    for val, txt, delay in dance_timeline:
        status.text(txt)
        progress.progress(val)
        time.sleep(delay)
        
    # 중간 방해 미니 팝업 등장 구현
    st.error("📢 [중간 광고 및 보안 경고] 서버 유지 비용 후원을 위해 아래의 '로봇이 아닙니다' 승인 버튼을 3초 내로 누르십시오!")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        click_pass = st.button("🤖 네, 저는 로봇이 절대 아닙니다.")
    with col_btn2:
        st.button("🤖 저는 사실 터미네이터입니다.")
        
    time.sleep(2.5) # 누를 시간 주기
    
    if not click_pass:
        st.error("❌ 반응 속도 지연! 보안관이 패킷을 거부하여 알고리즘이 대폭 탈탈 털렸습니다. 패널티 롤백!")
        progress.progress(15)
        status.text("🚨 데이터 세그먼트 손실 복구 및 메모리 가비지 컬렉션 가동 중 (-84%)...")
        time.sleep(2.0)
        
    status.text("✅ 우회 프로토콜 적용하여 최종 레포트 인덱스를 복구했습니다.")
    progress.progress(100)
    time.sleep(1.0)
    
    st.session_state.app_step = 5
    st.rerun()

# ---------------- 화면 5: 결과 및 모자이크 스크래치 (억까 모멘트 8) ----------------
if st.session_state.app_step == 5:
    st.title("종합 분석 결과 보고서")
    
    # 📌 억까 8: 결과 가려놓고 마우스 복권 긁기 미니게임 시키기
    if not st.session_state.scratched:
        st.subheader("🔒 결과지가 봉인되어 있습니다.")
        st.warning("아래의 '보안 스크래치 실체화' 슬라이더를 77% 혹은 100%로 정확히 밀어서 모자이크를 벗겨내십시오.")
        scratch_card = st.slider("▒▒▒ 모자이크 스크래치 액션 ▒▒▒", 0, 100, 0)
        
        if scratch_card == 77 or scratch_card == 100:
            st.success("🔓 봉인 해제 성공! 데이터가 가독화되었습니다.")
            if st.button("결과 확인하기"):
                st.session_state.scratched = True
                st.rerun()
        else:
            st.caption("💡 힌트: 복권은 77% 혹은 100%의 행운에서 긁힙니다.")
            st.stop()

    # 결과 표출 본문
    input_age = st.session_state.input_age
    input_smokes = st.session_state.input_smokes
    input_alcohol = st.session_state.input_alcohol

    new_patient = pd.DataFrame([{'나이': float(input_age), '흡연여부': float(input_smokes), '음주여부': float(input_alcohol)}])
    new_patient_scaled = scaler.transform(new_patient)
    pred_cluster = model.predict(new_patient_scaled)

    cluster_interpretations = {
        0: '매우 건강군 (통계적 안심 구역)',
        1: '주의군 (위험 인자 축적 중)',
        2: '중간 그룹 (주의 요망 상태)',
        3: '🚨 강력한 폐암 위험군 (즉시 정밀 검사 권고)'
    }

    st.write(f"의료 분석 결과 귀하는 통계학적으로 **{pred_cluster[0]}번 군집**에 배정되었습니다.")
    st.info(f"군집 임상적 소견: \'{cluster_interpretations.get(pred_cluster[0], '분류 불가 인덱스')}\'")

    # 시각화 그래프 출력
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df_original['나이'], df_original['음주여부'], c='gray', alpha=0.3, label='기존 대조 데이터')
    ax.scatter(input_age, input_alcohol, c='red', s=400, marker='*', label='당신의 위치 (★)')
    
    if 'font_prop' in locals():
        ax.set_xlabel("나이", fontproperties=font_prop)
        ax.set_ylabel("음주 지표", fontproperties=font_prop)
        ax.set_title("군집 내 나의 상대적 위치", fontproperties=font_prop)
        legend = ax.legend()
        for text in legend.get_texts(): text.set_fontproperties(font_prop)
    
    st.pyplot(fig)

    if st.button("🔄 처음 단계로 돌아가서 다시 고통받기"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
