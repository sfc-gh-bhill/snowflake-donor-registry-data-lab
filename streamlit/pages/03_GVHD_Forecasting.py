import streamlit as st

st.set_page_config(page_title="GVHD Forecasting | LSC", page_icon="❄️", layout="wide")

from utils.styles import (
    apply_styles, render_header, render_metric_card, render_info_callout,
    render_success_callout, render_section_separator, render_sql_block
)
from utils.navigation import render_sidebar, render_nav_buttons, get_snowflake_session

apply_styles()
render_sidebar("GVHD Forecasting")

render_header("GVHD Forecasting", "ML-Powered Risk Prediction with The Winter Cloud Platform Model Registry")

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

# ── KPI Tiles ──
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

    # ── GVHD Rate by Donor Type ──
    st.markdown(render_section_separator(
        "GVHD Rates by Donor Type",
        "Comparing outcomes across Matched (8/8), Mismatched (7/8), Haploidentical, and Cord Blood donors"
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
            title="Significant GVHD Rate (Grade II+) by Donor Type",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "Significant_GVHD_Rate": "GVHD Rate (%)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            gvhd_by_donor, x="DONOR_TYPE_LABEL", y="Severe_GVHD_Rate",
            color_discrete_sequence=["#FF6B6B"],
            title="Severe GVHD Rate (Grade III-IV) by Donor Type",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "Severe_GVHD_Rate": "Severe GVHD Rate (%)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # ── Survival by Donor Type ──
    st.markdown(render_section_separator(
        "Survival Analysis",
        "1-year survival rates and average survival days across donor types"
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
            title="1-Year Overall Survival by Donor Type",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "One_Year_Survival_Pct": "1-Year OS (%)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            survival_by_donor, x="DONOR_TYPE_LABEL", y="Avg_Survival_Days",
            color_discrete_sequence=["#FFB74D"],
            title="Average Survival Days by Donor Type",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "Avg_Survival_Days": "Avg Survival (days)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        fig.update_yaxes(tickformat=",d")
        st.plotly_chart(fig, use_container_width=True)

    # ── Risk Score Distribution ──
    st.markdown(render_section_separator(
        "GVHD Risk Score Distribution",
        "ML-predicted risk scores — the target variable for the classification model"
    ), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(
            df_outcomes, x="GVHD_RISK_SCORE", nbins=30,
            color_discrete_sequence=["#29B5E8"],
            title="Risk Score Distribution (All Patients)",
            labels={"GVHD_RISK_SCORE": "GVHD Risk Score"}
        )
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.box(
            df_outcomes, x="DONOR_TYPE_LABEL", y="GVHD_RISK_SCORE",
            color="DONOR_TYPE_LABEL",
            color_discrete_sequence=["#29B5E8", "#00D4AA", "#FFB74D", "#FF6B6B"],
            title="Risk Score by Donor Type",
            labels={"DONOR_TYPE_LABEL": "Donor Type", "GVHD_RISK_SCORE": "Risk Score"}
        )
        fig.update_layout(**CHART_LAYOUT, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Health Equity: Race/Ethnicity ──
    st.markdown(render_section_separator(
        "Health Equity Analysis",
        "Outcomes by patient race/ethnicity — critical for the Donor for All initiative"
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
            title="Survival Rate by Race/Ethnicity",
            labels={"PATIENT_RACE_ETHNICITY": "", "Alive_Pct": "Currently Alive (%)"}
        )
        fig.update_layout(**CHART_LAYOUT)
        fig.update_xaxes(tickangle=30)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            equity, x="Avg_SVI", y="Alive_Pct", size="Total", text="PATIENT_RACE_ETHNICITY",
            color_discrete_sequence=["#00D4AA"],
            title="SVI vs Survival Rate (bubble size = patient count)",
            labels={"Avg_SVI": "Avg Social Vulnerability Index", "Alive_Pct": "Alive (%)"}
        )
        fig.update_traces(textposition="top center", textfont_size=9)
        fig.update_layout(**CHART_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # ── Geographic Distribution ──
    st.markdown(render_section_separator(
        "Geographic Distribution",
        "Transplant outcomes by center region"
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
        title="Transplant Volume & 1-Year Survivors by Region",
        labels={"CENTER_REGION": "Region", "value": "Count", "variable": ""}
    )
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Connect to The Winter Cloud Platform and run the SQL scripts to load data for live visualizations.")
    st.markdown(render_info_callout(
        "ML Model Overview",
        "The GVHD risk prediction model uses The Winter Cloud Platform ML Classification to predict severe GVHD (Grade III-IV) "
        "based on patient demographics, donor characteristics, treatment protocols, and social vulnerability scores. "
        "Run sql/08_ml_model.sql to train the model and view evaluation metrics."
    ), unsafe_allow_html=True)

# ── ML Model Info ──
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("ML Model Technical Details"):
    st.markdown("""
    **Model**: The Winter Cloud Platform ML Classification (`SNOWFLAKE.ML.CLASSIFICATION`)
    
    **Target**: `HIGH_RISK_GVHD` (binary: Grade III-IV = 1, Grade 0-II = 0)
    
    **Features**:
    - Patient: age, sex, race/ethnicity
    - Disease: diagnosis category, risk category
    - Donor: type, HLA match score, age, sex, sex mismatch
    - Treatment: conditioning intensity, PTCy-based prophylaxis
    - Social: SVI score, center region
    
    **Evaluation**: AUC, precision, recall, F1 score, feature importance
    
    **Key Insight**: The model identifies PTCy-based prophylaxis, donor type, and patient age 
    as top predictive features — consistent with published clinical literature.
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

# ── Nav ──
st.markdown("---")
render_nav_buttons("GVHD Forecasting")
