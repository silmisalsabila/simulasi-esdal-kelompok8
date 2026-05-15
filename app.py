import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

# =====================================================
# PENGATURAN HALAMAN
# =====================================================

st.set_page_config(
    page_title="Dashboard Analisis Batu Bara",
    layout="wide"
)

# =====================================================
# LOGO DAN HEADER
# =====================================================

logo = Image.open("logo_unisba.png")

col_logo, col_title = st.columns([1, 6])

with col_logo:
    st.image(logo, width=100)

with col_title:
    st.title("Dashboard Analisis Intertemporal Batu Bara")
    st.markdown("### Studi Kasus: PT Indo Tambangraya Megah (ITM)")

st.markdown("---")

# =====================================================
# IDENTITAS
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

stok_awal = st.sidebar.slider(
    "Jumlah Stok Awal",
    1000,
    50000,
    10000
)

tahun_simulasi = st.sidebar.slider(
    "Jumlah Tahun Simulasi",
    5,
    30,
    10
)

harga_pasar = st.sidebar.slider(
    "Harga Pasar (Rp)",
    500000,
    10000000,
    2000000,
    step=100000
)

suku_bunga = st.sidebar.slider(
    "Tingkat Diskonto (%)",
    1,
    20,
    5
)

produksi_awal = st.sidebar.slider(
    "Produksi Dasar",
    100,
    10000,
    1000
)

# =====================================================
# TINGKAT DISKONTO
# =====================================================

r = suku_bunga / 100

# =====================================================
# STRUKTUR PASAR BERDASARKAN TEORI
# =====================================================

struktur_pasar = {

    "Persaingan Sempurna": {
        "rasio_dasar": 1.2,
        "respon_harga": 0.00000004,
        "respon_diskonto": 0.50
    },

    "Monopoli": {
        "rasio_dasar": 0.8,
        "respon_harga": 0.00000002,
        "respon_diskonto": 0.20
    },

    "Oligopoli": {
        "rasio_dasar": 1.0,
        "respon_harga": 0.00000003,
        "respon_diskonto": 0.35
    }
}

# =====================================================
# DATA SIMULASI
# =====================================================

hasil_pasar = []

# =====================================================
# PERULANGAN STRUKTUR PASAR
# =====================================================

for pasar, parameter in struktur_pasar.items():

    rasio_dasar = parameter["rasio_dasar"]

    respon_harga = parameter["respon_harga"]

    respon_diskonto = parameter["respon_diskonto"]

    # =================================================
    # PRODUKSI TERKONEKSI DENGAN:
    # harga pasar
    # tingkat diskonto
    # struktur pasar
    # =================================================

    produksi = (
        produksi_awal *
        rasio_dasar *
        (
            1 +
            (harga_pasar * respon_harga) +
            (r * respon_diskonto)
        )
    )

    # produksi tidak boleh melebihi stok

    if produksi > stok_awal:
        produksi = stok_awal * 0.9

    # =================================================
    # WAKTU HABIS SUMBER DAYA
    # =================================================

    waktu_habis = stok_awal / produksi

    # =================================================
    # SIMULASI PER TAHUN
    # =================================================

    tahun = []
    produksi_tahun = []
    stok_tahun = []
    harga_tahun = []

    sisa_stok = stok_awal

    for i in range(1, tahun_simulasi + 1):

        tahun.append(i)

        # harga meningkat mengikuti Hotelling

        harga_periode = harga_pasar * ((1 + r) ** (i - 1))

        harga_tahun.append(harga_periode)

        # produksi dipengaruhi harga & diskonto

        produksi_periode = produksi * ((1 + r) ** (i - 1))

        # stok tidak boleh negatif

        if produksi_periode > sisa_stok:
            produksi_periode = sisa_stok

        produksi_tahun.append(produksi_periode)

        # stok berkurang karena produksi

        sisa_stok -= produksi_periode

        if sisa_stok < 0:
            sisa_stok = 0

        stok_tahun.append(sisa_stok)

    # =================================================
    # DATAFRAME
    # =================================================

    df = pd.DataFrame({
        "Tahun": tahun,
        "Produksi": produksi_tahun,
        "Sisa Stok": stok_tahun,
        "Harga": harga_tahun
    })

    # =================================================
    # HASIL RINGKASAN
    # =================================================

    hasil_pasar.append({
        "Struktur Pasar": pasar,
        "Produksi Awal": round(produksi, 2),
        "Waktu Habis": round(waktu_habis, 2)
    })

    # =================================================
    # DASHBOARD TIAP STRUKTUR PASAR
    # =================================================

    st.subheader(f"Dashboard {pasar}")

    # =================================================
    # BARIS 1
    # =================================================

    col1, col2 = st.columns(2)

    # =================================================
    # GRAFIK PRODUKSI
    # =================================================

    with col1:

        fig1 = px.bar(
            df,
            x="Tahun",
            y="Produksi",
            text_auto=True,
            title=f"Grafik Produksi - {pasar}"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # =================================================
    # GRAFIK STOK
    # =================================================

    with col2:

        fig2 = px.line(
            df,
            x="Tahun",
            y="Sisa Stok",
            markers=True,
            title=f"Grafik Sisa Stok - {pasar}"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # =================================================
    # BARIS 2
    # =================================================

    col3, col4 = st.columns(2)

    # =================================================
    # GRAFIK HARGA
    # =================================================

    with col3:

        fig3 = px.line(
            df,
            x="Tahun",
            y="Harga",
            markers=True,
            title=f"Simulasi Harga - {pasar}"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # =================================================
    # METRIK
    # =================================================

    with col4:

        st.metric(
            "Produksi Awal",
            f"{produksi:,.0f}"
        )

        st.metric(
            "Waktu Habis",
            f"{waktu_habis:.1f} Tahun"
        )

        st.metric(
            "Stok Awal",
            f"{stok_awal:,.0f}"
        )

    st.markdown("---")

# =====================================================
# TABEL PERBANDINGAN
# =====================================================

st.subheader("Perbandingan Struktur Pasar")

hasil_df = pd.DataFrame(hasil_pasar)

st.dataframe(
    hasil_df,
    use_container_width=True
)

# =====================================================
# KESIMPULAN
# =====================================================

st.subheader("Kesimpulan")

st.write("""
Simulasi menunjukkan bahwa harga pasar dan tingkat diskonto
memengaruhi tingkat produksi sumber daya batu bara.

Semakin tinggi harga dan tingkat diskonto,
perusahaan cenderung meningkatkan produksi,
sehingga stok sumber daya lebih cepat habis.

Pada struktur pasar persaingan sempurna,
tingkat produksi menjadi paling tinggi karena perusahaan
lebih responsif terhadap perubahan harga.

Monopoli menghasilkan produksi yang lebih rendah
dan lebih terkendali untuk menjaga keberlanjutan sumber daya.

Oligopoli berada di antara persaingan sempurna
dan monopoli dalam menentukan tingkat produksi.
""")

st.markdown("---")

st.caption(
    "Dashboard Analisis Intertemporal Sumber Daya Batu Bara - Universitas Islam Bandung"
)
