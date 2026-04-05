"""Tests for word-level tokenization."""

import pytest
from tamil_tokenizer import TamilTokenizer, Token, TokenType
from .benchmark_data import WORD_CASES


class TestWordTokenization:
    """Word tokenization tests with benchmark data."""

    @pytest.mark.parametrize(
        "input_text, expected_words, description",
        WORD_CASES,
        ids=[c[2] for c in WORD_CASES],
    )
    def test_word_tokenization(self, tokenizer, input_text, expected_words, description):
        tokens = tokenizer.tokenize(input_text, level="word")
        actual_words = [t.text for t in tokens]
        assert actual_words == expected_words, (
            f"[{description}] Expected {expected_words}, got {actual_words}"
        )

    def test_word_token_types(self, tokenizer):
        """Each token should have the correct type."""
        tokens = tokenizer.tokenize("நான் 100 ரூபாய் கொடுத்தேன்.", level="word")
        types = [(t.text, t.token_type) for t in tokens]

        assert types[0] == ("நான்", TokenType.WORD)
        assert types[1] == ("100", TokenType.NUMBER)
        assert types[2] == ("ரூபாய்", TokenType.WORD)
        assert types[3] == ("கொடுத்தேன்", TokenType.WORD)
        assert types[4] == (".", TokenType.PUNCTUATION)

    def test_word_positions_are_valid(self, tokenizer):
        """Start/end positions must be non-negative and non-overlapping."""
        text = "தமிழ்நாடு இந்தியாவின் மாநிலம்."
        tokens = tokenizer.tokenize(text, level="word")

        prev_end = -1
        for t in tokens:
            assert t.start >= 0
            assert t.end > t.start
            assert t.start >= prev_end, f"Overlapping token: {t}"
            prev_end = t.end

    def test_word_positions_match_source(self, tokenizer):
        """Token text must match the source text at the given positions."""
        text = "அவன் வந்தான்."
        tokens = tokenizer.tokenize(text, level="word")

        for t in tokens:
            assert text[t.start:t.end] == t.text, (
                f"Position mismatch: text[{t.start}:{t.end}] = "
                f"'{text[t.start:t.end]}', token = '{t.text}'"
            )

    def test_word_multiple_punctuation_types(self, tokenizer):
        """Various punctuation characters should be recognized."""
        tokens = tokenizer.tokenize("வா! ஏன்? சரி.", level="word")
        punct = [t.text for t in tokens if t.token_type == TokenType.PUNCTUATION]
        assert "!" in punct
        assert "?" in punct
        assert "." in punct

    def test_word_preserves_all_content(self, tokenizer):
        """Concatenated token texts should reconstruct the non-whitespace content."""
        text = "நான் பள்ளிக்கு சென்றேன்."
        tokens = tokenizer.tokenize(text, level="word")
        reconstructed = "".join(t.text for t in tokens)
        original_no_ws = text.replace(" ", "")
        assert reconstructed == original_no_ws

    def test_word_tamil_numbers_mixed(self, tokenizer):
        """Numbers mixed with Tamil text should be correctly tokenized."""
        tokens = tokenizer.tokenize("2024 ஆம் ஆண்டு", level="word")
        assert tokens[0].token_type == TokenType.NUMBER
        assert tokens[0].text == "2024"
        assert tokens[1].token_type == TokenType.WORD

    def test_word_long_sentence(self, tokenizer):
        """Long sentence should tokenize without error."""
        text = (
            "தமிழ் மொழி உலகின் மிகப் பழமையான மொழிகளில் ஒன்று "
            "என்பதை அனைவரும் அறிவர்."
        )
        tokens = tokenizer.tokenize(text, level="word")
        assert len(tokens) >= 10
        assert all(isinstance(t, Token) for t in tokens)
