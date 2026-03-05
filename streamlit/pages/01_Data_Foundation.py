import streamlit as st

st.set_page_config(page_title="Data Foundation | LSC", page_icon="❄️", layout="wide")

from utils.styles import (
    apply_styles, render_header, render_metric_card, render_pipeline_step,
    render_info_callout, render_success_callout, render_sql_block, render_section_separator
)
from utils.navigation import render_sidebar, render_nav_buttons, get_snowflake_session
import streamlit.components.v1 as components

apply_styles()
render_sidebar("Data Foundation")

render_header("Data Foundation", "Bronze → Silver → Gold Pipeline with Dynamic Tables")

# ── Try to load live data ──
session = get_snowflake_session()

if session:
    try:
        tx_count = session.sql("SELECT COUNT(*) FROM MARROWCO_DONOR_LAB.HOL.TRANSPLANT_OUTCOMES").collect()[0][0]
        note_count = session.sql("SELECT COUNT(*) FROM MARROWCO_DONOR_LAB.HOL.CLINICAL_NOTES").collect()[0][0]
        dt_count = session.sql("SELECT COUNT(*) FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED").collect()[0][0]
        donor_types = session.sql(
            "SELECT DONOR_TYPE, COUNT(*) AS CNT FROM MARROWCO_DONOR_LAB.HOL.TRANSPLANT_OUTCOMES GROUP BY 1 ORDER BY 2 DESC"
        ).to_pandas()
        live_data = True
    except Exception:
        live_data = False
else:
    live_data = False

# ── KPI Tiles ──
col1, col2, col3, col4 = st.columns(4)
with col1:
    val = f"{tx_count:,}" if live_data else "500"
    st.markdown(render_metric_card(val, "Transplant Records", "Bronze Layer"), unsafe_allow_html=True)
with col2:
    val = f"{note_count:,}" if live_data else "800"
    st.markdown(render_metric_card(val, "Clinical Notes", "Unstructured"), unsafe_allow_html=True)
with col3:
    val = f"{dt_count:,}" if live_data else "500"
    st.markdown(render_metric_card(val, "Enriched Records", "Silver Layer"), unsafe_allow_html=True)
