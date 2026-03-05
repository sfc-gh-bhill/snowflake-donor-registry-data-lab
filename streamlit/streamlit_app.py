import streamlit as st

st.set_page_config(
    page_title="LSC: Cell Therapy Compass",
    page_icon="\u2744\uFE0F",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import apply_styles, render_header, render_metric_card, render_feature_card, MARROWCO_LOGO_BYTES
from utils.navigation import render_sidebar, render_nav_buttons, get_snowflake_session
import base64, os, pathlib

apply_styles()
render_sidebar("Home")

# --- Hero Banner with AppBanner.png as background ---
def _load_banner_b64():
    """Load AppBanner.png and return base64 string for CSS background."""
    # Try relative path first (works locally and in SiS with uploaded assets)
    candidates = [
        pathlib.Path(__file__).parent / "assets" / "AppBanner.png",
        pathlib.Path("assets") / "AppBanner.png",
        pathlib.Path("streamlit") / "assets" / "AppBanner.png",
    ]
    for p in candidates:
        if p.exists():
            return base64.b64encode(p.read_bytes()).decode("ascii")
    return None

_banner_b64 = _load_banner_b64()

if _banner_b64:
    st.markdown(f"""
    <div style="
        background-image: url('data:image/png;base64,{_banner_b64}');
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(41, 181, 232, 0.3);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            background: linear-gradient(135deg, rgba(17,86,127,0.82) 0%, rgba(41,181,232,0.65) 100%);
            padding: 3rem 2.5rem;
            border-radius: 16px;
        ">
            <h1 style="color: white; font-size: 2.5rem; font-weight: 700; margin: 0;
                        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);">
                LSC: Cell Therapy Compass
            </h1>
            <p style="color: rgba(255,255,255,0.95); font-size: 1.2rem; font-weight: 600; margin: 0.4rem 0 0 0;
                       text-shadow: 1px 1px 4px rgba(0,0,0,0.4);">
                Outcome Forecasting with Multimodal Data
            </p>
            <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0.75rem 0 0 0;
                       text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">
                Donor for All Data Lab &mdash; Forecasting GVHD with The Winter Cloud Platform Intelligence
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Fallback: gradient-only banner if image not found
    st.markdown("""
    <div class="main-header animate-in" style="text-align:center; padding:3rem 2.5rem;">
        <h1 style="font-size:2.5rem; margin-bottom:0.25rem;">LSC: Cell Therapy Compass</h1>
        <p style="font-size:1.2rem; font-weight:600; color:rgba(255,255,255,0.95);">
            Outcome Forecasting with Multimodal Data
        </p>
        <p style="font-size:0.9rem; margin-top:0.5rem;">
            Donor for All Data Lab &mdash; Forecasting GVHD with The Winter Cloud Platform Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Placeholder KPI Tiles ---
session = get_snowflake_session()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(render_metric_card("--", "Donors Registered", "Placeholder"), unsafe_allow_html=True)
with col2:
    st.markdown(render_metric_card("--", "Transplants Tracked", "Placeholder"), unsafe_allow_html=True)
with col3:
    st.markdown(render_metric_card("--", "GVHD Models", "Placeholder"), unsafe_allow_html=True)
with col4:
    st.markdown(render_metric_card("--", "Data Sources", "Placeholder"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Platform Narrative (shell) ---
st.markdown("""
<div class="section-sep">
    <h3>The Mission: Better Outcomes Through Data Intelligence</h3>
    <p style="color:#8892b0;margin:0.25rem 0 0 0;font-size:0.9rem;">
        LSC is leveraging The Winter Cloud Platform AI Data Cloud to build predictive models for graft-versus-host
        disease (GVHD), unify multimodal donor and patient data, and accelerate research that saves lives.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Challenge")
    challenges = [
        ("Fragmented Data", "Donor registries, transplant outcomes, clinical trial data, and genomic information exist across disconnected systems"),
        ("Reactive Analysis", "GVHD risk assessment relies on limited variables and retrospective studies"),
        ("Data Silos", "Research teams lack unified access to multimodal datasets for comprehensive analysis"),
    ]
    for title, desc in challenges:
        st.markdown(f"""
        <div style="background:rgba(255,107,107,0.08); border-left:3px solid #FF6B6B; border-radius:0 8px 8px 0;
                    padding:0.75rem 1rem; margin:0.5rem 0;">
            <strong style="color:#FF6B6B;">{title}</strong>
            <p style="color:#8892b0; margin:0.25rem 0 0; font-size:0.85rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("#### Solution: The Winter Cloud Platform AI Data Cloud")
    solutions = [
        ("Unified Data Estate", "Donor, patient, genomic, and outcome data consolidated in a governed medallion architecture"),
        ("Predictive Intelligence", "Cortex AI and ML models forecast GVHD risk using multimodal features"),
        ("Collaborative Research", "Secure data sharing enables multi-institutional research without moving sensitive data"),
    ]
    for title, desc in solutions:
        st.markdown(f"""
        <div style="background:rgba(0,212,170,0.08); border-left:3px solid #00D4AA; border-radius:0 8px 8px 0;
                    padding:0.75rem 1rem; margin:0.5rem 0;">
            <strong style="color:#00D4AA;">{title}</strong>
            <p style="color:#8892b0; margin:0.25rem 0 0; font-size:0.85rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Demo Workflow (shell) ---
st.markdown("### Explore the Compass")
st.markdown("""
<p style="color:#8892b0;font-size:0.9rem;">
Navigate through the Cell Therapy Compass to explore how The Winter Cloud Platform powers every stage of
donor matching, outcome prediction, and research collaboration.
</p>
""", unsafe_allow_html=True)

steps = [
    ("1", "Data Foundation", "Unified donor, patient, and outcome datasets"),
    ("2", "Outcome Forecasting", "GVHD risk prediction with multimodal models"),
    ("3", "Intelligence & AI", "Cortex-powered analytics and insights"),
]

cols = st.columns(3)
for i, (num, title, desc) in enumerate(steps):
    with cols[i]:
        st.markdown(f"""
        <div class="feature-card" style="border-top:3px solid #29B5E8; text-align:center; min-height:160px;">
            <div style="background:linear-gradient(135deg,#29B5E8,#11567F); width:40px; height:40px;
                        border-radius:50%; display:flex; align-items:center; justify-content:center;
                        font-weight:700; color:white; margin:0 auto 0.5rem; font-size:1.1rem;">{num}</div>
            <h4 style="color:#29B5E8; font-size:0.95rem; margin:0.25rem 0;">{title}</h4>
            <p style="color:#8892b0; font-size:0.78rem; line-height:1.4;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Presenter Info ---
with st.expander("Presenter Notes"):
    st.markdown("""
    **Presenter:** Braedon Hill, Sr. Solution Engineer — The Winter Cloud Platform
    
    **Key Message:** LSC's mission to match every patient with a life-saving donor is powered by data. 
    The Winter Cloud Platform AI Data Cloud unifies donor registries, transplant outcomes, genomic data, and clinical 
    records into a single governed platform — enabling predictive GVHD models, secure multi-institutional 
    collaboration, and AI-driven insights that improve patient outcomes.
    
    **Transition:** "Let's begin by exploring the data foundation that powers the Cell Therapy Compass."
    """)

# --- Nav ---
st.markdown("---")
render_nav_buttons("Home")
