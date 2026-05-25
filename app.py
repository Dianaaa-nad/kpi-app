import streamlit as st
import numpy as np
import plotly.graph_objects as go
from db import fetch_cabang, fetch_kpi_variables, fetch_kpi_detail

st.set_page_config(layout="wide", page_title="Dashboard KPI", page_icon="🏦")

# ===== DATA PER CABANG =====
CABANG_DATA = {
    "KCP Banjarmasin Lambung Mangkurat": {
        "kpis": [
            {"label": "Total Score KPI",     "value": "89,8",  "delta": "↑ 21%", "pos": True},
            {"label": "Score Profitabilitas", "value": "90,2",  "delta": "↑ $53", "pos": True},
            {"label": "Volume Bisnis",        "value": "88,7",  "delta": "↑ 4%",  "pos": True},
            {"label": "Customers Base",       "value": "87,9",  "delta": "↑ 114", "pos": True},
            {"label": "Operasional",          "value": "92,02", "delta": "↑ 21%", "pos": True},
        ],
        "chart_values": [2200, 2100, 2400, 3800, 5200, 6800, 7900],
        "key_results": [
            {"name": "Profitabilitas",                    "skor": "90,2",  "avg": 89, "color": "green"},
            {"name": "Volume Bisnis/Kualitas",            "skor": "88,7",  "avg": 88, "color": "blue"},
            {"name": "Customer Based",                    "skor": "87,9",  "avg": 90, "color": "red"},
            {"name": "Operasional & People Development",  "skor": "92,02", "avg": 91, "color": "green"},
        ],
    },
    "KC Kayu Tangi": {
        "kpis": [
            {"label": "Total Score KPI",     "value": "85,4",  "delta": "↑ 10%", "pos": True},
            {"label": "Score Profitabilitas", "value": "84,7",  "delta": "↓ $12", "pos": False},
            {"label": "Volume Bisnis",        "value": "86,3",  "delta": "↑ 6%",  "pos": True},
            {"label": "Customers Base",       "value": "83,1",  "delta": "↓ 22",  "pos": False},
            {"label": "Operasional",          "value": "87,50", "delta": "↑ 15%", "pos": True},
        ],
        "chart_values": [1800, 2200, 2000, 3100, 4200, 5500, 6100],
        "key_results": [
            {"name": "Profitabilitas",                    "skor": "84,7",  "avg": 89, "color": "red"},
            {"name": "Volume Bisnis/Kualitas",            "skor": "86,3",  "avg": 85, "color": "green"},
            {"name": "Customer Based",                    "skor": "83,1",  "avg": 86, "color": "red"},
            {"name": "Operasional & People Development",  "skor": "87,50", "avg": 85, "color": "green"},
        ],
    },
    "KC Tapin": {
        "kpis": [
            {"label": "Total Score KPI",     "value": "92,1",  "delta": "↑ 30%", "pos": True},
            {"label": "Score Profitabilitas", "value": "93,5",  "delta": "↑ $80", "pos": True},
            {"label": "Volume Bisnis",        "value": "91,2",  "delta": "↑ 12%", "pos": True},
            {"label": "Customers Base",       "value": "90,8",  "delta": "↑ 200", "pos": True},
            {"label": "Operasional",          "value": "94,10", "delta": "↑ 35%", "pos": True},
        ],
        "chart_values": [3500, 4000, 4800, 6200, 7100, 8500, 9200],
        "key_results": [
            {"name": "Profitabilitas",                    "skor": "93,5",  "avg": 89, "color": "green"},
            {"name": "Volume Bisnis/Kualitas",            "skor": "91,2",  "avg": 88, "color": "green"},
            {"name": "Customer Based",                    "skor": "90,8",  "avg": 90, "color": "blue"},
            {"name": "Operasional & People Development",  "skor": "94,10", "avg": 91, "color": "green"},
        ],
    },
    "KC Gatot Subroto": {
        "kpis": [
            {"label": "Total Score KPI",     "value": "78,5",  "delta": "↓ 5%",  "pos": False},
            {"label": "Score Profitabilitas", "value": "77,2",  "delta": "↓ $30", "pos": False},
            {"label": "Volume Bisnis",        "value": "80,1",  "delta": "↑ 2%",  "pos": True},
            {"label": "Customers Base",       "value": "76,4",  "delta": "↓ 50",  "pos": False},
            {"label": "Operasional",          "value": "80,30", "delta": "↓ 8%",  "pos": False},
        ],
        "chart_values": [3000, 2800, 2600, 2900, 3100, 2700, 2500],
        "key_results": [
            {"name": "Profitabilitas",                    "skor": "77,2",  "avg": 89, "color": "red"},
            {"name": "Volume Bisnis/Kualitas",            "skor": "80,1",  "avg": 88, "color": "red"},
            {"name": "Customer Based",                    "skor": "76,4",  "avg": 90, "color": "red"},
            {"name": "Operasional & People Development",  "skor": "80,30", "avg": 91, "color": "red"},
        ],
    },
    "KC Martapura": {
        "kpis": [
            {"label": "Total Score KPI",     "value": "88,0",  "delta": "↑ 18%", "pos": True},
            {"label": "Score Profitabilitas", "value": "87,5",  "delta": "↑ $45", "pos": True},
            {"label": "Volume Bisnis",        "value": "89,3",  "delta": "↑ 7%",  "pos": True},
            {"label": "Customers Base",       "value": "86,6",  "delta": "↑ 90",  "pos": True},
            {"label": "Operasional",          "value": "88,90", "delta": "↑ 12%", "pos": True},
        ],
        "chart_values": [2000, 2500, 3000, 3600, 4800, 5900, 7000],
        "key_results": [
            {"name": "Profitabilitas",                    "skor": "87,5",  "avg": 89, "color": "red"},
            {"name": "Volume Bisnis/Kualitas",            "skor": "89,3",  "avg": 88, "color": "green"},
            {"name": "Customer Based",                    "skor": "86,6",  "avg": 90, "color": "red"},
            {"name": "Operasional & People Development",  "skor": "88,90", "avg": 87, "color": "green"},
        ],
    },
}

