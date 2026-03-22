from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel
from uuid import uuid4
from utils.store_filter_words import (
    DEFAULT_SET_ID,
    load_filter_sets,
    save_filter_sets,
    get_enabled_words,
)

router = APIRouter()

class WordRequest(BaseModel):
    word: str

class SetRequest(BaseModel):
    name: str


class ToggleRequest(BaseModel):
    enabled: bool


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