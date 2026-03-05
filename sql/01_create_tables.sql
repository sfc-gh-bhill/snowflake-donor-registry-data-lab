/*=============================================================================
  LSC Donor for All Data Lab — Create Tables
  =============================================================================
  Creates the base (Bronze) landing tables for transplant outcome data
  and clinical notes.
  
  These tables receive raw data from CSV files and serve as the foundation
  for the Dynamic Tables pipeline (Bronze → Silver → Gold).
  
  Run after: 00_bootstrap.sql
  Run before: 02_load_data.sql
  =============================================================================*/

USE ROLE MARROWCO_HOL_ROLE;
USE WAREHOUSE MARROWCO_HOL_WH;
USE SCHEMA MARROWCO_DONOR_LAB.HOL;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ TABLE 1: TRANSPLANT_OUTCOMES (Structured Data — Bronze)                  ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Primary structured dataset containing transplant procedure details,      ║
-- ║ patient/donor demographics, and clinical outcomes.                        ║
-- ║                                                                          ║
-- ║ Key columns for analysis:                                                ║
-- ║   - DONOR_TYPE: MUD_8_8, MMUD_7_8, HAPLO, CORD                         ║
-- ║   - GVHD_RISK_SCORE: ML target variable (0.00 - 1.00)                  ║
-- ║   - ACUTE_GVHD_GRADE: Clinical outcome (0-4)                           ║
-- ║   - SURVIVAL_STATUS: ALIVE / DECEASED                                    ║
-- ║   - SVI_SCORE: Social Vulnerability Index (health equity metric)         ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE TABLE TRANSPLANT_OUTCOMES (
    TRANSPLANT_ID           VARCHAR(20)   NOT NULL,    -- Primary key: TXP-00001
    PATIENT_ID              VARCHAR(20)   NOT NULL,    -- Patient identifier: PAT-00001
    PATIENT_AGE             NUMBER(3,0)   NOT NULL,    -- Age at transplant
    PATIENT_SEX             VARCHAR(10)   NOT NULL,    -- Male / Female
    PATIENT_RACE_ETHNICITY  VARCHAR(50)   NOT NULL,    -- Self-reported race/ethnicity
    DIAGNOSIS               VARCHAR(100)  NOT NULL,    -- Primary diagnosis
    DIAGNOSIS_CATEGORY      VARCHAR(50)   NOT NULL,    -- Leukemia, Lymphoma, MDS/MPN, etc.
    DISEASE_STAGE           VARCHAR(30)   NOT NULL,    -- Early, Intermediate, Advanced, CR1, CR2, etc.
    DONOR_TYPE              VARCHAR(20)   NOT NULL,    -- MUD_8_8, MMUD_7_8, HAPLO, CORD
    HLA_MATCH_SCORE         NUMBER(2,0)   NOT NULL,    -- HLA match out of 8
    DONOR_AGE               NUMBER(3,0)   NOT NULL,    -- Donor age
    DONOR_SEX               VARCHAR(10)   NOT NULL,    -- Male / Female
    CONDITIONING_REGIMEN    VARCHAR(100)  NOT NULL,    -- MAC, RIC, NMA subtypes
    GVHD_PROPHYLAXIS        VARCHAR(100)  NOT NULL,    -- Immunosuppression protocol
    TRANSPLANT_DATE         DATE          NOT NULL,    -- Date of HCT procedure
    TRANSPLANT_CENTER_ID    VARCHAR(10)   NOT NULL,    -- Center identifier
    CENTER_REGION           VARCHAR(20)   NOT NULL,    -- Geographic region
    CENTER_STATE            VARCHAR(5)    NOT NULL,    -- US state abbreviation
    TIME_TO_ENGRAFTMENT_DAYS NUMBER(4,0)  NOT NULL,    -- Days to neutrophil engraftment
    ACUTE_GVHD_GRADE        NUMBER(1,0)  NOT NULL,    -- Grade 0-4 (0 = none)
    CHRONIC_GVHD            VARCHAR(20)   NOT NULL,    -- NONE, MILD, MODERATE, SEVERE
    RELAPSE_FLAG            NUMBER(1,0)   NOT NULL,    -- 0 = no relapse, 1 = relapsed
    SURVIVAL_DAYS           NUMBER(5,0)   NOT NULL,    -- Days of survival post-transplant
    SURVIVAL_STATUS         VARCHAR(10)   NOT NULL,    -- ALIVE / DECEASED
    GVHD_RISK_SCORE         FLOAT         NOT NULL,    -- Predicted risk score (0.00 - 1.00)
    PATIENT_ZIP_3DIGIT      VARCHAR(5)    NOT NULL,    -- 3-digit ZIP for geographic analysis
    SVI_SCORE               FLOAT         NOT NULL,    -- CDC Social Vulnerability Index (0.0 - 1.0)

    -- Constraints
    CONSTRAINT PK_TRANSPLANT PRIMARY KEY (TRANSPLANT_ID)
)
COMMENT = 'Bronze layer: Raw transplant outcome data from National Transplant Registry registry (synthetic for HOL)';

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ TABLE 2: CLINICAL_NOTES (Unstructured Data — Bronze)                     ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Physician narratives, GVHD assessments, discharge summaries, and         ║
-- ║ research annotations. This is the unstructured data that Looker           ║
-- ║ cannot handle — representing 80% of clinical intelligence.               ║
-- ║                                                                          ║
-- ║ Used by Cortex Search for semantic retrieval and RAG-based Q&A.          ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE TABLE CLINICAL_NOTES (
    NOTE_ID         VARCHAR(20)     NOT NULL,    -- Primary key: NOTE-00001
    TRANSPLANT_ID   VARCHAR(20)     NOT NULL,    -- FK to TRANSPLANT_OUTCOMES
    NOTE_DATE       DATE            NOT NULL,    -- Date of clinical note
    NOTE_TYPE       VARCHAR(40)     NOT NULL,    -- POST_TRANSPLANT_FOLLOWUP, GVHD_ASSESSMENT, etc.
    PHYSICIAN_ID    VARCHAR(10)     NOT NULL,    -- Physician identifier
    NOTE_TEXT       VARCHAR(5000)   NOT NULL,    -- Full clinical narrative text

    -- Constraints
    CONSTRAINT PK_NOTES PRIMARY KEY (NOTE_ID),
    CONSTRAINT FK_NOTES_TRANSPLANT FOREIGN KEY (TRANSPLANT_ID) 
        REFERENCES TRANSPLANT_OUTCOMES(TRANSPLANT_ID)
)
COMMENT = 'Bronze layer: Unstructured clinical notes — physician narratives, GVHD assessments, research annotations';

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify tables created                                                    ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
SELECT 'TRANSPLANT_OUTCOMES' AS TABLE_NAME, COUNT(*) AS COLUMN_COUNT 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'HOL' AND TABLE_NAME = 'TRANSPLANT_OUTCOMES'
UNION ALL
SELECT 'CLINICAL_NOTES', COUNT(*) 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'HOL' AND TABLE_NAME = 'CLINICAL_NOTES';
