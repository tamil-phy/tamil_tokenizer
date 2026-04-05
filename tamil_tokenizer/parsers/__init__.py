"""Tamil NLP parsers module."""

from .word_parser_interface import WordParserInterface
from .core_parser import CoreParser
from .root_word_parser import TamilRootWordParser
from .verb_parser import VerbParser
from .noun_parser import NounParser
from .number_parser import NumberParser
from .symbol_parser import SymbolParser
from .unicode_language_parser import UnicodeLanguageParser
from .other_grammar_parser import OtherGrammarParser
from .twin_word_parser import TwinWordParser
from .morphology_parser import MorphologyParser
from .parser_enum import ParserEnum, get_parser_name

__all__ = [
    'WordParserInterface',
    'CoreParser',
    'TamilRootWordParser',
    'VerbParser',
    'NounParser',
    'NumberParser',
    'SymbolParser',
    'UnicodeLanguageParser',
    'OtherGrammarParser',
    'TwinWordParser',
    'MorphologyParser',
    'ParserEnum',
    'get_parser_name'
]
