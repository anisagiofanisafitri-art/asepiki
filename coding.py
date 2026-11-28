# ==========================================================
# UJIAN PRAKTIK LENGKAP (Praktik 1-4) - 1 FILE
#
# Cara pakai:
#   python ujian_praktik_lengkap.py 1 [file.csv]   -> Praktik 1
#   python ujian_praktik_lengkap.py 2 [file.csv]   -> Praktik 2
#   python ujian_praktik_lengkap.py 3              -> Praktik 3
#   python ujian_praktik_lengkap.py all [file.csv] -> Praktik 1, 2, 3 berurutan
#   streamlit run ujian_praktik_lengkap.py         -> Praktik 4 (dashboard)
#
# Praktik 1 & 2 butuh raw_dataset_desa.csv di folder yang sama
# (di Colab: /content/raw_dataset_desa.csv untuk Praktik 2).
# ==========================================================
import sys
import os


# ==========================================================
# PRAKTIK 1 - AUDIT DATA DAN ANONIMISASI DATA DESA
# ==========================================================
def praktik_1():
    # ==========================================================
    # UJIAN PRAKTIK 1 - AUDIT DATA DAN ANONIMISASI DATA DESA (TP 1.1)
    # ==========================================================
    import sys
    import pandas as pd

    FILE_INPUT = sys.argv[2] if len(sys.argv) > 2 else "raw_dataset_desa.csv"

    # 1. MEMBACA DATASET
    print("=== 1. MEMBACA DATASET ===")
    try:
        df = pd.read_csv(
            FILE_INPUT,
            dtype={"NIK": "string", "Nama_Lengkap": "string"}
        )
    except FileNotFoundError:
        sys.exit(f"File '{FILE_INPUT}' tidak ditemukan. Taruh di folder yang sama "
                 f"atau jalankan: python ujian_praktik_lengkap.py 1 path/ke/file.csv")
    print(df.head())
    print("\nJumlah baris dan kolom:", df.shape)

    # 2. AUDIT KELENGKAPAN DATA
    print("\n=== 2. AUDIT MISSING VALUES ===")
    missing = df.isnull().sum()
    print(missing)
    print("Total data kosong:", missing.sum())

    # 3. AUDIT KETERBARUAN DATA
    print("\n=== 3. AUDIT TIMELINESS ===")
    if "Tahun_Data" in df.columns:
        df["Tahun_Data"] = pd.to_numeric(df["Tahun_Data"], errors="coerce")
        print("Tahun terlama:", df["Tahun_Data"].min())
        print("Tahun terbaru:", df["Tahun_Data"].max())
    else:
        print("Kolom Tahun_Data tidak ada, audit timeliness dilewati.")

    # 4. ANONIMISASI NAMA
    print("\n=== 4. MASKING NAMA ===")
    def samarkan_nama(nama):
        if pd.isna(nama):
            return nama
        kata = str(nama).split()
        return " ".join(k[0].upper() + "*." for k in kata if k)

    if "Nama_Lengkap" in df.columns:
        df["Nama_Lengkap"] = df["Nama_Lengkap"].apply(samarkan_nama)

    # 5. ANONIMISASI NIK
    print("\n=== 5. MASKING NIK ===")
    def samarkan_nik(nik):
        if pd.isna(nik):
            return nik
        nik = str(nik).strip()
        if not nik.isdigit() or len(nik) != 16:
            return "FORMAT_NIK_TIDAK_VALID"
        return nik[:6] + "******" + nik[12:]

    if "NIK" in df.columns:
        df["NIK"] = df["NIK"].apply(samarkan_nik)

    # 6. MENAMPILKAN HASIL
    print("\n=== 6. HASIL DATA ANONIM ===")
    print(df.head())

    # 7. MENYIMPAN DATASET
    df.to_csv("dataset_desa_anonim.csv", index=False)
    print("\n=== SELESAI ===")
    print("Dataset berhasil disimpan!")
    print("Nama file: dataset_desa_anonim.csv")


