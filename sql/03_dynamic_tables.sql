/*=============================================================================
  LSC Donor for All Data Lab -- Dynamic Tables Pipeline
  =============================================================================
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                    WHY DYNAMIC TABLES?                                  │
  │                                                                        │
  │  Traditional BI tools like Looker or Oracle OBIEE rely on:             │
  │    - Scheduled batch ETL (often hourly or daily)                       │
  │    - External orchestration (Informatica, Airflow, dbt)                │
  │    - Manual dependency management between transformations              │
  │    - Complex incremental logic written by engineers                    │
  │                                                                        │
  │  Snowflake Dynamic Tables provide:                                     │
  │    + Declarative SQL -- define the WHAT, Snowflake handles the HOW     │
  │    + Automatic incremental refresh -- only processes changed data      │
  │    + Built-in dependency DAG -- Snowflake manages pipeline ordering    │
  │    + Near real-time (target lag as low as 1 minute)                    │
  │    + No external orchestrator needed                                   │
  │                                                                        │
  │  This pipeline feeds the Semantic View, which is the single source     │
  │  of truth consumed by ALL downstream analytics and AI tools.           │
  └─────────────────────────────────────────────────────────────────────────┘
  
  Pipeline Architecture:
  
    SHARED: TRANSPLANT_OUTCOMES ─┐
    (Bronze - Read-only)         │
                                 ├──► DT_TRANSPLANT_ENRICHED ──► DT_GVHD_ANALYTICS
    SHARED: CLINICAL_NOTES ──────┘    (Silver - Your Schema)       (Gold - Your Schema)
    (Bronze - Read-only)                        │
                                                ▼
                                         SEMANTIC VIEW
                                                │
                                        ┌───────┼───────┐
                                        ▼       ▼       ▼
                                     Agent  Streamlit  Intelligence

  Run after: Admin has run 01_create_tables.sql + 02_load_data.sql
  Run before: 04_cortex_search.sql
  =============================================================================*/

-- ════════════════════════════════════════════════════════════════════════════
-- SET YOUR USER NUMBER (assigned by the lab admin)
-- ════════════════════════════════════════════════════════════════════════════
SET USER_NUM = '01';  -- << CHANGE THIS TO YOUR ASSIGNED NUMBER (01-20)

-- Set context to your isolated environment
USE ROLE IDENTIFIER('MARROWCO_HOL_ROLE_' || $USER_NUM);
USE WAREHOUSE IDENTIFIER('MARROWCO_HOL_WH_' || $USER_NUM);
USE SCHEMA IDENTIFIER('MARROWCO_DONOR_LAB.HOL_USER_' || $USER_NUM);

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ SILVER LAYER: DT_TRANSPLANT_ENRICHED                                     ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Enriches transplant outcomes with:                                       ║
-- ║   - Derived age groups and risk categories                              ║
-- ║   - Clinical note counts and latest note summary per patient            ║
-- ║   - Computed survival metrics                                           ║
-- ║   - Social vulnerability classification                                 ║
-- ║                                                                          ║
-- ║ TARGET_LAG = 1 MINUTE means:                                            ║
-- ║   When new data lands in the Bronze tables, this table automatically     ║
-- ║   refreshes within 1 minute -- NO cron jobs, NO orchestrator, NO code.   ║
-- ║   Snowflake handles the incremental logic internally.                    ║
-- ║                                                                          ║
-- ║ NOTE: Reads from SHARED schema (MARROWCO_DONOR_LAB.HOL) but creates    ║
-- ║ the Dynamic Table in YOUR schema (HOL_USER_<NN>).                       ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE DYNAMIC TABLE DT_TRANSPLANT_ENRICHED
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = IDENTIFIER('MARROWCO_HOL_WH_' || $USER_NUM)
    COMMENT = 'Silver layer: Enriched transplant data with derived analytics columns'
