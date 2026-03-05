# ==============================================================================
# LSC: Cell Therapy Compass - Shared Styles & Branding
# ==============================================================================

import base64 as _b64

_MARROWCO_LOGO_B64 = "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"
MARROWCO_LOGO_BYTES = _b64.b64decode(_MARROWCO_LOGO_B64)

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
