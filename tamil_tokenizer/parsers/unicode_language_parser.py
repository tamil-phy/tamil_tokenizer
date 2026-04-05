"""
Unicode Language Parser - Equivalent to UnicodeLanguageParser.java

This module provides language detection based on Unicode character ranges.

Author: Tamil Arasan
"""

import logging
from typing import Dict, List, Optional, Set, Tuple
from .core_parser import CoreParser

logger = logging.getLogger(__name__)
from .word_parser_interface import WordParserInterface
from ..config.constant_table import TamilConstantTable
from ..config.constants import ConfigConstants
from ..config.config_loader import ReadConfig


class UnicodeLanguageParser(CoreParser, WordParserInterface):
    """
    Parser that detects language based on Unicode ranges.

    Uses a mapping of Unicode ranges to language names to identify
    the language(s) present in a word.
    """

    # Class-level shared data
    _language_map: Dict[Tuple[int, int], str] = {}
    _parse_map_property: Optional[Dict[str, str]] = None
    _initialized: bool = False

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the Unicode language parser.

        Args:
            data_path: Path to data directory
        """
        super().__init__(data_path)

        if not UnicodeLanguageParser._initialized:
            self._initialize_parser()

    def _initialize_parser(self) -> None:
        """Initialize parser with Unicode range mappings."""
        try:
            self._init_language_map()

            UnicodeLanguageParser._parse_map_property = self.constant_table.get_parse_and_main_value_single(
                ConfigConstants.SPECIAL_CHARACTER_FILE_NAME
            )
            UnicodeLanguageParser._initialized = True
            logger.debug("Unicode Parser Loaded.")
        except Exception as e:
            logger.error(f"Error initializing UnicodeLanguageParser: {e}")
            UnicodeLanguageParser._initialized = True

    def _init_language_map(self) -> None:
        """Initialize the Unicode range to language mapping."""
        try:
            config = ReadConfig.get_instance()
            props = config.get_properties()
            current_root = config.get_current_root()

            unicode_file = props.get(ConfigConstants.UNICODE_MAP_FILE_NAME, '')
            if unicode_file:
                # Normalize path and join properly
                unicode_file = unicode_file.replace('\\', '/')
                if unicode_file.startswith('../'):
                    # Extract just the filename
                    parts = unicode_file.split('/')
                    for i, part in enumerate(parts):
                        if part == 'properties' and i + 1 < len(parts):
                            unicode_file = parts[i + 1]
                            break
                    else:
                        unicode_file = parts[-1]
                import os
                unicode_map = config.read_file_as_map(os.path.join(current_root, unicode_file))

                for key, value in unicode_map.items():
                    range_tuple = self._parse_range(key, " — ")
                    if range_tuple:
                        UnicodeLanguageParser._language_map[range_tuple] = value.strip() if value else key
        except Exception as e:
            logger.error(f"Error loading Unicode map: {e}")
            # Set default Tamil range
            UnicodeLanguageParser._language_map[(0x0B80, 0x0BFF)] = "Tamil"
            UnicodeLanguageParser._language_map[(0x0000, 0x007F)] = "Basic Latin"

    @staticmethod
    def _parse_range(range_str: str, delimiter: str) -> Optional[Tuple[int, int]]:
        """
        Parse a Unicode range string.

        Args:
            range_str: Range string (e.g., "0B80 — 0BFF")
            delimiter: Delimiter between start and end

        Returns:
            Tuple of (start, end) integers or None
        """
        try:
            parts = range_str.split(delimiter)
            if len(parts) >= 2:
                begin = int(parts[0].strip(), 16)
                end = int(parts[1].strip(), 16)
                return (begin, end)
        except (ValueError, IndexError):
            pass
        return None

    def find_language(self, word: str) -> Set[str]:
        """
        Find all languages present in a word.

        Args:
            word: Word to analyze

        Returns:
            Set of language names found
        """
        lang_set: Set[str] = set()

        if word is None:
            return lang_set

        for char in word:
            lang = self.which_language(char)
            if lang:
                lang_set.add(lang)

        return lang_set

    def which_language(self, char: str) -> Optional[str]:
        """
        Determine the language of a single character.

        Args:
            char: Character to check

        Returns:
            Language name or None
        """
        code_point = ord(char)

        for (start, end), language in UnicodeLanguageParser._language_map.items():
            if start <= code_point <= end:
                return language

        return None

    def get_parser_type(self) -> str:
        """Get parser type."""
        return "Unicode"

    def get_parse_map_property(self) -> Dict[str, str]:
        """Get parse map properties."""
        return UnicodeLanguageParser._parse_map_property or {}

    def parse(self, words: List[str], pass_counter: int = 0,
              no_details: bool = False, write_to_file: bool = False,
              word_of_list: Optional[List[str]] = None) -> Dict[str, List[List[str]]]:
        """
        Parse words for mixed-language content.

        Words with multiple languages are marked as (NW) - Non-Word.

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
                lang_set = self.find_language(word)

                if len(lang_set) > 1:
                    # Mixed language word
                    if no_details:
                        value = [word.strip(), ":", ":(NW) IgnoreList", ":", word.strip(), f":{word.strip()}"]
                    else:
                        value = [str(pass_counter), ":", ":(NW) IgnoreList", ":", word.strip(), f":{word.strip()}"]

                    if word not in map_of_list:
                        map_of_list[word] = []
                    map_of_list[word].append(value)

        except Exception as e:
            logger.error(f"Error in UnicodeLanguageParser.parse: {e}")

        return map_of_list

    def is_in_noun_list(self, word: str) -> bool:
        """Check if word is in noun list."""
        return False

    def is_in_verb_list(self, word: str) -> bool:
        """Check if word is in verb list."""
        return False

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
    parser = UnicodeLanguageParser()

    # Test cases
    test_words = ["Wordஅ?1", "அம்மா"]

    for word in test_words:
        languages = parser.find_language(word)
        print(f"{word}: {languages}")
