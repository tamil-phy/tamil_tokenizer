"""Tests for Python API, convenience methods, and edge cases."""

import pytest
from tamil_tokenizer import TamilTokenizer, Token, TokenType
from .benchmark_data import (
    EDGE_CASES_EMPTY,
    EDGE_CASES_SPECIAL,
    EDGE_CASES_SINGLE_CHAR,
    DIVERSE_SENTENCES,
)


class TestPythonAPI:
    """Core Python API tests."""

    def test_tokenizer_init(self):
        """TamilTokenizer should initialize without errors."""
        t = TamilTokenizer()
        assert t is not None

    def test_tokenizer_init_with_data_path(self):
        """TamilTokenizer should accept a custom data path."""
        t = TamilTokenizer(data_path="/nonexistent/path")
        assert t is not None

    def test_tokenize_returns_list_of_tokens(self, tokenizer):
        tokens = tokenizer.tokenize("அவன் வந்தான்.", level="word")
        assert isinstance(tokens, list)
        assert all(isinstance(t, Token) for t in tokens)

    def test_token_dataclass_fields(self, tokenizer):
        """Token should have text, token_type, start, end, metadata."""
        tokens = tokenizer.tokenize("வணக்கம்.", level="word")
        t = tokens[0]
        assert hasattr(t, "text")
        assert hasattr(t, "token_type")
        assert hasattr(t, "start")
        assert hasattr(t, "end")
        assert hasattr(t, "metadata")

    def test_token_repr(self, tokenizer):
        tokens = tokenizer.tokenize("அவன்", level="word")
        r = repr(tokens[0])
        assert "Token(" in r
        assert "அவன்" in r

    def test_invalid_level_raises(self, tokenizer):
        with pytest.raises(ValueError, match="Unknown tokenization level"):
            tokenizer.tokenize("test", level="invalid")


class TestConvenienceMethods:
    """tokenize_to_strings and tokenize_to_dicts."""

    def test_tokenize_to_strings(self, tokenizer):
        result = tokenizer.tokenize_to_strings("அவன் வந்தான்.", level="word")
        assert isinstance(result, list)
        assert all(isinstance(s, str) for s in result)
        assert result == ["அவன்", "வந்தான்", "."]

    def test_tokenize_to_dicts(self, tokenizer):
        result = tokenizer.tokenize_to_dicts("அவன் வந்தான்.", level="word")
        assert isinstance(result, list)
        assert all(isinstance(d, dict) for d in result)
        assert "text" in result[0]
        assert "type" in result[0]
        assert "start" in result[0]
        assert "end" in result[0]
        assert "metadata" in result[0]

    def test_tokenize_to_dicts_morpheme(self, tokenizer):
        result = tokenizer.tokenize_to_dicts("பள்ளிக்கு", level="morpheme")
        types = [d["type"] for d in result]
        assert "root" in types

    def test_tokenize_to_strings_character(self, tokenizer):
        result = tokenizer.tokenize_to_strings("தமிழ்", level="character")
        assert result == ["த", "மி", "ழ்"]

    def test_tokenize_to_strings_sentence(self, tokenizer):
        result = tokenizer.tokenize_to_strings(
            "அவன் வந்தான். அவள் பார்த்தாள்.", level="sentence"
        )
        assert len(result) == 2


