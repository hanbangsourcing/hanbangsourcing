# 한방소싱 v1.2 - 루미 제작 웹앱 (Streamlit 기반)

import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# 앱 제목
st.set_page_config(page_title="한방소싱 v1.2", layout="centered")
st.title("📦 한방소싱 v1.2")
st.caption("왕초보도 한 방에 도매꾹 → 쿠팡 → 수익화까지!")

# 키워드 입력
keyword = st.text_input("🔍 소싱 키워드를 입력하세요:", "양말")

# 도매꾹 탑백 키워드 샘플
dummy_top100 = ["아치형 깔창", "꽃무늬 양산", "스판 반바지 3종", "범유다 팬츠", "미세먼지 마스크"]

# 네이버 Suggest 기반 연관 검색어
@st.cache_data
def get_naver_related_keywords(keyword):
    try:
        url = f"https://ac.search.naver.com/nx/ac?q={keyword}&q_enc=utf-8&st=100&r_format=json"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        items = res.json()['items'][0]
        return [v[0] for v in items] if items else ["(데이터 없음)"]
    except:
        return ["(에러 발생)"]

# 쿠팡 검색결과 수 (상품 수 + 최저가)
@st.cache_data
def get_coupang_data(keyword):
    try:
        url = f"https://www.coupang.com/np/search?q={keyword}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 검색 결과 수 추출
        product_count_text = soup.select_one(".search-product-result strong")
        product_count = product_count_text.get_text(strip=True) if product_count_text else "(불러오기 실패)"

        # 최저가 추출
        price_tags = soup.select(".price-value")
        prices = [int(re.sub(r"[^0-9]", "", p.get_text())) for p in price_tags if p.get_text().strip()]
        min_price = f"{min(prices):,}원" if prices else "(없음)"

        return product_count, min_price
    except:
        return "(에러)", "(에러)"

# 마진 계산기
@st.cache_data
def calculate_margin(cost_price, selling_price, fee=0.13, shipping=2500):
    try:
        cost_price = int(cost_price)
        selling_price = int(selling_price)
        margin = selling_price - cost_price - shipping - int(selling_price * fee)
        margin_rate = (margin / selling_price) * 100
        return round(margin), round(margin_rate, 1)
    except:
        return 0, 0

# 실행 버튼
if st.button("📊 분석 시작"):
    st.subheader("✅ 연관 키워드 (네이버 Suggest API 기준)")
    related = get_naver_related_keywords(keyword)
    st.write(related)

    st.subheader("🔥 일체형 탑백 키워드")
    st.write(dummy_top100)

    st.subheader("🛒 쿠팡 검색 결과 요약")
    coupang_result, min_price = get_coupang_data(keyword)
    st.write(f"상품 수: {coupang_result}")
    st.write(f"최저가: {min_price}")

# 마진 계산기 UI
st.subheader("💰 마진 리터")
cost = st.text_input("도매가 입력(원)", "3000")
sell = st.text_input("판매가 입력(원)", "9900")
if st.button("📈 마진 계산하기"):
    margin_won, margin_rate = calculate_margin(cost, sell)
    st.success(f"예상 마진: {margin_won}원 / 마진율: {margin_rate}%")

# 메모장 다운로드
if st.button("📝 결과 메모장 저장"):
    related = get_naver_related_keywords(keyword)
    coupang_result, min_price = get_coupang_data(keyword)
    margin_won, margin_rate = calculate_margin(cost, sell)
    memo = f"[한방소싱 키워드 분석 결과]\n\n"
    memo += f"▶ 입력 키워드: {keyword}\n\n"
    memo += "▶ 네이버 연관 키워드:\n" + "\n".join(related) + "\n\n"
    memo += "▶ 도매꾹 탑백 키워드:\n" + "\n".join(dummy_top100) + "\n\n"
    memo += f"▶ 쿠팡 검색 결과:\n상품 수: {coupang_result}\n최저가: {min_price}\n\n"
    memo += f"▶ 마진 계산:\n도매가: {cost}원 / 판매가: {sell}원\n예상 마진: {margin_won}원 / 마진율: {margin_rate}%"
    st.download_button("📁 메모장 다운로드", memo, file_name="한방소싱_분석결과_v1.2.txt")
