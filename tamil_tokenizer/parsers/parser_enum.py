"""
Parser Enum - Equivalent to ParserEnum.java

This module defines the enumeration of available parser types.

Author: Tamil Arasan
"""

from enum import Enum, auto


class ParserEnum(Enum):
    """
    Enumeration of parser types available in the NLP system.

    Each parser type handles a specific aspect of Tamil text processing.
    """

    # Symbol parser - handles special characters
    SymbolParser = auto()

    # Verb parser - handles Tamil verb morphology
    VerbParser = auto()

    # Noun parser - handles Tamil noun morphology
    NounParser = auto()

    # Unicode language parser - detects language from Unicode ranges
    UnicodeLanguageParser = auto()

    # Number parser - handles numeric values
    NumberParser = auto()

    # Core parser - base parser functionality
    CoreParser = auto()

    # Twin word parser - handles reduplication patterns
    TwinWordParser = auto()

    # Other grammar parser - handles miscellaneous grammar
    OtherGrammarParser = auto()


# String mapping for backward compatibility
PARSER_TYPE_NAMES = {
    ParserEnum.SymbolParser: "Symbol",
    ParserEnum.VerbParser: "Verb",
    ParserEnum.NounParser: "Noun",
    ParserEnum.UnicodeLanguageParser: "Unicode",
    ParserEnum.NumberParser: "Number",
    ParserEnum.CoreParser: "Core",
    ParserEnum.TwinWordParser: "TwinWord",
    ParserEnum.OtherGrammarParser: "OtherGrammar",
}


def get_parser_name(parser_type: ParserEnum) -> str:
    """
    Get the string name for a parser type.

    Args:
        parser_type: Parser enum value

    Returns:
        String name of the parser
    """
    return PARSER_TYPE_NAMES.get(parser_type, "Unknown")
