
# 한방소싱 v1.2 - 실전 자동분석 + 상품명 생성기 (PRO 고정 기능)
import streamlit as st
import requests
from bs4 import BeautifulSoup

# 페이지 설정
st.set_page_config(page_title="한방소싱 v1.2", layout="centered")
st.title("📦 한방소싱 v1.2 🔍")
st.caption("왕초보도 한방에 도매꾹 → 쿠팡 수익화까지! (PRO 고정 기능)")

# 입력
keyword = st.text_input("🔎 소싱 키워드를 입력하세요:", "어린이 장화")

# 도매꾹 샘플 탑백
dummy_top100 = ["아치형 깔창", "꽃무늬 양산", "스판 반바지 3종", "범유다 팬츠", "미세먼지 마스크"]

# 네이버 연관 키워드
def get_naver_related_keywords(keyword):
    try:
        url = f"https://suggest-bar.daum.net/suggest?id=shopping&q={keyword}"
        response = requests.get(url)
        if response.ok and "[" in response.text:
            raw = eval(response.text.split("=", 1)[-1].strip())
            return raw[1] if isinstance(raw, list) and len(raw) > 1 else ["데이터 없음"]
        return ["데이터 없음"]
    except:
        return ["데이터 없음"]

# 마진 계산
def calculate_margin(cost_price, selling_price, fee=0.13, shipping=2500):
    try:
        cost_price = int(cost_price)
        selling_price = int(selling_price)
        margin = selling_price - cost_price - shipping - int(selling_price * fee)
        margin_rate = (margin / selling_price) * 100
        return round(margin), round(margin_rate, 1)
    except:
        return 0, 0

# 상품명 및 키워드 생성기
def generate_title_keywords(keyword):
    title = f"프리미엄 {keyword} 특가 모음전"
    words = [f"{keyword} 추천", f"{keyword} 인기", f"{keyword} 저렴한", f"{keyword} 선물용"]
    return title, words

# 자동 분석 실행
if keyword:
    st.subheader("✅ 연관 키워드 (네이버 기준)")
    related_keywords = get_naver_related_keywords(keyword)
    st.write(related_keywords)

    st.subheader("🔥 일체형 탑백 키워드")
    st.write(dummy_top100)

    st.subheader("🧠 쿠팡용 상품명 및 요약 키워드")
    title, keywords = generate_title_keywords(keyword)
    st.markdown(f"- 🛍️ 상품명: **{title}**")
    st.markdown(f"- 🔑 키워드: " + ", ".join(keywords))

    st.subheader("💰 마진 리터")
    cost = st.text_input("도매가 입력 (원)", "3000")
    sell = st.text_input("판매가 입력 (원)", "9900")
    if st.button("📈 마진 계산하기"):
        margin_won, margin_percent = calculate_margin(cost, sell)
        st.success(f"예상 마진: {margin_won}원 / 마진율: {margin_percent}%")

    if st.button("📝 결과 메모장 저장"):
        memo = f"[한방소싱 자동 분석 결과]

"
        memo += f"▶ 입력 키워드: {keyword}

"
        memo += "▶ 네이버 연관 키워드:
" + "\n".join(related_keywords) + "\n\n"
        memo += "▶ 도매꾹 탑백 키워드:
" + "\n".join(dummy_top100) + "\n\n"
        memo += f"▶ 쿠팡용 상품명: {title}\n▶ 키워드: {', '.join(keywords)}\n\n"
        margin_won, margin_percent = calculate_margin(cost, sell)
        memo += f"▶ 마진 계산 결과:\n도매가: {cost}원\n판매가: {sell}원\n예상 마진: {margin_won}원\n마진율: {margin_percent}%"
        st.download_button("📁 메모장 다운로드", memo, file_name="한방소싱_결과_v1.2.txt")
