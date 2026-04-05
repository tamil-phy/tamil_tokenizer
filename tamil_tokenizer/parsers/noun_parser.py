"""
Noun Parser - Equivalent to NounParser.java

This module provides specialized parsing for Tamil nouns.
It extends TamilRootWordParser with noun-specific rules.

Author: Tamil Arasan
"""

import logging
from typing import Dict, List, Optional
from .root_word_parser import TamilRootWordParser

logger = logging.getLogger(__name__)
from ..config.constant_table import TamilConstantTable
from ..config.constants import ConfigConstants
from ..grammar.tamil_util import TamilUtil


class NounParser(TamilRootWordParser):
    """
    Specialized parser for Tamil nouns.

    Uses noun-specific constant and parse order files.
    """

    # Class-level shared data
    _noun_global_list: Optional[List[List[List[str]]]] = None
    _noun_words: Optional[List[List[str]]] = None
    _noun_list_of_list: Optional[List[List[int]]] = None
    _noun_parse_map_property: Optional[Dict[str, str]] = None
    _noun_parse_order_to_value: Dict[tuple, List[List[str]]] = {}
    _noun_value_to_parse_order: Dict[tuple, tuple] = {}
    _noun_initialized: bool = False

    # Noun residue patterns
    noun_residue_list = [
        "கள்", "ஐ", "கு", "ஆல்", "ஓடு", "ஒடு", "இடம்",
        "உடன்", "இன்", "அது", "ஓட்", "ஒட்", "த்து"
    ]

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the noun parser.

        Args:
            data_path: Path to data directory containing rule files
        """
        super().__init__(data_path)

        # Initialize noun-specific rules if not already done
        if not NounParser._noun_initialized:
            self._initialize_noun_parser()

    def _initialize_noun_parser(self) -> None:
        """Initialize parser with noun-specific rule files"""
        try:
            # Load noun constants, parse order, and parse map
            noun_words, noun_list_of_list, noun_parse_map = \
                self.constant_table.get_parse_and_main_value(
                    ConfigConstants.NOUN_CONSTANT_FILE_NAME,
                    ConfigConstants.NOUN_PARSE_ORDER_FILE_NAME,
                    ConfigConstants.NOUN_PARSE_MAP_FILE_NAME
                )

            NounParser._noun_words = noun_words
            NounParser._noun_list_of_list = noun_list_of_list
            NounParser._noun_parse_map_property = noun_parse_map

            # Set start value (1-based indexing for noun rules)
            self.constant_table.set_start_value(1)

            # Build global list
            NounParser._noun_global_list = self.constant_table.get_main_table(
                noun_words, noun_list_of_list,
                NounParser._noun_parse_order_to_value,
                NounParser._noun_value_to_parse_order
            )

            NounParser._noun_initialized = True
            logger.debug("NounParser loaded.")

        except Exception as e:
            logger.error(f"Error initializing NounParser: {e}")
            # Fall back to main parser rules
            NounParser._noun_initialized = True

    def get_parser_type(self) -> str:
        """Get parser type"""
        return "Noun"

    def get_parse_map_property(self) -> Dict[str, str]:
        """Get noun parse map properties"""
        return NounParser._noun_parse_map_property or super().get_parse_map_property()

    def get_parser_order_to_values(self) -> Dict:
        """Get parser order to values mapping"""
        if NounParser._noun_parse_order_to_value:
            return NounParser._noun_parse_order_to_value
        return super().get_parser_order_to_values()

    def get_value_to_parse_order(self) -> Dict:
        """Get value to parse order mapping"""
        if NounParser._noun_value_to_parse_order:
            return NounParser._noun_value_to_parse_order
        return super().get_value_to_parse_order()

    def get_global_list(self) -> List[List[List[str]]]:
        """Get global suffix list"""
        if NounParser._noun_global_list:
            return NounParser._noun_global_list
        return super().get_global_list()

    def _find_verb_or_noun(self, word2: List[str], check_value: str) -> str:
        """
        Find verb or noun type from split residue.

        Prioritizes noun detection for this parser.

        Args:
            word2: Split word array
            check_value: Value to check

        Returns:
            Type string (V, N, PR, PL, PRE, NA)
        """
        # Check if residue matches noun patterns
        if len(word2) > 1 and word2[1]:
            joined = TamilUtil.எழுத்துகளைசேர்(word2[1])
            if joined in self.noun_residue_list:
                if self.constant_table.is_in_ignore_noun_word_list(check_value):
                    return "N"
                return "NA (N)"

        if self.constant_table.is_in_ignore_noun_word_list(check_value):
            return "N"
        if self.constant_table.is_in_prefix_list(check_value):
            return "PRE"
        if self.constant_table.is_in_ignore_person_list(check_value):
            return "PR"
        if self.constant_table.is_in_ignore_place_list(check_value):
            return "PL"

        return "NA"
