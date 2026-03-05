/*=============================================================================
  LSC Donor for All Data Lab -- Cortex Search Service
  =============================================================================
  
  Creates a Cortex Search Service on the clinical notes table to enable
  hybrid search (vector + keyword) over unstructured physician narratives.
  
  WHY CORTEX SEARCH?
    Looker and traditional BI tools can only query structured data.
    But 80% of clinical intelligence lives in unstructured text:
      - Physician notes describing GVHD symptoms and treatment response
      - Discharge summaries with nuanced clinical context
      - Research annotations linking cases to ongoing studies

    Cortex Search provides:
      + Hybrid search: vector similarity + BM25 keyword matching
      + Neural reranking for clinical relevance
      + Automatic sync with source table changes
      + Filterable by metadata (note type, transplant ID)
      + Direct integration with Cortex Agents for RAG
  
  The Cortex Agent uses this search service to answer questions about
  individual patient experiences, treatment responses, and clinical nuances
  that structured data alone cannot capture.
  
  Run after: Admin has loaded data (02_load_data.sql)
  Run before: 06_create_agent.sql
  =============================================================================*/

-- ════════════════════════════════════════════════════════════════════════════
-- SET YOUR USER NUMBER (assigned by the lab admin)
-- ════════════════════════════════════════════════════════════════════════════
SET USER_NUM = '01';  -- << CHANGE THIS TO YOUR ASSIGNED NUMBER (01-20)

USE ROLE IDENTIFIER('MARROWCO_HOL_ROLE_' || $USER_NUM);
USE WAREHOUSE IDENTIFIER('MARROWCO_HOL_WH_' || $USER_NUM);
USE SCHEMA IDENTIFIER('MARROWCO_DONOR_LAB.HOL_USER_' || $USER_NUM);

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Create Cortex Search Service on Clinical Notes                           ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ - SEARCH_COLUMN: NOTE_TEXT -- the main text field to search              ║
-- ║ - ATTRIBUTES: metadata columns available for filtering & display        ║
-- ║ - TARGET_LAG: auto-refresh when source data changes                     ║
-- ║ - SOURCE: Reads from SHARED schema (MARROWCO_DONOR_LAB.HOL)            ║
-- ║ - CREATED IN: Your per-user schema (HOL_USER_<NN>)                     ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE CORTEX SEARCH SERVICE CLINICAL_NOTES_SEARCH
    ON NOTE_TEXT
    ATTRIBUTES NOTE_ID, TRANSPLANT_ID, NOTE_DATE, NOTE_TYPE, PHYSICIAN_ID
    WAREHOUSE = IDENTIFIER('MARROWCO_HOL_WH_' || $USER_NUM)
    TARGET_LAG = '1 MINUTE'
    COMMENT = 'Hybrid search over clinical notes -- enables RAG for the LSC Research Agent'
AS (
    SELECT
        NOTE_ID,
        TRANSPLANT_ID,
        NOTE_DATE,
        NOTE_TYPE,
        PHYSICIAN_ID,
        NOTE_TEXT
    FROM MARROWCO_DONOR_LAB.HOL.CLINICAL_NOTES
);

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify the Search Service                                                ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

SHOW CORTEX SEARCH SERVICES;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Test Queries -- Try these after the service is ready                      ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ NOTE: The search service may take 1-2 minutes to fully index.           ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Test 1: Search for GVHD-related clinical observations
-- SELECT SNOWFLAKE.CORTEX.SEARCH(
--     'CLINICAL_NOTES_SEARCH',
--     'severe skin GVHD with rash and ruxolitinib treatment',
--     { 'limit': 5 }
-- );

-- Test 2: Search for specific treatment responses
-- SELECT SNOWFLAKE.CORTEX.SEARCH(
--     'CLINICAL_NOTES_SEARCH',
--     'PTCy prophylaxis outcomes haploidentical',
--     { 'limit': 5, 'filter': {'@eq': {'NOTE_TYPE': 'RESEARCH_ANNOTATION'}} }
-- );

-- Test 3: Search for discharge summaries mentioning engraftment
-- SELECT SNOWFLAKE.CORTEX.SEARCH(
--     'CLINICAL_NOTES_SEARCH',
--     'engraftment neutrophil recovery discharge',
--     { 'limit': 5, 'filter': {'@eq': {'NOTE_TYPE': 'DISCHARGE_SUMMARY'}} }
-- );