# ==========================================================
# PRAKTIK 2 - DATA CLEANING DAN VALIDASI DATASET
# ==========================================================
def praktik_2():
    # ==========================================================
    # PRAKTIK 2 - DATA CLEANING DAN VALIDASI DATASET
    # Jalan di Google Colab, Termux, maupun laptop.
    # Pakai: python praktik2_cleaning_validasi.py [path_csv]
    # ==========================================================
    import os
    import sys
    import pandas as pd
    import numpy as np

    # Deteksi Colab: kalau iya pakai /content, kalau tidak pakai folder sekarang
    try:
        from google.colab import files as colab_files
        DI_COLAB = True
        FOLDER = "/content"
    except ImportError:
        DI_COLAB = False
        FOLDER = "."

    FILE_INPUT = (sys.argv[2] if len(sys.argv) > 2
                  else os.path.join(FOLDER, "raw_dataset_desa.csv"))

    # ==========================================
    # 1. MEMUAT DATASET
    # ==========================================
    print("=== PROGRAM DATA CLEANING DAN VALIDASI ===")
    try:
        # NIK wajib dibaca sebagai teks supaya tidak rusak jadi angka/ilmiah
        df = pd.read_csv(FILE_INPUT, dtype={"NIK": "string"})
    except FileNotFoundError:
        sys.exit(f"File '{FILE_INPUT}' tidak ditemukan.")
    print("\nDATA AWAL:")
    print(df.head())
    print("\nJumlah baris dan kolom:", df.shape)

    # ==========================================
    # 2. MEMERIKSA DATA KOSONG
    # ==========================================
    print("\n=== PEMERIKSAAN DATA KOSONG ===")
    print(df.isnull().sum())

    # ==========================================
    # 3. MEMBERSIHKAN FORMAT TEKS
    # ==========================================
    kolom_teks = ["Nama_Lengkap", "Pekerjaan", "Pendidikan", "Jenis_Kelamin"]
    for kolom in kolom_teks:
        if kolom in df.columns:
            df[kolom] = (
                df[kolom]
                .fillna("Tidak Diketahui")
                .astype(str)
                .str.strip()
                .str.title()
            )

    # ==========================================
    # 4. MENGHAPUS DATA GANDA
    # ==========================================
    jumlah_awal = len(df)
    if "NIK" in df.columns:
        # Hanya baris dengan NIK terisi yang dicek ganda,
        # supaya baris NIK kosong tidak ikut terhapus semua
        ganda = df["NIK"].notna() & df.duplicated(subset=["NIK"], keep="first")
        df = df[~ganda]
    print("\nData ganda yang dihapus:", jumlah_awal - len(df))

    # ==========================================
    # 5. MENANGANI DATA KOSONG PADA UMUR
    # ==========================================
    if "Umur" in df.columns:
        df["Umur"] = pd.to_numeric(df["Umur"], errors="coerce")
        median_umur = df["Umur"].median()
        df["Umur"] = df["Umur"].fillna(median_umur)

    # ==========================================
    # 6. VALIDASI DATA
    # ==========================================
    # Umur harus lebih dari 0 dan maksimal 100 tahun
    if "Umur" in df.columns:
        kondisi_umur = (df["Umur"] > 0) & (df["Umur"] <= 100)
    else:
        kondisi_umur = pd.Series(True, index=df.index)

    # Tahun data harus berupa angka
    if "Tahun_Data" in df.columns:
        df["Tahun_Data"] = pd.to_numeric(df["Tahun_Data"], errors="coerce")
        kondisi_tahun = df["Tahun_Data"].notna()
    else:
        kondisi_tahun = pd.Series(True, index=df.index)

    df["Status_Validasi"] = np.where(
        kondisi_umur & kondisi_tahun, "VALID", "TIDAK VALID"
    )

    # ==========================================
    # 7. MEMISAHKAN DATA VALID DAN ANOMALI
    # ==========================================
    df_valid = df[df["Status_Validasi"] == "VALID"].copy()
    df_anomali = df[df["Status_Validasi"] == "TIDAK VALID"].copy()

    # ==========================================
    # 8. MENYIMPAN HASIL
    # ==========================================
    path_valid = os.path.join(FOLDER, "dataset_valid.csv")
    path_anomali = os.path.join(FOLDER, "dataset_anomali.csv")
    df_valid.to_csv(path_valid, index=False)
    df_anomali.to_csv(path_anomali, index=False)

    # ==========================================
    # 9. MENAMPILKAN LAPORAN
    # ==========================================
    print("\n=== HASIL VALIDASI DATA ===")
    print("Jumlah data valid:", len(df_valid))
    print("Jumlah data anomali:", len(df_anomali))
    print("\nDATA VALID:")
    print(df_valid.head())
    print("\nDATA ANOMALI:")
    print(df_anomali.head())
    print("\nFile berhasil disimpan:")
    print("1.", path_valid)
    print("2.", path_anomali)

    # ==========================================
    # 10. MENGUNDUH HASIL (khusus Colab)
    # ==========================================
    if DI_COLAB:
        colab_files.download(path_valid)
        colab_files.download(path_anomali)


