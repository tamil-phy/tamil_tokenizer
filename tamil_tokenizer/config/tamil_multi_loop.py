"""
Tamil Multi Loop - Equivalent to TamilMultiLoop.java

This module provides multi-loop iteration for generating
combinations with verb and noun placeholders.

Author: Tamil Arasan
"""

import logging
from typing import Dict, List, Optional, Any
from ..grammar.tamil_util import TamilUtil

logger = logging.getLogger(__name__)


class TamilMultiLoop:
    """
    Multi-loop iterator for generating verb/noun combinations.

    Handles patterns like [VERB], [NOUN] placeholders and
    generates all possible combinations.
    """

    def __init__(self):
        """Initialize the multi-loop handler."""
        self.verb_list: List[str] = ["V1", "V2"]
        self.noun_list: List[str] = ["N1", "N2", "N3", "N4"]
        self.EXIT_LOOP = False
        self.total_item_size = 0
        self.map: Dict[int, List[Any]] = {}
        self.map_with_item: Dict[int, List[Any]] = {}
        self.cache_loop: Dict[str, List[List[str]]] = {}

    def loop_main_simple(self, deeper_inner_list: List[str]) -> List[List[str]]:
        """
        Run loop with default verb/noun lists.

        Args:
            deeper_inner_list: List with [VERB] and [NOUN] placeholders

        Returns:
            List of generated combinations
        """
        verb_list = ["V1", "V2"]
        noun_list = ["N1", "N2", "N3", "N4"]
        return self.loop_main(deeper_inner_list, verb_list, noun_list)

    def loop_main(self, deeper_inner_list: List[str],
                  verb_list: List[str],
                  noun_list: List[str]) -> List[List[str]]:
        """
        Generate all combinations for placeholders.

        Args:
            deeper_inner_list: List with [VERB] and [NOUN] placeholders
            verb_list: List of verbs to substitute
            noun_list: List of nouns to substitute

        Returns:
            List of generated combinations
        """
        # Check cache
        cache_key = str(deeper_inner_list)
        if cache_key in self.cache_loop:
            return self.cache_loop[cache_key]

        list_of_list: List[List[str]] = []
        self.verb_list = verb_list
        self.noun_list = noun_list

        self._init(deeper_inner_list)
        self.EXIT_LOOP = False

        while not self.EXIT_LOOP:
            list_of_string: List[str] = []

            for index in range(len(deeper_inner_list)):
                try:
                    str_value = self._spinner(index, deeper_inner_list[index])
                    str_value = TamilUtil.எழுத்துகளைபிரி(str_value, False, False)
                except Exception as e:
                    logger.error(f"Exception: {str_value}")
                    logger.error(e)

                list_of_string.append(str_value)

                if self._is_all_size_max():
                    self.EXIT_LOOP = True

            list_of_list.append(list_of_string)

        self.cache_loop[cache_key] = list_of_list
        return list_of_list

    def _init(self, deeper_inner_list: List[str]) -> None:
        """
        Initialize state for loop processing.

        Args:
            deeper_inner_list: List with placeholders
        """
        self.total_item_size = 0
        self.map = {}
        self.map_with_item = {}

        for index, inner in enumerate(deeper_inner_list):
            if self._is_verb(inner):
                obj_array = [0, len(self.verb_list), self.total_item_size + 1, "Verb"]
                self.total_item_size += 1
                self.map[index] = obj_array
                self.map_with_item[self.total_item_size] = obj_array
            elif self._is_noun(inner):
                obj_array = [0, len(self.noun_list), self.total_item_size + 1, "Noun"]
                self.total_item_size += 1
                self.map[index] = obj_array
                self.map_with_item[self.total_item_size] = obj_array

    def _spinner(self, index: int, value: str) -> str:
        """
        Get next value for position.

        Args:
            index: Position index
            value: Current value/placeholder

        Returns:
            Substituted value
        """
        current_array = self.map.get(index)

        if current_array is not None:
            current_count = current_array[0]
            total_current_item_size = current_array[1]
            item_type = current_array[3]

            if self._is_verb(item_type):
                value = self.verb_list[current_array[0]]
                current_array[0] = self._increment_count(
                    current_count, total_current_item_size, current_array[2]
                )
                if total_current_item_size == current_array[0] and not self._is_all_size_max():
                    current_array[0] = 0

            elif self._is_noun(item_type):
                value = self.noun_list[current_array[0]]
                current_array[0] = self._increment_count(
                    current_count, total_current_item_size, current_array[2]
                )
                if total_current_item_size == current_array[0] and not self._is_all_size_max():
                    current_array[0] = 0

        return value

    def _is_all_size_max(self) -> bool:
        """Check if all positions are at max."""
        for obj_value in self.map.values():
            if obj_value[0] != obj_value[1]:
                return False
        return True

    def _increment_count(self, current_count: int,
                         total_current_item_size: int,
                         current_item_position: int) -> int:
        """
        Increment counter with carry-over logic.

        Args:
            current_count: Current count
            total_current_item_size: Total size for this item
            current_item_position: Position of this item

        Returns:
            New count
        """
        if self.total_item_size == current_item_position:
            if current_count != total_current_item_size:
                current_count += 1

                if current_count == total_current_item_size and current_item_position != 0:
                    for idx in range(1, current_item_position + 1):
                        prev_array = self.map_with_item.get(current_item_position - idx)

                        if prev_array and len(prev_array) > 0:
                            prev_array[0] += 1

                            if prev_array[0] == prev_array[1]:
                                prev_array[0] = 0
                                if current_item_position - idx == 0:
                                    self.EXIT_LOOP = True
                            else:
                                break
                        else:
                            self.EXIT_LOOP = True

        return current_count

    def get_verb(self, curr_global_pos: int, curr_index: int, total_size: int) -> str:
        """Get verb at index."""
        return self.verb_list[curr_index]

    def get_noun(self, curr_global_pos: int, curr_index: int, total_size: int) -> str:
        """Get noun at index."""
        return self.noun_list[curr_index]

    @staticmethod
    def _is_verb(text: str) -> bool:
        """Check if text is a verb placeholder."""
        return text.upper() == "VERB" or "[VERB]" in text.upper()

    @staticmethod
    def _is_noun(text: str) -> bool:
        """Check if text is a noun placeholder."""
        return text.upper() == "NOUN" or "[NOUN]" in text.upper()


if __name__ == "__main__":
    tml = TamilMultiLoop()

    deeper_inner_list = ["[VERB]", "[NOUN]"]
    result = tml.loop_main_simple(deeper_inner_list)

    for item in result:
        logger.debug(item)
