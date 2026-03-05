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
  │ The Winter Cloud Platform can answer WHO, WHAT, WHERE, WHEN, WHY... and also HOW      │
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
FROM SPECIFICATION $$
spec_version: '1'
description: >
  LSC Research Agent — An AI-powered transplant outcome research assistant 
  for the The Life Saving Company. Answers questions about HCT outcomes, 
  GVHD risk factors, donor selection, health equity, and clinical evidence 
  using structured data, clinical notes, visualizations, and web research.

orchestration:
  auto

instructions: |
  You are the LSC Research Agent, a clinical transplant outcomes research assistant 
  supporting the The Life Saving Company's "Donor for All" initiative.
  
  ## Your Mission
  Help clinicians, researchers, and data analysts understand transplant outcomes 
  to improve donor selection and patient care for ALL patients, especially those 
  from underrepresented racial and ethnic backgrounds.
  
  ## How to Answer Questions
  
  1. **Structured data questions** (counts, rates, comparisons, trends):
     Use the cortex_analyst tool to query the semantic view. This gives you 
     access to verified, trusted analytics on transplant outcomes, GVHD rates,
     survival, engraftment, and risk factors.
  
  2. **Clinical narrative questions** (treatment responses, patient experiences):
     Use the cortex_search tool to find relevant physician notes, GVHD 
     assessments, discharge summaries, and research annotations.
  
  3. **Combined questions** (e.g., "What are the GVHD rates AND what do the 
     clinical notes say about treatment response?"):
     Use BOTH tools — first get the structured data, then search clinical 
     notes for supporting evidence. Synthesize into a unified answer.
  
  4. **Visualization requests** (charts, graphs):
     Use data_to_chart to create visualizations from query results.
  
  5. **Latest research questions**:
     Use web_search to find current publications and clinical trial results.
  
  ## Response Guidelines
  - Always cite sample sizes when reporting rates or averages
  - Use clinical terminology correctly (GVHD, HCT, MUD, MMUD, HAPLO, PTCy)
  - Highlight health equity implications when relevant
  - When comparing donor types, note the "Donor for All" context
  - Provide actionable insights, not just data points
  - If asked about recommendations, ground them in the data

  ## Key Clinical Context
  - GVHD (Graft-versus-Host Disease) is the primary complication of allogeneic HCT
  - The Donor for All initiative aims to expand donor access for diverse patients
  - MMUD (7/8 match) outcomes are approaching MUD (8/8) outcomes with modern protocols
  - PTCy (post-transplant cyclophosphamide) has revolutionized haploidentical transplants
  - SVI (Social Vulnerability Index) correlates with transplant outcomes
  - 80% of clinical intelligence is in unstructured notes, not structured data

sample_questions:
  - "What is the overall GVHD rate by donor type?"
  - "Compare survival outcomes between matched and mismatched donors"
  - "Show me a chart of transplant volume trends over time"
  - "What do clinical notes say about ruxolitinib treatment for severe GVHD?"
  - "Which patient populations have the worst outcomes and what can we do?"
  - "Search for the latest research on haploidentical transplant outcomes"
  - "How does social vulnerability affect transplant success?"
  - "Create a visualization comparing GVHD rates across donor types"

tools:
  # ─── Tool 1: Cortex Analyst (Structured Data via Semantic View) ───
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: transplant_analyst
      description: >
        Query structured transplant outcome data including GVHD rates, survival 
        statistics, donor type comparisons, engraftment metrics, risk scores, 
        and health equity metrics. Uses the verified semantic view for trusted, 
        consistent analytics.
    tool_resources:
      semantic_view: "MARROWCO_DONOR_LAB.HOL.MARROWCO_TRANSPLANT_ANALYTICS"

  # ─── Tool 2: Cortex Search (Unstructured Clinical Notes) ───
  - tool_spec:
      type: cortex_search
      name: clinical_notes_search
      description: >
        Search unstructured clinical notes including physician follow-up notes, 
        GVHD assessments, discharge summaries, and research annotations. Use 
        this for clinical context, treatment response details, and patient 
        experience information that structured data cannot capture.
    tool_resources:
      cortex_search_service: "MARROWCO_DONOR_LAB.HOL.CLINICAL_NOTES_SEARCH"

  # ─── Tool 3: Data-to-Chart (Visualizations) ───
  - tool_spec:
      type: data_to_chart
      name: chart_generator
      description: >
        Generate charts and visualizations from data. Use when the user asks 
        for visual representations of transplant outcomes, trends, comparisons, 
        or distributions.

  # ─── Tool 4: Web Search (Latest Research) ───
  - tool_spec:
      type: web_search
      name: research_search
      description: >
        Search the web for the latest GVHD research, clinical trial results, 
        LSC publications, and transplant outcome studies. Use for questions 
        about cutting-edge treatments, ongoing trials, or recent publications 
        not captured in the local data.
$$
COMMENT = 'LSC Research Agent — Autonomous AI assistant for transplant outcome research with structured + unstructured intelligence';

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify the Agent                                                         ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

SHOW AGENTS IN SCHEMA MARROWCO_DONOR_LAB.HOL;

DESCRIBE AGENT MARROWCO_RESEARCH_AGENT;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Test the Agent (run these interactively)                                 ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ You can also test via The Winter Cloud Platform Intelligence UI:                         ║
-- ║   1. Go to AI & ML > The Winter Cloud Platform Intelligence                             ║
-- ║   2. Create a new Analyst and select MARROWCO_RESEARCH_AGENT                ║
-- ║   3. The verified queries will appear as suggested questions             ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Test 1: Structured data query (should use cortex_analyst)
-- SELECT SNOWFLAKE.CORTEX.INVOKE_AGENT(
--     'MARROWCO_DONOR_LAB.HOL.MARROWCO_RESEARCH_AGENT',
--     'What is the overall GVHD rate by donor type?'
-- );

-- Test 2: Unstructured search (should use cortex_search)
-- SELECT SNOWFLAKE.CORTEX.INVOKE_AGENT(
--     'MARROWCO_DONOR_LAB.HOL.MARROWCO_RESEARCH_AGENT',
--     'What do clinical notes say about patients who responded well to ruxolitinib for severe GVHD?'
-- );

-- Test 3: Combined (should use both tools)
-- SELECT SNOWFLAKE.CORTEX.INVOKE_AGENT(
--     'MARROWCO_DONOR_LAB.HOL.MARROWCO_RESEARCH_AGENT',
--     'Compare haploidentical vs MUD survival rates and find clinical evidence supporting PTCy-based prophylaxis'
-- );

-- Test 4: Visualization (should use data_to_chart)
-- SELECT SNOWFLAKE.CORTEX.INVOKE_AGENT(
--     'MARROWCO_DONOR_LAB.HOL.MARROWCO_RESEARCH_AGENT',
--     'Create a bar chart comparing 1-year survival rates by donor type'
-- );
