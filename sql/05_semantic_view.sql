/*=============================================================================
  LSC Donor for All Data Lab — Semantic View  ★ KEY SHOWCASE ★
  =============================================================================
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                        │
  │   THE SEMANTIC VIEW IS THE SINGLE SOURCE OF TRUTH                      │
  │                                                                        │
  │   Every downstream consumer — Cortex Agent, Snowflake Intelligence,    │
  │   Streamlit dashboards, and future BI tools — queries data through     │
  │   this semantic layer. It defines:                                     │
  │                                                                        │
  │     • What questions can be asked (dimensions + metrics)               │
  │     • How data relates across tables (relationships)                   │
  │     • What answers are trusted (verified queries)                      │
  │     • How AI should behave (generation instructions)                   │
  │                                                                        │
  └─────────────────────────────────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ HOW THIS DIFFERS FROM LOOKER                                            │
  │                                                                        │
  │ Looker LookML:                                                         │
  │   ❌ Separate modeling language outside the database                   │
  │   ❌ Requires Looker infrastructure and licensing                      │
  │   ❌ Only works with structured data (can't handle clinical notes)     │
  │   ❌ Static explore — users must know what to ask                      │
  │   ❌ No AI-native question understanding                               │
  │   ❌ Batch-refreshed data (not real-time)                              │
  │                                                                        │
  │ Snowflake Semantic View:                                                │
  │   ✅ Native SQL DDL — lives IN the database, version-controlled        │
  │   ✅ AI-native: Cortex Analyst understands natural language questions   │
  │   ✅ Pairs with Cortex Search for structured + unstructured answers     │
  │   ✅ Feeds Dynamic Tables for near real-time data                      │
  │   ✅ Verified queries create a "trust layer" for governance            │
  │   ✅ Auto-generates suggested questions for Snowflake Intelligence     │
  │   ✅ No additional infrastructure or licensing required                 │
  └─────────────────────────────────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ HOW THIS DIFFERS FROM ORACLE OBIEE                                      │
  │                                                                        │
  │ Oracle OBIEE / Oracle Analytics:                                        │
  │   ❌ RPD (Repository) is a complex binary metadata layer               │
  │   ❌ Requires specialized OBIEE admin skills                           │
  │   ❌ Monolithic — changes require full RPD redeploy                    │
  │   ❌ No native AI or natural language query                            │
  │   ❌ Tightly coupled to Oracle database                                │
  │                                                                        │
  │ Snowflake Semantic View:                                                │
  │   ✅ Declarative SQL — any SQL user can read and modify                │
  │   ✅ Modular — update dimensions/metrics independently                 │
  │   ✅ AI-powered natural language → SQL translation                     │
  │   ✅ Works with any data source in Snowflake (incl. Iceberg)           │
  │   ✅ Git-friendly — plain SQL, easy to review and version              │
  └─────────────────────────────────────────────────────────────────────────┘
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ THE PIPELINE THAT FEEDS THIS MODEL                                      │
  │                                                                        │
  │  Raw Tables (Bronze)                                                    │
  │      │                                                                  │
  │      ▼                                                                  │
  │  Dynamic Table: DT_TRANSPLANT_ENRICHED (Silver)                         │
  │      │   → Auto-refresh every 1 minute                                 │
  │      │   → Joins outcomes + notes, derives risk categories             │
  │      ▼                                                                  │
  │  Dynamic Table: DT_GVHD_ANALYTICS (Gold)                               │
  │      │   → Pre-aggregated metrics for fast BI queries                  │
  │      ▼                                                                  │
  │  ★ SEMANTIC VIEW ★  ← You are here                                     │
  │      │                                                                  │
  │      ├──► Cortex Agent (natural language Q&A)                           │
  │      ├──► Snowflake Intelligence (auto-insights)                        │
  │      ├──► Streamlit App (dashboards)                                    │
  │      └──► Future consumers (APIs, other BI tools)                       │
  └─────────────────────────────────────────────────────────────────────────┘
  
  Clause order: TABLES → FACTS → DIMENSIONS → METRICS → COMMENT →
                AI_SQL_GENERATION → AI_QUESTION_CATEGORIZATION

  Run after: 03_dynamic_tables.sql
  Run before: 06_create_agent.sql
  =============================================================================*/

