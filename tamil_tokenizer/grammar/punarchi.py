"""
Tamil Sandhi Rules (புணர்ச்சி) - Equivalent to TamilPunarchi.java

This module handles Tamil sandhi (word joining) rules including:
- உடம்படுமெய் (Glide insertion)
- வல்லின மிகல் (Hard consonant doubling)
- மெய்யீறு (Consonant-ending sandhi)

Author: Tamil Arasan
"""

from typing import Tuple, Optional, List
from ..constants.tamil_letters import TamilConstants as TC
from .tamil_util import TamilUtil


class TamilPunarchi:
    """
    Tamil sandhi (புணர்ச்சி) rule handler.
    Implements rules for joining Tamil words according to traditional grammar.
    """

    @staticmethod
    def join_words(word1: str, word2: str) -> str:
        """
        இரு சொற்களை புணர்
        Join two words applying appropriate sandhi rules

        Args:
            word1: First word (நிலைமொழி)
            word2: Second word (வருமொழி)

        Returns:
            Joined word with sandhi applied
        """
        if not word1 or not word2:
            return (word1 or "") + (word2 or "")

        # Get split forms for analysis
        split1 = TamilUtil.split_letters(word1)
        split2 = TamilUtil.split_letters(word2)

        # Check last char of first word and first char of second word
        last_char_code = ord(split1[-1]) if split1 else 0
        first_char_code = ord(split2[0]) if split2 else 0

        # உடம்படுமெய் - Glide insertion when both are vowels
        if TamilPunarchi._is_vowel_ending(split1) and TamilPunarchi._is_vowel_starting(split2):
            return TamilPunarchi._apply_udampadumei(word1, word2, split1, split2)

        # வல்லின மிகல் - Hard consonant doubling
        if TamilPunarchi._needs_vallinam_mikal(split1, split2):
            return TamilPunarchi._apply_vallinam_mikal(word1, word2)

        # Simple concatenation if no special rules apply
        return word1 + word2

    @staticmethod
    def split_sandhi(word: str) -> Tuple[str, str]:
        """
        புணர்ச்சியைப் பிரி
        Split a sandhi-joined word back to its components

        Args:
            word: Combined word

        Returns:
            Tuple of (word1, word2)
        """
        # This is complex and context-dependent
        # Basic implementation - check common patterns
        split_word = TamilUtil.split_letters(word)

        # Check for ய் insertion
        if "ய்" in split_word:
            idx = split_word.find("ய்")
            # Check if this is a sandhi ய்
            before = split_word[:idx]
            after = split_word[idx + 2:]
            if before and after:
                before_joined = TamilUtil.join_letters(before)
                after_joined = TamilUtil.join_letters(after)
                return (before_joined, after_joined)

        # Check for வ் insertion
        if "வ்" in split_word:
            idx = split_word.find("வ்")
            before = split_word[:idx]
            after = split_word[idx + 2:]
            if before and after:
                before_joined = TamilUtil.join_letters(before)
                after_joined = TamilUtil.join_letters(after)
                return (before_joined, after_joined)

        return (word, "")

    @staticmethod
    def _is_vowel_ending(split_word: str) -> bool:
        """Check if word ends with a vowel"""
        if not split_word:
            return False
        last_char = ord(split_word[-1])
        return last_char in TC.UYIR_EZHUTHU_MUDIKIRATHA

    @staticmethod
    def _is_vowel_starting(split_word: str) -> bool:
        """Check if word starts with a vowel"""
        if not split_word:
            return False
        first_char = ord(split_word[0])
        return first_char in TC.UYIR_EZHUTHU_MUDIKIRATHA

    @staticmethod
    def _apply_udampadumei(word1: str, word2: str, split1: str, split2: str) -> str:
        """
        உடம்படுமெய் - Apply glide insertion rule

        When நிலைமொழி ends with vowel and வருமொழி starts with vowel:
        - இ, ஈ, ஐ, ஓ endings get ய்
        - அ, ஆ, உ, ஊ, எ, ஏ, ஒ, ஔ endings get வ்
        """
        last_char = ord(split1[-1])

        # ய் insertion for இ, ஈ, ஐ, ஓ
        if last_char in TC.YA_NILAI_MOZHIYIN_IRU:
            return TamilUtil.join_letters(split1 + "ய்" + split2)

        # வ் insertion for அ, ஆ, உ, ஊ, எ, ஏ, ஒ, ஔ
        if last_char in TC.VA_NILAI_MOZHIYIN_IRU:
            return TamilUtil.join_letters(split1 + "வ்" + split2)

        return word1 + word2

    @staticmethod
    def _needs_vallinam_mikal(split1: str, split2: str) -> bool:
        """
        Check if vallinam mikal (வல்லின மிகல்) is needed

        Conditions:
        - நிலைமொழி ends with certain patterns
        - வருமொழி starts with வல்லினம்
        """
        if not split1 or not split2:
            return False

        # Check if வருமொழி starts with வல்லினம்
        first_char = split2[0] if split2 else ''
        first_in_vallinam = first_char in [chr(c) for c in TC.VALLINAM]

        if not first_in_vallinam:
            return False

        # Check நிலைமொழி patterns that trigger வல்லின மிகல்
        # 1. Ends with றை, லை, ளை (second case ending)
        if split1.endswith("ஐ"):
            return True

        # 2. Ends with ஆ (question form)
        if split1.endswith("ஆ"):
            return True

        # 3. Various other patterns
        trigger_endings = ["து", "று", "ளி", "ணி", "ம்"]
        for ending in trigger_endings:
            if split1.endswith(ending):
                return True

        return False

    @staticmethod
    def _apply_vallinam_mikal(word1: str, word2: str) -> str:
        """
        வல்லின மிகல் - Apply hard consonant doubling

        Doubles the initial consonant of வருமொழி
        """
        if not word2:
            return word1

        first_char = word2[0]
        first_char_code = ord(first_char)

        # Map consonant to its pure form for doubling
        doubling_map = {
            TC.க: TC.க்,
            TC.ச: TC.ச்,
            TC.ட: TC.ட்,
            TC.த: TC.த்,
            TC.ப: TC.ப்,
            TC.ற: TC.ற்,
        }

        if first_char_code in doubling_map:
            return word1 + doubling_map[first_char_code] + word2

        return word1 + word2

    # ==================== Specific Sandhi Types ====================

    @staticmethod
    def is_ina_punarchi(word: str) -> bool:
        """
        இன புணர்ச்சியா
        Check if word contains cognate consonant cluster (இன மெய்)
        """
        ina_patterns = TC.INA_EZHUTHU
        for pattern in ina_patterns:
            if pattern in word:
                return True
        return False

    @staticmethod
    def is_mei_mayakkam(word: str) -> Tuple[bool, str]:
        """
        மெய்ம்மயக்கமா
        Check if word contains consonant cluster (மெய்ம்மயக்கம்)

        Returns:
            Tuple of (is_mayakkam, type)
        """
        # உடனிலை மெய்ம்மயக்கம் (same consonant)
        for pattern in TC.UDAN_NILAI_MEY_MAYAKKAM:
            if pattern in word:
                return (True, "உடனிலை")

        # வேற்றுநிலை மெய்ம்மயக்கம் (different consonants)
        split_word = TamilUtil.split_letters(word)
        for i in range(len(split_word) - 3):
            if (split_word[i + 1:i + 2] == chr(TC.ஃ_EXT) and
                split_word[i + 3:i + 4] == chr(TC.ஃ_EXT) and
                split_word[i] != split_word[i + 2]):
                return (True, "வேற்றுநிலை")

        return (False, "")

    @staticmethod
    def get_ina_mei(consonant: str) -> Optional[str]:
        """
        இன மெய் கொடு
        Get the cognate nasal for a hard consonant

        Args:
            consonant: Hard consonant (க, ச, ட, த, ப, ற)

        Returns:
            Corresponding nasal (ங, ஞ, ண, ந, ம, ன)
        """
        ina_map = {
            'க': 'ங்',
            'ச': 'ஞ்',
            'ட': 'ண்',
            'த': 'ந்',
            'ப': 'ம்',
            'ற': 'ன்',
            'க்': 'ங்',
            'ச்': 'ஞ்',
            'ட்': 'ண்',
            'த்': 'ந்',
            'ப்': 'ம்',
            'ற்': 'ன்',
        }
        return ina_map.get(consonant)

    @staticmethod
    def apply_rule(word1: str, word2: str, rule_type: str) -> str:
        """
        Apply a specific sandhi rule

        Args:
            word1: First word
            word2: Second word
            rule_type: Type of rule to apply

        Returns:
            Result of applying the rule
        """
        if rule_type == "udampadumei":
            split1 = TamilUtil.split_letters(word1)
            split2 = TamilUtil.split_letters(word2)
            return TamilPunarchi._apply_udampadumei(word1, word2, split1, split2)
        elif rule_type == "vallinam_mikal":
            return TamilPunarchi._apply_vallinam_mikal(word1, word2)
        elif rule_type == "ina_punarchi":
            # Insert cognate nasal before hard consonant
            if word2:
                first_char = word2[0]
                ina_mei = TamilPunarchi.get_ina_mei(first_char)
                if ina_mei:
                    return word1 + ina_mei + word2
        return word1 + word2
