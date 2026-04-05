"""
Twin Word Parser - Equivalent to TwinWordParser.java

This module provides parsing for Tamil twin/reduplication words.

Twin words are words formed by repeating a base word, like
"சலசல" (sound of water), "திக்குத்திக்கு" (in all directions).

Author: Tamil Arasan
"""

import logging
from typing import Dict, List, Optional
from .core_parser import CoreParser

logger = logging.getLogger(__name__)
from .word_parser_interface import WordParserInterface
from ..config.constant_table import TamilConstantTable
from ..config.constants import ConfigConstants
from ..utils.tamil_iterator import TamilStringIterator
from ..utils.word_class import WordClass


class TwinWordParser(CoreParser, WordParserInterface):
    """
    Parser for Tamil twin/reduplication words.

    Detects words that are formed by repeating a base pattern.
    """

    # Class-level shared data
    _global_list: Optional[List[List[List[str]]]] = None
    _twin_words: Optional[List[List[str]]] = None
    _twin_list_of_list: Optional[List[List[int]]] = None
    _twin_parse_map_property: Optional[Dict[str, str]] = None
    _twin_parse_order_to_value: Dict[tuple, List[List[str]]] = {}
    _twin_value_to_parse_order: Dict[tuple, tuple] = {}
    _initialized: bool = False

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the twin word parser.

        Args:
            data_path: Path to data directory
        """
        super().__init__(data_path)

        if not TwinWordParser._initialized:
            self._initialize_parser()

    def _initialize_parser(self) -> None:
        """Initialize parser with twin word rules."""
        try:
            # Load twin word constants
            twin_words, twin_list_of_list, twin_parse_map = \
                self.constant_table.get_parse_and_main_value(
                    ConfigConstants.TWIN_CONSTANT_FILE_NAME,
                    ConfigConstants.TWIN_PARSE_ORDER_FILE_NAME,
                    ConfigConstants.MAIN_PARSE_MAP_FILE_NAME
                )

            TwinWordParser._twin_words = twin_words
            TwinWordParser._twin_list_of_list = twin_list_of_list
            TwinWordParser._twin_parse_map_property = twin_parse_map

            # Build global list
            TwinWordParser._global_list = self.constant_table.get_main_table(
                twin_words, twin_list_of_list,
                TwinWordParser._twin_parse_order_to_value,
                TwinWordParser._twin_value_to_parse_order
            )

            TwinWordParser._initialized = True
            logger.debug("TwinWord Parser Loaded.")
        except Exception as e:
            logger.error(f"Error initializing TwinWordParser: {e}")
            TwinWordParser._initialized = True

    def get_parser_type(self) -> str:
        """Get parser type."""
        return "TwinWord"

    def get_global_list(self) -> List[List[List[str]]]:
        """Get global suffix list."""
        return TwinWordParser._global_list or []

    def get_parse_map_property(self) -> Dict[str, str]:
        """Get parse map properties."""
        return TwinWordParser._twin_parse_map_property or {}

    def get_value_to_parse_order(self) -> Dict:
        """Get value to parse order mapping."""
        return TwinWordParser._twin_value_to_parse_order

    def get_parser_order_to_values(self) -> Dict:
        """Get parser order to values mapping."""
        return TwinWordParser._twin_parse_order_to_value

    def parse(self, words: List[str], pass_counter: int = 0,
              no_details: bool = False, write_to_file: bool = False,
              word_of_list: Optional[List[str]] = None) -> Dict[str, List[List[str]]]:
        """
        Parse words for twin word patterns.

        Args:
            words: List of words to parse
            pass_counter: Pass counter for tracking
            no_details: Whether to skip detailed output
            write_to_file: Whether to write results to file
            word_of_list: List to collect matched words

        Returns:
            Dictionary mapping words to parse results
        """
        # Use base parser implementation
        return super().parse(words, pass_counter, no_details, write_to_file, word_of_list)

    def is_twin_word(self, word: str) -> bool:
        """
        Check if word is a twin word (reduplication).

        A twin word has identical first and second halves.

        Args:
            word: Word to check

        Returns:
            True if word is a twin word
        """
        if word is None:
            return False

        tsi = TamilStringIterator(word)
        length = tsi.length()
        half_length = length // 2

        chars = tsi.forward_iterator()

        first_half = []
        second_half = []

        for i, char in enumerate(chars):
            # Skip middle character for odd-length words
            if length % 2 != 0 and i == half_length:
                continue
            elif i < half_length:
                first_half.append(char)
            else:
                second_half.append(char)

        return ''.join(first_half) == ''.join(second_half)

    def is_twin_word_pair(self, word1: str, word2: str) -> bool:
        """
        Check if two words form a twin pair.

        Args:
            word1: First word
            word2: Second word

        Returns:
            True if words are equal or form a twin when combined
        """
        if word1 == word2:
            return True

        wc_list = self.get_twin_word(word1 + word2)
        for wc in wc_list:
            if wc.get_type() == "Twin":
                return True

        return False

    def get_twin_word(self, word: str) -> List[WordClass]:
        """
        Get twin word analysis.

        Args:
            word: Word to analyze

        Returns:
            List of WordClass results with twin analysis
        """
        wc_list: List[WordClass] = []
        word_of_list: List[str] = []

        result_map = self.parse([word], 0, False, False, word_of_list)
        check_value_arr_list = result_map.get(word, [])

        at_least_one_twin = False

        for str_arr in check_value_arr_list:
            word_of_list = list(str_arr)

            if self.is_twin_word(str_arr[0]):
                map_parse_vals = {"Type": "Twin"}
                wc = WordClass(
                    pass_count=0,
                    word=word,
                    suffix=None,
                    type_val=None,
                    map_vals=map_parse_vals,
                    raw_split_list=[word_of_list]
                )
                at_least_one_twin = True
                wc_list.append(wc)
            else:
                if not at_least_one_twin:
                    map_parse_vals = {"Type": "NA"}
                    wc = WordClass(
                        pass_count=0,
                        word=word,
                        suffix=None,
                        type_val=None,
                        map_vals=map_parse_vals,
                        raw_split_list=[word_of_list]
                    )
                    wc_list.append(wc)

        return wc_list

    def create_single_instance(self, word: str,
                               deep_search: bool = False) -> List[WordClass]:
        """
        Create word class instances for a word.

        Args:
            word: Word to parse
            deep_search: Whether to perform deep search

        Returns:
            List of WordClass results
        """
        wc_list: List[WordClass] = []

        is_twin = self.is_twin_word(word)

        if is_twin:
            map_parse_vals = {"Type": "Twin"}
            wc = WordClass(
                pass_count=0,
                word=word,
                suffix=None,
                type_val="Twin",
                map_vals=map_parse_vals,
                raw_split_list=None
            )
            wc_list.append(wc)
            return wc_list
        else:
            return self.get_twin_word(word)


if __name__ == "__main__":
    twp = TwinWordParser()

    # Test cases
    wc_list = twp.create_single_instance("எதிர் எதிராக")
    for wc in wc_list:
        logger.debug(f"{wc.get_word()}:{wc.get_type()}:{wc.get_raw_split_list()}")

    # Test twin word detection
    logger.debug(f"திக்குத்திக்கு is twin: {twp.is_twin_word('திக்குத்திக்கு')}")
    logger.debug(f"பக்குப்பக்கு is twin: {twp.is_twin_word('பக்குப்பக்கு')}")
