"""
Letter grouping utilities and mappings for Tamil characters.

This module provides character mapping dictionaries and grouping functions
used for letter classification and transformation operations.
"""

from typing import Dict, List, Optional
from .tamil_letters import TamilConstants as TC


class LetterGroups:
    """
    Provides character mappings and grouping utilities for Tamil letters.
    Used for letter splitting, joining, and classification operations.
    """

    # Map character to its string representation (for splitting)
    MAP_CHARACTER: Dict[int, str] = {
        ord(' '): " ",
        TC.அ: "அ",
        TC.ஆ: "ஆ",
        TC.இ: "இ",
        TC.ஈ: "ஈ",
        TC.உ: "உ",
        TC.ஊ: "ஊ",
        TC.எ: "எ",
        TC.ஏ: "ஏ",
        TC.ஐ: "ஐ",
        TC.ஒ: "ஒ",
        TC.ஓ: "ஓ",
        TC.ஃ: "ஃ",
        0x0BBE: "ஆ்",  # Vowel sign AA
        0x0BBF: "இ்",  # Vowel sign I
        0x0BC0: "ஈ்",  # Vowel sign II
        0x0BC1: "உ்",  # Vowel sign U
        0x0BC2: "ஊ்",  # Vowel sign UU
        0x0BC6: "எ்",  # Vowel sign E
        0x0BC7: "ஏ்",  # Vowel sign EE
        0x0BC8: "ஐ்",  # Vowel sign AI
        0x0BCA: "ஒ்",  # Vowel sign O
        0x0BCB: "ஓ்",  # Vowel sign OO
        0x0B94: "ஔ",   # Vowel AU
        0x0BCD: "்",   # Virama (pulli)
    }

    # Map for forward direction (splitting)
    MAP_CHARACTER_FORWARD: Dict[int, str] = {
        ord(' '): " ",
        0x0BCD: "்",     # Virama
        0x0BBE: "்ஆ",   # Vowel sign AA
        0x0BBF: "்இ",   # Vowel sign I
        0x0BC0: "்ஈ",   # Vowel sign II
        0x0BC1: "்உ",   # Vowel sign U
        0x0BC2: "்ஊ",   # Vowel sign UU
        0x0BC6: "்எ",   # Vowel sign E
        0x0BC7: "்ஏ",   # Vowel sign EE
        0x0BC8: "்ஐ",   # Vowel sign AI
        0x0BCA: "்ஒ",   # Vowel sign O
        0x0BCB: "்ஓ",   # Vowel sign OO
        0x0BCC: "்ஔ",   # Vowel sign AU
    }

    # Map for multiple special characters
    MAP_MULTIPLE_SPECIAL_CHARACTER: Dict[str, str] = {
        "ோ": "்ஓ",
    }

    # Reverse map for joining
    REVERSE_MAP_CHARACTER: Dict[int, int] = {
        TC.அ: ord(' '),
        TC.ஆ: 0x0BBE,
        TC.இ: 0x0BBF,
        TC.ஈ: 0x0BC0,
        TC.உ: 0x0BC1,
        TC.ஊ: 0x0BC2,
        TC.எ: 0x0BC6,
        TC.ஏ: 0x0BC7,
        TC.ஐ: 0x0BC8,
        TC.ஒ: 0x0BCA,
        TC.ஓ: 0x0BCB,
        TC.ஔ: 0x0B94,
    }

    # Support characters (vowel signs)
    SUPPORT_CHARACTER: set = {
        0x0BBE, 0x0BBF, 0x0BC0, 0x0BC1, 0x0BC2, 0x0BC6,
        0x0BC7, 0x0BC8, 0x0BCA, 0x0BCB, 0x0BCD
    }

    # Support character map for combining
    SUPPORT_CHARACTER_MAP: Dict[int, Optional[int]] = {
        0x0BC6 + 0x0BBE: 0x0BCA,  # ெ + ா = ொ
        0x0BC7 + 0x0BBE: 0x0BCB,  # ே + ா = ோ
        0x0BBE + 0x0BCD: None,
    }

    # Vowel to vowel sign mapping
    VOWEL_TO_SIGN: Dict[str, str] = {
        'ஆ': '\u0BBE',
        'இ': '\u0BBF',
        'ஈ': '\u0BC0',
        'உ': '\u0BC1',
        'ஊ': '\u0BC2',
        'எ': '\u0BC6',
        'ஏ': '\u0BC7',
        'ஐ': '\u0BC8',
        'ஒ': '\u0BCA',
        'ஓ': '\u0BCB',
        'ஔ': '\u0BCC',
    }

    @classmethod
    def is_pulli(cls, char: str) -> bool:
        """Check if character is pulli (virama)"""
        if len(char) == 1:
            return ord(char) == TC.ஃ_EXT
        return False

    @classmethod
    def is_vowel(cls, char: str) -> bool:
        """Check if character is an independent vowel"""
        if len(char) == 1:
            return ord(char) in TC.UYIR_EZHUTHU
        return False

    @classmethod
    def is_consonant(cls, char: str) -> bool:
        """Check if character is a consonant"""
        if len(char) == 1:
            return ord(char) in TC.UYIRMEY_EZHUTHU
        return False

    @classmethod
    def is_vowel_sign(cls, char: str) -> bool:
        """Check if character is a dependent vowel sign"""
        if len(char) == 1:
            return ord(char) in TC.D_VOWELS
        return False

    @classmethod
    def is_support_character(cls, char: str) -> bool:
        """Check if character is a support character (vowel sign or virama)"""
        if len(char) == 1:
            return ord(char) in cls.SUPPORT_CHARACTER
        return False

    @classmethod
    def get_consonant_group(cls, char: str) -> Optional[str]:
        """Get the consonant group (வல்லினம், மெல்லினம், இடையினம்) for a character"""
        if char in TC.VALLINAM_MEY or char in TC.get_vallinam_varisai():
            return "வல்லினம்"
        elif char in TC.MELLINAM_MEY or char in TC.get_mellinam_varisai():
            return "மெல்லினம்"
        elif char in TC.IDAIYINAM_MEY or char in TC.get_idaiyinam_varisai():
            return "இடையினம்"
        return None

    @classmethod
    def get_mei_for_letter(cls, first_letter: str) -> Optional[str]:
        """
        எழுத்தின் மெய்யாடு வல்லினம் இணை
        Get the pure consonant (மெய்) form for a given letter
        """
        if first_letter in TC.KA_VARISAI:
            return "க்"
        elif first_letter in TC.CA_VARISAI:
            return "ச்"
        elif first_letter in TC.TA_VARISAI:
            return "ட்"
        elif first_letter in TC.THA_VARISAI:
            return "ந்"
        elif first_letter in TC.PA_VARISAI:
            return "ப்"
        elif first_letter in TC.RA_VARISAI:
            return "ற்"
        elif first_letter in TC.YA_VARISAI:
            return "ய்"
        elif first_letter in TC.RA2_VARISAI:
            return "ர்"
        elif first_letter in TC.LA_VARISAI:
            return "ற்"
        elif first_letter in TC.VA_VARISAI:
            return "வ்"
        elif first_letter in TC.ZHA_VARISAI:
            return "ழ்"
        elif first_letter in TC.LA2_VARISAI:
            return "ட்"
        elif first_letter in TC.NGA_VARISAI:
            return "ங்"
        elif first_letter in TC.NYA_VARISAI:
            return "ஞ்"
        elif first_letter in TC.NA_VARISAI:
            return "ட்"
        elif first_letter in TC.NDA_VARISAI:
            return "ந்"
        elif first_letter in TC.MA_VARISAI:
            return "ம்"
        elif first_letter in TC.NA2_VARISAI:
            return "ற்"
        return None

    @classmethod
    def get_mei_mellinam(cls, first_letter: str) -> Optional[str]:
        """
        எழுத்தின் மெய்யாடு மெல்லினம் இணை
        Get the soft consonant (மெல்லினம்) pairing for a letter
        """
        if first_letter in TC.KA_VARISAI:
            return "க்"
        elif first_letter in TC.CA_VARISAI:
            return "ச்"
        elif first_letter in TC.TA_VARISAI:
            return "ட்"
        elif first_letter in TC.THA_VARISAI:
            return "ந்"
        elif first_letter in TC.PA_VARISAI:
            return "ப்"
        elif first_letter in TC.RA_VARISAI:
            return "ற்"
        elif first_letter in TC.YA_VARISAI:
            return "ய்"
        elif first_letter in TC.RA2_VARISAI:
            return "ர்"
        elif first_letter in TC.LA_VARISAI:
            return "ன்"
        elif first_letter in TC.VA_VARISAI:
            return "வ்"
        elif first_letter in TC.ZHA_VARISAI:
            return "ழ்"
        elif first_letter in TC.LA2_VARISAI:
            return "ன்"
        elif first_letter in TC.NGA_VARISAI:
            return "ங்"
        elif first_letter in TC.NYA_VARISAI:
            return "ஞ்"
        elif first_letter in TC.NA_VARISAI:
            return "ட்"
        elif first_letter in TC.NDA_VARISAI:
            return "ந்"
        elif first_letter in TC.MA_VARISAI:
            return "ம்"
        elif first_letter in TC.NA2_VARISAI:
            return "ற்"
        return None
