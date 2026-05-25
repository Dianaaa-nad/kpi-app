import streamlit as st

st.set_page_config(layout="wide", page_title="Import Data Real/Growth", page_icon="📥")

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* ── Light-theme defaults ── */
    :root {
        --bg-body: #f5f6fa;
        --bg-card: #fff;
        --text-primary: #1a1a2e;
        --text-secondary: #262626;
        --text-muted: #8c8c8c;
        --text-soft: #595959;
        --border-card: #f0f2f5;
        --border-light: #f0f0f0;
        --border-input: #d9d9d9;
        --shadow-card: 0 1px 4px rgba(0,0,0,0.05);
        --hr-color: #f0f0f0;
        --cat-header-bg: #fafafa;
        --accent: #1677ff;
        --accent-light: #e6f4ff;
        --accent-border: #91caff;
        --success: #52c41a;
        --success-bg: #f6ffed;
        --success-border: #b7eb8f;
        --warning-bg: #fffbe6;
        --warning-border: #ffe58f;
        --warning-text: #d48806;
    }

    /* ── Dark-theme overrides ── */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-body: #0e1117;
            --bg-card: #1a1d24;
            --text-primary: #e6e8ec;
            --text-secondary: #cfd2d6;
            --text-muted: #8b8fa3;
            --text-soft: #a0a4b0;
            --border-card: #2a2d35;
            --border-light: #2a2d35;
            --border-input: #3a3d45;
            --shadow-card: 0 1px 6px rgba(0,0,0,0.30);
            --hr-color: #2a2d35;
            --cat-header-bg: #1e2128;
            --accent: #4096ff;
            --accent-light: #111d2c;
            --accent-border: #15395b;
            --success: #73d13d;
            --success-bg: #162312;
            --success-border: #274916;
            --warning-bg: #2b2111;
            --warning-border: #594214;
            --warning-text: #d48806;
        }
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
    }

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: var(--bg-body);
    }
    .stApp { background-color: var(--bg-body); }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .main .block-container { padding-top: 2rem; padding-left: 2.5rem; padding-right: 2.5rem; max-width: 100%; }

    /* ── Import page specific ── */
    .import-header {
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 8px;
    }
    .import-header-icon {
        width: 44px; height: 44px; border-radius: 12px;
        background: linear-gradient(135deg, #1677ff 0%, #4096ff 100%);
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; color: white;
        box-shadow: 0 4px 12px rgba(22,119,255,0.25);
    }
    .import-header-text h1 {
        font-size: 22px; font-weight: 700; color: var(--text-primary);
        margin: 0; line-height: 1.3;
    }
    .import-header-text p {
        font-size: 13px; color: var(--text-muted); margin: 0;
    }

    .import-card {
        background: var(--bg-card); border: 1px solid var(--border-card);
        border-radius: 14px; padding: 24px 28px;
        box-shadow: var(--shadow-card);
        margin-bottom: 20px;
    }
    .import-card-title {
        font-size: 15px; font-weight: 700; color: var(--text-primary);
        margin-bottom: 6px; display: flex; align-items: center; gap: 8px;
    }
    .import-card-desc {
        font-size: 12.5px; color: var(--text-muted); margin-bottom: 18px;
    }

    /* Upload zone */
    .upload-zone {
        border: 2px dashed var(--border-input);
        border-radius: 12px; padding: 40px 20px;
        text-align: center;
        background: var(--bg-body);
        transition: all 0.25s ease;
    }
    .upload-zone-icon { font-size: 40px; margin-bottom: 10px; opacity: 0.7; }
    .upload-zone-text { font-size: 14px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }
    .upload-zone-hint { font-size: 12px; color: var(--text-muted); }
    .upload-zone-formats { display: flex; gap: 8px; justify-content: center; margin-top: 14px; }
    .format-badge { font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 6px; letter-spacing: 0.3px; }
    .format-xlsx { background: #e6f4ff; color: #1677ff; border: 1px solid #91caff; }
    .format-csv { background: #f6ffed; color: #389e0d; border: 1px solid #b7eb8f; }
    @media (prefers-color-scheme: dark) {
        .format-xlsx { background: #111d2c; color: #4096ff; border-color: #15395b; }
        .format-csv  { background: #162312; color: #73d13d; border-color: #274916; }
    }

    /* Template card */
    .template-card {
        display: flex; align-items: center; gap: 14px;
        padding: 14px 18px; border-radius: 10px;
        border: 1px solid var(--border-light); background: var(--bg-body);
        margin-bottom: 10px; transition: all 0.2s;
    }
    .template-card:hover { border-color: var(--accent); box-shadow: 0 2px 8px rgba(22,119,255,0.08); }
    .template-icon {
        width: 36px; height: 36px; border-radius: 8px;
        display: flex; align-items: center; justify-content: center; font-size: 18px;
    }
    .template-icon-xlsx { background: #e6f4ff; color: #1677ff; }
    .template-icon-csv  { background: #f6ffed; color: #389e0d; }
    @media (prefers-color-scheme: dark) {
        .template-icon-xlsx { background: #111d2c; color: #4096ff; }
        .template-icon-csv  { background: #162312; color: #73d13d; }
    }
    .template-info { flex: 1; }
    .template-name { font-size: 13px; font-weight: 600; color: var(--text-primary); }
    .template-desc { font-size: 11px; color: var(--text-muted); }
    .template-dl { font-size: 12px; font-weight: 600; color: var(--accent); cursor: pointer; }

    /* Preview table */
    .preview-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
    .preview-table th {
        font-size: 11px; color: var(--text-muted); font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.4px;
        padding: 10px 10px; border-bottom: 2px solid var(--border-light);
        text-align: center; background: var(--cat-header-bg);
        position: sticky; top: 0; z-index: 1;
    }
    .preview-table th:first-child { text-align: left; border-radius: 8px 0 0 0; }
    .preview-table th:last-child { border-radius: 0 8px 0 0; }
    .preview-table td {
        padding: 9px 10px; border-bottom: 1px solid var(--border-light);
        color: var(--text-secondary); text-align: center;
    }
    .preview-table td:first-child {
        text-align: left; font-weight: 600; color: var(--text-primary); white-space: nowrap;
    }
    .preview-table tr:last-child td { border-bottom: none; }
    .preview-table tr:hover td { background: var(--accent-light); }

    /* Status badge */
    .status-badge {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 6px 14px; border-radius: 8px; font-size: 12.5px; font-weight: 600;
    }
    .status-ready { background: var(--success-bg); color: var(--success); border: 1px solid var(--success-border); }

    /* Info strip */
    .info-strip {
        display: flex; gap: 24px; padding: 14px 20px;
        background: var(--accent-light); border: 1px solid var(--accent-border);
        border-radius: 10px; margin-bottom: 18px;
    }
    @media (prefers-color-scheme: dark) { .info-strip { border-color: #15395b; } }
    .info-strip-item { font-size: 12.5px; color: var(--text-soft); display: flex; align-items: center; gap: 6px; }
    .info-strip-value { font-weight: 700; color: var(--accent); }

    /* Action buttons */
    .action-row { display: flex; gap: 12px; justify-content: flex-end; margin-top: 20px; padding-top: 18px; border-top: 1px solid var(--border-light); }
    .btn-submit {
        padding: 10px 28px; border-radius: 10px; font-size: 13.5px; font-weight: 600;
        background: linear-gradient(135deg, #1677ff 0%, #4096ff 100%);
        color: white; border: none; cursor: pointer;
        box-shadow: 0 4px 12px rgba(22,119,255,0.25); transition: all 0.2s;
    }
    .btn-submit:hover { box-shadow: 0 6px 20px rgba(22,119,255,0.35); transform: translateY(-1px); }
    .btn-cancel {
        padding: 10px 28px; border-radius: 10px; font-size: 13.5px; font-weight: 600;
        background: var(--bg-card); color: var(--text-soft);
        border: 1px solid var(--border-input); cursor: pointer; transition: all 0.2s;
    }
    .btn-cancel:hover { border-color: var(--accent); color: var(--accent); }

    /* Step indicator */
    .steps { display: flex; gap: 0; margin-bottom: 28px; }
    .step { flex: 1; text-align: center; padding: 12px 8px; position: relative; }
    .step-number {
        width: 30px; height: 30px; border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 13px; font-weight: 700; margin-bottom: 6px;
    }
    .step-active .step-number { background: linear-gradient(135deg, #1677ff 0%, #4096ff 100%); color: white; box-shadow: 0 3px 10px rgba(22,119,255,0.3); }
    .step-done .step-number { background: var(--success); color: white; }
    .step-pending .step-number { background: var(--border-light); color: var(--text-muted); }
    .step-label { font-size: 11.5px; font-weight: 600; display: block; }
    .step-active .step-label { color: var(--accent); }
    .step-done .step-label { color: var(--success); }
    .step-pending .step-label { color: var(--text-muted); }

    /* Streamlit file uploader */
    [data-testid="stFileUploader"] {
        background: var(--bg-body); border: 2px dashed var(--border-input);
        border-radius: 12px; padding: 10px;
    }
    [data-testid="stFileUploader"]:hover { border-color: var(--accent); }

    /* Back link */
    .back-link {
        display: inline-flex; align-items: center; gap: 6px;
        font-size: 13px; font-weight: 500; color: var(--text-muted);
        text-decoration: none; margin-bottom: 20px; transition: color 0.2s;
    }
    .back-link:hover { color: var(--accent); }
</style>
""", unsafe_allow_html=True)


# ===== BACK NAVIGATION =====
st.markdown('<a class="back-link" href="/" target="_self">← Kembali ke Dashboard</a>', unsafe_allow_html=True)

# ===== PAGE HEADER =====
st.markdown("""
<div class="import-header">
    <div class="import-header-icon">📥</div>
    <div class="import-header-text">
        <h1>Import Data Real/Growth</h1>
        <p>Upload file Excel atau CSV untuk mengisi nilai real/growth tiap indikator per cabang</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ===== STEP INDICATOR =====
st.markdown("""
<div class="steps">
    <div class="step step-active">
        <span class="step-number">1</span>
        <span class="step-label">Pilih Periode</span>
    </div>
    <div class="step step-pending">
        <span class="step-number">2</span>
        <span class="step-label">Upload File</span>
    </div>
    <div class="step step-pending">
        <span class="step-number">3</span>
        <span class="step-label">Preview Data</span>
    </div>
    <div class="step step-pending">
        <span class="step-number">4</span>
        <span class="step-label">Submit</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== PERIODE SELECTION =====
st.markdown("""
<div class="import-card">
    <div class="import-card-title">📅 Pilih Periode</div>
    <div class="import-card-desc">Tentukan bulan dan tahun untuk data yang akan diimport</div>
""", unsafe_allow_html=True)

col_month, col_year, _ = st.columns([1, 1, 3])
with col_month:
    st.selectbox(
        "Bulan",
        ["Januari","Februari","Maret","April","Mei","Juni",
         "Juli","Agustus","September","Oktober","November","Desember"],
        index=4, key="import_month"
    )
with col_year:
    st.selectbox("Tahun", [2026, 2025, 2024], key="import_year")

st.markdown("</div>", unsafe_allow_html=True)

# ===== TWO COLUMN LAYOUT: Upload + Template =====
col_upload, col_template = st.columns([3, 2], gap="medium")

with col_upload:
    st.markdown("""
    <div class="import-card">
        <div class="import-card-title">📤 Upload File</div>
        <div class="import-card-desc">Upload file Excel (.xlsx) atau CSV (.csv) berisi data real/growth per cabang</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="upload-zone">
        <div class="upload-zone-icon">☁️</div>
        <div class="upload-zone-text">Drag & drop file di sini</div>
        <div class="upload-zone-hint">atau klik tombol di bawah untuk browse file</div>
        <div class="upload-zone-formats">
            <span class="format-badge format-xlsx">.XLSX</span>
            <span class="format-badge format-csv">.CSV</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.file_uploader("Upload file", type=["xlsx", "csv"], label_visibility="collapsed", key="import_file")
    st.markdown("</div>", unsafe_allow_html=True)

with col_template:
    st.markdown("""
    <div class="import-card" style="height: calc(100% - 20px);">
        <div class="import-card-title">📋 Template File</div>
        <div class="import-card-desc">Download template sesuai format yang dibutuhkan</div>
        <div class="template-card">
            <div class="template-icon template-icon-xlsx">📊</div>
            <div class="template-info">
                <div class="template-name">Template Excel (.xlsx)</div>
                <div class="template-desc">Format spreadsheet dengan header var_code</div>
            </div>
            <span class="template-dl">⬇ Download</span>
        </div>
        <div class="template-card">
            <div class="template-icon template-icon-csv">📄</div>
            <div class="template-info">
                <div class="template-name">Template CSV (.csv)</div>
                <div class="template-desc">Format comma-separated values</div>
            </div>
            <span class="template-dl">⬇ Download</span>
        </div>
        <div style="margin-top:18px; padding:14px 16px; background:var(--warning-bg); border:1px solid var(--warning-border); border-radius:10px;">
            <div style="font-size:12px; font-weight:600; color:var(--warning-text); margin-bottom:6px;">⚠️ Panduan Format</div>
            <ul style="font-size:11.5px; color:var(--text-soft); margin:0; padding-left:18px; line-height:1.8;">
                <li>Baris = Nama Cabang</li>
                <li>Kolom = Kode Variabel (CM, FBI, ACE, dst.)</li>
                <li>Bisa import per cabang atau semua cabang sekaligus</li>
                <li>Nama cabang harus sesuai dengan database</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ===== PREVIEW TABLE (Static Dummy Data) =====
st.markdown("""
<div class="import-card">
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">
        <div class="import-card-title">📊 Preview Data</div>
        <span class="status-badge status-ready">✓ 5 cabang terdeteksi</span>
    </div>
    <div class="import-card-desc">Preview data yang akan diimport ke database</div>
    <div class="info-strip">
        <div class="info-strip-item">📅 Periode: <span class="info-strip-value">Mei 2026</span></div>
        <div class="info-strip-item">🏦 Cabang: <span class="info-strip-value">5</span></div>
        <div class="info-strip-item">📋 Variabel: <span class="info-strip-value">17</span></div>
        <div class="info-strip-item">📊 Total Data: <span class="info-strip-value">85 cells</span></div>
    </div>
    <div style="overflow-x:auto; border-radius:10px; border:1px solid var(--border-light);">
        <table class="preview-table">
            <thead>
                <tr>
                    <th style="min-width:220px">Cabang</th>
                    <th>CM</th><th>FBI</th><th>ACE</th><th>TAB</th>
                    <th>GIRO</th><th>DEPOSITO</th><th>DGT</th><th>PBY</th>
                    <th>GOLD</th><th>SMG</th><th>DG</th><th>NPF</th>
                    <th>KOL2</th><th>ALL_CUST</th><th>CUST_PAY</th><th>PNS</th><th>MIKRO</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>KC BANJARMASIN LAMBUNG MANGKURAT</td>
                    <td>120.5</td><td>45.2</td><td>30.0</td><td>500</td>
                    <td>200</td><td>85.0</td><td>150</td><td>300</td>
                    <td>50.5</td><td>75.3</td><td>2.5</td><td>1.8</td>
                    <td>3.2</td><td>200</td><td>80</td><td>88.5</td><td>120</td>
                </tr>
                <tr>
                    <td>KC MARTAPURA</td>
                    <td>95.0</td><td>38.0</td><td>22.0</td><td>400</td>
                    <td>180</td><td>70.0</td><td>120</td><td>250</td>
                    <td>40.0</td><td>60.0</td><td>3.1</td><td>2.0</td>
                    <td>4.0</td><td>150</td><td>60</td><td>82.0</td><td>100</td>
                </tr>
                <tr>
                    <td>KCP BANJARMASIN KAYU TANGI</td>
                    <td>88.3</td><td>32.1</td><td>18.5</td><td>350</td>
                    <td>140</td><td>55.0</td><td>95</td><td>180</td>
                    <td>30.2</td><td>48.7</td><td>4.2</td><td>2.5</td>
                    <td>5.1</td><td>120</td><td>45</td><td>75.0</td><td>80</td>
                </tr>
                <tr>
                    <td>KCP BANJARMASIN GATOT SUBROTO</td>
                    <td>75.0</td><td>28.4</td><td>15.0</td><td>280</td>
                    <td>110</td><td>48.0</td><td>80</td><td>150</td>
                    <td>22.0</td><td>35.5</td><td>5.0</td><td>3.2</td>
                    <td>6.3</td><td>90</td><td>35</td><td>70.0</td><td>65</td>
                </tr>
                <tr>
                    <td>KC TAPIN</td>
                    <td>110.2</td><td>42.5</td><td>28.0</td><td>480</td>
                    <td>190</td><td>82.0</td><td>140</td><td>280</td>
                    <td>48.0</td><td>70.0</td><td>2.0</td><td>1.5</td>
                    <td>2.8</td><td>180</td><td>75</td><td>90.0</td><td>115</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="action-row">
        <button class="btn-cancel">❌ Cancel</button>
        <button class="btn-submit">✅ Submit Import</button>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