USE ROLE MARROWCO_HOL_ROLE;
USE WAREHOUSE MARROWCO_HOL_WH;
USE SCHEMA MARROWCO_DONOR_LAB.HOL;

CREATE OR REPLACE SEMANTIC VIEW MARROWCO_TRANSPLANT_ANALYTICS

TABLES (
    transplant_enriched AS MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
        PRIMARY KEY (TRANSPLANT_ID)
        COMMENT = 'Enriched transplant-level data with derived risk categories, demographics, and clinical note summaries',
    gvhd_analytics AS MARROWCO_DONOR_LAB.HOL.DT_GVHD_ANALYTICS
        COMMENT = 'Pre-aggregated transplant outcome analytics by key dimensions — optimized for BI queries'
)

FACTS (
    transplant_enriched.PATIENT_AGE AS PATIENT_AGE
        COMMENT = 'Patient age at the time of transplant',
    transplant_enriched.HLA_MATCH_SCORE AS HLA_MATCH_SCORE
        COMMENT = 'HLA match score out of 8 alleles. 8/8 = fully matched, lower = more mismatch.',
    transplant_enriched.DONOR_AGE AS DONOR_AGE
        COMMENT = 'Donor age at time of donation',
    transplant_enriched.TIME_TO_ENGRAFTMENT_DAYS AS TIME_TO_ENGRAFTMENT_DAYS
        WITH SYNONYMS = ('engraftment time', 'time to engraft', 'days to engraftment')
        COMMENT = 'Days from transplant to neutrophil engraftment (ANC > 500)',
    transplant_enriched.ACUTE_GVHD_GRADE AS ACUTE_GVHD_GRADE
        WITH SYNONYMS = ('GVHD grade', 'graft versus host disease grade', 'aGVHD')
        COMMENT = 'Acute GVHD clinical grade: 0 (none), 1-2 (mild-moderate), 3-4 (severe/life-threatening)',
    transplant_enriched.RELAPSE_FLAG AS RELAPSE_FLAG
        COMMENT = 'Disease relapse indicator: 0 = no relapse, 1 = relapsed post-transplant',
    transplant_enriched.SURVIVAL_DAYS AS SURVIVAL_DAYS
        WITH SYNONYMS = ('survival time', 'days survived', 'overall survival')
        COMMENT = 'Total days of patient survival after transplant',
    transplant_enriched.GVHD_RISK_SCORE AS GVHD_RISK_SCORE
        WITH SYNONYMS = ('risk score', 'GVHD risk', 'predicted risk')
        COMMENT = 'Predicted GVHD risk score (0.00 to 1.00). ML target variable. Higher = greater risk.',
    transplant_enriched.SVI_SCORE AS SVI_SCORE
        WITH SYNONYMS = ('social vulnerability', 'SVI', 'vulnerability index')
        COMMENT = 'CDC Social Vulnerability Index (0.0 to 1.0). Higher = more socially vulnerable community.',
    transplant_enriched.NOTE_COUNT AS NOTE_COUNT
        COMMENT = 'Number of clinical notes associated with this transplant',
    transplant_enriched.GVHD_ASSESSMENT_COUNT AS GVHD_ASSESSMENT_COUNT
        COMMENT = 'Number of GVHD-specific assessment notes for this transplant',
    gvhd_analytics.TRANSPLANT_COUNT AS gvhd_analytics.TRANSPLANT_COUNT
        WITH SYNONYMS = ('count', 'volume', 'number of transplants')
        COMMENT = 'Number of transplants in this cohort',
    gvhd_analytics.AVG_GVHD_GRADE AS gvhd_analytics.AVG_GVHD_GRADE
        COMMENT = 'Average acute GVHD grade in cohort',
    gvhd_analytics.SIGNIFICANT_GVHD_COUNT AS gvhd_analytics.SIGNIFICANT_GVHD_COUNT
        COMMENT = 'Count of grade II+ GVHD cases',
    gvhd_analytics.SEVERE_GVHD_COUNT AS gvhd_analytics.SEVERE_GVHD_COUNT
        COMMENT = 'Count of grade III-IV severe GVHD cases',
    gvhd_analytics.GVHD_RATE_PCT AS gvhd_analytics.GVHD_RATE_PCT
        WITH SYNONYMS = ('GVHD rate', 'incidence rate', 'GVHD percentage')
        COMMENT = 'Percentage of transplants with significant GVHD (grade II+)',
    gvhd_analytics.AVG_SURVIVAL_DAYS AS gvhd_analytics.AVG_SURVIVAL_DAYS
        COMMENT = 'Average survival days in cohort',
    gvhd_analytics.ONE_YEAR_SURVIVAL_PCT AS gvhd_analytics.ONE_YEAR_SURVIVAL_PCT
        WITH SYNONYMS = ('1-year survival', 'one year OS', '1yr survival rate')
        COMMENT = 'Percentage of patients surviving at least 1 year',
    gvhd_analytics.TWO_YEAR_SURVIVAL_PCT AS gvhd_analytics.TWO_YEAR_SURVIVAL_PCT
        WITH SYNONYMS = ('2-year survival', 'two year OS')
        COMMENT = 'Percentage of patients surviving at least 2 years',
    gvhd_analytics.ALIVE_COUNT AS gvhd_analytics.ALIVE_COUNT
        COMMENT = 'Number of patients currently alive',
    gvhd_analytics.AVG_ENGRAFTMENT_DAYS AS gvhd_analytics.AVG_ENGRAFTMENT_DAYS
        COMMENT = 'Average days to neutrophil engraftment',
    gvhd_analytics.MEDIAN_ENGRAFTMENT_DAYS AS gvhd_analytics.MEDIAN_ENGRAFTMENT_DAYS
        COMMENT = 'Median days to neutrophil engraftment',
    gvhd_analytics.AVG_RISK_SCORE AS gvhd_analytics.AVG_RISK_SCORE
        COMMENT = 'Average GVHD risk score in cohort',
    gvhd_analytics.AVG_SVI_SCORE AS gvhd_analytics.AVG_SVI_SCORE
        COMMENT = 'Average Social Vulnerability Index in cohort',
    gvhd_analytics.RELAPSE_RATE_PCT AS gvhd_analytics.RELAPSE_RATE_PCT
        WITH SYNONYMS = ('relapse rate', 'relapse percentage')
        COMMENT = 'Percentage of patients who relapsed',
    gvhd_analytics.AVG_NOTES_PER_PATIENT AS gvhd_analytics.AVG_NOTES_PER_PATIENT
        COMMENT = 'Average number of clinical notes per patient'
)

