import re
import argparse


GUTENBERG_START = re.compile(r"\*\*\* START OF (THIS|THE) PROJECT GUTENBERG EBOOK", re.IGNORECASE)
GUTENBERG_END   = re.compile(r"\*\*\* END OF (THIS|THE) PROJECT GUTENBERG EBOOK", re.IGNORECASE)

#https://www.gutenberg.org/files/1661/1661-0.txt
#https://www.gutenberg.org/files/2701/2701-0.txt
#https://www.gutenberg.org/files/2600/2600-0.txt

def strip_gutenberg_headers(text):
    lines = text.split("\n")
    start, end = 0, len(lines)

    for i, line in enumerate(lines):
        if GUTENBERG_START.search(line):
            start = i + 1
            break

    for i, line in enumerate(lines):
        if GUTENBERG_END.search(line):
            end = i
            break

    return "\n".join(lines[start:end])


def normalize_text(text):
    text = text.lower()

    # Normalize punctuation
    text = text.replace("“", "\"").replace("”", "\"")
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("—", "-").replace("–", "-")

    # Remove strange symbols
    text = re.sub(r"[^a-z0-9\s\.,;:\?!'\-]", " ", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_sentences(text):
    sentences = re.split(r"[\.!?]+", text)
    clean = [s.strip() for s in sentences if s.strip()]
    return "\n".join(clean)


def preprocess_file_in_place(path, split=False):
    with open(path, "r", encoding="utf8") as f:
        raw = f.read()

    cleaned = strip_gutenberg_headers(raw)
    cleaned = normalize_text(cleaned)

    if split:
        cleaned = split_sentences(cleaned)

    # overwrite the same file
    with open(path, "w", encoding="utf8") as f:
        f.write(cleaned)

    print(f"✓ Cleaned file in place: {path}")


def main():
    """ python preprocess.py text/sherlock.txt --split"""
    parser = argparse.ArgumentParser(description="Preprocess a text file IN PLACE")
    parser.add_argument("file", help="Path to the .txt file you want to clean")
    parser.add_argument("--split", action="store_true", help="Split into sentences")
    args = parser.parse_args()

    preprocess_file_in_place(args.file, split=args.split)


if __name__ == "__main__":
    main()