AS
SELECT
    -- Core identifiers
    t.TRANSPLANT_ID,
    t.PATIENT_ID,
    t.TRANSPLANT_DATE,
    
    -- Patient demographics
    t.PATIENT_AGE,
    CASE 
        WHEN t.PATIENT_AGE < 18 THEN 'Pediatric (<18)'
        WHEN t.PATIENT_AGE BETWEEN 18 AND 39 THEN 'Young Adult (18-39)'
        WHEN t.PATIENT_AGE BETWEEN 40 AND 59 THEN 'Middle Age (40-59)'
        ELSE 'Older Adult (60+)'
    END AS AGE_GROUP,
    t.PATIENT_SEX,
    t.PATIENT_RACE_ETHNICITY,
    
    -- Diagnosis
    t.DIAGNOSIS,
    t.DIAGNOSIS_CATEGORY,
    t.DISEASE_STAGE,
    CASE 
        WHEN t.DISEASE_STAGE IN ('Early', 'CR1') THEN 'Low'
        WHEN t.DISEASE_STAGE IN ('Intermediate', 'CR2') THEN 'Medium'
        ELSE 'High'
    END AS DISEASE_RISK_CATEGORY,
    
    -- Donor information
    t.DONOR_TYPE,
    CASE t.DONOR_TYPE
        WHEN 'MUD_8_8'  THEN 'Matched Unrelated (8/8)'
        WHEN 'MMUD_7_8' THEN 'Mismatched Unrelated (7/8)'
        WHEN 'HAPLO'    THEN 'Haploidentical'
        WHEN 'CORD'     THEN 'Cord Blood'
    END AS DONOR_TYPE_LABEL,
    t.HLA_MATCH_SCORE,
    t.DONOR_AGE,
    t.DONOR_SEX,
    CASE 
        WHEN t.DONOR_SEX = 'Female' AND t.PATIENT_SEX = 'Male' THEN TRUE
        ELSE FALSE
    END AS SEX_MISMATCH_FLAG,
    
    -- Treatment
    t.CONDITIONING_REGIMEN,
    CASE 
        WHEN t.CONDITIONING_REGIMEN LIKE '%MAC%' THEN 'Myeloablative'
        WHEN t.CONDITIONING_REGIMEN LIKE '%RIC%' THEN 'Reduced Intensity'
        ELSE 'Non-Myeloablative'
    END AS CONDITIONING_INTENSITY,
    t.GVHD_PROPHYLAXIS,
    CASE 
        WHEN t.GVHD_PROPHYLAXIS LIKE '%PTCy%' THEN TRUE 
        ELSE FALSE 
    END AS PTCY_BASED_PROPHYLAXIS,
    
    -- Outcomes
    t.TIME_TO_ENGRAFTMENT_DAYS,
    CASE 
        WHEN t.TIME_TO_ENGRAFTMENT_DAYS <= 14 THEN 'Fast (<=14d)'
        WHEN t.TIME_TO_ENGRAFTMENT_DAYS <= 21 THEN 'Normal (15-21d)'
        ELSE 'Delayed (>21d)'
    END AS ENGRAFTMENT_SPEED,
    t.ACUTE_GVHD_GRADE,
    CASE 
        WHEN t.ACUTE_GVHD_GRADE = 0 THEN 'None'
        WHEN t.ACUTE_GVHD_GRADE <= 2 THEN 'Mild-Moderate (I-II)'
        ELSE 'Severe (III-IV)'
    END AS GVHD_SEVERITY,
    t.CHRONIC_GVHD,
    t.RELAPSE_FLAG,
    t.SURVIVAL_DAYS,
    t.SURVIVAL_STATUS,
    CASE 
        WHEN t.SURVIVAL_DAYS >= 365 THEN TRUE
        ELSE FALSE
    END AS ONE_YEAR_SURVIVOR,
    CASE 
        WHEN t.SURVIVAL_DAYS >= 730 THEN TRUE
        ELSE FALSE
    END AS TWO_YEAR_SURVIVOR,
    t.GVHD_RISK_SCORE,
    CASE 
        WHEN t.GVHD_RISK_SCORE < 0.3 THEN 'Low Risk'
        WHEN t.GVHD_RISK_SCORE < 0.6 THEN 'Moderate Risk'
        ELSE 'High Risk'
    END AS RISK_TIER,
    
    -- Geography & Social Determinants
    t.TRANSPLANT_CENTER_ID,
    t.CENTER_REGION,
    t.CENTER_STATE,
    t.PATIENT_ZIP_3DIGIT,
    t.SVI_SCORE,
    CASE 
        WHEN t.SVI_SCORE < 0.25 THEN 'Low Vulnerability'
        WHEN t.SVI_SCORE < 0.50 THEN 'Moderate Vulnerability'
        WHEN t.SVI_SCORE < 0.75 THEN 'High Vulnerability'
        ELSE 'Very High Vulnerability'
    END AS SVI_CATEGORY,
    
    -- Clinical Notes Aggregation
    n.NOTE_COUNT,
    n.GVHD_ASSESSMENT_COUNT,
    n.LATEST_NOTE_DATE,
    n.LATEST_NOTE_TEXT
    
