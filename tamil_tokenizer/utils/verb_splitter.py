"""
Verb Splitter - Equivalent to VerbSplitter.java

This module provides utilities for splitting Tamil verbs
to extract root forms based on verb suffix patterns.

Verb suffix patterns are loaded from mainConstant.list via TamilConstantTable.

Author: Tamil Arasan
"""

import logging
from typing import List, Optional
from .file_io import ReadFromFile, WriteToFile

logger = logging.getLogger(__name__)
from ..config.constant_table import TamilConstantTable


class VerbSplitter:
    """
    Utility for extracting verb roots from Tamil verbs.

    Uses pattern matching on verb suffixes loaded from mainConstant.list
    to identify and extract the root form.
    """

    def __init__(self):
        """Initialize the verb splitter with patterns from TamilConstantTable."""
        self.patterns = self._load_verb_patterns()

    def _load_verb_patterns(self) -> List[str]:
        """Load verb suffix patterns from TamilConstantTable (mainConstant.list)"""
        try:
            from ..config.constants import ConfigConstants

            ct = TamilConstantTable.get_instance()

            # Load main_words from the constant table
            main_words, _, _ = ct.get_parse_and_main_value(
                ConfigConstants.MAIN_CONSTANT_FILE_NAME,
                ConfigConstants.PARSE_ORDER_FILE_NAME,
                ConfigConstants.MAIN_PARSE_MAP_FILE_NAME
            )

            patterns = []
            if main_words:
                # Line 1 (index 0): Present tense markers
                # க்கின்ற்,கின்ற்,க்கிற்,கிற்,ப்ப்,ப்,ந்த்,இன்,இ,ட்,ஈ,ஊ,குவ்
                if len(main_words) > 0:
                    patterns.extend(main_words[0])

                # Line 3 (index 2): Person/number endings
                # ஓன்,ஏன்,ஓம்,ஆய்,ஈர்கள்,ஈர்,ஆள்,ஆர்,ஆர்கள்,அது,அத்,அன்,அள்,அர்,ஏம்
                if len(main_words) > 2:
                    patterns.extend(main_words[2])

            return patterns if patterns else []
        except Exception as e:
            logger.error(f"Error loading verb patterns: {e}")
            return []

    def verb_splitter(self, word: str) -> Optional[str]:
        """
        Split a verb to extract its root.

        Searches for known verb suffixes and returns the root form.

        Args:
            word: Tamil verb to split

        Returns:
            String in format "word:root" or None if no pattern matched
        """
        for pattern in self.patterns:
            if pattern in word:
                root = word.replace(pattern, "")
                return f"{word}:{root}"
        return None

    def read_file(self, file_name: str) -> List[str]:
        """
        Read words from file.

        Args:
            file_name: Input file path

        Returns:
            List of words
        """
        rff = ReadFromFile()
        return rff.read_file_as_list(file_name)

    def write_file(self, str_list: List[str], file_name: str) -> None:
        """
        Write results to file.

        Args:
            str_list: List of results
            file_name: Output file path
        """
        WriteToFile.write_to_file(str_list, file_name)

    def find_verb(self, read_file_name: str, write_file_name: str) -> None:
        """
        Process file to find and extract verb roots.

        Reads words from input file, extracts verb roots,
        and writes results to output file.

        Args:
            read_file_name: Input file path
            write_file_name: Output file path
        """
        str_list = self.read_file(read_file_name)
        final_list = []

        for word in str_list:
            result = self.verb_splitter(word)
            if result is not None:
                final_list.append(result)

        if final_list:
            self.write_file(final_list, write_file_name)


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        vs = VerbSplitter()
        vs.find_verb(sys.argv[1], sys.argv[2])
