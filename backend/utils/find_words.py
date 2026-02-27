import re


def find_word_matches(plaintext, wordlist):
    with open(wordlist, 'r', encoding='utf-8') as f:
        words = {re.escape(line.strip()) for line in f if line.strip()}
    if not words:
        return []
    pattern = r'\b(' + '|'.join(words) + r')\b'
    regex = re.compile(pattern)
    """
    with open(plaintext, 'r', encoding='utf-8') as f:
        text = f.read()
    """
    matches = []
    timestamps=[]
    for match in regex.finditer(plaintext):
        word = match.group(1)
        start = match.start()
        end = match.end()
        matches.append((word, start, end))
        timestamps.append((start, end))
    print (timestamps)
    return matches, timestamps

def updated_find_word_matches(text, wordList):
    with open(wordList, 'r', encoding='utf-8') as f:
        words = {line.strip().lower() for line in f if line.strip()}

    if not words:
        return [], []

    matches = []
    timestamps = []

    for start, end, word in text:
        print(word)
        clean_word = word.lower()
        print (clean_word)
        if clean_word in words:
            matches.append((clean_word, start, end))
            timestamps.append((start, end))

    return matches, timestamps
if __name__ == "__main__":
    plaintext_path = "text.txt"
    wordlist_path = "words.txt"
    results, timestamps = find_word_matches(plaintext_path, wordlist_path)
    print(f"Found {len(results)} matches")
    for word, start, end in results:
        print(f"{word:20} @ {start:6} -> {end}")