"""
Symbol Parser - Equivalent to SymbolParser.java

This module provides parsing for special characters and symbols in Tamil text.

Author: Tamil Arasan
"""

import logging
import re
from typing import Dict, List, Optional
from .core_parser import CoreParser

logger = logging.getLogger(__name__)
from .word_parser_interface import WordParserInterface
from ..config.constant_table import TamilConstantTable
from ..config.constants import ConfigConstants


class SymbolParser(CoreParser, WordParserInterface):
    """
    Parser for special characters and symbols.

    Removes and processes special characters like .,;!? etc.
    """

    # Pattern for matching special characters
    SPECIAL_CHAR_PATTERN = r'[.,;!"?]*'

    # Class-level shared data
    _parse_map_property: Optional[Dict[str, str]] = None
    _initialized: bool = False

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the symbol parser.

        Args:
            data_path: Path to data directory
        """
        super().__init__(data_path)

        if not SymbolParser._initialized:
            self._initialize_parser()

    def _initialize_parser(self) -> None:
        """Initialize parser with configuration."""
        try:
            SymbolParser._parse_map_property = self.constant_table.get_parse_and_main_value_single(
                ConfigConstants.SPECIAL_CHARACTER_FILE_NAME
            )
            SymbolParser._initialized = True
            logger.debug("Symbol Parser Loaded.")
        except Exception as e:
            logger.error(f"Error initializing SymbolParser: {e}")
            SymbolParser._initialized = True

    def get_parser_type(self) -> str:
        """Get parser type."""
        return "Symbol"

    def get_parse_map_property(self) -> Dict[str, str]:
        """Get parse map properties."""
        return SymbolParser._parse_map_property or {}

    def parse(self, words: List[str], pass_counter: int = 0,
              no_details: bool = False, write_to_file: bool = False,
              word_of_list: Optional[List[str]] = None) -> Dict[str, List[List[str]]]:
        """
        Parse words for symbols.

        Args:
            words: List of words to parse
            pass_counter: Pass counter for tracking
            no_details: Whether to skip detailed output
            write_to_file: Whether to write results to file
            word_of_list: List to collect matched words

        Returns:
            Dictionary mapping words to parse results
        """
        map_of_list: Dict[str, List[List[str]]] = {}

        if words is None:
            words = self.constant_table.get_word_list()

        try:
            for word in words:
                org_word = word
                # Remove special characters
                word = re.sub(self.SPECIAL_CHAR_PATTERN, '', word)

                if word is None or word.strip() == '':
                    # Word was entirely special characters
                    symbol_meaning = self.get_parse_map_property().get(org_word.strip(), org_word)
                    value = [
                        str(pass_counter), ":",
                        ":(Symbol) IgnoreList", ":",
                        symbol_meaning or org_word,
                        ":", f":{symbol_meaning or org_word}"
                    ]
                    map_of_list[org_word.strip()] = [value]

        except Exception as e:
            logger.error(f"Error in SymbolParser.parse: {e}")

        return map_of_list

    def get_parser_order_to_values(self) -> Dict:
        """Get parser order to values mapping."""
        return {}

    def get_value_to_parse_order(self) -> Dict:
        """Get value to parse order mapping."""
        return {}

    def get_global_list(self) -> List[List[List[str]]]:
        """Get global suffix list."""
        return []


if __name__ == "__main__":
    sp = SymbolParser()

    # Test cases
    test_words = ["வின்னர்!", "!", "...", "வின்னர்..."]

    for test in test_words:
        result = sp.parse([test], 0, True, False, None)
        print(f"{test}: {result}")