DIMENSIONS (
    transplant_enriched.TRANSPLANT_ID AS TRANSPLANT_ID
        COMMENT = 'Unique transplant procedure identifier',
    transplant_enriched.PATIENT_ID AS PATIENT_ID
        COMMENT = 'Unique patient identifier',
    transplant_enriched.TRANSPLANT_DATE AS TRANSPLANT_DATE
        COMMENT = 'Date the transplant procedure was performed',
    transplant_enriched.AGE_GROUP AS AGE_GROUP
        COMMENT = 'Patient age category: Pediatric (<18), Young Adult (18-39), Middle Age (40-59), Older Adult (60+)',
    transplant_enriched.PATIENT_SEX AS PATIENT_SEX
        COMMENT = 'Patient biological sex: Male or Female',
    transplant_enriched.PATIENT_RACE_ETHNICITY AS PATIENT_RACE_ETHNICITY
        COMMENT = 'Patient self-reported race/ethnicity. Key for health equity analysis under Donor for All initiative.',
    transplant_enriched.DIAGNOSIS AS DIAGNOSIS
        COMMENT = 'Primary diagnosis requiring transplant (e.g., Acute Myeloid Leukemia, Sickle Cell Disease)',
    transplant_enriched.DIAGNOSIS_CATEGORY AS DIAGNOSIS_CATEGORY
        COMMENT = 'Broad disease category: Leukemia, Lymphoma, MDS/MPN, Bone Marrow Failure, Hemoglobinopathy',
    transplant_enriched.DISEASE_STAGE AS DISEASE_STAGE
        COMMENT = 'Disease stage at transplant: Early, Intermediate, Advanced, CR1, CR2, Relapsed/Refractory',
    transplant_enriched.DISEASE_RISK_CATEGORY AS DISEASE_RISK_CATEGORY
        COMMENT = 'Simplified risk tier: Low (Early/CR1), Medium (Intermediate/CR2), High (Advanced/Relapsed)',
    transplant_enriched.DONOR_TYPE AS DONOR_TYPE
        COMMENT = 'Donor source code: MUD_8_8 (matched unrelated 8/8), MMUD_7_8 (mismatched 7/8), HAPLO (haploidentical), CORD (cord blood)',
    transplant_enriched.DONOR_TYPE_LABEL AS DONOR_TYPE_LABEL
        COMMENT = 'Human-readable donor type label for display',
    transplant_enriched.DONOR_SEX AS DONOR_SEX
        COMMENT = 'Donor biological sex',
    transplant_enriched.SEX_MISMATCH_FLAG AS SEX_MISMATCH_FLAG
        COMMENT = 'TRUE if female donor to male recipient (known GVHD risk factor)',
    transplant_enriched.CONDITIONING_REGIMEN AS CONDITIONING_REGIMEN
        COMMENT = 'Pre-transplant conditioning protocol (e.g., MAC-BuCy, RIC-FluBu)',
    transplant_enriched.CONDITIONING_INTENSITY AS CONDITIONING_INTENSITY
        COMMENT = 'Conditioning intensity category: Myeloablative, Reduced Intensity, Non-Myeloablative',
    transplant_enriched.GVHD_PROPHYLAXIS AS GVHD_PROPHYLAXIS
        COMMENT = 'Post-transplant immunosuppression regimen for GVHD prevention',
    transplant_enriched.PTCY_BASED_PROPHYLAXIS AS PTCY_BASED_PROPHYLAXIS
        COMMENT = 'TRUE if prophylaxis includes post-transplant cyclophosphamide (PTCy) — key for haploidentical outcomes',
    transplant_enriched.TRANSPLANT_CENTER_ID AS TRANSPLANT_CENTER_ID
        COMMENT = 'Transplant center identifier code',
    transplant_enriched.CENTER_REGION AS CENTER_REGION
        COMMENT = 'Geographic region of transplant center: Northeast, Southeast, Midwest, Southwest, West, Central',
    transplant_enriched.CENTER_STATE AS CENTER_STATE
        COMMENT = 'US state of transplant center',
    transplant_enriched.PATIENT_ZIP_3DIGIT AS PATIENT_ZIP_3DIGIT
        COMMENT = '3-digit patient ZIP code for geographic analysis',
    transplant_enriched.SVI_CATEGORY AS SVI_CATEGORY
        COMMENT = 'Social vulnerability classification: Low, Moderate, High, Very High Vulnerability',
    transplant_enriched.ENGRAFTMENT_SPEED AS ENGRAFTMENT_SPEED
        COMMENT = 'Engraftment speed category: Fast (<=14d), Normal (15-21d), Delayed (>21d)',
    transplant_enriched.GVHD_SEVERITY AS GVHD_SEVERITY
        COMMENT = 'Acute GVHD severity category: None, Mild-Moderate (I-II), Severe (III-IV)',
    transplant_enriched.CHRONIC_GVHD AS CHRONIC_GVHD
        COMMENT = 'Chronic GVHD status: NONE, MILD, MODERATE, SEVERE',
    transplant_enriched.SURVIVAL_STATUS AS SURVIVAL_STATUS
        COMMENT = 'Current survival status: ALIVE or DECEASED',
    transplant_enriched.ONE_YEAR_SURVIVOR AS ONE_YEAR_SURVIVOR
        COMMENT = 'TRUE if patient survived at least 365 days post-transplant',
    transplant_enriched.TWO_YEAR_SURVIVOR AS TWO_YEAR_SURVIVOR
        COMMENT = 'TRUE if patient survived at least 730 days post-transplant',
    transplant_enriched.RISK_TIER AS RISK_TIER
        COMMENT = 'Risk classification: Low Risk (<0.3), Moderate Risk (0.3-0.6), High Risk (>0.6)',
    transplant_enriched.LATEST_NOTE_DATE AS LATEST_NOTE_DATE
        COMMENT = 'Date of the most recent clinical note',
    transplant_enriched.LATEST_NOTE_TEXT AS LATEST_NOTE_TEXT
        COMMENT = 'Text of the most recent clinical note',
    gvhd_analytics.ANALYTICS_DONOR_TYPE AS gvhd_analytics.DONOR_TYPE
        COMMENT = 'Donor source type',
    gvhd_analytics.ANALYTICS_DONOR_TYPE_LABEL AS gvhd_analytics.DONOR_TYPE_LABEL
        COMMENT = 'Donor type display name',
    gvhd_analytics.ANALYTICS_DIAGNOSIS_CATEGORY AS gvhd_analytics.DIAGNOSIS_CATEGORY
        COMMENT = 'Disease category',
    gvhd_analytics.ANALYTICS_AGE_GROUP AS gvhd_analytics.AGE_GROUP
        COMMENT = 'Patient age group',
    gvhd_analytics.ANALYTICS_RACE_ETHNICITY AS gvhd_analytics.PATIENT_RACE_ETHNICITY
        COMMENT = 'Patient race/ethnicity',
    gvhd_analytics.ANALYTICS_CENTER_REGION AS gvhd_analytics.CENTER_REGION
        COMMENT = 'Transplant center region',
    gvhd_analytics.ANALYTICS_CONDITIONING_INTENSITY AS gvhd_analytics.CONDITIONING_INTENSITY
        COMMENT = 'Conditioning regimen intensity',
    gvhd_analytics.ANALYTICS_GVHD_SEVERITY AS gvhd_analytics.GVHD_SEVERITY
        COMMENT = 'GVHD severity category',
    gvhd_analytics.ANALYTICS_RISK_TIER AS gvhd_analytics.RISK_TIER
        COMMENT = 'Risk classification tier',
    gvhd_analytics.ANALYTICS_SVI_CATEGORY AS gvhd_analytics.SVI_CATEGORY
        COMMENT = 'Social vulnerability category',
    gvhd_analytics.ANALYTICS_DISEASE_RISK_CATEGORY AS gvhd_analytics.DISEASE_RISK_CATEGORY
        COMMENT = 'Disease risk level',
    gvhd_analytics.ANALYTICS_PTCY_BASED AS gvhd_analytics.PTCY_BASED_PROPHYLAXIS
        COMMENT = 'Whether PTCy-based prophylaxis was used',
    gvhd_analytics.TRANSPLANT_MONTH AS gvhd_analytics.TRANSPLANT_MONTH
        COMMENT = 'Month of transplant (for trend analysis)',
    gvhd_analytics.TRANSPLANT_YEAR AS gvhd_analytics.TRANSPLANT_YEAR
        COMMENT = 'Year of transplant'
)

