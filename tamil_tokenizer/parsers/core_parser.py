"""
Core Parser - Equivalent to CoreParser.java

This module provides the abstract base class for all Tamil word parsers.
It contains the core suffix matching and word splitting algorithms.

Author: Tamil Arasan
Since: Feb 09, 2020
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any, Set
from collections import OrderedDict
import copy

logger = logging.getLogger(__name__)

from ..grammar.tamil_util import TamilUtil
from ..constants.tamil_letters import TamilConstants as TC
from ..utils.tamil_iterator import TamilStringIterator
from ..utils.recursive_algorithm import RecursiveAlgorithm
from ..utils.splitting import SplittingUtil
from ..utils.word_class import WordClass
from .word_parser_interface import WordParserInterface


class CoreParser(WordParserInterface, ABC):
    """
    Abstract base class for Tamil word parsers.

    Provides core functionality for:
    - Suffix pattern matching
    - Word splitting based on parse rules
    - Ignore list checking
    - Result building
    """

    # Circuit breaker to avoid infinite loops
    EXIT_LOOP = 20000000

    # Shared cache for cartesian product results
    _map_cache: Dict[str, List[List[str]]] = {}

    def __init__(self, constant_table=None):
        """
        Initialize core parser.

        Args:
            constant_table: TamilConstantTable instance
        """
        self.constant_table = constant_table
        self.splitting_util = SplittingUtil(constant_table) if constant_table else None
        self.verb_noun = ""
        self.total_counter = 0

    def get_parser_type(self) -> str:
        """Get parser type"""
        return "Core"

    def is_special_character(self, word: str) -> bool:
        """Check if word is a special character"""
        if self.constant_table:
            return self.constant_table.get_special_property(word) is not None
        return False

    def get_special_character(self, word: str) -> Optional[str]:
        """Get special character mapping"""
        if self.constant_table:
            return self.constant_table.get_special_property(word)
        return None

    def is_in_noun_list(self, word: str) -> bool:
        """Check if word is in noun ignore list"""
        if self.constant_table:
            return self.constant_table.is_in_ignore_noun_word_list(word)
        return False

    def is_in_verb_list(self, word: str) -> bool:
        """Check if word is in verb ignore list"""
        if self.constant_table:
            return self.constant_table.is_in_ignore_verb_word_list(word)
        return False

    def splitted_global_list(self, global_list: List[List[List[str]]],
                             split_word: str,
                             split_value_to_parse_order: Dict) -> List[List[List[str]]]:
        """
        Filter global list based on split word.

        For performance, only include suffix patterns that could
        potentially match the given word.

        Args:
            global_list: Full list of suffix patterns
            split_word: Split form of the word
            split_value_to_parse_order: Output map for filtered parse orders

        Returns:
            Filtered list of suffix patterns
        """
        splitted_outer_list: List[List[List[str]]] = []
        value_to_parse_order: Dict = {}

        for list_of_list in global_list:
            val_integer = self.get_value_to_parse_order().get(
                tuple(tuple(lst) for lst in list_of_list)
            )
            if val_integer is None:
                continue

            splitted_inner1: List[List[str]] = []

            for lst in list_of_list:
                splitted_inner2: List[str] = []
                for global_str in lst:
                    split_str = TamilUtil.எழுத்துகளைபிரி(global_str, False, False)
                    if (split_word and split_str in split_word) or \
                       "VERB" in global_str or "NOUN" in global_str:
                        if "VERB" in global_str or "NOUN" in global_str:
                            splitted_inner2.append(split_str)
                        else:
                            splitted_inner2.append(TamilUtil.எழுத்துகளைசேர்(split_str))

                if splitted_inner2:
                    splitted_inner1.append(splitted_inner2)

            if splitted_inner1 and len(splitted_inner1) == len(val_integer):
                key = tuple(tuple(lst) for lst in splitted_inner1)
                split_value_to_parse_order[key] = val_integer
                splitted_outer_list.append(splitted_inner1)
                value_to_parse_order[tuple(tuple(lst) for lst in list_of_list)] = val_integer

        return splitted_outer_list

    @staticmethod
    def கடைஎழுத்து_கொடுக்கபட்வையில்_முடிந்தால்பிரி(
            word: str, deeper_inner_list: List[str],
            last_deep_map: Dict[tuple, List[str]],
            outer_key: str,
            last_deep_parse_list: Dict[str, str],
            constant_table=None) -> List[str]:
        """
        கடைஎழுத்து_கொடுக்கபட்வையில்_முடிந்தால்பிரி - Split word if it ends with given suffixes.

        This is the core suffix stripping algorithm. If the word ends with
        the given suffix pattern, extract the root and suffixes.

        Args:
            word: Split form of the word
            deeper_inner_list: List of suffixes to match
            last_deep_map: Map to store partial results
            outer_key: Parse order key
            last_deep_parse_list: Map of parse results
            constant_table: TamilConstantTable for lookups

        Returns:
            Array where [0] is root, [1:] are matched suffixes
        """
        existing_word = last_deep_map.get(tuple(deeper_inner_list))
        if existing_word is not None:
            return [existing_word[0], None]

        # Check if last suffix is in the word
        if len(deeper_inner_list) > 1:
            total_size = len(deeper_inner_list)
            last_letters = deeper_inner_list[total_size - 2] + deeper_inner_list[total_size - 1]
            last_letters = TamilUtil.எழுத்துகளைபிரி(last_letters, False, False)
            if "NOUN" not in last_letters and "VERB" not in last_letters:
                if not word.endswith(last_letters):
                    return [word, None]
        elif len(deeper_inner_list) > 0:
            total_size = len(deeper_inner_list)
            last_letters = deeper_inner_list[total_size - 1]
            last_letters = TamilUtil.எழுத்துகளைபிரி(last_letters, False, False)
            if "NOUN" not in last_letters and "VERB" not in last_letters:
                if not word.endswith(last_letters):
                    return [word, None]

        str_array = [""] * (len(deeper_inner_list) + 1)
        str_array[0] = word
        index = [0, 0]
        old_index = [0, 0]

        # Convert suffixes to split form
        for count in range(len(deeper_inner_list)):
            deeper_inner_list[count] = TamilUtil.எழுத்துகளைபிரி(
                deeper_inner_list[count], False, False
            )

        if CoreParser._கடைஎழுத்து_கொடுக்கபட்வையில்_முடிகிறதா(
                word, deeper_inner_list, constant_table):
            for count in range(len(deeper_inner_list) + 1):
                try:
                    if count + 1 == len(deeper_inner_list):
                        if count - 1 == -1:
                            last_idx = word.rfind(deeper_inner_list[count])
                            str_array[count] = word[:last_idx] if last_idx >= 0 else word
                        else:
                            temp_count = word.rfind(deeper_inner_list[count])
                            temp_word = word[:temp_count]
                            prev_idx = temp_word.rfind(deeper_inner_list[count - 1])
                            str_array[count] = word[prev_idx:temp_count] if prev_idx >= 0 else ""

                    elif count == len(deeper_inner_list):
                        last_idx = word.rfind(deeper_inner_list[count - 1])
                        str_array[count] = word[last_idx:] if last_idx >= 0 else ""

                    elif CoreParser._index_match(
                            word, deeper_inner_list,
                            deeper_inner_list[count],
                            deeper_inner_list[count + 1], index):
                        if count == 0:
                            str_array[count] = word[:index[0]]
                        else:
                            CoreParser._index_match(
                                word, deeper_inner_list,
                                deeper_inner_list[count - 1],
                                deeper_inner_list[count], old_index
                            )
                            str_array[count] = word[old_index[0]:old_index[1]]
                    else:
                        if not str_array[count]:
                            CoreParser._index_match(
                                word, deeper_inner_list,
                                deeper_inner_list[count - 1],
                                deeper_inner_list[count], old_index
                            )
                            str_array[count] = word[old_index[0]:old_index[1]]

                    old_index[0] = index[0]
                    old_index[1] = index[1]

                except Exception as e:
                    logger.error(f"Error in suffix extraction: {e}")

            ignore_string = CoreParser._check_ignore_list(
                str_array, deeper_inner_list, last_deep_map,
                outer_key, last_deep_parse_list, constant_table
            )

            if ignore_string is not None:
                str_array[0] = TamilUtil.எழுத்துகளைபிரி(ignore_string)
            else:
                str_array[1] = ""

            return str_array

        return str_array

    @staticmethod
    def _check_ignore_list(str_array: List[str], deep_list: List[str],
                           last_deep_map: Dict[tuple, List[str]],
                           outer_key: str,
                           last_deep_parse_list: Dict[str, str],
                           constant_table=None) -> Optional[str]:
        """
        Check if the extracted root is in any ignore list.

        Args:
            str_array: Array with root and suffixes
            deep_list: Suffix list
            last_deep_map: Map for partial results
            outer_key: Parse order key
            last_deep_parse_list: Parse result map
            constant_table: TamilConstantTable

        Returns:
            Root word if found in ignore list, else None
        """
        if not constant_table:
            return None

        all_list = [TamilUtil.எழுத்துகளைசேர்(str_array[0])]

        for s in all_list:
            prefix = constant_table.get_prefix_list(s)
            end_value_modified = CoreParser._end_with_certain_values(s)
            conditional_str = constant_table.get_conditional_property(s)

            conditional = None
            if conditional_str and "-" in conditional_str:
                conditional = conditional_str[conditional_str.index("-") + 1:].strip()

            if conditional:
                ok = outer_key.replace("[", "").replace("]", "")
                if "," in ok:
                    ok = ok.split(",")[0].strip()
                if ok == conditional:
                    return conditional_str[:conditional_str.index("-")]

            if prefix is not None:
                return s
            elif conditional_str and conditional is None and \
                    (constant_table.is_in_ignore_verb_word_list(conditional_str) or
                     constant_table.is_in_ignore_noun_word_list(conditional_str)):
                return conditional_str
            elif constant_table.is_in_ignore_verb_word_list(s) or \
                    constant_table.is_in_ignore_noun_word_list(s):
                return s
            elif end_value_modified and \
                    (constant_table.is_in_ignore_verb_word_list(end_value_modified) or
                     constant_table.is_in_ignore_noun_word_list(end_value_modified)):
                cond = constant_table.get_conditional_property(end_value_modified)
                return cond if cond else end_value_modified
            elif s and (constant_table.is_in_ignore_person_list(s) or
                       constant_table.is_in_ignore_place_list(s)):
                return s
            else:
                # Store partial result
                str_new_array = str_array.copy()
                last_deep_map[tuple(deep_list)] = str_new_array
                last_deep_parse_list[str(deep_list)] = outer_key

        return None

    @staticmethod
    def _end_with_certain_values(org_word: str) -> Optional[str]:
        """
        Apply morphophonemic changes to word ending.

        Handles cases like:
        - Hard consonant endings: add உ
        - 'அ' endings: add ம்
        - ஞ் endings: replace with ம்
        - ங் endings: replace with ம்

        Args:
            org_word: Original word

        Returns:
            Modified word or None
        """
        word = TamilUtil.எழுத்துகளைபிரி(org_word)
        modified_word = None
        tsi = TamilStringIterator(org_word)
        last_value = tsi.last()

        if TamilUtil.exist_in_check_list(last_value, TC.VALLINAM_MEY_V_TO_RR):
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + chr(TC.உ))
        elif word.endswith("அ"):
            modified_word = TamilUtil.எழுத்துகளைசேர்(word + TC.ம்)
        elif word.endswith(TC.ஞ்):
            modified_word = TamilUtil.எழுத்துகளைசேர்(
                word.replace(TC.ஞ், TC.ம்)
            )
        elif word.endswith(TC.ங்):
            modified_word = TamilUtil.எழுத்துகளைசேர்(
                word.replace(TC.ங், TC.ம்)
            )

        return modified_word

    @staticmethod
    def _கடைஎழுத்து_கொடுக்கபட்வையில்_முடிகிறதா(
            word: str, deeper_inner_list: List[str],
            constant_table=None) -> bool:
        """
        Check if word ends with the given suffix pattern.

        Handles VERB/NOUN placeholders by substituting from ignore lists.

        Args:
            word: Split form of the word
            deeper_inner_list: List of suffixes
            constant_table: TamilConstantTable

        Returns:
            True if word ends with the suffix pattern
        """
        # Check for VERB/NOUN placeholders
        if "VERB" in deeper_inner_list or "NOUN" in deeper_inner_list:
            if constant_table:
                verb_list = constant_table.get_ignore_verb_list()
                noun_list = constant_table.get_ignore_noun_list()

                # Try substituting verbs/nouns
                result_list_of_list = CoreParser._loop_main(
                    deeper_inner_list, verb_list, noun_list
                )

                result_match_list = []
                final_result_list_of_list = []

                for result_list in result_list_of_list:
                    result = "".join(result_list)
                    if word.endswith(result) and result not in result_match_list:
                        final_result_list = []
                        for count in range(len(deeper_inner_list)):
                            deeper_inner_list[count] = result_list[count]
                            final_result_list.append(result_list[count])
                        final_result_list_of_list.append(final_result_list)
                        result_match_list.append(result)

                if result_match_list:
                    # Find longest match
                    temp = ""
                    curr_index = 0
                    for final_str_list in final_result_list_of_list:
                        if len(temp) < len(str(final_str_list)):
                            temp = str(final_str_list)
                            curr_index += 1

                    deeper_inner_list.clear()
                    deeper_inner_list.extend(final_result_list_of_list[curr_index - 1])
                    return True

        # Simple check
        sb = ""
        for inner in deeper_inner_list:
            sb += TamilUtil.எழுத்துகளைபிரி(inner, False, False)
        return word.endswith(sb)

    @staticmethod
    def _loop_main(deeper_inner_list: List[str],
                   verb_list: List[str],
                   noun_list: List[str]) -> List[List[str]]:
        """
        Generate all combinations with VERB/NOUN substituted.

        Args:
            deeper_inner_list: Pattern with VERB/NOUN placeholders
            verb_list: List of verbs to substitute
            noun_list: List of nouns to substitute

        Returns:
            List of all possible combinations
        """
        result_list_of_list = []

        # Find indices of VERB and NOUN
        has_verb = "VERB" in deeper_inner_list
        has_noun = "NOUN" in deeper_inner_list

        if not has_verb and not has_noun:
            return [deeper_inner_list]

        # Generate combinations
        substitutions = []
        for i, item in enumerate(deeper_inner_list):
            if item == "VERB":
                substitutions.append([(i, v) for v in verb_list[:100]])  # Limit for performance
            elif item == "NOUN":
                substitutions.append([(i, n) for n in noun_list[:100]])
            else:
                substitutions.append([(i, item)])

        # Generate cartesian product
        from itertools import product
        for combo in product(*substitutions):
            result = [""] * len(deeper_inner_list)
            for idx, val in combo:
                result[idx] = val
            result_list_of_list.append(result)

        return result_list_of_list

    @staticmethod
    def _index_match(word: str, deeper_inner_list: List[str],
                     first: str, second: str, index: List[int]) -> bool:
        """
        Find indices of first and second suffix in word.

        Args:
            word: The word to search
            deeper_inner_list: Full suffix list
            first: First suffix to find
            second: Second suffix to find
            index: Output [start, end] indices

        Returns:
            True if valid indices found
        """
        join_remaining = "".join(deeper_inner_list)
        total_begin_idx = word.find(join_remaining)
        if total_begin_idx < 0:
            total_begin_idx = 0
        total_begin = word[:total_begin_idx]

        first_last = word.find(first, index[1])
        if first_last == -1:
            first_last = word.find(first, index[0])

        if index[0] == 0 and index[1] == 0:
            word_index = len(total_begin)
            if first_last < word_index:
                first_last = word.find(first, word_index)

        if first == second:
            second_last = word.find(second, first_last) + len(second)
        else:
            if first in second:
                second_last = word.find(second, first_last + len(first))
            else:
                second_last = word.find(second, first_last)

        repeat = 0
        while first_last > 0:
            repeat += 1
            if repeat > 50:
                return False

            if first_last < second_last:
                index[0] = first_last
                index[1] = second_last
                return True
            elif first_last == second_last:
                temp_first = first_last
                temp_count = first_last + 2
                first_last = word.rfind(first, 0, first_last + 2)
                if temp_first == first_last:
                    first_last = temp_count
            else:
                first_last = word.rfind(first, 0, first_last - 1)

        index[0] = 0
        index[1] = 0
        return False

    def is_eligible(self, word: str, deeper_inner_list: List[str]) -> bool:
        """
        Check if word is long enough for the suffix pattern.

        Args:
            word: The word to check
            deeper_inner_list: Suffix pattern

        Returns:
            True if word is longer than suffix pattern
        """
        suffix_str = "".join(deeper_inner_list)
        return len(word) > len(suffix_str)

    def build_na_values(self, word2: List[str], check_value: str,
                        value: str, last_deep_map: Dict) -> Tuple[str, str, List[str], List[List[str]]]:
        """
        Build NA (not available) values from partial results.

        Args:
            word2: Current word array
            check_value: Current check value
            value: Current value string
            last_deep_map: Map of partial results

        Returns:
            Tuple of (check_value, value, word2, check_value_arr_list)
        """
        map_of_list_of_unparse_value: Dict[int, List[List[str]]] = {}
        prev_size = 0

        for unparse_key, unparse_value in last_deep_map.items():
            if len(unparse_key) >= prev_size:
                prev_size = len(unparse_key)

            list_of_unparse_value = map_of_list_of_unparse_value.get(len(unparse_key), [])
            list_of_unparse_value.append(unparse_value)
            map_of_list_of_unparse_value[len(unparse_key)] = list_of_unparse_value

        check_value_arr_list: List[List[str]] = []

        try:
            while prev_size != 0:
                list_of_unparse_value = map_of_list_of_unparse_value.get(prev_size)
                if list_of_unparse_value:
                    for unparse_value1 in list_of_unparse_value:
                        if unparse_value1 and len(unparse_value1) > 0:
                            word2 = unparse_value1.copy()
                            check_value = TamilUtil.எழுத்துகளைசேர்(unparse_value1[0]) if unparse_value1 else ""
                            check_value_arr_list.append(unparse_value1)

                            if unparse_value1[0].endswith("ட்ட்"):
                                word2 = unparse_value1.copy()
                                word2[0] = word2[0].replace("ட்ட்", "ட்")
                                check_value = TamilUtil.எழுத்துகளைசேர்(word2[0])
                                check_value_arr_list.append(word2)

                prev_size -= 1

        except Exception as e:
            logger.error(f"{check_value}:{value}")
            raise e

        return (check_value, value, word2, check_value_arr_list)

    @abstractmethod
    def get_parser_order_to_values(self) -> Dict:
        """Get parser order to values mapping"""
        pass

    @abstractmethod
    def get_value_to_parse_order(self) -> Dict:
        """Get value to parse order mapping"""
        pass

    @abstractmethod
    def get_global_list(self) -> List[List[List[str]]]:
        """Get global suffix list"""
        pass
