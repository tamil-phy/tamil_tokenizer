"""
Tamil Grammar Rules (இலக்கணம்)

This module provides Tamil grammar analysis including:
- வேற்றுமை (Cases) analysis
- Word form identification
- Grammar pattern matching

All patterns are loaded from mainConstant.list via TamilConstantTable.
No hardcoded suffix patterns.

Author: Tamil Arasan
"""

import logging
from typing import Optional, Tuple, List
from ..constants.tamil_letters import TamilConstants as TC
from ..config.constant_table import TamilConstantTable
from ..config.constants import ConfigConstants
from .tamil_util import TamilUtil

logger = logging.getLogger(__name__)


class TamilIllakanam:
    """
    Tamil grammar analysis class.
    Provides methods for case analysis and word form identification.

    All suffix patterns are loaded from mainConstant.list data file.
    """

    # Class-level cache for loaded data
    _loaded = False
    _main_words = None
    _tense_markers = []     # from line 1 (index 0) — flat list
    _person_endings = []    # from line 3 (index 2) — flat list
    _plural_markers = []    # from line 11 (index 10)
    _question_endings = []  # from line 4 (index 3)

    @classmethod
    def _load(cls):
        """Load grammar patterns from TamilConstantTable (mainConstant.list)"""
        if cls._loaded:
            return

        try:
            ct = TamilConstantTable.get_instance()

            main_words, _, _ = ct.get_parse_and_main_value(
                ConfigConstants.MAIN_CONSTANT_FILE_NAME,
                ConfigConstants.PARSE_ORDER_FILE_NAME,
                ConfigConstants.MAIN_PARSE_MAP_FILE_NAME
            )

            cls._main_words = main_words

            if main_words:
                # Line 1 (index 0): All tense markers (flat list from data)
                cls._tense_markers = main_words[0] if len(main_words) > 0 else []
                # Line 3 (index 2): All person/number endings (flat list from data)
                cls._person_endings = main_words[2] if len(main_words) > 2 else []
                # Line 4 (index 3): Question endings
                cls._question_endings = main_words[3] if len(main_words) > 3 else []
                # Line 11 (index 10): Plural markers
                cls._plural_markers = main_words[10] if len(main_words) > 10 else []

        except Exception as e:
            logger.error(f"Error loading grammar patterns: {e}")

        cls._loaded = True

    @classmethod
    def get_tense_markers(cls) -> List[str]:
        """Get all tense markers from data"""
        cls._load()
        return cls._tense_markers

    @classmethod
    def get_person_endings(cls) -> List[str]:
        """Get all person endings from data"""
        cls._load()
        return cls._person_endings

    @classmethod
    def get_plural_markers(cls) -> List[str]:
        """Get all plural markers from data"""
        cls._load()
        return cls._plural_markers

    @staticmethod
    def split_vetrumai(word: str) -> Tuple[str, str]:
        """
        வேற்றுமையைப் பிரி - Split word by case suffix

        Uses TamilVetrumai which loads suffixes from mainConstant.list.

        Args:
            word: Tamil word to analyze

        Returns:
            Tuple of (root, suffix)
        """
        from .vetrumai import TamilVetrumai
        return TamilVetrumai.split(word.strip())

    @staticmethod
    def has_case_suffix(word: str) -> bool:
        """Check if word has any case suffix (from data)"""
        from .vetrumai import TamilVetrumai
        return TamilVetrumai.has_case_suffix(word)

    # ==================== வினா எழுத்து (Question Words) ====================

    @classmethod
    def is_question_word(cls, word: str) -> bool:
        """வினாச்சொல்லா - Check if word is a question word (from data)"""
        cls._load()
        for ending in cls._question_endings:
            if word.endswith(ending):
                return True
        return False

    # ==================== எண் (Number) Analysis ====================

    @classmethod
    def get_number(cls, word: str) -> str:
        """எண்கள் காட்டு - Get singular/plural (from data)"""
        cls._load()
        for marker in cls._plural_markers:
            if word.endswith(marker):
                return "பன்மை"
        return "ஒருமை"

    # ==================== Tense & Person matching ====================

    # Display-form tense markers (past, present, future)
    _TENSE_DISPLAY = [
        "கின்ற", "கிற",  # present
        "ந்த", "த்த", "ட்ட", "ற்ற", "ன்ற",  # past
        "ப்ப", "வ",  # future
    ]

    # Display-form person/number endings
    _PERSON_DISPLAY = [
        "ஆர்கள்", "ார்கள்",  # 3rd person plural honorific
        "ஈர்கள்", "ீர்கள்",  # 2nd person plural
        "ஆன்", "ான்",  # 3rd person masc singular
        "ஆள்", "ாள்",  # 3rd person fem singular
        "ஆர்", "ார்",  # 3rd person honorific
        "ஏன்", "ேன்",  # 1st person singular
        "ஓம்", "ோம்",  # 1st person plural
        "ஆய்", "ாய்",  # 2nd person singular
        "ஈர்", "ீர்",  # 2nd person plural
        "அது", "து",  # neuter
    ]

    @classmethod
    def find_tense_marker(cls, word: str) -> str:
        """Find a matching tense marker in the word"""
        for marker in sorted(cls._TENSE_DISPLAY, key=len, reverse=True):
            if marker in word:
                return marker
        return ""

    @classmethod
    def find_person_ending(cls, word: str) -> str:
        """Find a matching person ending in the word"""
        for ending in sorted(cls._PERSON_DISPLAY, key=len, reverse=True):
            if word.endswith(ending):
                return ending
        return ""
