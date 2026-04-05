"""
File I/O Utilities - Equivalent to WriteToFile.java and ReadFromFile.java

This module provides file reading and writing utilities for Tamil NLP.

Author: Tamil Arasan
Since: Oct 25, 2017 / Apr 17, 2019
"""

import logging
import os
from typing import List, Dict, Collection, Optional, Set, Union
from pathlib import Path

logger = logging.getLogger(__name__)


class WriteToFile:
    """
    Utility class for writing data to files.

    Supports writing various data types including strings, lists, maps, and sets.
    """

    @staticmethod
    def write_to_file(content: Union[str, 'StringBuilder', List, Set, Dict],
                      file_name: Optional[str] = None,
                      append: bool = True) -> None:
        """
        Write content to a file.

        Args:
            content: Content to write (string, StringBuilder, list, set, or dict)
            file_name: Output file path (uses default if None)
            append: Whether to append to existing file
        """
        # Convert content to string if needed
        if hasattr(content, 'to_string'):
            text = content.to_string()
        elif isinstance(content, list):
            if content and isinstance(content[0], list):
                # List of lists
                text = '\n'.join(str(item) for item in content) + '\n'
            else:
                # Simple list
                text = '\n'.join(str(item) for item in content) + '\n'
        elif isinstance(content, (set, frozenset)):
            text = '\n'.join(str(item) for item in content) + '\n'
        elif isinstance(content, dict):
            lines = [f"{key},{value}" for key, value in content.items()]
            text = '\n'.join(lines) + '\n'
        else:
            text = str(content)

        # Determine file path
        if file_name is None:
            # Get default from config
            try:
                from ..config.config_loader import ReadConfig
                config = ReadConfig.get_instance()
                props = config.get_properties()
                from ..config.constants import ConfigConstants
                file_name = config.get_current_root() + props.get(ConfigConstants.RESULT_FILE_NAME, 'result.txt')
            except Exception:
                file_name = 'result.txt'
        elif not ('/' in file_name or '\\' in file_name):
            # Relative path - prepend current root
            try:
                from ..config.config_loader import ReadConfig
                config = ReadConfig.get_instance()
                file_name = config.get_current_root() + file_name
            except Exception:
                pass

        # Write to file
        mode = 'a' if append else 'w'
        try:
            with open(file_name, mode, encoding='utf-8') as f:
                f.write(text)
        except IOError as e:
            logger.error(f"Error writing to file: {e}")

    @staticmethod
    def write_word_with_collection(word: str, collection: Collection[str],
                                   file_name: str) -> None:
        """
        Write a word with its associated collection to file.

        Args:
            word: The word
            collection: Collection of associated values
            file_name: Output file path
        """
        text = f"{word},{list(collection)}\n"
        WriteToFile.write_to_file(text, file_name)

    @staticmethod
    def write_list_of_lists(list_of_list: List[List[str]],
                            file_name: str) -> None:
        """
        Write a list of lists to file.

        Args:
            list_of_list: List of string lists
            file_name: Output file path
        """
        lines = [str(lst) for lst in list_of_list]
        WriteToFile.write_to_file('\n'.join(lines) + '\n', file_name)


class ReadFromFile:
    """
    Utility class for reading data from files.

    Supports reading files as strings, lists, or maps.
    """

    def read_file_as_string(self, file_name: str) -> str:
        """
        Read entire file as a single string with spaces between lines.

        Args:
            file_name: Input file path

        Returns:
            File content as string
        """
        result = []
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                for line in f:
                    result.append(line.rstrip('\n'))
        except IOError as e:
            logger.error(f"Error reading file: {e}")

        return ' '.join(result)

    def read_file_as_list(self, file_name: str) -> List[str]:
        """
        Read file as a list of lines.

        Args:
            file_name: Input file path

        Returns:
            List of lines (stripped)
        """
        result = []
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                for line in f:
                    result.append(line.strip())
        except IOError as e:
            logger.error(f"Error reading file: {e}")

        return result

    def read_file_as_map(self, file_name: str) -> Dict[str, Optional[str]]:
        """
        Read file as a map (key from first part of '=' split).

        Args:
            file_name: Input file path

        Returns:
            Dictionary with keys from file
        """
        result = {}
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line:
                        parts = line.split('=', 1)
                        result[parts[0]] = None
        except IOError as e:
            logger.error(f"Error reading file: {e}")

        return result


class StringBuilder:
    """
    StringBuilder equivalent for Python.

    Provides mutable string building functionality.
    """

    def __init__(self):
        """Initialize empty StringBuilder."""
        self._parts: List[str] = []

    def append(self, text: str) -> 'StringBuilder':
        """
        Append text to the builder.

        Args:
            text: Text to append

        Returns:
            Self for chaining
        """
        self._parts.append(str(text))
        return self

    def to_string(self) -> str:
        """
        Get the built string.

        Returns:
            Concatenated string
        """
        return ''.join(self._parts)

    def __str__(self) -> str:
        return self.to_string()

    def __len__(self) -> int:
        return len(self.to_string())

    def clear(self) -> None:
        """Clear the builder."""
        self._parts = []
