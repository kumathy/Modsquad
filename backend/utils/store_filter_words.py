import json
import os
from typing import List

DATA_DIR = os.getenv("DATA_DIR", "data")
WORDS_FILE = os.path.join(DATA_DIR, "filtered_words.json")
DEFAULT_SET_ID = "default"


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _normalize_set(raw_set: dict, fallback_id: str) -> dict:
    set_id = str(raw_set.get("id") or fallback_id)
    name = str(raw_set.get("name") or "New Set").strip() or "New Set"
    enabled = bool(raw_set.get("enabled", True))
    words = [str(w).strip().lower() for w in raw_set.get("words", []) if str(w).strip()]
    unique_words = list(dict.fromkeys(words))
    return {
        "id": set_id,
        "name": name,
        "enabled": enabled,
        "words": unique_words,
    }


def load_filter_sets() -> List[dict]:
    ensure_data_dir()
    if not os.path.exists(WORDS_FILE):
        return [
            {
                "id": DEFAULT_SET_ID,
                "name": "Default",
                "enabled": True,
                "words": [],
            }
        ]

    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            # Backward compatibility: old format stored a plain word list.
            if all(isinstance(item, str) for item in data):
                words = [str(w).strip().lower() for w in data if str(w).strip()]
                unique_words = list(dict.fromkeys(words))
                return [
                    {
                        "id": DEFAULT_SET_ID,
                        "name": "Default",
                        "enabled": True,
                        "words": unique_words,
                    }
                ]

            normalized_sets = []
            for idx, item in enumerate(data):
                if not isinstance(item, dict):
                    continue
                normalized_sets.append(_normalize_set(item, f"set-{idx + 1}"))

            if normalized_sets:
                return normalized_sets

    except Exception:
        pass

    return [
        {
            "id": DEFAULT_SET_ID,
            "name": "Default",
            "enabled": True,
            "words": [],
        }
    ]


def save_filter_sets(filter_sets: List[dict]) -> None:
    ensure_data_dir()
    normalized_sets = []
    for idx, item in enumerate(filter_sets):
        if not isinstance(item, dict):
            continue
        normalized_sets.append(_normalize_set(item, f"set-{idx + 1}"))

    if not normalized_sets:
        normalized_sets = [
            {
                "id": DEFAULT_SET_ID,
                "name": "Default",
                "enabled": True,
                "words": [],
            }
        ]

    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized_sets, f, ensure_ascii=False, indent=2)


def get_enabled_words(filter_sets: List[dict] | None = None) -> List[str]:
    sets = filter_sets if filter_sets is not None else load_filter_sets()
    words = []
    for filter_set in sets:
        if filter_set.get("enabled", True):
            words.extend(filter_set.get("words", []))
    return list(dict.fromkeys([w.strip().lower() for w in words if isinstance(w, str) and w.strip()]))


def load_words() -> List[str]:
    return get_enabled_words()


def save_words(words: List[str]) -> None:
    # Backward-compatible helper: update default set words.
    filter_sets = load_filter_sets()
    default_set = next((s for s in filter_sets if s.get("id") == DEFAULT_SET_ID), None)
    if default_set is None:
        default_set = {
            "id": DEFAULT_SET_ID,
            "name": "Default",
            "enabled": True,
            "words": [],
        }
        filter_sets.insert(0, default_set)

    default_set["words"] = list(dict.fromkeys([w.strip().lower() for w in words if isinstance(w, str) and w.strip()]))
    save_filter_sets(filter_sets)