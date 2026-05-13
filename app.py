import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================================
# PENGATURAN HALAMAN
# =====================================================

st.set_page_config(
    page_title="Analisis Intertemporal Sumber Daya Batu Bara",
    layout="wide"
)

# =====================================================
# HEADER (LOGO + JUDUL)
# =====================================================

col_logo, col_title = st.columns([1, 6])

with col_logo:
    st.image("logo_unisba.png", width=90)

with col_title:
    st.title("Analisis Intertemporal Sumber Daya Batu Bara")

st.markdown("""
### Studi Kasus: PT Indo Tambangraya Megah (ITM)

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
    ["Persaingan", "Monopoli", "Oligopoli"]
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
    Pada pasar persaingan, banyak perusahaan berproduksi
    sehingga eksploitasi sumber daya lebih tinggi.
    """

elif pasar == "Monopoli":
    produksi = stok_awal * 0.10
    penjelasan_pasar = """
    Pada pasar monopoli, produksi dikendalikan satu perusahaan
    sehingga eksploitasi lebih terkontrol.
    """

else:
    produksi = stok_awal * 0.12
    penjelasan_pasar = """
    Pada pasar oligopoli, beberapa perusahaan besar
    saling bersaing dalam produksi dan harga.
    """

harga_simulasi = harga_pasar + biaya_marginal + (muc_awal * r)

waktu_habis = stok_awal / produksi

# =====================================================
# SIMULASI STOK
# =====================================================

tahun = []
stok = []

sisa = stok_awal

for i in range(1, 11):
    tahun.append(i)
    sisa -= produksi
    if sisa < 0:
        sisa = 0
    stok.append(sisa)

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
    st.metric("Struktur Pasar", pasar)

with col2:
    st.metric("Produksi", f"{produksi:,.0f}")

with col3:
    st.metric("Harga Simulasi", f"Rp {harga_simulasi:,.0f}")

with col4:
    st.metric("Waktu Habis", f"{waktu_habis:.1f} Tahun")

st.info(penjelasan_pasar)

# =====================================================
# GRAFIK STOK
# =====================================================

fig1 = px.line(
    stok_df,
    x="Tahun",
    y="Sisa Stok",
    markers=True,
    title="Penurunan Stok Batu Bara"
)

st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# HOTELLING MODEL
# =====================================================

hotelling_tahun = np.arange(1, 11)
hotelling_harga = [harga_pasar * ((1 + r) ** t) for t in hotelling_tahun]

hotelling_df = pd.DataFrame({
    "Tahun": hotelling_tahun,
    "Harga Hotelling": hotelling_harga
})

st.subheader("Model Hotelling")
st.dataframe(hotelling_df)

fig2 = px.line(
    hotelling_df,
    x="Tahun",
    y="Harga Hotelling",
    markers=True,
    title="Optimasi Hotelling"
)

st.plotly_chart(fig2, use_container_width=True)

st.write("""
Model Hotelling menjelaskan bahwa harga sumber daya tidak terbarukan
akan meningkat seiring waktu sesuai tingkat suku bunga.
""")

# =====================================================
# GREEN PARADOX
# =====================================================

st.subheader("Green Paradox")

green_df = pd.DataFrame({
    "Tahun": hotelling_tahun,
    "Ekstraksi": np.linspace(produksi, produksi * 1.5, 10)
})

fig3 = px.line(
    green_df,
    x="Tahun",
    y="Ekstraksi",
    markers=True,
    title="Green Paradox"
)

st.plotly_chart(fig3, use_container_width=True)

if suku_bunga > 10:
    st.warning("""
Suku bunga tinggi → percepatan eksploitasi sumber daya.
Fenomena ini disebut Green Paradox.
""")
else:
    st.success("""
Suku bunga rendah → eksploitasi lebih stabil dan berkelanjutan.
""")

# =====================================================
# KESIMPULAN
# =====================================================

st.subheader("Kesimpulan")

st.write(f"""
Pada studi kasus PT Indo Tambangraya Megah,
struktur pasar {pasar} menghasilkan produksi {produksi:,.0f}
dengan estimasi stok habis {waktu_habis:.1f} tahun.

Model Hotelling menunjukkan kenaikan harga dari waktu ke waktu,
sedangkan Green Paradox menunjukkan dampak kebijakan suku bunga
terhadap percepatan eksploitasi sumber daya.
""")

st.markdown("---")
st.caption("Analisis Intertemporal Sumber Daya Batu Bara - Streamlit | UNISBA")
