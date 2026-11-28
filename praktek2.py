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

FILE_INPUT = (sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-")
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
