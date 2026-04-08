# Donor for All Data Lab: Forecasting GVHD with Snowflake Intelligence

> **Duration:** 1.5 hours | **Level:** Beginner-Intermediate | **Presenter:** Braedon Hill, Sr. Solution Engineer — Snowflake

---

## Quick Start

Clone the repo and deploy the entire lab in under 10 minutes using **one of the two paths** below.

### Path A: Cortex Code / Snow CLI

```bash
# 1. Clone and enter the repo
git clone https://github.com/sfc-gh-bhill/customer-marrowco-donor-for-all-data-lab.git
cd customer-marrowco-donor-for-all-data-lab

# 2. Run SQL scripts in order (replace DEMO with your connection name)
snow sql -c DEMO -f sql/00_bootstrap.sql
snow sql -c DEMO -f sql/01_create_tables.sql

# 3. Upload CSV files to stage
snow stage copy data/transplant_outcomes.csv @MARROWCO_DONOR_LAB.HOL.DATA_STAGE \
  --overwrite -c DEMO --role MARROWCO_HOL_ROLE --database MARROWCO_DONOR_LAB --schema HOL
snow stage copy data/clinical_notes.csv @MARROWCO_DONOR_LAB.HOL.DATA_STAGE \
  --overwrite -c DEMO --role MARROWCO_HOL_ROLE --database MARROWCO_DONOR_LAB --schema HOL

# 4. Load data and build all objects
snow sql -c DEMO -f sql/02_load_data.sql
snow sql -c DEMO -f sql/03_dynamic_tables.sql
snow sql -c DEMO -f sql/04_cortex_search.sql
snow sql -c DEMO -f sql/05_semantic_view.sql
snow sql -c DEMO -f sql/06_create_agent.sql
snow sql -c DEMO -f sql/07_snowflake_intelligence.sql
snow sql -c DEMO -f sql/08_ml_model.sql
snow sql -c DEMO -f sql/09_grants.sql

# 5. Deploy the Streamlit app
snow streamlit deploy --replace -c DEMO \
  --project streamlit/ \
  --role MARROWCO_HOL_ROLE \
  --database MARROWCO_DONOR_LAB \
  --schema HOL
```

### Path B: Manual via Snowsight

1. **Download** or clone the repository from GitHub
2. Open **Snowsight** and create a new **SQL Worksheet**
3. Copy-paste and run each SQL script in order: `00_bootstrap.sql` → `01_create_tables.sql`
4. **Upload CSVs** — Navigate to **Data > Databases > MARROWCO_DONOR_LAB > HOL > Stages > DATA_STAGE**, click **"+ Files"**, and upload both CSV files from the `data/` folder
5. Run `02_load_data.sql` through `09_grants.sql` in order in the SQL Worksheet
6. **Deploy Streamlit** — Go to **Projects > Streamlit > + Streamlit App**, set Database to `MARROWCO_DONOR_LAB`, Schema to `HOL`, Warehouse to `MARROWCO_HOL_WH`, then upload all files from the `streamlit/` directory

---

## Overview

In this hands-on lab, you will build a complete data intelligence platform for the **Life Saving Company (LSC)** that forecasts Graft-versus-Host Disease (GVHD) outcomes using Snowflake's AI Data Cloud.

By the end of this lab, you will have:

- Loaded realistic transplant outcome and clinical note data
- Built a near real-time **Dynamic Tables** pipeline (Bronze → Silver → Gold)
- Created a **Semantic View** — the single source of truth for all analytics and AI
- Deployed a **Cortex Agent** that combines structured data, clinical notes, charts, and web search
- Connected the agent to **Snowflake Intelligence** with auto-suggested questions
- Trained a **GVHD risk prediction ML model** with the Snowflake Model Registry
- Explored a production-grade **Streamlit in Snowflake** application

### What You'll Learn

