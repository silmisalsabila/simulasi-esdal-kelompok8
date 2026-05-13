import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================================
# PENGATURAN HALAMAN
# =====================================================

st.set_page_config(
    page_title="Simulasi Batu Bara",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title("Simulasi Harga Sumber Daya Batu Bara")

st.markdown("""
### Kelompok 8

* Nadylah Agustinawati (10090224003)
* Silmi Yusniah Salsabila (10090224020)
* Siti Annisa Dewanty (10090224033)

### Mata Kuliah
Ekonomi Sumber Daya Alam dan Lingkungan

### Dosen Pengampu
Yuhka Sundaya S.E., M.Si.
""")

st.markdown("---")

# =====================================================
# SIDEBAR INPUT
# =====================================================

st.sidebar.header("Input Simulasi")

pasar = st.sidebar.selectbox(
    "Pilih Struktur Pasar",
    [
        "Persaingan",
        "Monopoli",
        "Oligopoli"
    ]
)

stok_awal = st.sidebar.slider(
    "Jumlah Stok Batu Bara",
    100,
    10000,
    5000
)

# =====================================================
# PARAMETER DASAR ANALISIS
# =====================================================

st.sidebar.subheader("Parameter Dasar Analisis")

harga_pasar = st.sidebar.slider(
    "Harga Pasar (Rp)",
    500000,
    10000000,
    2000000,
    step=100000
)

biaya_marginal = st.sidebar.slider(
    "Biaya Marginal (Rp)",
    100000,
    5000000,
    1000000,
    step=50000
)

muc_awal = st.sidebar.slider(
    "MUC Awal (Rp)",
    100000,
    5000000,
    1000000,
    step=50000
)

suku_bunga = st.sidebar.slider(
    "Suku Bunga (%)",
    1,
    20,
    5
)

# =====================================================
# PERHITUNGAN
# =====================================================

r = suku_bunga / 100

# Produksi berdasarkan struktur pasar

if pasar == "Persaingan":
    produksi = stok_awal * 0.15
elif pasar == "Monopoli":
    produksi = stok_awal * 0.10
else:
    produksi = stok_awal * 0.12

# Rumus harga simulasi

harga_simulasi = harga_pasar + biaya_marginal + (muc_awal * r)

# Waktu habis sumber daya

waktu_habis = stok_awal / produksi

# =====================================================
# SISA STOK TAHUNAN
# =====================================================

tahun = []
stok = []

sisa = stok_awal

for i in range(1, 11):

    tahun.append(i)

    sisa = sisa - produksi

    if sisa < 0:
        sisa = 0

    stok.append(sisa)

# =====================================================
# DATAFRAME
# =====================================================

df = pd.DataFrame({
    "Tahun": tahun,
    "Sisa Stok": stok
})

# =====================================================
# HASIL SIMULASI
# =====================================================

st.subheader("Hasil Simulasi")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Struktur Pasar",
        pasar
    )

with col2:
    st.metric(
        "Produksi",
        f"{produksi:,.0f}"
    )

with col3:
    st.metric(
        "Harga Simulasi",
        f"Rp {harga_simulasi:,.0f}"
    )

with col4:
    st.metric(
        "Waktu Habis",
        f"{waktu_habis:.1f} Tahun"
    )

# =====================================================
# PARAMETER DASAR ANALISIS
# =====================================================

st.subheader("Parameter Dasar Analisis")

parameter_df = pd.DataFrame({
    "Parameter": [
        "Harga Pasar",
        "Biaya Marginal",
        "MUC Awal",
        "Suku Bunga"
    ],
    "Nilai": [
        f"Rp {harga_pasar:,.0f}",
        f"Rp {biaya_marginal:,.0f}",
        f"Rp {muc_awal:,.0f}",
        f"{suku_bunga}%"
    ]
})

st.table(parameter_df)

# =====================================================
# TABEL DATA
# =====================================================

st.subheader("Sisa Stok Batu Bara")

st.dataframe(df)

# =====================================================
# GRAFIK STOK
# =====================================================

st.subheader("Grafik Penurunan Stok")

fig1 = px.line(
    df,
    x="Tahun",
    y="Sisa Stok",
    markers=True,
    title="Penurunan Stok Batu Bara"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# GRAFIK PRODUKSI
# =====================================================

produksi_df = pd.DataFrame({
    "Kategori": ["Produksi"],
    "Nilai": [produksi]
})

st.subheader("Grafik Produksi")

fig2 = px.bar(
    produksi_df,
    x="Kategori",
    y="Nilai",
    title="Jumlah Produksi"
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# ANALISIS GREEN PARADOX
# =====================================================

st.subheader("Analisis Green Paradox")

if suku_bunga > 10:
    st.warning("""
Tingkat suku bunga yang tinggi menyebabkan perusahaan
cenderung mempercepat ekstraksi sumber daya alam.

Kondisi ini mencerminkan Green Paradox,
yaitu eksploitasi sumber daya yang semakin cepat
sebelum nilainya menurun di masa depan.
""")

else:
    st.success("""
Tingkat suku bunga yang rendah menunjukkan
pengelolaan sumber daya yang lebih berkelanjutan.

Eksploitasi dilakukan lebih terkendali
sehingga stok sumber daya bertahan lebih lama.
""")

# =====================================================
# KESIMPULAN
# =====================================================

st.subheader("Kesimpulan")

st.write(f"""
Pada struktur pasar {pasar},
jumlah produksi sebesar {produksi:,.0f}
menyebabkan stok batu bara habis dalam
sekitar {waktu_habis:.1f} tahun.

Harga pasar sebesar Rp {harga_pasar:,.0f},
biaya marginal sebesar Rp {biaya_marginal:,.0f},
MUC awal sebesar Rp {muc_awal:,.0f},
dan suku bunga {suku_bunga}%
mempengaruhi harga simulasi serta kecepatan
eksploitasi sumber daya batu bara.
""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption("Project Simulasi Harga Batu Bara - Streamlit")
