"""
Word Class - Equivalent to WordClass.java

This module provides the WordClass data structure for holding parsed word results.

Author: Rajamani David (Original Java)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from functools import total_ordering


@total_ordering
@dataclass
class WordClass:
    """
    Data class for holding parsed word information.

    Contains the word, its parse result, type classification,
    and split component lists.
    """

    number: int = 0
    word: str = ""
    value: str = ""
    splitted_val: str = ""
    map_parse_vals: Dict[str, str] = field(default_factory=dict)
    raw_split_list: List[List[str]] = field(default_factory=list)
    type_: str = "NA"
    sub_type: str = ""
    alt_value: str = ""

    def __post_init__(self):
        """Initialize type and alt_value from map_parse_vals"""
        if self.map_parse_vals:
            self.type_ = self.map_parse_vals.get("Type", "NA")
            self.sub_type = self.map_parse_vals.get("SubType", "")

        # Extract alt_value from IgnoreList if present
        if "IgnoreList" in self.value:
            val_arr = self.value.split(":")
            if len(val_arr) >= 2:
                self.alt_value = val_arr[-2].replace("]", "")

    @classmethod
    def create(cls, number: int, word: str, value: str = "", splitted_val: str = "",
               map_parse_vals: Optional[Dict[str, str]] = None,
               raw_split_list: Optional[List[List[str]]] = None) -> 'WordClass':
        """
        Factory method to create WordClass instance.

        Args:
            number: Index number
            word: The original word
            value: Parse result value
            splitted_val: Comma-separated split values
            map_parse_vals: Dictionary of parse values
            raw_split_list: List of split component lists

        Returns:
            WordClass instance
        """
        return cls(
            number=number,
            word=word,
            value=value,
            splitted_val=splitted_val,
            map_parse_vals=map_parse_vals or {},
            raw_split_list=raw_split_list or []
        )

    def get_word(self) -> str:
        """Get the original word"""
        return self.word

    def get_map_vals(self) -> Dict[str, str]:
        """Get the parse values map"""
        return self.map_parse_vals

    def get_value(self) -> str:
        """Get the parse result value"""
        return self.value

    def get_alt_value(self) -> str:
        """Get the alternative value (from IgnoreList)"""
        return self.alt_value

    def get_splitted_val(self) -> str:
        """Get the comma-separated split values"""
        return self.splitted_val

    def get_splitted_val_to_list(self) -> List[str]:
        """Get split values as list"""
        if self.splitted_val:
            return self.splitted_val.split(",")
        return []

    def get_type(self) -> str:
        """Get the word type (V, N, PL, PR, etc.)"""
        return self.type_

    def get_sub_type(self) -> str:
        """Get the sub-type"""
        return self.sub_type

    def get_raw_split_list(self) -> List[List[str]]:
        """Get the raw split list"""
        return self.raw_split_list

    def get_index(self) -> int:
        """Get the index number"""
        return self.number

    def __eq__(self, other: Any) -> bool:
        """Equality comparison by number"""
        if isinstance(other, WordClass):
            return self.number == other.number
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        """Less than comparison by number"""
        if isinstance(other, WordClass):
            return self.number < other.number
        return NotImplemented

    def __repr__(self) -> str:
        """String representation"""
        return (f"WordClass[number={self.number}, value={self.value}, "
                f"subType={self.sub_type}, altValue={self.alt_value}, "
                f"word={self.word}, type={self.type_}, "
                f"splittedVal={self.splitted_val}, "
                f"mapParseVals={self.map_parse_vals}, "
                f"rawSplitList={self.raw_split_list}]")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'number': self.number,
            'word': self.word,
            'value': self.value,
            'splitted_val': self.splitted_val,
            'type': self.type_,
            'sub_type': self.sub_type,
            'alt_value': self.alt_value,
            'map_parse_vals': self.map_parse_vals,
            'raw_split_list': self.raw_split_list
        }


# Type code mappings
TYPE_CODES = {
    'V': 'வினை',      # Verb
    'N': 'பெயர்',      # Noun
    'PL': 'இடம்',     # Place
    'PR': 'நபர்',      # Person
    'PRE': 'முன்னொட்டு',  # Prefix
    'NU': 'எண்',      # Number
    'OG': 'மற்றவை',   # Other
    'NA': 'NA',       # Not Available
    'Symbol': 'குறி'  # Symbol
}


def get_type_description(type_code: str) -> str:
    """
    Get Tamil description for type code.

    Args:
        type_code: Type code (V, N, PL, etc.)

    Returns:
        Tamil description
    """
    return TYPE_CODES.get(type_code, type_code)
