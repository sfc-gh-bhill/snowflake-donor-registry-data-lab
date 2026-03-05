import streamlit as st

st.set_page_config(page_title="GVHD Forecasting | LSC", page_icon="snowflake", layout="wide")

from utils.styles import (
    apply_styles, render_header, render_metric_card, render_info_callout,
    render_success_callout, render_section_separator, render_sql_block
)
from utils.navigation import render_sidebar, render_nav_buttons, get_snowflake_session
import streamlit.components.v1 as components

apply_styles()
render_sidebar("GVHD Forecasting")

render_header("GVHD Forecasting", "ML-Powered Risk Prediction with Snowflake Model Registry")

session = get_snowflake_session()
live_data = False

if session:
    try:
        df_outcomes = session.sql("""
            SELECT DONOR_TYPE_LABEL, GVHD_SEVERITY, RISK_TIER, 
                   PATIENT_RACE_ETHNICITY, AGE_GROUP, CENTER_REGION,
                   ACUTE_GVHD_GRADE, SURVIVAL_DAYS, SURVIVAL_STATUS,
                   GVHD_RISK_SCORE, TIME_TO_ENGRAFTMENT_DAYS, SVI_SCORE,
                   ONE_YEAR_SURVIVOR, CONDITIONING_INTENSITY
            FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
        """).to_pandas()
        live_data = True
    except Exception:
        pass

# -- KPI Tiles --
if live_data:
    total = len(df_outcomes)
    severe = len(df_outcomes[df_outcomes["ACUTE_GVHD_GRADE"] >= 3])
    alive_pct = round(len(df_outcomes[df_outcomes["SURVIVAL_STATUS"] == "ALIVE"]) / total * 100, 1)
    avg_risk = round(df_outcomes["GVHD_RISK_SCORE"].mean(), 3)
else:
    total, severe, alive_pct, avg_risk = 500, 67, 46.6, 0.42

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(render_metric_card(str(total), "Total Transplants", "Study Cohort"), unsafe_allow_html=True)
with col2:
    st.markdown(render_metric_card(str(severe), "Severe GVHD (III-IV)", f"{round(severe/total*100,1)}% of cohort"), unsafe_allow_html=True)
with col3:
    st.markdown(render_metric_card(f"{alive_pct}%", "Currently Alive", "Overall Survival"), unsafe_allow_html=True)
