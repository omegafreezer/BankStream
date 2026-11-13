import sqlite3
from .config import DB_PATH, DB_TYPE, MYSQL_CONFIG

SQLITE_SCHEMA = [
    """CREATE TABLE IF NOT EXISTS branches (
        branch_id TEXT PRIMARY KEY, branch_name TEXT, city TEXT, state TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY, full_name TEXT, email TEXT,
        customer_segment TEXT, created_at TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS accounts (
        account_id TEXT PRIMARY KEY, customer_id TEXT, branch_id TEXT,
        account_type TEXT, opened_at TEXT, account_status TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY(branch_id) REFERENCES branches(branch_id)
    )""",
    """CREATE TABLE IF NOT EXISTS transactions (
        transaction_id TEXT PRIMARY KEY, account_id TEXT, transaction_ts TEXT,
        amount REAL, currency TEXT, transaction_type TEXT, channel TEXT,
        merchant TEXT, status TEXT, is_anomaly INTEGER, anomaly_reason TEXT,
        source_file TEXT, loaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(account_id) REFERENCES accounts(account_id)
    )"""
]

MYSQL_SCHEMA = [
    """CREATE TABLE IF NOT EXISTS branches (
        branch_id VARCHAR(20) PRIMARY KEY, branch_name VARCHAR(100), city VARCHAR(80), state VARCHAR(80)
    ) ENGINE=InnoDB""",
    """CREATE TABLE IF NOT EXISTS customers (
        customer_id VARCHAR(20) PRIMARY KEY, full_name VARCHAR(120), email VARCHAR(160),
        customer_segment VARCHAR(30), created_at VARCHAR(40)
    ) ENGINE=InnoDB""",
    """CREATE TABLE IF NOT EXISTS accounts (
        account_id VARCHAR(20) PRIMARY KEY, customer_id VARCHAR(20), branch_id VARCHAR(20),
        account_type VARCHAR(30), opened_at VARCHAR(40), account_status VARCHAR(30),
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY(branch_id) REFERENCES branches(branch_id)
    ) ENGINE=InnoDB""",
    """CREATE TABLE IF NOT EXISTS transactions (
        transaction_id VARCHAR(30) PRIMARY KEY, account_id VARCHAR(20), transaction_ts DATETIME,
        amount DECIMAL(14,2), currency VARCHAR(5), transaction_type VARCHAR(20),
        channel VARCHAR(30), merchant VARCHAR(80), status VARCHAR(20),
        is_anomaly TINYINT, anomaly_reason VARCHAR(200), source_file VARCHAR(120),
        loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(account_id) REFERENCES accounts(account_id)
    ) ENGINE=InnoDB"""
]

def connect():
    if DB_TYPE == "mysql":
        try:
            import mysql.connector
        except ImportError as exc:
            raise RuntimeError("Install mysql-connector-python to use DB_TYPE=mysql.") from exc
        return mysql.connector.connect(**MYSQL_CONFIG)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize(conn):
    statements = MYSQL_SCHEMA if DB_TYPE == "mysql" else SQLITE_SCHEMA
    cur = conn.cursor()
    for statement in statements:
        cur.execute(statement)
    conn.commit()
    cur.close()

def get_existing_ids(conn):
    cur = conn.cursor()
    cur.execute("SELECT transaction_id FROM transactions")
    ids = {row[0] for row in cur.fetchall()}
    cur.close()
    return ids

def insert_dimensions(conn, dimensions):
    cur = conn.cursor()
    for table, frame in dimensions.items():
        if frame.empty:
            continue
        columns = list(frame.columns)
        placeholder = "%s" if DB_TYPE == "mysql" else "?"
        prefix = "INSERT IGNORE" if DB_TYPE == "mysql" else "INSERT OR IGNORE"
        sql = f" {prefix} INTO {table} ({','.join(columns)}) VALUES ({','.join([placeholder] * len(columns))})"
        rows = [tuple(row) for row in frame.itertuples(index=False, name=None)]
        cur.executemany(sql.strip(), rows)
    conn.commit()
    cur.close()
