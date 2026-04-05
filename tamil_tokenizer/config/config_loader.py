"""
Config Loader - Equivalent to ReadConfig.java

This module provides file reading utilities for configuration and rule files.

Author: Tamil Arasan
Since: Oct 23, 2017
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import OrderedDict


class ConfigLoader:
    """
    Configuration and rule file loader.

    Reads various file formats used by the Tamil NLP system:
    - CSV-style constant files
    - Parse order files (comma-separated integers)
    - Properties files (key=value)
    - Delimiter-separated lists
    """

    _instance: Optional['ConfigLoader'] = None
    _properties: Dict[str, str] = {}
    _current_root: str = ""

    def __init__(self, root_path: Optional[str] = None):
        """
        Initialize config loader.

        Args:
            root_path: Root path for relative file lookups
        """
        if root_path:
            self._current_root = root_path
        else:
            # Default to package data directory
            self._current_root = str(Path(__file__).parent.parent / "data")

    @classmethod
    def get_instance(cls, root_path: Optional[str] = None) -> 'ConfigLoader':
        """
        Get singleton instance of ConfigLoader.

        Args:
            root_path: Optional root path override

        Returns:
            ConfigLoader instance
        """
        if cls._instance is None:
            cls._instance = ConfigLoader(root_path)
            # Try to load initial properties if available
            try:
                all_files_path = os.path.join(cls._instance._current_root, "allFileList.list")
                if os.path.exists(all_files_path):
                    cls._properties = cls._instance.read_initial_properties(all_files_path)
            except Exception:
                pass

        return cls._instance

    @property
    def current_root(self) -> str:
        """Get current root path"""
        return self._current_root

    def get_current_root(self) -> str:
        """Get current root path (Java-style method)"""
        return self._current_root

    def get_properties(self) -> Dict[str, str]:
        """Get loaded properties"""
        return self._properties

    def convert_main_constant_file_as_array(self, filename: str) -> List[List[str]]:
        """
        Read main constant file as 2D array (list of lists).

        Args:
            filename: Path to constant file

        Returns:
            List of string lists (each row is a list)
        """
        return self.read_main_constant_file_as_list(filename)

    def read_main_constant_file_as_list(self, filename: str) -> List[List[str]]:
        """
        Read main constant file as list of lists.

        File format: comma-separated values, one row per line.

        Args:
            filename: Path to constant file

        Returns:
            List of string lists
        """
        main_list: List[List[str]] = []

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        values = [v.strip() for v in line.split(',')]
                        main_list.append(values)
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

        return main_list

    def read_parse_order_file_as_list(self, filename: str) -> List[List[int]]:
        """
        Read parse order file as list of integer lists.

        File format: comma-separated integers, one rule per line.

        Args:
            filename: Path to parse order file

        Returns:
            List of integer lists (each representing a parse rule)
        """
        main_list: List[List[int]] = []

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        line_list: List[int] = []
                        values = line.split(',')
                        for val in values:
                            val = val.strip()
                            if val:
                                try:
                                    line_list.append(int(val))
                                except ValueError:
                                    pass
                        if line_list:
                            main_list.append(line_list)
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

        return main_list

    def read_properties_file(self, filename: str) -> Dict[str, str]:
        """
        Read properties file (key=value format).

        Args:
            filename: Path to properties file

        Returns:
            Dictionary of key-value pairs
        """
        props: Dict[str, str] = {}

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        # Handle = in value
                        idx = line.index('=')
                        key = line[:idx].strip()
                        value = line[idx + 1:].strip()
                        props[key] = value
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

        return props

    def read_delimiter_separated_file(self, filename: str,
                                      delimiter: str = " ") -> List[str]:
        """
        Read file with delimiter-separated values.

        Args:
            filename: Path to file
            delimiter: Value separator (default: space)

        Returns:
            List of values
        """
        result_list: List[str] = []

        try:
            # Patterns to strip (matching Java regex)
            match1 = re.compile(r'^[a-zA-Z]*')
            match2 = re.compile(r'^[,._\-?]*')

            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    # Apply regex replacements
                    line = match1.sub('', line)
                    line = match2.sub('', line)

                    values = line.strip().split(delimiter)
                    for val in values:
                        val = val.strip()
                        if val:
                            result_list.append(val)
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

        return result_list

    def read_file_as_is(self, filename: str) -> str:
        """
        Read file contents as-is.

        Args:
            filename: Path to file

        Returns:
            File contents as string
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            print(f"Error reading file {filename}: {e}")
            return ""

    def read_file_as_map(self, filename: str) -> Dict[str, str]:
        """
        Read file as ordered map (key=value per line).

        Args:
            filename: Path to file

        Returns:
            Ordered dictionary of key-value pairs
        """
        main_map: Dict[str, str] = OrderedDict()

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line:
                        idx = line.index('=')
                        key = line[:idx]
                        value = line[idx + 1:]
                        main_map[key] = value
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

        return main_map

    def read_initial_properties(self, filename: str) -> Dict[str, str]:
        """
        Read initial properties from allFileList.list.

        Args:
            filename: Path to allFileList.list

        Returns:
            Dictionary mapping config keys to file paths
        """
        print(f"Loading configuration from: {filename}")
        file_map: Dict[str, str] = {}

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        parts = line.split('=', 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            file_map[key] = value
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

        print(f"Loaded {len(file_map)} file mappings")
        return file_map

    def read_simple_list_file(self, filename: str) -> List[str]:
        """
        Read file as simple list (one item per line, no regex processing).

        Args:
            filename: Path to file

        Returns:
            List of lines
        """
        result_list: List[str] = []

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        result_list.append(line)
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

        return result_list

    def read_comma_separated_file(self, filename: str) -> List[str]:
        """
        Read comma-separated file (like ignore lists).

        Args:
            filename: Path to file

        Returns:
            List of values
        """
        result_list: List[str] = []

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        values = line.split(',')
                        for val in values:
                            val = val.strip()
                            if val:
                                result_list.append(val)
        except IOError as e:
            print(f"Error reading file {filename}: {e}")

        return result_list

    def get_full_path(self, relative_path: str) -> str:
        """
        Get full path by joining with current root.

        Args:
            relative_path: Relative file path

        Returns:
            Full file path
        """
        return os.path.join(self._current_root, relative_path)

    def file_exists(self, filename: str) -> bool:
        """
        Check if file exists.

        Args:
            filename: Path to check

        Returns:
            True if file exists
        """
        return os.path.exists(filename)


# Convenience functions
def load_constant_file(filepath: str) -> List[List[str]]:
    """Load a constant file as list of lists"""
    return ConfigLoader.get_instance().read_main_constant_file_as_list(filepath)


def load_parse_order(filepath: str) -> List[List[int]]:
    """Load a parse order file as list of integer lists"""
    return ConfigLoader.get_instance().read_parse_order_file_as_list(filepath)


def load_properties(filepath: str) -> Dict[str, str]:
    """Load a properties file as dictionary"""
    return ConfigLoader.get_instance().read_properties_file(filepath)


def load_ignore_list(filepath: str) -> List[str]:
    """Load an ignore list file"""
    return ConfigLoader.get_instance().read_comma_separated_file(filepath)


# Alias for Java compatibility
class ReadConfig(ConfigLoader):
    """
    Alias for ConfigLoader to maintain Java naming compatibility.

    This is equivalent to ReadConfig.java
    """

    def get_current_root(self) -> str:
        """Get current root path (Java-style method name)"""
        return self.current_root

    @classmethod
    def get_instance(cls, root_path: Optional[str] = None) -> 'ReadConfig':
        """
        Get singleton instance of ReadConfig.

        Args:
            root_path: Optional root path override

        Returns:
            ReadConfig instance
        """
        if ConfigLoader._instance is None:
            ConfigLoader._instance = ReadConfig(root_path)
            # Try to load initial properties if available
            try:
                all_files_path = os.path.join(ConfigLoader._instance._current_root, "allFileList.list")
                if os.path.exists(all_files_path):
                    ConfigLoader._properties = ConfigLoader._instance.read_initial_properties(all_files_path)
            except Exception:
                pass

        return ConfigLoader._instance
