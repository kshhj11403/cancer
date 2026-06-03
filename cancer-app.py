import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import time
import random
import os

# ---------------- 기본 설정 (표면상 아주 진중하게 변경) ----------------
st.set_page_config(
    page_title="AI 기반 종합 건강검진 결과 사전 분석 시스템",
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
    # 파일이 없는 환경을 위한 자동 백업용 더미 객체 정의 (Sklearn 에러 방지용)
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

    # 파일이 정상적으로 존재할 때만 로드 시도
    model = joblib.load('cancer_model.pkl') if os.path.exists('cancer_model.pkl') else DummyModel()
    scaler = joblib.load('cancer_scaler.pkl') if os.path.exists('cancer_scaler.pkl') else DummyScaler()
    df_original = pd.read_csv('cancer.csv')

    numeric_cols = [col for col in df_original.columns if pd.to_numeric(df_original[col], errors='coerce').notnull().all()]
    df_original.rename(columns={numeric_cols[0]: '나이', numeric_cols[1]: '흡연여부', numeric_cols[2]: '음주여부'}, inplace=True)
except Exception as e:
    st.error(f"정밀 분석 인프라 연동 중 예외가 발생했습니다: {e}")
    st.caption("의존성 패키지(scikit-learn 등) 설치 여부를 확인하십시오.")
    st.stop()

# ---------------- 공통 사이드바 (정상적인 척 압박하기) ----------------
with st.sidebar:
    st.caption("데이터 노드 상태")
    st.error("⚠️ 트래픽 과부하 (인접 세션 대기열 가동 중)")
    st.caption("현재 분석 예상 소요시간")
    st.write(f"⏳ 약 {random.randint(45, 120)}분 대기 필요")
    st.divider()
    if st.button("처음으로 이동 (입력 데이터는 즉시 유실됨)", type="primary"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# ---------------- 화면 0: 분석 시작 ----------------
if st.session_state.app_step == 0:
    st.title("🏥 AI 기반 종합 건강검진 결과 사전 분석 시스템")
    st.subheader("임상 통계 예측 모델 고도화 솔루션 v2.4")
    st.caption("본 정보 시스템은 검진 데이터를 고차원 클러스터링 알고리즘으로 분석하는 보건 예방 참고용 서비스입니다.")
    
    confirm = st.checkbox("데이터 분석 목적의 위탁 및 오차 가능성에 대해 명확히 인지하고 동의합니다.")
    st.write("")
    if st.button("종합 분석 프로세스 진입", type="secondary"):
        if confirm:
            st.session_state.app_step = 1
            st.rerun()
        else:
            st.warning("🚨 안전한 데이터 처리를 위해 상단의 인지 서약 체크박스를 체크하셔야 알고리즘이 가동됩니다.")
    st.stop()

# ---------------- 화면 1: 약관 동의 (억까 모멘트 1, 2) ----------------
if st.session_state.app_step == 1:
    st.title("의료 데이터 처리 및 서비스 이용 동의")
    
    agree1 = st.checkbox("[필수] 개인정보 수집 및 이용 동의")
    agree2 = st.checkbox("[필수] 고유식별정보 및 민감정보 처리 동의")
    agree3 = st.checkbox("[필수] 분석 인프라 이용약관 동의")
    # 📌 억까 1: 선택 항목인 것처럼 유저를 기만하는 필수 마케팅 동의
    agree4 = st.checkbox("[선택] 맞춤형 정밀 건강관리 가이드 및 제휴 보험 상품 안내 동의")

    st.text_area("보안 및 이용약관 전문", value="제1조(목적) 본 시스템은 유클리드 거리를 기반으로 한 통계 분석 모델을 적용합니다. 약관을 완전히 정독해야 하므로 하단의 정독 동의 슬라이더를 100%로 설정하십시오.", height=120, disabled=True)
    
    # 📌 억까 2: 스크롤 대신 슬라이더 정독 요구
    scroll_emulation = st.slider("📜 시스템 약관 정독 인증 (가장 우측인 100까지 정밀하게 드래그하십시오)", 0, 100, 0)

    if st.button("동의 후 다음 단계 진입"):
        if not (agree1 and agree2 and agree3):
            st.error("필수 항목에 대해 모두 동의 절차를 밟아주십시오.")
        elif scroll_emulation < 100:
            st.error("🚨 [비정상 접근 감지] 시스템이 약관 정독을 신뢰하지 못했습니다. 정독 인증 바를 100% 위치에 정확히 매칭하십시오.")
        elif not agree4:
            # 선택 사항이라 써놓고 뒤통수 치기
            st.error("🚨 [데이터 무결성 오류] [선택] 항목 미동의 시 공공 의료 보건 데이터 커넥션 개방이 거부됩니다. 약관에 동의하십시오.")
        else:
            with st.spinner("암호화 토큰 무결성 검증 중..."): time.sleep(1.2)
            st.session_state.app_step = 2
            st.session_state.captcha_time = time.time()
            st.rerun()
    st.stop()

# ---------------- 화면 2: 자동 입력 방지 (억까 모멘트 3: 시한폭탄 타이머) ----------------
if st.session_state.app_step == 2:
    st.title("네트워크 보안 및 자동 입력 방지")
    
    # 📌 억까 3: 10초 타임아웃 압박
    elapsed = int(time.time() - st.session_state.captcha_time)
    time_left = max(0, 10 - elapsed)
    
    if time_left <= 0:
        st.error("⏰ [세션 만료] 보안 패킷 타임아웃(10초)이 초과되어 암호화 코드가 자동 파기되었습니다. 새 코드가 할당됩니다.")
        st.session_state.generated_code = str(random.randint(100000, 999999))
        st.session_state.captcha_time = time.time()
        time.sleep(1.5)
        st.rerun()

    st.warning(f"🚨 디도스 매크로 방지를 위해 반드시 {time_left}초 이내에 보안 코드를 판독 및 입력해야 합니다.")
    st.code(st.session_state.generated_code, language="text")
    code = st.text_input("보안 코드 6자리 입력", max_chars=6)

    if st.button("보안인증 확인"):
        st.session_state.captcha_attempts += 1
        if st.session_state.captcha_attempts == 1:
            # 무조건 1회 실패 유도
            st.error("❌ [통신 동기화 재시도] 첫 번째 인증 세션은 보안 협상(Handshake) 규격에 따라 만료 처리됩니다. 갱신된 하단 코드로 즉시 재시도하십시오.")
            st.session_state.generated_code = str(random.randint(100000, 999999))
            st.session_state.captcha_time = time.time()
            st.rerun()
        elif code != st.session_state.generated_code:
            st.error("보안 코드가 일치하지 않습니다. 실시간 타이머는 멈추지 않습니다.")
        else:
            st.success("✅ 패킷 유효성 검증 서버 통과 완료.")
            time.sleep(1.0)
            st.session_state.app_step = 3
            st.rerun()
            
    if st.button("⏱️ 네트워크 클럭 동기화 (남은 시간 새로고침)"): st.rerun()
    st.stop()

# ---------------- 화면 3: 검진 정보 입력 (억까 모멘트 4, 5, 6) ----------------
if st.session_state.app_step == 3:
    st.title("피험자 임상 지표 파라미터 매핑")
    
    # 📌 억까 4: 조작할 때마다 값이 튀는 연령 조정 슬라이더
    st.subheader("1. 연령(Age) 파라미터 설정")
    st.caption("※ 보안 매크로 제어를 위해 난수 가변 인코딩 휠이 적용되어 있습니다.")
    age_seed = st.slider("연령 미세조정 휠 (정교하게 조절하십시오)", 1, 100, 40)
    # 40% 확률로 유저가 설정한 값과 다른 오차값 강제 주입
    input_age = age_seed + random.choice([-3, 0, 2]) if random.random() < 0.4 else age_seed
    st.info(f"🎯 실시간 인덱싱된 보정 연령: 만 {input_age}세")

    st.divider()

    # 📌 억까 5: 광클 유도 지표 빌딩 + 크리티컬 패널티
    st.subheader("2. 가변형 생활 습관 지표 생성")
    st.caption("안전 표준 규격에 따라 키보드 직접 입력은 차단되었습니다. 증량 버튼을 연타하여 목표 수치를 누적하십시오.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("현재 매핑된 흡연 지표", f"{st.session_state.smokes_score:.1f}")
        if st.button("🚬 흡연 지표 가중치 +1.5 축적"):
            if random.random() < 0.15:
                st.error("💥 [시스템 간섭] 니코틴 초기화 필터가 가동되어 지표가 전량 차감되었습니다! (-3.0)")
                st.session_state.smokes_score = max(0.0, st.session_state.smokes_score - 3.0)
            else:
                st.session_state.smokes_score += 1.5
            st.rerun()
            
    with c2:
        st.metric("현재 매핑된 음주 지표", f"{st.session_state.alcohol_score:.1f}")
        if st.button("🍺 음주 지표 가중치 +1.0 축적"):
            if random.random() < 0.20:
                st.warning("🤮 [오버플로우] 알코올 데이터 임계치 초과로 지표가 역류했습니다! (-4.0)")
                st.session_state.alcohol_score = max(0.0, st.session_state.alcohol_score - 4.0)
            else:
                st.session_state.alcohol_score += 1.0
            st.rerun()

    if st.button("데이터 영점(0.0) 초기화 캘리브레이션 실행"):
        st.session_state.smokes_score = 0.0
        st.session_state.alcohol_score = 0.0
        st.rerun()

    # 도망치는 마우스 CSS 애니메이션
    st.markdown("""
    <style>
    @keyframes flyAroundTargeted {
      0% { transform: translate(0px, 0px); }
      25% { transform: translate(130px, -30px); }
      50% { transform: translate(-110px, 40px); }
      75% { transform: translate(110px, 20px); }
      100% { transform: translate(0px, 0px); }
    }
    div.element-container button[kind="secondary"] {
      animation: flyAroundTargeted 1.1s infinite alternate ease-in-out;
      position: relative; z-index: 999; cursor: crosshair;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("분석 요청", type="secondary"):
        # 📌 억까 6: 뜬금없이 나타나는 전문적인 블루스크린 커널 에러
        if random.random() < 0.15:
            st.code("""
            A problem has been detected and Kernel system has been shut down to prevent damage
            to your core_analysis_matrix.
            
            UNEXPECTED_HEALTH_DATA_SPOOFING_ERROR
            
            Technical Information:
            *** STOP: 0x000000D1 (0x0000000C, 0x00000002, 0x00000000, 0xF73120AE)
            """, language="text")
            st.error("🚨 [치명적 커널 에러] 데이터 스트림 오버플로우가 발생하여 보안 프로토콜에 의해 세션이 0단계로 초기 사출됩니다.")
            time.sleep(3.5)
            st.session_state.app_step = 0
            st.rerun()
            
        st.session_state.input_age = input_age
        st.session_state.input_smokes = st.session_state.smokes_score
        st.session_state.input_alcohol = st.session_state.alcohol_score
        st.session_state.app_step = 4
        st.rerun()
    st.stop()

# ---------------- 화면 4: 지옥의 로딩바 + 팝업 대처 (억까 모멘트 7) ----------------
if st.session_state.app_step == 4:
    st.title("고차원 커널 분산 가속 연산 중")
    
    # 📌 억까 7: 게이지가 99% 멈추고 강제로 미니게임 팝업창 띄우기
    progress = st.progress(0)
    status = st.empty()
    
    dance_timeline = [
        (12, "가중치 매트릭스 다차원 변환 중...", 0.5),
        (51, "커널 스택 분산 메모리 로드 중...", 0.5),
        (99, "⚠️ 동기화 대기: 연산 최종 노드의 서명 패킷 검증 대기 중 (99%에서 홀딩)...", 2.0)
    ]
    
    for val, txt, delay in dance_timeline:
        status.text(txt)
        progress.progress(val)
        time.sleep(delay)
        
    st.error("📢 [데이터 무결성 검증] 중앙 연산 장치 점유 비용 확보를 위해 아래의 '비인가 매크로 방지 우회 노드'를 3초 내로 승인하십시오!")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        click_pass = st.button("🤖 본인은 휴먼(Human) 개체임을 최종 승인합니다.")
    with col_btn2:
        st.button("🤖 본인은 지각 능력이 있는 AI 에이전트입니다.")
        
    time.sleep(2.5) 
    
    if not click_pass:
        # 반응 못하면 대폭 롤백 패널티
        st.error("❌ [승인 지연 패널티] 인간 개체 증명 반응 속도 지연으로 연산 코어 패킷이 난도질당했습니다. 롤백을 수행합니다.")
        progress.progress(15)
        status.text("🚨 세그먼트 손실 복구 및 메모리 가비지 컬렉션 재가동 진행 중 (-84%)...")
        time.sleep(2.0)
        
    status.text("✅ 보안 우회 터널링이 가동되어 연산 결과를 정상 복구 및 인출했습니다.")
    progress.progress(100)
    time.sleep(1.0)
    
    st.session_state.app_step = 5
    st.rerun()

# ---------------- 화면 5: 결과 및 모자이크 스크래치 (억까 모멘트 8) ----------------
if st.session_state.app_step == 5:
    st.title("AI 임상 진단 통계 결과 보고서")
    
    # 📌 억까 8: 드디어 끝났는데 결과를 복권 긁듯이 긁어야 오픈해 줌
    if not st.session_state.scratched:
        st.subheader("🔒 데이터 보안 암호화 봉인 해제 필요")
        st.warning("개인정보 보호 표준(ISO 27001)에 의거하여, 아래의 '데이터 시각화 스크래치' 슬라이더를 77% 또는 100%에 정확히 도킹하여 마스킹을 해제하십시오.")
        scratch_card = st.slider("▒▒▒▒ 데이터 마스킹 스크래치 액션 ▒▒▒▒", 0, 100, 0)
        
        if scratch_card in [77, 100]:
            st.success("🔓 암호화 해제 알고리즘 디코딩 완료. 데이터 가독화가 활성화되었습니다.")
            if st.button("최종 리포트 열람 확인"):
                st.session_state.scratched = True
                st.rerun()
        else:
            st.caption("💡 시스템 가이드: 복권 마스킹은 77% 혹은 100%의 주파수에서 정확히 디코딩됩니다.")
            st.stop()

    # 분석 결과 데이터 처리
    input_age = st.session_state.input_age
    input_smokes = st.session_state.input_smokes
    input_alcohol = st.session_state.input_alcohol

    new_patient = pd.DataFrame([{'나이': float(input_age), '흡연여부': float(input_smokes), '음주여부': float(input_alcohol)}])
    new_patient_scaled = scaler.transform(new_patient)
    pred_cluster = model.predict(new_patient_scaled)

    cluster_interpretations = {
        0: '최적 건강군 (통계적 저위험 지대)',
        1: '관리 요망군 (위험 인자 축적 경향성 관찰)',
        2: '중간 위험군 (체계적 식이 관리 필요)',
        3: '🚨 고위험 집중군 (임상 전문의 정밀 검진 권고)'
    }

    st.write(f"의료 데이터 분석 결과 귀하는 통계학적으로 **{pred_cluster[0]}번 군집**에 분류되었습니다.")
    st.info(f"종합 소견 보고: \'{cluster_interpretations.get(pred_cluster[0], '분류 불가 인덱스')}\'")

    # 결과 시각화 차트
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df_original['나이'], df_original['음주여부'], c='gray', alpha=0.3, label='기존 대조 코호트 데이터군')
    ax.scatter(input_age, input_alcohol, c='red', s=400, marker='*', label='현재 피험자 좌표 위치 (★)')
    
    if 'font_prop' in locals():
        ax.set_xlabel("나이", fontproperties=font_prop)
        ax.set_ylabel("음주 임상 지표", fontproperties=font_prop)
        ax.set_title("다차원 코호트 군집 내 피험자 상대 위치 매핑", fontproperties=font_prop)
        legend = ax.legend()
        for text in legend.get_texts(): text.set_fontproperties(font_prop)
    
    st.pyplot(fig)

    if st.button("🔄 새로운 피험자 데이터 분석 요청 (처음으로 돌아가기)"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
