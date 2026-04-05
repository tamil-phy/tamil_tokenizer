"""
Morphology Parser - Equivalent to MorphologyParser.java

This module orchestrates multiple parsers for comprehensive
Tamil morphological analysis.

Author: Tamil Arasan
Since: Jun 7, 2020
"""

import logging
from typing import Dict, List, Optional
from .word_parser_interface import WordParserInterface

logger = logging.getLogger(__name__)
from .parser_enum import ParserEnum
from ..utils.tamil_ngram import TamilNGram
from ..utils.word_class import WordClass
from ..utils.word_splitter import WordSplitter
from ..utils.file_io import WriteToFile
from ..config.config_loader import ReadConfig
from ..config.constants import ConfigConstants


class MorphologyParser:
    """
    Orchestrates multiple parsers for morphological analysis.

    Uses a chain of parsers to analyze Tamil words from different
    perspectives (symbols, language, numbers, verbs, nouns, etc.).
    """

    def __init__(self):
        """Initialize the morphology parser."""
        self.gram_list_of_list: Optional[List[List[str]]] = None
        self.list_of_parser: List[WordParserInterface] = []

    def get_gram_list(self) -> Optional[List[List[str]]]:
        """Get the N-gram list of lists."""
        return self.gram_list_of_list

    def create_ngrams(self, str_list: List[str], gram: int) -> None:
        """
        Create word N-grams from a list of words.

        Args:
            str_list: List of words
            gram: N-gram size
        """
        self.gram_list_of_list = TamilNGram.create_word_gram_from_list(str_list, gram)

    def create_ngrams_from_string(self, text: str, gram: int) -> None:
        """
        Create word N-grams from text.

        Args:
            text: Input text
            gram: N-gram size
        """
        self.gram_list_of_list = TamilNGram.create_word_gram(text, " \r\n", gram)

    def build_parser(self, parser_list: List[ParserEnum]) -> None:
        """
        Build parser chain from enum list.

        Args:
            parser_list: List of parser enums to use
        """
        # Import here to avoid circular imports
        from .verb_parser import VerbParser
        from .noun_parser import NounParser
        from .unicode_language_parser import UnicodeLanguageParser
        from .twin_word_parser import TwinWordParser
        from .number_parser import NumberParser
        from .symbol_parser import SymbolParser
        from .other_grammar_parser import OtherGrammarParser

        for pe in parser_list:
            if pe == ParserEnum.VerbParser:
                self.list_of_parser.append(VerbParser())
            elif pe == ParserEnum.NounParser:
                self.list_of_parser.append(NounParser())
            elif pe == ParserEnum.UnicodeLanguageParser:
                self.list_of_parser.append(UnicodeLanguageParser())
            elif pe == ParserEnum.TwinWordParser:
                self.list_of_parser.append(TwinWordParser())
            elif pe == ParserEnum.NumberParser:
                self.list_of_parser.append(NumberParser())
            elif pe == ParserEnum.SymbolParser:
                self.list_of_parser.append(SymbolParser())
            elif pe == ParserEnum.OtherGrammarParser:
                self.list_of_parser.append(OtherGrammarParser())

    def build_default_parser(self) -> None:
        """Build the default parser chain."""
        from .verb_parser import VerbParser
        from .noun_parser import NounParser
        from .unicode_language_parser import UnicodeLanguageParser
        from .number_parser import NumberParser
        from .symbol_parser import SymbolParser
        from .other_grammar_parser import OtherGrammarParser

        self.list_of_parser.append(SymbolParser())
        self.list_of_parser.append(UnicodeLanguageParser())
        self.list_of_parser.append(OtherGrammarParser())
        self.list_of_parser.append(NumberParser())
        self.list_of_parser.append(VerbParser())
        self.list_of_parser.append(NounParser())

    def run_parsers(self, word: str) -> List[WordClass]:
        """
        Run all parsers on a single word.

        Args:
            word: Word to analyze

        Returns:
            List of WordClass results
        """
        wp_possible_list: List[WordClass] = []
        wp_final_list: List[WordClass] = []
        word_type = "NA"

        for cp in self.list_of_parser:
            if word_type == "NA":
                wp_list = cp.create_single_instance(word, True)

                if wp_list:
                    for wc in wp_list:
                        wp_possible_list.append(wc)

                        wc_type = wc.get_type()
                        wc_sub_type = wc.get_sub_type()

                        if wc_type != "NA" or (wc_sub_type and wc_sub_type == "NA"):
                            flag = False
                            wp_final_list.append(wc)

                            raw_list_of_list = wc.get_raw_split_list()
                            if raw_list_of_list:
                                for raw_list in raw_list_of_list:
                                    if raw_list and len(raw_list) > 0:
                                        first_item = raw_list[0]
                                        if wc_type == "V" and cp.is_in_noun_list(first_item):
                                            flag = True
                                        if wc_type == "N" and cp.is_in_verb_list(first_item):
                                            flag = True
                                        if wc_sub_type and wc_sub_type == "NA":
                                            flag = True

                            if not flag:
                                word_type = wc_type
                                break

        if not wp_final_list:
            wp_final_list.extend(wp_possible_list)

        return wp_final_list

    def run_parsers_on_list(self, str_list_of_list: List[List[str]]) -> List[WordClass]:
        """
        Run parsers on a list of word lists (N-grams).

        Args:
            str_list_of_list: List of word lists

        Returns:
            List of WordClass results
        """
        from .core_parser import CoreParser

        my_sort_list: List[WordClass] = []
        my_final_list: List[WordClass] = []

        for str_list in str_list_of_list:
            word_type = "NA"
            CoreParser.EXIT_LOOP = 20000000

            if not str_list:
                continue

            word = str_list[0]

            for cp in self.list_of_parser:
                if word_type == "NA":
                    logger.debug(f"{cp.get_parser_type()}:{word}")
                    wp_list = cp.create_single_instance(word, True)

                    if wp_list:
                        for wc in wp_list:
                            my_sort_list.append(wc)

                            wc_type = wc.get_type()
                            wc_sub_type = wc.get_sub_type()

                            if wc_type != "NA" or (wc_sub_type and wc_sub_type == "NA"):
                                flag = False
                                raw_list_of_list = wc.get_raw_split_list()

                                if raw_list_of_list:
                                    for raw_list in raw_list_of_list:
                                        if raw_list and len(raw_list) > 0:
                                            first_item = raw_list[0]
                                            if wc_type == "V" and cp.is_in_noun_list(first_item):
                                                flag = True
                                            if wc_type == "N" and cp.is_in_verb_list(first_item):
                                                flag = True
                                            if wc_sub_type and wc_sub_type == "NA":
                                                flag = True

                                if not flag:
                                    word_type = wc_type
                                    break

                        if word_type != "NA":
                            break

        return my_final_list

    def write_other_files(self, my_sort_list: List[WordClass]) -> None:
        """
        Write analysis results to multiple files.

        Args:
            my_sort_list: List of analyzed words
        """
        sb1_lines = []
        sb2_lines = []
        sb3_lines = []
        sb4_lines = []

        for wc in my_sort_list:
            sb1_lines.append(f"{wc.get_word()}:{wc.get_raw_split_list()}")

            map_vals = wc.get_map_vals().copy() if wc.get_map_vals() else {}
            map_vals.pop("Type", None)
            map_vals.pop("Key", None)
            sb2_lines.append(f"{wc.get_word()}:{map_vals}")

            sb3_lines.append(f"{wc.get_word()}:{wc.get_splitted_val()}")

            if wc.get_type() == "NA":
                sb4_lines.append(f"{wc.get_word()}:{wc.get_splitted_val()}")

        WriteToFile.write_to_file('\n'.join(sb1_lines) + '\n', "correctParser.txt")
        WriteToFile.write_to_file('\n'.join(sb2_lines) + '\n', "grammarWithNo.txt")
        WriteToFile.write_to_file('\n'.join(sb3_lines) + '\n', "suffixWithGrammar.txt")
        WriteToFile.write_to_file('\n'.join(sb4_lines) + '\n', "incorrectParser.txt")

    def read_file(self) -> str:
        """
        Read the word list file.

        Returns:
            File contents as string
        """
        try:
            config = ReadConfig.get_instance()
            props = config.get_properties()
            word_list_file = props.get(ConfigConstants.WORD_LIST_FILE_NAME, '')
            current_root = config.get_current_root()
            return config.read_file_as_is(current_root + word_list_file)
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return ""

    def create_ngram_analysis(self, ngram_value: int) -> None:
        """
        Create N-gram analysis from word list file.

        Args:
            ngram_value: N-gram size
        """
        import time

        begin_millis = time.time() * 1000

        file_str = self.read_file()
        splitter = WordSplitter()
        str_list = splitter.split_words(file_str)

        self.create_ngrams(str_list, ngram_value)
        self.build_default_parser()
        self.run_parsers_on_list(self.get_gram_list())

        end_millis = time.time() * 1000 - begin_millis
        logger.debug(f"End: {end_millis}")

    def create_parser(self, word: str, parser_list: List[ParserEnum]) -> List[WordClass]:
        """
        Create parser and analyze a word.

        Args:
            word: Word to analyze
            parser_list: List of parsers to use

        Returns:
            List of WordClass results
        """
        mp = MorphologyParser()
        mp.build_parser(parser_list)
        return mp.run_parsers(word)


if __name__ == "__main__":
    mp = MorphologyParser()
    mp.create_ngram_analysis(1)
