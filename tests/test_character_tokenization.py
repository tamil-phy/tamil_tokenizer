"""Tests for character-level tokenization."""

import pytest
from tamil_tokenizer import TamilTokenizer, Token, TokenType
from .benchmark_data import CHARACTER_CASES, CONSONANT_CLASSES


class TestCharacterTokenization:
    """Character (letter) tokenization tests."""

    @pytest.mark.parametrize(
        "input_word, expected_letters, expected_types, description",
        CHARACTER_CASES,
        ids=[c[3] for c in CHARACTER_CASES],
    )
    def test_character_letters(self, tokenizer, input_word, expected_letters, expected_types, description):
        tokens = tokenizer.character_tokenize(input_word)
        actual_letters = [t.text for t in tokens]
        assert actual_letters == expected_letters, (
            f"[{description}] Expected {expected_letters}, got {actual_letters}"
        )

    @pytest.mark.parametrize(
        "input_word, expected_letters, expected_types, description",
        CHARACTER_CASES,
        ids=[c[3] for c in CHARACTER_CASES],
    )
    def test_character_types(self, tokenizer, input_word, expected_letters, expected_types, description):
        tokens = tokenizer.character_tokenize(input_word)
        actual_types = [t.token_type.value for t in tokens]
        assert actual_types == expected_types, (
            f"[{description}] Expected types {expected_types}, got {actual_types}"
        )

    @pytest.mark.parametrize(
        "letter, expected_class",
        CONSONANT_CLASSES,
        ids=[f"{c[0]}_{c[1]}" for c in CONSONANT_CLASSES],
    )
    def test_consonant_classification(self, tokenizer, letter, expected_class):
        """Verify vallinam/mellinam/idaiyinam classification for all 18 consonants."""
        tokens = tokenizer.character_tokenize(letter)
        assert len(tokens) == 1
        assert tokens[0].token_type == TokenType.CONSONANT
        assert tokens[0].metadata.get("class_en") == expected_class, (
            f"'{letter}' should be {expected_class}, got {tokens[0].metadata}"
        )

    def test_character_metadata_vowel(self, tokenizer):
        """Vowels should have correct metadata."""
        tokens = tokenizer.character_tokenize("அ")
        assert tokens[0].metadata["category"] == "உயிரெழுத்து"
        assert tokens[0].metadata["category_en"] == "vowel"

    def test_character_metadata_vowel_consonant(self, tokenizer):
        """Vowel-consonants should have correct metadata."""
        tokens = tokenizer.character_tokenize("கா")
        assert tokens[0].metadata["category"] == "உயிர்மெய்யெழுத்து"
        assert tokens[0].metadata["category_en"] == "vowel_consonant"

    def test_character_metadata_aytham(self, tokenizer):
        """Aytham (ஃ) should have special category."""
        tokens = tokenizer.character_tokenize("ஃ")
        assert tokens[0].metadata["category_en"] == "aytham"

    def test_all_12_vowels(self, tokenizer):
        """All 12 Tamil vowels should be recognized."""
        vowels = "அஆஇஈஉஊஎஏஐஒஓஔ"
        tokens = tokenizer.character_tokenize(vowels)
        assert len(tokens) == 12
        assert all(t.token_type == TokenType.VOWEL for t in tokens)

    def test_character_positions_sequential(self, tokenizer):
        """Character positions should be sequential and cover the full word."""
        word = "வணக்கம்"
        tokens = tokenizer.character_tokenize(word)
        assert tokens[0].start == 0
        for i in range(1, len(tokens)):
            assert tokens[i].start == tokens[i - 1].end
        assert tokens[-1].end == len(word)

    def test_character_via_tokenize_level(self, tokenizer):
        """tokenize(level='character') should split words into characters, keep punctuation."""
        tokens = tokenizer.tokenize("தமிழ்.", level="character")
        types = [t.token_type.value for t in tokens]
        texts = [t.text for t in tokens]
        assert "த" in texts
        assert "." in texts
        assert "consonant" in types  # ழ்
        assert "punctuation" in types

    def test_empty_word_returns_empty(self, tokenizer):
        """Empty input should return empty list."""
        assert tokenizer.character_tokenize("") == []
        assert tokenizer.character_tokenize(None) == []
