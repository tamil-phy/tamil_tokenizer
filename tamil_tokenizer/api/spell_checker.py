"""
Tamil Spell Checker - Core spell checking engine

This module provides comprehensive spell checking for Tamil text using
morphological analysis, dictionary lookups, and grammar rules.
"""

import logging
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import re

logger = logging.getLogger(__name__)

from ..parsers.root_word_parser import TamilRootWordParser
from ..parsers.verb_parser import VerbParser
from ..parsers.noun_parser import NounParser
from ..parsers.morphology_parser import MorphologyParser
from ..parsers.unicode_language_parser import UnicodeLanguageParser
from ..parsers.twin_word_parser import TwinWordParser
from ..config.constant_table import TamilConstantTable
from ..grammar.tamil_util import TamilUtil
from ..utils.tamil_iterator import TamilStringIterator
from ..utils.word_splitter import WordSplitter
from ..utils.tamil_ngram import TamilNGram


class ErrorType(Enum):
    """Types of spelling/grammar errors."""
    SPELLING = "spelling"
    GRAMMAR = "grammar"
    UNKNOWN_WORD = "unknown"
    MIXED_LANGUAGE = "mixed_language"
    SUGGESTION = "suggestion"


@dataclass
class SpellError:
    """Represents a spelling or grammar error."""
    word: str
    start_pos: int
    end_pos: int
    error_type: ErrorType
    message: str
    suggestions: List[str] = field(default_factory=list)
    severity: str = "error"  # error, warning, info
    rule_id: str = ""
    context: str = ""


@dataclass
class AnalysisResult:
    """Result of word analysis."""
    word: str
    is_valid: bool
    word_type: str  # V, N, NA, etc.
    root_word: Optional[str] = None
    suffixes: List[str] = field(default_factory=list)
    grammar_info: Dict[str, str] = field(default_factory=dict)
    confidence: float = 1.0


@dataclass
class CheckResult:
    """Complete spell check result."""
    original_text: str
    corrected_text: str
    errors: List[SpellError] = field(default_factory=list)
    word_analyses: List[AnalysisResult] = field(default_factory=list)
    statistics: Dict[str, int] = field(default_factory=dict)


