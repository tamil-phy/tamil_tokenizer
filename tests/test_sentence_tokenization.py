"""Tests for sentence-level tokenization."""

import pytest
from tamil_tokenizer import TamilTokenizer, Token, TokenType
from .benchmark_data import SENTENCE_CASES


class TestSentenceTokenization:
    """Sentence tokenization tests with benchmark data."""

    @pytest.mark.parametrize(
        "input_text, expected_count, description",
        SENTENCE_CASES,
        ids=[c[2] for c in SENTENCE_CASES],
    )
    def test_sentence_count(self, tokenizer, input_text, expected_count, description):
        tokens = tokenizer.tokenize(input_text, level="sentence")
        assert len(tokens) == expected_count, (
            f"[{description}] Expected {expected_count} sentences, "
            f"got {len(tokens)}: {[t.text for t in tokens]}"
        )

    @pytest.mark.parametrize(
        "input_text, expected_count, description",
        SENTENCE_CASES,
        ids=[c[2] for c in SENTENCE_CASES],
    )
    def test_sentence_type(self, tokenizer, input_text, expected_count, description):
        tokens = tokenizer.tokenize(input_text, level="sentence")
        for t in tokens:
            assert t.token_type == TokenType.SENTENCE

    def test_sentence_text_not_empty(self, tokenizer):
        """No sentence token should have empty text."""
        text = "அவன் வந்தான். அவள் பார்த்தாள்."
        tokens = tokenizer.sentence_tokenize(text)
        for t in tokens:
            assert t.text.strip() != ""

    def test_sentence_positions(self, tokenizer):
        """Start/end positions should be valid and non-overlapping."""
        text = "வணக்கம்! நன்றி. போய் வா?"
        tokens = tokenizer.sentence_tokenize(text)
        prev_end = -1
        for t in tokens:
            assert t.start >= 0
            assert t.end > t.start
            assert t.start >= prev_end
            prev_end = t.end

    def test_sentence_preserves_punctuation(self, tokenizer):
        """Sentence-ending punctuation should be included in the sentence text."""
        tokens = tokenizer.sentence_tokenize("வணக்கம்! நன்றி.")
        assert tokens[0].text.endswith("!")
        assert tokens[1].text.endswith(".")

    def test_sentence_single_word(self, tokenizer):
        """A single word without punctuation is one sentence."""
        tokens = tokenizer.sentence_tokenize("வணக்கம்")
        assert len(tokens) == 1
        assert tokens[0].text == "வணக்கம்"

    def test_sentence_empty_input(self, tokenizer):
        """Empty/whitespace input should return empty list."""
        assert tokenizer.sentence_tokenize("") == []
        assert tokenizer.sentence_tokenize("   ") == []

    def test_sentence_question_marks(self, tokenizer):
        """Multiple questions should split correctly."""
        tokens = tokenizer.sentence_tokenize("என்ன? ஏன்? எப்போது?")
        assert len(tokens) == 3

    def test_sentence_exclamation(self, tokenizer):
        """Exclamation marks should split sentences."""
        tokens = tokenizer.sentence_tokenize("ஆஹா! அருமை!")
        assert len(tokens) == 2
