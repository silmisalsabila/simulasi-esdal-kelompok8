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
    "Jumlah Stok Batu Bara",
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
# SIMULASI PERMINTAAN
# =====================================================

permintaan = st.sidebar.selectbox(
    "Simulasi Perubahan Permintaan",
    [
        "Permintaan Normal",
        "Permintaan Naik",
        "Permintaan Turun"
    ]
)

# =====================================================
# PARAMETER DASAR
# =====================================================

r = suku_bunga / 100

if permintaan == "Permintaan Naik":
    faktor_permintaan = 1.3

elif permintaan == "Permintaan Turun":
    faktor_permintaan = 0.7

else:
    faktor_permintaan = 1.0

# =====================================================
# STRUKTUR PASAR
# =====================================================

struktur_pasar = {
    "Persaingan": 0.15,
    "Monopoli": 0.10,
    "Oligopoli": 0.12
}

# =====================================================
# DATA SIMULASI
# =====================================================

hasil_pasar = []
gabungan_df = pd.DataFrame()

for pasar, rasio in struktur_pasar.items():

    produksi = stok_awal * rasio * faktor_permintaan

    harga_simulasi = (
        harga_pasar +
        biaya_marginal +
        (muc_awal * r)
    )

    waktu_habis = stok_awal / produksi

    tahun = []
    stok = []
    ekstraksi = []

    sisa = stok_awal

    for i in range(1, tahun_simulasi + 1):

        tahun.append(i)

        if sisa > produksi:
            ekstraksi_tahun = produksi
        else:
            ekstraksi_tahun = sisa

        ekstraksi.append(ekstraksi_tahun)

        sisa -= ekstraksi_tahun

        if sisa < 0:
            sisa = 0

        stok.append(sisa)

    df = pd.DataFrame({
        "Tahun": tahun,
        "Ekstraksi": ekstraksi,
        "Sisa Stok": stok
    })

    df["Struktur Pasar"] = pasar

    gabungan_df = pd.concat(
        [gabungan_df, df],
        ignore_index=True
    )

    hasil_pasar.append({
        "Struktur Pasar": pasar,
        "Produksi/Tahun": round(produksi, 2),
        "Harga Simulasi": round(harga_simulasi, 2),
        "Waktu Habis": round(waktu_habis, 2)
    })

hasil_df = pd.DataFrame(hasil_pasar)

# =====================================================
# METRIK UTAMA
# =====================================================

st.subheader("Ringkasan Simulasi")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Jumlah Stok Awal",
        f"{stok_awal:,.0f}"
    )

with col2:
    st.metric(
        "Suku Bunga",
        f"{suku_bunga}%"
    )

with col3:
    st.metric(
        "Kondisi Permintaan",
        permintaan
    )

# =====================================================
# TABEL PERBANDINGAN
# =====================================================

st.subheader("Perbandingan Struktur Pasar")

st.dataframe(
    hasil_df,
    use_container_width=True
)

# =====================================================
# DASHBOARD VISUALISASI
# =====================================================

st.subheader("Dashboard Visualisasi")

tab1, tab2, tab3 = st.tabs([
    "Persaingan",
    "Monopoli",
    "Oligopoli"
])

# =====================================================
# TAB PERSAINGAN
# =====================================================

with tab1:

    st.markdown("## Struktur Pasar Persaingan")

    df_persaingan = gabungan_df[
        gabungan_df["Struktur Pasar"] == "Persaingan"
    ]

    col_a, col_b = st.columns(2)

    with col_a:

        fig1 = px.line(
            df_persaingan,
            x="Tahun",
            y="Sisa Stok",
            markers=True,
            title="Grafik Sisa Stok Batu Bara"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col_b:

        fig2 = px.bar(
            df_persaingan,
            x="Tahun",
            y="Ekstraksi",
            text_auto=True,
            title="Grafik Ekstraksi Batu Bara"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# =====================================================
# TAB MONOPOLI
# =====================================================

with tab2:

    st.markdown("## Struktur Pasar Monopoli")

    df_monopoli = gabungan_df[
        gabungan_df["Struktur Pasar"] == "Monopoli"
    ]

    col_c, col_d = st.columns(2)

    with col_c:

        fig3 = px.line(
            df_monopoli,
            x="Tahun",
            y="Sisa Stok",
            markers=True,
            title="Grafik Sisa Stok Batu Bara"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with col_d:

        fig4 = px.bar(
            df_monopoli,
            x="Tahun",
            y="Ekstraksi",
            text_auto=True,
            title="Grafik Ekstraksi Batu Bara"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

# =====================================================
# TAB OLIGOPOLI
# =====================================================

with tab3:

    st.markdown("## Struktur Pasar Oligopoli")

    df_oligopoli = gabungan_df[
        gabungan_df["Struktur Pasar"] == "Oligopoli"
    ]

    col_e, col_f = st.columns(2)

    with col_e:

        fig5 = px.line(
            df_oligopoli,
            x="Tahun",
            y="Sisa Stok",
            markers=True,
            title="Grafik Sisa Stok Batu Bara"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    with col_f:

        fig6 = px.bar(
            df_oligopoli,
            x="Tahun",
            y="Ekstraksi",
            text_auto=True,
            title="Grafik Ekstraksi Batu Bara"
        )

        st.plotly_chart(
            fig6,
            use_container_width=True
        )

# =====================================================
# HOTELLING MODEL
# =====================================================

st.subheader("Model Hotelling")

hotelling_tahun = np.arange(1, tahun_simulasi + 1)

hotelling_harga = [
    harga_pasar * ((1 + r) ** t)
    for t in hotelling_tahun
]

hotelling_df = pd.DataFrame({
    "Tahun": hotelling_tahun,
    "Harga Hotelling": hotelling_harga
})

fig7 = px.line(
    hotelling_df,
    x="Tahun",
    y="Harga Hotelling",
    markers=True,
    title="Kenaikan Harga Berdasarkan Model Hotelling"
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

# =====================================================
# GREEN PARADOX
# =====================================================

st.subheader("Green Paradox")

green_df = pd.DataFrame({
    "Tahun": hotelling_tahun,
    "Ekstraksi": np.linspace(
        stok_awal * 0.10,
        stok_awal * 0.20,
        tahun_simulasi
    )
})

fig8 = px.line(
    green_df,
    x="Tahun",
    y="Ekstraksi",
    markers=True,
    title="Simulasi Green Paradox"
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

# =====================================================
# KESIMPULAN
# =====================================================

st.subheader("Kesimpulan")

st.write(f"""
Dashboard ini menunjukkan pengaruh struktur pasar
dan perubahan permintaan terhadap tingkat ekstraksi,
sisa stok sumber daya, dan umur cadangan batu bara.

Pada kondisi {permintaan.lower()},
struktur pasar persaingan menghasilkan ekstraksi terbesar,
sedangkan monopoli lebih mampu menjaga keberlanjutan stok.

Model Hotelling memperlihatkan kenaikan harga sumber daya
seiring waktu, sedangkan Green Paradox menunjukkan
potensi percepatan eksploitasi akibat ekspektasi harga masa depan.
""")

st.markdown("---")

st.caption(
    "Dashboard Analisis Intertemporal Sumber Daya Batu Bara - Universitas Islam Bandung"
)
