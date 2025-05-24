import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="한방소싱 v1.1", layout="centered")
st.title("📦 한방소싱 v1.1 ∞")
st.caption("왕초보도 한 방에 도매꾹 → 쿠팡 수익화까지! (PRO 업그레이드)")

keyword = st.text_input("🔍 소싱 키워드를 입력하세요:", "어린이 양말")

if st.button("📑 분석 시작"):
    st.subheader("✅ 연관 키워드 (네이버 Suggest API 기준)")
    try:
        url = f"https://ac.search.naver.com/nx/ac?q={keyword}&q_enc=utf-8&st=100&r_format=json"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        items = res.json().get("items", [])[0]
        for idx, word in enumerate(items):
            st.write(f"{idx + 1} : {word[0]}")
    except:
        st.write("🔴 연관 키워드 불러오기 실패")

    st.subheader("🔥 일체형 탑백 키워드")
    dummy_top100 = ["아치형 깔창", "꽃무늬 양산", "스판 반바지 3종", "범유다 팬츠", "미세먼지 마스크"]
    for idx, val in enumerate(dummy_top100):
        st.write(f"{idx + 1} : {val}")

st.subheader("💰 마진 리터")
cost = st.text_input("도매가 입력(원)", "3000")
sell = st.text_input("판매가 입력(원)", "9900")

def calculate_margin(cost_price, selling_price, fee=0.13, shipping=2500):
    try:
        cost_price = int(cost_price)
        selling_price = int(selling_price)
        margin = selling_price - cost_price - shipping - int(selling_price * fee)
        margin_rate = (margin / selling_price) * 100
        return margin, round(margin_rate, 1)
    except:
        return 0, 0

if st.button("📈 마진 계산하기"):
    m, r = calculate_margin(cost, sell)
    st.success(f"예상 마진: {m}원 / 마진율: {r}%")

# 실전 가격 분석 블럭
st.subheader("💸 실전 가격 분석 블럭")

if st.button("🔎 가격 분석 실행"):
    st.write("🔧 현재는 쿠팡 자동 연결은 제한되어 있어요.")
    st.info("👉 직접 쿠팡에서 검색 후 상위 가격 데이터를 붙여 넣으면 자동 분석됩니다.")

    sample_prices = st.text_area("🔢 복사한 가격 데이터 붙여넣기 (숫자만 줄바꿈)", "9900
10800
9200
10500")
    try:
        prices = list(map(int, sample_prices.strip().splitlines()))
        if prices:
            st.write(f"📊 총 {len(prices)}개 상품 가격 분석:")
            st.write(f"🔹 평균가: {sum(prices)//len(prices)}원")
            st.write(f"🔹 최저가: {min(prices)}원")
            st.write(f"🔹 최고가: {max(prices)}원")
            st.write(f"💡 권장 판매가 제안: {int(sum(prices)//len(prices) * 0.97)}원 (경쟁력 고려)")
    except:
        st.warning("❗ 가격 숫자를 정확히 입력해주세요.")