
Claude finished the response
You said: di atas adalah file app.
Design.png
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

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
di atas adalah file app.py yang saya miliki sekarang. Saya ingin membuat tampilan yang ada pada gambar saya berikan ini.

Show more
9:41 AM
Claude responded: Saya akan membuat ulang tampilan dashboard tersebut dengan Streamlit yang mendekati desain pada gambar.

Reading frontend design skill
Reading frontend design skill
Saya akan membuat ulang tampilan dashboard tersebut dengan Streamlit yang mendekati desain pada gambar. Mari kita buat app.py yang lengkap dan polished.


Created a file, read a file
Created a file, read a file
Ini adalah app.py yang sudah diperbarui sesuai desain pada gambar. Berikut perubahan utama yang dilakukan:

KPI Cards — Dibuat dengan HTML custom menggunakan card style dengan border, shadow tipis, dan badge hijau untuk delta positif (mengganti st.metric bawaan Streamlit yang tampilannya lebih polos).

Growth Chart — Menggunakan Plotly go.Scatter dengan fill area biru transparan, marker bulat, dan spline curve — mirip tampilan di desain. Grid halus dan sumbu bersih.

Key Result Cabang — Tabel HTML custom dengan warna skor: hijau untuk nilai di atas rata-rata region, merah untuk di bawah, biru untuk netral.

Key Performance Indikator — Tabel detail dengan pemisah kategori (Profitabilitas, Volume Bisnis, Customer Based, Operasional) menggunakan header baris berwarna abu-abu — persis seperti desain.

Sidebar & Filter — Sidebar dengan logo "150 Store", tombol filter Bulan Ini (primary/biru) dan Tahun Ini, serta dropdown bulan.

Untuk menjalankan: streamlit run app.py


App
PY 
You said: hi
hi

9:58 AM
Claude responded: Hi!
Hi! How can I help you today?

You said: buatkan navbar yang ada profille dropdown yang berisi logout

import streamlit as st import pandas as pd import numpy as np import plotly.graph_objects as go st.set_page_config(layout="wide", page_title="KC Lambung Mangkurat", page_icon="🏦") # ===== CUSTOM CSS ===== st.markdown(""" <style> /* Import Google Font */ @import url('https://fon

pasted

buatkan navbar yang ada profille dropdown yang berisi logout

10:00 AM
Claude responded: Saya akan tulis ulang file lengkap dengan navbar yang terintegrasi: Navbar dengan profile dropdown sudah ditambahkan.

Edited 3 files, viewed 2 files
Edited 3 files, viewed 2 files
Saya akan tulis ulang file lengkap dengan navbar yang terintegrasi:


Ran a command, read a file
Ran a command, read a file
Navbar dengan profile dropdown sudah ditambahkan. Berikut yang baru ada:

Navbar (pojok kanan atas):

Ikon notifikasi 🔔 dan pengaturan ⚙️
Tombol "👤 Budi S. ▾" — klik untuk toggle dropdown
Dropdown Profile berisi:

Header dengan nama lengkap, email, dan badge jabatan "Kepala Cabang"
Menu: Profil Saya, Ubah Password, Pengaturan, Bantuan
Tombol Logout (merah) di bawah
Saat Logout:

Halaman bersih dengan pesan "Anda telah logout"
Tombol "Login Kembali" untuk reset session
Cara kerja dropdown menggunakan st.session_state sehingga toggle buka/tutup berfungsi dengan baik di Streamlit.


App
PY 




Claude is AI and can make mistakes. Please double-check responses.
App · PY
Copy

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
 
st.set_page_config(layout="wide", page_title="KC Lambung Mangkurat", page_icon="🏦")
 
# ===== SESSION STATE =====
if "show_dropdown" not in st.session_state:
    st.session_state.show_dropdown = False
if "logged_out" not in st.session_state:
    st.session_state.logged_out = False
 
