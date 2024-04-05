def sanitise_string(text: str) -> str:
    text = text.strip()
    words: list[str] = text.split(None)
    for i, word in enumerate(words):
        word = word.strip().lower()
        word = word[0].upper() + word[1:]
        words[i] = word
    text = " ".join(words)
    return text
