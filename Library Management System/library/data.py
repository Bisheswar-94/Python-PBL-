"""In-memory lists of dictionaries with lightweight JSON persistence."""
import json
from pathlib import Path
DATA_FILE=Path(__file__).resolve().parent.parent/'library_data.json'

def load_library():
    """Load the list of book dictionaries, or start with an empty list."""
    if not DATA_FILE.exists(): return []
    try:
        data=json.loads(DATA_FILE.read_text(encoding='utf-8'))
        return data if isinstance(data,list) else []
    except (OSError,json.JSONDecodeError): return []

def save_library(books):
    """Save the complete list of book dictionaries."""
    DATA_FILE.write_text(json.dumps(books,indent=2),encoding='utf-8')