CABANG_LIST = list(CABANG_DATA.keys())

# ===== SESSION STATE =====
if "selected_cabang" not in st.session_state:
    st.session_state.selected_cabang = CABANG_LIST[0]
if "show_cabang_dd" not in st.session_state:
    st.session_state.show_cabang_dd = False

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* ── Light-theme defaults (CSS variables) ── */
    :root {
        --bg-body: #f5f6fa;
        --bg-card: #fff;
        --bg-card-hover-shadow: rgba(22,119,255,0.10);
        --text-primary: #1a1a2e;
        --text-secondary: #262626;
        --text-muted: #8c8c8c;
        --text-soft: #595959;
        --border-card: #f0f2f5;
        --border-light: #f0f0f0;
        --border-input: #d9d9d9;
        --border-dropdown: #e8e8e8;
        --shadow-card: 0 1px 4px rgba(0,0,0,0.05);
        --shadow-dropdown: 0 12px 40px rgba(0,0,0,0.13);
        --dd-hover: #f0f7ff;
        --dd-active: #eff6ff;
        --hr-color: #f0f0f0;
        --cat-header-bg: #fafafa;
        --delta-pos-bg: #f6ffed;  --delta-pos-border: #b7eb8f;
        --delta-neg-bg: #fff2f0;  --delta-neg-border: #ffccc7;
        /* table column bands – light */
        --col-blue-head: #e8f4fd;   --col-blue-cell: #f0f8ff;
        --col-orange-head: #fff7e6; --col-orange-cell: #fffbe6;
        --col-green-head: #f6ffed;  --col-green-cell: #f6ffed;
        --col-purple-head: #f9f0ff; --col-purple-cell: #f9f0ff;
        --col-red-head: #fff1f0;    --col-red-cell: #fff1f0;
        --grid-line: #f5f5f5;
    }

    /* ── Dark-theme overrides ── */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-body: #0e1117;
            --bg-card: #1a1d24;
            --bg-card-hover-shadow: rgba(22,119,255,0.20);
            --text-primary: #e6e8ec;
            --text-secondary: #cfd2d6;
            --text-muted: #8b8fa3;
            --text-soft: #a0a4b0;
            --border-card: #2a2d35;
            --border-light: #2a2d35;
            --border-input: #3a3d45;
            --border-dropdown: #2a2d35;
            --shadow-card: 0 1px 6px rgba(0,0,0,0.30);
            --shadow-dropdown: 0 12px 40px rgba(0,0,0,0.50);
            --dd-hover: #1c2636;
            --dd-active: #17253a;
            --hr-color: #2a2d35;
            --cat-header-bg: #1e2128;
            --delta-pos-bg: #162312;  --delta-pos-border: #274916;
            --delta-neg-bg: #2a1215;  --delta-neg-border: #58181c;
            --col-blue-head: #111d2c;   --col-blue-cell: #111d2c;
            --col-orange-head: #2b1d11; --col-orange-cell: #2b1d11;
            --col-green-head: #162312;  --col-green-cell: #162312;
            --col-purple-head: #1a1325; --col-purple-cell: #1a1325;
            --col-red-head: #2a1215;    --col-red-cell: #2a1215;
            --grid-line: #262930;
        }
        /* Streamlit internal overrides for dark */
        .stApp, .main, [data-testid="stAppViewContainer"],
        [data-testid="stHeader"], [data-testid="stToolbar"] {
            background-color: var(--bg-body) !important;
        }
        .stSelectbox > div > div,
        [data-baseweb="select"] > div {
            background-color: var(--bg-card) !important;
            color: var(--text-secondary) !important;
            border-color: var(--border-input) !important;
        }
        [data-baseweb="menu"] {
            background-color: var(--bg-card) !important;
        }
        [data-baseweb="menu"] li {
            color: var(--text-secondary) !important;
        }
        [data-baseweb="menu"] li:hover {
            background-color: var(--dd-hover) !important;
        }
    }

    /* ── Base styles ── */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: var(--bg-body);
    }
    .stApp { background-color: var(--bg-body); }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main .block-container { padding-top: 2rem; padding-left: 2.5rem; padding-right: 2.5rem; max-width: 100%; }

    /* Title button */
    [data-testid="stButton"] > button[kind="secondary"] {
        background: transparent !important; border: none !important;
        padding: 0 4px !important; font-size: 24px !important; font-weight: 700 !important;
        color: var(--text-primary) !important; box-shadow: none !important;
        text-align: left !important; line-height: 1.2 !important; cursor: pointer !important;
    }
    [data-testid="stButton"] > button[kind="secondary"]:hover {
        color: #1677ff !important; background: transparent !important; border: none !important;
    }

    /* Dropdown card */
    .cabang-dropdown {
        background: var(--bg-card); border: 1px solid var(--border-dropdown);
        border-radius: 14px; padding: 8px;
        box-shadow: var(--shadow-dropdown); min-width: 260px;
    }
    .cabang-dd-header {
        font-size: 10px; font-weight: 700; color: var(--text-muted);
        text-transform: uppercase; letter-spacing: 0.8px;
        padding: 6px 10px 10px 10px;
        border-bottom: 1px solid var(--border-light); margin-bottom: 6px;
    }
    .cabang-dd-item {
        display: flex; align-items: center; justify-content: space-between;
        padding: 9px 12px; border-radius: 8px;
        font-size: 13px; color: var(--text-secondary); cursor: pointer;
        transition: background 0.15s;
    }
    .cabang-dd-item:hover { background: var(--dd-hover); color: #1677ff; }
    .cabang-dd-item-active { background: var(--dd-active); color: #1677ff; font-weight: 600; }
    .cabang-dd-check { color: #1677ff; font-size: 13px; }

    /* KPI card */
    .kpi-card {
        background: var(--bg-card); border: 1px solid var(--border-card);
        border-radius: 12px; padding: 18px 20px;
        box-shadow: var(--shadow-card); transition: box-shadow 0.2s;
    }
    .kpi-card:hover { box-shadow: 0 4px 16px var(--bg-card-hover-shadow); }
    .kpi-label { font-size: 12px; color: var(--text-muted); font-weight: 500; margin-bottom: 6px; }
    .kpi-value { font-size: 26px; font-weight: 700; color: var(--text-primary); line-height: 1.2; margin-bottom: 6px; }
    .kpi-delta-pos { font-size: 12px; color: #52c41a; font-weight: 600; background: var(--delta-pos-bg); border: 1px solid var(--delta-pos-border); border-radius: 20px; padding: 2px 8px; display: inline-block; }
    .kpi-delta-neg { font-size: 12px; color: #ff4d4f; font-weight: 600; background: var(--delta-neg-bg); border: 1px solid var(--delta-neg-border); border-radius: 20px; padding: 2px 8px; display: inline-block; }

    /* Section card */
    .section-card { background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; padding: 20px 24px; box-shadow: var(--shadow-card); height: 100%; }

    /* Buttons */
    .stButton > button { border-radius: 8px; font-size: 13px; font-weight: 500; padding: 6px 16px; border: 1px solid var(--border-input); background: var(--bg-card); color: var(--text-soft); transition: all 0.2s; }
    .stButton > button:hover { border-color: #1677ff; color: #1677ff; }

    /* Key-result table – Skor Cabang */
    .key-result-table th:nth-child(3) { background: var(--col-green-head); color: #389e0d !important; }
    .key-result-table td:nth-child(3) { background: var(--col-green-cell); color: #389e0d; font-weight: 600; }
    /* Key-result table – Avg Region */
    .key-result-table th:nth-child(4) { background: var(--col-blue-head); color: #1677ff !important; }
    .key-result-table td:nth-child(4) { background: var(--col-blue-cell); color: #1677ff; font-weight: 600; }

    /* Tables base */
    .key-result-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .key-result-table th { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; padding: 8px 12px; border-bottom: 1px solid var(--border-light); text-align: left; }
    .key-result-table td { padding: 10px 12px; border-bottom: 1px solid var(--border-light); color: var(--text-secondary); font-size: 13px; }
    .key-result-table tr:last-child td { border-bottom: none; }
    .score-green { color: #52c41a; font-weight: 600; }
    .score-red   { color: #ff4d4f; font-weight: 600; }
    .score-blue  { color: #1677ff; font-weight: 600; }

    /* KPI detail table */
    .kpi-table-wrapper { background: var(--bg-card); border: 1px solid var(--border-card); border-radius: 12px; padding: 20px 24px; box-shadow: var(--shadow-card); }
    .kpi-detail-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .kpi-detail-table th { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.4px; padding: 10px 10px; text-align: right; }
    .kpi-detail-table th:first-child, .kpi-detail-table th:nth-child(2) { text-align: left; }
    .kpi-detail-table td { padding: 10px 10px; border-top: 1px solid var(--border-light); color: var(--text-secondary); vertical-align: middle; text-align: right; }
    .kpi-detail-table td:first-child { text-align: center; color: var(--text-muted); width: 30px; }
    .kpi-detail-table td:nth-child(2) { text-align: left; }
    .category-header td { border-top: 1px solid var(--border-light) !important; background: var(--cat-header-bg); color: var(--text-muted) !important; font-weight: 700 !important; font-size: 11px !important; text-align: left !important; letter-spacing: 0.5px; text-transform: uppercase; }

    /* Column color bands */
    .kpi-detail-table th:nth-child(3) { background: var(--col-blue-head); color: #1677ff !important; border-radius: 6px 6px 0 0; }
    .kpi-detail-table th:nth-child(4) { background: var(--col-orange-head); color: #d46b08 !important; border-radius: 6px 6px 0 0; }
    .kpi-detail-table th:nth-child(5) { background: var(--col-green-head); color: #389e0d !important; border-radius: 6px 6px 0 0; }
    .kpi-detail-table th:nth-child(6) { background: var(--col-purple-head); color: #722ed1 !important; border-radius: 6px 6px 0 0; }
    .kpi-detail-table th:nth-child(7) { background: var(--col-red-head); color: #cf1322 !important; border-radius: 6px 6px 0 0; }

    .kpi-detail-table tr:not(.category-header) td:nth-child(3) { background: var(--col-blue-cell); color: #1677ff; font-weight: 600; }
    .kpi-detail-table tr:not(.category-header) td:nth-child(4) { background: var(--col-orange-cell); color: #d46b08; font-weight: 600; }
    .kpi-detail-table tr:not(.category-header) td:nth-child(5) { background: var(--col-green-cell); color: #389e0d; font-weight: 600; }
    .kpi-detail-table tr:not(.category-header) td:nth-child(6) { background: var(--col-purple-cell); color: #722ed1; font-weight: 600; }
    .kpi-detail-table tr:not(.category-header) td:nth-child(7) { background: var(--col-red-cell); color: #cf1322; font-weight: 600; }

    .tab-active { background: #1677ff; color: white; border-radius: 6px; padding: 4px 14px; font-size: 13px; font-weight: 600; display: inline-block; }
    .tab-inactive { color: var(--text-soft); padding: 4px 14px; font-size: 13px; display: inline-block; cursor: pointer; }
    hr { border: none; border-top: 1px solid var(--hr-color); margin: 16px 0; }
    div[data-testid="stDataFrame"] { display: none; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ===== ACTIVE DATA =====
data = CABANG_DATA[st.session_state.selected_cabang]

# ===== PAGE HEADER =====
col_title, col_export = st.columns([6, 1])
with col_title:
    btn_label = f"{st.session_state.selected_cabang}  ▾"
    if st.button(btn_label, key="cabang_title_btn"):
        st.session_state.show_cabang_dd = not st.session_state.show_cabang_dd   

with col_export:
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.button("⬇ Export")

# ===== CABANG DROPDOWN =====
if st.session_state.show_cabang_dd:
    dd_col, _ = st.columns([2, 5])
    with dd_col:
        st.markdown('<div class="cabang-dropdown">', unsafe_allow_html=True)
        st.markdown('<div class="cabang-dd-header">🏦 &nbsp; Pilih Unit Kerja</div>', unsafe_allow_html=True)
        for cabang in CABANG_LIST:
            is_active = cabang == st.session_state.selected_cabang
            css_class = "cabang-dd-item cabang-dd-item-active" if is_active else "cabang-dd-item"
            check = "✓" if is_active else ""
            # render label + check via HTML, button to capture click
            st.markdown(f'<div class="{css_class}" style="margin-bottom:2px;">'
                        f'<span>{cabang}</span>'
                        f'<span class="cabang-dd-check">{check}</span>'
                        f'</div>', unsafe_allow_html=True)
            if st.button(cabang, key=f"dd_{cabang}", use_container_width=True):
                st.session_state.selected_cabang = cabang
                st.session_state.show_cabang_dd = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ===== FILTER TABS =====
fc1, fc2, _ = st.columns([0.3, 0.5, 2])
with fc1:
    st.selectbox("", ["Bulan Ini", "Tahun Ini"], label_visibility="collapsed")
with fc2:
    st.selectbox("", ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"], label_visibility="collapsed")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ===== KPI CARDS =====
k_cols = st.columns(5, gap="small")
for i, kpi in enumerate(data["kpis"]):
    with k_cols[i]:
        delta_class = "kpi-delta-pos" if kpi["pos"] else "kpi-delta-neg"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{kpi['label']}</div>
            <div class="kpi-value">{kpi['value']}</div>
            <span class="{delta_class}">{kpi['delta']}</span>            
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ===== GROWTH CHART + KEY RESULT =====
col_chart, col_table = st.columns([2, 1], gap="medium")

with col_chart:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:4px;margin-bottom:16px;">
        <span style="font-weight:700;font-size:15px;color:var(--text-primary);margin-right:12px;">Growth Performance</span>
        <span class="tab-active">Bulan Ini</span>
        <span class="tab-inactive">All Performance</span>
    </div>
    """, unsafe_allow_html=True)

    days = ["Mon\n15", "Tue\n16", "Wed\n17", "Thu\n18", "Fri\n19", "Sat\n20", "Sun\n21"]
    values = data["chart_values"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=values,
        mode='lines+markers',
        line=dict(color='#1677ff', width=2.5, shape='spline'),
        marker=dict(size=6, color='#1677ff', line=dict(width=2, color='white')),
        fill='tozeroy', fillcolor='rgba(22,119,255,0.08)',
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=220,
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11, color='#8c8c8c'), tickmode='array', tickvals=days),
        yaxis=dict(showgrid=True, gridcolor='#f5f5f5', zeroline=False, tickfont=dict(size=11, color='#8c8c8c'), nticks=6),
        hovermode='x unified',
        hoverlabel=dict(bgcolor='#1677ff', font_color='white', bordercolor='#1677ff'),
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_table:
    rows_html = ""
    for i, kr in enumerate(data["key_results"], 1):
        color_class = f"score-{kr['color']}"
        rows_html += f"""
        <tr>
            <td style="color:var(--text-muted);">{i}</td>
            <td>{kr['name']}</td>
            <td class="{color_class}">{kr['skor']}</td>
            <td>{kr['avg']}</td>
        </tr>"""

    st.markdown(f"""
    <div class="section-card">
        <div style="font-weight:700;font-size:15px;color:var(--text-primary);margin-bottom:14px;">Key Result Cabang</div>
        <table class="key-result-table">
            <thead><tr>
                <th>#</th><th>Key Result</th><th>Skor Cabang</th><th>Avg Region</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ===== KPI DETAIL TABLE =====
kpi_detail_data = fetch_kpi_detail()

# Group variables by category
from collections import OrderedDict
category_groups = OrderedDict()
for row in kpi_detail_data:
    cat_name = row["key_result_name"]
    if cat_name not in category_groups:
        category_groups[cat_name] = []
    category_groups[cat_name].append(row)

# Build table body HTML
tbody_html = ""
for cat_name, variables in category_groups.items():
    tbody_html += f'<tr class="category-header"><td colspan="7"># &nbsp; {cat_name.title()}</td></tr>\n'
    for idx, var in enumerate(variables, 1):
        weight_pct = f"{var['weight'] * 100:.1f}%" if var['weight'] else "-"
        tbody_html += (
            f'<tr>'
            f'<td>{idx}</td>'
            f'<td style="text-align:left">{var["variable_name"].title()}</td>'
            f'<td></td>'
            f'<td></td>'
            f'<td></td>'
            f'<td>{weight_pct}</td>'
            f'<td>-</td>'
            f'</tr>\n'
        )

st.markdown(f"""
<div class="kpi-table-wrapper">
    <div style="font-weight:700;font-size:15px;color:var(--text-primary);margin-bottom:16px;">Key Performance Indikator</div>
    <table class="kpi-detail-table">
        <thead>
            <tr><th>#</th><th>Indikator</th><th>Real/Growth</th><th>Target</th><th>Real %</th><th>Bobot</th><th>Skor</th></tr>
        </thead>
        <tbody>
            {tbody_html}</tbody></table>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)