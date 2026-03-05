from fastapi import APIRouter
from pydantic import BaseModel
from utils.store_filter_words import load_words, save_words

router = APIRouter()

# todo: use the filtered_words for moderation in transcribed video
filtered_words = load_words()

class WordRequest(BaseModel):
    word: str

@router.post("/add-word")
def add_word(data: WordRequest):
    word = data.word.strip().lower()
    if word not in filtered_words:
        filtered_words.append(word)
        save_words(filtered_words)

    print(f"[Settings] Current filtered words: ", filtered_words)
    return {
        "success": True,
        "words": filtered_words
    }


@router.get("/words")
def get_words():
    return {
        "words": filtered_words
    }

@router.post("/remove-word")
def remove_word(data: WordRequest):
    word = data.word.strip().lower()

    if word in filtered_words:
        filtered_words.remove(word)
        save_words(filtered_words)

    print("[Settings] Current filtered words:", filtered_words)

    return {
        "success": True,
        "words": filtered_words
    }