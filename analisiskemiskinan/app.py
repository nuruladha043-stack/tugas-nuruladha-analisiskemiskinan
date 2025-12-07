import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb

# ===========================
# SETUP HALAMAN
# ===========================
st.set_page_config(
    page_title="📉 Dashboard Kemiskinan Indonesia",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📉 Dashboard Analisis Kemiskinan Indonesia")
st.caption("Data: Penduduk Miskin Per Provinsi 2024")

# ===========================
# UPLOAD DATA
# ===========================
uploaded_file = st.file_uploader("📂 Upload file Excel", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("📌 Data Preview")
    st.dataframe(df.head())

    # ===========================
    # PASTIKAN NAMA KOLOM SESUAI
    # ===========================
    df = df.rename(columns={
        df.columns[0]: "Provinsi",
        df.columns[1]: "Perkotaan_Sem1",
        df.columns[2]: "Perkotaan_Sem2",
        df.columns[4]: "Perdesaan_Sem1",
        df.columns[5]: "Perdesaan_Sem2",
        df.columns[7]: "Jumlah_Sem1",
        df.columns[8]: "Jumlah_Sem2"
    })

    # Convert dash (–) to NaN
    df = df.replace("-", None)

    # Convert numeric columns
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ===========================
    # DASHBOARD SECTION
    # ===========================
    st.subheader("📊 Grafik Jumlah Penduduk Miskin")

    # Bar Chart: Jumlah Semester 1
    fig1 = px.bar(
        df, x="Provinsi", y="Jumlah_Sem1",
        title="Jumlah Penduduk Miskin per Provinsi (Semester 1)",
        text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Bar Chart: Jumlah Semester 2
    fig2 = px.bar(
        df, x="Provinsi", y="Jumlah_Sem2",
        title="Jumlah Penduduk Miskin per Provinsi (Semester 2)",
        text_auto=True,
        color="Jumlah_Sem2"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Line Chart Perkotaan vs Perdesaan (Average)
    st.subheader("📈 Rata-rata Nasional: Perkotaan vs Perdesaan")

    mean_df = pd.DataFrame({
        "Kategori": ["Perkotaan Sem 1", "Perkotaan Sem 2",
                     "Perdesaan Sem 1", "Perdesaan Sem 2"],
        "Rata_Rata": [
            df["Perkotaan_Sem1"].mean(),
            df["Perkotaan_Sem2"].mean(),
            df["Perdesaan_Sem1"].mean(),
            df["Perdesaan_Sem2"].mean()
        ]
    })

    fig3 = px.line(
        mean_df, x="Kategori", y="Rata_Rata",
        markers=True, title="Rata-rata Nasional Penduduk Miskin"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ===========================
    # ANALISIS OTOMATIS (RULE-BASED)
    # ===========================
    st.subheader("📝 Analisis Otomatis")

    max_prov = df.loc[df["Jumlah_Sem1"].idxmax()]
    min_prov = df.loc[df["Jumlah_Sem1"].idxmin()]

    st.markdown(f"""
    ### 🔍 Insight Penting:
    - Provinsi dengan penduduk miskin **tertinggi** semester 1: **{max_prov['Provinsi']}** ({max_prov['Jumlah_Sem1']:.2f} ribu jiwa)
    - Provinsi dengan penduduk miskin **terendah** semester 1: **{min_prov['Provinsi']}** ({min_prov['Jumlah_Sem1']:.2f} ribu jiwa)
    - Perbedaan antara keduanya: **{max_prov['Jumlah_Sem1'] - min_prov['Jumlah_Sem1']:.2f} ribu jiwa**  
    """)

else:
    st.info("⬆️ Upload file Excel untuk memulai.")
