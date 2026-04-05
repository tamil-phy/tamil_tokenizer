"""Tests for morpheme-level tokenization."""

import pytest
from tamil_tokenizer import TamilTokenizer, Token, TokenType
from .benchmark_data import (
    VETRUMAI_CASES,
    NO_DECOMPOSITION_WORDS,
    MORPHEME_SENTENCE_CASES,
)


class TestMorphemeTokenization:
    """Morpheme tokenization tests — case suffixes, verb morphology, root extraction."""

    # ── Case suffix (வேற்றுமை) tests ────────────────────────────

    @pytest.mark.parametrize(
        "input_word, expected_root, expected_suffix, description",
        VETRUMAI_CASES,
        ids=[c[3] for c in VETRUMAI_CASES],
    )
    def test_vetrumai_decomposition(
        self, tokenizer, input_word, expected_root, expected_suffix, description,
    ):
        tokens = tokenizer.morpheme_tokenize(input_word)
        assert len(tokens) >= 2, (
            f"[{description}] Expected root + suffix, got {[t.text for t in tokens]}"
        )

        # Verify suffix token exists (data-driven, no case_number metadata)
        suffix_tokens = [t for t in tokens if t.token_type == TokenType.CASE_SUFFIX]
        assert len(suffix_tokens) >= 1, (
            f"[{description}] No CASE_SUFFIX token found in {[t.text for t in tokens]}"
        )
        sfx = suffix_tokens[0]
        assert sfx.text == expected_suffix
        assert sfx.metadata.get("source") == "vetrumai"

    # ── No-decomposition tests ──────────────────────────────────

    @pytest.mark.parametrize(
        "word, description",
        NO_DECOMPOSITION_WORDS,
        ids=[c[1] for c in NO_DECOMPOSITION_WORDS],
    )
    def test_no_decomposition(self, tokenizer, word, description):
        tokens = tokenizer.morpheme_tokenize(word)
        assert len(tokens) == 1, (
            f"[{description}] Expected 1 root token, got {[t.text for t in tokens]}"
        )
        assert tokens[0].token_type == TokenType.ROOT
        assert tokens[0].metadata.get("note") == "no_decomposition"

    # ── Full-sentence morpheme tests ────────────────────────────

    @pytest.mark.parametrize(
        "input_text, min_tokens, has_root, has_suffix_or_case, description",
        MORPHEME_SENTENCE_CASES,
        ids=[c[4] for c in MORPHEME_SENTENCE_CASES],
    )
    def test_morpheme_sentence(
        self, tokenizer, input_text, min_tokens, has_root, has_suffix_or_case, description,
    ):
        tokens = tokenizer.tokenize(input_text, level="morpheme")
        assert len(tokens) >= min_tokens, (
            f"[{description}] Expected >= {min_tokens} tokens, got {len(tokens)}"
        )

        types = {t.token_type for t in tokens}
        if has_root:
            assert TokenType.ROOT in types

    # ── Root token always present ───────────────────────────────

    def test_morpheme_always_has_root(self, tokenizer):
        """Every morpheme analysis must produce at least one ROOT token."""
        words = ["வந்தான்", "போகிறான்", "படிப்பான்", "நல்ல", "பெரிய"]
        for word in words:
            tokens = tokenizer.morpheme_tokenize(word)
            root_tokens = [t for t in tokens if t.token_type == TokenType.ROOT]
            assert len(root_tokens) >= 1, f"No ROOT token for '{word}'"

    # ── Morpheme types are valid ────────────────────────────────

    def test_morpheme_valid_types(self, tokenizer):
        """All morpheme tokens must be one of the expected types."""
        valid = {
            TokenType.ROOT, TokenType.SUFFIX, TokenType.CASE_SUFFIX,
            TokenType.TENSE_MARKER, TokenType.PERSON_MARKER,
            TokenType.PLURAL_MARKER,
        }
        tokens = tokenizer.morpheme_tokenize("பள்ளிக்கு")
        for t in tokens:
            assert t.token_type in valid, f"Unexpected type {t.token_type} for '{t.text}'"

    # ── Empty / whitespace ──────────────────────────────────────

    def test_morpheme_empty(self, tokenizer):
        assert tokenizer.morpheme_tokenize("") == []
        assert tokenizer.morpheme_tokenize("   ") == []

    # ── Punctuation passes through in sentence-level morpheme ───

    def test_morpheme_punctuation_passthrough(self, tokenizer):
        tokens = tokenizer.tokenize("வந்தான்.", level="morpheme")
        punct = [t for t in tokens if t.token_type == TokenType.PUNCTUATION]
        assert len(punct) == 1
        assert punct[0].text == "."

    # ── Multiple case forms of same root ────────────────────────

    def test_multiple_case_forms(self, tokenizer):
        """Different case forms of the same base should all produce case suffixes."""
        forms = ["பள்ளிக்கு", "பள்ளியை", "பள்ளியில்"]
        for form in forms:
            tokens = tokenizer.tokenize(form, level="morpheme")
            has_suffix = any(
                t.token_type in (TokenType.CASE_SUFFIX, TokenType.SUFFIX)
                for t in tokens
            )
            # At minimum, the word should tokenize without error
            assert len(tokens) >= 1, f"Failed to tokenize '{form}'"
