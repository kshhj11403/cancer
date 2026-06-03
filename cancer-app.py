import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import time
import random
import os

# ---------------- 시스템 핵심 설정 ----------------
st.set_page_config(
    page_title="국가 지정 AI 보건의료 데이터 통합 분석 연동망",
    page_icon="🏢",
    layout="centered"
)

# 나눔고딕 실시간 로드 및 백업 서체 설정
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
except:
    plt.rcParams['font.family'] = ['Malgun Gothic', 'AppleGothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# ---------------- 세션 상태 스택 관리 ----------------
if 'app_step' not in st.session_state: st.session_state.app_step = 0
if 'smokes_score' not in st.session_state: st.session_state.smokes_score = 0.0
if 'alcohol_score' not in st.session_state: st.session_state.alcohol_score = 0.0
if 'vip_unlocked' not in st.session_state: st.session_state.vip_unlocked = False

# 🎮 공룡 게임 세션 변수
if 'dino_y' not in st.session_state: st.session_state.dino_y = 0  # 0: 바닥, 1: 점프 중
if 'cactus_x' not in st.session_state: st.session_state.cactus_x = 10
if 'dino_score' not in st.session_state: st.session_state.dino_score = 0

# 🥁 리듬 게임 세션 변수
if 'beat_pos' not in st.session_state: st.session_state.beat_pos = 0
if 'rhythm_score' not in st.session_state: st.session_state.rhythm_score = 0
if 'rhythm_msg' not in st.session_state: st.session_state.rhythm_msg = "대기 중"

# ---------------- 데이터 및 모델 가상화 (무결성 보장) ----------------
class DummyModel:
    def predict(self, X): return [random.randint(0, 3) for _ in range(len(X))]
    @property
    def n_clusters(self): return 4
    @property
    def cluster_centers_(self): return [[38, 4, 1], [48, 15, 6], [51, 8, 3], [65, 25, 9]]
class DummyScaler:
    def transform(self, X): return X
    def inverse_transform(self, X): return X

try:
    if not os.path.exists('cancer.csv'):
        pd.DataFrame({'A': [30,40,50,60], 'B': [1,5,10,20], 'C': [0,2,5,8]}).to_csv('cancer.csv', index=False)
    model = joblib.load('cancer_model.pkl') if os.path.exists('cancer_model.pkl') else DummyModel()
    scaler = joblib.load('cancer_scaler.pkl') if os.path.exists('cancer_scaler.pkl') else DummyScaler()
    df_original = pd.read_csv('cancer.csv')
    cols = [c for c in df_original.columns if pd.to_numeric(df_original[c], errors='coerce').notnull().all()]
    df_original.rename(columns={cols[0]: '나이', cols[1]: '흡연여부', cols[2]: '음주여부'}, inplace=True)
except:
    pass

# ---------------- 사이드바 고정 ----------------
with st.sidebar:
    st.subheader("🌐 원격 노드 관제")
    st.info("국가 정보 보건 허브 보안 인증 완료")
    st.caption("인접 노드 대기 순번")
    st.markdown(f"**{random.randint(450, 890)}번째 대기 중**")

# ---------------- [화면 0] 게이트웨이 ----------------
if st.session_state.app_step == 0:
    st.title("🏢 국가 보건의료 AI 빅데이터 통합 분석 연동망")
    st.subheader("Public Health Intelligence Cloud Core v4.5")
    
    st.markdown("""
    > **[공지]** 본 전산망은 임상 코호트 예측 모델 연동을 위한 보안 세션망입니다. 
    > 분석 도중 매크로 우회 방지를 위한 **생체 반응성 검증 테스트(인프라 연동 미니게임)**가 강제 실행될 수 있습니다.
    """)
    
    if st.button("공공 인증 세션 수립 및 진입", type="primary"):
        st.session_state.app_step = 1
        st.rerun()
    st.stop()

# ---------------- [화면 1] 독소 조항 약관 ----------------
if st.session_state.app_step == 1:
    st.title("보안 전자 서명 및 동의서 기술 준수")
    
    col1, col2 = st.columns(2)
    with col1:
        a1 = st.checkbox("[필수] 고유인식정보 분산 연산 동의")
        a2 = st.checkbox("[필수] 의료 데이터 제3자 위탁 제공 동의")
    with col2:
        a3 = st.checkbox("[필수] 시스템 이용 약관 규격 준수 동의")
        a4 = st.checkbox("[필수] 분석 실패 시 서버 과열 부담금 14,000원 청구 동의")

    st.text_area("연동 협약 조항 전문", value="[특약 사항] 피험자는 시스템의 방화벽 해제를 위한 보안 미니게임 수행 의무를 가지며, 실패 시 사출됨을 동의한다.", height=80, disabled=True)
    
    if st.button("전자 서명 제출", type="secondary"):
        if not (a1 and a2 and a3):
            st.error("필수 약관에 동의하지 않았습니다.")
        elif a4:
            st.error("🚨 [보안 위반] '서버 부담금 조항'은 함정 독소 조항입니다! 체크를 해제하고 다시 제출하십시오.")
        else:
            st.success("인증 서명이 정상 수립되었습니다.")
            time.sleep(0.8)
            st.session_state.app_step = 3
            st.rerun()
    st.stop()

# ---------------- [화면 3] 지표 파라미터 매핑 ----------------
if st.session_state.app_step == 3:
    st.title("임상 지표 파라미터 매핑 엔진")
    
    st.subheader("1. 생체 연령 동적 락인 (Age Dynamic Lock-in)")
    dynamic_age = random.randint(20, 70)
    col_age1, col_age2 = st.columns([3, 1])
    with col_age1:
        st.metric("🚨 실시간 동적 스캔 연령", f"만 {dynamic_age} 세")
    with col_age2:
        if st.button("🎯 지금 나이로 확정"):
            st.session_state.locked_age = dynamic_age
            
    if 'locked_age' in st.session_state:
        st.info(f"현재 고정된 파라미터: 만 {st.session_state.locked_age}세")
    else:
        st.warning("연령 타이밍 고정이 완료되어야 분석 요청이 가능합니다.")

    st.divider()

    st.subheader("2. 가변 축적형 생활 습관 데이터")
    col_smoke, col_alc = st.columns(2)
    with col_smoke:
        st.metric("누적 흡연 지표", f"{st.session_state.smokes_score:.1f}")
        if st.button("🚬 흡연 가중치 +1.5"):
            if random.random() < 0.25:
                st.warning("🚭 금연 패치 가동! 지표 차감 (-2.5)")
                st.session_state.smokes_score = max(0.0, st.session_state.smokes_score - 2.5)
            else:
                st.session_state.smokes_score += 1.5
            st.rerun()
            
    with col_alc:
        st.metric("누적 음주 지표", f"{st.session_state.alcohol_score:.1f}")
        if st.button("🍺 음주 가중치 +1.0"):
            if random.random() < 0.25:
                st.error("🤢 알코올 데이터 역류 발생 (-3.0)")
                st.session_state.alcohol_score = max(0.0, st.session_state.alcohol_score - 3.0)
            else:
                st.session_state.alcohol_score += 1.0
            st.rerun()

    st.write("")
    if st.button("국가 연산망 자원 요청", type="secondary"):
        if 'locked_age' not in st.session_state:
            st.error("연령 동적 락인이 누락되었습니다.")
        else:
            st.session_state.input_age = st.session_state.locked_age
            st.session_state.input_smokes = st.session_state.smokes_score
            st.session_state.input_alcohol = st.session_state.alcohol_score
            st.session_state.app_step = 4  # 공룡게임 스테이지 진입
            st.rerun()
    st.stop()

# ---------------- [화면 4] 억까 공룡 게임 (Dino Jump) ----------------
if st.session_state.app_step == 4:
    st.title("🦖 패킷 우회용 생체 반응성 테스트 (Step 1)")
    st.caption("방화벽의 매크로 차단 센서 우회를 위해 선인장을 3회 점프하여 통과하십시오.")
    
    # 장애물 동적 이동 시뮬레이션
    st.session_state.cactus_x -= random.choice([2, 3])
    if st.session_state.cactus_x <= 0:
        st.session_state.cactus_x = 10
        st.session_state.dino_score += 1
        st.session_state.dino_y = 0 # 바닥으로 리셋
        
    # 충돌 판정 (장애물이 도달했는데 점프를 안 한 경우)
    if st.session_state.cactus_x in [1, 2] and st.session_state.dino_y == 0:
        st.error("💥 [충돌 감지] 선인장에 척추를 부딪혔습니다! 임상 연산 신뢰도가 깎여 스코어가 초기화됩니다.")
        st.session_state.dino_score = 0
        st.session_state.cactus_x = 10
        time.sleep(1.2)
        st.rerun()

    if st.session_state.dino_score >= 3:
        st.success("🎉 공룡 방화벽 돌파 성공! 다음 리듬 보안 레이어로 진입합니다.")
        time.sleep(1.0)
        st.session_state.app_step = 42 # 리듬게임으로 이동
        st.rerun()

    # 렌더링 화면
    sky = "☁️" + " " * 30 + "☁️"
    
    # 공룡 위치 렌더링
    if st.session_state.dino_y == 1:
        dino_line = "      🦖 (Jump!)"
        ground_line = "🏃" + " " * (st.session_state.cactus_x * 3) + "🌵"
    else:
        dino_line = " "
        ground_line = "      🦖" + " " * (st.session_state.cactus_x * 3) + "🌵"
        
    floor = "—" * 40
    
    st.code(f"{sky}\n{dino_line}\n{ground_line}\n{floor}", language="text")
    st.metric("🌵 피해낸 선인장 갯수", f"{st.session_state.dino_score} / 3")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        if st.button("🦘 [점프!!] 고도 상승", type="primary"):
            st.session_state.dino_y = 1
            st.rerun()
    with col_d2:
        if st.button("🏃 시간 전진 (장애물 다가오기)"):
            if st.session_state.dino_y == 1 and st.session_state.cactus_x > 3:
                # 공룡이 공중에 떠있는 동안 시간이 흐르면 낙하 준비
                st.session_state.dino_y = 0
            st.rerun()
    st.stop()

# ---------------- [화면 4-2] 임상 비트 리듬 게임 (Clinical Beat) ----------------
if st.session_state.app_step == 42:
    st.title("🥁 인프라 무결성 싱크로율 측정 (Step 2)")
    st.caption("연산 비트박스 판정선 [ | ] 정중앙에 노드(◯)가 올 때 정확히 스매시 버튼을 누르십시오.")
    
    # 노드 임의 이동
    st.session_state.beat_pos += random.choice([1, 2])
    if st.session_state.beat_pos > 14:
        st.session_state.beat_pos = 0
        st.session_state.rhythm_msg = "MISS (비트 이탈)"
        
    # 판정선 렌더링
    lane = [" "] * 15
    lane[7] = "|" # 판정 영역
    if st.session_state.beat_pos < 15:
        lane[st.session_state.beat_pos] = "◯"
        
    render_lane = "비트 레일: [ " + "".join(lane) + " ]"
    st.code(render_lane, language="text")
    
    st.markdown(f"**직전 판정:** `{st.session_state.rhythm_msg}`")
    st.metric("🎯 PERFECT 누적 횟수", f"{st.session_state.rhythm_score} / 3")

    if st.session_state.rhythm_score >= 3:
        st.success("🥇 전산 비트 동기화 완벽 완료! 최종 코어 소견 리포트 인출 단계로 자동 이행합니다.")
        time.sleep(1.2)
        st.session_state.app_step = 5
        st.rerun()

    c_r1, c_r2 = st.columns(2)
    with c_r1:
        if st.button("💥 [판정 스매시!]", type="primary"):
            # 정중앙 (인덱스 7 주변) 판정 로직
            if st.session_state.beat_pos == 7:
                st.session_state.rhythm_score += 1
                st.session_state.rhythm_msg = "🔥 PERFECT! (싱크로율 100%)"
            elif st.session_state.beat_pos in [6, 8]:
                st.session_state.rhythm_msg = "⚠️ GOOD (타이밍 미세 불안정)"
            else:
                st.session_state.rhythm_msg = "❌ BAD (박치 감지)"
            st.session_state.beat_pos = 0 # 노드 리셋
            st.rerun()
    with c_r2:
        if st.button("🎵 비트 흘려보내기 (다음 프레임)"):
            st.rerun()
    st.stop()

# ---------------- [화면 5] 결제 유도 페이크 및 결과 보고 ----------------
if st.session_state.app_step == 5:
    st.title("🔬 AI 임상 진단 종합 분석 보고서")
    
    if not st.session_state.vip_unlocked:
        st.subheader("🔒 개인 맞춤형 정밀 소견서 암호화 상태")
        st.markdown("""
        <div style="background-color:#fff3cd; padding:20px; border-radius:10px; text-align:center; border:1px solid #ffeeba;">
            <h4 style="color:#856404; margin:0;">💎 국가지정 프리미엄 보건 가이드라인 개방</h4>
            <p style="color:#856404; font-size:14px;">월 9,900원으로 제한 없는 실시간 AI 처방 가이드를 열람하십시오.</p>
            <h3 style="color:#dc3545; margin:10px 0;">클라우드 전산망 유지비 첫 달 100원!</h3>
        </div>
        """, unsafe_allow_html=True)
        
        c_vip1, c_vip2 = st.columns([4, 1])
        with c_vip1:
            if st.button("💳 100원 결제 후 프리미엄 즉시 개방", type="primary"):
                st.error("💳 [결제 시스템 대기] 현재 금융결제원 망 과부하로 일반 결제가 반려되었습니다. 무료 마이크로 링크를 추적하십시오.")
        with c_vip2:
            if st.button(".", help="무료로 결과 강제 열람 (비권장)"):
                st.session_state.vip_unlocked = True
                st.rerun()
        st.caption("※ 무료 열람용 마이크로 트리거 버튼은 우측 상단 점(.) 영역에 1픽셀 크기로 기재되어 있습니다.")
        st.stop()

    # 최종 결과 바인딩
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

    st.success("🔓 암호화 해제 성공. 억까 미니게임 클리어 보상으로 임상 리포트가 인출되었습니다.")
    st.write(f"의료 AI 임상 연산 결과 귀하는 통계학적으로 **{pred_cluster[0]}번 코호트 군집**에 분류되었습니다.")
    st.info(f"🧬 종합 소견 보고: \'{cluster_interpretations.get(pred_cluster[0], '분류 불가 인덱스')}\'")

    # 결과 차트 출력
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(df_original['나이'], df_original['음주여부'], c='gray', alpha=0.3, label='기존 대조군 데이터셋')
    ax.scatter(input_age, input_alcohol, c='red', s=400, marker='*', label='피험자 스냅샷 위치 (★)')
    
    if 'font_prop' in locals():
        ax.set_xlabel("나이", fontproperties=font_prop)
        ax.set_ylabel("음주 임상 지표", fontproperties=font_prop)
        ax.set_title("다차원 코호트 군집 내 피험자 상대 위치 매핑", fontproperties=font_prop)
        legend = ax.legend()
        for text in legend.get_texts(): text.set_fontproperties(font_prop)
    
    st.pyplot(fig)

    if st.button("🔄 원격 세션 로그아웃 (초기화)"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
