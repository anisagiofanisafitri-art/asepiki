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