METRICS (
    transplant_enriched.TOTAL_TRANSPLANTS AS COUNT(transplant_enriched.TRANSPLANT_ID)
        COMMENT = 'Total number of transplant procedures',
    transplant_enriched.OVERALL_GVHD_RATE AS
        (COUNT_IF(transplant_enriched.ACUTE_GVHD_GRADE >= 2) * 100.0
            / NULLIF(COUNT(transplant_enriched.TRANSPLANT_ID), 0))
        COMMENT = 'Overall rate of significant GVHD (grade II+) across all transplants',
    transplant_enriched.SEVERE_GVHD_RATE AS
        (COUNT_IF(transplant_enriched.ACUTE_GVHD_GRADE >= 3) * 100.0
            / NULLIF(COUNT(transplant_enriched.TRANSPLANT_ID), 0))
        COMMENT = 'Rate of severe GVHD (grade III-IV)',
    transplant_enriched.OVERALL_SURVIVAL_RATE AS
        (COUNT_IF(transplant_enriched.SURVIVAL_STATUS = 'ALIVE') * 100.0
            / NULLIF(COUNT(transplant_enriched.TRANSPLANT_ID), 0))
        COMMENT = 'Percentage of patients currently alive',
    transplant_enriched.ONE_YEAR_OS_RATE AS
        (COUNT_IF(transplant_enriched.ONE_YEAR_SURVIVOR) * 100.0
            / NULLIF(COUNT(transplant_enriched.TRANSPLANT_ID), 0))
        COMMENT = '1-year overall survival rate',
    transplant_enriched.AVG_SURVIVAL AS AVG(transplant_enriched.SURVIVAL_DAYS)
        COMMENT = 'Average survival time in days post-transplant',
    transplant_enriched.AVG_ENGRAFTMENT_TIME AS AVG(transplant_enriched.TIME_TO_ENGRAFTMENT_DAYS)
        COMMENT = 'Average time to neutrophil engraftment in days',
    transplant_enriched.AVG_GVHD_RISK AS AVG(transplant_enriched.GVHD_RISK_SCORE)
        COMMENT = 'Average predicted GVHD risk score across the cohort',
    transplant_enriched.RELAPSE_RATE AS
        (SUM(transplant_enriched.RELAPSE_FLAG) * 100.0
            / NULLIF(COUNT(transplant_enriched.TRANSPLANT_ID), 0))
        COMMENT = 'Overall relapse rate post-transplant',
    transplant_enriched.AVG_SVI AS AVG(transplant_enriched.SVI_SCORE)
        COMMENT = 'Average Social Vulnerability Index'
)

