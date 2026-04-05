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

Case suffixes are loaded from vetrumai_suffixes.list data file.

Author: Tamil Arasan
"""

import os
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

    Case suffixes are loaded from vetrumai_suffixes.list data file.
    """

    # Case names (these are grammar rules, not suffix data)
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

    # Class variable to cache loaded suffixes
    _case_suffixes_loaded = False
    _case_suffixes = {}

    @classmethod
    def _load_case_suffixes(cls):
        """Load case suffixes from vetrumai_suffixes.list data file"""
        if cls._case_suffixes_loaded:
            return

        cls._case_suffixes = {i: [] for i in range(2, 9)}

        try:
            data_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'data'
            )
            suffix_file = os.path.join(data_dir, 'vetrumai_suffixes.list')

            with open(suffix_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split(',', 1)
                    if len(parts) == 2:
                        case_num = int(parts[0].strip())
                        suffix = parts[1].strip()
                        if case_num in cls._case_suffixes:
                            cls._case_suffixes[case_num].append(suffix)

        except Exception as e:
            print(f"Error loading vetrumai_suffixes.list: {e}")

        cls._case_suffixes_loaded = True

    @classmethod
    def get_case_suffixes(cls, case_num: int) -> List[str]:
        """Get suffixes for a case number"""
        cls._load_case_suffixes()
        return cls._case_suffixes.get(case_num, [])

    @classmethod
    def analyze(cls, word: str) -> VetrumaiResult:
        """
        Analyze word for case using suffixes loaded from vetrumai_suffixes.list

        Args:
            word: Tamil word to analyze

        Returns:
            VetrumaiResult with case information
        """
        word = word.strip()
        cls._load_case_suffixes()

        # Check each case in order of specificity (longer suffixes first)
        for case_num in range(2, 9):
            suffixes = cls.get_case_suffixes(case_num)
            for suffix in sorted(suffixes, key=len, reverse=True):
                if cls._ends_with_suffix(word, suffix):
                    root, matched_suffix = cls._strip_suffix(word, suffix)
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
    def _check_case(cls, word: str, case_num: int) -> bool:
        """Check if word has a specific case suffix"""
        for suffix in cls.get_case_suffixes(case_num):
            if cls._ends_with_suffix(word, suffix):
                return True
        return False

    @classmethod
    def _split_case(cls, word: str, case_num: int) -> Tuple[str, str]:
        """Split word by case suffix"""
        for suffix in sorted(cls.get_case_suffixes(case_num), key=len, reverse=True):
            if cls._ends_with_suffix(word, suffix):
                return cls._strip_suffix(word, suffix)
        return (word, "")

    @classmethod
    def is_nominative(cls, word: str) -> bool:
        """எழுவாய் வேற்றுமையா - Usually the base form"""
        result = cls.analyze(word)
        return result.case_number == 1

    @classmethod
    def is_accusative(cls, word: str) -> bool:
        """இரண்டாம் வேற்றுமையா"""
        return cls._check_case(word, 2)

    @classmethod
    def is_instrumental(cls, word: str) -> bool:
        """மூன்றாம் வேற்றுமையா"""
        return cls._check_case(word, 3)

    @classmethod
    def is_dative(cls, word: str) -> bool:
        """நான்காம் வேற்றுமையா"""
        return cls._check_case(word, 4)

    @classmethod
    def is_ablative(cls, word: str) -> bool:
        """ஐந்தாம் வேற்றுமையா"""
        return cls._check_case(word, 5)

    @classmethod
    def is_genitive(cls, word: str) -> bool:
        """ஆறாம் வேற்றுமையா"""
        return cls._check_case(word, 6)

    @classmethod
    def is_locative(cls, word: str) -> bool:
        """ஏழாம் வேற்றுமையா"""
        return cls._check_case(word, 7)

    @classmethod
    def is_vocative(cls, word: str) -> bool:
        """விளி வேற்றுமையா"""
        return cls._check_case(word, 8)

    # ==================== Case Splitting ====================

    @classmethod
    def split_accusative(cls, word: str) -> Tuple[str, str]:
        """இரண்டாம் வேற்றுமையைப் பிரி"""
        return cls._split_case(word, 2)

    @classmethod
    def split_instrumental(cls, word: str) -> Tuple[str, str]:
        """மூன்றாம் வேற்றுமையைப் பிரி"""
        return cls._split_case(word, 3)

    @classmethod
    def split_dative(cls, word: str) -> Tuple[str, str]:
        """நான்காம் வேற்றுமையைப் பிரி"""
        return cls._split_case(word, 4)

    @classmethod
    def split_ablative(cls, word: str) -> Tuple[str, str]:
        """ஐந்தாம் வேற்றுமையைப் பிரி"""
        return cls._split_case(word, 5)

    @classmethod
    def split_genitive(cls, word: str) -> Tuple[str, str]:
        """ஆறாம் வேற்றுமையைப் பிரி"""
        return cls._split_case(word, 6)

    @classmethod
    def split_locative(cls, word: str) -> Tuple[str, str]:
        """ஏழாம் வேற்றுமையைப் பிரி"""
        return cls._split_case(word, 7)

    @classmethod
    def split_vocative(cls, word: str) -> Tuple[str, str]:
        """விளி வேற்றுமையைப் பிரி"""
        return cls._split_case(word, 8)
