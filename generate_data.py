from pathlib import Path
from datetime import datetime, timedelta
import random
import pandas as pd

random.seed(42)
RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

branches = [
    {"branch_id": "BR001", "branch_name": "Central Branch", "city": "Bhubaneswar", "state": "Odisha"},
    {"branch_id": "BR002", "branch_name": "Park Street", "city": "Kolkata", "state": "West Bengal"},
    {"branch_id": "BR003", "branch_name": "Connaught Place", "city": "New Delhi", "state": "Delhi"},
]
pd.DataFrame(branches).to_csv(RAW / "branches.csv", index=False)

customers = []
for i in range(1, 101):
    customers.append({
        "customer_id": f"C{i:04d}", "full_name": f"Customer {i}",
        "email": f"customer{i}@example.com",
        "customer_segment": random.choice(["Retail", "Premium", "Business"]),
        "created_at": (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 700))).isoformat()
    })
pd.DataFrame(customers).to_csv(RAW / "customers.csv", index=False)

accounts = []
for i in range(1, 151):
    accounts.append({
        "account_id": f"A{i:05d}", "customer_id": f"C{random.randint(1, 100):04d}",
        "branch_id": random.choice(branches)["branch_id"],
        "account_type": random.choice(["Savings", "Current"]),
        "opened_at": (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 700))).date().isoformat(),
        "account_status": random.choice(["Active", "Active", "Active", "Dormant"])
    })
pd.DataFrame(accounts).to_csv(RAW / "accounts.csv", index=False)

transactions = []
start = datetime(2025, 1, 1, 8, 0, 0)
for i in range(1, 2001):
    timestamp = start + timedelta(minutes=random.randint(0, 60 * 24 * 180))
    amount = round(random.uniform(100, 8000), 2)
    if i % 137 == 0:
        amount = round(random.uniform(12000, 25000), 2)
    transactions.append({
        "transaction_id": f"T{i:07d}", "account_id": f"A{random.randint(1, 150):05d}",
        "transaction_ts": timestamp.isoformat(sep=" "), "amount": amount, "currency": "INR",
        "transaction_type": random.choice(["Debit", "Credit", "Transfer"]),
        "channel": random.choice(["ATM", "UPI", "Branch", "NetBanking", "POS"]),
        "merchant": random.choice(["Grocery", "Fuel", "Utilities", "Online", "Transfer"]),
        "status": random.choice(["SUCCESS", "SUCCESS", "SUCCESS", "PENDING", "FAILED"])
    })

# Intentionally invalid examples to exercise the quarantine logic.
transactions.extend([
    {"transaction_id": "TBAD001", "account_id": "A00001", "transaction_ts": "not-a-date",
     "amount": 500, "currency": "INR", "transaction_type": "Debit", "channel": "UPI",
     "merchant": "Test", "status": "SUCCESS"},
    {"transaction_id": "TBAD002", "account_id": "A99999", "transaction_ts": "2025-03-01 12:00:00",
     "amount": 900, "currency": "INR", "transaction_type": "Debit", "channel": "ATM",
     "merchant": "Test", "status": "SUCCESS"},
    {"transaction_id": "TBAD003", "account_id": "A00001", "transaction_ts": "2025-03-01 12:00:00",
     "amount": -50, "currency": "INR", "transaction_type": "Debit", "channel": "ATM",
     "merchant": "Test", "status": "SUCCESS"},
])
pd.DataFrame(transactions).to_csv(RAW / "transactions_001.csv", index=False)
print(f"Generated {len(customers)} customers, {len(accounts)} accounts, {len(transactions)} transactions.")
