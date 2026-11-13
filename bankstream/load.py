from .config import DB_TYPE

def load_transactions(conn, frame):
    if frame.empty:
        return 0
    columns = ["transaction_id", "account_id", "transaction_ts", "amount", "currency",
               "transaction_type", "channel", "merchant", "status", "is_anomaly",
               "anomaly_reason", "source_file"]
    placeholder = "%s" if DB_TYPE == "mysql" else "?"
    prefix = "INSERT IGNORE" if DB_TYPE == "mysql" else "INSERT OR IGNORE"
    sql = f" {prefix} INTO transactions ({','.join(columns)}) VALUES ({','.join([placeholder] * len(columns))})"
    rows = []
    for _, row in frame.iterrows():
        rows.append((
            row["transaction_id"], row["account_id"],
            row["transaction_ts"].strftime("%Y-%m-%d %H:%M:%S"),
            float(row["amount"]), row["currency"], row["transaction_type"],
            row["channel"], row.get("merchant", ""), row["status"],
            int(bool(row["is_anomaly"])), row["anomaly_reason"], row.get("source_file", "")
        ))
    cur = conn.cursor()
    cur.executemany(sql.strip(), rows)
    conn.commit()
    cur.close()
    return len(rows)
