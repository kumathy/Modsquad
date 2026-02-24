from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# todo: use the filtered_words for moderation in transcribed video
filtered_words = []

class WordRequest(BaseModel):
    word: str

@router.post("/add-word")
def add_word(data: WordRequest):
    word = data.word.strip().lower()
    if word not in filtered_words:
        filtered_words.append(word)

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