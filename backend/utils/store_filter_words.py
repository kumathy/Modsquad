import json
import os
from typing import List

DATA_DIR = os.getenv("DATA_DIR", "data")
WORDS_FILE = os.path.join(DATA_DIR, "filtered_words.json")
DEFAULT_SET_ID = "default"

DEFAULT_FILTER_SETS = [
    {
        "id": "common-profanity",
        "name": "Common Profanity",
        "enabled": True,
        "isDefault": True,
        "words": [
            "ass", "asshole", "arsehole", "bastard", "bitch", "bloody",
            "bollocks", "bullshit", "cock", "crap", "cunt", "damn",
            "dick", "dingleberry", "dogshit", "fuck", "fucking",
            "fucker", "fuckhead", "fucktard", "fuckwit", "goddamn",
            "hell", "horseshit", "jackass", "motherfucker", "piss",
            "pissed", "prick", "pussy", "shit", "shitty", "shithead",
            "slut", "son of a bitch", "tits", "tosser", "twat",
            "wanker", "whore",
        ],
    },
    {
        "id": "slurs-hate-speech",
        "name": "Slurs & Hate Speech",
        "enabled": True,
        "isDefault": True,
        "words": [
            "beaner", "chink", "coon", "cracker", "darkie", "dyke",
            "fag", "faggot", "gook", "gringo", "hajji", "honkey",
            "jap", "jigaboo", "kike", "kraut", "lesbo", "negro",
            "nigga", "nigger", "paki", "raghead", "retard", "spastic",
            "spic", "towelhead", "tranny", "wetback", "wigger",
            "zipperhead",
        ],
    },
]

DEFAULT_SET_IDS = {s["id"] for s in DEFAULT_FILTER_SETS}


def get_default_words(set_id: str) -> List[str]:
    for s in DEFAULT_FILTER_SETS:
        if s["id"] == set_id:
            return list(s["words"])
    return []


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _normalize_set(raw_set: dict, fallback_id: str) -> dict:
    set_id = str(raw_set.get("id") or fallback_id)
    name = str(raw_set.get("name") or "New Set").strip() or "New Set"
    enabled = bool(raw_set.get("enabled", True))
    is_default = set_id in DEFAULT_SET_IDS
    words = [str(w).strip().lower() for w in raw_set.get("words", []) if str(w).strip()]
    unique_words = list(dict.fromkeys(words))
    result = {
        "id": set_id,
        "name": name,
        "enabled": enabled,
        "words": unique_words,
    }
    if is_default:
        result["isDefault"] = True
    return result


def load_filter_sets() -> List[dict]:
    import copy
    ensure_data_dir()
    if not os.path.exists(WORDS_FILE):
        defaults = copy.deepcopy(DEFAULT_FILTER_SETS)
        save_filter_sets(defaults)
        return defaults

    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            normalized_sets = []

            # Backward compatibility: old format stored a plain word list.
            if data and all(isinstance(item, str) for item in data):
                words = [str(w).strip().lower() for w in data if str(w).strip()]
                unique_words = list(dict.fromkeys(words))
                normalized_sets = [
                    {
                        "id": DEFAULT_SET_ID,
                        "name": "Default",
                        "enabled": True,
                        "words": unique_words,
                    }
                ]
            else:
                for idx, item in enumerate(data):
                    if not isinstance(item, dict):
                        continue
                    normalized_sets.append(_normalize_set(item, f"set-{idx + 1}"))

            # Ensure default sets are present
            existing_ids = {s["id"] for s in normalized_sets}
            missing_defaults = [
                copy.deepcopy(d) for d in DEFAULT_FILTER_SETS
                if d["id"] not in existing_ids
            ]
            if missing_defaults:
                normalized_sets = missing_defaults + normalized_sets
                save_filter_sets(normalized_sets)
            return normalized_sets

    except Exception:
        pass

    return copy.deepcopy(DEFAULT_FILTER_SETS)


def save_filter_sets(filter_sets: List[dict]) -> None:
    ensure_data_dir()
    normalized_sets = []
    for idx, item in enumerate(filter_sets):
        if not isinstance(item, dict):
            continue
        normalized_sets.append(_normalize_set(item, f"set-{idx + 1}"))

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