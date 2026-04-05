"""
Verb Parser - Equivalent to VerbParser.java

This module provides specialized parsing for Tamil verbs.
It extends TamilRootWordParser with verb-specific rules.

Author: Tamil Arasan
"""

import logging
from typing import Dict, List, Optional
from .root_word_parser import TamilRootWordParser

logger = logging.getLogger(__name__)
from ..config.constant_table import TamilConstantTable
from ..config.constants import ConfigConstants
from ..grammar.tamil_util import TamilUtil


class VerbParser(TamilRootWordParser):
    """
    Specialized parser for Tamil verbs.

    Uses verb-specific constant and parse order files.
    """

    # Class-level shared data
    _verb_global_list: Optional[List[List[List[str]]]] = None
    _verb_words: Optional[List[List[str]]] = None
    _verb_list_of_list: Optional[List[List[int]]] = None
    _verb_parse_map_property: Optional[Dict[str, str]] = None
    _verb_parse_order_to_value: Dict[tuple, List[List[str]]] = {}
    _verb_value_to_parse_order: Dict[tuple, tuple] = {}
    _verb_initialized: bool = False

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the verb parser.

        Args:
            data_path: Path to data directory containing rule files
        """
        super().__init__(data_path)

        # Initialize verb-specific rules if not already done
        if not VerbParser._verb_initialized:
            self._initialize_verb_parser()

    def _initialize_verb_parser(self) -> None:
        """Initialize parser with verb-specific rule files"""
        try:
            # Load verb constants, parse order, and parse map
            verb_words, verb_list_of_list, verb_parse_map = \
                self.constant_table.get_parse_and_main_value(
                    ConfigConstants.VERB_CONSTANT_FILE_NAME,
                    ConfigConstants.VERB_PARSE_ORDER_FILE_NAME,
                    ConfigConstants.VERB_PARSE_MAP_FILE_NAME
                )

            VerbParser._verb_words = verb_words
            VerbParser._verb_list_of_list = verb_list_of_list
            VerbParser._verb_parse_map_property = verb_parse_map

            # Set start value (1-based indexing for verb rules)
            self.constant_table.set_start_value(1)

            # Build global list
            VerbParser._verb_global_list = self.constant_table.get_main_table(
                verb_words, verb_list_of_list,
                VerbParser._verb_parse_order_to_value,
                VerbParser._verb_value_to_parse_order
            )

            VerbParser._verb_initialized = True
            logger.debug("VerbParser loaded.")

        except Exception as e:
            logger.error(f"Error initializing VerbParser: {e}")
            # Fall back to main parser rules
            VerbParser._verb_initialized = True

    def get_parser_type(self) -> str:
        """Get parser type"""
        return "Verb"

    def get_parse_map_property(self) -> Dict[str, str]:
        """Get verb parse map properties"""
        return VerbParser._verb_parse_map_property or super().get_parse_map_property()

    def get_parser_order_to_values(self) -> Dict:
        """Get parser order to values mapping"""
        if VerbParser._verb_parse_order_to_value:
            return VerbParser._verb_parse_order_to_value
        return super().get_parser_order_to_values()

    def get_value_to_parse_order(self) -> Dict:
        """Get value to parse order mapping"""
        if VerbParser._verb_value_to_parse_order:
            return VerbParser._verb_value_to_parse_order
        return super().get_value_to_parse_order()

    def get_global_list(self) -> List[List[List[str]]]:
        """Get global suffix list"""
        if VerbParser._verb_global_list:
            return VerbParser._verb_global_list
        return super().get_global_list()

    def _find_verb_or_noun(self, word2: List[str], check_value: str) -> str:
        """
        Find verb or noun type from split residue.

        Prioritizes verb detection for this parser.

        Args:
            word2: Split word array
            check_value: Value to check

        Returns:
            Type string (V, N, PR, PL, PRE, NA)
        """
        if self.constant_table.is_in_ignore_verb_word_list(check_value):
            return "V"
        if self.constant_table.is_in_prefix_list(check_value):
            return "PRE"
        if self.constant_table.is_in_ignore_person_list(check_value):
            return "PR"
        if self.constant_table.is_in_ignore_place_list(check_value):
            return "PL"

        return "NA"
