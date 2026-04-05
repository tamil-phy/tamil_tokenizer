"""
Tamil Root Word Parser - Equivalent to TamilRootWordParser.java

This module provides the main Tamil word parser that extracts root words
from inflected Tamil words using suffix pattern matching.

Author: Tamil Arasan, Kamatchi (Original Java)
Since: Oct 21, 2017
"""

import logging
import os
import re
from typing import Dict, List, Optional, Tuple, Any, Set
from collections import OrderedDict
from pathlib import Path

logger = logging.getLogger(__name__)
import copy

from ..grammar.tamil_util import TamilUtil
from ..constants.tamil_letters import TamilConstants as TC
from ..utils.tamil_iterator import TamilStringIterator
from ..utils.recursive_algorithm import RecursiveAlgorithm
from ..utils.splitting import SplittingUtil
from ..utils.word_class import WordClass
from ..config.constant_table import TamilConstantTable
from ..config.constants import ConfigConstants
from .core_parser import CoreParser


class TamilRootWordParser(CoreParser):
    """
    Main Tamil word parser for extracting root words.

    Uses suffix pattern matching with parse order rules to identify
    and strip grammatical suffixes from Tamil words.
    """

    # Class-level shared data
    _global_list: Optional[List[List[List[str]]]] = None
    _main_words: Optional[List[List[str]]] = None
    _main_list_of_list: Optional[List[List[int]]] = None
    _parse_map_property: Optional[Dict[str, str]] = None
    _main_parse_order_to_value: Dict[tuple, List[List[str]]] = {}
    _main_value_to_parse_order: Dict[tuple, tuple] = {}
    _initialized: bool = False

    # Instance variables
    _map_cache: Dict[str, List[List[str]]] = {}

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the root word parser.

        Args:
            data_path: Path to data directory containing rule files
        """
        # Get constant table
        if data_path:
            self.constant_table = TamilConstantTable.get_instance(data_path)
        else:
            self.constant_table = TamilConstantTable.get_instance()

        super().__init__(self.constant_table)

        # Initialize if not already done
        if not TamilRootWordParser._initialized:
            self._initialize_parser()

        # Instance-level data
        self.map_of_list: Dict[str, List[List[str]]] = {}
        self.word_of_map: Dict[str, str] = {}
        self.verb_noun = ""
        self.total_counter = 0

        # Residue patterns
        self.verb_residue_list = [
            "க்கின்ற்", "கின்ற்", "க்கிற்", "கிற்", "ப்ப்", "ப்",
            "வ்", "ந்த்", "இன்", "இ", "க்க்", "ட்", "த்", "ஈ"
        ]
        self.noun_residue_list = [
            "கள்", "ஐ", "கு", "ஆல்", "ஓடு", "ஒடு", "இடம்",
            "உடன்", "இன்", "அது", "ஓட்", "ஒட்", "த்து"
        ]

    def _initialize_parser(self) -> None:
        """Initialize parser with rule files"""
        try:
            # Load main constants, parse order, and parse map
            main_words, main_list_of_list, parse_map = \
                self.constant_table.get_parse_and_main_value(
                    ConfigConstants.MAIN_CONSTANT_FILE_NAME,
                    ConfigConstants.PARSE_ORDER_FILE_NAME,
                    ConfigConstants.MAIN_PARSE_MAP_FILE_NAME
                )

            TamilRootWordParser._main_words = main_words
            TamilRootWordParser._main_list_of_list = main_list_of_list
            TamilRootWordParser._parse_map_property = parse_map

            # Set start value (0-based indexing)
            self.constant_table.set_start_value(0)

            # Build global list
            TamilRootWordParser._global_list = self.constant_table.get_main_table(
                main_words, main_list_of_list,
                TamilRootWordParser._main_parse_order_to_value,
                TamilRootWordParser._main_value_to_parse_order
            )

            TamilRootWordParser._initialized = True
            logger.debug("TamilRootWordParser loaded.")

        except Exception as e:
            logger.error(f"Error initializing TamilRootWordParser: {e}")
            raise

    def get_parser_type(self) -> str:
        """Get parser type"""
        return "Main"

    def get_parse_map_property(self) -> Dict[str, str]:
        """Get parse map properties"""
        return TamilRootWordParser._parse_map_property or {}

    def get_parser_order_to_values(self) -> Dict:
        """Get parser order to values mapping"""
        return TamilRootWordParser._main_parse_order_to_value

    def get_value_to_parse_order(self) -> Dict:
        """Get value to parse order mapping"""
        return TamilRootWordParser._main_value_to_parse_order

    def get_global_list(self) -> List[List[List[str]]]:
        """Get global suffix list"""
        return TamilRootWordParser._global_list or []

    def parse(self, words: Optional[List[str]] = None,
              pass_counter: int = 0,
              no_details: bool = False,
              write_to_file: bool = False,
              word_of_list: Optional[List[str]] = None) -> Dict[str, List[List[str]]]:
        """
        Parse a list of Tamil words.

        Args:
            words: List of words to parse (None for default word list)
            pass_counter: Counter for multi-pass parsing
            no_details: If True, return minimal details
            write_to_file: If True, write results to file
            word_of_list: Output list for word components

        Returns:
            Dictionary mapping words to their parse results
        """
        if word_of_list is None:
            word_of_list = []

        self.map_of_list = {}
        self.word_of_map = {}

        word1 = None
        word2 = None
        counter = pass_counter
        self.verb_noun = ""
        match_pattern = r"[.,;!\"?]*"

        if words is None:
            words = self.constant_table.get_word_list()

        try:
            for word0 in words:
                self.total_counter = 0

                # Remove special characters
                org_word = word0
                word0 = re.sub(match_pattern, "", word0)

                if not word0 or not word0.strip():
                    value = [str(counter), ":", ":(Symbol) IgnoreList", ":", org_word, ":", f":{org_word}"]
                    self.map_of_list[word0] = [value]
                    continue

                if pass_counter == 0:
                    counter += 1

                # Check for numeric
                if word0.isdigit() or any(c.isdigit() for c in word0):
                    self.verb_noun = "NU"
                    self._add_ignore_words(word2, counter, word0, word0, self.verb_noun, no_details, "IgnoreList")
                    key_list = self._build_key_values_list([word0, ""])
                    word_of_list.extend(key_list)
                    self.word_of_map[word0] = f"{word0} {key_list}"
                    continue

                # Check ignore lists
                verb_ignore = self.constant_table.is_in_ignore_verb_word_list(word0)
                noun_ignore = self.constant_table.is_in_ignore_noun_word_list(word0)
                person_ignore = self.constant_table.is_in_ignore_person_list(word0)
                place_ignore = self.constant_table.is_in_ignore_place_list(word0)
                other_ignore = self.constant_table.is_in_ignore_word_list(word0)

                word1 = word0

                if not (verb_ignore or noun_ignore or other_ignore or person_ignore or place_ignore):
                    temp_word = self._end_with_certain_values_extended(word0)
                    if temp_word:
                        word1 = temp_word
                        verb_ignore = self.constant_table.is_in_ignore_verb_word_list(word1)
                        noun_ignore = self.constant_table.is_in_ignore_noun_word_list(word1)

                # Build verb/noun type string
                verb_noun = ""
                if verb_ignore:
                    verb_noun = "(V)"
                if noun_ignore:
                    verb_noun = f"{verb_noun}(N)"
                if person_ignore:
                    verb_noun = f"{verb_noun}(PR)"
                if place_ignore:
                    verb_noun = f"{verb_noun}(PL)"
                if other_ignore:
                    verb_noun = f"{verb_noun}(OTHER)"

                if verb_ignore or noun_ignore or other_ignore or person_ignore or place_ignore:
                    self._add_ignore_words(word2, counter, word0, word1, verb_noun, no_details, "IgnoreList")
                    key_list = self._build_key_values_list([word1, ""])
                    word_of_list.extend(key_list)
                    self.word_of_map[word0] = f"{word1} {key_list}"
                    continue

                # Parse the word
                try:
                    word2 = None
                    word1 = TamilUtil.எழுத்துகளைபிரி(word0, False, False)
                    logger.debug(f"{word0}:{word1}")

                    last_deep_list: Dict[tuple, List[str]] = {}
                    last_deep_parse_list: Dict[str, str] = {}
                    last_parser_order = None

                    split_list = self._get_split_word_list(word1)

                    # Clone global list
                    global_list = [
                        [lst.copy() for lst in outer]
                        for outer in self.get_global_list()
                    ]

                    # Filter for performance
                    split_value_to_parse_order: Dict = {}
                    splitted_global_list = self.splitted_global_list(
                        global_list, word1, split_value_to_parse_order
                    )

                    for outer_list in splitted_global_list:
                        # Performance check
                        if not self._contains_ending(outer_list, split_list):
                            continue

                        if word2 and word2[1] and word2[1].strip():
                            break

                        # Get cached combinations or compute
                        outer_key_str = str(outer_list)
                        list_of_inner_list = self._map_cache.get(outer_key_str)

                        if list_of_inner_list is None or \
                           "NOUN" in outer_key_str or "VERB" in outer_key_str:
                            list_of_inner_list = RecursiveAlgorithm.get_all_combined_values(outer_list)

                        self._map_cache[outer_key_str] = list_of_inner_list

                        outer_key = str(split_value_to_parse_order.get(
                            tuple(tuple(lst) for lst in outer_list), []
                        ))

                        depth_size = len(outer_list)
                        logger.debug(f"{outer_key}: OuterList Size:{len(list_of_inner_list)}:depthSize:{depth_size},TotalCount:{self.total_counter}")

                        try:
                            list_of_inner_list_clone = [lst.copy() for lst in list_of_inner_list]

                            for deeper_inner_list in list_of_inner_list_clone:
                                if deeper_inner_list and \
                                   depth_size == len(deeper_inner_list) and \
                                   self.is_eligible(word1, deeper_inner_list):

                                    word2 = CoreParser.கடைஎழுத்து_கொடுக்கபட்வையில்_முடிந்தால்பிரி(
                                        word1, deeper_inner_list, last_deep_list,
                                        outer_key, last_deep_parse_list,
                                        self.constant_table
                                    )

                                    if word2[1] and word2[1].strip():
                                        last_parser_order = str(
                                            self.get_value_to_parse_order().get(
                                                tuple(tuple(lst) for lst in outer_list), []
                                            )
                                        )
                                        break

                                if self.total_counter > self.EXIT_LOOP:
                                    break

                        except Exception as e:
                            logger.error(f"Error in parse loop: {e}")

                        if self.total_counter > self.EXIT_LOOP:
                            logger.debug(f"{words}:T Break totalCounter:{self.total_counter}: ExitLoop:{self.EXIT_LOOP}")
                            self.total_counter = 0
                            break

                        if word2 and word2[1] and word2[1].strip():
                            check_value_arr_list: List[List[str]] = []
                            self._group_words(
                                word2, counter, word0, word1,
                                last_deep_list, last_deep_parse_list,
                                last_parser_order, check_value_arr_list, word_of_list
                            )

                    if word2 is None:
                        self._add_ignore_words(
                            word2, counter, word0, word1, self.verb_noun,
                            no_details, "Parse Order Not Found"
                        )

                except Exception as e:
                    logger.error(f"Error parsing word: {e}")

                self.total_counter = 0

        except Exception as e:
            logger.error(f"Error in parse: {e}")

        return self.map_of_list

    def _get_split_word_list(self, split_word: str) -> List[str]:
        """Get reversed list of letters from split word"""
        tsi = TamilStringIterator(split_word)
        return tsi.backward_iterator()

    def _contains_ending(self, outer_list: List[List[str]], split_list: List[str]) -> bool:
        """Check if outer_list could match split_list endings"""
        if len(split_list) >= len(outer_list):
            if len(outer_list) >= 1 and self._contains_ending_at(outer_list, split_list, 1):
                if len(outer_list) >= 2 and self._contains_ending_at(outer_list, split_list, 2):
                    if len(outer_list) >= 3 and self._contains_ending_at(outer_list, split_list, 3):
                        return True
                return True
        return False

    def _contains_ending_at(self, outer_list: List[List[str]], split_list: List[str], size: int) -> bool:
        """Check if outer_list at position matches split_list"""
        last_list = outer_list[len(outer_list) - size]

        if "NOUN" in last_list or "VERB" in last_list:
            return True

        temp = ""
        counter = 0

        for split in split_list:
            counter += 1
            temp = split + temp
            temp_join = TamilUtil.எழுத்துகளைசேர்(temp)
            if temp_join in last_list:
                return True

            if len(split_list) - 1 < counter:
                return False
            if counter > 7:
                return False

        return False

    def _add_ignore_words(self, word2: Optional[List[str]], counter: int,
                          word0: str, word1: str, verb_or_noun: str,
                          no_details: bool, hint: str) -> None:
        """Add word to ignore results"""
        value = [str(counter), ":", f":(", verb_or_noun, f") {hint}", ":", word0.strip(), f":{word1.strip()}"]
        if no_details:
            value[0] = word0.strip()

        list_of_string = self.map_of_list.get(word0, [])
        list_of_string.append(value)
        self.map_of_list[word0] = list_of_string

    def _group_words(self, word2: List[str], counter: int, word0: str, word1: str,
                     last_deep_map: Dict, last_deep_parse_list: Dict,
                     last_parser_order: Optional[str],
                     check_value_arr_list: List, word_of_list: List[str]) -> bool:
        """Group and process parsed words"""
        key_list: List[str] = []
        value = f":{word0.strip()}:{word1.strip()}:"
        verb_or_noun = ""
        check_value = None

        if word2[0]:
            check_value = TamilUtil.எழுத்துகளைசேர்(word2[0]) if word2 else ""

        add_value = ""
        add_value_map: Dict[str, str] = {}

        str_arr_list: List[List[str]] = []
        word_of_na_list: List[str] = []
        word_non_na_list: List[str] = []

        if not word2[1] or not word2[1].strip():
            # Build NA values
            arr = self.build_na_values(word2, check_value, value, last_deep_map)
            check_value = arr[0]
            value = arr[1]
            word2 = arr[2]
            check_value_arr_list.extend(arr[3])

            add_value = "(NA)"
            if self.constant_table.is_in_ignore_word_list(check_value):
                add_value = "(IgnList)" + add_value

            if check_value_arr_list:
                for str_arr in check_value_arr_list:
                    str_arr_join = self._build_regular_values(
                        str_arr, TamilUtil.எழுத்துகளைசேர்(str_arr[0]), value, ":", ""
                    )
                    str_arr_list.append(str_arr_join)

                    word_type = "(NA)"
                    if self.constant_table.is_in_ignore_noun_word_list(str_arr_join[0]):
                        word_type = "(N)"
                        str_arr[0] = TamilUtil.எழுத்துகளைபிரி(str_arr_join[0])
                    elif self.constant_table.is_in_ignore_verb_word_list(str_arr_join[0]):
                        word_type = "(V)"
                        str_arr[0] = TamilUtil.எழுத்துகளைபிரி(str_arr_join[0])
                    elif self.constant_table.is_in_ignore_person_list(str_arr_join[0]):
                        word_type = "(PR)"
                        str_arr[0] = TamilUtil.எழுத்துகளைபிரி(str_arr_join[0])
                    elif self.constant_table.is_in_ignore_place_list(str_arr_join[0]):
                        word_type = "(PL)"
                        str_arr[0] = TamilUtil.எழுத்துகளைபிரி(str_arr_join[0])
                    elif self.constant_table.is_in_ignore_word_list(str_arr_join[0]):
                        word_type = "(UNKN)(NA)"

                    add_value_map[str_arr[0]] = word_type
                    key_list = self._build_key_values_list_with_value(str_arr, str_arr_join[0], value)

                    if "NA" in word_type:
                        word_of_na_list.extend(key_list)
                    else:
                        word_non_na_list.extend(key_list)

                    self.word_of_map[word0] = str(key_list)

                if word_non_na_list:
                    word_of_list.extend(word_non_na_list)
                else:
                    word_of_list.extend(word_of_na_list)
            else:
                key_list = self._build_key_values_list_with_value(word2, "", value)
                value = value + str(key_list)
                word_of_list.extend(key_list)
                self.word_of_map[word0] = f"{check_value} {str(key_list).strip()}"
        else:
            arr = self._build_regular_values(word2, check_value, value, "", ":")
            check_value = arr[0]
            value = arr[1]
            key_list = self._build_key_values_list_with_value(word2, "", value)
            value = value + str(key_list)
            word_of_list.extend(key_list)
            self.word_of_map[word0] = f"{check_value} {str(key_list)}"

        # Build final results
        list_of_string_with_no_na: List[List[str]] = []
        list_of_string = self.map_of_list.get(word0, [])

        if check_value_arr_list:
            for i, str_arr in enumerate(check_value_arr_list):
                verb_or_noun = self._find_verb_or_noun(str_arr, str_arr[0])
                final_value = [
                    str(counter), ":",
                    last_parser_order or last_deep_parse_list.get(self._build_suffix_key(str_arr), ""),
                    ":",
                    add_value_map.get(str_arr[0], "(NA)"),
                    "",
                    verb_or_noun,
                    f"{value}{key_list}" if i >= len(check_value_arr_list) else value
                ]

                if verb_or_noun and "NA" not in verb_or_noun:
                    list_of_string_with_no_na.append(final_value)
                list_of_string.append(final_value)
        else:
            verb_or_noun = self._find_verb_or_noun(word2, check_value)
            final_value = [
                str(counter), ":",
                last_parser_order or "",
                ":",
                add_value,
                "",
                verb_or_noun,
                value
            ]
            list_of_string.append(final_value)

        if list_of_string_with_no_na:
            self.map_of_list[word0] = list_of_string_with_no_na
        else:
            self.map_of_list[word0] = list_of_string

        return "NA" in "".join(str(v) for v in (final_value if 'final_value' in dir() else []))

    def _build_suffix_key(self, str_arr: List[str]) -> str:
        """Build suffix key from array"""
        sb = "["
        for count in range(1, len(str_arr)):
            sb += str_arr[count]
            if count + 1 < len(str_arr):
                sb += ", "
        sb += "]"
        return sb

    def _find_verb_or_noun(self, word2: List[str], check_value: str) -> str:
        """Find verb or noun from split residue"""
        if self.constant_table.is_in_ignore_verb_word_list(check_value):
            return "(V)"
        elif self.constant_table.is_in_ignore_noun_word_list(check_value):
            return "(N)"
        elif self.constant_table.is_in_ignore_person_list(check_value):
            return "(PR)"
        elif self.constant_table.is_in_ignore_place_list(check_value):
            return "(PL)"
        return "(NA)"

    def _build_key_values_list(self, word2: List[str]) -> List[str]:
        """Build key values list from word array"""
        key_list: List[str] = []
        if len(word2) > 1:
            key_list.append(word2[0])
            word2[0] = word2[0]

        for i in range(1, 13):
            if len(word2) > i:
                key_list.append(word2[i])
            else:
                key_list.append("")

        return key_list

    def _build_key_values_list_with_value(self, word2: List[str], key: str, value: str) -> List[str]:
        """Build key values list with joined letters"""
        key_list: List[str] = []
        if len(word2) > 1:
            temp_str = TamilUtil.எழுத்துகளைசேர்(word2[0])
            key_list.append(temp_str)
            word2[0] = temp_str

        for i in range(1, 13):
            if len(word2) > i:
                key_list.append(TamilUtil.எழுத்துகளைசேர்(word2[i]))
            else:
                key_list.append("")

        return key_list

    def _build_regular_values(self, word2: List[str], check_value: str,
                              value: str, front_delimiter: str,
                              back_delimiter: str) -> List[str]:
        """Build regular values with morphophonemic adjustments"""
        tsi = TamilStringIterator(check_value)
        last_value = tsi.last()

        if word2[0] and TamilUtil.exist_in_check_list(last_value, TC.VALLINAM_MEY_V_TO_RR):
            if not front_delimiter:
                value = f"{value}{check_value}{back_delimiter} "
            temp_value = TamilUtil.எழுத்துகளைசேர்(
                word2[0] + chr(TC.உ)
            ) if word2 else ""

            if (self.constant_table.is_in_ignore_noun_word_list(temp_value) or
                self.constant_table.is_in_ignore_place_list(temp_value) or
                self.constant_table.is_in_ignore_person_list(temp_value)):
                check_value = TamilUtil.எழுத்துகளைசேர்(word2[0] + chr(TC.உ)) if word2 else ""
            value = f"{value}{check_value} "

        elif word2[0] and TamilUtil.எழுத்துகளைபிரி(check_value).endswith("அ"):
            if not front_delimiter:
                value = f"{value}{check_value}{back_delimiter} "
            temp_value = TamilUtil.எழுத்துகளைசேர்(word2[0] + TC.ம்) if word2 else ""

            if (self.constant_table.is_in_ignore_noun_word_list(temp_value) or
                self.constant_table.is_in_ignore_place_list(temp_value) or
                self.constant_table.is_in_ignore_person_list(temp_value)):
                check_value = TamilUtil.எழுத்துகளைசேர்(word2[0] + TC.ம்) if word2 else ""
            value = f"{value}{check_value} "

        elif word2[0] and TamilUtil.எழுத்துகளைபிரி(check_value).endswith(TC.ஞ்):
            check_value = check_value.replace(TC.ஞ், TC.ம்)
            value = f"{value}{check_value}{back_delimiter} "

        elif word2[0] and TamilUtil.எழுத்துகளைபிரி(check_value).endswith(TC.ங்):
            check_value = check_value.replace(TC.ங், TC.ம்)
            value = f"{value}{check_value}{back_delimiter} "

        else:
            value = f"{value}{check_value} "

        return [check_value, value, None]

    def _end_with_certain_values_extended(self, org_word: str) -> Optional[str]:
        """Extended version of end_with_certain_values with ignore list checks"""
        word = TamilUtil.எழுத்துகளைபிரி(org_word)
        modified_word = None
        tsi = TamilStringIterator(org_word)
        last_value = tsi.last()

        if TamilUtil.exist_in_check_list(last_value, TC.VALLINAM_MEY_V_TO_RR):
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + chr(TC.உ))

        elif word.endswith("அ"):
            if self.constant_table.is_in_ignore_verb_word_list(org_word):
                return word

            # Try adding ம்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + TC.ம்)
            if self.constant_table.is_in_ignore_noun_word_list(modified_word):
                return modified_word

            # Try adding ர்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + TC.ர்)
            if self.constant_table.is_in_ignore_noun_word_list(modified_word):
                return modified_word

            # Try adding ன்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + TC.ன்)
            if self.constant_table.is_in_ignore_noun_word_list(modified_word):
                return modified_word

            return None

        elif word.endswith(TC.ஞ்):
            word = word[:word.rfind(TC.ஞ்)] + TC.ம்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word)

        elif word.endswith(TC.ங்):
            word = word[:word.rfind(TC.ங்)] + TC.ம்
            modified_word = TamilUtil.எழுத்துகளைசேர்(word)

        return modified_word

    def create_single_instance(self, word: str, write_to_file: bool = False) -> List[WordClass]:
        """
        Parse a single word and return WordClass results.

        Args:
            word: Word to parse
            write_to_file: Whether to write results to file

        Returns:
            List of WordClass objects
        """
        word_of_list: List[str] = []
        result_map = self.parse([word], 0, False, False, word_of_list)

        wc_list: List[WordClass] = []
        if result_map:
            wc_list = self.splitting_util.build_word_class(
                result_map, word, word_of_list, self.get_parse_map_property()
            )

        return wc_list

    def create_multiple_instance(self, word_list: Optional[List[str]] = None) -> str:
        """
        Parse multiple words and return formatted results.

        Args:
            word_list: List of words to parse (None for default)

        Returns:
            Formatted result string
        """
        my_sort_list: List[WordClass] = []
        index = 0

        if not word_list:
            word_list = self.constant_table.get_word_list()

        for word in word_list:
            word_of_list: List[str] = []
            result_map = self.parse([word], 0, False, False, word_of_list)
            self.splitting_util.build_sort_list(
                result_map, word, word_of_list,
                my_sort_list, index, self.get_parse_map_property()
            )
            index += 1

        return SplittingUtil.sort_and_format(my_sort_list)
