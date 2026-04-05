"""Tamil tokenizer parsers module."""

from .word_parser_interface import WordParserInterface
from .core_parser import CoreParser
from .root_word_parser import TamilRootWordParser

__all__ = [
    'WordParserInterface',
    'CoreParser',
    'TamilRootWordParser',
]
