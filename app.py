import streamlit as st

st.set_page_config(page_title="한방소싱 v1.1", layout="centered")
st.title("📦 한방소싱 v1.1")
st.caption("왕초보도 한 방에 도매꾹 → 쿠팡 수익화까지! (PRO 업그레이드)")


# 🔍 키워드 입력
keyword = st.text_input("🔑 소싱 키워드를 입력하세요:", "귀여운 양말")


# ✅ 네이버 연관 검색어 (샘플)
if st.button("📊 분석 시작"):
    st.subheader("✅ 연관 키워드 (네이버 Suggest API 기준)")
    st.json([
        "귀여운 양말",
        "귀여운 양말 추천",
        "귀여운 양말 코디",
        "귀여운 양말 여자",
        "귀여운 양말 남자",
        "귀여운 양말 세트",
        "귀여운 양말 브랜드",
        "귀여운 양말 선물",
        "귀여운 양말 쇼핑몰",
        "귀여운 양말 파는 곳"
    ])

    st.subheader("🔥 일체형 탑백 키워드")
    st.json([
        "양말 추천",
        "귀여운 양말",
        "패션 양말 3종",
        "여성 양말 세트"
    ])


# 💸 마진 리터
st.subheader("💰 마진 리터")
cost = st.text_input("도매가 입력(원)", "3000")
sell = st.text_input("판매가 입력(원)", "9900")

if st.button("📈 마진 계산하기"):
    try:
        cost = int(cost)
        sell = int(sell)
        margin = sell - cost - 2500 - int(sell * 0.13)
        margin_rate = margin / sell * 100
        st.success(f"예상 마진: {margin}원 / 마진율: {margin_rate:.1f}%")
    except:
        st.error("숫자만 입력해주세요.")

# 🧮 실전 가격 분석 블럭
st.subheader("📦 실전 가격 분석 블럭")
sample_prices = st.text_area("📘 복사한 가격 데이터 붙여넣기 (숫자만 줄바꿈)", "9900\n9800\n8700\n11900\n8800")

if st.button("🔍 평균가 분석"):
    try:
        prices = [int(p.strip()) for p in sample_prices.strip().split("\n") if p.strip().isdigit()]
        avg_price = sum(prices) / len(prices)
        st.success(f"입력한 {len(prices)}건 평균 판매가: {round(avg_price)}원")
    except:
        st.error("가격 데이터가 올바르지 않습니다.")