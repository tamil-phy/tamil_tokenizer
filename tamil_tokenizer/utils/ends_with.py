"""
EndsWith Utilities - Equivalent to EndsWith.java

This module provides utilities for analyzing word endings
and finding root forms based on suffix conditions.

Author: Tamil Arasan
"""

from typing import Dict, List, Set
from .tamil_iterator import TamilStringIterator
from .file_io import ReadFromFile, WriteToFile
from ..grammar.tamil_util import TamilUtil


class EndsWith:
    """
    Utility class for analyzing Tamil word endings.

    Processes words based on suffix conditions to find root forms.
    """

    @staticmethod
    def process_words(words_file: str, conditions_file: str,
                      output_file: str) -> None:
        """
        Process words based on suffix conditions.

        Args:
            words_file: File containing words to process
            conditions_file: File with condition rules (CSV format)
            output_file: Output file for results
        """
        rff = ReadFromFile()
        str_list = rff.read_file_as_list(words_file)
        cond_list = rff.read_file_as_list(conditions_file)

        # Parse conditions into list of maps
        list_of_str_map: List[Dict[str, str]] = []

        for cond in cond_list:
            cond_arr = cond.split(',')
            str_map: Dict[str, str] = {}

            for cond_item in cond_arr:
                if '=' in cond_item:
                    key, value = cond_item.split('=', 1)
                    str_map[key] = value

            list_of_str_map.append(str_map)

        # Process each word
        all_set: Set[str] = set()
        non_exist_set: Set[str] = set()
        exist_set: Set[str] = set()
        not_checked_set: Set[str] = set()
        all_split_set: Set[str] = set()

        for word in str_list:
            all_split_set.add(f"{word}:{TamilUtil.எழுத்துகளைபிரி(word, False, False)}")

            for str_map in list_of_str_map:
                split_val = str_map.get('SPLIT', '')
                b_split = split_val.lower() == 'true' if split_val else False

                if b_split:
                    temp_str = TamilUtil.எழுத்துகளைபிரி(word, False, False)
                else:
                    temp_str = word

                ends = str_map.get('ENDS', '')
                delete = str_map.get('DELETE', '')

                if temp_str.endswith(ends):
                    add = str_map.get('ADD', '')

                    # Remove the ending
                    if delete and delete in temp_str:
                        temp_str = temp_str[:temp_str.rfind(delete)]

                    # Add suffix if needed
                    # Note: In Java, there were calls to TamilConstantTable
                    # which we're simplifying here
                    noun_exist = False
                    verb_exist = False
                    person_exist = False
                    place_exist = False

                    if not (noun_exist or verb_exist or person_exist or place_exist):
                        temp_str = temp_str + add

                    if b_split:
                        temp_str_split = TamilUtil.எழுத்துகளைசேர்(temp_str)
                        if not (noun_exist or verb_exist or person_exist or place_exist):
                            non_exist_set.add(temp_str_split)
                        else:
                            exist_set.add(temp_str_split)
                    else:
                        if not (noun_exist or verb_exist or person_exist or place_exist):
                            non_exist_set.add(temp_str)
                        else:
                            exist_set.add(temp_str)
                    break
                else:
                    not_checked_set.add(TamilUtil.எழுத்துகளைசேர்(temp_str))

            all_set.add(f"{word}:{TamilUtil.எழுத்துகளைசேர்(temp_str)}")

        # Write results
        WriteToFile.write_to_file(
            EndsWith._build_string(non_exist_set),
            output_file
        )

    @staticmethod
    def remove_set(target_set: Set[str], source_set: Set[str]) -> None:
        """
        Remove elements in source_set from target_set.

        Args:
            target_set: Set to modify
            source_set: Set of elements to remove
        """
        for item in source_set:
            target_set.discard(item)

    @staticmethod
    def _build_string(string_set: Set[str]) -> str:
        """
        Build newline-separated string from set.

        Args:
            string_set: Set of strings

        Returns:
            Newline-separated string
        """
        return '\n'.join(string_set) + '\n' if string_set else ''


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 4:
        EndsWith.process_words(sys.argv[1], sys.argv[2], sys.argv[3])