with col4:
    st.markdown(render_metric_card("4", "Donor Types", "MUD, MMUD, HAPLO, CORD"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Architecture Diagram ──
st.markdown(render_section_separator(
    "Data Architecture",
    "Medallion architecture powered by Dynamic Tables for near real-time analytics"
), unsafe_allow_html=True)

components.html("""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body { margin: 0; padding: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; }</style>
</head><body>
<div style="background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%); border-radius: 16px;
            padding: 2rem; border: 1px solid rgba(255,255,255,0.1); margin: 0;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div style="flex: 1; min-width: 200px; text-align: center;">
            <div style="background: linear-gradient(135deg, #CD7F32, #8B4513); padding: 1.25rem;
                        border-radius: 12px; margin-bottom: 0.5rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">&#x1F949;</div>
                <div style="color: white; font-weight: 700; font-size: 1rem;">Bronze Layer</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.75rem; margin-top: 0.25rem;">Raw Data</div>
            </div>
            <div style="color: #8892b0; font-size: 0.7rem;">
                TRANSPLANT_OUTCOMES<br>CLINICAL_NOTES
            </div>
        </div>
        <div style="color: #29B5E8; font-size: 2rem; font-weight: 700;">&rarr;</div>
        <div style="flex: 1; min-width: 200px; text-align: center;">
            <div style="background: linear-gradient(135deg, #C0C0C0, #808080); padding: 1.25rem;
                        border-radius: 12px; margin-bottom: 0.5rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">&#x1F948;</div>
                <div style="color: white; font-weight: 700; font-size: 1rem;">Silver Layer</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.75rem; margin-top: 0.25rem;">Dynamic Table</div>
            </div>
            <div style="color: #8892b0; font-size: 0.7rem;">
                DT_TRANSPLANT_ENRICHED<br>Auto-refresh: 1 min
            </div>
        </div>
        <div style="color: #29B5E8; font-size: 2rem; font-weight: 700;">&rarr;</div>
        <div style="flex: 1; min-width: 200px; text-align: center;">
            <div style="background: linear-gradient(135deg, #FFD700, #DAA520); padding: 1.25rem;
                        border-radius: 12px; margin-bottom: 0.5rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">&#x1F947;</div>
                <div style="color: white; font-weight: 700; font-size: 1rem;">Gold Layer</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.75rem; margin-top: 0.25rem;">Dynamic Table</div>
            </div>
            <div style="color: #8892b0; font-size: 0.7rem;">
                DT_GVHD_ANALYTICS<br>Pre-aggregated metrics
            </div>
        </div>
        <div style="color: #29B5E8; font-size: 2rem; font-weight: 700;">&rarr;</div>
        <div style="flex: 1; min-width: 200px; text-align: center;">
            <div style="background: linear-gradient(135deg, #29B5E8, #11567F); padding: 1.25rem;
                        border-radius: 12px; margin-bottom: 0.5rem;">
                <div style="font-size: 1.5rem; margin-bottom: 0.25rem;">&#x1F9E0;</div>
                <div style="color: white; font-weight: 700; font-size: 1rem;">Semantic View</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.75rem; margin-top: 0.25rem;">Single Source of Truth</div>
            </div>
            <div style="color: #8892b0; font-size: 0.7rem;">
                Agent / Intelligence<br>Streamlit / BI Tools
            </div>
        </div>
    </div>
</div>
</body></html>""", height=220, scrolling=False)

st.markdown("<br>", unsafe_allow_html=True)

# ── Dynamic Tables Deep Dive ──
st.markdown(render_section_separator(
    "Dynamic Tables Pipeline",
    "Declarative, auto-refreshing transformations — no ETL orchestrator needed"
), unsafe_allow_html=True)

st.markdown(render_pipeline_step(1, "Bronze: Raw Landing",
    "CSV files loaded into TRANSPLANT_OUTCOMES (500 structured records) and CLINICAL_NOTES (800 physician narratives)"), unsafe_allow_html=True)
st.markdown(render_pipeline_step(2, "Silver: DT_TRANSPLANT_ENRICHED",
    "Joins outcomes + notes, derives age groups, risk tiers, SVI categories, and sex mismatch flags. Auto-refreshes every 1 minute."), unsafe_allow_html=True)
st.markdown(render_pipeline_step(3, "Gold: DT_GVHD_ANALYTICS",
    "Pre-aggregated cohort metrics by donor type, race/ethnicity, region, and time. Feeds the Semantic View for consistent BI answers."), unsafe_allow_html=True)

st.markdown(render_info_callout(
    "Why Dynamic Tables over traditional ETL?",
    "Dynamic Tables are declarative — you define the SQL transformation and Snowflake handles the rest. "
    "No Informatica, no Airflow, no dbt. The pipeline DAG is managed automatically. "
    "When source data changes, downstream tables refresh within the target lag (1 minute). "
    "This replaces the batch ETL pattern that Looker and Oracle OBIEE depend on."
), unsafe_allow_html=True)

# ── Data Preview ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Data Preview")

if live_data:
    tab1, tab2 = st.tabs(["Transplant Outcomes", "Clinical Notes"])
    with tab1:
        df = session.sql("SELECT * FROM MARROWCO_DONOR_LAB.HOL.TRANSPLANT_OUTCOMES LIMIT 20").to_pandas()
        st.dataframe(df, use_container_width=True, height=400)
    with tab2:
        df = session.sql("SELECT * FROM MARROWCO_DONOR_LAB.HOL.CLINICAL_NOTES LIMIT 20").to_pandas()
        st.dataframe(df, use_container_width=True, height=400)
else:
    st.info("Connect to Snowflake to view live data. Run the SQL scripts in sql/ to load data first.")
    st.markdown(render_sql_block(
        "-- Quick peek at the data structure\n"
        "SELECT * FROM MARROWCO_DONOR_LAB.HOL.TRANSPLANT_OUTCOMES LIMIT 5;\n"
        "SELECT * FROM MARROWCO_DONOR_LAB.HOL.CLINICAL_NOTES LIMIT 5;"
    ), unsafe_allow_html=True)

# ── Donor Type Distribution ──
if live_data and donor_types is not None:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Donor Type Distribution")
    import plotly.express as px
    fig = px.pie(
        donor_types, values="CNT", names="DONOR_TYPE",
        color_discrete_sequence=["#29B5E8", "#00D4AA", "#FFB74D", "#FF6B6B"],
        hole=0.4
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FAFAFA", margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(font=dict(color="#8892b0"))
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Nav ──
st.markdown("---")
render_nav_buttons("Data Foundation")
