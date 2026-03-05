# Donor for All Data Lab: Forecasting GVHD with Snowflake Intelligence

A collaborative data lab built for the **The Life Saving Company (LSC)** to forecast Graft-versus-Host Disease (GVHD) outcomes using Snowflake's AI and data intelligence capabilities.

## Overview

This project leverages Snowflake Intelligence to analyze donor and transplant data, build predictive models for GVHD risk, and deliver actionable insights through an interactive Streamlit application.

## Project Structure

```
donor-for-all-data-lab/
├── setup/              # Snowflake SQL setup scripts (databases, schemas, tables, etc.)
├── streamlit/          # Streamlit application source code
├── scripts/            # Utility and validation scripts
├── sample_data/        # Sample datasets for development and testing
└── .streamlit/         # Streamlit configuration (secrets excluded via .gitignore)
```

## Getting Started

### Prerequisites

- Snowflake account with appropriate privileges
- Python 3.8+
- Streamlit

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/sfc-gh-bhill/customer-marrowco-donor-for-all-data-lab.git
   cd customer-marrowco-donor-for-all-data-lab
   ```

2. Copy the secrets template and fill in your Snowflake credentials:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

3. Run the setup SQL scripts in order against your Snowflake account:
   ```
   setup/01_setup_infrastructure.sql
   ```

4. Launch the Streamlit app:
   ```bash
   streamlit run streamlit/app.py
   ```

## Built With

- [Snowflake](https://www.snowflake.com/) - Data Cloud platform
- [Snowflake Cortex](https://docs.snowflake.com/en/user-guide/snowflake-cortex/overview) - AI/ML functions
- [Streamlit](https://streamlit.io/) - Interactive data applications

## Author

**Braedon Hill** - Sr. Solution Engineer, Snowflake

## License

This project is shared for collaboration with the LSC team. See the repository settings for access details.
