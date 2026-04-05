"""
Cleanup Utilities - Equivalent to Cleanup.java

This module provides utilities for cleaning up and processing
Tamil word lists, including duplicate removal and N-gram analysis.

Author: Tamil Arasan
"""

import logging
from typing import Dict, List, Set, Collection
from .tamil_iterator import TamilStringIterator

logger = logging.getLogger(__name__)
from .file_io import ReadFromFile, WriteToFile


class Cleanup:
    """
    Utility class for cleaning up Tamil word lists.

    Provides functionality for:
    - Loading N-character lists
    - Finding first N characters of words
    - Removing duplicates
    - N-gram based word analysis
    """

    # Class-level character maps
    char1_map: Dict[str, str] = {}
    char2_map: Dict[str, str] = {}
    char3_map: Dict[str, str] = {}
    char4_map: Dict[str, str] = {}
    char5_map: Dict[str, str] = {}

    @classmethod
    def load_n_char_list(cls, str_list: List[str], n: int) -> None:
        """
        Load N-character prefixes from word list into character maps.

        Args:
            str_list: List of words
            n: Character length to extract
        """
        for word in str_list:
            tsi = TamilStringIterator(word.strip())
            chars = tsi.forward_iterator()

            if len(chars) == n:
                key = ''.join(chars[:n])
                if n == 1:
                    cls.char1_map[key] = key
                elif n == 2:
                    cls.char2_map[key] = key
                elif n == 3:
                    cls.char3_map[key] = key
                elif n == 4:
                    cls.char4_map[key] = key
                elif n == 5:
                    cls.char5_map[key] = key

    @classmethod
    def load_all_n_char_lists(cls, str_list: List[str]) -> None:
        """
        Load all N-character lists (1-5) from word list.

        Args:
            str_list: List of words
        """
        cls.load_n_char_list(str_list, 1)
        cls.load_n_char_list(str_list, 2)
        cls.load_n_char_list(str_list, 3)
        cls.load_n_char_list(str_list, 4)
        cls.load_n_char_list(str_list, 5)

    @classmethod
    def first_n_chars(cls, word: str, n: int) -> str:
        """
        Get first N Tamil characters from a word.

        Args:
            word: Input word
            n: Number of characters

        Returns:
            First N Tamil characters
        """
        tsi = TamilStringIterator(word.strip())
        chars = tsi.forward_iterator()

        if len(chars) >= n:
            return ''.join(chars[:n])
        return ''

    @staticmethod
    def cleanup(input_file: str, output_file: str) -> None:
        """
        Clean up a word list file.

        Processes each word using Tamil iterator for proper character handling.

        Args:
            input_file: Input file path
            output_file: Output file path
        """
        rff = ReadFromFile()
        str_list = rff.read_file_as_list(input_file)

        new_set: Set[str] = set()

        for word in str_list:
            tsi = TamilStringIterator(word.strip())
            _ = tsi.forward_iterator()  # Process through iterator
            new_set.add(word.strip())

        WriteToFile.write_to_file(
            Cleanup._build_string(new_set),
            output_file
        )

    @classmethod
    def ngram_write(cls, input_file: str, output_file: str) -> None:
        """
        Write N-gram analysis for words.

        For each word, writes the word along with its 1-5 character prefix matches.

        Args:
            input_file: Input file path
            output_file: Output file path
        """
        rff = ReadFromFile()
        str_list = rff.read_file_as_list(input_file)

        cls.load_all_n_char_lists(str_list)

        new_set: Set[str] = set()

        for word in str_list:
            word = word.strip()
            parts = [
                word,
                cls.char1_map.get(cls.first_n_chars(word, 1), ''),
                cls.char2_map.get(cls.first_n_chars(word, 2), ''),
                cls.char3_map.get(cls.first_n_chars(word, 3), ''),
                cls.char4_map.get(cls.first_n_chars(word, 4), ''),
                cls.char5_map.get(cls.first_n_chars(word, 5), '')
            ]
            new_set.add(':'.join(parts))

        WriteToFile.write_to_file(
            Cleanup._build_string(new_set),
            output_file
        )

    @staticmethod
    def remove_duplicates(input_file: str, output_file: str) -> None:
        """
        Remove duplicate entries from a file.

        Args:
            input_file: Input file path
            output_file: Output file path
        """
        rff = ReadFromFile()
        str_list = rff.read_file_as_list(input_file)

        str_set: Set[str] = set(str_list)

        WriteToFile.write_to_file(
            Cleanup._build_string(str_set),
            output_file
        )
        logger.debug("Done.")

    @staticmethod
    def find_duplicates(file1: str, file2: str,
                        unique_output: str, duplicate_output: str) -> None:
        """
        Find duplicates between two files.

        Args:
            file1: First input file
            file2: Second input file
            unique_output: File for unique entries
            duplicate_output: File for duplicate entries
        """
        rff = ReadFromFile()
        str_list1 = rff.read_file_as_list(file1)
        str_list2 = rff.read_file_as_list(file2)

        set1 = set(s.strip() for s in str_list1)

        final_list: List[str] = []
        dup_list: List[str] = []

        for word in str_list2:
            word = word.strip()
            if word in set1:
                dup_list.append(word)
            else:
                final_list.append(word)

        WriteToFile.write_to_file(
            Cleanup._build_string(final_list),
            unique_output
        )
        WriteToFile.write_to_file(
            Cleanup._build_string(dup_list),
            duplicate_output
        )

    @staticmethod
    def _build_string(collection: Collection[str]) -> str:
        """
        Build newline-separated string from collection.

        Args:
            collection: Collection of strings

        Returns:
            Newline-separated string
        """
        return '\n'.join(collection) + '\n' if collection else ''


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        Cleanup.remove_duplicates(sys.argv[1], sys.argv[2])
