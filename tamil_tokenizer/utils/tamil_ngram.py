"""
Tamil N-Gram - Equivalent to TamilNGram.java

This module provides N-gram generation functionality for Tamil text,
supporting both word-level and letter-level N-grams.

Author: Tamil Arasan
Since: Apr 1, 2019
"""

import logging
from typing import List, Set, Optional
from .tamil_iterator import TamilStringIterator

logger = logging.getLogger(__name__)
from ..grammar.tamil_util import TamilUtil


class TamilNGram:
    """
    Generate N-grams for Tamil text at word or letter level.

    Supports:
    - Word N-grams from strings or lists
    - Letter N-grams with Tamil character awareness
    - Unique N-gram sets
    - All possible N-grams for a word
    """

    DELIMITER = " "

    def n_gram_word(self, text: str, gram_size: int,
                    parse_delimiter: str = " ",
                    ignore_delimiter: str = ",") -> List[List[str]]:
        """
        Generate word-level N-grams from text.

        Args:
            text: Input text to process
            gram_size: Size of each N-gram
            parse_delimiter: Delimiter to split words
            ignore_delimiter: Delimiter to ignore (unused in current impl)

        Returns:
            List of word N-grams (each N-gram is a list of words)
        """
        # Split text into words
        str_list = []
        tokens = text.split(parse_delimiter) if parse_delimiter else text.split()
        for token in tokens:
            if token.strip():
                str_list.append(token)

        return self._build_grams_list(str_list, len(str_list), gram_size, ignore_delimiter)

    def n_gram_word_from_list(self, str_list: List[str], gram_size: int,
                              parse_delimiter: str = " ",
                              ignore_delimiter: str = ",") -> List[List[str]]:
        """
        Generate word-level N-grams from a list of words.

        Args:
            str_list: List of words
            gram_size: Size of each N-gram
            parse_delimiter: Delimiter (unused for list input)
            ignore_delimiter: Delimiter to ignore

        Returns:
            List of word N-grams
        """
        return self._build_grams_list(str_list, len(str_list), gram_size, ignore_delimiter)

    def _build_grams_list(self, str_list: List[str], actual_length: int,
                          gram_size: int, ignore_delimiter: str) -> List[List[str]]:
        """
        Build list of N-grams from word list.

        Args:
            str_list: List of words
            actual_length: Length of the list
            gram_size: Size of each N-gram
            ignore_delimiter: Delimiter to ignore

        Returns:
            List of N-grams where each N-gram is a list of words
        """
        new_list = []
        final_ids = 0

        while actual_length >= final_ids:
            internal_list = []
            for index in range(gram_size):
                if final_ids + index < len(str_list):
                    internal_list.append(str_list[final_ids + index])

            new_list.append(internal_list)

            if final_ids + gram_size >= len(str_list):
                break

            final_ids += 1

        return new_list

    def _build_grams(self, str_list: List[str], actual_length: int,
                     gram_size: int) -> List[str]:
        """
        Build letter-level N-grams from character list.

        Args:
            str_list: List of Tamil characters
            actual_length: Length of the list
            gram_size: Size of each N-gram

        Returns:
            List of N-gram strings
        """
        new_list = []
        final_ids = 0

        while actual_length >= final_ids:
            sb = []
            for index in range(gram_size):
                if final_ids + index < len(str_list):
                    sb.append(str_list[final_ids + index])

            # Join and convert back to Tamil
            joined = TamilUtil.எழுத்துகளைசேர்(''.join(sb))
            new_list.append(joined)

            if final_ids + gram_size >= len(str_list):
                break
            if final_ids + gram_size >= gram_size:
                break

            final_ids += gram_size

        return new_list

    def n_gram_letter_with_delimiter(self, text: str, size: int,
                                      result_delimiter: str = "") -> List[str]:
        """
        Generate letter-level N-grams with optional delimiter.

        Args:
            text: Input Tamil text
            size: N-gram size
            result_delimiter: Delimiter for results (unused)

        Returns:
            List of character N-grams
        """
        tsi = TamilStringIterator(text)
        str_list = tsi.forward_iterator()

        if size <= 1:
            return str_list

        return self._build_grams(str_list, tsi.length(), size)

    def n_gram_letter_splitted(self, text: str, size: int) -> List[str]:
        """
        Generate letter N-grams from split Tamil text.

        Args:
            text: Input Tamil text (will be split first)
            size: N-gram size

        Returns:
            List of character N-grams
        """
        splitted = TamilUtil.எழுத்துகளைபிரி(text)
        return self.n_gram_letter(splitted, size)

    def n_gram_letter_unique(self, text: str, size: int) -> Set[str]:
        """
        Generate unique letter-level N-grams.

        Args:
            text: Input Tamil text
            size: N-gram size

        Returns:
            Set of unique character N-grams
        """
        return set(self.n_gram_letter(text, size))

    def n_gram_letter(self, text: str, size: int) -> List[str]:
        """
        Generate letter-level N-grams with all sub-grams.

        Args:
            text: Input Tamil text
            size: N-gram size

        Returns:
            List of character N-grams including all sub-grams
        """
        tsi = TamilStringIterator(text)
        str_list = tsi.forward_iterator()

        if size <= 1:
            return str_list

        n_gram_list = []

        for i in range(size + 1):
            if i > 0:
                n_gram_list.extend(str_list[:i])
            n_gram_list.extend(self._build_grams(str_list[i:], tsi.length(), size))

        return n_gram_list

    def all_possible_letter_ngram(self, word: str) -> List[str]:
        """
        Generate all possible letter N-grams for a word.

        Generates N-grams of all sizes from 1 to word length.

        Args:
            word: Input Tamil word

        Returns:
            List of all possible N-grams
        """
        tsi = TamilStringIterator(word)
        result = []
        length = tsi.length()

        for index in range(1, length + 1):
            result.extend(self.letter_gram(word, index))

        return result

    def letter_gram(self, text: str, size: int) -> List[str]:
        """
        Generate letter N-grams of specified size.

        Args:
            text: Input Tamil text
            size: N-gram size

        Returns:
            List of character N-grams
        """
        return self.n_gram_letter(text, size)

    @staticmethod
    def create_word_gram(text: str, delimiter: str = " ", gram: int = 2) -> List[List[str]]:
        """
        Static method to create word N-grams.

        Args:
            text: Input text
            delimiter: Word delimiter
            gram: N-gram size

        Returns:
            List of word N-grams
        """
        if text is None:
            return []

        ngram = TamilNGram()
        return ngram.n_gram_word(text, gram, delimiter, ",")

    @staticmethod
    def create_word_gram_default(text: str, gram: int = 2) -> List[List[str]]:
        """
        Static method to create word N-grams with default delimiter.

        Args:
            text: Input text
            gram: N-gram size

        Returns:
            List of word N-grams
        """
        if text is None:
            return []

        ngram = TamilNGram()
        return ngram.n_gram_word(text, gram, TamilNGram.DELIMITER, ",")

    @staticmethod
    def create_word_gram_from_list(str_list: List[str], gram: int = 2) -> List[List[str]]:
        """
        Static method to create word N-grams from list.

        Args:
            str_list: List of words
            gram: N-gram size

        Returns:
            List of word N-grams
        """
        ngram = TamilNGram()
        return ngram.n_gram_word_from_list(str_list, gram, TamilNGram.DELIMITER, ",")


def test_letter_gram(text: str, size: int):
    """Test letter N-gram generation."""
    ngram = TamilNGram()
    tamil_list = ngram.n_gram_letter(text, size)
    logger.debug(tamil_list)


def test_word_gram(text: Optional[str], gram: int):
    """Test word N-gram generation."""
    if text is None:
        text = ("வான மழை போலே புது பாடல்கள் கான மழை தூவும் முகில் ஆடல்கள் "
                "நிலைக்கும் கானம் இது நெடுநாள் வாழும் இது")

    list_of_list = TamilNGram.create_word_gram(text, " \r\n", gram)
    for lst in list_of_list:
        logger.debug(lst)


if __name__ == "__main__":
    # Test with sample Tamil words
    word_list = ["பிறவிப்", "பெருங்கடல்", "நீந்துவர்", "நீந்தார்", "இறைவன்", "அடிசேராதார்"]

    for word in word_list:
        split_word = TamilUtil.எழுத்துகளைபிரி(word)
        tsi = TamilStringIterator(split_word)
        length = tsi.length()

        for index in range(1, length + 1):
            test_letter_gram(split_word, index)

    # Test word gram
    test_word_gram(None, 4)
