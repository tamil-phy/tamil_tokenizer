"""
Tamil String Iterator - Equivalent to TamilStringIterator.java

This module provides an iterator for Tamil strings that properly handles
multi-byte characters and vowel signs.

Author: Tamil Arasan
"""

from typing import List, Optional, Iterator
from ..constants.tamil_letters import TamilConstants as TC
from ..constants.letter_groups import LetterGroups as LG


class TamilStringIterator:
    """
    Iterator for Tamil strings that handles Tamil character composition.

    Tamil characters can be composed of:
    - A single vowel (உயிர்)
    - A consonant + virama (மெய்)
    - A consonant + vowel sign (உயிர்மெய்)

    This iterator returns each logical Tamil character as a unit.
    """

    def __init__(self, text: str):
        """
        Initialize iterator with Tamil text.

        Args:
            text: Tamil string to iterate over
        """
        self.text = text or ""
        self._position = 0
        self._letters: List[str] = []
        self._parse_letters()

    def _parse_letters(self) -> None:
        """Parse text into individual Tamil letters"""
        if not self.text:
            return

        i = 0
        while i < len(self.text):
            char = self.text[i]
            char_code = ord(char)

            # Check if this is a consonant
            if char_code in TC.UYIRMEY_EZHUTHU:
                # Look ahead for vowel sign or virama
                if i + 1 < len(self.text):
                    next_char = self.text[i + 1]
                    next_code = ord(next_char)

                    if next_code in TC.D_VOWELS:
                        # Consonant + vowel sign
                        # Check for two-part vowel signs (ொ, ோ, ௌ)
                        if i + 2 < len(self.text):
                            third_char = self.text[i + 2]
                            third_code = ord(third_char)
                            if third_code in [0x0BBE, 0x0BD7]:  # ா or ௗ
                                self._letters.append(char + next_char + third_char)
                                i += 3
                                continue
                        self._letters.append(char + next_char)
                        i += 2
                        continue

                # Just the consonant (treated as consonant + அ implicitly)
                self._letters.append(char)
                i += 1

            elif char_code in TC.UYIR_EZHUTHU:
                # Independent vowel
                self._letters.append(char)
                i += 1

            elif char_code in TC.D_VOWELS:
                # Standalone vowel sign (shouldn't happen in valid Tamil, but handle it)
                self._letters.append(char)
                i += 1

            else:
                # Other characters (numbers, punctuation, etc.)
                self._letters.append(char)
                i += 1

    def __iter__(self) -> Iterator[str]:
        """Return iterator"""
        self._position = 0
        return self

    def __next__(self) -> str:
        """Get next Tamil letter"""
        if self._position >= len(self._letters):
            raise StopIteration
        letter = self._letters[self._position]
        self._position += 1
        return letter

    def __len__(self) -> int:
        """Get number of logical Tamil letters"""
        return len(self._letters)

    def length(self) -> int:
        """Get number of logical Tamil letters (Java-compatible method)"""
        return len(self._letters)

    def __getitem__(self, index: int) -> str:
        """Get letter at index"""
        return self._letters[index]

    def reset(self) -> None:
        """Reset iterator to beginning"""
        self._position = 0

    def has_next(self) -> bool:
        """Check if more letters available"""
        return self._position < len(self._letters)

    def next(self) -> Optional[str]:
        """Get next letter or None"""
        if self.has_next():
            return self.__next__()
        return None

    def previous(self) -> Optional[str]:
        """Get previous letter or None"""
        if self._position > 1:
            self._position -= 2
            return self.__next__()
        return None

    def first(self) -> Optional[str]:
        """Get first letter"""
        if self._letters:
            return self._letters[0]
        return None

    def last(self) -> Optional[str]:
        """Get last letter"""
        if self._letters:
            return self._letters[-1]
        return None

    def get_letters(self) -> List[str]:
        """Get all letters as list"""
        return self._letters.copy()

    def forward_iterator(self) -> List[str]:
        """Get letters in forward order"""
        return self._letters.copy()

    def backward_iterator(self) -> List[str]:
        """Get letters in reverse order"""
        return self._letters[::-1]

    def at(self, index: int) -> Optional[str]:
        """Get letter at specific index"""
        if 0 <= index < len(self._letters):
            return self._letters[index]
        return None

    def slice(self, start: int, end: Optional[int] = None) -> List[str]:
        """Get slice of letters"""
        if end is None:
            return self._letters[start:]
        return self._letters[start:end]

    def join(self) -> str:
        """Join all letters back to string"""
        return ''.join(self._letters)

    def index_of(self, letter: str) -> int:
        """Find index of letter, -1 if not found"""
        try:
            return self._letters.index(letter)
        except ValueError:
            return -1

    def last_index_of(self, letter: str) -> int:
        """Find last index of letter, -1 if not found"""
        for i in range(len(self._letters) - 1, -1, -1):
            if self._letters[i] == letter:
                return i
        return -1

    def contains(self, letter: str) -> bool:
        """Check if letter is in string"""
        return letter in self._letters

    def starts_with(self, prefix: str) -> bool:
        """Check if starts with given letter(s)"""
        if not prefix:
            return True
        prefix_iter = TamilStringIterator(prefix)
        prefix_letters = prefix_iter.get_letters()
        if len(prefix_letters) > len(self._letters):
            return False
        return self._letters[:len(prefix_letters)] == prefix_letters

    def ends_with(self, suffix: str) -> bool:
        """Check if ends with given letter(s)"""
        if not suffix:
            return True
        suffix_iter = TamilStringIterator(suffix)
        suffix_letters = suffix_iter.get_letters()
        if len(suffix_letters) > len(self._letters):
            return False
        return self._letters[-len(suffix_letters):] == suffix_letters

    def substring(self, start: int, end: Optional[int] = None) -> str:
        """Get substring by letter indices"""
        letters = self.slice(start, end)
        return ''.join(letters)

    @staticmethod
    def letter_count(text: str) -> int:
        """Count Tamil letters in text"""
        return len(TamilStringIterator(text))

    @staticmethod
    def is_valid_tamil(text: str) -> bool:
        """Check if text contains only valid Tamil characters"""
        for char in text:
            code = ord(char)
            # Allow Tamil Unicode range, spaces, and common punctuation
            if not (0x0B80 <= code <= 0x0BFF or
                    char in ' \t\n.,;:!?()-"\'0123456789'):
                return False
        return True