# ===== CUSTOM CSS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main .block-container {
        padding-top: 0rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 100%;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #f0f0f0;
    }
    [data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }
 
    /* NAVBAR */
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ffffff;
        border-bottom: 1px solid #f0f0f0;
        padding: 12px 28px;
        margin-bottom: 2rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }
    .navbar-left { display: flex; align-items: center; gap: 10px; }
    .navbar-logo {
        width: 34px; height: 34px;
        background: #1677ff;
        border-radius: 8px;
        display: inline-flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 11px; color: white;
    }
    .navbar-brand { font-weight: 700; font-size: 15px; color: #1a1a2e; line-height:1.2; }
    .navbar-subtitle { font-size: 11px; color: #8c8c8c; }
    .navbar-right { display: flex; align-items: center; gap: 14px; }
    .nav-icon-btn {
        width: 34px; height: 34px;
        border-radius: 8px;
        background: #f5f7fa;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 15px; cursor: pointer;
        border: 1px solid #f0f0f0;
    }
    .profile-pill {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 4px 12px 4px 4px;
        background: #f5f7fa;
        border: 1px solid #f0f0f0;
        border-radius: 30px;
        cursor: pointer;
        transition: box-shadow 0.2s;
    }
    .profile-pill:hover { box-shadow: 0 2px 8px rgba(22,119,255,0.15); }
    .profile-avatar {
        width: 28px; height: 28px;
        background: linear-gradient(135deg, #1677ff, #0050cc);
        border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 12px; color: white;
    }
    .profile-name-pill { font-size: 13px; font-weight: 600; color: #1a1a2e; }
    .chevron { font-size: 10px; color: #8c8c8c; margin-left:2px; }
 
    /* DROPDOWN */
    .dropdown-card {
        background: #ffffff;
        border: 1px solid #eee;
        border-radius: 14px;
        padding: 6px;
        box-shadow: 0 12px 32px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06);
    }
    .dropdown-user-header {
        padding: 12px 14px 14px 14px;
        border-bottom: 1px solid #f5f5f5;
        margin-bottom: 4px;
    }
    .dropdown-avatar-lg {
        width: 40px; height: 40px;
        background: linear-gradient(135deg, #1677ff, #0050cc);
        border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 16px; color: white;
        margin-bottom: 8px;
    }
    .dropdown-user-name { font-size: 14px; font-weight: 700; color: #1a1a2e; }
    .dropdown-user-email { font-size: 12px; color: #8c8c8c; }
    .dropdown-item {
        display: flex; align-items: center; gap: 10px;
        padding: 9px 14px;
        border-radius: 8px;
        font-size: 13px; color: #262626;
        cursor: pointer; margin: 1px 0;
        transition: background 0.15s;
    }
    .dropdown-item:hover { background: #f5f7fa; }
    .dropdown-item-icon { font-size: 14px; width: 20px; text-align: center; }
    .dropdown-divider { border: none; border-top: 1px solid #f0f0f0; margin: 6px 0; }
    .dropdown-item-danger { color: #ff4d4f !important; }
    .dropdown-item-danger:hover { background: #fff2f0 !important; }
 
    /* KPI CARD */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #f0f2f5;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .kpi-label { font-size: 12px; color: #8c8c8c; font-weight: 500; margin-bottom: 6px; }
    .kpi-value { font-size: 28px; font-weight: 700; color: #1a1a2e; line-height: 1.2; margin-bottom: 6px; }
    .kpi-delta-pos {
        font-size: 12px; color: #52c41a; font-weight: 600;
        background: #f6ffed; border: 1px solid #b7eb8f;
        border-radius: 20px; padding: 2px 8px; display: inline-block;
    }
    .kpi-delta-neg {
        font-size: 12px; color: #ff4d4f; font-weight: 600;
        background: #fff2f0; border: 1px solid #ffccc7;
        border-radius: 20px; padding: 2px 8px; display: inline-block;
    }
    .section-card {
        background: #ffffff;
        border: 1px solid #f0f2f5;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        height: 100%;
    }
    .stButton > button {
        border-radius: 8px; font-size: 13px; font-weight: 500;
        padding: 6px 16px; border: 1px solid #d9d9d9;
        background: #ffffff; color: #595959; transition: all 0.2s;
    }
    .stButton > button:hover { border-color: #1677ff; color: #1677ff; }
    h1 { font-size: 28px !important; font-weight: 700 !important; color: #1a1a2e !important; margin-bottom: 0 !important; }
    .key-result-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .key-result-table th {
        font-size: 11px; color: #8c8c8c; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.5px;
        padding: 8px 12px; border-bottom: 1px solid #f0f0f0; text-align: left;
    }
    .key-result-table td { padding: 10px 12px; border-bottom: 1px solid #f8f8f8; color: #262626; font-size: 13px; }
    .key-result-table tr:last-child td { border-bottom: none; }
    .score-green { color: #52c41a; font-weight: 600; }
    .score-red   { color: #ff4d4f; font-weight: 600; }
    .score-blue  { color: #1677ff; font-weight: 600; }
    .kpi-table-wrapper {
        background: #ffffff; border: 1px solid #f0f2f5;
        border-radius: 12px; padding: 20px 24px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .kpi-detail-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .kpi-detail-table th {
        font-size: 11px; color: #8c8c8c; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.4px;
        padding: 8px 10px; text-align: right;
    }
    .kpi-detail-table th:first-child, .kpi-detail-table th:nth-child(2) { text-align: left; }
    .kpi-detail-table td {
        padding: 10px 10px; border-top: 1px solid #f5f5f5;
        color: #262626; vertical-align: middle; text-align: right;
    }
    .kpi-detail-table td:first-child { text-align: center; color: #8c8c8c; width: 30px; }
    .kpi-detail-table td:nth-child(2) { text-align: left; }
    .category-header td {
        border-top: 1px solid #f0f0f0 !important;
        background: #fafafa; color: #8c8c8c !important;
        font-weight: 700 !important; font-size: 11px !important;
        text-align: left !important; letter-spacing: 0.5px; text-transform: uppercase;
    }
    .tab-active {
        background: #1677ff; color: white; border-radius: 6px;
        padding: 4px 14px; font-size: 13px; font-weight: 600; display: inline-block;
    }
    .tab-inactive { color: #595959; padding: 4px 14px; font-size: 13px; display: inline-block; }
    hr { border: none; border-top: 1px solid #f0f0f0; margin: 16px 0; }
    div[data-testid="stDataFrame"] {display: none;}
</style>
""", unsafe_allow_html=True)
 
# ===== LOGOUT PAGE =====
if st.session_state.logged_out:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                height:70vh;font-family:'Plus Jakarta Sans',sans-serif;text-align:center;">
        <div style="font-size:56px;margin-bottom:16px;">👋</div>
        <h2 style="color:#1a1a2e;margin-bottom:8px;font-size:24px;">Anda telah logout</h2>
        <p style="color:#8c8c8c;font-size:14px;">Terima kasih telah menggunakan KC Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([2,1,2])
    with col_b:
        if st.button("🔐 Login Kembali", use_container_width=True, type="primary"):
            st.session_state.logged_out = False
            st.rerun()
    st.stop()
 
# ===== NAVBAR =====
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:0 8px 16px 8px;
                border-bottom:1px solid #f0f0f0;margin-bottom:16px;">
        <div style="width:36px;height:36px;background:#1677ff;border-radius:8px;
                    display:flex;align-items:center;justify-content:center;">
            <span style="color:white;font-weight:700;font-size:13px;">150</span>
        </div>
        <div>
            <div style="font-weight:700;font-size:14px;color:#1a1a2e;">150 Store</div>
            <div style="font-size:11px;color:#8c8c8c;">Free trial</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#eff6ff;border-radius:8px;padding:10px 14px;
                display:flex;align-items:center;gap:10px;">
        <span style="font-size:16px;">📊</span>
        <span style="font-weight:600;font-size:14px;color:#1677ff;">Dashboard</span>
    </div>
    """, unsafe_allow_html=True)
 
# Top Navbar
nav_left, nav_right = st.columns([6, 2])
with nav_left:
    st.markdown("""
    <div style="padding:12px 0 16px 0; border-bottom:1px solid #f0f0f0; margin-bottom:20px;
                display:flex; align-items:center; gap:12px;">
        <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:20px;">📊</span>
            <span style="font-weight:700;font-size:16px;color:#1a1a2e;">Dashboard</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
with nav_right:
    st.markdown("<div style='padding-top:6px; border-bottom:1px solid #f0f0f0; margin-bottom:20px; padding-bottom:6px;'>", unsafe_allow_html=True)
    nav_col1, nav_col2 = st.columns([1, 2])
    with nav_col1:
        st.markdown("""
        <div style="display:flex;gap:6px;justify-content:flex-end;">
            <div class="nav-icon-btn">🔔</div>
            <div class="nav-icon-btn">⚙️</div>
        </div>
        """, unsafe_allow_html=True)
    with nav_col2:
        if st.button("👤  Budi S.  ▾", key="profile_btn", use_container_width=True):
            st.session_state.show_dropdown = not st.session_state.show_dropdown
    st.markdown("</div>", unsafe_allow_html=True)
 
# Profile Dropdown
if st.session_state.show_dropdown:
    _, dd_col, _ = st.columns([5, 2, 0.1])
    with dd_col:
        st.markdown("""
        <div class="dropdown-card">
            <div class="dropdown-user-header">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div class="dropdown-avatar-lg">B</div>
                    <div>
                        <div class="dropdown-user-name">Budi Santoso</div>
                        <div class="dropdown-user-email">budi.s@kcbisnis.id</div>
                        <div style="margin-top:4px;">
                            <span style="font-size:10px;background:#eff6ff;color:#1677ff;
                                         border:1px solid #bae0ff;border-radius:10px;
                                         padding:1px 8px;font-weight:600;">Kepala Cabang</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="dropdown-item">
                <span class="dropdown-item-icon">👤</span> Profil Saya
            </div>
            <div class="dropdown-item">
                <span class="dropdown-item-icon">🔒</span> Ubah Password
            </div>
            <div class="dropdown-item">
                <span class="dropdown-item-icon">⚙️</span> Pengaturan
            </div>
            <hr class="dropdown-divider">
            <div class="dropdown-item">
                <span class="dropdown-item-icon">❓</span> Bantuan
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("🚪  Logout", key="logout_btn", use_container_width=True, type="primary"):
            st.session_state.logged_out = True
            st.session_state.show_dropdown = False
            st.rerun()
 
# ===== PAGE HEADER =====
col_title, col_export = st.columns([6, 1])
with col_title:
    st.markdown("""
    <h1>KC Lambung Mangkurat</h1>
    <p style="color:#8c8c8c; font-size:13px; margin-top:2px;">Have a look at your recent status</p>
    """, unsafe_allow_html=True)
with col_export:
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.button("⬇ Export")
 
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
 
# ===== FILTER TABS =====
fc1, fc2, fc3 = st.columns([0.5, 1, 2])
with fc1:
    kategori_list = ["Bulan Ini", "Tahun Ini"]
    st.selectbox("", kategori_list, label_visibility="collapsed")
with fc2:
    bulan_list = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    st.selectbox("", bulan_list, label_visibility="collapsed")
 
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
 
# ===== KPI CARDS =====
kpis = [
    {"label": "Total Score KPI",     "value": "89,8",  "delta": "↑ 21%", "sub": "From last week", "pos": True},
    {"label": "Score Profitabilitas", "value": "90,2",  "delta": "↑ $53", "sub": "From last week", "pos": True},
    {"label": "Volume Bisnis",        "value": "88,7",  "delta": "↑ 4%",  "sub": "From last week", "pos": True},
    {"label": "Customers Base",       "value": "87,9",  "delta": "↑ 114", "sub": "From last week", "pos": True},
    {"label": "Operasional",          "value": "92,02", "delta": "↑ 21%", "sub": "From last week", "pos": True},
]
k_cols = st.columns(5, gap="small")
for i, kpi in enumerate(kpis):
    with k_cols[i]:
        delta_class = "kpi-delta-pos" if kpi["pos"] else "kpi-delta-neg"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{kpi['label']}</div>
            <div class="kpi-value">{kpi['value']}</div>
            <span class="{delta_class}">{kpi['delta']}</span>
            <span style="font-size:11px;color:#8c8c8c;margin-left:4px;">{kpi['sub']}</span>
        </div>
        """, unsafe_allow_html=True)
 
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
 
# ===== GROWTH CHART + KEY RESULT =====
col_chart, col_table = st.columns([2, 1], gap="medium")
 
with col_chart:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:4px;margin-bottom:16px;">
        <span style="font-weight:700;font-size:15px;color:#1a1a2e;margin-right:12px;">Growth Performance</span>
        <span class="tab-active">Bulan Ini</span>
        <span class="tab-inactive">All Performance</span>
    </div>
    """, unsafe_allow_html=True)
    days = ["Mon\n15","Tue\n16","Wed\n17","Thu\n18","Fri\n19","Sat\n20","Sun\n21"]
    values = [2200, 2100, 2400, 3800, 5200, 6800, 7900]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=values,
        mode='lines+markers',
        line=dict(color='#1677ff', width=2.5, shape='spline'),
        marker=dict(size=6, color='#1677ff', line=dict(width=2, color='white')),
        fill='tozeroy', fillcolor='rgba(22,119,255,0.08)',
    ))
    fig.update_layout(
        margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=220,
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11,color='#8c8c8c'), tickmode='array', tickvals=days),
        yaxis=dict(showgrid=True, gridcolor='#f5f5f5', zeroline=False, tickfont=dict(size=11,color='#8c8c8c'), nticks=6),
        hovermode='x unified',
        hoverlabel=dict(bgcolor='#1677ff', font_color='white', bordercolor='#1677ff'),
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
 
with col_table:
    st.markdown("""
    <div class="section-card">
        <div style="font-weight:700;font-size:15px;color:#1a1a2e;margin-bottom:14px;">Key Result Cabang</div>
        <table class="key-result-table">
            <thead><tr>
                <th>#</th><th>Key Result</th><th>Skor Cabang</th><th>Avg Region</th>
            </tr></thead>
            <tbody>
                <tr><td style="color:#8c8c8c;">1</td><td>Profitabilitas</td><td class="score-green">90,2</td><td>89</td></tr>
                <tr><td style="color:#8c8c8c;">2</td><td>Volume Bisnis/Kualitas</td><td class="score-blue">88,7</td><td>88</td></tr>
                <tr><td style="color:#8c8c8c;">3</td><td>Customer Based</td><td class="score-red">87,9</td><td>90</td></tr>
                <tr><td style="color:#8c8c8c;">4</td><td>Operasional & People Development</td><td class="score-green">92,02</td><td>91</td></tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
 
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
 
# ===== KPI DETAIL TABLE =====
st.markdown("""
<div class="kpi-table-wrapper">
    <div style="font-weight:700;font-size:15px;color:#1a1a2e;margin-bottom:16px;">Key Performance Indikator</div>
    <table class="kpi-detail-table">
        <thead>
            <tr>
                <th>#</th><th>Indikator</th>
                <th>Real/Growth</th><th>Target</th><th>Real %</th><th>Penc Maks %</th><th>Skor</th>
            </tr>
        </thead>
        <tbody>
            <tr class="category-header"><td colspan="7"># &nbsp; Profitabilitas</td></tr>
            <tr><td>1</td><td style="text-align:left">Contribution Margin</td><td></td><td></td><td></td><td>88%</td><td>8,8</td></tr>
            <tr><td>2</td><td style="text-align:left">FBI Selain Bancasurance</td><td></td><td></td><td></td><td>$1,250</td><td>90</td></tr>
            <tr><td>3</td><td style="text-align:left">Ace Bancasurance</td><td></td><td></td><td></td><td>$1,030</td><td>330</td></tr>
 
            <tr class="category-header"><td colspan="7"># &nbsp; Volume Bisnis / Kualitas</td></tr>
            <tr><td>1</td><td style="text-align:left">DPK - Tabungan</td><td></td><td></td><td></td><td>$1,304</td><td>195</td></tr>
            <tr><td>2</td><td style="text-align:left">DPK - Giro</td><td></td><td></td><td></td><td>$1,250</td><td>90</td></tr>
            <tr><td>3</td><td style="text-align:left">DPK - Deposito</td><td></td><td></td><td></td><td>$1,030</td><td>330</td></tr>
            <tr><td>4</td><td style="text-align:left">DPK - Penambahan User Aktif Digital Transaction (Byond, Qris, EDC, BSI Agen, BEWIZE)</td><td></td><td></td><td></td><td>$1,030</td><td>330</td></tr>
            <tr><td>5</td><td style="text-align:left">Consumer +Mikro</td><td></td><td></td><td></td><td>$1,030</td><td>330</td></tr>
            <tr><td>6</td><td style="text-align:left">Gold Business</td><td></td><td></td><td></td><td>$1,030</td><td>330</td></tr>
            <tr><td>7</td><td style="text-align:left">Retail - SME</td><td></td><td></td><td></td><td>$1,030</td><td>330</td></tr>
            <tr><td>8</td><td style="text-align:left">Pengendalian Kualitas - Net DG</td><td></td><td></td><td></td><td>$1,030</td><td>330</td></tr>
            <tr><td>9</td><td style="text-align:left">Pengendalian Kualitas - NPF</td><td></td><td></td><td></td><td>$1,030</td><td>330</td></tr>
            <tr><td>10</td><td style="text-align:left">Pengendalian Kualitas - Kol 2</td><td></td><td></td><td></td><td>$1,030</td><td>330</td></tr>
 
            <tr class="category-header"><td colspan="7"># &nbsp; Customer Based</td></tr>
            <tr><td>1</td><td style="text-align:left">Penambahan Customer Based : All Customer</td><td></td><td></td><td></td><td>$1,304</td><td>195</td></tr>
            <tr><td>2</td><td style="text-align:left">Penambahan Customer Based : Payroll, Bisnis Emas & Hajj Customer</td><td></td><td></td><td></td><td>$1,250</td><td>90</td></tr>
 
            <tr class="category-header"><td colspan="7"># &nbsp; Operasional & People Development</td></tr>
            <tr><td>1</td><td style="text-align:left">Produktifitas Perindividu Non Sales (Rasio Sales : Non Sales)</td><td></td><td></td><td></td><td>$1,304</td><td>195</td></tr>
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)
 
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
 


