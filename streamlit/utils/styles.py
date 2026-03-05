# ==============================================================================
# LSC: Cell Therapy Compass - Shared Styles & Branding
# ==============================================================================

SHARED_CSS = """
<style>
    :root {
        --primary-color: #29B5E8;
        --sf-blue-dark: #11567F;
        --sf-blue-light: #29B5E8;
        --accent-color: #00D4AA;
        --warning-color: #FF6B6B;
        --success-color: #4ECDC4;
        --background-dark: #0E1117;
        --card-background: #1E2130;
        --text-light: #FAFAFA;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent !important;
        backdrop-filter: none !important;
    }
    header[data-testid="stHeader"] [data-testid="stToolbar"] { visibility: hidden; }
    .main .block-container { padding-top: 1rem; padding-bottom: 2rem; }
    .main-header {
        background: linear-gradient(135deg, #29B5E8 0%, #11567F 100%);
        padding: 1.5rem 2rem; border-radius: 16px; margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(41, 181, 232, 0.3);
        position: relative; overflow: hidden;
    }
    .main-header::before {
        content: ''; position: absolute;
        top: 0; left: -100%; width: 200%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    @keyframes shimmer { 0% { transform: translateX(-50%); } 100% { transform: translateX(50%); } }
    .main-header h1 {
        color: white; font-size: 2rem; font-weight: 700; margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2); position: relative;
    }
    .main-header p { color: rgba(255,255,255,0.9); font-size: 1rem; margin: 0.5rem 0 0 0; position: relative; }
    h2, h3 { color: #FAFAFA; border-bottom: 2px solid rgba(41, 181, 232, 0.3); padding-bottom: 0.5rem; }
    .metric-card {
        background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%);
        border-radius: 16px; padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 12px 48px rgba(41, 181, 232, 0.2); }
    .metric-value {
        font-size: 2.2rem; font-weight: 800;
        background: linear-gradient(135deg, #29B5E8 0%, #00D4AA 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0;
    }
    .metric-label { color: #8892b0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.5rem; }
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%);
        border-radius: 16px; padding: 1rem 1.25rem;
        border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    [data-testid="metric-container"] label { color: #8892b0 !important; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #29B5E8 !important; font-weight: 700; }
    .feature-card {
        background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%);
        border-radius: 16px; padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease; height: 100%;
    }
    .feature-card:hover { transform: translateY(-5px); box-shadow: 0 12px 48px rgba(41, 181, 232, 0.2); }
    .feature-card h4 { color: #29B5E8; margin: 0.5rem 0; font-size: 1.1rem; }
    .feature-card p { color: #8892b0; font-size: 0.9rem; line-height: 1.5; }
    .feature-icon { font-size: 2rem; margin-bottom: 0.25rem; }
    .status-badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .status-valid { background: rgba(78,205,196,0.2); color: #4ECDC4; }
    .status-warning { background: rgba(255,183,77,0.2); color: #FFB74D; }
    .status-error { background: rgba(255,107,107,0.2); color: #FF6B6B; }
    .status-info { background: rgba(41,181,232,0.2); color: #29B5E8; }
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1117 0%, #161b22 100%); }
    [data-testid="stSidebar"] * { color: #FAFAFA !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent; }
    .stTabs [data-baseweb="tab"] { background: rgba(255,255,255,0.05); border-radius: 8px; padding: 0.5rem 1rem; color: #8892b0; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #29B5E8 0%, #11567F 100%); color: white; }
    .stButton > button {
        background: linear-gradient(135deg, #29B5E8 0%, #00D4AA 100%);
        color: white; border: none; padding: 0.6rem 1.25rem; border-radius: 8px; font-weight: 600; transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: scale(1.02); box-shadow: 0 8px 24px rgba(41,181,232,0.4); }
    .pipeline-step {
        background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%);
        border-radius: 12px; padding: 1rem 1.25rem; margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center;
    }
    .pipeline-step-number {
        background: linear-gradient(135deg, #29B5E8 0%, #11567F 100%);
        width: 32px; height: 32px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; margin-right: 1rem; color: white; flex-shrink: 0;
    }
    .section-sep {
        background: linear-gradient(135deg, rgba(41,181,232,0.1), rgba(0,212,170,0.1));
        border-radius: 12px; padding: 1.25rem 1.5rem; margin: 1.5rem 0; border-left: 4px solid #29B5E8;
    }
    .section-sep h3 { border: none; padding: 0; margin: 0; color: #29B5E8; font-size: 1rem; }
    .sql-block {
        background: #0d1117; border: 1px solid rgba(41,181,232,0.3);
        border-radius: 12px; padding: 1rem 1.25rem;
        font-family: 'Courier New', monospace; font-size: 0.85rem; overflow-x: auto; color: #e6edf3;
    }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .animate-in { animation: fadeIn 0.5s ease-out forwards; }
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #29B5E8; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #11567F; }
    hr { border: none; height: 1px; background: linear-gradient(90deg, rgba(41,181,232,0.5), transparent); margin: 1.5rem 0; }
    .info-callout { background: rgba(41,181,232,0.08); border-left: 4px solid #29B5E8; border-radius: 0 12px 12px 0; padding: 1rem 1.25rem; margin: 1rem 0; }
    .info-callout h4 { color: #29B5E8; margin: 0 0 0.5rem 0; font-size: 0.95rem; }
    .info-callout p { color: #8892b0; margin: 0; font-size: 0.85rem; line-height: 1.5; }
    .success-callout { background: rgba(0,212,170,0.08); border-left: 4px solid #00D4AA; border-radius: 0 12px 12px 0; padding: 1rem 1.25rem; margin: 1rem 0; }
    .success-callout h4 { color: #00D4AA; margin: 0 0 0.5rem 0; font-size: 0.95rem; }
    .success-callout p { color: #8892b0; margin: 0; font-size: 0.85rem; line-height: 1.5; }
    .warning-callout { background: rgba(255,107,107,0.08); border-left: 4px solid #FF6B6B; border-radius: 0 12px 12px 0; padding: 1rem 1.25rem; margin: 1rem 0; }
    .warning-callout h4 { color: #FF6B6B; margin: 0 0 0.5rem 0; font-size: 0.95rem; }
    .warning-callout p { color: #8892b0; margin: 0; font-size: 0.85rem; line-height: 1.5; }
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    .stDataFrame [data-testid="stTable"] { background: #1a1f35; }
</style>
"""


