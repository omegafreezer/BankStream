import pandas as pd
from .config import HIGH_VALUE_THRESHOLD, FREQUENCY_WINDOW_MINUTES, FREQUENCY_THRESHOLD

def flag_anomalies(frame):
    if frame.empty:
        out = frame.copy()
        out["is_anomaly"] = pd.Series(dtype=bool)
        out["anomaly_reason"] = pd.Series(dtype=str)
        return out

    out = frame.copy()
    out["is_anomaly"] = False
    out["anomaly_reason"] = ""
    high_value = out["amount"] >= HIGH_VALUE_THRESHOLD
    out.loc[high_value, "is_anomaly"] = True
    out.loc[high_value, "anomaly_reason"] = "high_value"

    for account_id, group in out.groupby("account_id"):
        ordered = group.sort_values("transaction_ts").set_index("transaction_ts")
        rolling_counts = ordered["transaction_id"].rolling(
            f"{FREQUENCY_WINDOW_MINUTES}min"
        ).count()
        frequent_times = rolling_counts[rolling_counts >= FREQUENCY_THRESHOLD].index
        mask = (out["account_id"] == account_id) & out["transaction_ts"].isin(frequent_times)
        out.loc[mask, "is_anomaly"] = True
        out.loc[mask, "anomaly_reason"] = out.loc[mask, "anomaly_reason"].apply(
            lambda value: value + ";high_frequency" if value else "high_frequency"
        )
    return out.sort_values("transaction_id").reset_index(drop=True)
