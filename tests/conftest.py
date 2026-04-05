"""Shared fixtures for Tamil Tokenizer test suite."""

import pytest
from tamil_tokenizer import TamilTokenizer, Token, TokenType


@pytest.fixture(scope="session")
def tokenizer():
    """Session-scoped tokenizer instance (reused across all tests)."""
    return TamilTokenizer()