class TestEdgeCases:
    """Edge case handling."""

    @pytest.mark.parametrize(
        "input_text, description",
        EDGE_CASES_EMPTY,
        ids=[c[1] for c in EDGE_CASES_EMPTY],
    )
    def test_empty_inputs(self, tokenizer, input_text, description):
        for level in ["word", "character", "sentence", "morpheme"]:
            tokens = tokenizer.tokenize(input_text, level=level)
            assert tokens == [], (
                f"[{description}] Expected empty list for level '{level}', got {tokens}"
            )

    @pytest.mark.parametrize(
        "input_text, expected_count, description",
        EDGE_CASES_SPECIAL,
        ids=[c[2] for c in EDGE_CASES_SPECIAL],
    )
    def test_special_inputs(self, tokenizer, input_text, expected_count, description):
        tokens = tokenizer.tokenize(input_text, level="word")
        assert len(tokens) == expected_count, (
            f"[{description}] Expected {expected_count} tokens, "
            f"got {len(tokens)}: {[t.text for t in tokens]}"
        )

    @pytest.mark.parametrize(
        "input_char, expected_type, description",
        EDGE_CASES_SINGLE_CHAR,
        ids=[c[2] for c in EDGE_CASES_SINGLE_CHAR],
    )
    def test_single_char_word(self, tokenizer, input_char, expected_type, description):
        tokens = tokenizer.tokenize(input_char, level="word")
        assert len(tokens) == 1
        assert tokens[0].token_type.value == expected_type

    def test_very_long_text(self, tokenizer):
        """Tokenizer should handle long text without crashing."""
        text = "தமிழ் மொழி சிறந்தது. " * 100
        tokens = tokenizer.tokenize(text, level="word")
        assert len(tokens) > 100

    def test_mixed_tamil_english(self, tokenizer):
        """Mixed Tamil/English text should not crash."""
        tokens = tokenizer.tokenize("Hello வணக்கம் World", level="word")
        assert len(tokens) >= 3

    def test_numbers_only(self, tokenizer):
        tokens = tokenizer.tokenize("12345", level="word")
        assert len(tokens) == 1
        assert tokens[0].token_type == TokenType.NUMBER

    def test_repeated_punctuation(self, tokenizer):
        tokens = tokenizer.tokenize("...!!!", level="word")
        assert all(t.token_type == TokenType.PUNCTUATION for t in tokens)


class TestDiverseCorpus:
    """Run tokenization on diverse real-world Tamil sentences."""

    @pytest.mark.parametrize(
        "sentence",
        DIVERSE_SENTENCES,
        ids=[f"diverse_{i}" for i in range(len(DIVERSE_SENTENCES))],
    )
    def test_word_tokenize_no_crash(self, tokenizer, sentence):
        tokens = tokenizer.tokenize(sentence, level="word")
        assert len(tokens) >= 1
        assert all(isinstance(t, Token) for t in tokens)

    @pytest.mark.parametrize(
        "sentence",
        DIVERSE_SENTENCES,
        ids=[f"diverse_{i}" for i in range(len(DIVERSE_SENTENCES))],
    )
    def test_character_tokenize_no_crash(self, tokenizer, sentence):
        tokens = tokenizer.tokenize(sentence, level="character")
        assert len(tokens) >= 1

    @pytest.mark.parametrize(
        "sentence",
        DIVERSE_SENTENCES,
        ids=[f"diverse_{i}" for i in range(len(DIVERSE_SENTENCES))],
    )
    def test_morpheme_tokenize_no_crash(self, tokenizer, sentence):
        tokens = tokenizer.tokenize(sentence, level="morpheme")
        assert len(tokens) >= 1
        # Every morpheme result should have at least one ROOT
        root_tokens = [t for t in tokens if t.token_type == TokenType.ROOT]
        assert len(root_tokens) >= 1, (
            f"No ROOT token found for: {sentence}"
        )

    @pytest.mark.parametrize(
        "sentence",
        DIVERSE_SENTENCES,
        ids=[f"diverse_{i}" for i in range(len(DIVERSE_SENTENCES))],
    )
    def test_sentence_tokenize_no_crash(self, tokenizer, sentence):
        tokens = tokenizer.tokenize(sentence, level="sentence")
        assert len(tokens) >= 1


class TestTokenTypeEnum:
    """Verify TokenType enum values."""

    def test_all_expected_types_exist(self):
        expected = [
            "sentence", "word", "punctuation", "number", "symbol",
            "whitespace", "vowel", "consonant", "vowel_consonant",
            "special", "root", "suffix", "case_suffix",
            "tense_marker", "person_marker", "plural_marker",
        ]
        actual = [t.value for t in TokenType]
        for e in expected:
            assert e in actual, f"Missing TokenType: {e}"