| Snowflake Capability | What It Does |
|---|---|
| **Dynamic Tables** | Declarative, auto-refreshing pipeline — replaces ETL orchestrators |
| **Semantic Views** | AI-native semantic layer — single source of truth for BI + AI |
| **Cortex Agent** | Autonomous AI with structured + unstructured data access |
| **Cortex Search** | Hybrid vector + keyword search over clinical notes |
| **Snowflake Intelligence** | Conversational analytics UI with auto-suggested questions |
| **ML Classification** | Native model training with evaluation metrics and registry |
| **Streamlit in Snowflake** | Production data applications with zero infrastructure |

---

## Prerequisites

Before the lab, complete the setup in **[prework/setup.md](prework/setup.md)**:

- [ ] Snowflake account (AWS US-East-1 preferred, cross-region calling enabled)
- [ ] `ACCOUNTADMIN` role access
- [ ] Cortex Code available (either Snowsight UI or CLI)

---

## Lab Outline (1.5 Hours)

| Time | Step | What You Do |
|---|---|---|
| 0:00 - 0:10 | **Step 1** | Overview & Bootstrap Infrastructure |
| 0:10 - 0:20 | **Step 2** | Load Data (structured + unstructured) |
| 0:20 - 0:40 | **Step 3** | Dynamic Tables + **Semantic View** (deep dive) |
| 0:40 - 0:55 | **Step 4** | Cortex Agent + Snowflake Intelligence |
| 0:55 - 1:05 | **Step 5** | ML Model (train + evaluate) |
| 1:05 - 1:20 | **Step 6** | Streamlit App Tour |
| 1:20 - 1:30 | **Step 7** | Take Action (email demo) + Wrap-up |

---

## Step 1: Bootstrap Infrastructure (10 min)

### 1.1 Download the Lab Materials

Clone or download this repository from GitHub:

```bash
git clone https://github.com/sfc-gh-bhill/customer-marrowco-donor-for-all-data-lab.git
cd customer-marrowco-donor-for-all-data-lab
```

### 1.2 Run the Bootstrap Script

