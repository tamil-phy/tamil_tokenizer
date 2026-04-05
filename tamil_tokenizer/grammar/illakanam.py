"""
Tamil Grammar Rules (இலக்கணம்) - Equivalent to TamilIllakanam.java

This module provides Tamil grammar analysis including:
- வேற்றுமை (Cases) analysis
- Word form identification
- Grammar pattern matching

All patterns are loaded from mainConstant.list via TamilConstantTable.
No hardcoded suffix patterns.

Author: Tamil Arasan
"""

from typing import Optional, Tuple, List
from ..constants.tamil_letters import TamilConstants as TC
from ..config.constant_table import TamilConstantTable
from ..config.constants import ConfigConstants
from .tamil_util import TamilUtil


class TamilIllakanam:
    """
    Tamil grammar analysis class.
    Provides methods for case analysis and word form identification.

    All suffix patterns are loaded from mainConstant.list data file.
    """

    # Class-level cache for loaded patterns
    _patterns_loaded = False
    _tense_markers = {}  # {tense_name: [markers]}
    _person_endings = {}  # {person_name: [endings]}
    _main_words = None

    @classmethod
    def _load_patterns(cls):
        """Load grammar patterns from TamilConstantTable (mainConstant.list)"""
        if cls._patterns_loaded:
            return

        try:
            ct = TamilConstantTable.get_instance()

            # Load main_words from the constant table
            main_words, _, _ = ct.get_parse_and_main_value(
                ConfigConstants.MAIN_CONSTANT_FILE_NAME,
                ConfigConstants.PARSE_ORDER_FILE_NAME,
                ConfigConstants.MAIN_PARSE_MAP_FILE_NAME
            )

            cls._main_words = main_words

            if main_words:
                # Line 1 (index 0): Tense markers
                # க்கின்ற்,கின்ற்,க்கிற்,கிற்,ப்ப்,ப்,ந்த்,இன்,இ,ட்,ஈ,ஊ,குவ்
                tense_line = main_words[0] if len(main_words) > 0 else []

                # Categorize tense markers based on Tamil grammar
                cls._tense_markers = {
                    "நிகழ்காலம்": [m for m in tense_line if m in ['க்கின்ற்', 'கின்ற்', 'க்கிற்', 'கிற்']],
                    "எதிர்காலம்": [m for m in tense_line if m in ['ப்ப்', 'ப்', 'வ்']],
                    "இறந்தகாலம்": [m for m in tense_line if m in ['ந்த்', 'ட்', 'த்']],
                }

                # Line 3 (index 2): Person/number endings
                # ஓன்,ஏன்,ஓம்,ஆய்,ஈர்கள்,ஈர்,ஆள்,ஆர்,ஆர்கள்,அது,அத்,அன்,அள்,அர்,ஏம்
                person_line = main_words[2] if len(main_words) > 2 else []

                cls._person_endings = {
                    "தன்மை": [e for e in person_line if e in ['ஏன்', 'ஓம்', 'ஏம்']],
                    "முன்னிலை": [e for e in person_line if e in ['ஆய்', 'ஈர்', 'ஈர்கள்']],
                    "படர்க்கை": [e for e in person_line if e in ['ஆன்', 'ஆள்', 'ஆர்', 'ஆர்கள்', 'அது', 'அன்', 'அர்']],
                }

            cls._patterns_loaded = True

        except Exception as e:
            print(f"Error loading grammar patterns: {e}")
            cls._tense_markers = {}
            cls._person_endings = {}
            cls._patterns_loaded = True

    @classmethod
    def get_tense_markers(cls, tense: str) -> List[str]:
        """Get tense markers for a specific tense"""
        cls._load_patterns()
        return cls._tense_markers.get(tense, [])

    @classmethod
    def get_person_endings(cls, person: str) -> List[str]:
        """Get person endings for a specific person"""
        cls._load_patterns()
        return cls._person_endings.get(person, [])

    @staticmethod
    def split_vetrumai(word: str) -> Tuple[str, str, str]:
        """
        வேற்றுமையைப் பிரி - Split word by case suffix

        Uses TamilVetrumai which loads suffixes from data files.

        Args:
            word: Tamil word to analyze

        Returns:
            Tuple of (root, suffix, case_type)
        """
        from .vetrumai import TamilVetrumai

        result = TamilVetrumai.analyze(word.strip())
        return (result.root, result.suffix, result.case_tamil_name)

    # ==================== Case Checks (delegate to TamilVetrumai) ====================

    @staticmethod
    def is_second_case(word: str) -> bool:
        """இரண்டாம் வேற்றுமையா"""
        from .vetrumai import TamilVetrumai
        return TamilVetrumai.is_accusative(word)

    @staticmethod
    def split_second_case(word: str) -> Tuple[str, str, str]:
        """இரண்டாம் வேற்றுமையைப் பிரி"""
        from .vetrumai import TamilVetrumai
        root, suffix = TamilVetrumai.split_accusative(word)
        return (root, suffix, "இரண்டாம் வேற்றுமை")

    @staticmethod
    def is_third_case(word: str) -> bool:
        """மூன்றாம் வேற்றுமையா"""
        from .vetrumai import TamilVetrumai
        return TamilVetrumai.is_instrumental(word)

    @staticmethod
    def split_third_case(word: str) -> Tuple[str, str, str]:
        """மூன்றாம் வேற்றுமையைப் பிரி"""
        from .vetrumai import TamilVetrumai
        root, suffix = TamilVetrumai.split_instrumental(word)
        return (root, suffix, "மூன்றாம் வேற்றுமை")

    @staticmethod
    def is_fourth_case(word: str) -> bool:
        """நான்காம் வேற்றுமையா"""
        from .vetrumai import TamilVetrumai
        return TamilVetrumai.is_dative(word)

    @staticmethod
    def split_fourth_case(word: str) -> Tuple[str, str, str]:
        """நான்காம் வேற்றுமையைப் பிரி"""
        from .vetrumai import TamilVetrumai
        root, suffix = TamilVetrumai.split_dative(word)
        return (root, suffix, "நான்காம் வேற்றுமை")

    @staticmethod
    def is_fifth_case(word: str) -> bool:
        """ஐந்தாம் வேற்றுமையா"""
        from .vetrumai import TamilVetrumai
        return TamilVetrumai.is_ablative(word)

    @staticmethod
    def split_fifth_case(word: str) -> Tuple[str, str, str]:
        """ஐந்தாம் வேற்றுமையைப் பிரி"""
        from .vetrumai import TamilVetrumai
        root, suffix = TamilVetrumai.split_ablative(word)
        return (root, suffix, "ஐந்தாம் வேற்றுமை")

    @staticmethod
    def is_sixth_case(word: str) -> bool:
        """ஆறாம் வேற்றுமையா"""
        from .vetrumai import TamilVetrumai
        return TamilVetrumai.is_genitive(word)

    @staticmethod
    def split_sixth_case(word: str) -> Tuple[str, str, str]:
        """ஆறாம் வேற்றுமையைப் பிரி"""
        from .vetrumai import TamilVetrumai
        root, suffix = TamilVetrumai.split_genitive(word)
        return (root, suffix, "ஆறாம் வேற்றுமை")

    @staticmethod
    def is_seventh_case(word: str) -> bool:
        """ஏழாம் வேற்றுமையா"""
        from .vetrumai import TamilVetrumai
        return TamilVetrumai.is_locative(word)

    @staticmethod
    def split_seventh_case(word: str) -> Tuple[str, str, str]:
        """ஏழாம் வேற்றுமையைப் பிரி"""
        from .vetrumai import TamilVetrumai
        root, suffix = TamilVetrumai.split_locative(word)
        return (root, suffix, "ஏழாம் வேற்றுமை")

    # ==================== வினா எழுத்து (Question Words) ====================

    @staticmethod
    def is_question_word(word: str) -> bool:
        """
        வினாச்சொல்லா
        Check if word is a question word
        """
        # Question endings from mainConstant.list
        TamilIllakanam._load_patterns()

        # Check question ending suffixes from data
        if TamilIllakanam._main_words and len(TamilIllakanam._main_words) > 3:
            # Line 4 (index 3): ஆ,ஓ (question endings)
            q_endings = TamilIllakanam._main_words[3] if len(TamilIllakanam._main_words) > 3 else []
            for ending in q_endings:
                if word.endswith(ending):
                    return True

        return False

    # ==================== எண் (Number) Analysis ====================

    @staticmethod
    def get_number(word: str) -> str:
        """
        எண்கள் காட்டு - Get singular/plural

        Uses plural markers from mainConstant.list
        """
        TamilIllakanam._load_patterns()

        # Line 11 (index 10): கள்,கட் (plural markers)
        if TamilIllakanam._main_words and len(TamilIllakanam._main_words) > 10:
            plural_markers = TamilIllakanam._main_words[10]
            for marker in plural_markers:
                if word.endswith(marker):
                    return "பன்மை"  # Plural

        return "ஒருமை"  # Singular

    # ==================== பால் (Gender) Analysis ====================

    @classmethod
    def get_gender(cls, word: str) -> str:
        """
        பால் காட்டு - Get gender from word ending

        Uses person endings from mainConstant.list
        """
        cls._load_patterns()
        split_word = TamilUtil.split_letters(word)

        # Get person endings and check for gender patterns
        padarkkai = cls._person_endings.get("படர்க்கை", [])

        # Check masculine (ஆன், அன்)
        for ending in padarkkai:
            if ending in ['ஆன்', 'அன்'] and split_word.endswith(ending):
                return "ஆண்பால்"

        # Check feminine (ஆள், அள்)
        for ending in padarkkai:
            if ending in ['ஆள்', 'அள்'] and split_word.endswith(ending):
                return "பெண்பால்"

        # Check rational plural (ஆர், ஆர்கள்)
        for ending in padarkkai:
            if ending in ['ஆர்', 'ஆர்கள்', 'அர்'] and split_word.endswith(ending):
                return "பலர்பால்"

        # Check neuter (அது)
        for ending in padarkkai:
            if ending in ['அது'] and split_word.endswith(ending):
                return "ஒன்றன்பால்"

        return ""

    # ==================== இடம் (Person) Analysis ====================

    @classmethod
    def get_person(cls, word: str) -> str:
        """
        படர்க்கை காட்டு - Get person (1st, 2nd, 3rd)

        Uses person endings from mainConstant.list
        """
        cls._load_patterns()
        split_word = TamilUtil.split_letters(word)

        # Check first person (தன்மை)
        for ending in cls._person_endings.get("தன்மை", []):
            if split_word.endswith(ending):
                return "தன்மை"

        # Check second person (முன்னிலை)
        for ending in cls._person_endings.get("முன்னிலை", []):
            if split_word.endswith(ending):
                return "முன்னிலை"

        # Check third person (படர்க்கை)
        for ending in cls._person_endings.get("படர்க்கை", []):
            if split_word.endswith(ending):
                return "படர்க்கை"

        return "படர்க்கை"  # Default to third person

    # ==================== காலம் (Tense) Analysis ====================

    @classmethod
    def get_tense(cls, word: str) -> str:
        """
        காலம் காட்டு - Get tense from word

        Uses tense markers from mainConstant.list
        """
        cls._load_patterns()
        split_word = TamilUtil.split_letters(word)

        # Check past tense (இறந்தகாலம்)
        for marker in cls._tense_markers.get("இறந்தகாலம்", []):
            if marker in split_word:
                return "இறந்தகாலம்"

        # Check present tense (நிகழ்காலம்)
        for marker in cls._tense_markers.get("நிகழ்காலம்", []):
            if marker in split_word:
                return "நிகழ்காலம்"

        # Check future tense (எதிர்காலம்)
        for marker in cls._tense_markers.get("எதிர்காலம்", []):
            if marker in split_word:
                return "எதிர்காலம்"

        return ""
