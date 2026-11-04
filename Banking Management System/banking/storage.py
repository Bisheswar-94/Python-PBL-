"""Simple JSON persistence helpers used by the banking packages."""
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "bank_data.json"

def load_data():
    """Return saved data, creating an empty data structure when needed."""
    if not DATA_FILE.exists():
        return {"accounts": [], "transactions": [], "next_account": 1001, "next_transaction": 1}
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        data.setdefault("accounts", []); data.setdefault("transactions", [])
        data.setdefault("next_account", 1001); data.setdefault("next_transaction", 1)
        return data
    except (OSError, json.JSONDecodeError):
        return {"accounts": [], "transactions": [], "next_account": 1001, "next_transaction": 1}

def save_data(data):
    """Write all banking records to the local JSON file."""
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
