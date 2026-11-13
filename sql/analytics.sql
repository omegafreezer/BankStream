-- Run these queries in SQLite or adapt DATE() syntax for your SQL engine.
CREATE VIEW IF NOT EXISTS vw_daily_transaction_summary AS
SELECT substr(transaction_ts,1,10) AS transaction_date,
       COUNT(*) AS transaction_count, SUM(amount) AS total_amount,
       AVG(amount) AS average_amount
FROM transactions
WHERE status = 'SUCCESS'
GROUP BY substr(transaction_ts,1,10);

CREATE VIEW IF NOT EXISTS vw_customer_activity AS
SELECT c.customer_id, c.full_name, c.customer_segment,
       COUNT(t.transaction_id) AS transaction_count,
       COALESCE(SUM(t.amount),0) AS total_amount,
       MAX(t.transaction_ts) AS last_transaction_at
FROM customers c
LEFT JOIN accounts a ON a.customer_id=c.customer_id
LEFT JOIN transactions t ON t.account_id=a.account_id
GROUP BY c.customer_id,c.full_name,c.customer_segment;

CREATE VIEW IF NOT EXISTS vw_branch_performance AS
SELECT b.branch_id,b.branch_name,b.city,
       COUNT(t.transaction_id) AS transaction_count,
       COALESCE(SUM(t.amount),0) AS total_amount
FROM branches b
LEFT JOIN accounts a ON a.branch_id=b.branch_id
LEFT JOIN transactions t ON t.account_id=a.account_id
GROUP BY b.branch_id,b.branch_name,b.city;

CREATE VIEW IF NOT EXISTS vw_channel_performance AS
SELECT channel,COUNT(*) AS transaction_count,SUM(amount) AS total_amount,
       SUM(is_anomaly) AS flagged_count
FROM transactions GROUP BY channel;

CREATE VIEW IF NOT EXISTS vw_anomaly_review AS
SELECT transaction_id,account_id,transaction_ts,amount,channel,anomaly_reason
FROM transactions WHERE is_anomaly=1;
