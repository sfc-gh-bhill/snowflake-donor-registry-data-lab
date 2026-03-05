/*=============================================================================
  LSC Donor for All Data Lab -- Cortex Agent
  =============================================================================
  
  Creates the LSC Research Agent -- an AI assistant that can:
    1. Query structured transplant data via Cortex Analyst (Semantic View)
    2. Search unstructured clinical notes via Cortex Search
    3. Generate charts and visualizations from data
    4. Search the web for latest GVHD research
  
  HOW THE AGENT WORKS:
    1. UNDERSTANDS your question in natural language
    2. DECIDES which tool(s) to use
    3. EXECUTES the tool(s) autonomously
    4. SYNTHESIZES results into a coherent answer

  MULTI-USER NOTE:
    The agent is created in YOUR per-user schema and references YOUR
    per-user semantic view and search service. Each participant has their
    own independent agent instance.
  
  Run after: 04_cortex_search.sql, 05_semantic_view.sql
  =============================================================================*/

-- ════════════════════════════════════════════════════════════════════════════
-- SET YOUR USER NUMBER (assigned by the lab admin)
-- ════════════════════════════════════════════════════════════════════════════
SET USER_NUM = '01';  -- << CHANGE THIS TO YOUR ASSIGNED NUMBER (01-20)

USE ROLE IDENTIFIER('MARROWCO_HOL_ROLE_' || $USER_NUM);
USE WAREHOUSE IDENTIFIER('MARROWCO_HOL_WH_' || $USER_NUM);
USE SCHEMA IDENTIFIER('MARROWCO_DONOR_LAB.HOL_USER_' || $USER_NUM);

-- Build fully-qualified references for the agent's tool resources
SET MY_SCHEMA = 'MARROWCO_DONOR_LAB.HOL_USER_' || $USER_NUM;
SET MY_SEMANTIC_VIEW = $MY_SCHEMA || '.MARROWCO_TRANSPLANT_ANALYTICS';
SET MY_SEARCH_SERVICE = $MY_SCHEMA || '.CLINICAL_NOTES_SEARCH';

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ CREATE THE AGENT                                                         ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- NOTE: The agent YAML spec requires literal strings for tool_resources.
-- We use a stored procedure to inject the per-user schema dynamically.

DECLARE
    agent_ddl VARCHAR;
BEGIN
    agent_ddl := '
CREATE OR REPLACE AGENT MARROWCO_RESEARCH_AGENT
COMMENT = ''LSC Research Agent -- AI assistant for transplant outcome research with structured + unstructured intelligence''
FROM SPECIFICATION $$
orchestration:
  budget:
    seconds: 60
    tokens: 32000

instructions:
  system: |
    You are the MarrowCo Research Agent, a clinical transplant outcomes research assistant
    supporting the MarrowCo "Donor for All" initiative.

    Key Clinical Context:
    - GVHD (Graft-versus-Host Disease) is the primary complication of allogeneic HCT
    - The Donor for All initiative aims to expand donor access for diverse patients
    - MMUD (7/8 match) outcomes are approaching MUD (8/8) outcomes with modern protocols
    - PTCy (post-transplant cyclophosphamide) has revolutionized haploidentical transplants
    - SVI (Social Vulnerability Index) correlates with transplant outcomes
    - 80% of clinical intelligence is in unstructured notes, not structured data

  orchestration: |
    For structured data questions (counts, rates, comparisons, trends), use the transplant_analyst tool.
    For clinical narrative questions (treatment responses, patient experiences), use the clinical_notes_search tool.
    For combined questions, use BOTH tools and synthesize results into a unified answer.
    For visualization requests, use the chart_generator tool.
    For latest research questions, use the research_search tool.

  response: |
    Always cite sample sizes when reporting rates or averages.
    Use clinical terminology correctly (GVHD, HCT, MUD, MMUD, HAPLO, PTCy).
    Highlight health equity implications when relevant.
    When comparing donor types, note the Donor for All context.
    Provide actionable insights, not just data points.

  sample_questions:
    - question: "What is the overall GVHD rate by donor type?"
      answer: "I''ll analyze the GVHD rates across different donor types using the transplant analytics data."
    - question: "Compare survival outcomes between matched and mismatched donors"
      answer: "I''ll compare survival rates between MUD (8/8) and MMUD (7/8) donors."
    - question: "What do clinical notes say about ruxolitinib treatment for severe GVHD?"
      answer: "I''ll search the clinical notes for mentions of ruxolitinib treatment and outcomes."
    - question: "How does social vulnerability affect transplant success?"
      answer: "I''ll analyze transplant outcomes by Social Vulnerability Index category."

tools:
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: transplant_analyst
      description: >
        Query structured transplant outcome data including GVHD rates, survival
        statistics, donor type comparisons, engraftment metrics, risk scores,
        and health equity metrics. Uses the verified semantic view for trusted,
        consistent analytics.
  - tool_spec:
      type: cortex_search
      name: clinical_notes_search
      description: >
        Search unstructured clinical notes including physician follow-up notes,
        GVHD assessments, discharge summaries, and research annotations. Use
        this for clinical context, treatment response details, and patient
        experience information that structured data cannot capture.
  - tool_spec:
      type: data_to_chart
      name: chart_generator
      description: >
        Generate charts and visualizations from data. Use when the user asks
        for visual representations of transplant outcomes, trends, comparisons,
        or distributions.
  - tool_spec:
      type: web_search
      name: research_search
      description: >
        Search the web for the latest GVHD research, clinical trial results,
        MarrowCo publications, and transplant outcome studies. Use for questions
        about cutting-edge treatments, ongoing trials, or recent publications
        not captured in the local data.

tool_resources:
  transplant_analyst:
    semantic_view: "' || $MY_SEMANTIC_VIEW || '"
  clinical_notes_search:
    name: "' || $MY_SEARCH_SERVICE || '"
$$
;';
    EXECUTE IMMEDIATE agent_ddl;
    RETURN 'Agent created with semantic_view=' || $MY_SEMANTIC_VIEW || ' and search=' || $MY_SEARCH_SERVICE;
END;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify the Agent                                                         ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

SHOW AGENTS;

DESCRIBE AGENT MARROWCO_RESEARCH_AGENT;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Test the Agent (run these interactively)                                 ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ You can also test via Snowflake Intelligence UI:                         ║
-- ║   1. Go to AI & ML > Snowflake Intelligence                             ║
-- ║   2. Click "New Analyst" (or "+" button)                                ║
-- ║   3. Select: "Use an Agent"                                             ║
-- ║   4. Choose: MARROWCO_RESEARCH_AGENT (in your schema)                   ║
-- ║   5. Name it: "LSC Research Intelligence"                               ║
-- ║   6. Click "Create"                                                      ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Try these questions in Snowflake Intelligence or the Streamlit app:
--
--   Structured: "What is the overall GVHD rate by donor type?"
--   Unstructured: "What do clinical notes say about ruxolitinib for severe GVHD?"
--   Combined: "Compare haploidentical vs MUD survival and find clinical evidence for PTCy"
--   Chart: "Create a bar chart comparing 1-year survival rates by donor type"
--   Web Search: "Search for latest 2024-2025 publications on GVHD prevention with PTCy"
