import streamlit as st

st.set_page_config(page_title="Semantic Intelligence | LSC", page_icon="❄️", layout="wide")

from utils.styles import (
    apply_styles, render_header, render_metric_card, render_info_callout,
    render_success_callout, render_warning_callout, render_sql_block,
    render_section_separator, render_pipeline_step
)
from utils.navigation import render_sidebar, render_nav_buttons, get_snowflake_session
import streamlit.components.v1 as components

apply_styles()
render_sidebar("Semantic Intelligence")

render_header("Semantic Intelligence", "The Semantic View — Single Source of Truth for All AI and BI")

session = get_snowflake_session()

# ── KPI Tiles ──
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(render_metric_card("8", "Verified Queries", "Trusted & Validated"), unsafe_allow_html=True)
with col2:
    st.markdown(render_metric_card("10", "Defined Metrics", "Consistent Answers"), unsafe_allow_html=True)
with col3:
    st.markdown(render_metric_card("2", "Logical Tables", "Silver + Gold"), unsafe_allow_html=True)
with col4:
    st.markdown(render_metric_card("40+", "Columns Mapped", "Dimensions & Facts"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── What is a Semantic View? ──
st.markdown(render_section_separator(
    "What is a Semantic View?",
    "The semantic layer that sits between your data and every consumer — AI agents, dashboards, and analysts"
), unsafe_allow_html=True)

components.html("""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body { margin: 0; padding: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; }</style>
</head><body>
<div style="background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%); border-radius: 16px;
            padding: 2rem; border: 1px solid rgba(255,255,255,0.1); margin: 0;">
    <p style="color: #FAFAFA; font-size: 0.95rem; line-height: 1.8;">
        A <strong style="color: #29B5E8;">Semantic View</strong> is a native Snowflake object that defines:
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
        <div style="background: rgba(41,181,232,0.1); border-radius: 10px; padding: 1rem;">
            <div style="color: #29B5E8; font-weight: 700;">Tables &amp; Relationships</div>
            <div style="color: #8892b0; font-size: 0.8rem; margin-top: 0.25rem;">Which physical tables participate and how they join</div>
        </div>
        <div style="background: rgba(0,212,170,0.1); border-radius: 10px; padding: 1rem;">
            <div style="color: #00D4AA; font-weight: 700;">Dimensions &amp; Facts</div>
            <div style="color: #8892b0; font-size: 0.8rem; margin-top: 0.25rem;">Categorical columns (dimensions) and numeric measures (facts)</div>
        </div>
        <div style="background: rgba(255,183,77,0.1); border-radius: 10px; padding: 1rem;">
            <div style="color: #FFB74D; font-weight: 700;">Metrics</div>
            <div style="color: #8892b0; font-size: 0.8rem; margin-top: 0.25rem;">Pre-defined business calculations for consistent answers</div>
        </div>
        <div style="background: rgba(255,107,107,0.1); border-radius: 10px; padding: 1rem;">
            <div style="color: #FF6B6B; font-weight: 700;">Verified Queries</div>
            <div style="color: #8892b0; font-size: 0.8rem; margin-top: 0.25rem;">Trusted question-SQL pairs that create a "trust layer"</div>
        </div>
        <div style="background: rgba(41,181,232,0.1); border-radius: 10px; padding: 1rem;">
            <div style="color: #29B5E8; font-weight: 700;">AI Instructions</div>
            <div style="color: #8892b0; font-size: 0.8rem; margin-top: 0.25rem;">Guide how Cortex Analyst translates questions to SQL</div>
        </div>
        <div style="background: rgba(0,212,170,0.1); border-radius: 10px; padding: 1rem;">
            <div style="color: #00D4AA; font-weight: 700;">Guardrails</div>
            <div style="color: #8892b0; font-size: 0.8rem; margin-top: 0.25rem;">Define what questions are appropriate and what to decline</div>
        </div>
    </div>
</div>
</body></html>""", height=340, scrolling=False)

st.markdown("<br>", unsafe_allow_html=True)

# ── Comparison: Snowflake vs Looker vs Oracle OBIEE ──
st.markdown(render_section_separator(
    "How Does This Compare?",
    "Snowflake Semantic Views vs Looker LookML vs Oracle OBIEE"
), unsafe_allow_html=True)

comparison_data = [
    ("Definition Language", "Native SQL DDL", "LookML (proprietary)", "RPD Binary Repository"),
    ("Where It Lives", "Inside the database", "Separate Looker instance", "OBIEE metadata layer"),
    ("AI-Native", "Yes — powers Cortex Analyst", "No — manual explores only", "No"),
    ("Unstructured Data", "Yes — pairs with Cortex Search", "No — structured only", "No — structured only"),
    ("Real-Time Pipeline", "Dynamic Tables (1-min lag)", "Batch extract/PDTs", "ETL batch (Informatica)"),
    ("Verified Queries", "Yes — trust layer", "No equivalent", "No equivalent"),
    ("Auto Suggestions", "Yes — Snowflake Intelligence", "No", "No"),
    ("Version Control", "Git-friendly SQL", "Git possible but complex", "Binary — not git-friendly"),
    ("Licensing", "Included with Snowflake", "Separate Looker license", "Separate Oracle license"),
    ("Skill Required", "SQL (any analyst)", "LookML developer", "OBIEE RPD specialist"),
]

_comparison_rows = "".join([
    f'<tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">'
    f'<td style="padding: 0.6rem 1rem; color: #FAFAFA; font-size: 0.8rem; font-weight: 600;">{cap}</td>'
    f'<td style="padding: 0.6rem 1rem; color: #00D4AA; font-size: 0.8rem;">{sf}</td>'
    f'<td style="padding: 0.6rem 1rem; color: #8892b0; font-size: 0.8rem;">{lk}</td>'
    f'<td style="padding: 0.6rem 1rem; color: #8892b0; font-size: 0.8rem;">{ob}</td>'
    f'</tr>'
    for cap, sf, lk, ob in comparison_data
])

components.html(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body {{ margin: 0; padding: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; }}</style>
</head><body>
<div style="overflow-x: auto;">
<table style="width: 100%; border-collapse: collapse; background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%);
              border-radius: 12px; overflow: hidden;">
    <thead>
        <tr style="background: linear-gradient(135deg, #29B5E8, #11567F);">
            <th style="padding: 0.75rem 1rem; text-align: left; color: white; font-size: 0.85rem;">Capability</th>
            <th style="padding: 0.75rem 1rem; text-align: left; color: white; font-size: 0.85rem;">Snowflake Semantic View</th>
            <th style="padding: 0.75rem 1rem; text-align: left; color: white; font-size: 0.85rem;">Looker LookML</th>
            <th style="padding: 0.75rem 1rem; text-align: left; color: white; font-size: 0.85rem;">Oracle OBIEE</th>
        </tr>
    </thead>
    <tbody>
{_comparison_rows}
    </tbody>
</table>
</div>
</body></html>""", height=480, scrolling=False)

st.markdown(render_success_callout(
    "The Key Insight",
    "The Semantic View holds the TRUE VALUE that all other BI and AI solutions consume. "
    "It is not just a metadata layer — it is the governed, AI-native interface between your data and every question anyone will ever ask. "
    "When you update a metric definition here, every consumer (Agent, Intelligence, Streamlit, future BI tools) "
    "automatically gets the updated answer. No more conflicting dashboards."
), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Pipeline Feeding the Semantic View ──
st.markdown(render_section_separator(
    "The Pipeline Feeding the Semantic View",
    "Dynamic Tables provide near real-time data to the semantic layer"
), unsafe_allow_html=True)

st.markdown(render_pipeline_step(1, "Raw Data Lands",
    "New transplant records or clinical notes are loaded into Bronze tables"), unsafe_allow_html=True)
st.markdown(render_pipeline_step(2, "Silver Refreshes Automatically",
    "DT_TRANSPLANT_ENRICHED detects changes and refreshes within 1 minute — no scheduler needed"), unsafe_allow_html=True)
st.markdown(render_pipeline_step(3, "Gold Cascades",
    "DT_GVHD_ANALYTICS auto-refreshes because Snowflake manages the dependency DAG"), unsafe_allow_html=True)
st.markdown(render_pipeline_step(4, "Semantic View Reflects Current Data",
    "Cortex Analyst, Snowflake Intelligence, and this Streamlit app all see the latest data"), unsafe_allow_html=True)

st.markdown(render_info_callout(
    "Compare this to Looker",
    "In Looker, you would need: an ETL tool (Informatica/Fivetran) to extract data, "
    "a dbt/PDT layer to transform it, a scheduling system (cron/Airflow) to orchestrate, "
    "and a LookML developer to maintain the model. With Snowflake: one Dynamic Table SQL statement does it all."
), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Verified Queries Explorer ──
st.markdown(render_section_separator(
    "Verified Queries — The Trust Layer",
    "Pre-validated question-SQL pairs that ensure consistent, trusted answers"
), unsafe_allow_html=True)

verified_queries = {
    "What is the overall GVHD rate by donor type?": (
        "The most fundamental question in transplant outcomes research",
        """SELECT DONOR_TYPE_LABEL, COUNT(*) AS TOTAL_TRANSPLANTS,
    COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) AS SIGNIFICANT_GVHD,
    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) * 100.0 / COUNT(*), 1) AS GVHD_RATE_PCT