FROM MARROWCO_DONOR_LAB.HOL.TRANSPLANT_OUTCOMES t
LEFT JOIN (
    SELECT 
        TRANSPLANT_ID,
        COUNT(*) AS NOTE_COUNT,
        COUNT(CASE WHEN NOTE_TYPE = 'GVHD_ASSESSMENT' THEN 1 END) AS GVHD_ASSESSMENT_COUNT,
        MAX(NOTE_DATE) AS LATEST_NOTE_DATE,
        MAX_BY(NOTE_TEXT, NOTE_DATE) AS LATEST_NOTE_TEXT
    FROM MARROWCO_DONOR_LAB.HOL.CLINICAL_NOTES
    GROUP BY TRANSPLANT_ID
) n ON t.TRANSPLANT_ID = n.TRANSPLANT_ID;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ GOLD LAYER: DT_GVHD_ANALYTICS                                           ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Pre-aggregated analytics table optimized for BI and AI consumption.      ║
-- ║                                                                          ║
-- ║ This table automatically updates when DT_TRANSPLANT_ENRICHED changes.   ║
-- ║ Snowflake detects the dependency and manages the refresh order.          ║
-- ║                                                                          ║
-- ║ KEY INSIGHT: This is the table that feeds the Semantic View.            ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE DYNAMIC TABLE DT_GVHD_ANALYTICS
    TARGET_LAG = '1 MINUTE'
    WAREHOUSE = IDENTIFIER('MARROWCO_HOL_WH_' || $USER_NUM)
    COMMENT = 'Gold layer: Pre-aggregated GVHD analytics for BI and AI consumption'
AS
SELECT
    -- Dimensions
    DONOR_TYPE,
    DONOR_TYPE_LABEL,
    DIAGNOSIS_CATEGORY,
    AGE_GROUP,
    PATIENT_RACE_ETHNICITY,
    CENTER_REGION,
    CONDITIONING_INTENSITY,
    GVHD_SEVERITY,
    RISK_TIER,
    SVI_CATEGORY,
    DISEASE_RISK_CATEGORY,
    PTCY_BASED_PROPHYLAXIS,
    DATE_TRUNC('MONTH', TRANSPLANT_DATE)::DATE AS TRANSPLANT_MONTH,
    YEAR(TRANSPLANT_DATE) AS TRANSPLANT_YEAR,
    
    -- Measures
    COUNT(*) AS TRANSPLANT_COUNT,
    
    -- GVHD metrics
    AVG(ACUTE_GVHD_GRADE)::DECIMAL(4,2) AS AVG_GVHD_GRADE,
    COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) AS SIGNIFICANT_GVHD_COUNT,
    COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 3 THEN 1 END) AS SEVERE_GVHD_COUNT,
    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) * 100.0 / COUNT(*), 1) AS GVHD_RATE_PCT,
    
    -- Survival metrics
    AVG(SURVIVAL_DAYS)::INT AS AVG_SURVIVAL_DAYS,
    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
    ROUND(COUNT(CASE WHEN TWO_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS TWO_YEAR_SURVIVAL_PCT,
    COUNT(CASE WHEN SURVIVAL_STATUS = 'ALIVE' THEN 1 END) AS ALIVE_COUNT,
    
    -- Engraftment metrics
    AVG(TIME_TO_ENGRAFTMENT_DAYS)::DECIMAL(4,1) AS AVG_ENGRAFTMENT_DAYS,
    MEDIAN(TIME_TO_ENGRAFTMENT_DAYS)::DECIMAL(4,1) AS MEDIAN_ENGRAFTMENT_DAYS,
    
    -- Risk metrics
    AVG(GVHD_RISK_SCORE)::DECIMAL(4,3) AS AVG_RISK_SCORE,
    AVG(SVI_SCORE)::DECIMAL(4,3) AS AVG_SVI_SCORE,
    
    -- Relapse
    ROUND(COUNT(CASE WHEN RELAPSE_FLAG = 1 THEN 1 END) * 100.0 / COUNT(*), 1) AS RELAPSE_RATE_PCT,
    
    -- Clinical notes coverage
    AVG(NOTE_COUNT)::DECIMAL(4,1) AS AVG_NOTES_PER_PATIENT

FROM DT_TRANSPLANT_ENRICHED
GROUP BY ALL;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify Dynamic Tables                                                    ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Check pipeline status
SHOW DYNAMIC TABLES;

-- Verify Silver layer
SELECT 
    COUNT(*) AS TOTAL_ROWS,
    COUNT(DISTINCT TRANSPLANT_ID) AS UNIQUE_TRANSPLANTS,
    COUNT(DISTINCT AGE_GROUP) AS AGE_GROUPS,
    COUNT(DISTINCT RISK_TIER) AS RISK_TIERS,
    'Silver layer (DT_TRANSPLANT_ENRICHED) ready' AS STATUS
FROM DT_TRANSPLANT_ENRICHED;

-- Verify Gold layer
SELECT 
    COUNT(*) AS AGGREGATE_ROWS,
    SUM(TRANSPLANT_COUNT) AS TOTAL_TRANSPLANTS,
    COUNT(DISTINCT DONOR_TYPE) AS DONOR_TYPES,
    'Gold layer (DT_GVHD_ANALYTICS) ready' AS STATUS
FROM DT_GVHD_ANALYTICS;
