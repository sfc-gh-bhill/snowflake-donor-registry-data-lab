/*=============================================================================
  LSC Donor for All Data Lab — Load Data
  =============================================================================
  Uploads CSV files to the internal stage and loads them into tables.
  
  Two options are provided:
    Option A: Upload from local machine via SnowSQL/Snowsight
    Option B: Upload from GitHub URL (if using Cortex Code)
  
  Run after: 01_create_tables.sql
  Run before: 03_dynamic_tables.sql
  =============================================================================*/

USE ROLE MARROWCO_HOL_ROLE;
USE WAREHOUSE MARROWCO_HOL_WH;
USE SCHEMA MARROWCO_DONOR_LAB.HOL;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ OPTION A: Upload via Snowsight UI                                        ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ 1. Go to Data > Databases > MARROWCO_DONOR_LAB > HOL > Stages > DATA_STAGE  ║
-- ║ 2. Click "+ Files" button                                                ║
-- ║ 3. Upload transplant_outcomes.csv and clinical_notes.csv                 ║
-- ║ 4. Then run the COPY INTO statements below                               ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ OPTION B: Upload via Snow CLI (run in your terminal, NOT in a SQL        ║
-- ║ worksheet). Run from the repo root directory.                            ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║                                                                          ║
-- ║   snow stage copy data/transplant_outcomes.csv                           ║
-- ║     @MARROWCO_DONOR_LAB.HOL.DATA_STAGE --overwrite                      ║
-- ║     -c <your_connection> --role MARROWCO_HOL_ROLE                        ║
-- ║                                                                          ║
-- ║   snow stage copy data/clinical_notes.csv                                ║
-- ║     @MARROWCO_DONOR_LAB.HOL.DATA_STAGE --overwrite                      ║
-- ║     -c <your_connection> --role MARROWCO_HOL_ROLE                        ║
-- ║                                                                          ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 1: Verify files are staged                                          ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
LIST @DATA_STAGE;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 2: Load TRANSPLANT_OUTCOMES                                         ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
COPY INTO TRANSPLANT_OUTCOMES
FROM @DATA_STAGE/transplant_outcomes.csv
FILE_FORMAT = CSV_FORMAT
ON_ERROR = 'CONTINUE'
PURGE = FALSE;

-- Verify load
SELECT 
    COUNT(*) AS ROW_COUNT,
    COUNT(DISTINCT DONOR_TYPE) AS DONOR_TYPES,
    COUNT(DISTINCT DIAGNOSIS) AS DIAGNOSES,
    MIN(TRANSPLANT_DATE) AS EARLIEST_TRANSPLANT,
    MAX(TRANSPLANT_DATE) AS LATEST_TRANSPLANT,
    '✅ Transplant outcomes loaded' AS STATUS
FROM TRANSPLANT_OUTCOMES;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 3: Load CLINICAL_NOTES                                              ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
COPY INTO CLINICAL_NOTES
FROM @DATA_STAGE/clinical_notes.csv
FILE_FORMAT = CSV_FORMAT
ON_ERROR = 'CONTINUE'
PURGE = FALSE;

-- Verify load
SELECT 
    COUNT(*) AS ROW_COUNT,
    COUNT(DISTINCT NOTE_TYPE) AS NOTE_TYPES,
    COUNT(DISTINCT TRANSPLANT_ID) AS LINKED_TRANSPLANTS,
    AVG(LENGTH(NOTE_TEXT))::INT AS AVG_NOTE_LENGTH,
    '✅ Clinical notes loaded' AS STATUS
FROM CLINICAL_NOTES;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 4: Quick data quality check                                         ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
-- Verify FK integrity: all clinical note TRANSPLANT_IDs exist in outcomes
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '✅ FK integrity verified — all notes link to valid transplants'
        ELSE '❌ WARNING: ' || COUNT(*) || ' orphaned clinical notes found'
    END AS FK_CHECK
FROM CLINICAL_NOTES cn
LEFT JOIN TRANSPLANT_OUTCOMES t ON cn.TRANSPLANT_ID = t.TRANSPLANT_ID
WHERE t.TRANSPLANT_ID IS NULL;

-- Preview the data
SELECT * FROM TRANSPLANT_OUTCOMES LIMIT 5;
SELECT * FROM CLINICAL_NOTES LIMIT 5;