FROM DT_TRANSPLANT_ENRICHED GROUP BY DONOR_TYPE_LABEL ORDER BY GVHD_RATE_PCT DESC"""
    ),
    "Compare survival rates between matched and mismatched donors": (
        "Core to the 'Donor for All' thesis — MMUD approaching MUD outcomes",
        """SELECT DONOR_TYPE_LABEL, COUNT(*) AS TOTAL_PATIENTS,
    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
    ROUND(AVG(SURVIVAL_DAYS)) AS AVG_SURVIVAL_DAYS
FROM DT_TRANSPLANT_ENRICHED WHERE DONOR_TYPE IN ('MUD_8_8', 'MMUD_7_8')
GROUP BY DONOR_TYPE_LABEL"""
    ),
    "Which transplant centers have the best outcomes?": (
        "Center performance comparison for quality benchmarking",
        """SELECT TRANSPLANT_CENTER_ID, CENTER_REGION, COUNT(*) AS TRANSPLANT_COUNT,
    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT
FROM DT_TRANSPLANT_ENRICHED GROUP BY 1, 2 HAVING COUNT(*) >= 10
ORDER BY ONE_YEAR_SURVIVAL_PCT DESC"""
    ),
    "How does race/ethnicity affect outcomes?": (
        "Critical health equity analysis for the Donor for All initiative",
        """SELECT PATIENT_RACE_ETHNICITY, COUNT(*) AS TOTAL_PATIENTS,
    ROUND(AVG(HLA_MATCH_SCORE), 1) AS AVG_HLA_MATCH,
    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
    ROUND(AVG(SVI_SCORE), 3) AS AVG_SVI_SCORE
