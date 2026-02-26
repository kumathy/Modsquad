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
    for match in regex.finditer(plaintext):
        word = match.group(1)
        start = match.start()
        end = match.end()
        matches.append((word, start, end))
    return matches

if __name__ == "__main__":
    plaintext_path = "text.txt"
    wordlist_path = "words.txt"
    results = find_word_matches(plaintext_path, wordlist_path)
    print(f"Found {len(results)} matches")
    for word, start, end in results:
        print(f"{word:20} @ {start:6} -> {end}")