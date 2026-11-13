-- SQLite-compatible logical schema; run_pipeline.py creates these tables automatically.
CREATE TABLE branches (
    branch_id TEXT PRIMARY KEY, branch_name TEXT, city TEXT, state TEXT
);
CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY, full_name TEXT, email TEXT,
    customer_segment TEXT, created_at TEXT
);
CREATE TABLE accounts (
    account_id TEXT PRIMARY KEY, customer_id TEXT, branch_id TEXT,
    account_type TEXT, opened_at TEXT, account_status TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(branch_id) REFERENCES branches(branch_id)
);
CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY, account_id TEXT, transaction_ts TEXT,
    amount REAL, currency TEXT, transaction_type TEXT, channel TEXT,
    merchant TEXT, status TEXT, is_anomaly INTEGER, anomaly_reason TEXT,
    source_file TEXT, loaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(account_id) REFERENCES accounts(account_id)
);