# ==========================================================
# PRAKTIK 3 - ANALISIS TREN DAN PREDIKSI REGRESI LINEAR
# ==========================================================
def praktik_3():
    # ==========================================================
    # PRAKTIK 3 - ANALISIS TREN DAN PREDIKSI REGRESI LINEAR
    # VOLUME SAMPAH DESA
    # ==========================================================
    import os
    import numpy as np
    import pandas as pd
    import matplotlib

    # Kalau tidak ada layar (Termux/server), pakai backend tanpa tampilan
    if not os.environ.get("DISPLAY") and "google.colab" not in str(os.sys.modules):
        if os.name != "nt" and os.uname().sysname != "Darwin":
            matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score

    # 1. MEMBUAT DATA HISTORIS
    data = {
        "Tahun": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
        "Volume_Sampah": [120, 135, 142, 160, 175, 190, 205]
    }
    df = pd.DataFrame(data)
    print("=== DATA HISTORIS VOLUME SAMPAH ===")
    print(df)

    # 2. MENENTUKAN VARIABEL X DAN Y
    X = df[["Tahun"]]
    y = df["Volume_Sampah"]

    # 3. MEMBUAT DAN MELATIH MODEL
    model = LinearRegression()
    model.fit(X, y)

    # 4. MENAMPILKAN PERSAMAAN REGRESI
    a = model.coef_[0]
    b = model.intercept_
    print("\n=== PERSAMAAN REGRESI LINEAR ===")
    print("Nilai a (slope):", round(a, 2))
    print("Nilai b (intercept):", round(b, 2))
    print(f"Persamaan: y = {a:.2f}x + {b:.2f}")

    # 5. MENGHITUNG NILAI R-SQUARED
    prediksi_historis = model.predict(X)
    r2 = r2_score(y, prediksi_historis)
    print("\n=== EVALUASI MODEL ===")
    print("Nilai R-Squared:", round(r2, 4))

    # 6. MENGHITUNG KESALAHAN MODEL (MSE)
    mse = mean_squared_error(y, prediksi_historis)
    print("Mean Squared Error (MSE):", round(mse, 2))

    # 7. MEMPREDIKSI TAHUN 2026-2028
    tahun_mendatang = pd.DataFrame({"Tahun": [2026, 2027, 2028]})
    hasil_prediksi = model.predict(tahun_mendatang)
    tahun_mendatang["Prediksi_Ton"] = hasil_prediksi
    print("\n=== HASIL PREDIKSI ===")
    print(tahun_mendatang.round(2))

    # 8. MEMBUAT GRAFIK TREN
    plt.figure(figsize=(10, 6))
    plt.scatter(df["Tahun"], df["Volume_Sampah"], label="Data Historis")
    plt.plot(df["Tahun"], prediksi_historis, linestyle="--", label="Garis Regresi")
    plt.scatter(
        tahun_mendatang["Tahun"], hasil_prediksi,
        marker="o", s=100, label="Prediksi 2026-2028"
    )
    plt.title("Analisis Tren dan Prediksi Volume Sampah Desa")
    plt.xlabel("Tahun")
    plt.ylabel("Volume Sampah (Ton)")
    plt.legend()
    plt.grid(True)

    # Selalu simpan ke file; tampilkan hanya kalau ada layar
    plt.savefig("grafik_tren_sampah.png", dpi=150, bbox_inches="tight")
    print("\nGrafik disimpan: grafik_tren_sampah.png")
    if matplotlib.get_backend().lower() != "agg":
        plt.show()

    # 9. MENAMPILKAN REKOMENDASI
    print("\n=== REKOMENDASI STRATEGIS ===")
    prediksi_2028 = hasil_prediksi[-1]
    print(f"Perkiraan volume sampah tahun 2028: {prediksi_2028:.2f} ton")
    print(
        "Pemerintah desa perlu merencanakan "
        "penambahan fasilitas pengelolaan sampah, "
        "memperkuat pemilahan sampah, dan "
        "meningkatkan edukasi masyarakat."
    )
    print("\nCatatan: Hasil prediksi merupakan perkiraan "
          "berdasarkan pola data historis, bukan kepastian.")


# ==========================================================
# PRAKTIK 4 - DASHBOARD INTERAKTIF PREDIKSI KONSUMSI ENERGI
# ==========================================================
def praktik_4():
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


# ==========================================================
# PENJALAN UTAMA
# ==========================================================
def _di_streamlit():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        try:
            return get_script_run_ctx(suppress_warning=True) is not None
        except TypeError:
            return get_script_run_ctx() is not None
    except Exception:
        return False


if _di_streamlit():
    praktik_4()
elif __name__ == "__main__":
    pilihan = sys.argv[1].lower() if len(sys.argv) > 1 else ""
    if pilihan == "1":
        praktik_1()
    elif pilihan == "2":
        praktik_2()
    elif pilihan == "3":
        praktik_3()
    elif pilihan == "all":
        praktik_1()
        praktik_2()
        praktik_3()
    elif pilihan == "4":
        print("Praktik 4 jalankan pakai: streamlit run ujian_praktik_lengkap.py")
    else:
        print("Pilih praktik: 1 | 2 | 3 | all  (Praktik 4: streamlit run ujian_praktik_lengkap.py)")
