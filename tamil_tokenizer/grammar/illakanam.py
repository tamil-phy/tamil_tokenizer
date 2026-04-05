"""
Tamil Grammar Rules (இலக்கணம்) - Equivalent to TamilIllakanam.java

This module provides Tamil grammar analysis including:
- வேற்றுமை (Cases) analysis
- Word form identification
- Grammar pattern matching

Author: Rajamani David (Original Java)
"""

from typing import Optional, Tuple, List
from ..constants.tamil_letters import TamilConstants as TC
from .tamil_util import TamilUtil


class TamilIllakanam:
    """
    Tamil grammar analysis class.
    Provides methods for case analysis and word form identification.
    """

    @staticmethod
    def split_vetrumai(word: str) -> Tuple[str, str, str]:
        """
        வேற்றுமையைப் பிரி - Split word by case suffix

        Analyzes the word and returns the root and case suffix.

        Args:
            word: Tamil word to analyze

        Returns:
            Tuple of (root, suffix, case_type)
        """
        word = word.strip()

        # Check each case type
        if TamilIllakanam.is_second_case(word):
            return TamilIllakanam.split_second_case(word)
        elif TamilIllakanam.is_third_case(word):
            return TamilIllakanam.split_third_case(word)
        elif TamilIllakanam.is_fourth_case(word):
            return TamilIllakanam.split_fourth_case(word)
        elif TamilIllakanam.is_fifth_case(word):
            return TamilIllakanam.split_fifth_case(word)
        elif TamilIllakanam.is_sixth_case(word):
            return TamilIllakanam.split_sixth_case(word)
        elif TamilIllakanam.is_seventh_case(word):
            return TamilIllakanam.split_seventh_case(word)

        return (word, "", "")

    # ==================== இரண்டாம் வேற்றுமை (Accusative Case) ====================

    @staticmethod
    def is_second_case(word: str) -> bool:
        """
        இரண்டாம் வேற்றுமையா
        Check if word is in accusative case (ends with ஐ)
        """
        return word.endswith("ை") or word.endswith("யை")

    @staticmethod
    def split_second_case(word: str) -> Tuple[str, str, str]:
        """
        இரண்டாம் வேற்றுமையைப் பிரி
        Split accusative case word
        """
        if word.endswith("யை"):
            return (word[:-2], "யை", "இரண்டாம் வேற்றுமை")
        elif word.endswith("ை"):
            # Find the suffix position
            idx = len(word) - 1
            # The ை is attached to the previous character
            return (word[:-1], "ஐ", "இரண்டாம் வேற்றுமை")
        return (word, "", "")

    # ==================== மூன்றாம் வேற்றுமை (Instrumental Case) ====================

    @staticmethod
    def is_third_case(word: str) -> bool:
        """
        மூன்றாம் வேற்றுமையா
        Check if word is in instrumental case (ends with ஆல், ஒடு, ஓடு, etc.)
        """
        return (word.endswith("ால்") or
                word.endswith("ொடு") or
                word.endswith("ோடு") or
                word.endswith("ான்"))

    @staticmethod
    def split_third_case(word: str) -> Tuple[str, str, str]:
        """
        மூன்றாம் வேற்றுமையைப் பிரி
        Split instrumental case word
        """
        if word.endswith("ால்"):
            return (word[:-2], "ஆல்", "மூன்றாம் வேற்றுமை")
        elif word.endswith("ொடு"):
            return (word[:-2], "ஒடு", "மூன்றாம் வேற்றுமை")
        elif word.endswith("ோடு"):
            return (word[:-2], "ஓடு", "மூன்றாம் வேற்றுமை")
        elif word.endswith("ான்"):
            return (word[:-2], "ஆன்", "மூன்றாம் வேற்றுமை")
        return (word, "", "")

    # ==================== நான்காம் வேற்றுமை (Dative Case) ====================

    @staticmethod
    def is_fourth_case(word: str) -> bool:
        """
        நான்காம் வேற்றுமையா
        Check if word is in dative case (ends with க்கு, உக்கு, etc.)
        """
        return (word.endswith("க்கு") or
                word.endswith("க்குக்") or
                word.endswith("க்குச்") or
                word.endswith("க்குப்"))

    @staticmethod
    def split_fourth_case(word: str) -> Tuple[str, str, str]:
        """
        நான்காம் வேற்றுமையைப் பிரி
        Split dative case word
        """
        if word.endswith("க்குப்"):
            return (word[:-5], "க்குப்", "நான்காம் வேற்றுமை")
        elif word.endswith("க்குக்"):
            return (word[:-5], "க்குக்", "நான்காம் வேற்றுமை")
        elif word.endswith("க்குச்"):
            return (word[:-5], "க்குச்", "நான்காம் வேற்றுமை")
        elif word.endswith("க்கு"):
            return (word[:-3], "க்கு", "நான்காம் வேற்றுமை")
        return (word, "", "")

    # ==================== ஐந்தாம் வேற்றுமை (Ablative Case) ====================

    @staticmethod
    def is_fifth_case(word: str) -> bool:
        """
        ஐந்தாம் வேற்றுமையா
        Check if word is in ablative case (ends with இன், இல், இலிருந்து, etc.)
        """
        return (word.endswith("ின்") or
                word.endswith("ில்") or
                word.endswith("த்தில்") or
                word.endswith("இலிருந்து") or
                word.endswith("யிலிருந்து") or
                word.endswith("னின்று") or
                word.endswith("னினின்று"))

    @staticmethod
    def split_fifth_case(word: str) -> Tuple[str, str, str]:
        """
        ஐந்தாம் வேற்றுமையைப் பிரி
        Split ablative case word
        """
        if word.endswith("இலிருந்து"):
            return (word[:-8], "இலிருந்து", "ஐந்தாம் வேற்றுமை")
        elif word.endswith("யிலிருந்து"):
            return (word[:-9], "யிலிருந்து", "ஐந்தாம் வேற்றுமை")
        elif word.endswith("னினின்று"):
            return (word[:-7], "னினின்று", "ஐந்தாம் வேற்றுமை")
        elif word.endswith("னின்று"):
            return (word[:-5], "னின்று", "ஐந்தாம் வேற்றுமை")
        elif word.endswith("த்தில்"):
            return (word[:-4], "த்தில்", "ஐந்தாம் வேற்றுமை")
        elif word.endswith("ில்"):
            return (word[:-2], "இல்", "ஐந்தாம் வேற்றுமை")
        elif word.endswith("ின்"):
            return (word[:-2], "இன்", "ஐந்தாம் வேற்றுமை")
        return (word, "", "")

    # ==================== ஆறாம் வேற்றுமை (Genitive Case) ====================

    @staticmethod
    def is_sixth_case(word: str) -> bool:
        """
        ஆறாம் வேற்றுமையா
        Check if word is in genitive case (possessive - அது, உடைய, etc.)
        """
        return (word.endswith("அது") or
                word.endswith("ுடைய") or
                word.endswith("உடைய") or
                word in ["என", "எனது", "உன்", "உனது", "அவன்", "அவள்", "அது", "அவர்", "நாம்", "நாங்கள்"])

    @staticmethod
    def split_sixth_case(word: str) -> Tuple[str, str, str]:
        """
        ஆறாம் வேற்றுமையைப் பிரி
        Split genitive case word
        """
        if word.endswith("ுடைய"):
            return (word[:-4], "உடைய", "ஆறாம் வேற்றுமை")
        elif word.endswith("உடைய"):
            return (word[:-4], "உடைய", "ஆறாம் வேற்றுமை")
        elif word.endswith("அது"):
            return (word[:-3], "அது", "ஆறாம் வேற்றுமை")
        return (word, "", "")

    # ==================== ஏழாம் வேற்றுமை (Locative Case) ====================

    @staticmethod
    def is_seventh_case(word: str) -> bool:
        """
        ஏழாம் வேற்றுமையா
        Check if word is in locative case (இல், கண், இடம், etc.)
        """
        return (word.endswith("ில்") or
                word.endswith("த்தில்") or
                word.endswith("கண்") or
                word.endswith("இடம்") or
                word.endswith("இடத்தில்"))

    @staticmethod
    def split_seventh_case(word: str) -> Tuple[str, str, str]:
        """
        ஏழாம் வேற்றுமையைப் பிரி
        Split locative case word
        """
        if word.endswith("இடத்தில்"):
            return (word[:-7], "இடத்தில்", "ஏழாம் வேற்றுமை")
        elif word.endswith("த்தில்"):
            return (word[:-4], "த்தில்", "ஏழாம் வேற்றுமை")
        elif word.endswith("ில்"):
            return (word[:-2], "இல்", "ஏழாம் வேற்றுமை")
        elif word.endswith("கண்"):
            return (word[:-2], "கண்", "ஏழாம் வேற்றுமை")
        elif word.endswith("இடம்"):
            return (word[:-3], "இடம்", "ஏழாம் வேற்றுமை")
        return (word, "", "")

    # ==================== வினா எழுத்து (Question Words) ====================

    @staticmethod
    def is_question_word(word: str) -> bool:
        """
        வினாச்சொல்லா
        Check if word is a question word
        """
        question_starters = ["யார்", "என்ன", "எது", "எங்கே", "எப்போது", "எப்படி", "ஏன்"]
        question_enders = ["ஆ", "ஓ"]

        for starter in question_starters:
            if word.startswith(starter):
                return True

        for ender in question_enders:
            if word.endswith(ender):
                return True

        return False

    # ==================== எண் (Number) Analysis ====================

    @staticmethod
    def get_number(word: str) -> str:
        """
        எண்கள் காட்டு - Get singular/plural
        """
        if word.endswith("கள்") or word.endswith("மார்") or word.endswith("ர்கள்"):
            return "பன்மை"  # Plural
        return "ஒருமை"  # Singular

    # ==================== பால் (Gender) Analysis ====================

    @staticmethod
    def get_gender(word: str) -> str:
        """
        பால் காட்டு - Get gender from word ending
        """
        split_word = TamilUtil.split_letters(word)

        # ஆண்பால் (Masculine)
        if split_word.endswith("ஆன்") or split_word.endswith("ன்"):
            return "ஆண்பால்"

        # பெண்பால் (Feminine)
        if split_word.endswith("ஆள்") or split_word.endswith("ள்"):
            return "பெண்பால்"

        # பலர்பால் (Rational plural)
        if (split_word.endswith("ஆர்") or split_word.endswith("மார்") or
            split_word.endswith("ர்கள்") or word.endswith("ய")):
            return "பலர்பால்"

        # ஒன்றன்பால் (Neuter singular)
        if split_word.endswith("து") or split_word.endswith("அது"):
            return "ஒன்றன்பால்"

        # பலவின்பால் (Neuter plural)
        if word.endswith("கள்") or split_word.endswith("அ"):
            return "பலவின்பால்"

        return ""

    # ==================== இடம் (Person) Analysis ====================

    @staticmethod
    def get_person(word: str) -> str:
        """
        படர்க்கை காட்டு - Get person (1st, 2nd, 3rd)
        """
        split_word = TamilUtil.split_letters(word)

        # தன்மை (First person)
        first_person_endings = ["ஏன்", "ஓம்", "ஏம்"]
        for ending in first_person_endings:
            if split_word.endswith(ending):
                return "தன்மை"

        # முன்னிலை (Second person)
        second_person_endings = ["ஆய்", "ஈர்", "ஈர்கள்"]
        for ending in second_person_endings:
            if split_word.endswith(ending):
                return "முன்னிலை"

        # படர்க்கை (Third person) - default
        third_person_endings = ["ஆன்", "ஆள்", "ஆர்", "ஆர்கள்", "அது", "அன", "அர்"]
        for ending in third_person_endings:
            if split_word.endswith(ending):
                return "படர்க்கை"

        return "படர்க்கை"  # Default to third person

    # ==================== காலம் (Tense) Analysis ====================

    @staticmethod
    def get_tense(word: str) -> str:
        """
        காலம் காட்டு - Get tense from word
        """
        split_word = TamilUtil.split_letters(word)

        # இறந்தகாலம் (Past tense)
        past_markers = ["த்த்", "ந்த்", "ட்ட்", "ற்ற்", "ன்"]
        for marker in past_markers:
            if marker in split_word:
                return "இறந்தகாலம்"

        # நிகழ்காலம் (Present tense)
        present_markers = ["கிற்", "கின்ற்", "க்கிற்", "க்கின்ற்"]
        for marker in present_markers:
            if marker in split_word:
                return "நிகழ்காலம்"

        # எதிர்காலம் (Future tense)
        future_markers = ["ப்ப்", "வ்"]
        for marker in future_markers:
            if marker in split_word:
                return "எதிர்காலம்"

        return ""
