import json
from datetime import datetime
import pandas as pd
from .config import RAW_DIR, PROCESSED_DIR, QUARANTINE_DIR, REPORTS_DIR, DB_TYPE
from .ingest import load_dimensions, load_transaction_files
from .transform import standardize_transactions, validate_transactions
from .quality import flag_anomalies
from .db import connect, initialize, insert_dimensions, get_existing_ids
from .load import load_transactions

def export_reports(conn):
    queries = {
        "daily_transaction_summary.csv": """SELECT substr(transaction_ts,1,10) AS txn_date,
            COUNT(*) AS txn_count, ROUND(SUM(amount),2) AS total_amount
            FROM transactions GROUP BY substr(transaction_ts,1,10) ORDER BY txn_date""",
        "channel_performance.csv": """SELECT channel, COUNT(*) AS txn_count,
            ROUND(SUM(amount),2) AS total_amount, SUM(is_anomaly) AS anomaly_count
            FROM transactions GROUP BY channel ORDER BY txn_count DESC""",
        "branch_performance.csv": """SELECT b.branch_name, b.city, COUNT(t.transaction_id) AS txn_count,
            ROUND(COALESCE(SUM(t.amount),0),2) AS total_amount
            FROM branches b LEFT JOIN accounts a ON a.branch_id=b.branch_id
            LEFT JOIN transactions t ON t.account_id=a.account_id
            GROUP BY b.branch_id,b.branch_name,b.city ORDER BY total_amount DESC""",
        "data_quality_summary.csv": """SELECT COUNT(*) AS loaded_rows,
            COALESCE(SUM(is_anomaly),0) AS anomaly_rows,
            COUNT(DISTINCT transaction_id) AS unique_transactions
            FROM transactions"""
    }
    for filename, query in queries.items():
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        columns = [item[0] for item in cur.description]
        pd.DataFrame(rows, columns=columns).to_csv(REPORTS_DIR / filename, index=False)
        cur.close()

def run():
    started = datetime.now()
    print("BankStream ETL started")
    dimensions = load_dimensions(RAW_DIR)
    conn = connect()
    try:
        initialize(conn)
        insert_dimensions(conn, dimensions)
        raw = load_transaction_files(RAW_DIR)
        if raw.empty:
            print("No transaction files found in data/raw.")
            return
        standardized = standardize_transactions(raw)
        existing_ids = get_existing_ids(conn)
        new_rows = standardized[~standardized["transaction_id"].isin(existing_ids)].copy()
        valid_account_ids = set(dimensions["accounts"]["account_id"].astype(str))
        accepted, rejected = validate_transactions(new_rows, valid_account_ids)

        if not rejected.empty:
            rejected.to_csv(QUARANTINE_DIR / f"rejected_{started:%Y%m%d_%H%M%S}.csv", index=False)
        flagged = flag_anomalies(accepted)
        if not flagged.empty:
            flagged.to_csv(PROCESSED_DIR / f"accepted_{started:%Y%m%d_%H%M%S}.csv", index=False)

        loaded = load_transactions(conn, flagged)
        export_reports(conn)
        summary = {
            "started_at": started.isoformat(timespec="seconds"),
            "finished_at": datetime.now().isoformat(timespec="seconds"),
            "source_rows": int(len(raw)),
            "new_rows": int(len(new_rows)),
            "loaded_rows_this_run": int(loaded),
            "rejected_rows_this_run": int(len(rejected)),
            "previously_loaded_rows_skipped": int(len(standardized) - len(new_rows)),
            "anomaly_flags_this_run": int(flagged["is_anomaly"].sum()) if not flagged.empty else 0
        }
        (REPORTS_DIR / "latest_run_summary.json").write_text(json.dumps(summary, indent=2))
        print(json.dumps(summary, indent=2))
    finally:
        conn.close()
