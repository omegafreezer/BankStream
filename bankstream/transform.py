import pandas as pd

REQUIRED = ["transaction_id", "account_id", "transaction_ts", "amount",
            "currency", "transaction_type", "channel", "status"]
VALID_TYPES = {"Debit", "Credit", "Transfer"}
VALID_STATUSES = {"SUCCESS", "PENDING", "FAILED"}

def standardize_transactions(frame):
    out = frame.copy()
    if out.empty:
        return out
    for col in out.columns:
        if out[col].dtype == "object":
            out[col] = out[col].astype(str).str.strip()
    out["transaction_id"] = out["transaction_id"].str.upper()
    out["account_id"] = out["account_id"].str.upper()
    out["amount"] = pd.to_numeric(out["amount"], errors="coerce")
    out["transaction_ts"] = pd.to_datetime(out["transaction_ts"], errors="coerce")
    out["currency"] = out["currency"].str.upper()
    out["transaction_type"] = out["transaction_type"].str.title()
    out["status"] = out["status"].str.upper()
    return out

def validate_transactions(frame, valid_account_ids):
    accepted, rejected = [], []
    for _, row in frame.iterrows():
        reasons = []
        for col in REQUIRED:
            if col not in row or pd.isna(row[col]) or str(row[col]).strip() == "":
                reasons.append("missing_" + col)
        if pd.isna(row.get("amount")):
            reasons.append("invalid_amount")
        elif float(row["amount"]) <= 0:
            reasons.append("amount_must_be_positive")
        if pd.isna(row.get("transaction_ts")):
            reasons.append("invalid_transaction_timestamp")
        if row.get("transaction_type") not in VALID_TYPES:
            reasons.append("invalid_transaction_type")
        if row.get("status") not in VALID_STATUSES:
            reasons.append("invalid_status")
        if row.get("account_id") not in valid_account_ids:
            reasons.append("unknown_account_id")
        record = row.to_dict()
        if reasons:
            record["rejection_reason"] = ";".join(sorted(set(reasons)))
            rejected.append(record)
        else:
            accepted.append(record)
    return pd.DataFrame(accepted), pd.DataFrame(rejected)