def apply_styles():
    """Apply shared styles to a Streamlit page."""
    import streamlit as st
    st.markdown(SHARED_CSS, unsafe_allow_html=True)


def render_header(title: str, subtitle: str, icon: str = ""):
    """Render a styled page header with shimmer animation."""
    import streamlit as st
    st.markdown(f"""
    <div class="main-header animate-in">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(value: str, label: str, delta: str = "", delta_type: str = "positive"):
    """Return HTML for a styled metric card."""
    delta_color = "#4ECDC4" if delta_type == "positive" else "#FF6B6B"
    delta_html = f'<p style="color:{delta_color};font-size:0.8rem;">{delta}</p>' if delta else ''
    return f"""
    <div class="metric-card">
        <p class="metric-value">{value}</p>
        <p class="metric-label">{label}</p>
        {delta_html}
    </div>
    """


def render_feature_card(icon: str, title: str, description: str, accent: str = "#29B5E8"):
    """Return HTML for a feature/pillar card."""
    return f"""
    <div class="feature-card" style="border-top: 3px solid {accent};">
        <div class="feature-icon">{icon}</div>
        <h4 style="color: {accent};">{title}</h4>
        <p>{description}</p>
    </div>
    """


def render_status_badge(status: str, text: str):
    """Render a status badge."""
    return f'<span class="status-badge status-{status}">{text}</span>'


def render_section_separator(title: str, description: str = ""):
    """Render a section separator with title."""
    desc_html = f'<p style="color:#8892b0;margin:0.25rem 0 0 0;font-size:0.9rem;">{description}</p>' if description else ''
    return f"""
    <div class="section-sep">
        <h3>{title}</h3>
        {desc_html}
    </div>
    """


def render_sql_block(sql: str):
    """Return HTML for a styled SQL code block."""
    import html
    escaped = html.escape(sql)
    return f'<div class="sql-block"><pre style="margin:0;white-space:pre-wrap;">{escaped}</pre></div>'


def render_info_callout(title: str, text: str):
    """Return HTML for an info callout box."""
    return f'<div class="info-callout"><h4>{title}</h4><p>{text}</p></div>'


def render_success_callout(title: str, text: str):
    """Return HTML for a success callout box."""
    return f'<div class="success-callout"><h4>{title}</h4><p>{text}</p></div>'


def render_warning_callout(title: str, text: str):
    """Return HTML for a warning callout box."""
    return f'<div class="warning-callout"><h4>{title}</h4><p>{text}</p></div>'


def render_pipeline_step(number: int, title: str, description: str, accent: str = "#29B5E8"):
    """Return HTML for a pipeline step."""
    return f"""
    <div class="pipeline-step">
        <div class="pipeline-step-number" style="background:linear-gradient(135deg,{accent},#11567F);">{number}</div>
        <div>
            <strong style="color:{accent};">{title}</strong>
            <p style="color:#8892b0;margin:0.25rem 0 0;font-size:0.85rem;">{description}</p>
        </div>
    </div>
    """

# ── Acronym Tooltip Definitions ──
ACRONYM_MAP = {
    "GVHD": "Graft-versus-Host Disease",
    "HCT": "Hematopoietic Cell Transplantation",
    "LSC": "The Life Saving Company (fictional)",
    "PTCy": "Post-Transplant Cyclophosphamide",
    "MMUD": "Mismatched Unrelated Donor (7/8 HLA match)",
    "MUD": "Matched Unrelated Donor (8/8 HLA match)",
    "HAPLO": "Haploidentical Donor (half-matched, usually family)",
    "SVI": "Social Vulnerability Index",
    "HLA": "Human Leukocyte Antigen",
    "OS": "Overall Survival",
    "DLI": "Donor Lymphocyte Infusion",
    "AML": "Acute Myeloid Leukemia",
    "ALL": "Acute Lymphoblastic Leukemia",
    "MDS": "Myelodysplastic Syndromes",
    "TBI": "Total Body Irradiation",
    "MAC": "Myeloablative Conditioning",
    "RIC": "Reduced Intensity Conditioning",
}


def tooltip(abbr: str) -> str:
    """Return an HTML <abbr> tag with hover tooltip for a clinical acronym."""
    full = ACRONYM_MAP.get(abbr, abbr)
    return (
        f'<abbr title="{full}" style="text-decoration: underline dotted #29B5E8; "'
        f'cursor: help; color: inherit; font-weight: inherit;">{abbr}</abbr>'
    )
