# BankStream — Banking Transaction Data Engineering Platform

A locally runnable portfolio project demonstrating batch data ingestion, incremental ETL, data cleaning, validation, rejected-record quarantine, relational loading, anomaly flagging, SQL analytics, and Power BI-ready reporting.

**Data disclaimer:** All generated records are synthetic. This is a learning/portfolio simulation, not a real bank system.

## 1. Run locally (SQLite; no database server needed)

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python generate_data.py
python run_pipeline.py
python -m unittest discover -s tests -v
```

Run `python run_pipeline.py` a second time. Previously loaded transaction IDs should be skipped, demonstrating idempotent incremental loading.

## MySQL option (optional)

The default SQLite configuration is easiest for a first run. To use MySQL:
1. Start Docker Desktop.
2. Run `docker compose up -d` from the project folder.
3. Copy `.env.example` to `.env`.
4. Set `DB_TYPE=mysql` and match the MySQL credentials in `.env` to `docker-compose.yml`.
5. Install dependencies with `pip install -r requirements.txt`.
6. Run `python generate_data.py` and `python run_pipeline.py`.

## 2. What the pipeline does

1. Reads branch, customer, account, and transaction CSV files.
2. Standardizes IDs, text fields, timestamps, and numeric amounts.
3. Validates required fields, positive amounts, timestamps, transaction types/statuses, and account references.
4. Writes invalid rows and rejection reasons to `data/quarantine/`.
5. Flags high-value and high-frequency transactions for review; flags are not fraud determinations.
6. Loads valid records into SQLite tables with primary/foreign keys.
7. Exports analytical CSVs into `reports/` for Power BI.

## 3. Data model

- `branches`: branch details
- `customers`: customer details and segment
- `accounts`: customer/branch relationship and account type
- `transactions`: transaction facts, status, channel, anomaly flag, source file, load timestamp

Relationships: one customer can own multiple accounts; one branch can service multiple accounts; one account can have multiple transactions.

## 4. Outputs

- `data/bankstream.db` — SQLite database (default; MySQL is optional)
- `data/processed/` — standardized, accepted transaction batch
- `data/quarantine/` — rejected records with reasons
- `reports/latest_run_summary.json` — run-level counts
- `reports/daily_transaction_summary.csv`
- `reports/channel_performance.csv`
- `reports/branch_performance.csv`
- `reports/data_quality_summary.csv`

## 5. Power BI dashboard

Import the four report CSVs from `reports/` into Power BI Desktop. Suggested visuals:
- KPI cards: loaded transaction count, transaction value, flagged anomalies, rejected rows
- Line chart: daily transaction count/value
- Bar chart: transaction value by channel
- Bar chart: transaction value by branch
- Table: channel, transaction count, value, anomaly count
- Data-quality summary card

See `reports/POWER_BI_GUIDE.md`.

## 6. SQL

`sql/schema.sql` contains the relational schema. `sql/analytics.sql` contains reusable analytical queries/views for a MySQL-compatible environment. The Python pipeline creates its SQLite schema automatically.

## 7. Interview preparation

Be able to explain:
- Why data validation occurs before loading
- Why invalid rows are quarantined rather than silently dropped
- How transaction IDs make repeat runs idempotent
- Difference between rejecting a bad record and flagging a suspicious one
- Primary/foreign keys and the relational model
- How SQL views and report extracts support analytics
- Limitations of batch processing versus streaming

## 8. Resume wording — only after you run and understand the project

**BankStream — Banking Transaction Data Engineering Platform | Python, Pandas, SQL, SQLite/MySQL, Power BI, Git**
- Built a batch ETL pipeline to ingest, standardize, validate, and incrementally load synthetic banking transaction data into a relational database.
- Implemented duplicate handling, data-quality checks, rejected-record quarantine, and configurable anomaly flags.
- Designed a relational schema and analytical SQL queries for transaction trends, customer activity, and branch/channel performance.
- Generated Power BI-ready reporting extracts for transaction volume, value, channel mix, and data-quality monitoring.

Do not claim MySQL, Power BI, cloud, or production-scale performance until you have actually configured, used, and can demonstrate those components.
