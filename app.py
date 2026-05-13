import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

# =====================================================
# PENGATURAN HALAMAN
# =====================================================

st.set_page_config(
    page_title="Analisis Intertemporal Sumber Daya Batu Bara",
    layout="wide"
)

# =====================================================
# LOAD LOGO
# =====================================================

# GANTI NAMA FILE SESUAI NAMA LOGO DI FOLDER KALIAN
logo = image.open("LOGO UNISBA.jpg")

# =====================================================
# HEADER
# =====================================================

col1, col2 = st.columns([1, 6])

with col1:
    st.image(logo, width=120)

with col2:

    st.title("Analisis Intertemporal Sumber Daya Batu Bara")

    st.markdown("""
    ### PT Indo Tambangraya Megah

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
# PERHITUNGAN DASAR
# =====================================================

r = suku_bunga / 100

if pasar == "Persaingan":

    produksi = stok_awal * 0.15

    penjelasan_pasar = """
    Pada struktur pasar persaingan, banyak perusahaan melakukan produksi
    sehingga tingkat eksploitasi sumber daya cenderung lebih tinggi.
    Harga ditentukan oleh mekanisme pasar dan perusahaan bertindak sebagai price taker.
    """

elif pasar == "Monopoli":

    produksi = stok_awal * 0.10

    penjelasan_pasar = """
    Pada struktur pasar monopoli, produksi dikendalikan oleh satu perusahaan utama.
    Perusahaan memiliki kekuatan menentukan harga sehingga produksi cenderung lebih rendah
    untuk menjaga keuntungan jangka panjang.
    """

else:

    produksi = stok_awal * 0.12

    penjelasan_pasar = """
    Pada struktur pasar oligopoli, hanya beberapa perusahaan besar yang menguasai pasar.
    Produksi dilakukan secara strategis karena setiap perusahaan mempertimbangkan
    keputusan pesaing dalam menentukan jumlah produksi dan harga.
    """

# Harga simulasi

harga_simulasi = harga_pasar + biaya_marginal + (muc_awal * r)

# Waktu habis

waktu_habis = stok_awal / produksi

# =====================================================
# DATA SIMULASI STOK
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
# DATAFRAME STOK
# =====================================================

stok_df = pd.DataFrame({
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
# ANALISIS STRUKTUR PASAR
# =====================================================

st.subheader("Analisis Struktur Pasar")

st.info(penjelasan_pasar)

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
# TABEL SISA STOK
# =====================================================

st.subheader("Sisa Stok Batu Bara")

st.dataframe(stok_df)

# =====================================================
# GRAFIK PENURUNAN STOK
# =====================================================

st.subheader("Grafik Penurunan Stok")

fig1 = px.line(
    stok_df,
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
# DATA HISTORIS PRODUKSI DAN HARGA
# =====================================================

st.subheader("Data Historis Produksi dan Harga Batu Bara")

historis_df = pd.DataFrame({
    "Tahun": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "Produksi": [28.5, 25.6, 21.8, 22.1, 23.4, 18.4, 18.2, 16.6],
    "Harga": [1040331, 1069758, 1486929, 1713690, 1348449, 1007442, 2103165, 4992204]
})

st.dataframe(historis_df)

# =====================================================
# GRAFIK HISTORIS PRODUKSI
# =====================================================

fig3 = px.line(
    historis_df,
    x="Tahun",
    y="Produksi",
    markers=True,
    title="Grafik Historis Produksi Batu Bara"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# GRAFIK HISTORIS HARGA
# =====================================================

fig4 = px.line(
    historis_df,
    x="Tahun",
    y="Harga",
    markers=True,
    title="Grafik Historis Harga Batu Bara"
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# MODEL HOTELLING
# =====================================================

st.subheader("Model Optimasi Hotelling")

hotelling_tahun = np.arange(1, 11)

hotelling_harga = []

for t in hotelling_tahun:

    harga_t = harga_pasar * ((1 + r) ** t)

    hotelling_harga.append(harga_t)

hotelling_df = pd.DataFrame({
    "Tahun": hotelling_tahun,
    "Harga Hotelling": hotelling_harga
})

st.dataframe(hotelling_df)

# =====================================================
# GRAFIK HOTELLING
# =====================================================

fig5 = px.line(
    hotelling_df,
    x="Tahun",
    y="Harga Hotelling",
    markers=True,
    title="Grafik Optimasi Hotelling"
)

st.plotly_chart(fig5, use_container_width=True)

st.write("""
Model Hotelling menjelaskan bahwa harga sumber daya tidak terbarukan
akan meningkat seiring waktu sesuai tingkat suku bunga.

Dalam simulasi ini, semakin tinggi suku bunga,
maka harga optimal batu bara di masa depan juga meningkat.
Hal tersebut mendorong perusahaan untuk mempercepat ekstraksi
agar memperoleh keuntungan lebih cepat.
""")

# =====================================================
# ANALISIS GREEN PARADOX
# =====================================================

st.subheader("Analisis Green Paradox")

green_df = pd.DataFrame({
    "Tahun": hotelling_tahun,
    "Ekstraksi": np.linspace(produksi, produksi * 1.5, 10)
})

fig6 = px.line(
    green_df,
    x="Tahun",
    y="Ekstraksi",
    markers=True,
    title="Grafik Green Paradox"
)

st.plotly_chart(fig6, use_container_width=True)

if suku_bunga > 10:

    st.warning("""
    Tingkat suku bunga yang tinggi menyebabkan perusahaan
    cenderung mempercepat ekstraksi sumber daya alam.

    Kondisi ini mencerminkan Green Paradox,
    yaitu eksploitasi sumber daya yang semakin cepat
    sebelum nilainya menurun di masa depan.

    Grafik menunjukkan adanya peningkatan ekstraksi
    seiring kenaikan ekspektasi harga sumber daya.
    """)

else:

    st.success("""
    Tingkat suku bunga yang rendah menunjukkan
    pengelolaan sumber daya yang lebih berkelanjutan.

    Eksploitasi dilakukan lebih terkendali
    sehingga stok sumber daya bertahan lebih lama.

    Grafik menunjukkan laju ekstraksi yang lebih stabil
    sehingga risiko Green Paradox lebih rendah.
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

Model Hotelling menunjukkan bahwa harga sumber daya
akan meningkat dari waktu ke waktu,
sedangkan Green Paradox menunjukkan risiko
percepatan eksploitasi akibat ekspektasi kenaikan harga
atau kebijakan lingkungan di masa depan.
""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption("Project Analisis Intertemporal Sumber Daya Batu Bara")
