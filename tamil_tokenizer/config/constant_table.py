"""
Tamil Constant Table - Equivalent to TamilConstantTable.java

This module manages the loading and lookup of Tamil grammar rules,
ignore lists, and parse configurations.

Author: Tamil Arasan
Since: Oct 13, 2017
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from .config_loader import ConfigLoader
from .constants import ConfigConstants, DEFAULT_FILE_PATHS


class TamilConstantTable:
    """
    Central manager for Tamil grammar rules and lookup tables.

    Loads and provides access to:
    - Suffix pattern tables (mainConstant.list)
    - Parse order rules (parseOrder.list)
    - Ignore lists (verbs, nouns, places, persons)
    - Special character mappings
    - Conditional rules
    """

    _instance: Optional['TamilConstantTable'] = None

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize constant table.

        Args:
            data_path: Path to data directory containing rule files
        """
        # Set data path
        if data_path:
            self.data_path = data_path
        else:
            self.data_path = str(Path(__file__).parent.parent / "data")

        # Initialize config loader
        self.config_loader = ConfigLoader.get_instance(self.data_path)

        # Initialize lists
        self.ignore_verb_list: List[str] = []
        self.ignore_noun_list: List[str] = []
        self.ignore_other_grammar_list: List[str] = []
        self.ignore_list: List[str] = []
        self.ignore_place_list: List[str] = []
        self.ignore_person_list: List[str] = []
        self.prefix_list: List[str] = []
        self.word_list: List[str] = []
        self.unique_list: List[str] = []

        # Properties
        self.special_character_property: Dict[str, str] = {}
        self.conditional_property: Dict[str, str] = {}

        # Parse order start value (0 or 1)
        self.START_VALUE = 0

        # File name mappings from allFileList.list
        self.file_map: Dict[str, str] = {}

    @classmethod
    def get_instance(cls, data_path: Optional[str] = None) -> 'TamilConstantTable':
        """
        Get singleton instance.

        Args:
            data_path: Optional data path override

        Returns:
            TamilConstantTable instance
        """
        if cls._instance is None:
            cls._instance = TamilConstantTable(data_path)
            cls._instance.load_basic_files()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset singleton instance (for testing)"""
        cls._instance = None

    def load_basic_files(self) -> None:
        """Load basic configuration files (ignore lists, properties)"""
        try:
            # Try to load allFileList.list for file mappings
            all_files_path = os.path.join(self.data_path, "allFileList.list")
            if os.path.exists(all_files_path):
                self.file_map = self.config_loader.read_initial_properties(all_files_path)

            # Load ignore lists
            self._load_ignore_lists()

            # Load properties
            self._load_properties()

            # Load prefix list
            self._load_prefix_list()

            # Load word list
            self._load_word_list()

        except Exception as e:
            print(f"Error loading basic files: {e}")

    def _load_ignore_lists(self) -> None:
        """Load all ignore lists"""
        # Ignore verb list
        verb_file = self._get_file_path(ConfigConstants.IGNORE_VERB_LIST_FILE_NAME,
                                        "ignoreVerb.list")
        if os.path.exists(verb_file):
            self.ignore_verb_list = self.config_loader.read_comma_separated_file(verb_file)
            print(f"Loaded {len(self.ignore_verb_list)} verbs to ignore")

        # Ignore noun list
        noun_file = self._get_file_path(ConfigConstants.IGNORE_NOUN_LIST_FILE_NAME,
                                        "ignoreNoun.list")
        if os.path.exists(noun_file):
            self.ignore_noun_list = self.config_loader.read_comma_separated_file(noun_file)
            print(f"Loaded {len(self.ignore_noun_list)} nouns to ignore")

        # Ignore other grammar list
        other_file = self._get_file_path(ConfigConstants.IGNORE_OTHER_GRAMMAR_LIST_FILE_NAME,
                                         "ignoreOtherGrammar.list")
        if os.path.exists(other_file):
            self.ignore_other_grammar_list = self.config_loader.read_comma_separated_file(other_file)

        # Ignore place list
        place_file = self._get_file_path(ConfigConstants.IGNORE_PLACE_LIST_FILE_NAME,
                                         "ignorePlace.list")
        if os.path.exists(place_file):
            self.ignore_place_list = self.config_loader.read_comma_separated_file(place_file)

        # Ignore person list
        person_file = self._get_file_path(ConfigConstants.IGNORE_PERSON_LIST_FILE_NAME,
                                          "ignorePerson.list")
        if os.path.exists(person_file):
            self.ignore_person_list = self.config_loader.read_comma_separated_file(person_file)

    def _load_properties(self) -> None:
        """Load property files"""
        # Special character properties
        special_file = self._get_file_path(ConfigConstants.SPECIAL_CHARACTER_FILE_NAME,
                                           "specialCharacter.list")
        if os.path.exists(special_file):
            self.special_character_property = self.config_loader.read_properties_file(special_file)

        # Conditional properties
        cond_file = self._get_file_path(ConfigConstants.CONDITIONAL_FILE_NAME,
                                        "condition_rule.list")
        if os.path.exists(cond_file):
            self.conditional_property = self.config_loader.read_properties_file(cond_file)

    def _load_prefix_list(self) -> None:
        """Load prefix list"""
        prefix_file = self._get_file_path(ConfigConstants.PREFIX_FILE_NAME, "prefix.list")
        if os.path.exists(prefix_file):
            self.prefix_list = self.config_loader.read_comma_separated_file(prefix_file)

    def _load_word_list(self) -> None:
        """Load word list"""
        word_file = self._get_file_path(ConfigConstants.WORD_LIST_FILE_NAME, "word.list")
        if os.path.exists(word_file):
            self.word_list = self.config_loader.read_delimiter_separated_file(word_file, " ")

    def _get_file_path(self, config_key: str, default_name: str) -> str:
        """
        Get file path from config or use default.

        Args:
            config_key: Key in file_map
            default_name: Default filename if key not found

        Returns:
            Full file path
        """
        filename = self.file_map.get(config_key, default_name)

        # Normalize Windows-style paths to Unix-style
        # Handle paths like "..\properties\mainConstant.list"
        filename = filename.replace('\\', '/')

        # If path starts with "..", resolve it relative to data_path
        if filename.startswith('../') or filename.startswith('..\\'):
            # Remove the ../ prefix and use just the filename
            parts = filename.split('/')
            # Find the actual filename (last part after properties/)
            for i, part in enumerate(parts):
                if part == 'properties' and i + 1 < len(parts):
                    filename = parts[i + 1]
                    break
            else:
                # Fallback: just use the last part
                filename = parts[-1]

        return os.path.join(self.data_path, filename)

    def get_main_word_list(self, main_words: List[List[str]]) -> List[List[str]]:
        """
        Get main word list from 2D array.

        Args:
            main_words: 2D array of suffix patterns

        Returns:
            List of string lists
        """
        return [list(row) for row in main_words]

    # ==================== Ignore List Checks ====================

    def is_in_unique_constant_word_list(self, word: str) -> bool:
        """Check if word is in unique list"""
        return word in self.unique_list

    def is_in_ignore_word_list(self, word: str) -> bool:
        """Check if word is in general ignore list"""
        return word in self.ignore_list

    def is_in_ignore_verb_word_list(self, word: str) -> bool:
        """Check if word is in verb ignore list"""
        return word in self.ignore_verb_list

    def is_in_ignore_noun_word_list(self, word: str) -> bool:
        """Check if word is in noun ignore list"""
        return word in self.ignore_noun_list

    def is_in_ignore_place_list(self, word: str) -> bool:
        """Check if word is in place ignore list"""
        return word in self.ignore_place_list

    def is_in_ignore_person_list(self, word: str) -> bool:
        """Check if word is in person ignore list"""
        return word in self.ignore_person_list

    def is_in_ignore_other_grammar_list(self, word: str) -> bool:
        """Check if word is in other grammar ignore list"""
        return word in self.ignore_other_grammar_list

    def is_in_prefix_list(self, word: str) -> bool:
        """Check if word is a prefix"""
        return word in self.prefix_list

    def get_prefix_list(self, word: str) -> Optional[str]:
        """Get word if it's a prefix, else None"""
        return word if self.is_in_prefix_list(word) else None

    # ==================== List Getters ====================

    def get_ignore_noun_list(self) -> List[str]:
        """Get noun ignore list"""
        return self.ignore_noun_list

    def get_ignore_verb_list(self) -> List[str]:
        """Get verb ignore list"""
        return self.ignore_verb_list

    def get_ignore_other_grammar_list(self) -> List[str]:
        """Get other grammar ignore list"""
        return self.ignore_other_grammar_list

    def get_word_list(self) -> List[str]:
        """Get word list"""
        return self.word_list

    # ==================== Property Access ====================

    def get_property(self, props: Dict[str, str], key: str) -> Optional[str]:
        """
        Get property value by key.

        Args:
            props: Property dictionary
            key: Property key

        Returns:
            Property value or None
        """
        return props.get(key)

    def get_main_parse_property(self, parse_map: Optional[Dict[str, str]],
                                key: str) -> Optional[str]:
        """
        Get main parse property.

        Args:
            parse_map: Parse map properties
            key: Property key

        Returns:
            Property value or None
        """
        if parse_map:
            return parse_map.get(key)
        return None

    def get_conditional_property(self, key: str) -> Optional[str]:
        """Get conditional property"""
        return self.conditional_property.get(key)

    def get_special_property(self, key: str) -> Optional[str]:
        """Get special character property"""
        return self.special_character_property.get(key)

    # ==================== Parse Order Management ====================

    def get_start_value(self) -> int:
        """Get parse order start value (0 or 1)"""
        return self.START_VALUE

    def set_start_value(self, start_value: int) -> None:
        """Set parse order start value"""
        self.START_VALUE = start_value

    def get_parse_order_list(self, main_list_of_list: List[List[int]]) -> List[List[int]]:
        """Get parse order list"""
        return main_list_of_list

    # ==================== Table Building ====================

    def get_parse_and_main_value(self, main_constant_file: str,
                                 parse_order_file: str,
                                 parse_map_file: str) -> Tuple[List[List[str]],
                                                               List[List[int]],
                                                               Dict[str, str]]:
        """
        Get main constants, parse order, and parse map.

        Args:
            main_constant_file: Key for main constant file
            parse_order_file: Key for parse order file
            parse_map_file: Key for parse map file

        Returns:
            Tuple of (main_words, parse_order_list, parse_map)
        """
        main_file = self._get_file_path(main_constant_file,
                                        DEFAULT_FILE_PATHS.get(main_constant_file, ""))
        order_file = self._get_file_path(parse_order_file,
                                         DEFAULT_FILE_PATHS.get(parse_order_file, ""))
        map_file = self._get_file_path(parse_map_file,
                                       DEFAULT_FILE_PATHS.get(parse_map_file, ""))

        main_words = self.config_loader.read_main_constant_file_as_list(main_file)
        parse_order = self.config_loader.read_parse_order_file_as_list(order_file)
        parse_map = self.config_loader.read_properties_file(map_file)

        return (main_words, parse_order, parse_map)

    def get_parse_map(self, main_constant_file: str) -> Dict[str, str]:
        """
        Get parse map for a constant file.

        Args:
            main_constant_file: Key for constant file

        Returns:
            Dictionary mapping
        """
        map_file = self._get_file_path(main_constant_file,
                                       DEFAULT_FILE_PATHS.get(main_constant_file, ""))
        return self.config_loader.read_file_as_map(map_file)

    def get_parse_and_main_value_single(self, file_name: str) -> Dict[str, str]:
        """
        Get parse map for a single file.

        Args:
            file_name: Key for the file

        Returns:
            Dictionary mapping
        """
        try:
            file_path = self._get_file_path(file_name,
                                           DEFAULT_FILE_PATHS.get(file_name, ""))
            return self.config_loader.read_properties_file(file_path)
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
            return {}

    def get_main_table(self, main_words: List[List[str]],
                       main_list_of_list: List[List[int]],
                       main_parse_order_to_value: Dict[Tuple[int, ...], List[List[str]]],
                       main_value_to_parse_order: Dict[Tuple[Tuple[str, ...], ...], Tuple[int, ...]]) -> List[List[List[str]]]:
        """
        Build main table from parse order and suffix patterns.

        Args:
            main_words: 2D array of suffix patterns
            main_list_of_list: Parse order rules
            main_parse_order_to_value: Map from parse order to suffix lists
            main_value_to_parse_order: Reverse map

        Returns:
            3D list of suffix combinations per parse rule
        """
        return self._get_common_table(main_list_of_list, main_words,
                                      main_parse_order_to_value,
                                      main_value_to_parse_order)

    def _get_common_table(self, common_list_of_list: List[List[int]],
                          common_words: List[List[str]],
                          common_parse_order_to_value: Dict,
                          common_value_to_parse_order: Dict) -> List[List[List[str]]]:
        """
        Build common table structure.

        For each parse order rule, collect the corresponding suffix lists
        from the main words array.

        Args:
            common_list_of_list: List of parse order rules
            common_words: 2D suffix pattern array
            common_parse_order_to_value: Output map
            common_value_to_parse_order: Output reverse map

        Returns:
            3D list structure
        """
        global_list_str: List[List[List[str]]] = []

        for parse_rule in common_list_of_list:
            outer_list_str: List[List[str]] = []

            for idx in parse_rule:
                try:
                    # Adjust index by START_VALUE
                    adjusted_idx = idx - self.START_VALUE
                    if 0 <= adjusted_idx < len(common_words):
                        inner_list_str = list(common_words[adjusted_idx])
                        outer_list_str.append(inner_list_str)
                except Exception as e:
                    print(f"TamilConstantTable...Error: {idx}:{self.START_VALUE}:{e}")

            # Store mappings
            rule_key = tuple(parse_rule)
            common_parse_order_to_value[rule_key] = outer_list_str

            # Create tuple key for reverse mapping
            value_key = tuple(tuple(lst) for lst in outer_list_str)
            common_value_to_parse_order[value_key] = rule_key

            global_list_str.append(outer_list_str)

        return global_list_str

    def print_main_parse_property(self, parse_map: Dict[str, str]) -> None:
        """Print parse map properties for debugging"""
        for key, value in parse_map.items():
            print(f"{key}-:-{value}")
