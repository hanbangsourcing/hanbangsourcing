
# 한방소싱 v1.1 - 루미 제작 웹앱 (네이버 Suggest API 기반)

import streamlit as st
import requests

# 앱 제목
st.set_page_config(page_title="한방소싱 v1.1", layout="centered")
st.title("📦 한방소싱 v1.1")
st.caption("왕초보도 한 방에 도매꾹 → 쿠팡 수익화까지!")

# 키워드 입력
keyword = st.text_input("🔍 소싱 키워드를 입력하세요:", "젤리")

# 도매꾹 탑백 키워드 샘플 (고정값)
dummy_top100 = ["아치형 깔창", "꽃무늬 양산", "스판 반바지 3종", "범유다 팬츠", "미세먼지 마스크"]

# 네이버 Suggest API 연관 키워드 함수 (개선된 방식)
def get_naver_related_keywords(keyword):
    try:
        url = f"https://ac.search.naver.com/nx/ac?q={keyword}&con=shopping&frm=nv&ans=1&r_format=json"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return [item[0] for item in result.get("items", [])[0]] or ["(연관 키워드 없음)"]
        else:
            return ["(요청 실패)"]
    except:
        return ["(에러 발생)"]

# 쿠팡 가격 마진 계산 함수 (간단한 예시)
def calculate_margin(cost_price, selling_price, fee=0.13, shipping=2500):
    try:
        cost_price = int(cost_price)
        selling_price = int(selling_price)
        margin = selling_price - cost_price - shipping - (selling_price * fee)
        margin_rate = (margin / selling_price) * 100
        return round(margin, 2), round(margin_rate, 1)
    except:
        return 0, 0

# 실행 버튼
if st.button("📊 분석 시작"):
    st.subheader("✅ 연관 키워드 (네이버 Suggest API 기준)")
    related_keywords = get_naver_related_keywords(keyword)
    st.write(related_keywords)

    st.subheader("🔥 일체형 탑백 키워드")
    st.write(dummy_top100)

# 마진 계산기
st.subheader("💰 마진 리터")
cost = st.text_input("도매가 입력(원)", "3000")
sell = st.text_input("판매가 입력(원)", "9900")

if st.button("📈 마진계산하기"):
    margin_won, margin_percent = calculate_margin(cost, sell)
    st.success(f"예상 마진: {margin_won}원 / 마진율: {margin_percent}%")

# 메모장 형식 결과 저장
if st.button("📝 결과 메모장 저장"):
    related_keywords = get_naver_related_keywords(keyword)
    margin_won, margin_percent = calculate_margin(cost, sell)
    memo = f"[한방소싱 키워드 분석 결과]\n\n"
    memo += f"▶ 입력 키워드: {keyword}\n\n"
    memo += "▶ 네이버 연관 키워드:\n" + "\n".join(related_keywords) + "\n\n"
    memo += "▶ 도매꾹 탑백 키워드:\n" + "\n".join(dummy_top100) + "\n\n"
    memo += f"▶ 마진 계산 결과:\n도매가: {cost}원\n판매가: {sell}원\n예상 마진: {margin_won}원\n마진율: {margin_percent}%"
    st.download_button("📁 메모장 다운로드", memo, file_name="한방소싱_결과.txt")
