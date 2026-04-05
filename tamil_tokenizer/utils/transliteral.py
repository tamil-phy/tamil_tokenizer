"""
Transliteral Convertor and Util - Equivalent to TransliteralConvertor.java and TransliteralUtil.java

This module provides transliteration functionality for converting between
English transliteral representation and Tamil script.

Example:
    peVN -> பெண்
    neram -> நேரம்

Author: Tamil Arasan
Since: Nov 30, 2017
"""

import logging
import os
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class TransliteralUtil:
    """
    Utility for transliterating text using a mapping configuration.

    Translates each letter pattern to another style based on the given map.
    """

    def __init__(self, mapping: Dict[str, str]):
        """
        Initialize with transliteration mapping.

        Args:
            mapping: Dictionary mapping source patterns to target patterns
        """
        self.mapping = mapping

    def n_gram(self, word: str, start: int, end: int) -> Optional[str]:
        """
        Get transliteration for a substring.

        Args:
            word: Source word
            start: Start index
            end: End index

        Returns:
            Transliterated value or None
        """
        value = word[start:end]
        return self.mapping.get(value)

    def n_gram_convert(self, word: str, n: int = 5) -> str:
        """
        Convert a word using N-gram based transliteration.

        Tries to match the longest possible pattern first,
        then falls back to shorter patterns.

        Args:
            word: Source word to transliterate
            n: Maximum N-gram size to try

        Returns:
            Transliterated word
        """
        total_length = len(word)
        start = 0
        end = n
        result = []
        counter_map: Dict[str, int] = {}

        while start != total_length:
            try:
                if end >= total_length:
                    end = total_length

                counter_key = f"{start}:{end}"
                counter = counter_map.get(counter_key, 0)

                if counter > 1:
                    return f"{word} has issue."
                if start >= end:
                    return f"{word} has issues."

                counter_map[counter_key] = counter + 1
                value = self.n_gram(word, start, end)

                if value is not None:
                    result.append(value)
                    start = end
                    end = end + n
                else:
                    if end - 1 != 0:
                        end = end - 1
            except Exception as e:
                logger.error(f"Error processing {word}: {e}")

        return ''.join(result)

    def store_words(self, word_list: List[str], file_name: str) -> None:
        """
        Process and store transliterated words to file.

        Args:
            word_list: List of words to transliterate
            file_name: Output file path
        """
        from .file_io import WriteToFile

        match_pattern = r"^[,._-_?!)]*"
        counter = 0
        lines = []

        for word in word_list:
            if counter < 1000:
                try:
                    import re
                    word = re.sub(match_pattern, '', word)
                    word = word.replace(".", "")
                    word = word.replace(")", "")
                    word = word.replace("`", "")
                    word = word.replace("'", "")
                    word = word.replace("-", " ")
                    word = word.replace("–", " ")

                    converted = self.n_gram_convert(word.strip(), 5)
                    lines.append(f"{word}:{converted}")
                    counter += 1
                except Exception as e:
                    logger.error(f"{counter}:{word}")
                    logger.error(e)
            else:
                WriteToFile.write_to_file('\n'.join(lines) + '\n', file_name)
                lines = []
                counter = 0

        if lines:
            WriteToFile.write_to_file('\n'.join(lines) + '\n', file_name)

    def read_delimiter_separated_file(self, file_name: str) -> List[str]:
        """
        Read a file and split by spaces.

        Args:
            file_name: Input file path

        Returns:
            List of words from the file
        """
        ignore_list = []
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                for line in f:
                    values = line.strip().split(' ')
                    ignore_list.extend(values)
        except IOError as e:
            logger.error(e)

        return ignore_list


class TransliteralConvertor:
    """
    Main converter class for transliteration.

    Loads configuration and coordinates the conversion process.
    """

    def __init__(self):
        """Initialize the converter."""
        self.mapping: Dict[str, str] = {}

    def load(self, config_file_name: str) -> Dict[str, str]:
        """
        Load transliteration mapping from config file.

        Config file format: key=value per line

        Args:
            config_file_name: Path to configuration file

        Returns:
            Dictionary with transliteration mappings
        """
        mapping = {}
        try:
            with open(config_file_name, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line:
                        key, value = line.split('=', 1)
                        mapping[key] = value
        except IOError as e:
            logger.error(f"Error loading config: {e}")

        return mapping

    def convert_file(self, config_file: str, input_file: str, output_file: str) -> None:
        """
        Convert an entire file using transliteration.

        Args:
            config_file: Path to configuration file
            input_file: Path to input file
            output_file: Path to output file
        """
        mapping = self.load(config_file)
        util = TransliteralUtil(mapping)
        word_list = util.read_delimiter_separated_file(input_file)
        util.store_words(word_list, output_file)


def print_usage():
    """Print usage instructions."""
    logger.info("-----------Usage---------------------")
    logger.info("Command Line params should include -Dfile.encoding=UTF-8")
    logger.info("Three files - Config, Input and Output all files are mandatory.")
    logger.info("1. Config file should contain key=value per row.")
    logger.info("2. Input file should contain English transliteral or Tamil word to convert.")
    logger.info("3. Output file can be empty file or file to append for collecting results.")
    logger.info("-----------Usage---------------------")


def main():
    """Main entry point for command line usage."""
    import sys

    if len(sys.argv) < 4:
        print_usage()
        return

    config_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    convertor = TransliteralConvertor()
    convertor.convert_file(config_file, input_file, output_file)


if __name__ == "__main__":
    main()
