import streamlit as st

st.title("광고 성과 MoM 대시보드")

st.write("✅ 실행 성공")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    st.write("파일 업로드 완료")
