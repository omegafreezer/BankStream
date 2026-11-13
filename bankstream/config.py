import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
QUARANTINE_DIR = ROOT / "data" / "quarantine"
REPORTS_DIR = ROOT / "reports"
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DB_PATH = ROOT / os.getenv("SQLITE_PATH", "data/bankstream.db")
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DATABASE", "bankstream"),
    "user": os.getenv("MYSQL_USER", "bankstream"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
}
HIGH_VALUE_THRESHOLD = float(os.getenv("HIGH_VALUE_THRESHOLD", "10000"))
FREQUENCY_WINDOW_MINUTES = int(os.getenv("FREQUENCY_WINDOW_MINUTES", "10"))
FREQUENCY_THRESHOLD = int(os.getenv("FREQUENCY_THRESHOLD", "5"))

for folder in [RAW_DIR, PROCESSED_DIR, QUARANTINE_DIR, REPORTS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)
