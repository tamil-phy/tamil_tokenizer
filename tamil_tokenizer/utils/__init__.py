"""Tamil NLP utilities module."""

from .tamil_iterator import TamilStringIterator
from .recursive_algorithm import RecursiveAlgorithm, cartesian_product, get_all_combinations
from .splitting import SplittingUtil
from .word_class import WordClass, TYPE_CODES, get_type_description
from .tamil_ngram import TamilNGram
from .transliteral import TransliteralConvertor, TransliteralUtil
from .file_io import WriteToFile, ReadFromFile, StringBuilder
from .word_splitter import WordSplitter
from .cleanup import Cleanup
from .ends_with import EndsWith
from .verb_splitter import VerbSplitter
from .tamil_char_ngram_finder import TamilCharNGramWordFinder
from .tamil_word_ngram_writer import TamilWordNGramWriter

__all__ = [
    'TamilStringIterator',
    'RecursiveAlgorithm',
    'cartesian_product',
    'get_all_combinations',
    'SplittingUtil',
    'WordClass',
    'TYPE_CODES',
    'get_type_description',
    'TamilNGram',
    'TransliteralConvertor',
    'TransliteralUtil',
    'WriteToFile',
    'ReadFromFile',
    'StringBuilder',
    'WordSplitter',
    'Cleanup',
    'EndsWith',
    'VerbSplitter',
    'TamilCharNGramWordFinder',
    'TamilWordNGramWriter'
]
