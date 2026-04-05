# Tamil Tokenizer

A standalone, multi-level tokenizer for Tamil text. No external dependencies — uses only the Python standard library.

## Features

Four levels of tokenization:

| Level | Description | Example |
|-------|-------------|---------|
| **sentence** | Split text into sentences | `"அவன் வந்தான். அவள் பார்த்தாள்."` → 2 sentences |
| **word** | Split into words + punctuation | `"அவன் வந்தான்."` → `அவன்`, `வந்தான்`, `.` |
| **character** | Split into Tamil letters with classification (உயிர்/மெய்/உயிர்மெய், வல்லினம்/மெல்லினம்/இடையினம்) | `"வந்தான்"` → `வ`, `ந்`, `தா`, `ன்` |
| **morpheme** | Split into root + grammatical suffixes (case, tense, person) | `"பள்ளிக்கு"` → root `பள்ளி` + case suffix `க்கு` (Dative) |

## Installation

```bash
# From the project directory
pip install -e .

# Or just use directly (no install needed)
python -m tamil_tokenizer "அவன் வந்தான்."
```

## Usage

### Command Line

```bash
# Word tokenization (default)
python -m tamil_tokenizer "அவன் வந்தான்."

# Character tokenization
python -m tamil_tokenizer "தமிழ்நாடு" --level character

# Sentence tokenization
python -m tamil_tokenizer "அவன் வந்தான். அவள் பார்த்தாள்." --level sentence

# Morpheme tokenization
python -m tamil_tokenizer "பள்ளிக்கு சென்றான்." --level morpheme

# JSON output
python -m tamil_tokenizer "அவன் வந்தான்." --format json

# Plain text output (just token strings)
python -m tamil_tokenizer "அவன் வந்தான்." --format text

# Interactive mode
python -m tamil_tokenizer --interactive
```

### Python API

```python
from tamil_tokenizer import TamilTokenizer, Token, TokenType

tokenizer = TamilTokenizer()

# Sentence tokenization
sentences = tokenizer.sentence_tokenize("அவன் வந்தான். அவள் பார்த்தாள்.")

# Word tokenization
words = tokenizer.word_tokenize("அவன் வந்தான்.")

# Character tokenization
letters = tokenizer.character_tokenize("வந்தான்")
for letter in letters:
    print(f"{letter.text} -> {letter.token_type.value} ({letter.metadata})")

# Morpheme tokenization
morphemes = tokenizer.morpheme_tokenize("பள்ளிக்கு")
for m in morphemes:
    print(f"{m.text} -> {m.token_type.value} ({m.metadata})")

# Unified pipeline
tokens = tokenizer.tokenize("அவன் வந்தான்.", level="word")

# Convenience: get just strings
strings = tokenizer.tokenize_to_strings("அவன் வந்தான்.", level="word")
# ['அவன்', 'வந்தான்', '.']

# Convenience: get dicts (useful for JSON serialization)
dicts = tokenizer.tokenize_to_dicts("அவன் வந்தான்.", level="character")
```

## Token Types

### Word-level
- `word` — Tamil word
- `number` — Numeric value
- `punctuation` — Punctuation mark
- `symbol` — Other symbol

### Character-level
- `vowel` — உயிரெழுத்து (அ, ஆ, இ, ...)
- `consonant` — மெய்யெழுத்து (க், ங், ச், ...)
- `vowel_consonant` — உயிர்மெய்யெழுத்து (க, கா, கி, ...)
- `special` — ஆய்த எழுத்து (ஃ)

### Morpheme-level
- `root` — Root word
- `suffix` — Generic suffix
- `case_suffix` — வேற்றுமை உருபு (case marker)
- `tense_marker` — கால இடைநிலை (tense marker)
- `person_marker` — விகுதி (person/number marker)

## Project Structure

```
tamil_tokenizer/
├── __init__.py          # Package init + public API
├── __main__.py          # CLI entry point
├── tokenizer.py         # Main TamilTokenizer class
├── constants/           # Tamil Unicode constants & letter groups
├── grammar/             # Grammar analysis (util, case, tense)
├── config/              # Configuration & data file loading
├── parsers/             # Root word parser & core parsing
├── utils/               # Iterator, splitting, word class utilities
└── data/                # Grammar rule files (.list)
```

## Requirements

- Python 3.8+
- No external dependencies
