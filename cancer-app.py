import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import time
import random
import os
import streamlit.components.v1 as components

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
if 'ctrl_age' not in st.session_state: st.session_state.ctrl_age = 30
if 'smokes_score' not in st.session_state: st.session_state.smokes_score = 0.0
if 'alcohol_score' not in st.session_state: st.session_state.alcohol_score = 0.0
if 'vip_unlocked' not in st.session_state: st.session_state.vip_unlocked = False

# ---------------- 데이터 및 모델 가상화 ----------------
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
    st.subheader("Public Health Intelligence Cloud Core v6.0")
    
    st.markdown("""
    > **[중요 공지]** 본 전산망은 고도화된 클라우드 보안 환경(HTML5 하드웨어 가속 센서)을 요구합니다. 
    > 세션 무단 점유 방지를 위한 비인가 자동화(Macro) 차단 스크리닝 패널을 통과하셔야 최종 임상 분석 소견서 인출이 가능합니다.
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
        a4 = st.checkbox("[필수] 인프라 물리 가속(Canvas) 검증 미달 시 재유도 동의")

    st.text_area("연동 협약 조항 전문", value="[특약 사항] 피험자는 시스템의 방화벽 해제를 위한 고급 보안 인터랙티브 패널(Canvas Game) 수행 의무를 가지며, 스코어 미달 시 결과 열람 권한이 제한됨을 동의한다.", height=80, disabled=True)
    
    if st.button("전자 서명 제출", type="secondary"):
        if not (a1 and a2 and a3 and a4):
            st.error("필수 항목에 대해 전원 동의서 서명이 완료되어야 서브넷 게이트가 개방됩니다.")
        else:
            st.success("인증 서명이 정상 수립되었습니다.")
            time.sleep(0.5)
            st.session_state.app_step = 3
            st.rerun()
    st.stop()

# ---------------- [화면 3] 지표 파라미터 매핑 ----------------
if st.session_state.app_step == 3:
    st.title("임상 지표 파라미터 매핑 엔진")
    
    st.subheader("1. 생체 연령 동적 캘리브레이션")
    st.caption("※ 보안 인터록 장치: 입력값 수치가 5의 배수가 되는 순간 윤활 마찰 계수가 감소하여 -3만큼 미끄러집니다. 컨트롤력을 발휘해 타겟 연령을 맞추십시오.")
    
    col_a1, col_a2, col_a3 = st.columns([1, 2, 1])
    with col_a1:
        if st.button("🔽 나이 감소"):
            st.session_state.ctrl_age -= 1
            if st.session_state.ctrl_age % 5 == 0: st.session_state.ctrl_age -= 3
            st.rerun()
    with col_a2:
        st.metric("현재 조정된 연령 수치", f"만 {st.session_state.ctrl_age} 세")
    with col_a3:
        if st.button("🔼 나이 증가"):
            st.session_state.ctrl_age += 1
            if st.session_state.ctrl_age % 5 == 0: st.session_state.ctrl_age -= 3
            st.rerun()

    st.divider()

    st.subheader("2. 가변 축적형 생활 습관 데이터")
    col_smoke, col_alc = st.columns(2)
    with col_smoke:
        st.metric("누적 흡연 지표", f"{st.session_state.smokes_score:.1f}")
        if st.button("🚬 흡연 가중치 +1.5"):
            if random.random() < 0.2:
                st.warning(" Nicky 쉴드 가동! 수치 낙하 (-2.5)")
                st.session_state.smokes_score = max(0.0, st.session_state.smokes_score - 2.5)
            else:
                st.session_state.smokes_score += 1.5
            st.rerun()
            
    with col_alc:
        st.metric("누적 음주 지표", f"{st.session_state.alcohol_score:.1f}")
        if st.button("🍺 음주 가중치 +1.0"):
            if random.random() < 0.2:
                st.error("🤢 데이터 역류 발생 (-3.0)")
                st.session_state.alcohol_score = max(0.0, st.session_state.alcohol_score - 3.0)
            else:
                st.session_state.alcohol_score += 1.0
            st.rerun()

    st.write("")
    if st.button("국가 연산망 자원 요청", type="secondary"):
        st.session_state.input_age = st.session_state.ctrl_age
        st.session_state.input_smokes = st.session_state.smokes_score
        st.session_state.input_alcohol = st.session_state.alcohol_score
        st.session_state.app_step = 4  
        st.rerun()
    st.stop()

# ---------------- [화면 4] 초고퀄리티 HTML5 Canvas 공룡 게임 ----------------
if st.session_state.app_step == 4:
    st.title("🦖 패킷 가속용 크롬 다이노 센서 검증 (Step 1)")
    st.subheader("목표 점수: 15점 달성")
    st.caption("스페이스바(Space) 또는 마우스 클릭으로 점프할 수 있습니다. 충돌 시 스코어가 초기화됩니다.")
    
    dino_html = """
    <div style="text-align:center; background:#f7f7f7; padding:15px; border-radius:10px; border:2px solid #ccc; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <canvas id="dinoCanvas" width="600" height="150" style="background:#fff; border-bottom:3px solid #333;"></canvas>
        <h3 style="color:#333; font-family:sans-serif;">Score: <span id="scoreNum">0</span> / 15</h3>
        <p style="font-size:12px; color:#666;">[스페이스바] 또는 [화면 클릭]시 점프</p>
        <button id="nextStageBtn" disabled style="padding:10px 20px; font-weight:bold; background:#aaa; color:#fff; border:none; border-radius:5px; cursor:not-allowed; transition: 0.3s;">다음 스테이지 락 해제 대기</button>
    </div>

    <script>
        const canvas = document.getElementById("dinoCanvas");
        const ctx = canvas.getContext("2d");
        
        let score = 0;
        let dino = { x: 50, y: 120, wy: 30, h: 30, jumping: false, vY: 0 };
        let obstacles = [];
        let gameActive = true;
        let frame = 0;

        function spawnObstacle() {
            if (Math.random() < 0.02 && obstacles.length < 2) {
                obstacles.push({ x: 600, y: 125, w: 15, h: 25, speed: 4.5 + score*0.15 });
            }
        }

        function update() {
            if (!gameActive) return;
            frame++;
            
            if (dino.jumping) {
                dino.vY += 0.6; 
                dino.y += dino.vY;
                if (dino.y >= 120) {
                    dino.y = 120;
                    dino.jumping = false;
                    dino.vY = 0;
                }
            }

            spawnObstacle();
            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= obstacles[i].speed;
                
                if (obstacles[i].x < dino.x + 20 && obstacles[i].x + obstacles[i].w > dino.x &&
                    obstacles[i].y < dino.y + dino.h && obstacles[i].y + obstacles[i].h > dino.y) {
                    score = 0;
                    obstacles = [];
                    document.getElementById("scoreNum").innerText = score;
                }

                if (obstacles[i] && obstacles[i].x < -20) {
                    obstacles.splice(i, 1);
                    score++;
                    document.getElementById("scoreNum").innerText = score;
                    if (score >= 15) {
                        const btn = document.getElementById("nextStageBtn");
                        btn.disabled = false;
                        btn.style.background = "#28a745";
                        btn.style.cursor = "pointer";
                        btn.innerText = "클리어! 다음 레이어로 가기 (클릭)";
                    }
                }
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = "#535353";
            ctx.fillRect(dino.x, dino.y, 25, dino.h);
            ctx.fillStyle = "#fff";
            ctx.fillRect(dino.x + 18, dino.y + 5, 4, 4);
            
            ctx.fillStyle = "#228b22";
            for (let obs of obstacles) {
                ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
            }
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        window.addEventListener("keydown", (e) => {
            if (e.code === "Space" && !dino.jumping) {
                dino.jumping = true;
                dino.vY = -10.5;
            }
        });

        canvas.addEventListener("click", () => {
            if (!dino.jumping) {
                dino.jumping = true;
                dino.vY = -10.5;
            }
        });

        loop();
    </script>
    """
    components.html(dino_html, height=270)
    
    st.caption("💡 15점을 달성하면 캔버스 내부의 [클리어!] 버튼이 켜집니다. 그 후 아래 버튼을 눌러 확정하십시오.")
    if st.button("⏩ 공룡 보안망 통과 확정"):
        st.session_state.app_step = 42
        st.rerun()
    st.stop()

# ---------------- [화면 4-2] 리뉴얼된 초고퀄 아케이드 리듬 게임 (사운드/네온 추가) ----------------
if st.session_state.app_step == 42:
    st.title("🥁 전산 무결성 동기화 웹 리듬 센터 (Step 2)")
    st.subheader("목표: 스코어 30점 획득 (Sound On 🔊)")
    st.caption("A, S, D, F 키를 타이밍 맞춰 타격하십시오. 완벽한 타격 시 퍼펙트 판정과 추가 점수가 부여됩니다.")
    
    rhythm_html = """
    <div style="text-align:center; background:linear-gradient(180deg, #111 0%, #1a1a2e 100%); padding:20px; border-radius:12px; color:#fff; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 0 10px 20px rgba(0,0,0,0.5);">
        <div style="display:flex; justify-content:space-around; margin-bottom:15px; font-size: 18px; font-weight: bold; text-shadow: 0 0 10px #0ff;">
            <div>SCORE: <span id="rScore" style="color:#0f0;">0</span> / 30</div>
            <div>COMBO: <span id="rCombo" style="color:#ff00aa;">0</span></div>
        </div>
        <canvas id="rhythmCanvas" width="320" height="400" style="background:#0a0a0a; border:3px solid #333; border-radius: 8px; box-shadow: inset 0 0 20px #000;"></canvas>
        <div style="margin-top:15px; font-size:14px; color:#ccc; letter-spacing: 2px;">
            <span style="color:#ff3366">A</span> ━ <span style="color:#33ccff">S</span> ━ <span style="color:#33ff33">D</span> ━ <span style="color:#ffcc00">F</span>
        </div>
        <button id="finalGateBtn" disabled style="margin-top:15px; padding:12px 24px; background:#333; color:#777; border:none; border-radius:8px; cursor:not-allowed; font-weight:bold; font-size: 16px; transition: all 0.3s ease;">데이터베이스 락 해제 대기 중...</button>
    </div>

    <script>
        const canvas = document.getElementById("rhythmCanvas");
        const ctx = canvas.getContext("2d");
        
        // 사운드 컨텍스트 (Web Audio API)
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playSound(type) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            if (type === 'perfect') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(880, audioCtx.currentTime); // 고음 띠링
                osc.frequency.exponentialRampToValueAtTime(1760, audioCtx.currentTime + 0.1);
                gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
                osc.start(); osc.stop(audioCtx.currentTime + 0.2);
            } else if (type === 'good') {
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(440, audioCtx.currentTime); 
                gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
                osc.start(); osc.stop(audioCtx.currentTime + 0.15);
            } else { // miss
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(150, audioCtx.currentTime); 
                gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
                osc.start(); osc.stop(audioCtx.currentTime + 0.1);
            }
        }

        let score = 0, combo = 0, frames = 0;
        let notes = [];
        let hitTexts = [];
        let keyStates = [false, false, false, false];
        
        // 레일 설정: X좌표 및 네온 컬러
        const lanes = [
            { x: 40,  color: '#ff3366', key: 'KeyA' },
            { x: 120, color: '#33ccff', key: 'KeyS' },
            { x: 200, color: '#33ff33', key: 'KeyD' },
            { x: 280, color: '#ffcc00', key: 'KeyF' }
        ];
        
        function update() {
            frames++;
            // 비트에 맞춘 스폰 로직 (일정 프레임마다 스폰)
            if (frames % 40 === 0 && Math.random() > 0.2) {
                let laneIdx = Math.floor(Math.random() * 4);
                notes.push({ x: lanes[laneIdx].x, y: -20, lane: laneIdx, speed: 5 });
            }

            for (let i = notes.length - 1; i >= 0; i--) {
                notes[i].y += notes[i].speed;
                if (notes[i].y > 420) {
                    notes.splice(i, 1);
                    combo = 0;
                    hitTexts.push({ text: 'MISS', x: canvas.width/2, y: 320, alpha: 1.0, color: '#ff0000' });
                    playSound('miss');
                    updateUI();
                }
            }

            // 플로팅 텍스트 애니메이션 업데이트
            for (let i = hitTexts.length - 1; i >= 0; i--) {
                hitTexts[i].y -= 1;
                hitTexts[i].alpha -= 0.02;
                if (hitTexts[i].alpha <= 0) hitTexts.splice(i, 1);
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // 키가 눌려있을 때 레일 배경 점등 효과
            for (let i=0; i<4; i++) {
                if (keyStates[i]) {
                    let grad = ctx.createLinearGradient(0, 0, 0, 400);
                    grad.addColorStop(0, "rgba(0,0,0,0)");
                    grad.addColorStop(1, lanes[i].color + "66"); // 투명도 추가
                    ctx.fillStyle = grad;
                    ctx.fillRect(lanes[i].x - 40, 0, 80, 400);
                }
            }

            // 판정 라인 (네온 효과)
            ctx.shadowBlur = 15;
            ctx.shadowColor = "#fff";
            ctx.strokeStyle = "#fff";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 340);
            ctx.lineTo(320, 340);
            ctx.stroke();
            ctx.shadowBlur = 0; // 리셋

            // 떨어지는 노트 그리기
            for (let note of notes) {
                ctx.shadowBlur = 10;
                ctx.shadowColor = lanes[note.lane].color;
                ctx.fillStyle = lanes[note.lane].color;
                
                ctx.beginPath();
                // 둥근 사각형 형태의 노트
                ctx.roundRect(note.x - 30, note.y - 10, 60, 20, 10);
                ctx.fill();
                
                ctx.shadowBlur = 0;
                ctx.fillStyle = "#fff";
                ctx.fillRect(note.x - 15, note.y - 2, 30, 4); // 노트 내부 하이라이트
            }

            // 타격 판정 텍스트 렌더링
            ctx.font = "bold 24px Arial";
            ctx.textAlign = "center";
            for (let ht of hitTexts) {
                ctx.fillStyle = ht.color;
                ctx.globalAlpha = Math.max(0, ht.alpha);
                ctx.fillText(ht.text, ht.x, ht.y);
                ctx.globalAlpha = 1.0;
            }
        }

        function updateUI() {
            document.getElementById("rScore").innerText = score;
            document.getElementById("rCombo").innerText = combo;

            if (score >= 30) {
                const btn = document.getElementById("finalGateBtn");
                btn.disabled = false;
                btn.style.background = "#ffea00";
                btn.style.color = "#000";
                btn.style.boxShadow = "0 0 15px #ffea00";
                btn.style.cursor = "pointer";
                btn.innerText = "★ 소견서 봉인 전면 해제 (클릭) ★";
            }
        }

        function checkHit(laneIdx) {
            let hitFound = false;
            for (let i = 0; i < notes.length; i++) {
                if (notes[i].lane === laneIdx) {
                    let dist = Math.abs(notes[i].y - 340); // 판정선 y=340
                    if (dist < 25) { // Perfect
                        score += 3;
                        combo++;
                        hitTexts.push({ text: 'PERFECT!', x: lanes[laneIdx].x, y: 320, alpha: 1.0, color: '#00ffff' });
                        playSound('perfect');
                        notes.splice(i, 1);
                        hitFound = true;
                        break;
                    } else if (dist < 55) { // Good
                        score += 1;
                        combo++;
                        hitTexts.push({ text: 'GOOD', x: lanes[laneIdx].x, y: 320, alpha: 1.0, color: '#33ff33' });
                        playSound('good');
                        notes.splice(i, 1);
                        hitFound = true;
                        break;
                    }
                }
            }
            if (!hitFound) {
                combo = 0; // 허공 타격 시 콤보 초기화
            }
            updateUI();
        }

        window.addEventListener("keydown", (e) => {
            let idx = lanes.findIndex(l => l.key === e.code);
            if (idx !== -1 && !keyStates[idx]) {
                if (audioCtx.state === 'suspended') audioCtx.resume();
                keyStates[idx] = true;
                checkHit(idx);
            }
        });

        window.addEventListener("keyup", (e) => {
            let idx = lanes.findIndex(l => l.key === e.code);
            if (idx !== -1) {
                keyStates[idx] = false;
            }
        });

        function mainLoop() {
            update();
            draw();
            requestAnimationFrame(mainLoop);
        }
        mainLoop();
    </script>
    """
    components.html(rhythm_html, height=520)
    
    st.caption("💡 팁: 30점을 기록하면 리듬 채널 내부의 노란색 봉인 해제 버튼이 켜집니다. 확정 후 아래를 클릭하십시오.")
    if st.button("🔒 보안 최종 인덱스 개방 완료 확정"):
        st.session_state.app_step = 5
        st.rerun()
    st.stop()

# ---------------- [화면 5] 결제 유도 페이크 및 최종 결과 보고 ----------------
if st.session_state.app_step == 5:
    st.title("🔬 AI 임상 진단 종합 분석 보고서")
    
    if not st.session_state.vip_unlocked:
        st.subheader("🔒 보건복지 연동 인프라 데이터 차단 해제")
        st.markdown("""
        <div style="background-color:#fff3cd; padding:20px; border-radius:10px; text-align:center; border:1px solid #ffeeba;">
            <h4 style="color:#856404; margin:0;">💎 국가 지정 정밀 임상 코호트 가이드라인 개방 권한</h4>
            <p style="color:#856404; font-size:14px;">월 9,900원으로 하드코어 미니게임을 프리패스하고 실시간 처방 가이드를 열람하십시오.</p>
            <h3 style="color:#dc3545; margin:10px 0;">인프라 서버 구동비 단 100원 결제 찬스!</h3>
        </div>
        """, unsafe_allow_html=True)
        
        c_vip1, c_vip2 = st.columns([4, 1])
        with c_vip1:
            if st.button("💳 100원 즉시 결제 및 결과 패스트트랙 오픈", type="primary"):
                st.error("💳 [결제 채널 통신 지연] 중앙 전산망 밴사 토큰 처리가 무한 지연 상태입니다. 우측 끝의 극초미세 무료 우회 점(.)을 클릭하십시오.")
        with c_vip2:
            if st.button(".", help="무료로 결과 강제 열람"):
                st.session_state.vip_unlocked = True
                st.rerun()
        st.stop()

    # 결과 데이터 처리 연산 복구
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

    st.success("🔓 암호화 해제 성공. 아케이드 게임을 뚫어낸 피험자의 최종 임상 소견서입니다.")
    st.write(f"국가 AI 임상 모델 연산 결과 귀하는 통계학적으로 **{pred_cluster[0]}번 코호트 군집**에 분류되었습니다.")
    st.info(f"🧬 종합 소견 보고: \'{cluster_interpretations.get(pred_cluster[0], '분류 불가 인덱스')}\'")

    # 결과 차트 출력
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.scatter(df_original['나이'], df_original['음주여부'], c='gray', alpha=0.3, label='기존 대조 코호트군 데이터')
    ax.scatter(input_age, input_alcohol, c='red', s=400, marker='*', label='당신의 상대적 생체 매핑 점 (★)')
    
    if 'font_prop' in locals():
        ax.set_xlabel("나이", fontproperties=font_prop)
        ax.set_ylabel("음주 임상 지표", fontproperties=font_prop)
        ax.set_title("다차원 코호트 군집 내 피험자 상대 위치 매핑", fontproperties=font_prop)
        legend = ax.legend()
        for text in legend.get_texts(): text.set_fontproperties(font_prop)
    
    st.pyplot(fig)

    if st.button("🔄 원격 세션 로그아웃 및 전산 데이터 전량 파기 (초기화)"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
