"""
Number Parser - Equivalent to NumberParser.java

This module provides parsing for numeric values in Tamil text.

Author: Tamil Arasan
"""

import logging
from typing import Dict, List, Optional
from .core_parser import CoreParser

logger = logging.getLogger(__name__)
from .word_parser_interface import WordParserInterface
from ..config.constant_table import TamilConstantTable
from ..config.constants import ConfigConstants


class NumberParser(CoreParser, WordParserInterface):
    """
    Parser for numeric values in Tamil text.

    Identifies and marks numeric tokens (including alphanumeric values).
    """

    # Class-level shared data
    _parse_map_property: Optional[Dict[str, str]] = None
    _global_list: Optional[List[List[List[str]]]] = None
    _initialized: bool = False

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the number parser.

        Args:
            data_path: Path to data directory
        """
        super().__init__(data_path)

        if not NumberParser._initialized:
            self._initialize_parser()

    def _initialize_parser(self) -> None:
        """Initialize parser with configuration."""
        try:
            NumberParser._parse_map_property = self.constant_table.get_parse_and_main_value_single(
                ConfigConstants.SPECIAL_CHARACTER_FILE_NAME
            )
            NumberParser._initialized = True
            logger.debug("Number Parser Loaded.")
        except Exception as e:
            logger.error(f"Error initializing NumberParser: {e}")
            NumberParser._initialized = True

    def get_parser_type(self) -> str:
        """Get parser type."""
        return "Number"

    def get_parse_map_property(self) -> Dict[str, str]:
        """Get parse map properties."""
        return NumberParser._parse_map_property or {}

    def parse(self, words: List[str], pass_counter: int = 0,
              no_details: bool = False, write_to_file: bool = False,
              word_of_list: Optional[List[str]] = None) -> Dict[str, List[List[str]]]:
        """
        Parse words for numeric values.

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

        try:
            for word in words:
                word = word.strip()
                if not word:
                    continue

                # Check if word is numeric or contains digits
                is_numeric = word.isdigit()
                has_alphanumeric = any(c.isdigit() for c in word)

                if is_numeric or has_alphanumeric:
                    if no_details:
                        value = [word, ":", ":(NU) IgnoreList", ":", word, f":{word}"]
                        value[0] = word
                    else:
                        value = [str(pass_counter), ":", ":(NU) IgnoreList", ":", word, f":{word}"]

                    if word not in map_of_list:
                        map_of_list[word] = []
                    map_of_list[word].append(value)

        except Exception as e:
            logger.error(f"Error in NumberParser.parse: {e}")

        return map_of_list

    def get_global_list(self) -> List[List[List[str]]]:
        """Get global suffix list."""
        return NumberParser._global_list or []

    def get_parser_order_to_values(self) -> Dict:
        """Get parser order to values mapping."""
        return {}

    def get_value_to_parse_order(self) -> Dict:
        """Get value to parse order mapping."""
        return {}
