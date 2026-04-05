"""
Tamil Utility Functions - Equivalent to TamilUtil.java

This module provides core utility functions for Tamil text processing including:
- Letter splitting (எழுத்துகளைபிரி)
- Letter joining (எழுத்துகளைசேர்)
- Pattern matching for suffixes
- Character classification utilities

Author: Tamil Arasan
Since: May 2, 2017
"""

from typing import List, Optional, Tuple, Dict
from ..constants.tamil_letters import TamilConstants as TC
from ..constants.letter_groups import LetterGroups as LG


class TamilUtil:
    """
    Core utility class for Tamil text processing operations.
    Provides methods for splitting, joining, and analyzing Tamil words.
    """

    # Cache for memoization
    _mei_vallinam_cache: Dict[str, str] = {}
    _mei_mellinam_cache: Dict[str, str] = {}

    @staticmethod
    def is_null(word: Optional[str]) -> bool:
        """Check if word is None"""
        return word is None

    @staticmethod
    def length(text: str) -> int:
        """
        Get the logical length of Tamil text (counting dependent vowels correctly).
        Dependent vowels don't add to the character count.
        """
        count = sum(1 for char in text if ord(char) in TC.D_VOWELS)
        return len(text) - count

    @staticmethod
    def is_pulli(char: str) -> bool:
        """Check if character is virama (pulli - ்)"""
        if len(char) == 1:
            return ord(char) == TC.ஃ_EXT
        return False

    @staticmethod
    def is_vowel(char: str) -> bool:
        """Check if character is an independent vowel (உயிரெழுத்து)"""
        if len(char) == 1:
            return ord(char) in TC.UYIR_EZHUTHU
        return False

    @staticmethod
    def is_consonant(char: str) -> bool:
        """Check if character is a consonant base (உயிர்மெய்)"""
        if len(char) == 1:
            return ord(char) in TC.UYIRMEY_EZHUTHU
        return False

    @staticmethod
    def split_letters(word: str, need_brackets: bool = False, need_delimiter: bool = False) -> str:
        """
        எழுத்துகளைபிரி - Split Tamil word into constituent atomic letters.

        Converts compound characters to their base form:
        - "வந்தான்" -> "வ்அந்த்ஆன்"
        - Consonant + vowel sign -> consonant + pulli + vowel

        Args:
            word: Tamil word to split
            need_brackets: Whether to add brackets around components
            need_delimiter: Whether to add '+' delimiter between components

        Returns:
            Split representation of the word
        """
        if not word or len(word) == 0:
            return word

        # Handle special markers
        if "VERB" in word or "NOUN" in word:
            return word

        # Remove BOM if present
        word = word.replace("\ufeff", "")
        word = word.strip()

        if len(word) == 1:
            return word

        letters = list(word)
        result = []

        # Stack-based processing (similar to Java implementation)
        stack = []
        i = 0
        while i < len(letters):
            ch1 = letters[i]
            ch1_ord = ord(ch1)
            ch2 = letters[i + 1] if i + 1 < len(letters) else None
            ch2_ord = ord(ch2) if ch2 else 0

            # Check for two-part vowel signs
            if ch1_ord in LG.SUPPORT_CHARACTER and ch2_ord in LG.SUPPORT_CHARACTER:
                combined_key = ch1_ord + ch2_ord
                if combined_key in LG.SUPPORT_CHARACTER_MAP:
                    combined = LG.SUPPORT_CHARACTER_MAP.get(combined_key)
                    if combined is None:
                        stack.append('ர')
                        stack.append(ch2)
                    else:
                        stack.append(chr(combined))
                    i += 2
                    continue

            stack.append(ch1)
            i += 1

        # Process stack to build result
        result_chars = []
        extension = False

        while stack:
            letter = stack.pop()
            letter_ord = ord(letter)
            value = LG.MAP_CHARACTER.get(letter_ord)

            if value is None:
                # Not in map - it's a consonant or unknown
                if extension:
                    result_chars.append(letter)
                    if need_brackets:
                        result_chars.append("(")
                    extension = False
                else:
                    if need_delimiter and result_chars:
                        result_chars.append("+")
                    if need_brackets:
                        result_chars.append(")")
                    # Add consonant + pulli + அ
                    result_chars.append(chr(TC.அ))
                    if need_delimiter:
                        result_chars.append("+")
                    result_chars.append(chr(TC.ஃ_EXT))
                    result_chars.append(letter)
                    if need_brackets:
                        result_chars.append("(")
            else:
                # In map - it's a vowel or vowel sign
                if need_delimiter:
                    value = value.replace("+", "")
                    if result_chars:
                        result_chars.append("+")
                if need_brackets:
                    result_chars.append(")")
                result_chars.append(value)
                extension = True

        # Reverse and join
        result_chars.reverse()
        return ''.join(result_chars)

    @staticmethod
    def join_letters(word: str) -> str:
        """
        எழுத்துகளைசேர் - Join split Tamil letters back into compound form.

        Converts atomic representation back to display form:
        - "வ்அந்த்ஆன்" -> "வந்தான்"

        Args:
            word: Split Tamil word

        Returns:
            Joined display form
        """
        if not word:
            return word

        letters = list(word)
        result = []
        check_last_char = False
        i = 0
        prev_last_char = ''

        while i < len(word):
            i += 1
            last_char = letters[len(word) - i] if i <= len(word) else ''
            i += 1
            prev_last_char = letters[len(word) - i] if i <= len(word) else ''

            last_char_ord = ord(last_char) if last_char else 0
            check_last_char = last_char_ord in TC.UYIR_EZHUTHU_MUDIKIRATHA

            if last_char_ord == TC.ஃ_EXT:
                result.append(prev_last_char + last_char)
            elif check_last_char and prev_last_char and ord(prev_last_char) == TC.ஃ_EXT:
                i += 1
                if i <= len(word):
                    base_char = letters[len(word) - i]
                    reverse_char = LG.REVERSE_MAP_CHARACTER.get(last_char_ord)
                    if reverse_char:
                        combined = base_char + (chr(reverse_char) if reverse_char != ord(' ') else '')
                        result.append(combined.strip())
                    else:
                        result.append(base_char + last_char)
                check_last_char = False
            elif last_char == ' ':
                result.append(" ")
                result.append(prev_last_char)
            else:
                result.append(last_char)

        # Reverse and join
        result.reverse()
        return ''.join(result)

    @staticmethod
    def ends_with_mei(word: str) -> bool:
        """
        கடையெழுத்து மெய்யெழுத்தில் முடிகிறதா
        Check if word ends with a pure consonant (மெய்யெழுத்து)
        """
        if len(word) < 2:
            return False
        last_two = word[-2:]
        return last_two in TC.KADAI_MEY_EZHUTHU

    @staticmethod
    def ends_with_makara_mei(word: str) -> bool:
        """
        கடையெழுத்து மகர எழுத்தில் முடிகிறதா
        Check if word ends with ம்
        """
        if len(word) < 2:
            return False
        return word[-2:] == "ம்"

    @staticmethod
    def first_letter_is_vowel(word: str) -> bool:
        """
        முதல் எழுத்து உயிர் எழுத்தா
        Check if first letter is a vowel
        """
        if not word:
            return False
        first_char = ord(word[0])
        return first_char in TC.UYIR_EZHUTHU_MUDIKIRATHA

    @staticmethod
    def last_letter_is_vowel(word: str) -> bool:
        """
        கடை எழுத்து உயிர் எழுத்தா
        Check if last letter is a vowel
        """
        if not word:
            return False
        last_char = ord(word[-1])
        return last_char in TC.UYIR_EZHUTHU_MUDIKIRATHA

    @staticmethod
    def ends_with_a(word: str) -> bool:
        """
        அவில் முடிகிறதா
        Check if word ends with அ-form consonant
        """
        if not word:
            return False
        last_char = ord(word[-1])
        return last_char in TC.UYIRMEY_EZHUTHU

    @staticmethod
    def ends_with_pattern(word: str, pattern: List[int]) -> bool:
        """
        கொடுத்தவில் முடிகிறதா
        Check if word ends with given pattern (as Unicode code points)
        """
        if not word or len(word) < len(pattern):
            return False

        for i, code_point in enumerate(reversed(pattern)):
            if ord(word[-(i + 1)]) != code_point:
                return False
        return True

    @staticmethod
    def ends_with_pattern_str(word: str, pattern: str) -> bool:
        """Check if word ends with given string pattern"""
        return word.endswith(pattern)

    @staticmethod
    def split_if_ends_with(word: str, pattern: str) -> Tuple[str, str, str]:
        """
        கடை எழுத்து_1ல்_முடிந்தால்பிரி
        Split word if it ends with pattern
        """
        if word.endswith(pattern):
            idx = word.rfind(pattern)
            return (word[:idx], word[idx:], "")
        return (word, "", "")

    @staticmethod
    def ends_with_vallinam_mei(word: str) -> bool:
        """
        வல்லினம் மெய்யெழுத்து முடிகிறதா
        Check if word ends with வல்லின மெய் (hard consonant)
        """
        if len(word) < 2:
            return False
        last_two = word[-2:]
        return last_two in TC.VALLINAM_MEY_EZHUTHU_MUDIKIRATHA

    @staticmethod
    def exists_in_check_list(word: str, check_list) -> bool:
        """
        existInCheckList - Check if word exists in given list
        """
        if isinstance(check_list, (list, tuple, set)):
            return word in check_list
        return False

    @staticmethod
    def exist_in_check_list(word: str, check_list) -> bool:
        """Alias for exists_in_check_list"""
        return TamilUtil.exists_in_check_list(word, check_list)

    @staticmethod
    def ends_with_mei_in_list(word: str) -> bool:
        """
        மெய்யெழுத்தில் முடிகிறதா
        Check if word ends with any pure consonant
        """
        return word in TC.MEY_EZHUTHU_MUDIKIRATHA

    @staticmethod
    def add_sandhi(word1: str, word2: str) -> str:
        """
        சந்தியைச் சேர்
        Join two words with appropriate sandhi (புணர்ச்சி)
        """
        word11 = TamilUtil.split_letters(word1)
        word22 = TamilUtil.split_letters(word2)

        if not word11 or not word22:
            return word1 + " " + word2

        last_char = ord(word11[-1])
        first_char = ord(word22[0])

        check_last = last_char in TC.UYIR_EZHUTHU_MUDIKIRATHA
        check_first = first_char in TC.UYIR_EZHUTHU_MUDIKIRATHA

        if check_last and check_first:
            if last_char in TC.YA_NILAI_MOZHIYIN_IRU:
                return TamilUtil.join_letters(word11 + "ய்" + word22)
            elif last_char in TC.VA_NILAI_MOZHIYIN_IRU:
                return TamilUtil.join_letters(word11 + "வ்" + word22)

        return word1 + " " + word2

    @staticmethod
    def check_mei_mayakkam(word: str) -> str:
        """
        மெய் மயங்கிறதா
        Check for consonant cluster patterns
        """
        letters = list(word)

        for i in range(len(letters) - 3):
            letter1 = letters[i]
            letter2 = letters[i + 1] if i + 1 < len(letters) else ''
            letter3 = letters[i + 2] if i + 2 < len(letters) else ''
            letter4 = letters[i + 3] if i + 3 < len(letters) else ''

            if letter2 and ord(letter2) == TC.ஃ_EXT and letter4 and ord(letter4) == TC.ஃ_EXT:
                if letter1 == letter3:
                    return f"உடன்நிலைமெய்மயங்கிறது:{letter1}{letter2}{letter3}{letter4}"
                else:
                    return f"வேற்நிலைமெய்மயங்கிறது:{letter1}{letter2}{letter3}{letter4}"

        return ""

    @staticmethod
    def ends_with_suffix_list(word: str, deeper_inner_list: List[str]) -> bool:
        """
        கடைஎழுத்து_கொடுக்கபட்வையில்_முடிகிறதா
        Check if word ends with concatenation of suffix list
        """
        suffix = ''.join(TamilUtil.split_letters(inner) for inner in deeper_inner_list)
        return word.endswith(suffix)

    @staticmethod
    def split_by_suffix_list(word: str, deeper_inner_list: List[str]) -> List[str]:
        """
        கடைஎழுத்து_கொடுக்கபட்வையில்_முடிந்தால்பிரி
        Split word by suffix list pattern
        """
        result = [word] + [''] * len(deeper_inner_list)

        if not TamilUtil.ends_with_suffix_list(word, deeper_inner_list):
            return result

        # Find and extract each suffix
        index = [0, 0]
        for count in range(len(deeper_inner_list) + 1):
            try:
                if count + 1 == len(deeper_inner_list):
                    if count - 1 == -1:
                        result[count] = word[:word.rfind(deeper_inner_list[count])]
                    else:
                        temp_count = word.rfind(deeper_inner_list[count])
                        temp_word = word[:temp_count]
                        result[count] = word[temp_word.rfind(deeper_inner_list[count - 1]):word.rfind(deeper_inner_list[count])]
                elif count == len(deeper_inner_list):
                    result[count] = word[word.rfind(deeper_inner_list[count - 1]):]
                elif TamilUtil._index_match(word, deeper_inner_list[count], deeper_inner_list[count + 1], index):
                    if count == 0:
                        result[count] = word[:index[0]]
                    else:
                        old_index = [0, 0]
                        TamilUtil._index_match(word, deeper_inner_list[count - 1], deeper_inner_list[count], old_index)
                        result[count] = word[old_index[0]:old_index[1]]
            except Exception:
                pass

        return result

    @staticmethod
    def _index_match(word: str, first: str, second: str, index: List[int]) -> bool:
        """
        indexMatch - Find indices of first and second patterns in word
        """
        first_last = word.rfind(first)
        second_last = word.rfind(second)

        while first_last > 0:
            if first_last < second_last:
                index[0] = first_last
                index[1] = second_last
                return True
            else:
                first_last = word.rfind(first, 0, first_last)

        index[0] = 0
        index[1] = 0
        return False

    @staticmethod
    def end_with_certain_values(org_word: str) -> Optional[str]:
        """
        endWithCertianValues - Transform word ending based on certain patterns

        Used to convert truncated words back to their dictionary form:
        - Words ending with வல்லின மெய் get உ added
        - Words ending with அ may get ம், ர், or ன் added
        """
        word = TamilUtil.split_letters(org_word)
        modified_word = None

        # Get last value using iterator
        from ..utils.tamil_iterator import TamilStringIterator
        ist = TamilStringIterator(org_word)
        last_value = ist.last()

        if TamilUtil.exists_in_check_list(last_value, TC.VALLINAM_MEY_EZHUTHU_V_TO_RR_MUDIKIRATHA):
            # Add உ for words ending with vallinam mei
            modified_word = TamilUtil.join_letters(word + chr(TC.உ))
        elif word.endswith("அ"):
            # Try adding ம், ர், or ன்
            modified_word = TamilUtil.join_letters(word + TC.ம்)
        elif word.endswith(TC.ஞ்):
            modified_word = TamilUtil.join_letters(word.replace(TC.ஞ், TC.ம்))
        elif word.endswith(TC.ங்):
            modified_word = TamilUtil.join_letters(word.replace(TC.ங், TC.ம்))

        return modified_word

    @staticmethod
    def get_paal(word: str) -> str:
        """
        பால் காட்டு - Get gender/number from word ending

        Returns:
            Gender/number classification string
        """
        if TamilUtil.ends_with_pattern(word, [TC.ஆ_EXT, TC.ன, TC.ஃ_EXT]):
            return "ஆண்பால்"
        elif TamilUtil.ends_with_pattern(word, [TC.ஆ_EXT, TC.ள, TC.ஃ_EXT]):
            return "பெண்பால்"
        elif TamilUtil.ends_with_pattern(word, [TC.ஆ_EXT, TC.ர, TC.ஃ_EXT]):
            return "பலர்பால்"
        elif TamilUtil.ends_with_pattern(word, [TC.ய]) or TamilUtil.ends_with_a(word):
            return "பலவின்பால்"
        return ""

    # ==================== Compound Pattern Matching Methods ====================

    @staticmethod
    def ends_with_thth_athu(word: str) -> bool:
        """கடைஎழுத்து_த்த்_மற்றும்_அதுவில்_முடிகிறதா"""
        return word.endswith(TC.த்த்தில்முடிகிறதா + TC.அதுவில்முடிகிறதா)

    @staticmethod
    def split_if_ends_with_thth_athu(word: str) -> Tuple[str, str, str]:
        """கடைஎழுத்து_த்த்_மற்றும்_அதுவில்_முடிந்தால்பிரி"""
        if TamilUtil.ends_with_thth_athu(word):
            idx1 = word.rfind(TC.த்த்தில்முடிகிறதா)
            idx2 = word.rfind(TC.அதுவில்முடிகிறதா)
            return (word[:idx1], word[idx1:idx2], word[idx2:])
        return (word, "", "")

    @staticmethod
    def ends_with_ndth_aal(word: str) -> bool:
        """கடைஎழுத்து_ந்த்_மற்றும்_ஆல்லில்_முடிகிறதா"""
        return word.endswith(TC.ந்த்தில்முடிகிறதா + TC.ஆல்லில்முடிகிறதா)

    @staticmethod
    def ends_with_first_and_second(word: str, first: str, second: str) -> bool:
        """கடைஎழுத்து_1_மற்றும்_2ல்_முடிகிறதா"""
        return word.endswith(first + second)

    @staticmethod
    def split_if_ends_with_first_and_second(word: str, first: str, second: str) -> Tuple[str, str, str]:
        """கடைஎழுத்து_1_மற்றும்_2ல்_முடிந்தால்பிரி"""
        if TamilUtil.ends_with_first_and_second(word, first, second):
            idx1 = word.rfind(first)
            idx2 = word.rfind(second)
            if idx1 < idx2:
                return (word[:idx1], word[idx1:idx2], word[idx2:])
        return (word, "", "")

    @staticmethod
    def ends_with_three_patterns(word: str, first: str, second: str, third: str) -> bool:
        """கடைஎழுத்து_1_மற்றும்_2_மற்றும்_3ல்_முடிகிறதா"""
        return word.endswith(first + second + third)

    @staticmethod
    def ends_with_four_patterns(word: str, first: str, second: str, third: str, fourth: str) -> bool:
        """கடைஎழுத்து_1_மற்றும்_2_மற்றும்_3_மற்றும்_4ல்_முடிகிறதா"""
        return word.endswith(first + second + third + fourth)

    @staticmethod
    def ends_with_otru(word: str) -> bool:
        """ஒற்றில் முடிகிறதா"""
        if len(word) < 2:
            return False
        last_two = word[-2:]
        return last_two in TC.OTRU_MEY_EZHUTHU_MUDIKIRATHA

    @staticmethod
    def split_if_ends_with_otru(word: str) -> Tuple[str, str, str]:
        """ஒற்றில் முடிந்தால்பிரி"""
        if TamilUtil.ends_with_otru(word):
            return (word[:-2], word[-2:], "")
        return (word, "", "")

    # ==================== Specific Pattern Methods ====================

    @staticmethod
    def ends_with_aal(word: str) -> bool:
        """கடைஎழுத்து_ஆல்லில்_முடிகிறதா"""
        return word.endswith(TC.ஆல்லில்முடிகிறதா)

    @staticmethod
    def ends_with_in(word: str) -> bool:
        """கடைஎழுத்து_இன்லில்_முடிகிறதா"""
        return word.endswith(TC.இன்லில்முடிகிறதா)

    @staticmethod
    def ends_with_um(word: str) -> bool:
        """கடைஎழுத்து_உம்லில்_முடிகிறதா"""
        return word.endswith(TC.உம்மில்முடிகிறதா)

    @staticmethod
    def ends_with_kal(word: str) -> bool:
        """கடைஎழுத்து_கள்லில்_முடிகிறதா"""
        return word.endswith(TC.க்அள்லில்முடிகிறதா)

    @staticmethod
    def ends_with_than(word: str) -> bool:
        """கடைஎழுத்து_த்ஆன்லில்_முடிகிறதா"""
        return word.endswith(TC.த்ஆன்முடிகிறதா)

    @staticmethod
    def ends_with_irundu(word: str) -> bool:
        """கடைஎழுத்து_இர்உந்த்உலில்_முடிகிறதா"""
        return word.endswith(TC.இர்உந்த்உமுடிகிறதா)

    @staticmethod
    def ends_with_enru(word: str) -> bool:
        """கடைஎழுத்து_என்ற்உல்_முடிகிறதா"""
        return word.endswith(TC.என்ற்உல்முடிகிறதா)

    @staticmethod
    def ends_with_past_tense_and_a(word: str) -> bool:
        """
        கடைஎழுத்து_அ_மற்றும்_இறந்தகாலஉறுபுபில்_முடிகிறதா
        Check if word ends with past tense marker + அ
        """
        if len(word) < 6:
            return False

        letters = list(word.strip())
        if letters[-1] == chr(TC.அ):
            # Check for ந்த் or த்த் before the final அ
            last_part = ''.join(letters[-5:-1])
            return (TC.த் in last_part and TC.ந் in last_part) or \
                   (last_part.count(TC.த்) >= 2)

        return False

    # ==================== Tamil-named Aliases ====================
    # These provide backward compatibility with the original Java naming

    @staticmethod
    def எழுத்துகளைபிரி(word: str, need_brackets: bool = False, need_delimiter: bool = False) -> str:
        """Alias for split_letters (Tamil name)"""
        return TamilUtil.split_letters(word, need_brackets, need_delimiter)

    @staticmethod
    def எழுத்துகளைசேர்(split_word: str) -> str:
        """Alias for join_letters (Tamil name)"""
        return TamilUtil.join_letters(split_word)

    @staticmethod
    def is_uyir(char: str) -> bool:
        """Alias for is_vowel"""
        return TamilUtil.is_vowel(char)

    @staticmethod
    def is_mei(char: str) -> bool:
        """Check if character is a pure consonant (மெய்)"""
        if len(char) == 1:
            return ord(char) in [TC.க் - TC.க + c for c in TC.UYIRMEY_EZHUTHU]
        # Check if it's consonant + virama
        if len(char) == 2:
            return ord(char[0]) in TC.UYIRMEY_EZHUTHU and ord(char[1]) == TC.ஃ_EXT
        return False

    @staticmethod
    def is_uyirmei(char: str) -> bool:
        """Check if character is combined consonant-vowel (உயிர்மெய்)"""
        if len(char) == 1:
            code = ord(char)
            # Check if it's a base consonant (implicitly has அ)
            return code in TC.UYIRMEY_EZHUTHU
        if len(char) == 2:
            # Consonant + dependent vowel
            return ord(char[0]) in TC.UYIRMEY_EZHUTHU and ord(char[1]) in TC.D_VOWELS
        return False
