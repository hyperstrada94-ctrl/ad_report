import streamlit as st

st.title("광고 성과 MoM 대시보드")

st.write("✅ 실행 성공")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    st.write("파일 업로드 완료")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("광고 성과 MoM 대시보드")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8', header=1)

    # 숫자형 변환
    cols = ['노출수','클릭수','총비용(VAT포함,원)','총 전환수','총 전환매출액(원)','총 광고수익률(%)']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 캠페인 기준 집계
    summary = df.groupby('캠페인').agg({
        '노출수':'sum',
        '클릭수':'sum',
        '총비용(VAT포함,원)':'sum',
        '총 전환수':'sum',
        '총 전환매출액(원)':'sum'
    }).reset_index()

    # KPI 계산
    summary['CTR(%)'] = (summary['클릭수'] / summary['노출수']) * 100
    summary['ROAS(%)'] = (summary['총 전환매출액(원)'] / summary['총비용(VAT포함,원)']) * 100

    st.subheader("캠페인 요약")
    st.dataframe(summary)

    # ROAS 그래프
    fig, ax = plt.subplots()
    ax.bar(summary['캠페인'], summary['ROAS(%)'])
    ax.set_title("캠페인별 ROAS")
    plt.xticks(rotation=45)

    st.pyplot(fig)
