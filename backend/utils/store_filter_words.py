import json
import os
from typing import List

DATA_DIR = os.getenv("DATA_DIR", "data")
WORDS_FILE = os.path.join(DATA_DIR, "filtered_words.json")


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def load_words() -> List[str]:
    ensure_data_dir()
    if not os.path.exists(WORDS_FILE):
        return []
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            print(f"[StoreFilterWords] Loaded filtered words: {data}")
            return [str(w).strip().lower() for w in data if str(w).strip()]
        return []
    except Exception:
        return []


def save_words(words: List[str]) -> None:
    ensure_data_dir()
    # keep unique + stable order
    unique = list(dict.fromkeys([w.strip().lower() for w in words if w.strip()]))
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)