with col4:
    st.markdown(render_metric_card(str(avg_risk), "Avg Risk Score", "GVHD Prediction"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -- ML Model Explanation --
st.markdown(render_section_separator(
    "The ML Classification Model",
    "How Snowflake ML predicts which patients are at highest risk for severe GVHD"
), unsafe_allow_html=True)

components.html("""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body { margin: 0; padding: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; }</style>
</head><body>
<div style="background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%); border-radius: 16px;
            padding: 2rem; border: 1px solid rgba(255,255,255,0.1); margin: 0;">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
        <div>
            <h3 style="color: #29B5E8; margin: 0 0 0.75rem 0; font-size: 1.1rem;">What It Does</h3>
            <p style="color: #FAFAFA; font-size: 0.88rem; line-height: 1.7; margin: 0;">
                The model uses <strong style="color: #29B5E8;">Snowflake ML Classification</strong> to predict
                whether a transplant patient will develop <strong style="color: #FF6B6B;">severe Graft-vs-Host Disease
                (Grade III-IV)</strong> based on 12+ clinical and demographic features. It learns patterns from
                historical transplant outcomes to assign each patient a risk score between 0 and 1.
            </p>
        </div>
        <div>
            <h3 style="color: #00D4AA; margin: 0 0 0.75rem 0; font-size: 1.1rem;">Why It Matters</h3>
            <p style="color: #FAFAFA; font-size: 0.88rem; line-height: 1.7; margin: 0;">
                Severe GVHD is the <strong style="color: #FF6B6B;">leading cause of transplant-related mortality</strong>.
                Early risk identification enables transplant teams to adjust conditioning regimens,
                select optimal prophylaxis protocols, and allocate monitoring resources
                <em>before</em> complications develop &mdash; not after.
            </p>
        </div>
    </div>
    <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);">
        <h3 style="color: #FFB74D; margin: 0 0 0.75rem 0; font-size: 1.1rem;">How It Helps Clinicians</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="background: rgba(41,181,232,0.1); border-radius: 10px; padding: 0.75rem 1rem;">
                <div style="color: #29B5E8; font-weight: 700; font-size: 0.85rem;">Risk Stratification</div>
                <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">Classify patients into Low, Medium, and High risk tiers at time of transplant planning</div>
            </div>
            <div style="background: rgba(0,212,170,0.1); border-radius: 10px; padding: 0.75rem 1rem;">
                <div style="color: #00D4AA; font-weight: 700; font-size: 0.85rem;">Proactive Intervention</div>
                <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">High-risk patients can receive intensified prophylaxis or alternative donor selection</div>
            </div>
            <div style="background: rgba(255,183,77,0.1); border-radius: 10px; padding: 0.75rem 1rem;">
                <div style="color: #FFB74D; font-weight: 700; font-size: 0.85rem;">Equity Insights</div>
                <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">Reveals disparities in outcomes across race, ethnicity, and social vulnerability</div>
            </div>
            <div style="background: rgba(255,107,107,0.1); border-radius: 10px; padding: 0.75rem 1rem;">
                <div style="color: #FF6B6B; font-weight: 700; font-size: 0.85rem;">Feature Transparency</div>
                <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">Shows which factors drive predictions &mdash; PTCy prophylaxis, donor type, patient age</div>
            </div>
        </div>
    </div>
</div>
</body></html>""", height=380, scrolling=False)

st.markdown(render_info_callout(
    "Built Entirely in Snowflake",
    "No external ML infrastructure needed. The model is trained with a single SQL statement using "
    "SNOWFLAKE.ML.CLASSIFICATION, stored in the Snowflake Model Registry, and called for predictions "
    "directly in SQL. The same governed data in your Dynamic Tables feeds both the analytics dashboards "
    "below and the ML model -- no data movement, no pipeline to maintain."
), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if live_data:
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd

    CHART_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FAFAFA", margin=dict(t=40, b=40, l=40, r=20),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        legend=dict(font=dict(color="#8892b0")),
    )

    # -- GVHD Rate by Donor Type --
    st.markdown(render_section_separator(
        "GVHD Rates by Donor Type -- Which Donors Carry More Risk?",
        "Comparing GVHD complication rates across all four donor types to identify which pairings are safest"
    ), unsafe_allow_html=True)

    gvhd_by_donor = df_outcomes.groupby("DONOR_TYPE_LABEL").agg(
        Total=("ACUTE_GVHD_GRADE", "count"),
        Severe_Count=("ACUTE_GVHD_GRADE", lambda x: (x >= 3).sum()),
        Significant_Count=("ACUTE_GVHD_GRADE", lambda x: (x >= 2).sum()),
    ).reset_index()
    gvhd_by_donor["Severe_GVHD_Rate"] = round(gvhd_by_donor["Severe_Count"] / gvhd_by_donor["Total"] * 100, 1)
    gvhd_by_donor["Significant_GVHD_Rate"] = round(gvhd_by_donor["Significant_Count"] / gvhd_by_donor["Total"] * 100, 1)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            gvhd_by_donor, x="DONOR_TYPE_LABEL", y="Significant_GVHD_Rate",
            color_discrete_sequence=["#29B5E8"],
            title="Significant GVHD (Grade II+) -- How Often Does GVHD Develop?",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "Significant_GVHD_Rate": "GVHD Rate (%)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            gvhd_by_donor, x="DONOR_TYPE_LABEL", y="Severe_GVHD_Rate",
            color_discrete_sequence=["#FF6B6B"],
            title="Severe GVHD (Grade III-IV) -- Which Donors Are Most Dangerous?",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "Severe_GVHD_Rate": "Severe GVHD Rate (%)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # -- Survival by Donor Type --
    st.markdown(render_section_separator(
        "Survival Analysis -- Are Alternative Donors Closing the Gap?",
        "1-year survival rates and average survival days show whether mismatched and haplo donors can match traditional outcomes"
    ), unsafe_allow_html=True)

    survival_by_donor = df_outcomes.groupby("DONOR_TYPE_LABEL").agg(
        Total=("SURVIVAL_STATUS", "count"),
        Alive=("SURVIVAL_STATUS", lambda x: (x == "ALIVE").sum()),
        Avg_Survival_Days=("SURVIVAL_DAYS", "mean"),
        One_Year=("ONE_YEAR_SURVIVOR", "sum"),
    ).reset_index()
    survival_by_donor["One_Year_Survival_Pct"] = round(survival_by_donor["One_Year"] / survival_by_donor["Total"] * 100, 1)
    survival_by_donor["Alive_Pct"] = round(survival_by_donor["Alive"] / survival_by_donor["Total"] * 100, 1)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            survival_by_donor, x="DONOR_TYPE_LABEL", y="One_Year_Survival_Pct",
            color_discrete_sequence=["#00D4AA"],
            title="1-Year Survival -- Who Lives Past the Critical Window?",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "One_Year_Survival_Pct": "1-Year OS (%)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            survival_by_donor, x="DONOR_TYPE_LABEL", y="Avg_Survival_Days",
            color_discrete_sequence=["#FFB74D"],
            title="Avg Survival Days -- How Long Do Patients Live?",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "Avg_Survival_Days": "Avg Survival (days)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        fig.update_yaxes(tickformat=",d")
        st.plotly_chart(fig, use_container_width=True)

    # -- Risk Score Distribution --
    st.markdown(render_section_separator(
        "GVHD Risk Score Distribution -- What the Model Predicts",
        "ML-generated risk scores show how the model stratifies patients from low to high risk"
    ), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(
            df_outcomes, x="GVHD_RISK_SCORE", nbins=30,
            color_discrete_sequence=["#29B5E8"],
            title="Risk Score Spread -- Where Do Most Patients Fall?",
            labels={"GVHD_RISK_SCORE": "GVHD Risk Score"}
        )
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.box(
            df_outcomes, x="DONOR_TYPE_LABEL", y="GVHD_RISK_SCORE",
            color="DONOR_TYPE_LABEL",
            color_discrete_sequence=["#29B5E8", "#00D4AA", "#FFB74D", "#FF6B6B"],
            title="Risk by Donor Type -- Do Some Donors Predict Higher Risk?",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "GVHD_RISK_SCORE": "Risk Score"}
        )
        fig.update_layout(**CHART_LAYOUT, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # -- Health Equity: Race/Ethnicity --
    st.markdown(render_section_separator(
        "Health Equity Analysis -- Are Outcomes Equal Across Populations?",
        "Survival and risk differences by race/ethnicity reveal where disparities exist and where the Donor for All initiative must focus"
    ), unsafe_allow_html=True)

    equity = df_outcomes.groupby("PATIENT_RACE_ETHNICITY").agg(
        Total=("SURVIVAL_STATUS", "count"),
        Alive=("SURVIVAL_STATUS", lambda x: (x == "ALIVE").sum()),
        Avg_Risk=("GVHD_RISK_SCORE", "mean"),
        Avg_SVI=("SVI_SCORE", "mean"),
    ).reset_index()
    equity["Alive_Pct"] = round(equity["Alive"] / equity["Total"] * 100, 1)
    equity = equity.sort_values("Total", ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            equity, x="PATIENT_RACE_ETHNICITY", y="Alive_Pct",
            color_discrete_sequence=["#29B5E8"],
            title="Survival by Race/Ethnicity -- Who Has the Best Chance?",
            labels={"PATIENT_RACE_ETHNICITY": "", "Alive_Pct": "Currently Alive (%)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        fig.update_xaxes(tickangle=30)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            equity, x="Avg_SVI", y="Alive_Pct", size="Total", text="PATIENT_RACE_ETHNICITY",
            color_discrete_sequence=["#00D4AA"],
            title="Social Vulnerability vs Survival -- Does Poverty Affect Outcomes?",
            labels={"Avg_SVI": "Avg Social Vulnerability Index", "Alive_Pct": "Alive (%)"}
        )
        fig.update_traces(textposition="top center", textfont_size=9)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # -- Geographic Distribution --
    st.markdown(render_section_separator(
        "Geographic Distribution -- Where Are Outcomes Best?",
        "Regional volume and survival differences can indicate center quality or access disparities"
    ), unsafe_allow_html=True)

    geo = df_outcomes.groupby("CENTER_REGION").agg(
        Total=("SURVIVAL_STATUS", "count"),
        One_Year=("ONE_YEAR_SURVIVOR", "sum"),
        Avg_Risk=("GVHD_RISK_SCORE", "mean"),
    ).reset_index()
    geo["One_Year_Pct"] = round(geo["One_Year"] / geo["Total"] * 100, 1)

    fig = px.bar(
        geo, x="CENTER_REGION", y=["Total", "One_Year"],
        barmode="group",
        color_discrete_sequence=["#29B5E8", "#00D4AA"],
        title="Volume & Survivors by Region -- Which Regions Lead?",
        labels={"CENTER_REGION": "Region", "value": "Count", "variable": ""}
    )
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Connect to Snowflake and run the SQL scripts to load data for live visualizations.")
    st.markdown(render_info_callout(
        "ML Model Overview",
        "The GVHD risk prediction model uses Snowflake ML Classification to predict severe GVHD (Grade III-IV) "
        "based on patient demographics, donor characteristics, treatment protocols, and social vulnerability scores. "
        "Run sql/08_ml_model.sql to train the model and view evaluation metrics."
    ), unsafe_allow_html=True)

# -- ML Model Info --
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("ML Model Technical Details"):
    st.markdown("""
    **Model**: Snowflake ML Classification (`SNOWFLAKE.ML.CLASSIFICATION`)
    
    **Target**: `HIGH_RISK_GVHD` (binary: Grade III-IV = 1, Grade 0-II = 0)
    
    **Features**:
    - Patient: age, sex, race/ethnicity
    - Disease: diagnosis category, risk category
    - Donor: type, HLA match score, age, sex, sex mismatch
    - Treatment: conditioning intensity, PTCy-based prophylaxis
    - Social: SVI score, center region
    
    **Evaluation**: AUC, precision, recall, F1 score, feature importance
    
    **Key Insight**: The model identifies PTCy-based prophylaxis, donor type, and patient age 
    as top predictive features -- consistent with published clinical literature.
    """)
    st.markdown(render_sql_block(
        "-- Train the model\n"
        "CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION GVHD_RISK_MODEL(\n"
        "    INPUT_DATA => SYSTEM$REFERENCE('TABLE', 'ML_TRAINING_DATA'),\n"
        "    TARGET_COLNAME => 'HIGH_RISK_GVHD',\n"
        "    CONFIG_OBJECT => {'evaluate': TRUE}\n"
        ");\n\n"
        "-- View results\n"
        "CALL GVHD_RISK_MODEL!SHOW_EVALUATION_METRICS();\n"
        "CALL GVHD_RISK_MODEL!SHOW_FEATURE_IMPORTANCE();"
    ), unsafe_allow_html=True)

# -- Nav --
st.markdown("---")
render_nav_buttons("GVHD Forecasting")
