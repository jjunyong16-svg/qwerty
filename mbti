import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="감성 MBTI 테스트",
    page_icon="✨",
    layout="centered"
)

# --- Custom CSS for Pastel Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #fdfcf0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        border: 2px solid #ffccbc;
        background-color: #ffffff;
        color: #5d4037;
        font-weight: bold;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ffccbc;
        color: white;
    }
    .question-text {
        font-size: 1.2rem;
        color: #5d4037;
        background-color: #fff9f5;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #ffab91;
    }
    .result-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border: 2px dashed #b2dfdb;
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Definition ---
questions = [
    {"q": "주말에 시간이 생겼을 때 당신은?", "type": "EI", "a": "친구들과 만나 즐겁게 수다를 떤다", "b": "집에서 혼자 책을 보거나 푹 쉰다"},
    {"q": "새로운 사람을 만났을 때 당신의 반응은?", "type": "EI", "a": "먼저 말을 걸고 분위기를 주도한다", "b": "상대방이 말을 걸어줄 때까지 기다린다"},
    {"q": "모임에서 당신의 에너지는?", "type": "EI", "a": "사람들과 어울릴수록 충전된다", "b": "집에 돌아왔을 때 비로소 편안함을 느낀다"},
    
    {"q": "숲을 볼 때 당신의 생각은?", "type": "SN", "a": "나무의 종류, 날씨, 현재의 풍경에 집중한다", "b": "숲 너머에 무엇이 있을지, 어떤 이야기가 숨겨져 있을지 상상한다"},
    {"q": "설명서를 읽을 때 당신은?", "type": "SN", "a": "적힌 순서대로 정확하게 따라 하려 한다", "b": "대충 훑어보고 감으로 먼저 시도해 본다"},
    {"q": "현실적인 문제에 직면했을 때?", "type": "SN", "a": "실제 경험과 사실에 기반하여 해결책을 찾는다", "b": "새로운 가능성이나 아이디어를 떠올려 본다"},
    
    {"q": "친구가 고민을 털어놓을 때 당신은?", "type": "TF", "a": "상황을 분석하고 현실적인 조언을 해준다", "b": "친구의 감정에 공감하고 위로를 건넨다"},
    {"q": "영화나 드라마를 볼 때?", "type": "TF", "a": "스토리의 논리성이나 개연성을 따진다", "b": "등장인물의 감정선에 깊이 몰입한다"},
    {"q": "일 처리를 할 때 가장 중요한 것은?", "type": "TF", "a": "공정성과 객관적인 결과", "b": "사람들 간의 관계와 조화"},
    
    {"q": "여행을 갈 때 당신은?", "type": "JP", "a": "시간별로 세부 일정을 미리 짜둔다", "b": "목적지만 정하고 발길 닿는 대로 움직인다"},
    {"q": "책상을 정리할 때 당신의 스타일은?", "type": "JP", "a": "항상 정해진 위치에 깔끔하게 정리되어 있다", "b": "편하게 쓸 수 있도록 자연스럽게 흐트러져 있다"},
    {"q": "갑작스러운 약속 제안이 왔을 때?", "type": "JP", "a": "정해진 계획이 틀어지는 것 같아 부담스럽다", "b": "오히려 신나고 새로운 즐거움으로 느껴진다"}
]

