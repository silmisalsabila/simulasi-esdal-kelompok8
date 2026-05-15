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
# LOGO UNISBA
# =====================================================

logo = Image.open("logo_unisba.png")

col_logo, col_title = st.columns([1, 6])

with col_logo:
    st.image(logo, width=100)

with col_title:
    st.title("Analisis Intertemporal Sumber Daya Batu Bara")
    st.markdown("### Studi Kasus: PT Indo Tambangraya Megah (ITM)")

# =====================================================
# IDENTITAS KELOMPOK
# =====================================================

st.markdown("""
## Kelompok 8

- Nadylah Agustinawati (10090224003)  
- Silmi Yusniah Salsabila (10090224020)  
- Siti Annisa Dewanty (10090224033)  

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

tahun_simulasi = st.sidebar.slider(
    "Jumlah Tahun Simulasi",
    5,
    30,
    10
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
    """

elif pasar == "Monopoli":

    produksi = stok_awal * 0.10

    penjelasan_pasar = """
    Pada struktur pasar monopoli, produksi dikendalikan oleh satu perusahaan utama
    sehingga eksploitasi lebih terkendali untuk menjaga keuntungan jangka panjang.
    """

else:

    produksi = stok_awal * 0.12

    penjelasan_pasar = """
    Pada struktur pasar oligopoli, beberapa perusahaan besar saling bersaing
    dalam menentukan produksi dan harga.
    """

harga_simulasi = harga_pasar + biaya_marginal + (muc_awal * r)

waktu_habis = stok_awal / produksi

# =====================================================
# SIMULASI STOK DAN EKSTRAKSI
# =====================================================

tahun = []
stok = []
ekstraksi = []

sisa = stok_awal

for i in range(1, tahun_simulasi + 1):

    tahun.append(i)

    # ekstraksi per tahun
    if sisa > produksi:
        ekstraksi_tahun = produksi
    else:
        ekstraksi_tahun = sisa

    ekstraksi.append(ekstraksi_tahun)

    # update stok
    sisa -= ekstraksi_tahun

    if sisa < 0:
        sisa = 0

    stok.append(sisa)

# =====================================================
# DATAFRAME
# =====================================================

simulasi_df = pd.DataFrame({
    "Tahun": tahun,
    "Jumlah Ekstraksi": ekstraksi,
    "Sisa Stok": stok
})

# =====================================================
# HASIL SIMULASI
# =====================================================

st.subheader("Hasil Simulasi")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Struktur Pasar", pasar)

with col2:
    st.metric("Produksi/Tahun", f"{produksi:,.0f}")

with col3:
    st.metric("Harga Simulasi", f"Rp {harga_simulasi:,.0f}")

with col4:
    st.metric("Waktu Habis", f"{waktu_habis:.1f} Tahun")

st.info(penjelasan_pasar)

# =====================================================
# TABEL SIMULASI
# =====================================================

st.subheader("Tabel Ekstraksi dan Sisa Stok")

st.dataframe(simulasi_df, use_container_width=True)

# =====================================================
# GRAFIK STOK SUMBER DAYA
# =====================================================

st.subheader("Grafik Stok Sumber Daya")

fig1 = px.line(
    simulasi_df,
    x="Tahun",
    y="Sisa Stok",
    markers=True,
    title="Penurunan Stok Batu Bara",
    line_shape="linear"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# GRAFIK EKSTRAKSI PER TAHUN
# =====================================================

st.subheader("Grafik Jumlah Ekstraksi per Tahun")

fig_ekstraksi = px.bar(
    simulasi_df,
    x="Tahun",
    y="Jumlah Ekstraksi",
    title="Jumlah Ekstraksi Batu Bara per Tahun",
    text_auto=True
)

st.plotly_chart(fig_ekstraksi, use_container_width=True)

# =====================================================
# HOTELLING MODEL
# =====================================================

hotelling_tahun = np.arange(1, tahun_simulasi + 1)

hotelling_harga = [
    (harga_pasar * ((1 + r) ** t))
    for t in hotelling_tahun
]

hotelling_df = pd.DataFrame({
    "Tahun": hotelling_tahun,
    "Harga Hotelling": hotelling_harga
})

st.subheader("Model Hotelling")

st.dataframe(hotelling_df, use_container_width=True)

fig2 = px.line(
    hotelling_df,
    x="Tahun",
    y="Harga Hotelling",
    markers=True,
    title="Optimasi Hotelling"
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# GREEN PARADOX
# =====================================================

st.subheader("Green Paradox")

green_df = pd.DataFrame({
    "Tahun": hotelling_tahun,
    "Ekstraksi": np.linspace(produksi, produksi * 1.5, tahun_simulasi)
})

fig3 = px.line(
    green_df,
    x="Tahun",
    y="Ekstraksi",
    markers=True,
    title="Green Paradox"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# KESIMPULAN
# =====================================================

st.subheader("Kesimpulan")

st.write(f"""
Pada studi kasus PT Indo Tambangraya Megah,
struktur pasar {pasar} menghasilkan produksi sebesar {produksi:,.0f}
per tahun dengan estimasi stok habis dalam {waktu_habis:.1f} tahun.

Grafik stok sumber daya menunjukkan penurunan cadangan batu bara
seiring meningkatnya aktivitas ekstraksi.

Model Hotelling menunjukkan bahwa harga sumber daya
akan meningkat seiring waktu, sedangkan Green Paradox
menunjukkan potensi percepatan eksploitasi akibat
ekspektasi kenaikan harga di masa depan.
""")

st.markdown("---")
st.caption("Analisis Intertemporal Sumber Daya Batu Bara - Universitas Islam Bandung")
