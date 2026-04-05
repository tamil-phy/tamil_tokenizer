"""
Recursive Constants - Equivalent to RecursiveConstants.java

This module provides a data class for storing recursive algorithm state.

Author: Tamil Arasan
Since: Jan 20, 2018
"""

from typing import Optional


class RecursiveConstants:
    """
    Data class for storing recursive algorithm state.

    Holds information about index, key, possible combinations,
    and record active indicator for recursive processing.
    """

    def __init__(self, index: int = 0, key: str = "",
                 possible_combination: str = "",
                 record_active_ind: str = ""):
        """
        Initialize recursive constants.

        Args:
            index: Position index
            key: Key string
            possible_combination: Possible combination string
            record_active_ind: Record active indicator
        """
        self._recursive_id: Optional[int] = None
        self._index = index
        self._key = key
        self._possible_combination = possible_combination
        self._record_active_ind = record_active_ind

    @property
    def recursive_id(self) -> Optional[int]:
        """Get recursive ID."""
        return self._recursive_id

    @recursive_id.setter
    def recursive_id(self, value: int) -> None:
        """Set recursive ID."""
        self._recursive_id = value

    @property
    def index(self) -> int:
        """Get index."""
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        """Set index."""
        self._index = value

    @property
    def key(self) -> str:
        """Get key."""
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        """Set key."""
        self._key = value

    @property
    def possible_combination(self) -> str:
        """Get possible combination."""
        return self._possible_combination

    @possible_combination.setter
    def possible_combination(self, value: str) -> None:
        """Set possible combination."""
        self._possible_combination = value

    @property
    def record_active_ind(self) -> str:
        """Get record active indicator."""
        return self._record_active_ind

    @record_active_ind.setter
    def record_active_ind(self, value: str) -> None:
        """Set record active indicator."""
        self._record_active_ind = value

    def __repr__(self) -> str:
        return (f"RecursiveConstants(index={self._index}, key='{self._key}', "
                f"possible_combination='{self._possible_combination}', "
                f"record_active_ind='{self._record_active_ind}')")
