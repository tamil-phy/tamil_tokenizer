"""
Tamil Tokenizer - Standalone multi-level tokenizer for Tamil text.

Provides four levels of tokenization:
- Sentence tokenization
- Word tokenization
- Character (letter) tokenization
- Morpheme tokenization (root word + suffixes)

Usage:
    from tamil_tokenizer import TamilTokenizer, Token, TokenType

    tokenizer = TamilTokenizer()
    tokens = tokenizer.tokenize("அவன் வந்தான்.", level="word")
"""

__version__ = "1.0.0"

from .tokenizer import TamilTokenizer, Token, TokenType

def _import_hf_tokenizer():
    """Lazy import to avoid hard dependency on transformers."""
    from .hf_tokenizer import TamilHFTokenizer
    return TamilHFTokenizer

try:
    from .hf_tokenizer import TamilHFTokenizer
    __all__ = ['TamilTokenizer', 'TamilHFTokenizer', 'Token', 'TokenType']
except ImportError:
    __all__ = ['TamilTokenizer', 'Token', 'TokenType']