results_info = {
    "INTJ": {"theme": "미니멀 서재", "desc": "깊은 생각과 전략적인 삶을 즐기는 당신에게 어울리는 고요한 공간입니다."},
    "INTP": {"theme": "구름 위 작업실", "desc": "끝없는 호기심과 상상의 나래를 펼칠 수 있는 몽환적인 공간입니다."},
    "ENTJ": {"theme": "모던 오피스", "desc": "체계적이고 리더십 있는 당신의 아우라가 느껴지는 세련된 공간입니다."},
    "ENTP": {"theme": "다채로운 갤러리", "desc": "다양한 아이디어와 실험 정신이 돋보이는 활기찬 공간입니다."},
    "INFJ": {"theme": "포근한 찻집", "desc": "깊은 통찰력과 따뜻한 마음을 가진 당신을 위한 조용한 쉼터입니다."},
    "INFP": {"theme": "파스텔 수채화실", "desc": "부드러운 감성과 창의적인 예술가적 면모가 어울리는 공간입니다."},
    "ENFJ": {"theme": "해질녘 가든 파티", "desc": "사람들을 아끼고 화합을 이끄는 당신의 따뜻함이 담긴 공간입니다."},
    "ENFP": {"theme": "반짝이는 페스티벌", "desc": "밝은 에너지와 열정적인 당신의 매력을 듬뿍 담은 테마입니다."},
    "ISTJ": {"theme": "정갈한 한옥", "desc": "책임감 있고 원칙을 중시하는 당신의 차분함이 담긴 공간입니다."},
    "ISFJ": {"theme": "라벤더 들판", "desc": "헌신적이고 상냥한 당신을 편안하게 감싸주는 풍경입니다."},
    "ESTJ": {"theme": "정돈된 도서관", "desc": "명확하고 질서 정연한 당신의 추진력이 돋보이는 공간입니다."},
    "ESFJ": {"theme": "화사한 거실", "desc": "타인에게 베풀기를 좋아하는 당신의 정이 가득한 따뜻한 공간입니다."},
    "ISTP": {"theme": "빈티지 차고", "desc": "자유롭고 실용적인 감각을 지닌 당신의 아지트 같은 공간입니다."},
    "ISFP": {"theme": "비밀의 숲 하우스", "desc": "부드럽고 온화한 당신이 편안하게 머무를 수 있는 자연의 품입니다."},
    "ESTP": {"theme": "활기찬 스포츠 파크", "desc": "스릴을 즐기고 활동적인 당신의 에너지가 폭발하는 곳입니다."},
    "ESFP": {"theme": "컬러풀 시티 라이프", "desc": "즐거움을 찾아 떠나는 당신의 화려한 일상과 어울리는 테마입니다."}
}

# --- Logic ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

def select_answer(choice, q_type):
    # Update scores
    if q_type == "EI":
        if choice == 'a': st.session_state.scores["E"] += 1
        else: st.session_state.scores["I"] += 1
    elif q_type == "SN":
        if choice == 'a': st.session_state.scores["S"] += 1
        else: st.session_state.scores["N"] += 1
    elif q_type == "TF":
        if choice == 'a': st.session_state.scores["T"] += 1
        else: st.session_state.scores["F"] += 1
    elif q_type == "JP":
        if choice == 'a': st.session_state.scores["J"] += 1
        else: st.session_state.scores["P"] += 1
    
    st.session_state.step += 1

# --- UI Rendering ---
st.title("✨ 감성 MBTI 테스트")
st.write("나에게 어울리는 파스텔 톤 인생 테마는?")
st.divider()

if st.session_state.step < len(questions):
    # Current Question
    q_data = questions[st.session_state.step]
    
    # Progress Bar
    progress = (st.session_state.step) / len(questions)
    st.progress(progress)
    st.caption(f"질문 {st.session_state.step + 1} / {len(questions)}")
    
    st.markdown(f"<div class='question-text'>{q_data['q']}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(q_data['a']):
            select_answer('a', q_data['type'])
            st.rerun()
    with col2:
        if st.button(q_data['b']):
            select_answer('b', q_data['type'])
            st.rerun()

else:
    # Calculate Result
    s = st.session_state.scores
    mbti = ""
    mbti += "E" if s["E"] >= s["I"] else "I"
    mbti += "S" if s["S"] >= s["N"] else "N"
    mbti += "T" if s["T"] >= s["F"] else "F"
    mbti += "J" if s["J"] >= s["P"] else "P"
    
    result_data = results_info.get(mbti, {"theme": "미지의 공간", "desc": "당신은 아주 특별한 성향을 가지고 계시군요!"})
    
    st.balloons()
    st.markdown(f"""
        <div class='result-card'>
            <h3 style='color: #ff8a65;'>당신의 MBTI 결과는...</h3>
            <h1 style='font-size: 4rem; color: #5d4037;'>{mbti}</h1>
            <p style='font-size: 1.2rem; color: #8d6e63;'>추천 테마: <b>{result_data['theme']}</b></p>
            <hr style='border: 0.5px solid #eee;'>
            <p style='color: #6d4c41;'>{result_data['desc']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("테스트 다시 하기"):
        st.session_state.step = 0
        st.session_state.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("이 테스트는 단순 참고용으로 즐겨주세요. 당신의 모든 면을 담기엔 MBTI는 너무 작으니까요! 🌸")
