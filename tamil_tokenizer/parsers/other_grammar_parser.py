"""
Other Grammar Parser - Equivalent to OtherGrammarParser.java

This module provides parsing for miscellaneous grammar patterns.

Author: Tamil Arasan
"""

import logging
from typing import Dict, List, Optional
from .core_parser import CoreParser

logger = logging.getLogger(__name__)
from .word_parser_interface import WordParserInterface
from ..config.constant_table import TamilConstantTable


class OtherGrammarParser(CoreParser, WordParserInterface):
    """
    Parser for miscellaneous grammar patterns.

    Handles words that fall into the "other grammar" ignore list.
    """

    # Class-level shared data
    _parse_map_property: Optional[Dict[str, str]] = None
    _global_list: Optional[List[List[List[str]]]] = None
    _initialized: bool = False

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the other grammar parser.

        Args:
            data_path: Path to data directory
        """
        super().__init__(data_path)

        if not OtherGrammarParser._initialized:
            self._initialize_parser()

    def _initialize_parser(self) -> None:
        """Initialize parser."""
        try:
            OtherGrammarParser._initialized = True
            logger.debug("Other Grammar Parser.")
        except Exception as e:
            logger.error(f"Error initializing OtherGrammarParser: {e}")
            OtherGrammarParser._initialized = True

    def get_parser_type(self) -> str:
        """Get parser type."""
        return "OtherGrammar"

    def get_parse_map_property(self) -> Dict[str, str]:
        """Get parse map properties."""
        return {
            "OG": "மற்றவை",
            "0": "மற்றவை"
        }

    def parse(self, words: List[str], pass_counter: int = 0,
              no_details: bool = False, write_to_file: bool = False,
              word_of_list: Optional[List[str]] = None) -> Dict[str, List[List[str]]]:
        """
        Parse words for other grammar patterns.

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

        if word_of_list is None:
            word_of_list = []

        try:
            for word in words:
                if self.constant_table.is_in_ignore_other_grammar_list(word):
                    if no_details:
                        value = [word.strip(), ":", ":(OG) IgnoreList", ":", word.strip(), f":{word.strip()}"]
                    else:
                        value = [str(pass_counter), ":", ":(OG) IgnoreList", ":", word.strip(), f":{word.strip()}"]

                    if word not in map_of_list:
                        map_of_list[word] = []
                    map_of_list[word].append(value)

                    word_of_list.append(word)
                    # Add empty entries (matching Java behavior)
                    for _ in range(12):
                        word_of_list.append("")

        except Exception as e:
            logger.error(f"Error in OtherGrammarParser.parse: {e}")

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
