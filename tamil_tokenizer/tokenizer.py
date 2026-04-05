"""
Tamil Tokenizer - Multi-level tokenization for Tamil text.

Provides four levels of tokenization:
1. Sentence tokenization - split text into sentences
2. Word tokenization - split text/sentences into words
3. Character tokenization - split words into Tamil letters (எழுத்துகள்)
4. Morpheme tokenization - split words into root + grammatical suffixes

Uses the existing grammar analysis, case analysis, and root word
parsing infrastructure.

Author: Tamil NLP Project
"""

import re
import unicodedata
from enum import Enum
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field


class TokenType(Enum):
    """Types of tokens produced by the tokenizer."""
    SENTENCE = "sentence"
    WORD = "word"
    PUNCTUATION = "punctuation"
    NUMBER = "number"
    SYMBOL = "symbol"
    WHITESPACE = "whitespace"
    # Character-level types
    VOWEL = "vowel"              # உயிரெழுத்து
    CONSONANT = "consonant"      # மெய்யெழுத்து
    VOWEL_CONSONANT = "vowel_consonant"  # உயிர்மெய்யெழுத்து
    SPECIAL = "special"          # ஆய்த எழுத்து (ஃ)
    # Morpheme-level types
    ROOT = "root"
    SUFFIX = "suffix"
    CASE_SUFFIX = "case_suffix"          # வேற்றுமை உருபு
    TENSE_MARKER = "tense_marker"        # கால இடைநிலை
    PERSON_MARKER = "person_marker"      # விகுதி
    PLURAL_MARKER = "plural_marker"      # பன்மை விகுதி


@dataclass
class Token:
    """
    A single token produced by the tokenizer.

    Attributes:
        text: The token text
        token_type: Type of the token
        start: Start position in the original text
        end: End position in the original text
        metadata: Additional information about the token
    """
    text: str
    token_type: TokenType
    start: int = 0
    end: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        meta_str = f", metadata={self.metadata}" if self.metadata else ""
        return f"Token('{self.text}', {self.token_type.value}, [{self.start}:{self.end}]{meta_str})"


# Tamil Unicode ranges
_TAMIL_RANGE_START = 0x0B80
_TAMIL_RANGE_END = 0x0BFF
_TAMIL_VOWELS = set(range(0x0B85, 0x0B95))  # அ to ஔ + ஃ
_TAMIL_VOWELS.add(0x0B83)  # ஃ
_TAMIL_CONSONANTS = set(range(0x0B95, 0x0BBA))  # க to ஹ
_TAMIL_VOWEL_SIGNS = set(range(0x0BBE, 0x0BD0))  # Dependent vowel signs
_TAMIL_PULLI = 0x0BCD  # Virama ்

# Sentence-ending punctuation
_SENTENCE_ENDERS = {'.', '!', '?', '।', '॥'}
# Tamil-specific: sometimes sentences end with these
_SENTENCE_ENDER_PATTERN = re.compile(
    r'(?<=[.!?।॥])\s+|(?<=[.!?।॥])$'
)


def _is_tamil_char(ch: str) -> bool:
    """Check if a character is in the Tamil Unicode block."""
    code = ord(ch)
    return _TAMIL_RANGE_START <= code <= _TAMIL_RANGE_END


def _classify_tamil_letter(letter: str) -> TokenType:
    """
    Classify a Tamil letter into its type.

    Args:
        letter: A single Tamil letter (may be multi-codepoint for உயிர்மெய்)

    Returns:
        TokenType for the letter
    """
    if not letter:
        return TokenType.SYMBOL

    first_code = ord(letter[0])

    # ஃ (Aytham)
    if first_code == 0x0B83:
        return TokenType.SPECIAL

    # Independent vowel
    if first_code in _TAMIL_VOWELS:
        return TokenType.VOWEL

    # Consonant base
    if first_code in _TAMIL_CONSONANTS:
        if len(letter) == 1:
            # Bare consonant (implicitly has அ)
            return TokenType.VOWEL_CONSONANT
        elif len(letter) >= 2:
            second_code = ord(letter[1])
            if second_code == _TAMIL_PULLI:
                return TokenType.CONSONANT  # Pure consonant (மெய்)
            elif second_code in _TAMIL_VOWEL_SIGNS:
                return TokenType.VOWEL_CONSONANT  # Vowel-consonant combo
        return TokenType.VOWEL_CONSONANT

    return TokenType.SYMBOL


