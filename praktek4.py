# ==========================================================
# PRAKTIK 4 - DASHBOARD INTERAKTIF PREDIKSI KONSUMSI ENERGI
# Jalankan: streamlit run praktik4_dashboard_energi.py
# ==========================================================
import streamlit as st
import pandas as pd
import plotly.express as px


def tampil_chart(fig):
    """Kompatibel dengan Streamlit lama dan baru."""
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


def tampil_tabel(data):
    try:
        st.dataframe(data, width="stretch")
    except TypeError:
        st.dataframe(data, use_container_width=True)


# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Dashboard Energi Daerah",
    page_icon="⚡",
    layout="wide"
)

# 2. JUDUL DASHBOARD
st.title("Dashboard Prediksi Konsumsi Energi Daerah")
st.caption("Visualisasi Data dan Prediksi untuk Mendukung Keputusan Publik")
st.markdown("---")

# 3. MEMBUAT DATASET
data = {
    "Tahun": [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027],
    "Konsumsi_Energi_MW": [120, 135, 150, 170, 195, 220, 245, 275],
    "Status": [
        "Historis", "Historis", "Historis", "Historis", "Historis",
        "Prediksi", "Prediksi", "Prediksi"
    ]
}
df = pd.DataFrame(data)

# 4. FILTER INTERAKTIF
st.sidebar.header("Filter Dashboard")

pilihan_status = st.sidebar.multiselect(
    "Pilih Status Data:",
    options=list(df["Status"].unique()),
    default=list(df["Status"].unique())
)

pilihan_tahun = st.sidebar.slider(
    "Pilih Rentang Tahun:",
    min_value=int(df["Tahun"].min()),
    max_value=int(df["Tahun"].max()),
    value=(int(df["Tahun"].min()), int(df["Tahun"].max()))
)

df_filter = df[
    (df["Status"].isin(pilihan_status)) &
    (df["Tahun"] >= pilihan_tahun[0]) &
    (df["Tahun"] <= pilihan_tahun[1])
]

# 5. ANGKA RINGKASAN
st.subheader("Ringkasan Data")
kolom1, kolom2, kolom3 = st.columns(3)

if not df_filter.empty:
    kolom1.metric("Konsumsi Tertinggi", f"{df_filter['Konsumsi_Energi_MW'].max()} MW")
    kolom2.metric("Konsumsi Terendah", f"{df_filter['Konsumsi_Energi_MW'].min()} MW")
    kolom3.metric("Rata-rata Konsumsi", f"{df_filter['Konsumsi_Energi_MW'].mean():.2f} MW")
else:
    st.warning("Tidak ada data yang sesuai dengan filter.")

st.markdown("---")

# 6. LINE CHART
st.subheader("Grafik Tren Konsumsi Energi")
if not df_filter.empty:
    grafik_garis = px.line(
        df_filter,
        x="Tahun",
        y="Konsumsi_Energi_MW",
        color="Status",
        markers=True,
        title="Tren Konsumsi Energi Daerah",
        labels={"Tahun": "Tahun", "Konsumsi_Energi_MW": "Konsumsi Energi (MW)"}
    )
    grafik_garis.update_yaxes(rangemode="tozero")  # skala jujur
    tampil_chart(grafik_garis)

# 7. BAR CHART
st.subheader("Perbandingan Konsumsi Energi")
if not df_filter.empty:
    grafik_batang = px.bar(
        df_filter,
        x="Tahun",
        y="Konsumsi_Energi_MW",
        color="Status",
        title="Perbandingan Konsumsi Energi Setiap Tahun",
        labels={"Tahun": "Tahun", "Konsumsi_Energi_MW": "Konsumsi Energi (MW)"}
    )
    grafik_batang.update_yaxes(rangemode="tozero")
    tampil_chart(grafik_batang)

# 8. TABEL DATA
st.subheader("Tabel Dataset")
tampil_tabel(df_filter)

# 9. CATATAN ETIKA DATA
st.subheader("Catatan Etika dan Integritas Data")
st.info(
    "Data historis dan prediksi harus dibedakan dengan jelas. "
    "Grafik menggunakan skala sumbu Y yang dimulai dari nol agar tidak "
    "menimbulkan kesan perubahan yang berlebihan."
)
st.warning(
    "Data tahun 2025–2027 merupakan data prediksi simulasi untuk latihan, "
    "bukan angka resmi konsumsi energi daerah."
)
st.write("Sumber data: Dataset simulasi pembelajaran Informatika MA Nurur Rahmah.")

# 10. REKOMENDASI KEPUTUSAN STRATEGIS
st.subheader("Rekomendasi Keputusan Strategis")
st.success(
    "Pemerintah daerah perlu merencanakan peningkatan kapasitas energi "
    "terbarukan, mengembangkan Pembangkit Listrik Tenaga Surya (PLTS), "
    "dan melakukan penghematan energi."
)
st.markdown("---")

# 11. PENUTUP
st.caption("Dashboard Informatika Kelas XII - MA Nurur Rahmah")
st.caption("Prinsip: Jujur, Transparan, dan Bertanggung Jawab dalam Menyajikan Data.")
