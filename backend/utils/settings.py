import json
import os

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel
from uuid import uuid4
from utils.store_filter_words import (
    DEFAULT_SET_ID,
    DEFAULT_SET_IDS,
    load_filter_sets,
    save_filter_sets,
    get_enabled_words,
    get_default_words,
)

router = APIRouter()

DATA_DIR = os.getenv("DATA_DIR", "data")
AUDIO_SETTINGS_FILE = os.path.join(DATA_DIR, "audio_settings.json")


def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _normalize_buffer_seconds(value: float | int | str | None) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = 0.0

    if parsed < 0:
        parsed = 0.0
    if parsed > 5:
        parsed = 5.0

    return round(parsed, 3)


def load_audio_processing_settings() -> dict:
    _ensure_data_dir()

    if not os.path.exists(AUDIO_SETTINGS_FILE):
        return {"buffer_seconds": 0.0}

    try:
        with open(AUDIO_SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {"buffer_seconds": 0.0}
        return {
            "buffer_seconds": _normalize_buffer_seconds(data.get("buffer_seconds", 0.0))
        }
    except Exception:
        return {"buffer_seconds": 0.0}


def save_audio_processing_settings(buffer_seconds: float) -> dict:
    _ensure_data_dir()
    normalized = {"buffer_seconds": _normalize_buffer_seconds(buffer_seconds)}
    with open(AUDIO_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)
    return normalized


def get_audio_buffer_seconds() -> float:
    settings = load_audio_processing_settings()
    return settings["buffer_seconds"]

class WordRequest(BaseModel):
    word: str

class SetRequest(BaseModel):
    name: str


class ToggleRequest(BaseModel):
    enabled: bool


class AudioProcessingSettingsRequest(BaseModel):
    buffer_seconds: float


def _find_filter_set(filter_sets: list[dict], set_id: str) -> dict:
    target_set = next((s for s in filter_sets if s.get("id") == set_id), None)
    if target_set is None:
        raise HTTPException(status_code=404, detail="Filter set not found")
    return target_set


@router.get("/filter-sets")
def get_filter_sets():
    return {"filter_sets": load_filter_sets()}


@router.post("/filter-sets")
def create_filter_set(data: SetRequest):
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Set name is required")

    filter_sets = load_filter_sets()
    filter_sets.append(
        {
            "id": str(uuid4()),
            "name": name,
            "enabled": True,
            "words": [],
        }
    )
    save_filter_sets(filter_sets)
    return {"success": True, "filter_sets": filter_sets}


@router.post("/filter-sets/{set_id}/toggle")
def toggle_filter_set(set_id: str, data: ToggleRequest):
    filter_sets = load_filter_sets()
    target_set = _find_filter_set(filter_sets, set_id)
    target_set["enabled"] = bool(data.enabled)
    save_filter_sets(filter_sets)
    return {"success": True, "filter_sets": filter_sets}


@router.delete("/filter-sets/{set_id}")
def delete_filter_set(set_id: str):
    if set_id in DEFAULT_SET_IDS:
        raise HTTPException(status_code=400, detail="Cannot delete a default filter set")

    filter_sets = load_filter_sets()
    _find_filter_set(filter_sets, set_id)

    remaining_sets = [s for s in filter_sets if s.get("id") != set_id]
    save_filter_sets(remaining_sets)
    return {"success": True, "filter_sets": remaining_sets}


@router.post("/filter-sets/{set_id}/reset")
def reset_filter_set(set_id: str):
    if set_id not in DEFAULT_SET_IDS:
        raise HTTPException(status_code=400, detail="Only default filter sets can be reset")

    filter_sets = load_filter_sets()
    target_set = _find_filter_set(filter_sets, set_id)
    target_set["words"] = get_default_words(set_id)
    save_filter_sets(filter_sets)
    return {"success": True, "filter_sets": filter_sets}


@router.post("/filter-sets/{set_id}/add-word")
def add_word_to_set(set_id: str, data: WordRequest):
    word = data.word.strip().lower()
    if not word:
        raise HTTPException(status_code=400, detail="Word is required")

    filter_sets = load_filter_sets()
    target_set = _find_filter_set(filter_sets, set_id)
    words = target_set.get("words", [])
    if word not in words:
        words.append(word)
        target_set["words"] = words
        save_filter_sets(filter_sets)

    return {"success": True, "filter_sets": filter_sets}


@router.post("/filter-sets/{set_id}/remove-word")
def remove_word_from_set(set_id: str, data: WordRequest):
    word = data.word.strip().lower()
    filter_sets = load_filter_sets()
    target_set = _find_filter_set(filter_sets, set_id)
    words = target_set.get("words", [])

    if word in words:
        words.remove(word)
        target_set["words"] = words
        save_filter_sets(filter_sets)

    return {"success": True, "filter_sets": filter_sets}


@router.get("/audio-processing")
def get_audio_processing_settings_endpoint():
    return load_audio_processing_settings()


@router.post("/audio-processing")
def update_audio_processing_settings_endpoint(data: AudioProcessingSettingsRequest):
    if data.buffer_seconds < 0:
        raise HTTPException(status_code=400, detail="buffer_seconds must be >= 0")

    return {
        "success": True,
        **save_audio_processing_settings(data.buffer_seconds),
    }


# Backward-compatible endpoints
@router.post("/add-word")
def add_word(data: WordRequest):
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

    word = data.word.strip().lower()
    if word and word not in default_set["words"]:
        default_set["words"].append(word)
        save_filter_sets(filter_sets)

    return {"success": True, "words": get_enabled_words(filter_sets)}


@router.get("/words")
def get_words():
    return {"words": get_enabled_words()}

@router.post("/remove-word")
def remove_word(data: WordRequest):
    filter_sets = load_filter_sets()
    default_set = next((s for s in filter_sets if s.get("id") == DEFAULT_SET_ID), None)
    if default_set is None:
        return {"success": True, "words": get_enabled_words(filter_sets)}

    word = data.word.strip().lower()
    if word in default_set["words"]:
        default_set["words"].remove(word)
        save_filter_sets(filter_sets)

    return {"success": True, "words": get_enabled_words(filter_sets)}