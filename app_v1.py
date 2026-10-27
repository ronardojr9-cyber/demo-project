
import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="초록이의 숲",
    page_icon="🌳",
    layout="centered"
)

# 게임 데이터 초기화
if "name" not in st.session_state:
    st.session_state.name = "초록이"
if "exp" not in st.session_state:
    st.session_state.exp = 0
if "water" not in st.session_state:
    st.session_state.water = 50
if "sun" not in st.session_state:
    st.session_state.sun = 50
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "water_count" not in st.session_state:
    st.session_state.water_count = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "message" not in st.session_state:
    st.session_state.message = "나무를 키워보세요!"

# 성장 단계 계산
def get_tree():
    exp = st.session_state.exp

    if exp < 20:
        return "🫘", "씨앗", 1
    elif exp < 50:
        return "🌱", "새싹", 2
    elif exp < 100:
        return "🌿", "어린 나무", 3
    elif exp < 180:
        return "🌳", "튼튼한 나무", 4
    else:
        return "🌸🌳🌸", "전설의 꽃나무", 5

def add_history(action):
    st.session_state.history.append({
        "행동": action,
        "경험치": st.session_state.exp,
        "코인": st.session_state.coins
    })

# 화면 디자인
st.markdown("""
<style>
.stApp {
    background: linear-gradient(#e5f9e7, #ffffff);
}
h1, h2, h3 {
    text-align: center;
    color: #287a43;
}
.tree {
    text-align: center;
    font-size: 110px;
    padding: 25px;
    background: linear-gradient(#bdeeff 65%, #a4d683 65%);
    border-radius: 25px;
    margin: 15px 0;
}
.message {
    text-align: center;
    padding: 14px;
    background: #ffffff;
    border-radius: 15px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌳 초록이의 숲")
st.caption("나만의 작은 나무를 키우는 힐링 게임")

# 나무 이름
name = st.text_input(
    "✏️ 나무 이름",
    value=st.session_state.name,
    max_chars=12
)
st.session_state.name = name if name.strip() else "초록이"

tree_image, stage, level = get_tree()

st.subheader(f"{st.session_state.name}의 정원")

# 성장 이미지
st.markdown(
    f'<div class="tree">{tree_image}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"<h3>Lv.{level} · {stage}</h3>",
    unsafe_allow_html=True
)

st.progress(min(st.session_state.exp / 180, 1.0))
st.caption(f"성장 경험치: {st.session_state.exp} / 180")

# 상태 표시
col1, col2, col3 = st.columns(3)
col1.metric("💧 수분", f"{st.session_state.water}%")
col2.metric("☀️ 햇빛", f"{st.session_state.sun}%")
col3.metric("🪙 코인", st.session_state.coins)

st.divider()
st.subheader("🌼 나무 돌보기")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💧 물 주기", use_container_width=True):
        if st.session_state.water >= 100:
            st.session_state.message = "물이 충분해요!"
        else:
            st.session_state.water = min(
                100, st.session_state.water + 20
            )
            st.session_state.exp += 10
            st.session_state.coins += 5
            st.session_state.water_count += 1
            st.session_state.message = "💦 꿀꺽! 나무가 물을 마셨어요!"
            add_history("물 주기")
        st.rerun()

with col2:
    if st.button("☀️ 햇빛 주기", use_container_width=True):
        if st.session_state.sun >= 100:
            st.session_state.message = "햇빛이 충분해요!"
        else:
            st.session_state.sun = min(
                100, st.session_state.sun + 20
            )
            st.session_state.exp += 8
            st.session_state.coins += 3
            st.session_state.message = "☀️ 따뜻한 햇살을 받았어요!"
            add_history("햇빛 주기")
        st.rerun()

with col3:
    if st.button("🧪 비료 주기", use_container_width=True):
        if st.session_state.coins >= 20:
            st.session_state.coins -= 20
            st.session_state.exp += 25
            st.session_state.message = "✨ 비료 효과! 쑥쑥 자라요!"
            add_history("비료 주기")
        else:
            st.session_state.message = "코인이 20개 필요해요!"
        st.rerun()

st.markdown(
    f'<div class="message">{st.session_state.message}</div>',
    unsafe_allow_html=True
)

# 랜덤 이벤트
st.divider()
st.subheader("🎁 오늘의 행운")

if st.button("🎲 랜덤 선물 뽑기", use_container_width=True):
    reward = random.choice([5, 10, 15, 20, 30])
    st.session_state.coins += reward
    st.success(f"🎉 선물 상자에서 {reward}코인을 얻었어요!")
    add_history("랜덤 선물")

# 도감
st.divider()
st.subheader("📖 나무 성장 도감")

st.write("🫘 Lv.1 씨앗 — 경험치 0")
st.write("🌱 Lv.2 새싹 — 경험치 20")
st.write("🌿 Lv.3 어린 나무 — 경험치 50")
st.write("🌳 Lv.4 튼튼한 나무 — 경험치 100")
st.write("🌸 Lv.5 전설의 꽃나무 — 경험치 180")

# 활동 기록
with st.expander("📊 나의 성장 기록"):
    st.write(f"💧 물을 준 횟수: {st.session_state.water_count}회")
    st.write(f"⭐ 총 경험치: {st.session_state.exp}")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("아직 활동 기록이 없어요.")

# 초기화
st.divider()

if st.button("🔄 새로운 나무 키우기"):
    for key in [
        "exp", "water", "sun", "coins",
        "water_count", "history", "message"
    ]:
        del st.session_state[key]
    st.rerun()

st.caption("🌱 오늘도 초록이와 함께 성장해요!")