COMMENT = 'Semantic model for MarrowCo transplant outcome analytics — the single source of truth for all AI and BI consumption'

AI_SQL_GENERATION '
## Context
This data represents hematopoietic cell transplant (HCT) outcomes from the
MarrowCo / National Transplant Registry registry. The "Donor for All" initiative aims to ensure
every patient has access to a well-matched donor regardless of racial or
ethnic background.

## Key Clinical Terms
- GVHD (Graft-versus-Host Disease): when donor immune cells attack the patient
- HCT: Hematopoietic Cell Transplantation (also called bone marrow transplant)
- MUD: Matched Unrelated Donor (8/8 HLA match — gold standard)
- MMUD: Mismatched Unrelated Donor (7/8 HLA match — expanding access)
- HAPLO: Haploidentical donor (half-matched, usually a family member)
- PTCy: Post-transplant cyclophosphamide (key GVHD prevention strategy)
- SVI: Social Vulnerability Index (CDC measure of community health vulnerability)
- Engraftment: when transplanted cells begin producing new blood cells

## Query Guidelines
- Use transplant_enriched for patient-level detail queries
- Use gvhd_analytics for aggregated summary/trend queries
- When comparing donor types, use DONOR_TYPE_LABEL for readable output
- For survival analysis, prefer ONE_YEAR_SURVIVOR / TWO_YEAR_SURVIVOR booleans
- Always include sample size (COUNT) when showing rates or averages
- For health equity questions, cross-reference PATIENT_RACE_ETHNICITY with outcomes
- SVI_SCORE ranges from 0 (least vulnerable) to 1 (most vulnerable)
- GVHD_RISK_SCORE ranges from 0 (lowest risk) to 1 (highest risk)