class TamilSpellChecker:
    """
    Comprehensive Tamil spell checker using morphological analysis.

    Features:
    - Dictionary-based word validation
    - Morphological analysis for inflected words
    - Grammar rule checking
    - Suggestion generation
    - Mixed language detection
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the spell checker.

        Args:
            data_path: Path to data directory
        """
        self._initialized = False
        self.data_path = data_path

        # Parsers
        self.root_parser: Optional[TamilRootWordParser] = None
        self.verb_parser: Optional[VerbParser] = None
        self.noun_parser: Optional[NounParser] = None
        self.unicode_parser: Optional[UnicodeLanguageParser] = None
        self.twin_parser: Optional[TwinWordParser] = None

        # Constant table for dictionary lookups
        self.constant_table: Optional[TamilConstantTable] = None

        # Word splitter
        self.word_splitter = WordSplitter()

        # N-gram for suggestions
        self.ngram = TamilNGram()

        # Cache for performance
        self._word_cache: Dict[str, AnalysisResult] = {}
        self._max_cache_size = 10000

    def initialize(self) -> None:
        """Initialize all parsers and resources."""
        if self._initialized:
            return

        logger.debug("Initializing Tamil Spell Checker...")

        # Initialize constant table first
        self.constant_table = TamilConstantTable.get_instance(self.data_path)

        # Initialize parsers
        self.root_parser = TamilRootWordParser(self.data_path)
        self.verb_parser = VerbParser(self.data_path)
        self.noun_parser = NounParser(self.data_path)
        self.unicode_parser = UnicodeLanguageParser(self.data_path)
        self.twin_parser = TwinWordParser(self.data_path)

        self._initialized = True
        logger.debug("Tamil Spell Checker initialized.")

    def _ensure_initialized(self) -> None:
        """Ensure the spell checker is initialized."""
        if not self._initialized:
            self.initialize()

    def check_text(self, text: str) -> CheckResult:
        """
        Check text for spelling and grammar errors.

        Args:
            text: Tamil text to check

        Returns:
            CheckResult with errors and analysis
        """
        self._ensure_initialized()

        errors: List[SpellError] = []
        analyses: List[AnalysisResult] = []

        # Split text into words while preserving positions
        word_positions = self._get_word_positions(text)

        stats = {
            "total_words": len(word_positions),
            "valid_words": 0,
            "invalid_words": 0,
            "suggestions_made": 0
        }

        for word, start, end in word_positions:
            # Skip punctuation and numbers
            if self._is_punctuation(word) or word.isdigit():
                continue

            # Analyze the word
            analysis = self.analyze_word(word)
            analyses.append(analysis)

            if analysis.is_valid:
                stats["valid_words"] += 1
            else:
                stats["invalid_words"] += 1

                # Generate error
                error = self._create_error(word, start, end, analysis, text)
                if error:
                    errors.append(error)
                    if error.suggestions:
                        stats["suggestions_made"] += 1

        # Generate corrected text
        corrected_text = self._apply_corrections(text, errors)

        return CheckResult(
            original_text=text,
            corrected_text=corrected_text,
            errors=errors,
            word_analyses=analyses,
            statistics=stats
        )

    def analyze_word(self, word: str) -> AnalysisResult:
        """
        Analyze a single word using the rule-based morphological parser.

        The parser uses 617+ parse order rules from the ported Java system.
        This is the PRIMARY validation method - no hardcoded suffixes.

        Validation order:
        1. Dictionary lookup (for base words in ignore lists)
        2. Morphological parsing (617+ rules for inflected words)
        3. Pure Tamil character validation (fallback for unknown words)

        Args:
            word: Word to analyze

        Returns:
            AnalysisResult with word details
        """
        self._ensure_initialized()

        # Check cache first
        if word in self._word_cache:
            return self._word_cache[word]

        # STRATEGY 1: Check dictionary for base words
        if self._is_known_word(word):
            result = AnalysisResult(
                word=word,
                is_valid=True,
                word_type=self._get_word_type(word),
                root_word=word,
                confidence=1.0
            )
            self._cache_result(word, result)
            return result

        # STRATEGY 2: Use the rule-based morphological parser (PRIMARY METHOD)
        # This uses the 617+ parse order rules ported from Java
        try:
            wc_list = self.root_parser.create_single_instance(word)

            if wc_list:
                wc = wc_list[0]
                word_type = wc.get_type()
                splitted = wc.get_splitted_val_to_list()
                raw_value = wc.get_value()

                # Check if parser successfully decomposed the word
                # A valid parse means: word_type is V/N/PR/PL/OTHER (not NA)
                # OR the parser found the word in IgnoreList
                has_valid_type = word_type and word_type not in ["NA", ""]
                is_in_ignore_list = raw_value and "IgnoreList" in raw_value
                has_valid_split = splitted and len(splitted) > 0 and splitted[0] not in ['[]', '']

                if has_valid_type or is_in_ignore_list:
                    root = splitted[0] if has_valid_split else word
                    suffixes = splitted[1:] if len(splitted) > 1 else []

                    grammar_info = {}
                    map_vals = wc.get_map_vals()
                    if map_vals:
                        grammar_info = {k: v for k, v in map_vals.items()
                                       if k not in ['Type', 'Key']}

                    result = AnalysisResult(
                        word=word,
                        is_valid=True,
                        word_type=word_type if word_type else "VALID",
                        root_word=root.split('/')[0] if '/' in root else root,
                        suffixes=suffixes,
                        grammar_info=grammar_info,
                        confidence=0.9
                    )
                    self._cache_result(word, result)
                    return result
        except Exception as e:
            logger.error(f"Morphological analysis error for '{word}': {e}")

        # Word not found in dictionary and parser couldn't recognize it
        # Mark as INVALID - no fallback hacks
        result = AnalysisResult(
            word=word,
            is_valid=False,
            word_type="NA",
            confidence=0.0
        )
        self._cache_result(word, result)
        return result

    def get_suggestions(self, word: str, max_suggestions: int = 5) -> List[str]:
        """
        Get spelling suggestions for a word.

        Args:
            word: Misspelled word
            max_suggestions: Maximum number of suggestions

        Returns:
            List of suggested corrections
        """
        self._ensure_initialized()

        suggestions: Set[str] = set()

        # Strategy 1: Check for common Tamil typos
        typo_suggestions = self._get_typo_corrections(word)
        suggestions.update(typo_suggestions[:max_suggestions])

        # Strategy 2: N-gram based suggestions from known words
        ngram_suggestions = self._get_ngram_suggestions(word)
        suggestions.update(ngram_suggestions[:max_suggestions])

        # Strategy 3: Edit distance suggestions
        edit_suggestions = self._get_edit_distance_suggestions(word)
        suggestions.update(edit_suggestions[:max_suggestions])

        # Filter and validate suggestions
        valid_suggestions = []
        for sug in suggestions:
            if sug != word and self._is_known_word(sug):
                valid_suggestions.append(sug)

        # Sort by similarity
        valid_suggestions.sort(key=lambda s: self._similarity_score(word, s), reverse=True)

        return valid_suggestions[:max_suggestions]

    def _is_known_word(self, word: str) -> bool:
        """Check if word is in any dictionary."""
        if not self.constant_table:
            return False

        return (self.constant_table.is_in_ignore_verb_word_list(word) or
                self.constant_table.is_in_ignore_noun_word_list(word) or
                self.constant_table.is_in_ignore_person_list(word) or
                self.constant_table.is_in_ignore_place_list(word) or
                self.constant_table.is_in_ignore_word_list(word))

    def _get_word_type(self, word: str) -> str:
        """Get word type from dictionaries."""
        if not self.constant_table:
            return "NA"

        if self.constant_table.is_in_ignore_verb_word_list(word):
            return "V"
        elif self.constant_table.is_in_ignore_noun_word_list(word):
            return "N"
        elif self.constant_table.is_in_ignore_person_list(word):
            return "PR"
        elif self.constant_table.is_in_ignore_place_list(word):
            return "PL"
        return "NA"



    def _get_word_positions(self, text: str) -> List[Tuple[str, int, int]]:
        """Get words with their positions in text."""
        positions = []
        pattern = re.compile(r'[\u0B80-\u0BFF]+|[a-zA-Z]+|\d+|[^\s\u0B80-\u0BFFa-zA-Z\d]+')

        for match in pattern.finditer(text):
            positions.append((match.group(), match.start(), match.end()))

        return positions

    def _is_punctuation(self, text: str) -> bool:
        """Check if text is punctuation."""
        return bool(re.match(r'^[.,;:!?"\'()\-–—\s]+$', text))

    def _create_error(self, word: str, start: int, end: int,
                      analysis: AnalysisResult, context: str) -> Optional[SpellError]:
        """Create a SpellError from analysis."""
        if analysis.is_valid:
            return None

        # Determine error type
        if analysis.word_type == "MIXED":
            error_type = ErrorType.MIXED_LANGUAGE
            message = f"'{word}' contains mixed languages"
            severity = "warning"
        else:
            error_type = ErrorType.UNKNOWN_WORD
            message = f"'{word}' is not recognized"
            severity = "error"

        # Get suggestions
        suggestions = self.get_suggestions(word)

        # Get context
        ctx_start = max(0, start - 20)
        ctx_end = min(len(context), end + 20)
        error_context = context[ctx_start:ctx_end]

        return SpellError(
            word=word,
            start_pos=start,
            end_pos=end,
            error_type=error_type,
            message=message,
            suggestions=suggestions,
            severity=severity,
            rule_id=f"TAMIL_{error_type.value.upper()}",
            context=error_context
        )

    def _apply_corrections(self, text: str, errors: List[SpellError]) -> str:
        """Apply first suggestion for each error."""
        if not errors:
            return text

        # Sort errors by position (reverse to maintain positions)
        sorted_errors = sorted(errors, key=lambda e: e.start_pos, reverse=True)

        corrected = text
        for error in sorted_errors:
            if error.suggestions:
                corrected = (corrected[:error.start_pos] +
                            error.suggestions[0] +
                            corrected[error.end_pos:])

        return corrected

    def _get_typo_corrections(self, word: str) -> List[str]:
        """Get corrections for common typos."""
        corrections = []

        # Common Tamil character substitutions
        substitutions = {
            'ன': 'ண',
            'ண': 'ன',
            'ல': 'ள',
            'ள': 'ல',
            'ர': 'ற',
            'ற': 'ர',
            'ந': 'ன',
        }

        for i, char in enumerate(word):
            if char in substitutions:
                new_word = word[:i] + substitutions[char] + word[i+1:]
                if self._is_known_word(new_word):
                    corrections.append(new_word)

        return corrections

    def _get_ngram_suggestions(self, word: str) -> List[str]:
        """Get suggestions using N-gram similarity."""
        suggestions = []

        # Get all known words that share N-grams
        word_ngrams = set(self.ngram.n_gram_letter(word, 2))

        # Check against verb list
        if self.constant_table:
            for known in self.constant_table.get_ignore_verb_list()[:1000]:
                known_ngrams = set(self.ngram.n_gram_letter(known, 2))
                overlap = len(word_ngrams & known_ngrams)
                if overlap >= len(word_ngrams) * 0.5:
                    suggestions.append(known)

        return suggestions[:10]

    def _get_edit_distance_suggestions(self, word: str) -> List[str]:
        """Get suggestions based on edit distance."""
        suggestions = []
        tsi = TamilStringIterator(word)
        chars = tsi.forward_iterator()

        # Single character deletions
        for i in range(len(chars)):
            new_word = ''.join(chars[:i] + chars[i+1:])
            if self._is_known_word(new_word):
                suggestions.append(new_word)

        # Character swaps
        for i in range(len(chars) - 1):
            new_chars = chars.copy()
            new_chars[i], new_chars[i+1] = new_chars[i+1], new_chars[i]
            new_word = ''.join(new_chars)
            if self._is_known_word(new_word):
                suggestions.append(new_word)

        return suggestions

    def _similarity_score(self, word1: str, word2: str) -> float:
        """Calculate similarity score between two words."""
        if word1 == word2:
            return 1.0

        # Use Jaccard similarity on character bigrams
        set1 = set(self.ngram.n_gram_letter(word1, 2))
        set2 = set(self.ngram.n_gram_letter(word2, 2))

        if not set1 or not set2:
            return 0.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def _cache_result(self, word: str, result: AnalysisResult) -> None:
        """Cache analysis result."""
        if len(self._word_cache) >= self._max_cache_size:
            # Remove oldest entries
            keys = list(self._word_cache.keys())[:1000]
            for key in keys:
                del self._word_cache[key]

        self._word_cache[word] = result

    def clear_cache(self) -> None:
        """Clear the word cache."""
        self._word_cache.clear()
