"""
Tamil Word N-Gram Writer - Equivalent to TamilWordNGramWriter.java

This module builds and writes word N-grams with frequency counts.

Author: Tamil Arasan
"""

import logging
from typing import Dict, List
from .tamil_ngram import TamilNGram

logger = logging.getLogger(__name__)
from .file_io import ReadFromFile, WriteToFile


class TamilWordNGramWriter:
    """
    Build and write word N-grams with frequency analysis.
    """

    def __init__(self):
        """Initialize the N-gram writer."""
        self.frequency: Dict[str, int] = {}

    def read_file(self, file_name: str) -> str:
        """
        Read file contents as string.

        Args:
            file_name: Input file path

        Returns:
            File contents
        """
        rff = ReadFromFile()
        return rff.read_file_as_string(file_name)

    def build_ngram(self, input_file: str, output_file: str, ngram: int) -> None:
        """
        Build N-gram frequency map and write to file.

        Args:
            input_file: Input file path
            output_file: Output file path
            ngram: N-gram size
        """
        text = self.read_file(input_file)
        self.frequency = {}

        list_of_list = TamilNGram.create_word_gram(text, " \r\n", ngram)

        for word_list in list_of_list:
            key = str(word_list)
            counter = self.frequency.get(key, 0)
            self.frequency[key] = counter + 1

        self.write_file_map(self.frequency, output_file)

    def write_file_map(self, freq_map: Dict[str, int], file_name: str) -> None:
        """
        Write frequency map to file.

        Args:
            freq_map: Frequency dictionary
            file_name: Output file path
        """
        WriteToFile.write_to_file(freq_map, file_name)

    def write_file_list(self, final_set: List[List[str]], file_name: str) -> None:
        """
        Write list of lists to file.

        Args:
            final_set: List of word lists
            file_name: Output file path
        """
        WriteToFile.write_list_of_lists(final_set, file_name)


if __name__ == "__main__":
    # Example usage with sample files
    # This would need actual file paths to run

    file_list = [
        "pmuni0169_01_01",
        "pmuni0169_01_02",
        # ... more files
    ]

    writer = TamilWordNGramWriter()

    for ngram_size in range(3, 6):
        for file_name in file_list:
            input_path = f"C:/raj/Documents/Documents/ponnyin_selvan/{file_name}.txt"
            output_path = f"C:/raj/Documents/Documents/ponnyin_selvan/{file_name}_{ngram_size}_gram.txt"
            try:
                writer.build_ngram(input_path, output_path, ngram_size)
            except FileNotFoundError:
                logger.error(f"File not found: {input_path}")
