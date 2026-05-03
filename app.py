import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from streamlit_card import card

st.set_page_config(layout="wide")

# ===== HEADER =====
st.title("KC Lambung Mangkurat")
st.caption("Have a look at your recent status")

# ===== FILTER =====
col1, col2, col3 = st.columns([1,1,2])
with col1:
    st.button("Bulan Ini")
with col2:
    st.button("Tahun Ini")
with col3:
    st.selectbox("Pilih Bulan", ["Januari", "Februari", "Maret"])

# ===== KPI CARDS =====
def kpi_card(title, value, change):
    st.metric(label=title, value=value, delta=change)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    kpi_card("Total Score KPI", "89.8", "21%")
    # card(title="Total Score KPI", text= "89.8")
with k2:
    kpi_card("Score Profitabilitas", "90.2", "5.5")
with k3:
    kpi_card("Volume Bisnis", "88.7", "4%")
with k4:
    kpi_card("Customers Base", "87.9", "11%")
with k5:
    kpi_card("Operasional", "92.02", "21%")

# ===== CHART + TABLE =====
col_left, col_right = st.columns([2,1])

# Chart dummy
with col_left:
    st.subheader("Growth Performance")

    data = np.cumsum(np.random.randn(7)) * 1000
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    fig, ax = plt.subplots()
    ax.plot(days, data)
    st.plotly_chart(fig)

# Key Result Table
with col_right:
    st.subheader("Key Result Cabang")

    df = pd.DataFrame({
        "Key Result": ["Profitabilitas", "Volume Bisnis", "Customer Based", "Operasional"],
        "Skor Cabang": [90.2, 88.7, 87.9, 92.02],
        "Avg Region": [89, 88, 90, 91]
    })

    st.dataframe(df, use_container_width=True)

# ===== KPI DETAIL TABLE =====
st.subheader("Key Performance Indicator")

df_kpi = pd.DataFrame({
    "Kategori": ["Profitabilitas", "Volume Bisnis", "Customer Based", "Operasional"],
    "Indikator": [
        "Contribution Margin",
        "DPK - Tabungan",
        "Penambahan Customer",
        "Produktivitas Sales"
    ],
    "Target": [100, 200, 150, 80],
    "Realisasi": [88, 180, 120, 75],
    "Score": [8.8, 8.5, 8.0, 8.7]
})

st.dataframe(df_kpi, use_container_width=True)