## Verified Queries

### What is the overall GVHD rate by donor type?
```sql
SELECT
    DONOR_TYPE_LABEL,
    COUNT(*) AS TOTAL_TRANSPLANTS,
    COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) AS SIGNIFICANT_GVHD,
    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) * 100.0 / COUNT(*), 1) AS GVHD_RATE_PCT,
    ROUND(AVG(GVHD_RISK_SCORE), 3) AS AVG_RISK_SCORE
FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
GROUP BY DONOR_TYPE_LABEL
ORDER BY GVHD_RATE_PCT DESC
```

### Compare survival rates between 8/8 matched and 7/8 mismatched donors
```sql
SELECT
    DONOR_TYPE_LABEL,
    COUNT(*) AS TOTAL_PATIENTS,
    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
    ROUND(COUNT(CASE WHEN TWO_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS TWO_YEAR_SURVIVAL_PCT,
    ROUND(AVG(SURVIVAL_DAYS)) AS AVG_SURVIVAL_DAYS
FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
WHERE DONOR_TYPE IN (''MUD_8_8'', ''MMUD_7_8'')
GROUP BY DONOR_TYPE_LABEL
ORDER BY DONOR_TYPE_LABEL
```

### Which transplant centers have the best outcomes?
```sql
SELECT
    TRANSPLANT_CENTER_ID,
    CENTER_REGION,
    CENTER_STATE,
    COUNT(*) AS TRANSPLANT_COUNT,
    ROUND(AVG(SURVIVAL_DAYS)) AS AVG_SURVIVAL_DAYS,
    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
    ROUND(AVG(ACUTE_GVHD_GRADE), 2) AS AVG_GVHD_GRADE,
    ROUND(AVG(TIME_TO_ENGRAFTMENT_DAYS), 1) AS AVG_ENGRAFTMENT_DAYS
FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
GROUP BY TRANSPLANT_CENTER_ID, CENTER_REGION, CENTER_STATE
HAVING COUNT(*) >= 10
ORDER BY ONE_YEAR_SURVIVAL_PCT DESC
```

