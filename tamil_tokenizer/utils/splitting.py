"""
Splitting Utility - Equivalent to SplittingUtil.java

This module provides utilities for splitting and processing parsed word results.

Author: Tamil Arasan
"""

from typing import Dict, List, Optional, Tuple, Any
from .word_class import WordClass


class SplittingUtil:
    """
    Utility class for splitting and processing word parse results.

    Handles:
    - Splitting value lists into chunks
    - Merging split lists with parse maps
    - Building WordClass objects from parse results
    """

    def __init__(self, constant_table=None):
        """
        Initialize with constant table.

        Args:
            constant_table: TamilConstantTable instance for lookups
        """
        self.constant_table = constant_table

    @staticmethod
    def get_splitted_list(value_list: List[str]) -> List[List[str]]:
        """
        Split a list into chunks of 12 elements.

        This is used to organize parsed suffix components
        into groups for display.

        Args:
            value_list: List of values to split

        Returns:
            List of lists, each containing up to 12 elements
        """
        list_of_list: List[List[str]] = []

        if len(value_list) == 1:
            list_of_list.append(value_list)
        else:
            size = len(value_list) // 12
            for i in range(size):
                count = i * 12
                start_idx = i + count
                end_idx = i + count + 12
                if end_idx <= len(value_list):
                    list_of_list.append(value_list[start_idx:end_idx])

        return list_of_list

    def get_sub_value_by_keys(self, main_key: str, sub_key: str,
                              local_parse_map: Optional[Dict[str, str]] = None) -> Optional[str]:
        """
        Get sub-value by combining main and sub keys.

        Args:
            main_key: Main key
            sub_key: Sub key
            local_parse_map: Local parse map properties

        Returns:
            Value for combined key or None
        """
        if self.constant_table:
            return self.constant_table.get_main_parse_property(
                local_parse_map, f"{main_key}_{sub_key}"
            )
        return None

    def merge_splitted_list_with_map(self, list_of_list: List[List[str]],
                                     parse_map: Dict[str, str], index: int,
                                     local_parse_map: Optional[Dict[str, str]] = None) -> List[str]:
        """
        Merge split list with parse map to create annotated list.

        Args:
            list_of_list: List of split value lists
            parse_map: Parse values map
            index: Index into list_of_list
            local_parse_map: Local parse map properties

        Returns:
            List of annotated values
        """
        list_of_temp: List[str] = []

        try:
            if list_of_list and index < len(list_of_list):
                list_of_str = list_of_list[index]

                for counter, str_val in enumerate(list_of_str):
                    if str_val and str_val.strip():
                        temp_str = parse_map.get(str(counter), "")

                        if temp_str:
                            temp_first_str = self.get_sub_value_by_keys(
                                str_val.strip(), temp_str.strip(), local_parse_map
                            )
                            temp_second_str = self.get_sub_value_by_keys(
                                temp_str.strip(), str_val.strip(), local_parse_map
                            )

                            temp_str = "/" + temp_str

                            if temp_second_str:
                                temp_str = temp_str + "/" + temp_second_str

                            if temp_first_str:
                                str_val = temp_first_str

                        list_of_temp.append(str_val + temp_str)

        except Exception as e:
            print(f"Error: {list_of_list}")
            raise e

        return list_of_temp

    @staticmethod
    def get_index_number(s: str) -> int:
        """
        Extract index number from string.

        Args:
            s: String like "[14, ...]"

        Returns:
            Index number
        """
        start = s.index("[") + 1 if "[" in s else 1
        end = s.index(",") if "," in s else len(s)
        return int(s[start:end])

    def parse_values(self, s: str, prop: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Parse a result string into a map of values.

        Args:
            s: Result string to parse
            prop: Property map

        Returns:
            Dictionary of parsed values
        """
        result_map: Dict[str, str] = {}

        if s:
            s = s.strip()
            str_array = s.split("[")

            if "null" in s:
                result_map["0"] = "NA"
                result_map["Type"] = "NA"
            elif len(str_array) > 2 and "]" in str_array[2]:
                self._set_description_with_main(str_array[2], str_array[2], result_map, prop)
                self._set_description(str_array[2], result_map, prop)
            elif len(str_array) > 3 and "]" in str_array[3]:
                self._set_description_with_main(str_array[3], str_array[3], result_map, prop)
                self._set_description(str_array[3], result_map, prop)
            elif len(str_array) > 1 and "(" in str_array[1]:
                self._set_description(str_array[1], result_map, prop)

            if result_map.get("0") is None and "NA" in s:
                result_map["0"] = "NA"
                result_map["Type"] = "NA"

        return result_map

    def _set_description(self, main_str: str, result_map: Dict[str, str],
                         local_parse_map: Optional[Dict[str, str]] = None) -> None:
        """
        Set description in result map based on type markers.

        Args:
            main_str: Main string to parse
            result_map: Result map to update
            local_parse_map: Local parse map properties
        """
        str_all_element = main_str.split(":")

        if "V" in main_str:
            result_map["0"] = self._get_prop("V", local_parse_map)
            result_map["Type"] = "V"
            if "NA" in main_str:
                result_map["SubType"] = "NA"

        elif "PRE" in main_str:
            result_map["0"] = self._get_prop("PRE", local_parse_map)
            result_map["Type"] = "PRE"

        elif "PR" in main_str:
            result_map["0"] = self._get_prop("PR", local_parse_map)
            result_map["Type"] = "PR"

        elif "OG" in main_str:
            result_map["0"] = "மற்றவை"
            result_map["Type"] = "OG"

        elif "NU" in main_str:
            result_map["0"] = self._get_prop("NU", local_parse_map)
            result_map["Type"] = "NU"

        # Handle N (but not NA, NU, or Not)
        if "N" in main_str and "NA" not in main_str and "NU" not in main_str and "Not" not in main_str:
            if result_map.get("0"):
                temp_value = result_map["0"] + " or " + self._get_prop("N", local_parse_map)
                result_map["0"] = temp_value
            else:
                result_map["0"] = self._get_prop("N", local_parse_map)
            result_map["Type"] = "N"

        # Handle PL
        if "PL" in main_str:
            if result_map.get("0"):
                temp_value = result_map["0"] + " or " + self._get_prop("PL", local_parse_map)
                result_map["0"] = temp_value
            else:
                result_map["0"] = self._get_prop("PL", local_parse_map)
            result_map["Type"] = "PL"

        # Handle Symbol
        try:
            if "Symbol" in main_str:
                result_map["0"] = self._get_prop("Symbol", local_parse_map)
                if str_all_element and len(str_all_element) > 0 and result_map.get("0") is None:
                    value = str_all_element[3].replace(",", "")
                    if not value or not value.strip():
                        value = " "
                    result_map["0"] = self._get_prop(value, local_parse_map)

            if str_all_element and len(str_all_element) > 0:
                first_value = (result_map.get("0", "") + "_" +
                              str_all_element[-1].replace("]", "").replace("[", "").strip())
                first_value = self._get_prop(first_value, local_parse_map)
                if first_value:
                    result_map["0"] = first_value

        except Exception as e:
            print(f"{main_str}$$$1$$${str_all_element[0] if str_all_element else None}$$$$2$$$${result_map.get('0')}")
            raise e

    def _set_description_with_main(self, s: str, main_str: str,
                                   result_map: Dict[str, str],
                                   local_parse_map: Optional[Dict[str, str]] = None) -> None:
        """
        Set description with main string processing.

        Args:
            s: String to parse
            main_str: Main string
            result_map: Result map to update
            local_parse_map: Local parse map properties
        """
        if s:
            s = s.strip()
            type_val = ""

            if "]" in s:
                str_with_num = s[:s.index("]")]
                s = s.replace("[", "").replace("]", "")
                str_array = str_with_num.split(",")

                for str_val in str_array:
                    if ":" in str_val:
                        break

                    str_temp = self._get_prop(str_val.strip(), local_parse_map)

                    if str_temp:
                        result_map[str(len(result_map) + 1)] = str_temp
                        type_val = str_val.strip()
                        continue

                    # Check ignore lists
                    if str_temp is None and self.constant_table:
                        if self.constant_table.is_in_ignore_noun_word_list(str_val.strip()):
                            str_temp = "N"
                        elif self.constant_table.is_in_ignore_verb_word_list(str_val.strip()):
                            str_temp = "V"
                        elif self.constant_table.is_in_ignore_place_list(str_val.strip()):
                            str_temp = "PL"
                        elif self.constant_table.is_in_ignore_person_list(str_val.strip()):
                            str_temp = "PR"
                        elif self.constant_table.is_in_prefix_list(str_val.strip()):
                            str_temp = "PRE"

                    if str_temp:
                        result_map[str(len(result_map) + 1)] = self._get_prop(str_temp, local_parse_map)
                        type_val = str_temp

                result_map["Key"] = f"[{str_with_num}]"
                result_map["Type"] = type_val

    def _get_prop(self, key: str, local_parse_map: Optional[Dict[str, str]] = None) -> Optional[str]:
        """
        Get property from constant table or local map.

        Args:
            key: Property key
            local_parse_map: Local parse map

        Returns:
            Property value or None
        """
        if self.constant_table:
            return self.constant_table.get_main_parse_property(local_parse_map, key)
        if local_parse_map:
            return local_parse_map.get(key)
        return None

    def build_word_class(self, result_map: Dict[str, List[List[str]]],
                         word: str, word_of_list: List[str],
                         prop: Optional[Dict[str, str]] = None) -> List[WordClass]:
        """
        Build WordClass objects from parse results.

        Args:
            result_map: Map of words to parse result arrays
            word: The word being processed
            word_of_list: List of split word components
            prop: Property map

        Returns:
            List of WordClass objects
        """
        wc_list: List[WordClass] = []
        str_list = result_map.get(word)

        if str_list:
            raw_split_list = self.get_splitted_list(word_of_list)
            count = 0

            for str_arr in str_list:
                temp_split_list: List[List[str]] = []
                str_val = "[" + ",".join(str_arr) + "]"
                map_parse_vals = self.parse_values(str_val, prop)
                str_val = str_val + ":" + str(map_parse_vals)

                merge_split_str = str(self.merge_splitted_list_with_map(
                    raw_split_list, map_parse_vals, 0, prop
                ))

                try:
                    if raw_split_list and count < len(raw_split_list):
                        temp_split_list.append(raw_split_list[count])
                        count += 1
                except Exception:
                    print(f"Exception:********")
                    print(f"{word}:{len(raw_split_list)}")

                word_class = WordClass.create(
                    number=0,
                    word=word,
                    value=str_val,
                    splitted_val=merge_split_str,
                    map_parse_vals=map_parse_vals,
                    raw_split_list=temp_split_list
                )
                wc_list.append(word_class)

        return wc_list

    def build_sort_list(self, result_map: Dict[str, List[List[str]]],
                        word: str, word_of_list: List[str],
                        my_sort_list: List[WordClass], index_global: int,
                        local_parse_map: Optional[Dict[str, str]] = None) -> None:
        """
        Build and add to sorted list of WordClass objects.

        Args:
            result_map: Map of words to parse result arrays
            word: The word being processed
            word_of_list: List of split word components
            my_sort_list: List to add WordClass objects to
            index_global: Global index number
            local_parse_map: Local parse map properties
        """
        str_list = result_map.get(word)

        if str_list:
            raw_split_list = self.get_splitted_list(word_of_list)
            index = 0

            for str_arr in str_list:
                str_val = "[" + ",".join(str_arr) + "]"
                map_parse_vals = self.parse_values(str_val, local_parse_map)
                str_val = str_val + ":" + str(map_parse_vals)

                merge_split_str = str(self.merge_splitted_list_with_map(
                    raw_split_list, map_parse_vals, index, local_parse_map
                ))

                word_class = WordClass.create(
                    number=index_global,
                    word=word,
                    value=str_val,
                    splitted_val=merge_split_str,
                    map_parse_vals=map_parse_vals,
                    raw_split_list=raw_split_list
                )
                my_sort_list.append(word_class)
                index += 1

    @staticmethod
    def sort_and_format(my_sort_list: List[WordClass]) -> str:
        """
        Sort list and format as string.

        Args:
            my_sort_list: List of WordClass objects

        Returns:
            Formatted string
        """
        my_sort_list.sort()
        lines = []
        for word_class in my_sort_list:
            lines.append(f"{word_class.get_value()}||{word_class.get_splitted_val()}")
        return "\n".join(lines)

    @staticmethod
    def format_result_map(map_of_list: Dict[str, List[List[str]]]) -> str:
        """
        Format result map as string.

        Args:
            map_of_list: Map of words to result arrays

        Returns:
            Formatted string
        """
        lines = []
        for key, list_of_string in map_of_list.items():
            for str_arr in list_of_string:
                lines.append(" ".join(str_arr))
        return "\n".join(lines)

    @staticmethod
    def print_map_values(result_map: Dict[str, str]) -> None:
        """
        Print map values for debugging.

        Args:
            result_map: Map to print
        """
        for key, value in result_map.items():
            print(f"{key}:{value}:", end="")