FROM DT_TRANSPLANT_ENRICHED GROUP BY 1 ORDER BY TOTAL_PATIENTS DESC"""
    ),
}

selected_query = st.selectbox(
    "Select a verified query to explore:",
    list(verified_queries.keys())
)

if selected_query:
    desc, sql = verified_queries[selected_query]
    st.markdown(f'<p style="color: #8892b0; font-size: 0.9rem; margin-bottom: 1rem;">{desc}</p>', unsafe_allow_html=True)
    st.markdown(render_sql_block(sql), unsafe_allow_html=True)

    if session:
        if st.button("Run This Query", type="primary"):
            try:
                full_sql = sql.replace("DT_TRANSPLANT_ENRICHED", "MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED")
                df = session.sql(full_sql).to_pandas()
                st.dataframe(df, use_container_width=True)

                if len(df) > 0 and len(df.columns) >= 2:
                    import plotly.express as px
                    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
                    str_cols = df.select_dtypes(include=["object"]).columns.tolist()
                    if str_cols and numeric_cols:
                        fig = px.bar(
                            df, x=str_cols[0], y=numeric_cols[-1],
                            color_discrete_sequence=["#29B5E8"],
                            labels={str_cols[0]: str_cols[0].replace("_", " ").title(),
                                    numeric_cols[-1]: numeric_cols[-1].replace("_", " ").title()}
                        )
                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font_color="#FAFAFA", xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                            margin=dict(t=20, b=40, l=40, r=20)
                        )
                        st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Query failed: {e}")
    else:
        st.info("Connect to Snowflake to run queries live.")

# ── Nav ──
st.markdown("---")
render_nav_buttons("Semantic Intelligence")
