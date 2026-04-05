"""
Word Splitter - Equivalent to WordSplitter.java

This module provides utilities for splitting text into words,
handling special characters and Tamil text properly.

Author: Tamil Arasan
Since: May 31, 2019
"""

import logging
import re
from typing import List

logger = logging.getLogger(__name__)


class WordSplitter:
    """
    Utility for splitting text into individual words.

    Handles special characters, punctuation, and Tamil-specific patterns.
    """

    # Patterns for special characters
    ALL_SPECIAL_CHARS = r'(?=[, . ! " " , ; : \- \( \) \s " ?.@]+)'
    ALL_SPECIAL_CHARS_EXCEPT_DOT = r'(?=[, ! " " , ; : \- \( \) \s " ? @]+)'

    def __init__(self):
        """Initialize the word splitter."""
        self._numeric_pattern = re.compile(r'\d+(,\d+)*(\.\d+)?')

    def is_numeric(self, text: str) -> bool:
        """
        Check if text is numeric.

        Args:
            text: Text to check

        Returns:
            True if text matches numeric pattern
        """
        if text is None:
            return False
        return bool(self._numeric_pattern.fullmatch(text))

    def split_words(self, text: str) -> List[str]:
        """
        Split text into words.

        Handles numeric values specially and processes each token
        for special characters.

        Args:
            text: Input text

        Returns:
            List of words
        """
        word_list = []
        tokens = text.split()

        for token in tokens:
            if self.is_numeric(token):
                word_list.append(token)
            else:
                sub_words = self.split_words_detail(token)
                if sub_words:
                    word_list.extend(sub_words)

        return word_list

    def split_words_detail(self, text: str) -> List[str]:
        """
        Detailed word splitting with special character handling.

        Args:
            text: Text to split

        Returns:
            List of words/tokens
        """
        # Choose parser based on whether text ends with '.' and contains '.'
        if not text.endswith('.') and '.' in text:
            parser = self.ALL_SPECIAL_CHARS_EXCEPT_DOT
        else:
            parser = self.ALL_SPECIAL_CHARS

        # Split using the pattern
        try:
            arr_of_str = re.split(parser, text)
        except re.error:
            arr_of_str = [text]

        word_list = []

        for arr in arr_of_str:
            if arr != '(' and '(' in arr:
                arr = arr.replace('(', '( ')
            elif arr != '"' and '"' in arr:
                arr = arr.replace('"', '" ')

            # Further split with delimiters
            temp_arr = self.split_with_delimiters(arr.strip(), parser)
            for temp_str in temp_arr:
                if temp_str.strip():
                    word_list.append(temp_str.strip())

        return word_list

    def split_with_delimiters(self, text: str, regex: str) -> List[str]:
        """
        Split text while keeping delimiters as separate entries.

        Args:
            text: Text to split
            regex: Regular expression pattern

        Returns:
            List of parts including delimiters
        """
        parts = []

        try:
            pattern = re.compile(regex)
            last_end = 0

            for match in pattern.finditer(text):
                start = match.start()

                if last_end != start:
                    non_delim = text[last_end:start]
                    parts.append(non_delim)

                delim = match.group()
                parts.append(delim)

                last_end = match.end()

            if last_end != len(text):
                non_delim = text[last_end:]
                parts.append(non_delim)

        except re.error:
            parts = [text]

        return parts

    @staticmethod
    def to_char_array(value: str) -> List[str]:
        """
        Convert string to character array.

        Args:
            value: Input string

        Returns:
            List of characters
        """
        return list(value)

    @staticmethod
    def to_char_array_unicode(text: str) -> None:
        """
        Print Unicode code points for each character.

        Args:
            text: Input string
        """
        i = 0
        while i < len(text):
            ch = ord(text[i])
            char_count = 1 if ch < 0x10000 else 2
            logger.debug(f"{i + char_count}:{ch}:{char_count}")
            i += char_count


def read_file_as_string(file_name: str) -> str:
    """
    Read entire file as string.

    Args:
        file_name: Path to file

    Returns:
        File contents as string
    """
    result = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                result.append(line.rstrip('\n'))
    except IOError as e:
        logger.error(f"Error reading file: {e}")

    return ''.join(result)


if __name__ == "__main__":
    splitter = WordSplitter()

    # Test with sample text
    test_text = "புதிதாக 5,595 பேருக்கு ..."
    words = splitter.split_words(test_text)

    for word in words:
        logger.debug(word)
