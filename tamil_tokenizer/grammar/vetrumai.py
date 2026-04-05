"""
Tamil Case Analysis (வேற்றுமை)

This module provides case (வேற்றுமை) analysis for Tamil words.
All case suffix data is loaded from mainConstant.list via TamilConstantTable.
No hardcoded suffix patterns.

Author: Tamil Arasan
"""

import logging
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass
from ..constants.tamil_letters import TamilConstants as TC
from .tamil_util import TamilUtil

logger = logging.getLogger(__name__)


@dataclass
class VetrumaiResult:
    """Result of case analysis"""
    root: str
    suffix: str


# Build vowel → vowel sign map from TamilConstants (Unicode standard, not linguistic rules)
_VOWEL_SIGN_MAP = {
    chr(TC.ஐ): chr(TC.ஐ_EXT),
    chr(TC.ஆ): chr(TC.ஆ_EXT),
    chr(TC.இ): chr(TC.இ_EXT),
    chr(TC.ஈ): chr(TC.ஈ_EXT),
    chr(TC.உ): chr(TC.உ_EXT),
    chr(TC.ஊ): chr(TC.ஊ_EXT),
    chr(TC.எ): chr(TC.எ_EXT),
    chr(TC.ஏ): chr(TC.ஏ_EXT),
    chr(TC.ஒ): chr(TC.ஒ_EXT),
    chr(TC.ஓ): chr(TC.ஓ_EXT),
}


class TamilVetrumai:
    """
    Tamil case (வேற்றுமை) analyzer.
    Identifies and strips case suffixes from Tamil words.

    All suffix data loaded from mainConstant.list via TamilConstantTable.
    """

    # Class variable to cache loaded suffixes
    _loaded = False
    _case_suffixes = []       # from mainConstant.list line 14 (index 13)
    _postpositions = []       # from mainConstant.list line 16 (index 15)

    @classmethod
    def _load(cls):
        """Load case suffixes and postpositions from TamilConstantTable (mainConstant.list)"""
        if cls._loaded:
            return

        try:
            from ..config.constant_table import TamilConstantTable
            from ..config.constants import ConfigConstants

            ct = TamilConstantTable.get_instance()
            main_words, _, _ = ct.get_parse_and_main_value(
                ConfigConstants.MAIN_CONSTANT_FILE_NAME,
                ConfigConstants.PARSE_ORDER_FILE_NAME,
                ConfigConstants.MAIN_PARSE_MAP_FILE_NAME
            )

            if main_words:
                # Line 14 (index 13): case markers
                cls._case_suffixes = main_words[13] if len(main_words) > 13 else []
                # Line 16 (index 15): postpositions
                cls._postpositions = main_words[15] if len(main_words) > 15 else []

        except Exception as e:
            logger.error(f"Error loading case data: {e}")

        cls._loaded = True

    @classmethod
    def get_all_suffixes(cls) -> List[str]:
        """Get all case suffixes + postpositions from data, sorted longest first"""
        cls._load()
        return sorted(set(cls._case_suffixes + cls._postpositions), key=len, reverse=True)

    @classmethod
    def analyze(cls, word: str) -> VetrumaiResult:
        """
        Analyze word for case suffix using data from mainConstant.list.

        Uses iterative stripping: first try postposition, then case marker
        on the remainder (handles compound suffixes like க் + ஆக = க்காக).

        Args:
            word: Tamil word to analyze

        Returns:
            VetrumaiResult with root and suffix
        """
        word = word.strip()
        cls._load()

        # Pass 1: Try postposition first, then case marker on remainder
        postpositions_sorted = sorted(cls._postpositions, key=len, reverse=True)
        case_markers_sorted = sorted(cls._case_suffixes, key=len, reverse=True)

        for pp in postpositions_sorted:
            if cls._ends_with_suffix(word, pp):
                remainder, matched_pp = cls._strip_suffix(word, pp)
                if remainder:
                    # Check if remainder also ends with a case marker
                    for cm in case_markers_sorted:
                        if cls._ends_with_suffix(remainder, cm):
                            root, matched_cm = cls._strip_suffix(remainder, cm)
                            if root:
                                return VetrumaiResult(
                                    root=root,
                                    suffix=matched_cm + matched_pp
                                )
                    # Postposition alone (no case marker before it)
                    return VetrumaiResult(root=remainder, suffix=matched_pp)

        # Pass 2: Try case markers alone
        for cm in case_markers_sorted:
            if cls._ends_with_suffix(word, cm):
                root, matched_cm = cls._strip_suffix(word, cm)
                if root:
                    return VetrumaiResult(root=root, suffix=matched_cm)

        # No suffix found
        return VetrumaiResult(root=word, suffix="")

    @staticmethod
    def _ends_with_suffix(word: str, suffix: str) -> bool:
        """Check if word ends with suffix (handling vowel signs)"""
        if word.endswith(suffix):
            return True

        # Check with vowel sign variants (built from TamilConstants)
        if suffix and suffix[0] in _VOWEL_SIGN_MAP:
            attached_form = _VOWEL_SIGN_MAP[suffix[0]] + suffix[1:] if len(suffix) > 1 else _VOWEL_SIGN_MAP[suffix[0]]
            if word.endswith(attached_form):
                return True

        return False

    @staticmethod
    def _strip_suffix(word: str, suffix: str) -> Tuple[str, str]:
        """Strip suffix from word and return root and matched suffix"""
        if word.endswith(suffix):
            return (word[:-len(suffix)], suffix)

        # Handle vowel sign variants (built from TamilConstants)
        if suffix and suffix[0] in _VOWEL_SIGN_MAP:
            attached_form = _VOWEL_SIGN_MAP[suffix[0]] + suffix[1:] if len(suffix) > 1 else _VOWEL_SIGN_MAP[suffix[0]]
            if word.endswith(attached_form):
                return (word[:-len(attached_form)], suffix)

        return (word, suffix)

    @classmethod
    def has_case_suffix(cls, word: str) -> bool:
        """Check if word has any case suffix"""
        result = cls.analyze(word)
        return bool(result.suffix)

    @classmethod
    def split(cls, word: str) -> Tuple[str, str]:
        """Split word into root and case suffix"""
        result = cls.analyze(word)
        return (result.root, result.suffix)
