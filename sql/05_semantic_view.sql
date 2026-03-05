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
  
  Run after: 03_dynamic_tables.sql
  Run before: 06_create_agent.sql
  =============================================================================*/

USE ROLE MARROWCO_HOL_ROLE;
USE WAREHOUSE MARROWCO_HOL_WH;
USE SCHEMA MARROWCO_DONOR_LAB.HOL;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ CREATE THE SEMANTIC VIEW                                                 ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ The semantic view defines the logical data model that AI and BI          ║
-- ║ consumers use to understand your data. It includes:                      ║
-- ║                                                                          ║
-- ║   TABLES        → Which physical tables are part of the model           ║
-- ║   RELATIONSHIPS → How tables join together (foreign keys)               ║
-- ║   COLUMNS       → Dimensions (categorical) and Facts (numeric)          ║
-- ║   METRICS       → Pre-defined business calculations                     ║
-- ║   AI_SQL_GENERATION → Instructions for Cortex Analyst                   ║
-- ║   AI_QUESTION_CATEGORIZATION → Guardrails for appropriate questions     ║
-- ║   VERIFIED QUERIES → Trusted, pre-validated question-SQL pairs          ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE SEMANTIC VIEW MARROWCO_TRANSPLANT_ANALYTICS
    COMMENT = 'Semantic model for LSC transplant outcome analytics — the single source of truth for all AI and BI consumption'
AS

