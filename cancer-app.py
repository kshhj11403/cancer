import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import time
import random
import os

# ---------------- 기본 설정 ----------------
st.set_page_config(
    page_title="건강검진 결과 사전 분석 서비스",
    page_icon="🏥",
    layout="centered"
)

# ---------------- [핵심] 저장소에 올린 나눔고딕 폰트 로드 ----------------
font_path = "NanumGothic.ttf"

if os.path.exists(font_path):
    # 깃허브에 올린 폰트 파일이 있으면 그걸 사용
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = font_name
else:
    # 폰트 파일이 없을 때를 대비한 시스템 기본 폰트 백업
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']

plt.rcParams['axes.unicode_minus'] = False

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

# ---------------- 공통 사이드바 (처음으로 버튼 고정) ----------------
with st.sidebar:
    st.caption("서비스 상태")
    st.success("정상 운영 중")

    st.caption("현재 예상 대기시간")
    st.write(f"{random.randint(3, 18)}분")

    st.caption("권장 환경")
    st.write("Chrome 120 이상")

    st.divider()

    if st.button("처음으로", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ---------------- 화면 0: 분석 시작 ----------------
if st.session_state.app_step == 0:
    st.title("🏥 건강검진 결과 사전 분석 서비스")

    st.caption("""
    본 서비스는 검진 데이터를 기반으로 통계적 위험도를 분석하는 참고용 서비스입니다.
    實際 진단 결과와 차이가 발생할 수 있습니다.
    """)

    st.info("""
    현재 접속량 증가로 인해 일부 사용자의 분석 요청이 지연될 수 있습니다.
    """)

    st.checkbox("안내사항을 확인했습니다.")

    st.write("")
    st.write("")

    if st.button("분석 시작", type="secondary"):
        st.session_state.app_step = 1
        st.rerun()

    st.stop()

# ---------------- 화면 1: 약관 동의 ----------------
if st.session_state.app_step == 1:
    st.title("서비스 이용 동의")

    st.caption("""
    원활한 서비스 이용을 위해 아래 항목에 대한 동의가 필요합니다.
    """)

    agree1 = st.checkbox("[필수] 개인정보 수집 및 이용 동의")
    agree2 = st.checkbox("[필수] 민감정보 처리 동의")
    agree3 = st.checkbox("[필수] 서비스 이용약관 동의")
    agree4 = st.checkbox("[선택] 맞춤형 건강정보 및 이벤트 알림 수신 동의")

    st.write("")

    st.text_area(
        "약관 전문",
        value="""
제1조 (목적)
본 서비스는 사용자의 입력 데이터를 기반으로 통계적 분석 결과를 제공합니다.

제2조 (책임 제한)
본 서비스는 참고용 정보만 제공하며 실제 의료행위를 대체하지 않습니다.

제3조 (서비스 제한)
시스템 점검, 트래픽 증가 등의 사유로 서비스 이용이 제한될 수 있습니다.
        """,
        height=220,
        disabled=True
    )

    scroll_check = st.checkbox("약관 내용을 모두 확인했습니다.")

    st.caption("""
    ※ 선택 항목 미동의 시 일부 부가 기능 이용이 제한될 수 있습니다.
    """)

    if st.button(
        "다음",
        disabled=not (agree1 and agree2 and agree3 and scroll_check)
    ):
        with st.spinner("약관 확인 중..."):
            time.sleep(1.8)

        st.session_state.app_step = 2
        st.rerun()

    st.stop()

# ---------------- 화면 2: 자동 입력 방지 (캡차 억까) ----------------
if st.session_state.app_step == 2:
    st.title("본인 확인 및 자동입력방지")

    st.caption("""
    안전한 의료 데이터 자산 보호를 위해 화면에 유효화된 6자리 번호를 기입하십시오.
    """)

    st.code(st.session_state.generated_code)

    code = st.text_input("번호 입력", max_chars=6)

    if st.button("인증 확인"):
        st.session_state.captcha_attempts += 1

        if st.session_state.captcha_attempts == 1:
            st.error("""
            인증 세션이 만료되었습니다. 보안 패킷 전송 규칙에 의거하여 
            실시간 재할당된 하단의 코드로 재입력해 주십시오.
            """)
            st.session_state.generated_code = str(random.randint(100000, 999999))
            st.rerun()

        elif code != st.session_state.generated_code:
            st.error("번호가 일치하지 않습니다. 대소문자 및 오타를 확인하십시오.")
        else:
            with st.spinner("보안 토큰 유효성 검증 중..."):
                time.sleep(1.5)
            st.success("본인 확인이 완료되었습니다.")
            st.session_state.app_step = 3
            st.rerun()

    st.stop()

# ---------------- 화면 3: 검진 정보 입력 (분석 요청 버튼만 무빙) ----------------
if st.session_state.app_step == 3:
    st.title("검진 정보 입력")

    st.caption("""
    아래 항목을 입력한 뒤 분석을 진행해주세요.
    """)

    col1, col2 = st.columns(2)

    with col1:
        input_age = st.number_input(
            "연령",
            min_value=1,
            max_value=100,
            value=30
        )

        input_smokes = st.number_input(
            "흡연 지표",
            min_value=0.0,
            max_value=50.0,
            value=5.0
        )

    with col2:
        input_alcohol = st.number_input(
            "음주 지표",
            min_value=0.0,
            max_value=10.0,
            value=3.0
        )

    st.warning("""
    입력 후 수정사항이 있는 경우 분석 결과가 달라질 수 있습니다.
    """)

    st.markdown("""
    <style>
    @keyframes flyAroundTargeted {
      0% { transform: translate(0px, 0px); }
      20% { transform: translate(180px, -35px); }
      40% { transform: translate(-120px, 55px); }
      60% { transform: translate(160px, 75px); }
      80% { transform: translate(-140px, -25px); }
      100% { transform: translate(0px, 0px); }
    }
    
    div.element-container button[kind="secondary"] {
      animation: flyAroundTargeted 1.4s infinite alternate ease-in-out;
      position: relative;
      z-index: 999;
      cursor: crosshair;
    }
    </style>
    """, unsafe_allow_html=True)

    st.caption("※ 정보 시스템 보안 표준(ISO 27001)에 의거, 매크로 해킹 입력을 방지하기 위해 '동적 가변 좌표 인코딩' 기술이 분석 요청 트리거에 결착되어 있습니다. 궤적을 정밀 추적하여 조작하십시오.")

    st.write("")
    st.write("")

    if st.button("분석 요청", type="secondary"):
        if random.random() < 0.12:
            st.error("""
            세션 전송 오버플로우가 감지되었습니다. 
            보안을 위해 초기 단계로 회귀합니다. 다시 시도하십시오.
            """)
            time.sleep(2.0)
            st.session_state.app_step = 0
            st.rerun()

        st.session_state.input_age = input_age
        st.session_state.input_smokes = input_smokes
        st.session_state.input_alcohol = input_alcohol

        st.session_state.app_step = 4
        st.rerun()

    st.stop()

# ---------------- 화면 4: 춤추는 지옥의 로딩바 ----------------
if st.session_state.app_step == 4:
    st.title("임상 데이터 가속 연산 중")

    progress = st.progress(0)
    status = st.empty()

    dance_timeline = [
        (5, "입력 프로파일 가중치 매트릭스 변환 중...", 0.6),
        (18, "메인 클러스터 커널 스택 메모리 로드 중...", 0.7),
        (35, "알고리즘 대기열 순번 양도 확인 중...", 0.5),
        (55, "다차원 벡터 공간 내 유클리드 거리 지표 연산 중...", 0.8),
        (78, "통계학적 신뢰 구간 필터 레이어 교차 검증 중...", 0.9),
        (92, "분석 진단 종합 리포트 마크다운 구조화 중...", 1.2),
        (99, "⚠️ 동기화 홀드: 최종 연산 노드의 서명 패킷 대기 중 (99%에서 고정)...", 3.5), 
        (40, "🚨 패킷 거부: 연산 노드 거절 반응 발생. 완충을 위해 알고리즘 롤백 조치 수행 (-59%)...", 2.0),
        (15, "🚨 데이터 세그먼트 손실 복구 및 메모리 가비지 컬렉션 가동 중 (-25%)...", 1.8),
        (38, "세션 재연결 성공. 분산 처리 스택 강제 우회 프로토콜 적용 중...", 0.7),
        (64, "커널 분석 가중치 레이어 초고속 재연산 진행 중...", 0.4),
        (89, "무결성 서명 수동 우회 디코딩 완료...", 0.5),
        (99, "최종 연산 매트릭스 빌딩 완료...", 1.0),
        (100, "✅ 연산 성공. 최종 레포트 인덱스를 정상 복구하여 인출했습니다.", 0.8)
    ]

    for val, txt, delay in dance_timeline:
        status.text(txt)
        progress.progress(val)
        time.sleep(delay)

    st.session_state.app_step = 5
    st.rerun()

# ---------------- 화면 5: 결과 ----------------
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

    st.title("종합 분석 결과 보고서")

    cluster_interpretations = {
        0: '매우 건강군 (폐암진단여부 0이 많음)',
        1: '건강군 (폐암진단여부 1이 많음)',
        2: '중간 그룹 (폐암진단여부 0과 1이 혼재)',
        3: '강한 폐암 위험군 (폐암진단여부 1이 많음)'
    }

    st.write(f"의료 분석 결과 귀하는 통계학적으로 **{pred_cluster[0]}번 군집**에 배정되었습니다.")
    st.info(f"군집 임상적 소견: \'{cluster_interpretations.get(pred_cluster[0], '분류 불가 인덱스')}\'")

    st.caption("""
    본 결과는 입력 데이터를 기반으로 생성된 통계적 분석 결과이며,
    실제 의료기관의 진단 결과와 차이가 발생할 수 있습니다. 증상이 의심될 경우 전문의와 상담하십시오.
    """)

    X_original = df_original[['나이', '흡연여부', '음주여부']]
    X_scaled_original = scaler.transform(X_original)
    df_original['cluster'] = model.predict(X_scaled_original)

    colors = ['red', 'blue', 'green', 'purple']
    df_original['c'] = df_original['cluster'].map({
        0: colors[0],
        1: colors[1],
        2: colors[2],
        3: colors[3]
    })

    # [✨ 완벽한 한글화] 폰트 파일을 로드하므로 마음 놓고 한글을 사용하셔도 됩니다!
    subhead_text = '폐암 환자 군집 분석 및 새 환자 위치 (흡연여부 vs 음주여부)'
    st.subheader(subhead_text)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        df_original['흡연여부'],
        df_original['음주여부'],
        c=df_original['c'],
        alpha=0.5,
        s=50,
        label='기존 환자 군집 데이터셋'
    )

    ax.scatter(
        input_smokes,
        input_alcohol,
        c='black',
        s=300,
        marker='X',
        label='현재 피험자 매핑 위치 (X)'
    )

    ax.set_xlabel("흡연여부 (Smoking Index)")
    ax.set_ylabel("음주여부 (Alcohol Index)")
    ax.set_title("다차원 군집 내 피험자 상대 좌표 매핑")

    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    st.write("**알고리즘 참조용 군집 중심값 (역정규화 행렬 매트릭스)**")
    st.write(pd.DataFrame(scaler.inverse_transform(model.cluster_centers_),
            columns=['나이', '흡연여부', '음주여부'],
            index=[f'Cluster {i}' for i in range(model.n_clusters)]))

    st.write("")

    if st.button("신규 피험자 데이터 재분석 요청"):
        st.session_state.app_step = 3
        st.rerun()

    st.stop()
