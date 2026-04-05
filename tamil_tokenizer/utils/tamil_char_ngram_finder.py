"""
Tamil Character N-Gram Word Finder - Equivalent to TamilCharNGramWordFinder.java

This module finds words within a given Tamil text using N-gram analysis
and dictionary lookups.

Author: Tamil Arasan
"""

import logging
from typing import List, Set, Optional
from .tamil_ngram import TamilNGram

logger = logging.getLogger(__name__)
from .tamil_iterator import TamilStringIterator
from .file_io import ReadFromFile, WriteToFile
from ..grammar.tamil_util import TamilUtil
from ..constants.tamil_letters import TamilConstants


class TamilCharNGramWordFinder:
    """
    Find valid Tamil words within text using N-gram analysis.

    Uses dictionary lookups (verbs, nouns, persons, places) to
    identify valid Tamil words from N-gram candidates.
    """

    def __init__(self, constant_table=None):
        """
        Initialize the word finder.

        Args:
            constant_table: Optional TamilConstantTable instance
        """
        self._tct = constant_table
        if self._tct is None:
            try:
                from ..config.constant_table import TamilConstantTable
                self._tct = TamilConstantTable.get_instance()
            except Exception as e:
                logger.error(f"Error initializing TamilConstantTable: {e}")

    def write_found_words(self, read_file: str, write_file: str,
                          empty_file: str = None) -> None:
        """
        Process a file and write found words.

        Args:
            read_file: Input file path
            write_file: Output file for found words
            empty_file: Output file for words with no matches (optional)
        """
        word_list = self.read_file(read_file)

        for word in word_list:
            final_set = self.word_finder(word)
            if final_set:
                WriteToFile.write_to_file(final_set, write_file)

    def word_finder(self, word: str) -> Set[str]:
        """
        Find valid words from N-gram candidates.

        Args:
            word: Input word to analyze

        Returns:
            Set of found valid words with type prefixes
        """
        ngram = TamilNGram()
        final_list: Set[str] = set()
        possible_list = ngram.all_possible_letter_ngram(word)

        for candidate in possible_list:
            if candidate in final_list:
                continue

            found_flag = False
            word_type = None
            result_str = candidate

            # Check verb list
            if self._tct and self._tct.is_in_ignore_verb_word_list(candidate):
                found_flag = True
                word_type = "Verb"
                result_str = f"V:{candidate}"

            # Check noun list
            if not found_flag and self._tct:
                if self._tct.is_in_ignore_noun_word_list(candidate):
                    found_flag = True
                    word_type = "Noun"
                    result_str = f"N:{candidate}"
                else:
                    # Try modifying ending
                    try:
                        temp_str = self.end_with_certain_values(candidate)
                        if temp_str and self._tct.is_in_ignore_noun_word_list(temp_str):
                            found_flag = True
                            result_str = f"E:{temp_str}"
                    except Exception as e:
                        logger.debug(f"{word}:{candidate}")

            # Check person list
            if not found_flag and self._tct:
                if self._tct.is_in_ignore_person_list(candidate):
                    found_flag = True
                    word_type = "Person"
                    result_str = f"P:{candidate}"

            # Check place list
            if not found_flag and self._tct:
                if self._tct.is_in_ignore_place_list(candidate):
                    found_flag = True
                    word_type = "Place"
                    result_str = f"L:{candidate}"

            # Check ignore list
            if not found_flag and self._tct:
                if self._tct.is_in_ignore_word_list(candidate):
                    found_flag = True
                    result_str = f"I:{candidate}"

            if found_flag:
                # Check ending pattern
                ends_with_consonant = TamilUtil.ஒற்றில்_முடிகிறதா(result_str)
                if not ends_with_consonant:
                    final_list.add(result_str)

        return final_list

    def end_with_certain_values(self, org_word: str) -> Optional[str]:
        """
        Modify word ending to find root form.

        Handles various Tamil word ending patterns.

        Args:
            org_word: Original word

        Returns:
            Modified word or None
        """
        word = TamilUtil.எழுத்துகளைபிரி(org_word)
        modified_word = None

        tsi = TamilStringIterator(org_word)
        chars = tsi.forward_iterator()
        last_value = chars[-1] if chars else ""

        # Check vallinam endings
        if TamilUtil.exist_in_check_list(last_value, TamilConstants.VALLINAM_MEY_V_TO_RR):
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + chr(TamilConstants.உ))

        elif word.endswith("அ"):
            # Check if verb
            if self._tct and self._tct.is_in_ignore_verb_word_list(word):
                return word

            # Try adding ம்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + TamilConstants.ம்)
            if self._tct and self._tct.is_in_ignore_noun_word_list(modified_word):
                return modified_word

            # Try adding ர்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + TamilConstants.ர்)
            if self._tct and self._tct.is_in_ignore_noun_word_list(modified_word):
                return modified_word

            # Try adding ன்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + TamilConstants.ன்)
            if self._tct and self._tct.is_in_ignore_noun_word_list(modified_word):
                return modified_word

            return None

        elif word.endswith(TamilConstants.ஞ்):
            # Replace ஞ் with ம்
            word = word[:word.rfind(TamilConstants.ஞ்)] + TamilConstants.ம்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word)

        elif word.endswith(TamilConstants.ங்):
            # Replace ங் with ம்
            word = word[:word.rfind(TamilConstants.ங்)] + TamilConstants.ம்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word)

        return modified_word

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


if __name__ == "__main__":
    finder = TamilCharNGramWordFinder()

    # Test with sample words
    word_list = ["பிறவிப்", "பெருங்கடல்", "நீந்துவர்", "நீந்தார்", "இறைவன்", "அடிசேரா", "தார்"]

    final_set: Set[str] = set()

    # Process split words
    for word in word_list:
        split_word = TamilUtil.எழுத்துகளைபிரி(word)
        final_set.update(finder.word_finder(split_word))

    # Process original words
    for word in word_list:
        final_set.update(finder.word_finder(word))

    logger.debug(final_set)
