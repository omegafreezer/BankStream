# BankStream – Banking Transaction Data Engineering Platform

A Python-based data engineering project that processes banking transaction data through an ETL pipeline, performs data quality checks, and identifies unusual transaction patterns.

## Overview

BankStream is designed to demonstrate how structured banking data can be collected, cleaned, transformed, validated, and stored efficiently.

The project processes customer, account, and transaction records from CSV files. It uses Python and Pandas for data processing, SQL for database operations, and an incremental loading approach to prevent duplicate transaction records.

It also includes data validation and rule-based anomaly detection to improve data reliability and identify potentially unusual transactions.

## Key Features

- **Data Ingestion:** Reads customer, account, and transaction records from structured CSV files.
- **ETL Pipeline:** Performs data extraction, cleaning, transformation, and loading using Python and Pandas.
- **Incremental Loading:** Processes new transactions while preventing duplicate records.
- **Data Quality Checks:** Identifies missing values, invalid records, duplicates, and data inconsistencies.
- **Anomaly Detection:** Flags unusual transactions based on high-value and high-frequency transaction patterns.
- **Relational Data Modeling:** Organizes banking data into structured relational tables.
- **SQL Analytics:** Provides reusable SQL queries for transaction analysis and reporting.
- **Execution Reports:** Tracks processed records, rejected records, and detected anomalies.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Database | SQLite, MySQL (optional configuration) |
| Query Language | SQL |
| Data Pipeline | ETL, Incremental Loading |
| Data Quality | Validation, Duplicate Detection |
| Version Control | Git, GitHub |

## Project Architecture

```text
              Banking CSV Data
                     |
                     v
              Data Ingestion
                     |
                     v
             Data Transformation
             (Python + Pandas)
                     |
                     v
              Data Validation
                     |
              +------+------+
              |             |
              v             v
         Valid Records   Rejected Records
              |
              v
        Incremental Loading
              |
              v
         Relational Database
              |
              v
          SQL Analytics
              |
              v
       Anomaly Detection
              |
              v
        Execution Reports
```

## Project Structure

```text
BankStream/
│
├── bankstream/
│   ├── config.py
│   ├── ingest.py
│   ├── transform.py
│   ├── quality.py
│   ├── db.py
│   ├── load.py
│   └── pipeline.py
│
├── data/
│   └── raw/
│
├── reports/
│   └── POWER_BI_GUIDE.md
│
├── sql/
│   ├── schema.sql
│   └── analytics.sql
│
├── tests/
│   └── test_transform.py
│
├── generate_data.py
├── run_pipeline.py
├── requirements.txt
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/omegafreezer/BankStream.git

cd BankStream
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
py -m venv venv

.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv venv

source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Generate Sample Banking Data

```bash
python generate_data.py
```

This generates synthetic customer, account, and transaction datasets for pipeline execution.

### 5. Execute the ETL Pipeline

```bash
python run_pipeline.py
```

The pipeline performs ingestion, transformation, data validation, database loading, and anomaly detection.

## Database Support

BankStream uses SQLite as its default database configuration, allowing the pipeline to run locally without requiring a separate database server.

MySQL support is also included as an optional configuration using the provided database connection settings and Docker Compose setup.

## SQL Analytics

The project includes reusable SQL queries for exploring banking transaction data, including:

- Transaction volume and value analysis.
- Customer and account activity.
- Transaction trends.
- Identification of unusual transaction patterns.
- Data quality and pipeline monitoring.

Refer to the `sql/analytics.sql` file for the available analytical queries.

## Sample Data

The project uses synthetic banking datasets generated specifically for development and testing.

No real customer information, financial records, or sensitive banking data is used.

## Future Improvements

- Integrate a fully configured MySQL database.
- Build interactive Power BI dashboards for transaction analysis.
- Introduce more advanced anomaly detection techniques.
- Implement automated pipeline scheduling.
- Extend the pipeline with cloud-based data storage and processing.

## Learning Outcomes

Through this project, I explored practical data engineering concepts, including ETL pipeline development, incremental data processing, relational database design, SQL analytics, data validation, and transaction anomaly detection.

## Author

**Saksham Singh**

- GitHub: [@omegafreezer](https://github.com/omegafreezer)
- Project Repository: [BankStream](https://github.com/omegafreezer/BankStream)