class TamilTokenizer:
    """
    Multi-level tokenizer for Tamil text.

    Supports four tokenization levels:
    - **sentence**: Split text into sentences
    - **word**: Split text into words (and punctuation)
    - **character**: Split words into individual Tamil letters
    - **morpheme**: Split words into root + grammatical suffixes

    Usage:
        tokenizer = TamilTokenizer()

        # Sentence tokenization
        sentences = tokenizer.sentence_tokenize("வணக்கம். நன்றி.")

        # Word tokenization
        words = tokenizer.word_tokenize("அவன் வந்தான்.")

        # Character (letter) tokenization
        letters = tokenizer.character_tokenize("வந்தான்")

        # Morpheme tokenization
        morphemes = tokenizer.morpheme_tokenize("வந்தான்")

        # Full pipeline
        result = tokenizer.tokenize("அவன் வந்தான்.", level="morpheme")
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the tokenizer.

        Args:
            data_path: Optional path to the data directory for the root word parser.
                       If None, uses the default path.
        """
        self._data_path = data_path
        self._root_parser = None  # Lazy-loaded
        self._word_splitter = None  # Lazy-loaded

    def _get_word_splitter(self):
        """Lazy-load the WordSplitter."""
        if self._word_splitter is None:
            from .utils.word_splitter import WordSplitter
            self._word_splitter = WordSplitter()
        return self._word_splitter

    def _get_root_parser(self):
        """Lazy-load the TamilRootWordParser."""
        if self._root_parser is None:
            from .parsers.root_word_parser import TamilRootWordParser
            self._root_parser = TamilRootWordParser(self._data_path)
        return self._root_parser

    # ===================== Sentence Tokenization =====================

    def sentence_tokenize(self, text: str) -> List[Token]:
        """
        Split text into sentence tokens.

        Splits on sentence-ending punctuation (.!?।) followed by whitespace
        or end-of-string. Handles abbreviations and decimals gracefully.

        Args:
            text: Input Tamil text

        Returns:
            List of Token objects, one per sentence
        """
        if not text or not text.strip():
            return []

        sentences = []
        current_start = 0
        i = 0

        while i < len(text):
            ch = text[i]

            if ch in _SENTENCE_ENDERS:
                # Look ahead: is this truly end of sentence?
                # Not end-of-sentence if followed by a digit (e.g., "3.14")
                next_idx = i + 1
                while next_idx < len(text) and text[next_idx] == ' ':
                    next_idx += 1

                is_decimal = (ch == '.' and i + 1 < len(text) and text[i + 1].isdigit())

                if not is_decimal:
                    # Include the punctuation in the sentence
                    sent_text = text[current_start:i + 1].strip()
                    if sent_text:
                        sentences.append(Token(
                            text=sent_text,
                            token_type=TokenType.SENTENCE,
                            start=current_start,
                            end=i + 1,
                        ))
                    current_start = i + 1
            i += 1

        # Remaining text as a sentence
        remaining = text[current_start:].strip()
        if remaining:
            sentences.append(Token(
                text=remaining,
                token_type=TokenType.SENTENCE,
                start=current_start,
                end=len(text),
            ))

        return sentences

    # ===================== Word Tokenization =====================

    def word_tokenize(self, text: str) -> List[Token]:
        """
        Split text into word tokens.

        Produces tokens for Tamil words, numbers, punctuation, and symbols.
        Uses the existing WordSplitter and adds position tracking and type
        classification.

        Args:
            text: Input Tamil text

        Returns:
            List of Token objects
        """
        if not text or not text.strip():
            return []

        tokens = []
        # Use regex-based tokenization that preserves positions
        # Pattern: Tamil words | numbers | punctuation/symbols | whitespace
        pattern = re.compile(
            r'([\u0B80-\u0BFF]+)'   # Tamil characters
            r'|(\d[\d,]*\.?\d*)'     # Numbers
            r'|([.!?,;:\"\'()\-–—…।॥])'  # Punctuation
            r'|(\S+)'               # Other non-whitespace
        )

        for match in pattern.finditer(text):
            token_text = match.group()
            start = match.start()
            end = match.end()

            if match.group(1):  # Tamil word
                token_type = TokenType.WORD
            elif match.group(2):  # Number
                token_type = TokenType.NUMBER
            elif match.group(3):  # Punctuation
                token_type = TokenType.PUNCTUATION
            else:  # Other
                token_type = TokenType.SYMBOL

            tokens.append(Token(
                text=token_text,
                token_type=token_type,
                start=start,
                end=end,
            ))

        return tokens

    # ===================== Character Tokenization =====================

    def character_tokenize(self, word: str) -> List[Token]:
        """
        Split a Tamil word into its constituent letters (எழுத்துகள்).

        A Tamil "letter" may be:
        - A vowel (உயிரெழுத்து): அ, ஆ, இ, ...
        - A pure consonant (மெய்யெழுத்து): க், ங், ச், ...
        - A vowel-consonant (உயிர்மெய்யெழுத்து): க, கா, கி, ...
        - ஃ (ஆய்த எழுத்து)

        This groups Unicode codepoints into logical Tamil letters.

        Args:
            word: A Tamil word

        Returns:
            List of Token objects, one per Tamil letter
        """
        if not word:
            return []

        letters = self._split_to_tamil_letters(word)
        tokens = []
        pos = 0

        for letter in letters:
            letter_type = _classify_tamil_letter(letter)
            tokens.append(Token(
                text=letter,
                token_type=letter_type,
                start=pos,
                end=pos + len(letter),
                metadata=self._get_letter_metadata(letter, letter_type),
            ))
            pos += len(letter)

        return tokens

    def _split_to_tamil_letters(self, word: str) -> List[str]:
        """
        Split a word into logical Tamil letters by grouping codepoints.

        Groups: consonant + optional(vowel_sign | pulli) as one letter.

        Args:
            word: Input word

        Returns:
            List of logical Tamil letters
        """
        letters = []
        i = 0

        while i < len(word):
            ch = word[i]
            code = ord(ch)

            if code in _TAMIL_CONSONANTS:
                # Consonant: absorb following vowel sign or pulli
                letter = ch
                j = i + 1
                while j < len(word):
                    next_code = ord(word[j])
                    if next_code in _TAMIL_VOWEL_SIGNS or next_code == _TAMIL_PULLI:
                        letter += word[j]
                        j += 1
                        # Two-part vowel signs (ொ = ெ + ா, ோ = ே + ா, etc.)
                        if j < len(word) and ord(word[j]) in _TAMIL_VOWEL_SIGNS:
                            letter += word[j]
                            j += 1
                        break
                    else:
                        break
                letters.append(letter)
                i = j
            else:
                letters.append(ch)
                i += 1

        return letters

    def _get_letter_metadata(self, letter: str, letter_type: TokenType) -> Dict[str, str]:
        """Get metadata for a Tamil letter."""
        meta = {}

        if letter_type == TokenType.VOWEL:
            meta["category"] = "உயிரெழுத்து"
            meta["category_en"] = "vowel"
        elif letter_type == TokenType.CONSONANT:
            meta["category"] = "மெய்யெழுத்து"
            meta["category_en"] = "consonant"
            # Classify as vallinam/mellinam/idaiyinam
            base_code = ord(letter[0])
            vallinam = {0x0B95, 0x0B9A, 0x0B9F, 0x0BA4, 0x0BAA, 0x0BB1}
            mellinam = {0x0B99, 0x0B9E, 0x0BA3, 0x0BA8, 0x0BAE, 0x0BA9}
            idaiyinam = {0x0BAF, 0x0BB0, 0x0BB2, 0x0BB3, 0x0BB4, 0x0BB5}
            if base_code in vallinam:
                meta["class"] = "வல்லினம்"
                meta["class_en"] = "vallinam"
            elif base_code in mellinam:
                meta["class"] = "மெல்லினம்"
                meta["class_en"] = "mellinam"
            elif base_code in idaiyinam:
                meta["class"] = "இடையினம்"
                meta["class_en"] = "idaiyinam"
        elif letter_type == TokenType.VOWEL_CONSONANT:
            meta["category"] = "உயிர்மெய்யெழுத்து"
            meta["category_en"] = "vowel_consonant"
        elif letter_type == TokenType.SPECIAL:
            meta["category"] = "ஆய்த எழுத்து"
            meta["category_en"] = "aytham"

        return meta

    # ===================== Morpheme Tokenization =====================

    def morpheme_tokenize(self, word: str) -> List[Token]:
        """
        Split a Tamil word into morphemes (root + grammatical suffixes).

        Combines root word parsing with case and tense analysis to produce
        a sequence of morpheme tokens.

        Args:
            word: A Tamil word

        Returns:
            List of Token objects representing morphemes
        """
        if not word or not word.strip():
            return []

        word = word.strip()
        morphemes = []

        # 1. Try root word parsing
        root, suffixes, parse_meta = self._parse_root_and_suffixes(word)

        # 2. If no parse result, try case analysis
        if not suffixes:
            root, suffixes, parse_meta = self._analyze_case(word)

        # 3. If still no result, try tense/person analysis for verbs
        if not suffixes:
            root, suffixes, parse_meta = self._analyze_verb_morphology(word)

        # Build morpheme tokens
        if suffixes:
            morphemes.append(Token(
                text=root,
                token_type=TokenType.ROOT,
                start=0,
                end=len(root),
                metadata=parse_meta.get("root_meta", {}),
            ))
            pos = len(root)
            for sfx_text, sfx_type, sfx_meta in suffixes:
                morphemes.append(Token(
                    text=sfx_text,
                    token_type=sfx_type,
                    start=pos,
                    end=pos + len(sfx_text),
                    metadata=sfx_meta,
                ))
                pos += len(sfx_text)
        else:
            # No morphological decomposition found; return as single root
            morphemes.append(Token(
                text=word,
                token_type=TokenType.ROOT,
                start=0,
                end=len(word),
                metadata={"note": "no_decomposition"},
            ))

        return morphemes

    def _parse_root_and_suffixes(self, word: str):
        """Use TamilRootWordParser to extract root and suffixes."""
        try:
            parser = self._get_root_parser()
            wc_list = parser.create_single_instance(word)

            if wc_list:
                for wc in wc_list:
                    word_type = wc.get_type()
                    root_word = wc.get_word()
                    splitted = wc.get_splitted_val()

                    if splitted and root_word and root_word != word:
                        parts = [p.strip() for p in splitted.split(",") if p.strip()]
                        suffixes = []
                        for part in parts:
                            if part and part != root_word:
                                suffixes.append((
                                    part,
                                    TokenType.SUFFIX,
                                    {"source": "root_parser"}
                                ))

                        if suffixes:
                            root_meta = {
                                "word_type": word_type,
                                "source": "root_parser"
                            }
                            return root_word, suffixes, {"root_meta": root_meta}
        except Exception:
            pass

        return word, [], {}

    def _analyze_case(self, word: str):
        """Use TamilVetrumai (case analysis) to find case suffix."""
        try:
            from .grammar.vetrumai import TamilVetrumai
            result = TamilVetrumai.analyze(word)

            if result.suffix and result.case_number > 1:
                root = result.root
                suffix_text = result.suffix
                suffix_meta = {
                    "case_number": result.case_number,
                    "case_name": result.case_name,
                    "case_tamil": result.case_tamil_name,
                    "source": "vetrumai",
                }
                return root, [(suffix_text, TokenType.CASE_SUFFIX, suffix_meta)], {
                    "root_meta": {"source": "vetrumai"}
                }
        except Exception:
            pass

        return word, [], {}

    def _analyze_verb_morphology(self, word: str):
        """Analyze verb morphology for tense and person markers."""
        try:
            from .grammar.illakanam import TamilIllakanam
            from .grammar.tamil_util import TamilUtil

            split_word = TamilUtil.split_letters(word)
            suffixes = []

            # Tense markers
            tense = TamilIllakanam.get_tense(word)
            tense_markers_map = {
                "இறந்தகாலம்": ["த்த்", "ந்த்", "ட்ட்", "ற்ற்"],
                "நிகழ்காலம்": ["கிற்", "கின்ற்", "க்கிற்", "க்கின்ற்"],
                "எதிர்காலம்": ["ப்ப்", "வ்"],
            }

            tense_suffix = None
            if tense and tense in tense_markers_map:
                for marker in tense_markers_map[tense]:
                    if marker in split_word:
                        # Convert back to display form
                        tense_suffix = TamilUtil.join_letters(marker)
                        break

            # Person markers
            person = TamilIllakanam.get_person(word)
            person_markers_map = {
                "தன்மை": ["ஏன்", "ஓம்", "ஏம்"],
                "முன்னிலை": ["ஆய்", "ஈர்", "ஈர்கள்"],
                "படர்க்கை": ["ஆன்", "ஆள்", "ஆர்", "ஆர்கள்", "அது", "அன", "அர்"],
            }

            person_suffix = None
            if person and person in person_markers_map:
                for marker in person_markers_map[person]:
                    if split_word.endswith(marker):
                        person_suffix = TamilUtil.join_letters(marker)
                        break

            if tense_suffix or person_suffix:
                # Estimate root: strip known suffixes from end
                root = word
                if person_suffix and root.endswith(person_suffix):
                    root = root[:-len(person_suffix)]
                if tense_suffix and root.endswith(tense_suffix):
                    root = root[:-len(tense_suffix)]

                if tense_suffix:
                    suffixes.append((
                        tense_suffix,
                        TokenType.TENSE_MARKER,
                        {"tense": tense, "source": "illakanam"},
                    ))
                if person_suffix:
                    suffixes.append((
                        person_suffix,
                        TokenType.PERSON_MARKER,
                        {"person": person, "source": "illakanam"},
                    ))

                if suffixes and root != word:
                    return root, suffixes, {"root_meta": {"source": "illakanam"}}

        except Exception:
            pass

        return word, [], {}

    # ===================== Unified Pipeline =====================

    def tokenize(self, text: str, level: str = "word") -> List[Token]:
        """
        Tokenize Tamil text at the specified level.

        Args:
            text: Input Tamil text
            level: Tokenization level - one of:
                   "sentence", "word", "character", "morpheme"

        Returns:
            List of Token objects

        Raises:
            ValueError: If level is not recognized
        """
        level = level.lower()

        if level == "sentence":
            return self.sentence_tokenize(text)

        elif level == "word":
            return self.word_tokenize(text)

        elif level == "character":
            # Tokenize words first, then characters for each Tamil word
            word_tokens = self.word_tokenize(text)
            all_tokens = []
            for wt in word_tokens:
                if wt.token_type == TokenType.WORD:
                    char_tokens = self.character_tokenize(wt.text)
                    # Adjust positions relative to original text
                    for ct in char_tokens:
                        ct.start += wt.start
                        ct.end += wt.start
                    all_tokens.extend(char_tokens)
                else:
                    all_tokens.append(wt)
            return all_tokens

        elif level == "morpheme":
            # Tokenize words first, then morphemes for each Tamil word
            word_tokens = self.word_tokenize(text)
            all_tokens = []
            for wt in word_tokens:
                if wt.token_type == TokenType.WORD:
                    morph_tokens = self.morpheme_tokenize(wt.text)
                    # Adjust positions relative to original text
                    for mt in morph_tokens:
                        mt.start += wt.start
                        mt.end += wt.start
                    all_tokens.extend(morph_tokens)
                else:
                    all_tokens.append(wt)
            return all_tokens

        else:
            raise ValueError(
                f"Unknown tokenization level: '{level}'. "
                f"Use 'sentence', 'word', 'character', or 'morpheme'."
            )

    # ===================== Convenience Methods =====================

    def tokenize_to_strings(self, text: str, level: str = "word") -> List[str]:
        """
        Tokenize and return just the text strings (no metadata).

        Args:
            text: Input Tamil text
            level: Tokenization level

        Returns:
            List of token strings
        """
        return [t.text for t in self.tokenize(text, level)]

    def tokenize_to_dicts(self, text: str, level: str = "word") -> List[Dict[str, Any]]:
        """
        Tokenize and return list of dictionaries.

        Args:
            text: Input Tamil text
            level: Tokenization level

        Returns:
            List of token dictionaries
        """
        return [
            {
                "text": t.text,
                "type": t.token_type.value,
                "start": t.start,
                "end": t.end,
                "metadata": t.metadata,
            }
            for t in self.tokenize(text, level)
        ]
