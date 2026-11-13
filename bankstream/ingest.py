import pandas as pd

def read_csv(path):
    return pd.read_csv(path, dtype=str).fillna("")

def load_dimensions(raw_dir):
    return {
        "branches": read_csv(raw_dir / "branches.csv"),
        "customers": read_csv(raw_dir / "customers.csv"),
        "accounts": read_csv(raw_dir / "accounts.csv"),
    }

def load_transaction_files(raw_dir):
    frames = []
    for path in sorted(raw_dir.glob("transactions_*.csv")):
        frame = read_csv(path)
        frame["source_file"] = path.name
        frames.append(frame)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