-- ═══════════════════════════════════════════════════════════════════════════
-- TABLES: Define which physical tables are included in this semantic model
-- ═══════════════════════════════════════════════════════════════════════════
TABLES (

    -- Silver layer: enriched individual transplant records
    MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
        COMMENT = 'Enriched transplant-level data with derived risk categories, demographics, and clinical note summaries'
        PRIMARY KEY (TRANSPLANT_ID)
        
        -- ─── Dimensions (categorical/descriptive columns) ───
        COLUMNS (
            TRANSPLANT_ID
                COMMENT = 'Unique transplant procedure identifier',
            PATIENT_ID
                COMMENT = 'Unique patient identifier',
            TRANSPLANT_DATE
                COMMENT = 'Date the transplant procedure was performed',
            PATIENT_AGE
                COMMENT = 'Patient age at the time of transplant',
            AGE_GROUP
                COMMENT = 'Patient age category: Pediatric (<18), Young Adult (18-39), Middle Age (40-59), Older Adult (60+)',
            PATIENT_SEX
                COMMENT = 'Patient biological sex: Male or Female',
            PATIENT_RACE_ETHNICITY
                COMMENT = 'Patient self-reported race/ethnicity. Key for health equity analysis under Donor for All initiative.',
            DIAGNOSIS
                COMMENT = 'Primary diagnosis requiring transplant (e.g., Acute Myeloid Leukemia, Sickle Cell Disease)',
            DIAGNOSIS_CATEGORY
                COMMENT = 'Broad disease category: Leukemia, Lymphoma, MDS/MPN, Bone Marrow Failure, Hemoglobinopathy',
            DISEASE_STAGE
                COMMENT = 'Disease stage at transplant: Early, Intermediate, Advanced, CR1, CR2, Relapsed/Refractory',
            DISEASE_RISK_CATEGORY
                COMMENT = 'Simplified risk tier: Low (Early/CR1), Medium (Intermediate/CR2), High (Advanced/Relapsed)',
            DONOR_TYPE
                COMMENT = 'Donor source code: MUD_8_8 (matched unrelated 8/8), MMUD_7_8 (mismatched 7/8), HAPLO (haploidentical), CORD (cord blood)',
            DONOR_TYPE_LABEL
                COMMENT = 'Human-readable donor type label for display',
            HLA_MATCH_SCORE
                COMMENT = 'HLA match score out of 8 alleles. 8/8 = fully matched, lower = more mismatch.',
            DONOR_AGE
                COMMENT = 'Donor age at time of donation',
            DONOR_SEX
                COMMENT = 'Donor biological sex',
            SEX_MISMATCH_FLAG
                COMMENT = 'TRUE if female donor to male recipient (known GVHD risk factor)',
            CONDITIONING_REGIMEN
                COMMENT = 'Pre-transplant conditioning protocol (e.g., MAC-BuCy, RIC-FluBu)',
            CONDITIONING_INTENSITY
                COMMENT = 'Conditioning intensity category: Myeloablative, Reduced Intensity, Non-Myeloablative',
            GVHD_PROPHYLAXIS
                COMMENT = 'Post-transplant immunosuppression regimen for GVHD prevention',
            PTCY_BASED_PROPHYLAXIS
                COMMENT = 'TRUE if prophylaxis includes post-transplant cyclophosphamide (PTCy) — key for haploidentical outcomes',
            TRANSPLANT_CENTER_ID
                COMMENT = 'Transplant center identifier code',
            CENTER_REGION
                COMMENT = 'Geographic region of transplant center: Northeast, Southeast, Midwest, Southwest, West, Central',
            CENTER_STATE
                COMMENT = 'US state of transplant center',
            PATIENT_ZIP_3DIGIT
                COMMENT = '3-digit patient ZIP code for geographic analysis',
            SVI_CATEGORY
                COMMENT = 'Social vulnerability classification: Low, Moderate, High, Very High Vulnerability',
            
            -- ─── Facts (numeric/measurable columns) ───
            TIME_TO_ENGRAFTMENT_DAYS
                COMMENT = 'Days from transplant to neutrophil engraftment (ANC > 500)'
                SYNONYMS = ('engraftment time', 'time to engraft', 'days to engraftment'),
            ENGRAFTMENT_SPEED
                COMMENT = 'Engraftment speed category: Fast (≤14d), Normal (15-21d), Delayed (>21d)',
            ACUTE_GVHD_GRADE
                COMMENT = 'Acute GVHD clinical grade: 0 (none), 1-2 (mild-moderate), 3-4 (severe/life-threatening)'
                SYNONYMS = ('GVHD grade', 'graft versus host disease grade', 'aGVHD'),
            GVHD_SEVERITY
                COMMENT = 'Acute GVHD severity category: None, Mild-Moderate (I-II), Severe (III-IV)',
            CHRONIC_GVHD
                COMMENT = 'Chronic GVHD status: NONE, MILD, MODERATE, SEVERE',
            RELAPSE_FLAG
                COMMENT = 'Disease relapse indicator: 0 = no relapse, 1 = relapsed post-transplant',
            SURVIVAL_DAYS
                COMMENT = 'Total days of patient survival after transplant'
                SYNONYMS = ('survival time', 'days survived', 'overall survival'),
            SURVIVAL_STATUS
                COMMENT = 'Current survival status: ALIVE or DECEASED',
            ONE_YEAR_SURVIVOR
                COMMENT = 'TRUE if patient survived at least 365 days post-transplant',
            TWO_YEAR_SURVIVOR
                COMMENT = 'TRUE if patient survived at least 730 days post-transplant',
            GVHD_RISK_SCORE
                COMMENT = 'Predicted GVHD risk score (0.00 to 1.00). ML target variable. Higher = greater risk.'
                SYNONYMS = ('risk score', 'GVHD risk', 'predicted risk'),
            RISK_TIER
                COMMENT = 'Risk classification: Low Risk (<0.3), Moderate Risk (0.3-0.6), High Risk (>0.6)',
            SVI_SCORE
                COMMENT = 'CDC Social Vulnerability Index (0.0 to 1.0). Higher = more socially vulnerable community.'
                SYNONYMS = ('social vulnerability', 'SVI', 'vulnerability index'),
            NOTE_COUNT
                COMMENT = 'Number of clinical notes associated with this transplant',
            GVHD_ASSESSMENT_COUNT
                COMMENT = 'Number of GVHD-specific assessment notes for this transplant',
            LATEST_NOTE_DATE
                COMMENT = 'Date of the most recent clinical note',
            LATEST_NOTE_TEXT
                COMMENT = 'Text of the most recent clinical note'
        ),
        
    -- Gold layer: pre-aggregated analytics 
    MARROWCO_DONOR_LAB.HOL.DT_GVHD_ANALYTICS
        COMMENT = 'Pre-aggregated transplant outcome analytics by key dimensions — optimized for BI queries'
        
        COLUMNS (
            DONOR_TYPE
                COMMENT = 'Donor source type',
            DONOR_TYPE_LABEL
                COMMENT = 'Donor type display name',
            DIAGNOSIS_CATEGORY
                COMMENT = 'Disease category',
            AGE_GROUP
                COMMENT = 'Patient age group',
            PATIENT_RACE_ETHNICITY
                COMMENT = 'Patient race/ethnicity',
            CENTER_REGION
                COMMENT = 'Transplant center region',
            CONDITIONING_INTENSITY
                COMMENT = 'Conditioning regimen intensity',
            GVHD_SEVERITY
                COMMENT = 'GVHD severity category',
            RISK_TIER
                COMMENT = 'Risk classification tier',
            SVI_CATEGORY
                COMMENT = 'Social vulnerability category',
            DISEASE_RISK_CATEGORY
                COMMENT = 'Disease risk level',
            PTCY_BASED_PROPHYLAXIS
                COMMENT = 'Whether PTCy-based prophylaxis was used',
            TRANSPLANT_MONTH
                COMMENT = 'Month of transplant (for trend analysis)',
            TRANSPLANT_YEAR
                COMMENT = 'Year of transplant',
            TRANSPLANT_COUNT
                COMMENT = 'Number of transplants in this cohort'
                SYNONYMS = ('count', 'volume', 'number of transplants'),
            AVG_GVHD_GRADE
                COMMENT = 'Average acute GVHD grade in cohort',
            SIGNIFICANT_GVHD_COUNT
                COMMENT = 'Count of grade II+ GVHD cases',
            SEVERE_GVHD_COUNT
                COMMENT = 'Count of grade III-IV severe GVHD cases',
            GVHD_RATE_PCT
                COMMENT = 'Percentage of transplants with significant GVHD (grade II+)'
                SYNONYMS = ('GVHD rate', 'incidence rate', 'GVHD percentage'),
            AVG_SURVIVAL_DAYS
                COMMENT = 'Average survival days in cohort',
            ONE_YEAR_SURVIVAL_PCT
                COMMENT = 'Percentage of patients surviving at least 1 year'
                SYNONYMS = ('1-year survival', 'one year OS', '1yr survival rate'),
            TWO_YEAR_SURVIVAL_PCT
                COMMENT = 'Percentage of patients surviving at least 2 years'
                SYNONYMS = ('2-year survival', 'two year OS'),
            ALIVE_COUNT
                COMMENT = 'Number of patients currently alive',
            AVG_ENGRAFTMENT_DAYS
                COMMENT = 'Average days to neutrophil engraftment',
            MEDIAN_ENGRAFTMENT_DAYS
                COMMENT = 'Median days to neutrophil engraftment',
            AVG_RISK_SCORE
                COMMENT = 'Average GVHD risk score in cohort',
            AVG_SVI_SCORE
                COMMENT = 'Average Social Vulnerability Index in cohort',
            RELAPSE_RATE_PCT
                COMMENT = 'Percentage of patients who relapsed'
                SYNONYMS = ('relapse rate', 'relapse percentage'),
            AVG_NOTES_PER_PATIENT
                COMMENT = 'Average number of clinical notes per patient'
        )
)

