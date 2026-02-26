import re

def load_wordlist(wordlist_path):
    with open(wordlist_path, "r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def find_timestamp_matches(transcription_result: dict, wordlist_path: str):
    words_to_match = load_wordlist(wordlist_path)
    matches = []

    for segment in transcription_result.get("segments", []):
        for word_info in segment.get("words", []):
            if "start" in word_info and "end" in word_info:
                spoken_word = word_info["word"]
                cleaned = re.sub(r"[^\w']", "", spoken_word).lower()

                if cleaned in words_to_match:
                    matches.append({
                        "start": word_info["start"],
                        "end": word_info["end"]
                    })

    return matches