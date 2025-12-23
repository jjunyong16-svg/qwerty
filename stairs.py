import streamlit as st
import random
import time

# --- Page Configuration ---
st.set_page_config(page_title="Infinite Stairs - Streamlit", layout="centered")

def init_game():
    """게임 상태 초기화"""
    st.session_state.score = 0
    st.session_state.game_over = False
    # 계단 방향: 0은 왼쪽 위, 1은 오른쪽 위
    # 첫 계단은 항상 중앙에서 시작할 수 있도록 설정
    st.session_state.stairs = [random.randint(0, 1) for _ in range(20)]
    st.session_state.current_pos = 50  # 시각적 위치 (백분율)
    st.session_state.player_facing = 1 # 0: Left, 1: Right
    st.session_state.start_time = time.time()
    st.session_state.high_score = st.session_state.get('high_score', 0)

# 세션 상태 초기화
if 'score' not in st.session_state:
    init_game()

# --- CSS for Styling ---
st.markdown("""
    <style>
    .game-container {
        background-color: #87CEEB;
        height: 500px;
        position: relative;
        border: 5px solid #333;
        border-radius: 10px;
        overflow: hidden;
        display: flex;
        flex-direction: column-reverse;
        align-items: center;
    }
    .stair {
        width: 60px;
        height: 20px;
        background-color: #8B4513;
        border: 2px solid #5D2E0A;
        position: absolute;
    }
    .player {
        width: 40px;
        height: 40px;
        font-size: 30px;
        position: absolute;
        z-index: 10;
        transition: all 0.1s ease-out;
        bottom: 40px;
    }
    .stats {
        font-family: 'Courier New', Courier, monospace;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .btn-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }
    .stButton>button {
        width: 120px;
        height: 60px;
        font-size: 20px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Game Logic ---
def climb(action):
    """
    action: 'climb' (오르기), 'turn' (방향 전환)
    """
    if st.session_state.game_over:
        return

    next_stair_direction = st.session_state.stairs[0]
    
    if action == 'climb':
        # 현재 바라보는 방향과 다음 계단의 방향이 같아야 함
        if st.session_state.player_facing == next_stair_direction:
            st.session_state.score += 1
            # 계단 업데이트 (새 계단 추가)
            st.session_state.stairs.pop(0)
            st.session_state.stairs.append(random.randint(0, 1))
        else:
            st.session_state.game_over = True
    
    elif action == 'turn':
        # 방향 전환 후 오르기
        st.session_state.player_facing = 1 - st.session_state.player_facing
        if st.session_state.player_facing == next_stair_direction:
            st.session_state.score += 1
            st.session_state.stairs.pop(0)
            st.session_state.stairs.append(random.randint(0, 1))
        else:
            st.session_state.game_over = True

    # 최고 기록 업데이트
    if st.session_state.score > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score

# --- UI Layout ---
st.title("🏃‍♂️ 무한의 계단 (Infinite Stairs)")
st.write("방향을 잘 보고 계단을 오르세요! 잘못된 방향을 누르면 게임 오버!")

# 상단 스탯
col1, col2 = st.columns(2)
col1.metric("현재 점수", st.session_state.score)
col2.metric("최고 기록", st.session_state.high_score)

# 게임 화면 렌더링
# 시각적 계단 리스트 계산 (플레이어 위치 기준)
stairs_html = ""
current_x = 50  # 중앙 시작
for i, direction in enumerate(st.session_state.stairs[:15]):
    # 계단 쌓기 로직 (시각화용)
    if i > 0:
        if direction == 0: current_x -= 8
        else: current_x += 8
    
    bottom_pos = i * 30 + 20
    stairs_html += f'<div class="stair" style="bottom: {bottom_pos}px; left: calc({current_x}% - 30px);"></div>'

player_emoji = "🏃‍♂️" if st.session_state.player_facing == 1 else "🏃‍♀️"
player_flip = "scaleX(1)" if st.session_state.player_facing == 1 else "scaleX(-1)"

game_screen = f"""
    <div class="game-container">
        {stairs_html}
        <div class="player" style="left: calc(50% - 20px); transform: {player_flip};">
            {player_emoji}
        </div>
    </div>
"""
st.markdown(game_screen, unsafe_allow_html=True)

# 조작 버튼
if not st.session_state.game_over:
    st.markdown("<div class='btn-container'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬆️ 오르기 (Climb)", use_container_width=True):
            climb('climb')
            st.rerun()
    with c2:
        if st.button("🔄 방향전환 (Turn)", use_container_width=True):
            climb('turn')
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error(f"게임 오버! 최종 점수: {st.session_state.score}")
    if st.button("다시 시작하기", type="primary"):
        init_game()
        st.rerun()

# 도움말
with st.expander("게임 방법"):
    st.write("""
    1. **오르기**: 현재 캐릭터가 바라보는 방향에 계단이 있으면 한 칸 올라갑니다.
    2. **방향전환**: 캐릭터의 방향을 반대로 바꾸면서 동시에 한 칸 올라갑니다.
    3. 계단이 없는 방향으로 이동하려고 하면 게임이 종료됩니다.
    """)