-- ═══════════════════════════════════════════════════════════════════════════
-- RELATIONSHIPS: Define how tables join together
-- ═══════════════════════════════════════════════════════════════════════════
RELATIONSHIPS (
    -- Note: The Gold table is a pre-aggregated summary, not directly joinable
    -- to the Silver table by PK/FK. Each table serves different query patterns:
    -- Silver → detailed patient-level queries
    -- Gold → aggregated cohort-level analytics
)

-- ═══════════════════════════════════════════════════════════════════════════
-- METRICS: Pre-defined business calculations
-- These are the "golden metrics" that ensure consistent answers across
-- all consumers. When Cortex Analyst generates SQL, it uses these
-- definitions rather than letting each user write their own formulas.
-- ═══════════════════════════════════════════════════════════════════════════
METRICS (
    -- Transplant volume
    TOTAL_TRANSPLANTS
        COMMENT = 'Total number of transplant procedures'
        AS COUNT(DT_TRANSPLANT_ENRICHED.TRANSPLANT_ID),
    
    -- GVHD outcomes
    OVERALL_GVHD_RATE
        COMMENT = 'Overall rate of significant GVHD (grade II+) across all transplants'
        AS (COUNT_IF(DT_TRANSPLANT_ENRICHED.ACUTE_GVHD_GRADE >= 2) * 100.0 
            / NULLIF(COUNT(DT_TRANSPLANT_ENRICHED.TRANSPLANT_ID), 0)),
    
    SEVERE_GVHD_RATE
        COMMENT = 'Rate of severe GVHD (grade III-IV) — most clinically concerning outcome'
        AS (COUNT_IF(DT_TRANSPLANT_ENRICHED.ACUTE_GVHD_GRADE >= 3) * 100.0 
            / NULLIF(COUNT(DT_TRANSPLANT_ENRICHED.TRANSPLANT_ID), 0)),
    
    -- Survival metrics
    OVERALL_SURVIVAL_RATE
        COMMENT = 'Percentage of patients currently alive'
        AS (COUNT_IF(DT_TRANSPLANT_ENRICHED.SURVIVAL_STATUS = 'ALIVE') * 100.0 
            / NULLIF(COUNT(DT_TRANSPLANT_ENRICHED.TRANSPLANT_ID), 0)),
    
    ONE_YEAR_OS_RATE
        COMMENT = '1-year overall survival rate — key transplant outcome benchmark'
        AS (COUNT_IF(DT_TRANSPLANT_ENRICHED.ONE_YEAR_SURVIVOR) * 100.0 
            / NULLIF(COUNT(DT_TRANSPLANT_ENRICHED.TRANSPLANT_ID), 0)),
    
    AVG_SURVIVAL
        COMMENT = 'Average survival time in days post-transplant'
        AS AVG(DT_TRANSPLANT_ENRICHED.SURVIVAL_DAYS),
    
    -- Engraftment
    AVG_ENGRAFTMENT_TIME
        COMMENT = 'Average time to neutrophil engraftment in days'
        AS AVG(DT_TRANSPLANT_ENRICHED.TIME_TO_ENGRAFTMENT_DAYS),
    
    -- Risk
    AVG_GVHD_RISK
        COMMENT = 'Average predicted GVHD risk score across the cohort'
        AS AVG(DT_TRANSPLANT_ENRICHED.GVHD_RISK_SCORE),
    
    -- Health equity
    RELAPSE_RATE
        COMMENT = 'Overall relapse rate post-transplant'
        AS (SUM(DT_TRANSPLANT_ENRICHED.RELAPSE_FLAG) * 100.0 
            / NULLIF(COUNT(DT_TRANSPLANT_ENRICHED.TRANSPLANT_ID), 0)),
    
    AVG_SVI
        COMMENT = 'Average Social Vulnerability Index — measures health equity across patient population'
        AS AVG(DT_TRANSPLANT_ENRICHED.SVI_SCORE)
)

