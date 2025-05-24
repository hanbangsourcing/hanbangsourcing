# 한방소싱 v1.1 PRO - 루미 제작 웹앱 (Streamlit 기반)

import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="한방소싱 v1.1 PRO", layout="centered")
st.title("📦 한방소싱 v1.1 PRO")
st.caption("왕초보도 한 방에 도매꾹 → 쿠팡 수익화까지!")

keyword = st.text_input("🔍 소싱 키워드를 입력하세요:", "양말")

dummy_top100 = ["아치형 깔창", "꽃무늬 양산", "스판 반바지 3종", "범유다 팬츠", "미세먼지 마스크"]

def get_naver_related_keywords(keyword):
    try:
        url = f"https://ac.search.naver.com/nx/ac?q={keyword}&q_enc=utf-8&st=100&r_format=json&r_enc=utf-8"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        data = res.json()
        return [item[0] for item in data["items"][0]] if data["items"] else ["데이터 없음"]
    except:
        return ["데이터 없음"]

def calculate_margin(cost_price, selling_price, fee=0.13, shipping=2500):
    try:
        cost_price = int(cost_price)
        selling_price = int(selling_price)
        margin = selling_price - cost_price - shipping - (selling_price * fee)
        margin_rate = (margin / selling_price) * 100
        return round(margin, 2), round(margin_rate, 1)
    except:
        return 0, 0

# 👉 향후 쿠팡 연동 시 아래 함수 추가 예정
# def get_coupang_prices(keyword):
#     ...

if st.button("📊 분석 시작"):
    st.subheader("✅ 연관 키워드 (네이버 Suggest API 기준)")
    related_keywords = get_naver_related_keywords(keyword)
    st.write(related_keywords)

    st.subheader("🔥 일체형 탑백 키워드")
    st.write(dummy_top100)

st.subheader("💰 마진 리터")
cost = st.text_input("도매가 입력(원)", "3000")
sell = st.text_input("판매가 입력(원)", "9900")

if st.button("📈 마진 계산하기"):
    margin_won, margin_percent = calculate_margin(cost, sell)
    st.success(f"예상 마진: {margin_won}원 / 마진율: {margin_percent}%")

if st.button("📝 결과 메모장 저장"):
    related_keywords = get_naver_related_keywords(keyword)
    margin_won, margin_percent = calculate_margin(cost, sell)
    memo = f"[한방소싱 키워드 분석 결과 - PRO]

"
    memo += f"▶ 입력 키워드: {keyword}

"
    memo += "▶ 네이버 연관 키워드:
" + "
".join(related_keywords) + "

"
    memo += "▶ 도매꾹 탑백 키워드:
" + "
".join(dummy_top100) + "

"
    memo += f"▶ 마진 계산 결과:
도매가: {cost}원
판매가: {sell}원
예상 마진: {margin_won}원
마진율: {margin_percent}%"
    st.download_button("📁 메모장 다운로드", memo, file_name="hanbangsourcing_PRO_result.txt")