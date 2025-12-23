import streamlit as st
import numpy as np
import time
import random

# 설정
COLUMNS = 10
ROWS = 20

# 테트리스 블록 모양 정의
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#FFA500']

def init_game():
    st.session_state.board = np.zeros((ROWS, COLUMNS), dtype=int)
    st.session_state.current_piece = None
    st.session_state.score = 0
    st.session_state.game_over = False
    spawn_piece()

def spawn_piece():
    shape_name = random.choice(list(SHAPES.keys()))
    st.session_state.current_piece = {
        'shape': np.array(SHAPES[shape_name]),
        'x': COLUMNS // 2 - len(SHAPES[shape_name][0]) // 2,
        'y': 0,
        'color': random.randint(1, len(COLORS))
    }
    if not is_valid_move(st.session_state.current_piece, 0, 0):
        st.session_state.game_over = True

def is_valid_move(piece, dx, dy, shape=None):
    if shape is None:
        shape = piece['shape']
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val:
                new_x, new_y = piece['x'] + c + dx, piece['y'] + r + dy
                if not (0 <= new_x < COLUMNS and 0 <= new_y < ROWS) or \
                   (new_y >= 0 and st.session_state.board[new_y, new_x]):
                    return False
    return True

def merge_piece():
    p = st.session_state.current_piece
    for r, row in enumerate(p['shape']):
        for c, val in enumerate(row):
            if val:
                st.session_state.board[p['y'] + r, p['x'] + c] = p['color']
    clear_lines()
    spawn_piece()

def clear_lines():
    board = st.session_state.board
    full_lines = [i for i, row in enumerate(board) if all(row)]
    if full_lines:
        new_board = np.delete(board, full_lines, axis=0)
        padding = np.zeros((len(full_lines), COLUMNS), dtype=int)
        st.session_state.board = np.vstack([padding, new_board])
        st.session_state.score += len(full_lines) * 100

# 메인 UI
st.set_page_config(page_title="Streamlit Tetris", layout="centered")
st.title("🧱 Streamlit Tetris")

if 'board' not in st.session_state:
    init_game()

# 사이드바 컨트롤
with st.sidebar:
    st.header("Controls")
    col1, col2, col3 = st.columns(3)
    if col1.button("⬅️"): 
        if is_valid_move(st.session_state.current_piece, -1, 0): st.session_state.current_piece['x'] -= 1
    if col2.button("⬇️"): 
        if is_valid_move(st.session_state.current_piece, 0, 1): st.session_state.current_piece['y'] += 1
    if col3.button("➡️"): 
        if is_valid_move(st.session_state.current_piece, 1, 0): st.session_state.current_piece['x'] += 1
    
    if st.button("🔄 Rotate"):
        rotated = np.rot90(st.session_state.current_piece['shape'])
        if is_valid_move(st.session_state.current_piece, 0, 0, rotated):
            st.session_state.current_piece['shape'] = rotated
    
    if st.button("🆕 Reset Game"):
        init_game()
        st.rerun()

# 게임 로직 (자동 하강)
if not st.session_state.game_over:
    if is_valid_move(st.session_state.current_piece, 0, 1):
        st.session_state.current_piece['y'] += 1
    else:
        merge_piece()
    time.sleep(0.5) # 속도 조절
    st.rerun()

# 화면 그리기
board_display = st.session_state.board.copy()
p = st.session_state.current_piece
if p:
    for r, row in enumerate(p['shape']):
        for c, val in enumerate(row):
            if val and 0 <= p['y'] + r < ROWS:
                board_display[p['y'] + r, p['x'] + c] = p['color']

# HTML/CSS를 이용한 그리드 렌더링
grid_html = '<div style="display: grid; grid-template-columns: repeat(10, 25px); gap: 1px; background-color: #333; padding: 5px; width: fit-content; margin: auto;">'
for row in board_display:
    for cell in row:
        color = COLORS[cell-1] if cell > 0 else "#0e1117"
        grid_html += f'<div style="width: 25px; height: 25px; background-color: {color}; border-radius: 2px;"></div>'
grid_html += '</div>'

st.markdown(grid_html, unsafe_allow_html=True)
st.subheader(f"Score: {st.session_state.score}")

if st.session_state.game_over:
    st.error("GAME OVER!")
