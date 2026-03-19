import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("광고 성과 MoM 대시보드")

# 파일 업로드 (한 번만!)
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    st.success("파일 업로드 완료")

    df = pd.read_csv(uploaded_file, encoding='utf-8', header=1)

    # 숫자 변환
    cols = ['노출수','클릭수','총비용(VAT포함,원)','총 전환수','총 전환매출액(원)']
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

    # 그래프
    fig, ax = plt.subplots()
    ax.bar(summary['캠페인'], summary['ROAS(%)'])
    ax.set_title("캠페인별 ROAS")
    plt.xticks(rotation=45)

    st.pyplot(fig)

top_campaign = summary.sort_values('ROAS(%)', ascending=False).iloc[0]
worst_campaign = summary.sort_values('ROAS(%)').iloc[0]
avg_roas = summary['ROAS(%)'].mean()
total_cost = summary['총비용(VAT포함,원)'].sum()
total_revenue = summary['총 전환매출액(원)'].sum()
st.subheader("📊 자동 요약 리포트")

st.write(f"""
전체 광고비는 **{int(total_cost):,}원**,  
총 매출은 **{int(total_revenue):,}원**으로  
평균 ROAS는 **{avg_roas:.1f}%**입니다.

가장 성과가 좋은 캠페인은 **{top_campaign['캠페인']}**이며  
ROAS는 **{top_campaign['ROAS(%)']:.1f}%**입니다.

반면, 가장 성과가 낮은 캠페인은 **{worst_campaign['캠페인']}**으로  
개선 또는 중단 검토가 필요합니다.
""")

if avg_roas < 100:
    st.error("⚠️ 전체 광고가 적자 상태입니다. 구조 개선 필요")
elif avg_roas < 300:
    st.warning("📉 효율이 낮은 상태입니다. 최적화 필요")
else:
    st.success("🚀 효율이 우수합니다. 확장 검토 가능")
