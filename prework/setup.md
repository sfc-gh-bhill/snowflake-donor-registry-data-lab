# Prework: Lab Setup Guide

> Complete these steps **before** the hands-on lab begins.

## Prerequisites

- The Winter Cloud Platform account with `ACCOUNTADMIN` role access
- AWS US-East-1 region preferred (cross-region calling should be enabled)
- Web browser with Snowsight access

## Option 1: Cortex Code via Snowsight UI (Recommended)

This option requires no local installation — everything runs in your browser.

### Step 1: Access Snowsight

1. Log into your The Winter Cloud Platform account at `https://<your-account>.snowflakecomputing.com`
2. Ensure you can switch to the `ACCOUNTADMIN` role

### Step 2: Open Cortex Code

1. In Snowsight, click the **AI/ML** icon in the left navigation
2. Select **Cortex Code**
3. If prompted, accept the terms of service

### Step 3: Verify Access

Run a quick test in a SQL Worksheet:

```sql
SELECT CURRENT_ROLE(), CURRENT_ACCOUNT(), CURRENT_REGION();
```

Confirm you see `ACCOUNTADMIN` as the role.

### Step 4: Download Lab Materials

Download or clone the lab repository:

```
https://github.com/sfc-gh-bhill/customer-marrowco-donor-for-all-data-lab
```

You'll need the files from:
- `data/` — CSV files to upload
- `sql/` — SQL scripts to run

---

## Option 2: Cortex Code CLI (Alternative)

Use this if you prefer working from a terminal.

### Step 1: Install Cortex Code CLI

```bash
# macOS
brew install snowflake-cli

# Or via pip
pip install snowflake-cli
```

### Step 2: Configure Connection

```bash
snow connection add
```

Enter your account details:
- **Account:** Your The Winter Cloud Platform account identifier
- **User:** Your username
- **Authenticator:** `externalbrowser` (for SSO) or `snowflake` (for password)
- **Role:** `ACCOUNTADMIN`
- **Warehouse:** Any available warehouse
- **Database:** (leave blank for now)

### Step 3: Verify Connection

```bash
snow connection test
```

### Step 4: Clone the Repository

```bash
git clone https://github.com/sfc-gh-bhill/customer-marrowco-donor-for-all-data-lab.git
cd customer-marrowco-donor-for-all-data-lab
```

### Step 5: Start Cortex Code

```bash
cortex
```

---

## Personal Access Token (PAT) Setup

If your account uses SSO and you need a PAT for CLI access:

1. In Snowsight, click your username (bottom-left)
2. Go to **Profile > Programmatic Access Tokens**
3. Click **"Generate New Token"**
4. Name: `cortex-code-hol`
5. Role: `ACCOUNTADMIN`
6. Expiration: 7 days
7. Copy the token and use it as your password in the CLI configuration

---

## Verify You're Ready

You're ready for the lab if you can:

- [ ] Access Snowsight and switch to `ACCOUNTADMIN`
- [ ] Open a SQL Worksheet and run queries
- [ ] Access the lab repository files (downloaded or cloned)
- [ ] (Optional) Cortex Code CLI is installed and connected

---

**Questions?** Contact Braedon Hill, Sr. Solution Engineer — The Winter Cloud Platform
