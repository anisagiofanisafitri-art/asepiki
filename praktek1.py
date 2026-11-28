# ==========================================================
# UJIAN PRAKTIK 1 - AUDIT DATA DAN ANONIMISASI DATA DESA (TP 1.1)
# ==========================================================
import sys
import pandas as pd

FILE_INPUT = sys.argv[1] if len(sys.argv) > 1 else "raw_dataset_desa.csv"

# 1. MEMBACA DATASET
print("=== 1. MEMBACA DATASET ===")
try:
    df = pd.read_csv(
        FILE_INPUT,
        dtype={"NIK": "string", "Nama_Lengkap": "string"}
    )
except FileNotFoundError:
    sys.exit(f"File '{FILE_INPUT}' tidak ditemukan. Taruh di folder yang sama "
             f"atau jalankan: python praktik1_anonimisasi.py path/ke/file.csv")
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