-- ═══════════════════════════════════════════════════════════════════════════
-- AI SQL GENERATION: Instructions for Cortex Analyst
-- These guide how the AI translates natural language to SQL
-- ═══════════════════════════════════════════════════════════════════════════
AI_SQL_GENERATION (
    INSTRUCTIONS = '
        ## Context
        This data represents hematopoietic cell transplant (HCT) outcomes from the 
        The Life Saving Company (LSC) / National Transplant Registry registry. The "Donor for All"
        initiative aims to ensure every patient has access to a well-matched donor
        regardless of racial or ethnic background.
        
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
        - Use DT_TRANSPLANT_ENRICHED for patient-level detail queries
        - Use DT_GVHD_ANALYTICS for aggregated summary/trend queries
        - When comparing donor types, use DONOR_TYPE_LABEL for readable output
        - For survival analysis, prefer ONE_YEAR_SURVIVOR / TWO_YEAR_SURVIVOR booleans
        - Always include sample size (COUNT) when showing rates or averages
        - For health equity questions, cross-reference PATIENT_RACE_ETHNICITY with outcomes
        - SVI_SCORE ranges from 0 (least vulnerable) to 1 (most vulnerable)
        - GVHD_RISK_SCORE ranges from 0 (lowest risk) to 1 (highest risk)
    ',
    
    -- Verified queries: these are pre-validated question-SQL pairs.
    -- They appear as suggested questions in Snowflake Intelligence and
    -- ensure consistent, trusted answers for the most common questions.
    -- use_as_onboarding_question: true → shows in Snowflake Intelligence UI
    VERIFIED QUERIES (
    
        -- ═══════════════════════════════════════════════════════════════
        -- Verified Query 1: GVHD Rate by Donor Type
        -- The most fundamental question in transplant outcomes research
        -- ═══════════════════════════════════════════════════════════════
        'What is the overall GVHD rate by donor type?'
            AS 'SELECT 
                    DONOR_TYPE_LABEL,
                    COUNT(*) AS TOTAL_TRANSPLANTS,
                    COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) AS SIGNIFICANT_GVHD,
                    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) * 100.0 / COUNT(*), 1) AS GVHD_RATE_PCT,
                    ROUND(AVG(GVHD_RISK_SCORE), 3) AS AVG_RISK_SCORE
                FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
                GROUP BY DONOR_TYPE_LABEL
                ORDER BY GVHD_RATE_PCT DESC'
            USE_AS_ONBOARDING_QUESTION = TRUE,
        
        -- ═══════════════════════════════════════════════════════════════
        -- Verified Query 2: MUD vs MMUD Survival Comparison
        -- Core to the "Donor for All" thesis — MMUD approaching MUD
        -- ═══════════════════════════════════════════════════════════════
        'Compare survival rates between 8/8 matched and 7/8 mismatched donors'
            AS 'SELECT 
                    DONOR_TYPE_LABEL,
                    COUNT(*) AS TOTAL_PATIENTS,
                    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
                    ROUND(COUNT(CASE WHEN TWO_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS TWO_YEAR_SURVIVAL_PCT,
                    ROUND(AVG(SURVIVAL_DAYS)) AS AVG_SURVIVAL_DAYS,
                    ROUND(COUNT(CASE WHEN SURVIVAL_STATUS = ''ALIVE'' THEN 1 END) * 100.0 / COUNT(*), 1) AS CURRENTLY_ALIVE_PCT
                FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
                WHERE DONOR_TYPE IN (''MUD_8_8'', ''MMUD_7_8'')
                GROUP BY DONOR_TYPE_LABEL
                ORDER BY DONOR_TYPE_LABEL'
            USE_AS_ONBOARDING_QUESTION = TRUE,
        
        -- ═══════════════════════════════════════════════════════════════
        -- Verified Query 3: Transplant Center Performance
        -- Which centers achieve the best outcomes?
        -- ═══════════════════════════════════════════════════════════════
        'Which transplant centers have the best outcomes?'
            AS 'SELECT 
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
                ORDER BY ONE_YEAR_SURVIVAL_PCT DESC'
            USE_AS_ONBOARDING_QUESTION = TRUE,
        
        -- ═══════════════════════════════════════════════════════════════
        -- Verified Query 4: GVHD Risk Factors
        -- What drives severe GVHD? Actionable clinical intelligence.
        -- ═══════════════════════════════════════════════════════════════
        'What are the top risk factors for acute GVHD Grade 3-4?'
            AS 'SELECT 
                    ''Age Group'' AS FACTOR, AGE_GROUP AS VALUE,
                    COUNT(*) AS N,
                    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 3 THEN 1 END) * 100.0 / COUNT(*), 1) AS SEVERE_GVHD_PCT
                FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
                GROUP BY AGE_GROUP
                UNION ALL
                SELECT ''Donor Type'', DONOR_TYPE_LABEL, COUNT(*),
                    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 3 THEN 1 END) * 100.0 / COUNT(*), 1)
                FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
                GROUP BY DONOR_TYPE_LABEL
                UNION ALL
                SELECT ''Conditioning'', CONDITIONING_INTENSITY, COUNT(*),
                    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 3 THEN 1 END) * 100.0 / COUNT(*), 1)
                FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
                GROUP BY CONDITIONING_INTENSITY
                UNION ALL
                SELECT ''Sex Mismatch'', CASE WHEN SEX_MISMATCH_FLAG THEN ''F→M Mismatch'' ELSE ''No Mismatch'' END, COUNT(*),
                    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 3 THEN 1 END) * 100.0 / COUNT(*), 1)
                FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
                GROUP BY SEX_MISMATCH_FLAG
                ORDER BY SEVERE_GVHD_PCT DESC'
            USE_AS_ONBOARDING_QUESTION = TRUE,
        
        -- ═══════════════════════════════════════════════════════════════
        -- Verified Query 5: Monthly Transplant Trends
        -- Volume and outcome trends over time
        -- ═══════════════════════════════════════════════════════════════
        'Show monthly transplant volume trends'
            AS 'SELECT 
                    TRANSPLANT_MONTH,
                    SUM(TRANSPLANT_COUNT) AS MONTHLY_TRANSPLANTS,
                    ROUND(AVG(GVHD_RATE_PCT), 1) AS AVG_GVHD_RATE,
                    ROUND(AVG(ONE_YEAR_SURVIVAL_PCT), 1) AS AVG_1YR_SURVIVAL
                FROM MARROWCO_DONOR_LAB.HOL.DT_GVHD_ANALYTICS
                GROUP BY TRANSPLANT_MONTH
                ORDER BY TRANSPLANT_MONTH'
            USE_AS_ONBOARDING_QUESTION = TRUE,
        
        -- ═══════════════════════════════════════════════════════════════
        -- Verified Query 6: Health Equity — Race/Ethnicity & Outcomes
        -- Critical for "Donor for All" mission
        -- ═══════════════════════════════════════════════════════════════
        'How does patient race and ethnicity affect donor availability and outcomes?'
            AS 'SELECT 
                    PATIENT_RACE_ETHNICITY,
                    COUNT(*) AS TOTAL_PATIENTS,
                    ROUND(AVG(HLA_MATCH_SCORE), 1) AS AVG_HLA_MATCH,
                    ROUND(COUNT(CASE WHEN DONOR_TYPE = ''MUD_8_8'' THEN 1 END) * 100.0 / COUNT(*), 1) AS FULLY_MATCHED_PCT,
                    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
                    ROUND(AVG(GVHD_RISK_SCORE), 3) AS AVG_RISK_SCORE,
                    ROUND(AVG(SVI_SCORE), 3) AS AVG_SVI_SCORE
                FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
                GROUP BY PATIENT_RACE_ETHNICITY
                ORDER BY TOTAL_PATIENTS DESC'
            USE_AS_ONBOARDING_QUESTION = TRUE,

        -- ═══════════════════════════════════════════════════════════════
        -- Verified Query 7: PTCy Impact on Haploidentical Outcomes
        -- Key clinical question — PTCy revolutionized HAPLO transplants
        -- ═══════════════════════════════════════════════════════════════
        'What is the impact of PTCy on haploidentical transplant outcomes?'
            AS 'SELECT 
                    CASE WHEN PTCY_BASED_PROPHYLAXIS THEN ''PTCy-Based'' ELSE ''Non-PTCy'' END AS PROPHYLAXIS_TYPE,
                    COUNT(*) AS TOTAL_PATIENTS,
                    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 2 THEN 1 END) * 100.0 / COUNT(*), 1) AS GVHD_RATE_PCT,
                    ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 3 THEN 1 END) * 100.0 / COUNT(*), 1) AS SEVERE_GVHD_PCT,
                    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
                    ROUND(AVG(TIME_TO_ENGRAFTMENT_DAYS), 1) AS AVG_ENGRAFTMENT_DAYS
                FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
                WHERE DONOR_TYPE = ''HAPLO''
                GROUP BY PTCY_BASED_PROPHYLAXIS
                ORDER BY PROPHYLAXIS_TYPE'
            USE_AS_ONBOARDING_QUESTION = TRUE,

        -- ═══════════════════════════════════════════════════════════════
        -- Verified Query 8: Social Vulnerability & Transplant Outcomes
        -- Health equity analysis using CDC SVI data
        -- ═══════════════════════════════════════════════════════════════
        'How does social vulnerability affect transplant outcomes?'
            AS 'SELECT 
                    SVI_CATEGORY,
                    COUNT(*) AS TOTAL_PATIENTS,
                    ROUND(AVG(SURVIVAL_DAYS)) AS AVG_SURVIVAL_DAYS,
                    ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_SURVIVAL_PCT,
                    ROUND(AVG(GVHD_RISK_SCORE), 3) AS AVG_RISK_SCORE,
                    ROUND(AVG(TIME_TO_ENGRAFTMENT_DAYS), 1) AS AVG_ENGRAFTMENT_DAYS,
                    ROUND(SUM(RELAPSE_FLAG) * 100.0 / COUNT(*), 1) AS RELAPSE_RATE_PCT
                FROM MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED
                GROUP BY SVI_CATEGORY
                ORDER BY AVG_RISK_SCORE DESC'
            USE_AS_ONBOARDING_QUESTION = TRUE
    )
)

-- ═══════════════════════════════════════════════════════════════════════════
-- AI QUESTION CATEGORIZATION: Guardrails
-- Defines what questions the AI should and should NOT answer
-- ═══════════════════════════════════════════════════════════════════════════
AI_QUESTION_CATEGORIZATION (
    INSTRUCTIONS = '
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
);

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify the Semantic View                                                 ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

SHOW SEMANTIC VIEWS IN SCHEMA MARROWCO_DONOR_LAB.HOL;

DESCRIBE SEMANTIC VIEW MARROWCO_TRANSPLANT_ANALYTICS;