📄 **File:** [`sql/00_bootstrap.sql`](sql/00_bootstrap.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/00_bootstrap.sql
```
Replace `DEMO` with your connection name.
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Open **Snowsight** → **SQL Worksheet**
2. Copy-paste the contents of `sql/00_bootstrap.sql`
3. Click **Run All**
</details>

This creates:
- **Role:** `MARROWCO_HOL_ROLE`
- **Database:** `MARROWCO_DONOR_LAB`
- **Schema:** `MARROWCO_DONOR_LAB.HOL`
- **Warehouse:** `MARROWCO_HOL_WH` (X-Small, auto-suspend 60s)
- **Stage:** `DATA_STAGE` with CSV file format
- All required grants (Dynamic Tables, Semantic Views, Cortex, Agents, ML)

> **Verify:** The final query should show `Status: ✅ Bootstrap complete — infrastructure ready!`

### 1.3 Create Tables

📄 **File:** [`sql/01_create_tables.sql`](sql/01_create_tables.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/01_create_tables.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Open a new **SQL Worksheet** (or continue in the same one)
2. Copy-paste the contents of `sql/01_create_tables.sql`
3. Click **Run All**
</details>

Creates two Bronze layer tables:
- **`TRANSPLANT_OUTCOMES`** — 500 structured transplant records (27 columns)
- **`CLINICAL_NOTES`** — 800 unstructured physician narratives (6 columns)

---

## Step 2: Load Data (10 min)

### 2.1 Upload CSV Files to Stage

<details>
<summary><strong>Option A: Snow CLI</strong></summary>

From the repo root directory:

```bash
snow stage copy data/transplant_outcomes.csv @MARROWCO_DONOR_LAB.HOL.DATA_STAGE \
  --overwrite -c DEMO --role MARROWCO_HOL_ROLE --database MARROWCO_DONOR_LAB --schema HOL

snow stage copy data/clinical_notes.csv @MARROWCO_DONOR_LAB.HOL.DATA_STAGE \
  --overwrite -c DEMO --role MARROWCO_HOL_ROLE --database MARROWCO_DONOR_LAB --schema HOL
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Navigate to: **Data > Databases > MARROWCO_DONOR_LAB > HOL > Stages > DATA_STAGE**
2. Click **"+ Files"**
3. Upload both files from the `data/` folder:
   - `transplant_outcomes.csv`
   - `clinical_notes.csv`
</details>

### 2.2 Load into Tables

📄 **File:** [`sql/02_load_data.sql`](sql/02_load_data.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/02_load_data.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Copy-paste the contents of `sql/02_load_data.sql` into a SQL Worksheet
2. Click **Run All**
</details>

> **Verify:** 500 transplant records and 800 clinical notes loaded. FK integrity check passes.

### About the Data

The synthetic data is modeled on real National Transplant Registry registry patterns:

| Dataset | Records | Type | Key Columns |
|---|---|---|---|
| Transplant Outcomes | 500 | Structured | Donor type, GVHD grade, survival, risk score, SVI |
| Clinical Notes | 800 | Unstructured | Physician narratives, GVHD assessments, research annotations |

**Donor type distribution** mirrors LSC registry reality:
- MUD 8/8 (Matched Unrelated): ~35%
- MMUD 7/8 (Mismatched): ~25%
- Haploidentical: ~30%
- Cord Blood: ~10%

---

## Step 3: Dynamic Tables + Semantic View (20 min)

> **This is the most important section of the lab.** The Dynamic Tables pipeline and Semantic View together form the foundation that every downstream consumer uses.

### 3.1 Create the Dynamic Tables Pipeline

📄 **File:** [`sql/03_dynamic_tables.sql`](sql/03_dynamic_tables.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/03_dynamic_tables.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Copy-paste the contents of `sql/03_dynamic_tables.sql` into a SQL Worksheet
2. Click **Run All**
</details>

This creates two Dynamic Tables:

**Silver: `DT_TRANSPLANT_ENRICHED`**
- Joins outcomes + notes
- Derives: age groups, risk tiers, SVI categories, sex mismatch flags
- **Target lag: 1 minute** — auto-refreshes when source data changes

**Gold: `DT_GVHD_ANALYTICS`**
- Pre-aggregated cohort metrics
- Snowflake automatically manages the dependency DAG
- No scheduler, no orchestrator, no code needed

#### Why Dynamic Tables? (Presenter Talking Points)

> **"In a traditional Looker or OBIEE environment, this pipeline would require:**
> - An ETL tool (Informatica, Fivetran) to extract data
> - A transformation layer (dbt, PDTs) to model it
> - A scheduler (Airflow, cron) to orchestrate refreshes
> - An admin to monitor and fix failures
>
> **With Snowflake Dynamic Tables, it's one SQL statement.** Snowflake handles incremental refresh, dependency ordering, and failure recovery automatically. The data is fresh within 1 minute."

### 3.2 Create the Cortex Search Service

📄 **File:** [`sql/04_cortex_search.sql`](sql/04_cortex_search.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/04_cortex_search.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Copy-paste the contents of `sql/04_cortex_search.sql` into a SQL Worksheet
2. Click **Run All**
</details>

Creates a hybrid vector + keyword search over clinical notes. This enables the Agent to search unstructured physician narratives — the 80% of clinical intelligence that Looker cannot access.

### 3.3 Create the Semantic View (Deep Dive)

📄 **File:** [`sql/05_semantic_view.sql`](sql/05_semantic_view.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/05_semantic_view.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Copy-paste the contents of `sql/05_semantic_view.sql` into a SQL Worksheet
2. Click **Run All**
</details>

> **Take time here.** Walk through the SQL carefully. This is the highest-interest area for the LSC team.

The Semantic View defines:

| Component | What It Does | Why It Matters |
|---|---|---|
| **TABLES** | Maps physical tables into the logical model | AI knows what data exists |
| **COLUMNS** | Dimensions (categorical) + Facts (numeric) with comments & synonyms | AI understands column meaning |
| **METRICS** | Pre-defined calculations (GVHD rate, survival rate, etc.) | Every consumer gets the same answer |
| **VERIFIED QUERIES** | 8 trusted question-SQL pairs | Creates a "trust layer" for governance |
| **AI_SQL_GENERATION** | Instructions for Cortex Analyst | Guides AI to write correct SQL |
| **AI_QUESTION_CATEGORIZATION** | Guardrails for appropriate questions | Prevents misuse |

#### Semantic View vs Looker LookML vs Oracle OBIEE

| Capability | Snowflake Semantic View | Looker LookML | Oracle OBIEE |
|---|---|---|---|
| Definition | Native SQL DDL | Proprietary LookML | Binary RPD Repository |
| AI-Native | Yes (powers Cortex Analyst) | No | No |
| Unstructured Data | Yes (pairs with Search) | No | No |
| Real-Time Pipeline | Dynamic Tables (1 min) | Batch PDTs | Batch ETL |
| Verified Queries | Yes — trust layer | No | No |
| Git-Friendly | Plain SQL | Complex | Binary — not possible |
| Licensing | Included | Separate license | Separate license |

#### The Key Insight

> **"The Semantic View holds the TRUE VALUE that all other BI and AI solutions consume. When you update a metric definition here, every consumer — the Agent, Snowflake Intelligence, the Streamlit app, any future BI tool — automatically gets the updated, consistent answer. No more conflicting dashboards. No more 'my number is different from your number.'"**

---

## Step 4: Cortex Agent + Snowflake Intelligence (15 min)

### 4.1 Create the Agent

📄 **File:** [`sql/06_create_agent.sql`](sql/06_create_agent.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/06_create_agent.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Copy-paste the contents of `sql/06_create_agent.sql` into a SQL Worksheet
2. Click **Run All**
</details>

The **LSC Research Agent** has 4 tools:

| Tool | Type | Purpose |
|---|---|---|
| `transplant_analyst` | cortex_analyst_text_to_sql | Structured data via Semantic View |
| `clinical_notes_search` | cortex_search | Unstructured clinical note search |
| `chart_generator` | data_to_chart | AI-generated visualizations |
| `research_search` | web_search | Latest GVHD research from the web |

#### How the Agent Works

1. **You ask a question** in natural language
2. **The agent reasons** about which tool(s) to use
3. **It executes** — maybe Analyst for data, then Search for evidence
4. **It synthesizes** a unified answer with data, citations, and recommendations

> **"This is what makes Snowflake unlike any BI tool. Looker can answer the WHAT. Snowflake Intelligence can tell you the WHO, WHAT, WHERE, WHEN, WHY, and HOW — and make RECOMMENDATIONS. Because it combines structured analytics with unstructured clinical intelligence."**

### 4.2 Connect to Snowflake Intelligence

📄 **File:** [`sql/07_snowflake_intelligence.sql`](sql/07_snowflake_intelligence.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/07_snowflake_intelligence.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Copy-paste the contents of `sql/07_snowflake_intelligence.sql` into a SQL Worksheet
2. Click **Run All**
</details>

Then connect the agent in the Snowsight UI:

1. Navigate to **AI & ML > Snowflake Intelligence** in Snowsight
2. Click **"New Analyst"** → **"Use an Agent"**
3. Select **`MARROWCO_DONOR_LAB.HOL.MARROWCO_RESEARCH_AGENT`**
4. Name it **"LSC Research Intelligence"**

> **Notice:** The verified queries from the Semantic View automatically appear as suggested questions.

#### Demo Flow in Snowflake Intelligence

Try these questions in order to showcase different capabilities:

1. **"What is the overall GVHD rate by donor type?"** → Structured data + chart
2. **"What do clinical notes say about severe skin GVHD treatment?"** → Unstructured search
3. **"Compare haploidentical outcomes with PTCy and find clinical evidence"** → Both tools combined
4. **"How does race/ethnicity affect outcomes?"** → Health equity (Donor for All)
5. **"Create a chart of transplant volume trends"** → Visualization
6. **"What are the top 3 recommendations for improving minority patient outcomes?"** → Recommendations

---

## Step 5: ML Model (10 min)

📄 **File:** [`sql/08_ml_model.sql`](sql/08_ml_model.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/08_ml_model.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Copy-paste the contents of `sql/08_ml_model.sql` into a SQL Worksheet
2. Click **Run All**
</details>

### 5.1 Train the GVHD Risk Model

Uses `SNOWFLAKE.ML.CLASSIFICATION` to predict severe GVHD (Grade III-IV).

**Features:** Patient age, sex, race, diagnosis category, donor type, HLA match, conditioning intensity, PTCy usage, SVI score

### 5.2 Evaluate

```sql
CALL GVHD_RISK_MODEL!SHOW_EVALUATION_METRICS();
CALL GVHD_RISK_MODEL!SHOW_FEATURE_IMPORTANCE();
```

### 5.3 Score Patients

The model generates predictions with probability scores, enabling risk stratification.

> **Key takeaway:** The model is trained WHERE the data lives — no data movement, no separate ML infrastructure. The model is automatically registered in the Snowflake Model Registry.

---

## Step 6: Apply Grants & Deploy Streamlit App (15 min)

### 6.1 Apply Grants

📄 **File:** [`sql/09_grants.sql`](sql/09_grants.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/09_grants.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Copy-paste the contents of `sql/09_grants.sql` into a SQL Worksheet
2. Click **Run All**
</details>

### 6.2 Deploy the Streamlit App

The **LSC: Cell Therapy Compass** is a production-grade Streamlit in Snowflake application.

<details>
<summary><strong>Option A: Snow CLI</strong></summary>

From the repo root directory:

```bash
snow streamlit deploy --replace -c DEMO \
  --project streamlit/ \
  --role MARROWCO_HOL_ROLE \
  --database MARROWCO_DONOR_LAB \
  --schema HOL
```

The app will be deployed and a URL will be printed. Open the URL to view the app.
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. In Snowsight: **Projects > Streamlit > + Streamlit App**
2. Set **Database** to `MARROWCO_DONOR_LAB`, **Schema** to `HOL`, **Warehouse** to `MARROWCO_HOL_WH`
3. Name the app `CELL_THERAPY_COMPASS`
4. Replace the default code with the contents of `streamlit/streamlit_app.py`
5. Create a `pages/` folder and upload all files from `streamlit/pages/`
6. Create a `utils/` folder and upload `__init__.py`, `navigation.py`, and `styles.py` from `streamlit/utils/`
7. Create an `assets/` folder and upload `AppBanner.png` from `streamlit/assets/`
8. Upload `environment.yml` from `streamlit/`
9. Click **Run**
</details>

### Application Pages

| Page | What It Shows |
|---|---|
| **Home** | Hero banner, mission context, platform overview |
| **Data Foundation** | Architecture diagram, Dynamic Tables pipeline, data preview |
| **Semantic Intelligence** | Semantic View deep-dive, Looker/OBIEE comparison, verified query explorer |
| **GVHD Forecasting** | ML results, risk distributions, survival analysis, health equity charts |
| **Research Agent** | Chat interface to the Cortex Agent |
| **Take Action** | AI-powered email generator with LSC branding and live data |

---

## Step 7: Take Action + Wrap-up (10 min)

### 7.1 Email Generation Demo

Navigate to the **Take Action** page in the Streamlit app:

1. Fill in recipient details
2. Select a focus area (e.g., "GVHD Outcome Summary")
3. Click **"Generate Email"**

The email is dynamically generated with:
- LSC logo in the header
- Live metrics from the Snowflake pipeline
- Data-driven subject line
- Professional HTML/CSS formatting
- Actionable recommendations

> **"This demonstrates how Snowflake enables ACTION directly from insight. It's not just a passive dashboard — it drives clinical communication and decision-making."**

### 7.2 Wrap-up

Recap what was built:

| Layer | Component | Replaces |
|---|---|---|
| **Data Pipeline** | Dynamic Tables | Informatica + Airflow + dbt |
| **Semantic Layer** | Semantic View | Looker LookML / Oracle RPD |
| **AI Analytics** | Cortex Agent | Manual dashboard navigation |
| **Intelligence UI** | Snowflake Intelligence | Looker Explores / OBIEE Answers |
| **ML/AI** | Snowflake ML + Cortex | External ML platforms |
| **Application** | Streamlit in Snowflake | Custom app development |
| **Action** | AI-generated email | Manual report creation |

**All of this — in a single platform, with no data movement, no additional licensing, and governed by the Semantic View.**

---

## Cleanup

To remove all lab artifacts, run the full teardown script:

📄 **File:** [`sql/10_teardown.sql`](sql/10_teardown.sql)

<details>
<summary><strong>Option A: Cortex Code / Snow CLI</strong></summary>

```bash
snow sql -c DEMO -f sql/10_teardown.sql
```
</details>

<details>
<summary><strong>Option B: Manual via Snowsight</strong></summary>

1. Copy-paste the contents of `sql/10_teardown.sql` into a SQL Worksheet
2. Click **Run All**
</details>

This drops all objects in the correct dependency order: Streamlit App, Agent, ML Model, Semantic View, Search Service, Dynamic Tables, Tables, Stage, Database, Warehouse, and Role.

**Quick cleanup** (if you just want the essentials):

```sql
USE ROLE ACCOUNTADMIN;
DROP DATABASE IF EXISTS MARROWCO_DONOR_LAB;
DROP WAREHOUSE IF EXISTS MARROWCO_HOL_WH;
DROP ROLE IF EXISTS MARROWCO_HOL_ROLE;
```

---

## Resources

- [Snowflake Semantic Views Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view)
- [Snowflake Dynamic Tables](https://docs.snowflake.com/en/user-guide/dynamic-tables-about)
- [Cortex Agents](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agent)
- [Snowflake Intelligence](https://docs.snowflake.com/en/user-guide/snowflake-intelligence)
- [Snowflake ML Classification](https://docs.snowflake.com/en/user-guide/ml-functions/classification)

---

**Presenter:** Braedon Hill, Sr. Solution Engineer — Snowflake

*This lab was built to demonstrate how Snowflake's AI Data Cloud can unify transplant outcome data, clinical intelligence, and predictive analytics into a single governed platform supporting the "Donor for All" mission.*

---

## Legal Disclaimer

This project is the independent work of **Braedon Hill** and does not represent, reflect, or imply endorsement by any organization, employer, or third party. The views and content expressed in this repository are solely those of the author.

**All data used in this project is entirely synthetic.** Synthetic datasets were generated using Snowflake's synthetic data generation capabilities (Cortex AI functions). Where real-world reference data was used for structure or schema design, it was obtained exclusively from publicly available sources. **No real patient data, proprietary datasets, or confidential information of any kind is included in this repository.**

This project is provided "as is" without warranty of any kind, express or implied. The author assumes no liability for any use or misuse of the materials contained herein. This project is intended solely for educational and demonstration purposes.


---

## Disclaimer

This project was created by Braedon Hill as a personal/educational/demonstration exercise.
It is **not** official Snowflake documentation or software and is **not** reviewed,
endorsed, or supported by Snowflake Inc.

Provided "AS IS" — see [DISCLAIMER.md](./DISCLAIMER.md) for full details.

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