### How does patient race and ethnicity affect donor availability and outcomes?
```sql
SELECT
    PATIENT_RACE_ETHNICITY,
    COUNT(*) AS TOTAL_PATIENTS,
    ROUND(AVG(HLA_MATCH_SCORE), 1) AS AVG_HLA_MATCH,
    ROUND(COUNT(CASE WHEN DONOR_TYPE = ''MUD_8_8'' THEN 1 END) * 100.0 / COUNT(*), 1) AS FULLY_MATCHED_PCT,
    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
    ROUND(AVG(GVHD_RISK_SCORE), 3) AS AVG_RISK_SCORE,
    ROUND(AVG(SVI_SCORE), 3) AS AVG_SVI_SCORE
FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
GROUP BY PATIENT_RACE_ETHNICITY
ORDER BY TOTAL_PATIENTS DESC
```

### What is the impact of PTCy on haploidentical transplant outcomes?
```sql
SELECT
    CASE WHEN PTCY_BASED_PROPHYLAXIS THEN ''PTCy-Based'' ELSE ''Non-PTCy'' END AS PROPHYLAXIS_TYPE,
    COUNT(*) AS TOTAL_PATIENTS,
    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) * 100.0 / COUNT(*), 1) AS GVHD_RATE_PCT,
    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 3 THEN 1 END) * 100.0 / COUNT(*), 1) AS SEVERE_GVHD_PCT,
    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
    ROUND(AVG(TIME_TO_ENGRAFTMENT_DAYS), 1) AS AVG_ENGRAFTMENT_DAYS
FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
WHERE DONOR_TYPE = ''HAPLO''
GROUP BY PTCY_BASED_PROPHYLAXIS
ORDER BY PROPHYLAXIS_TYPE
```

### How does social vulnerability affect transplant outcomes?
```sql
SELECT
    SVI_CATEGORY,
    COUNT(*) AS TOTAL_PATIENTS,
    ROUND(AVG(SURVIVAL_DAYS)) AS AVG_SURVIVAL_DAYS,
    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
    ROUND(AVG(GVHD_RISK_SCORE), 3) AS AVG_RISK_SCORE,
    ROUND(AVG(TIME_TO_ENGRAFTMENT_DAYS), 1) AS AVG_ENGRAFTMENT_DAYS,
    ROUND(SUM(RELAPSE_FLAG) * 100.0 / COUNT(*), 1) AS RELAPSE_RATE_PCT
FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
GROUP BY SVI_CATEGORY
ORDER BY AVG_RISK_SCORE DESC
```
'

AI_QUESTION_CATEGORIZATION '
This semantic model is for hematopoietic cell transplant (HCT) outcome analytics.

ANSWER questions about:
- Transplant outcomes (survival, GVHD, engraftment, relapse)
- Donor type comparisons (MUD vs MMUD vs HAPLO vs CORD)
- Patient demographics and health equity
- Risk factors and predictive scores
- Transplant center performance
- Treatment protocols (conditioning, GVHD prophylaxis)
- Social determinants of health (SVI)
- Trends over time

DECLINE questions about:
- Individual patient identification or PHI
- Non-transplant medical topics
- Financial, billing, or insurance information
- Drug pricing or pharmaceutical recommendations
- Legal or regulatory compliance advice
- Topics unrelated to transplant outcome analytics
'
;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify the Semantic View                                                 ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

SHOW SEMANTIC VIEWS IN SCHEMA MARROWCO_DONOR_LAB.HOL;

DESCRIBE SEMANTIC VIEW MARROWCO_TRANSPLANT_ANALYTICS;
