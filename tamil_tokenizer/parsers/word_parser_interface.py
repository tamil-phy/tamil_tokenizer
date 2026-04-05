"""
Word Parser Interface - Equivalent to WordParserInterface.java

This module defines the interface for all word parsers.

Author: Tamil Arasan
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class WordParserInterface(ABC):
    """
    Interface for Tamil word parsers.

    All parsers must implement these methods for consistent
    word parsing behavior.
    """

    @abstractmethod
    def parse(self, words: List[str], pass_counter: int = 0,
              no_details: bool = False, write_to_file: bool = False,
              word_of_list: Optional[List[str]] = None) -> Dict[str, List[List[str]]]:
        """
        Parse a list of words.

        Args:
            words: List of Tamil words to parse
            pass_counter: Counter for multi-pass parsing
            no_details: If True, return minimal details
            write_to_file: If True, write results to file
            word_of_list: Output list for word components

        Returns:
            Dictionary mapping words to their parse results
        """
        pass

    @abstractmethod
    def get_parser_type(self) -> str:
        """
        Get the type of this parser.

        Returns:
            Parser type string (e.g., "Main", "Verb", "Noun")
        """
        pass

    @abstractmethod
    def get_global_list(self) -> List[List[List[str]]]:
        """
        Get the global suffix combination list.

        Returns:
            3D list of suffix patterns organized by parse rules
        """
        pass

    @abstractmethod
    def get_parse_map_property(self) -> Dict[str, str]:
        """
        Get the parse map properties.

        Returns:
            Dictionary of parse type codes to descriptions
        """
        pass

    @abstractmethod
    def get_parser_order_to_values(self) -> Dict[tuple, List[List[str]]]:
        """
        Get mapping from parse order to suffix values.

        Returns:
            Dictionary mapping parse order tuples to suffix lists
        """
        pass

    @abstractmethod
    def get_value_to_parse_order(self) -> Dict[tuple, tuple]:
        """
        Get mapping from suffix values to parse order.

        Returns:
            Dictionary mapping suffix value tuples to parse order tuples
        """
        pass
