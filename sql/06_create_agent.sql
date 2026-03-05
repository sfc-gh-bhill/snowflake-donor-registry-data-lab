/*=============================================================================
  LSC Donor for All Data Lab — Cortex Agent
  =============================================================================
  
  Creates the LSC Research Agent — an AI assistant that can:
    1. Query structured transplant data via Cortex Analyst (Semantic View)
    2. Search unstructured clinical notes via Cortex Search
    3. Generate charts and visualizations from data
    4. Search the web for latest GVHD research
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ HOW THE AGENT WORKS                                                     │
  │                                                                        │
  │ The Cortex Agent is an autonomous AI that:                              │
  │                                                                        │
  │ 1. UNDERSTANDS your question in natural language                        │
  │ 2. DECIDES which tool(s) to use:                                       │
  │    • Structured data question? → Cortex Analyst (Semantic View)        │
  │    • Clinical note search? → Cortex Search                             │
  │    • Need a chart? → Data-to-Chart                                     │
  │    • Latest research? → Web Search                                     │
  │    • Complex question? → Multiple tools in sequence                    │
  │ 3. EXECUTES the tool(s) autonomously                                   │
  │ 4. SYNTHESIZES results into a coherent answer                          │
  │                                                                        │
  │ KEY: The agent uses VERIFIED QUERIES from the Semantic View to         │
  │ ensure trusted, consistent answers. This is NOT just text generation — │
  │ it's grounded in validated SQL and real data.                           │
  │                                                                        │
  │ AUTONOMY: The agent chooses tools without user guidance.               │
  │ For example: "Compare GVHD outcomes and find clinical evidence for     │
  │ PTCy effectiveness" → Agent runs Analyst (structured) THEN Search      │
  │ (unstructured) and combines both into one answer.                       │
  │                                                                        │
  │ UNLIKE TRADITIONAL BI:                                                  │
  │ Snowflake can answer WHO, WHAT, WHERE, WHEN, WHY... and also HOW      │
  │ and provide RECOMMENDATIONS — because it combines structured data      │
  │ analytics with unstructured clinical intelligence and web research.    │
  └─────────────────────────────────────────────────────────────────────────┘
  
  Run after: 04_cortex_search.sql, 05_semantic_view.sql
  =============================================================================*/

USE ROLE MARROWCO_HOL_ROLE;
USE WAREHOUSE MARROWCO_HOL_WH;
USE SCHEMA MARROWCO_DONOR_LAB.HOL;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ CREATE THE AGENT                                                         ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE AGENT MARROWCO_RESEARCH_AGENT
COMMENT = 'LSC Research Agent — AI assistant for transplant outcome research with structured + unstructured intelligence'
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
      answer: "I'll analyze the GVHD rates across different donor types using the transplant analytics data."
    - question: "Compare survival outcomes between matched and mismatched donors"
      answer: "I'll compare survival rates between MUD (8/8) and MMUD (7/8) donors."
    - question: "What do clinical notes say about ruxolitinib treatment for severe GVHD?"
      answer: "I'll search the clinical notes for mentions of ruxolitinib treatment and outcomes."
    - question: "How does social vulnerability affect transplant success?"
      answer: "I'll analyze transplant outcomes by Social Vulnerability Index category."

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
    semantic_view: "MARROWCO_DONOR_LAB.HOL.MARROWCO_TRANSPLANT_ANALYTICS"
  clinical_notes_search:
    name: "MARROWCO_DONOR_LAB.HOL.CLINICAL_NOTES_SEARCH"
$$
;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify the Agent                                                         ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

SHOW AGENTS IN SCHEMA MARROWCO_DONOR_LAB.HOL;

DESCRIBE AGENT MARROWCO_RESEARCH_AGENT;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Test the Agent (run these interactively)                                 ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ You can also test via Snowflake Intelligence UI:                         ║
-- ║   1. Go to AI & ML > Snowflake Intelligence                             ║
-- ║   2. Create a new Analyst and select MARROWCO_RESEARCH_AGENT                ║
-- ║   3. The verified queries will appear as suggested questions             ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- ═══════════════════════════════════════════════════════════════════════════
-- HOW TO TEST THE AGENT
-- ═══════════════════════════════════════════════════════════════════════════
-- The agent is accessed via:
--   1. Snowflake Intelligence UI (AI & ML > Snowflake Intelligence)
--   2. The Cell Therapy Compass Streamlit app (Research Agent page)
--   3. The REST API: POST /api/v2/cortex/agent:run
--
-- Try these questions in Snowflake Intelligence or the Streamlit app:
--
--   Structured: "What is the overall GVHD rate by donor type?"
--   Unstructured: "What do clinical notes say about ruxolitinib for severe GVHD?"
--   Combined: "Compare haploidentical vs MUD survival and find clinical evidence for PTCy"
--   Chart: "Create a bar chart comparing 1-year survival rates by donor type"
--   Web Search: "Search for latest 2024-2025 publications on GVHD prevention with PTCy"
-- ═══════════════════════════════════════════════════════════════════════════
