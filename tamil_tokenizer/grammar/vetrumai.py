"""
Tamil Case Analysis (வேற்றுமை) - Equivalent to TamilVetrumai.java

This module provides detailed case (வேற்றுமை) analysis for Tamil words.
Tamil has 8 cases:
1. எழுவாய் வேற்றுமை (Nominative)
2. இரண்டாம் வேற்றுமை (Accusative) - ஐ
3. மூன்றாம் வேற்றுமை (Instrumental) - ஆல், ஒடு, ஓடு
4. நான்காம் வேற்றுமை (Dative) - கு, க்கு
5. ஐந்தாம் வேற்றுமை (Ablative) - இன், இல், இருந்து
6. ஆறாம் வேற்றுமை (Genitive) - அது, உடைய, இன்
7. ஏழாம் வேற்றுமை (Locative) - இல், இடம், கண்
8. விளி வேற்றுமை (Vocative) - ஏ, ஆ

Author: Rajamani David (Original Java)
"""

from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass
from ..constants.tamil_letters import TamilConstants as TC
from .tamil_util import TamilUtil


@dataclass
class VetrumaiResult:
    """Result of case analysis"""
    root: str
    suffix: str
    case_number: int
    case_name: str
    case_tamil_name: str


class TamilVetrumai:
    """
    Tamil case (வேற்றுமை) analyzer.
    Identifies and strips case suffixes from Tamil words.
    """

    # Case suffix patterns
    SECOND_CASE_SUFFIXES = ["ஐ", "யை"]
    THIRD_CASE_SUFFIXES = ["ஆல்", "ஒடு", "ஓடு", "ஆன்", "உடன்"]
    FOURTH_CASE_SUFFIXES = ["கு", "க்கு", "க்குக்", "க்குச்", "க்குப்", "உக்கு"]
    FIFTH_CASE_SUFFIXES = ["இன்", "இல்", "இலிருந்து", "இனின்று", "த்தில்", "த்திலிருந்து"]
    SIXTH_CASE_SUFFIXES = ["அது", "உடைய", "இன்", "அதன்", "உடைமை"]
    SEVENTH_CASE_SUFFIXES = ["இல்", "இடம்", "கண்", "த்தில்", "இடத்தில்", "மேல்", "கீழ்"]
    EIGHTH_CASE_SUFFIXES = ["ஏ", "ஆ"]

    # Case names
    CASE_NAMES = {
        1: ("Nominative", "எழுவாய் வேற்றுமை"),
        2: ("Accusative", "இரண்டாம் வேற்றுமை"),
        3: ("Instrumental", "மூன்றாம் வேற்றுமை"),
        4: ("Dative", "நான்காம் வேற்றுமை"),
        5: ("Ablative", "ஐந்தாம் வேற்றுமை"),
        6: ("Genitive", "ஆறாம் வேற்றுமை"),
        7: ("Locative", "ஏழாம் வேற்றுமை"),
        8: ("Vocative", "விளி வேற்றுமை"),
    }

    @classmethod
    def analyze(cls, word: str) -> VetrumaiResult:
        """
        Analyze word for case

        Args:
            word: Tamil word to analyze

        Returns:
            VetrumaiResult with case information
        """
        word = word.strip()

        # Check each case in order of specificity (longer suffixes first)
        for case_num, (check_fn, split_fn, suffixes) in cls._get_case_handlers().items():
            for suffix in sorted(suffixes, key=len, reverse=True):
                if check_fn(word, suffix):
                    root, matched_suffix = split_fn(word, suffix)
                    eng_name, tamil_name = cls.CASE_NAMES[case_num]
                    return VetrumaiResult(
                        root=root,
                        suffix=matched_suffix,
                        case_number=case_num,
                        case_name=eng_name,
                        case_tamil_name=tamil_name
                    )

        # Default: Nominative (no suffix)
        return VetrumaiResult(
            root=word,
            suffix="",
            case_number=1,
            case_name="Nominative",
            case_tamil_name="எழுவாய் வேற்றுமை"
        )

    @classmethod
    def _get_case_handlers(cls) -> Dict:
        """Get handlers for each case"""
        return {
            2: (cls._ends_with_suffix, cls._strip_suffix, cls.SECOND_CASE_SUFFIXES),
            3: (cls._ends_with_suffix, cls._strip_suffix, cls.THIRD_CASE_SUFFIXES),
            4: (cls._ends_with_suffix, cls._strip_suffix, cls.FOURTH_CASE_SUFFIXES),
            5: (cls._ends_with_suffix, cls._strip_suffix, cls.FIFTH_CASE_SUFFIXES),
            6: (cls._ends_with_suffix, cls._strip_suffix, cls.SIXTH_CASE_SUFFIXES),
            7: (cls._ends_with_suffix, cls._strip_suffix, cls.SEVENTH_CASE_SUFFIXES),
            8: (cls._ends_with_suffix, cls._strip_suffix, cls.EIGHTH_CASE_SUFFIXES),
        }

    @staticmethod
    def _ends_with_suffix(word: str, suffix: str) -> bool:
        """Check if word ends with suffix (handling vowel signs)"""
        # Direct check
        if word.endswith(suffix):
            return True

        # Check with vowel sign variants
        vowel_sign_map = {
            'ஐ': 'ை',
            'ஆ': 'ா',
            'இ': 'ி',
            'ஈ': 'ீ',
            'உ': 'ு',
            'ஊ': 'ூ',
            'எ': 'ெ',
            'ஏ': 'ே',
            'ஒ': 'ொ',
            'ஓ': 'ோ',
        }

        # Convert suffix to attached vowel form if applicable
        if suffix and suffix[0] in vowel_sign_map:
            attached_form = vowel_sign_map[suffix[0]] + suffix[1:] if len(suffix) > 1 else vowel_sign_map[suffix[0]]
            if word.endswith(attached_form):
                return True

        return False

    @staticmethod
    def _strip_suffix(word: str, suffix: str) -> Tuple[str, str]:
        """Strip suffix from word and return root and matched suffix"""
        if word.endswith(suffix):
            return (word[:-len(suffix)], suffix)

        # Handle vowel sign variants
        vowel_sign_map = {
            'ஐ': 'ை',
            'ஆ': 'ா',
            'இ': 'ி',
            'ஈ': 'ீ',
            'உ': 'ு',
            'ஊ': 'ூ',
            'எ': 'ெ',
            'ஏ': 'ே',
            'ஒ': 'ொ',
            'ஓ': 'ோ',
        }

        if suffix and suffix[0] in vowel_sign_map:
            attached_len = len(suffix)
            if suffix[0] in vowel_sign_map:
                # The vowel sign is attached to previous consonant
                # We need to handle this carefully
                pass

        return (word, suffix)

    # ==================== Individual Case Checkers ====================

    @classmethod
    def is_nominative(cls, word: str) -> bool:
        """எழுவாய் வேற்றுமையா - Usually the base form"""
        result = cls.analyze(word)
        return result.case_number == 1

    @classmethod
    def is_accusative(cls, word: str) -> bool:
        """இரண்டாம் வேற்றுமையா (ஐ)"""
        for suffix in cls.SECOND_CASE_SUFFIXES:
            if cls._ends_with_suffix(word, suffix):
                return True
        return False

    @classmethod
    def is_instrumental(cls, word: str) -> bool:
        """மூன்றாம் வேற்றுமையா (ஆல், ஒடு, ஓடு)"""
        for suffix in cls.THIRD_CASE_SUFFIXES:
            if cls._ends_with_suffix(word, suffix):
                return True
        return False

    @classmethod
    def is_dative(cls, word: str) -> bool:
        """நான்காம் வேற்றுமையா (கு, க்கு)"""
        for suffix in cls.FOURTH_CASE_SUFFIXES:
            if cls._ends_with_suffix(word, suffix):
                return True
        return False

    @classmethod
    def is_ablative(cls, word: str) -> bool:
        """ஐந்தாம் வேற்றுமையா (இன், இல், இருந்து)"""
        for suffix in cls.FIFTH_CASE_SUFFIXES:
            if cls._ends_with_suffix(word, suffix):
                return True
        return False

    @classmethod
    def is_genitive(cls, word: str) -> bool:
        """ஆறாம் வேற்றுமையா (உடைய, அது)"""
        for suffix in cls.SIXTH_CASE_SUFFIXES:
            if cls._ends_with_suffix(word, suffix):
                return True
        return False

    @classmethod
    def is_locative(cls, word: str) -> bool:
        """ஏழாம் வேற்றுமையா (இல், இடம், கண்)"""
        for suffix in cls.SEVENTH_CASE_SUFFIXES:
            if cls._ends_with_suffix(word, suffix):
                return True
        return False

    @classmethod
    def is_vocative(cls, word: str) -> bool:
        """விளி வேற்றுமையா (ஏ, ஆ)"""
        for suffix in cls.EIGHTH_CASE_SUFFIXES:
            if cls._ends_with_suffix(word, suffix):
                return True
        return False

    # ==================== Case Splitting ====================

    @classmethod
    def split_accusative(cls, word: str) -> Tuple[str, str]:
        """இரண்டாம் வேற்றுமையைப் பிரி"""
        for suffix in sorted(cls.SECOND_CASE_SUFFIXES, key=len, reverse=True):
            if cls._ends_with_suffix(word, suffix):
                return cls._strip_suffix(word, suffix)
        return (word, "")

    @classmethod
    def split_instrumental(cls, word: str) -> Tuple[str, str]:
        """மூன்றாம் வேற்றுமையைப் பிரி"""
        for suffix in sorted(cls.THIRD_CASE_SUFFIXES, key=len, reverse=True):
            if cls._ends_with_suffix(word, suffix):
                return cls._strip_suffix(word, suffix)
        return (word, "")

    @classmethod
    def split_dative(cls, word: str) -> Tuple[str, str]:
        """நான்காம் வேற்றுமையைப் பிரி"""
        for suffix in sorted(cls.FOURTH_CASE_SUFFIXES, key=len, reverse=True):
            if cls._ends_with_suffix(word, suffix):
                return cls._strip_suffix(word, suffix)
        return (word, "")

    @classmethod
    def split_ablative(cls, word: str) -> Tuple[str, str]:
        """ஐந்தாம் வேற்றுமையைப் பிரி"""
        for suffix in sorted(cls.FIFTH_CASE_SUFFIXES, key=len, reverse=True):
            if cls._ends_with_suffix(word, suffix):
                return cls._strip_suffix(word, suffix)
        return (word, "")

    @classmethod
    def split_genitive(cls, word: str) -> Tuple[str, str]:
        """ஆறாம் வேற்றுமையைப் பிரி"""
        for suffix in sorted(cls.SIXTH_CASE_SUFFIXES, key=len, reverse=True):
            if cls._ends_with_suffix(word, suffix):
                return cls._strip_suffix(word, suffix)
        return (word, "")

    @classmethod
    def split_locative(cls, word: str) -> Tuple[str, str]:
        """ஏழாம் வேற்றுமையைப் பிரி"""
        for suffix in sorted(cls.SEVENTH_CASE_SUFFIXES, key=len, reverse=True):
            if cls._ends_with_suffix(word, suffix):
                return cls._strip_suffix(word, suffix)
        return (word, "")

    @classmethod
    def split_vocative(cls, word: str) -> Tuple[str, str]:
        """விளி வேற்றுமையைப் பிரி"""
        for suffix in sorted(cls.EIGHTH_CASE_SUFFIXES, key=len, reverse=True):
            if cls._ends_with_suffix(word, suffix):
                return cls._strip_suffix(word, suffix)
        return (word, "")
