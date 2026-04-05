"""
Tamil Grammar Analyzer - Detailed grammatical analysis

This module provides detailed grammatical analysis for Tamil text,
including case analysis, tense detection, and sentence structure.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

from ..parsers.root_word_parser import TamilRootWordParser
from ..parsers.verb_parser import VerbParser
from ..parsers.noun_parser import NounParser
from ..grammar.vetrumai import TamilVetrumai
from ..grammar.tamil_util import TamilUtil
from ..config.constant_table import TamilConstantTable
from ..utils.tamil_iterator import TamilStringIterator


class GrammarCategory(Enum):
    """Grammar categories."""
    TENSE = "tense"
    PERSON = "person"
    NUMBER = "number"
    GENDER = "gender"
    CASE = "case"
    MOOD = "mood"


@dataclass
class GrammarInfo:
    """Grammatical information for a word."""
    category: GrammarCategory
    value: str
    tamil_name: str
    confidence: float = 1.0


@dataclass
class WordAnalysis:
    """Complete grammatical analysis of a word."""
    word: str
    word_type: str  # verb, noun, adjective, etc.
    word_type_tamil: str
    root: str
    suffixes: List[str] = field(default_factory=list)
    grammar: List[GrammarInfo] = field(default_factory=list)
    meaning_hints: List[str] = field(default_factory=list)


@dataclass
class SentenceAnalysis:
    """Analysis of a complete sentence."""
    sentence: str
    words: List[WordAnalysis] = field(default_factory=list)
    sentence_type: str = "statement"  # statement, question, command
    structure_notes: List[str] = field(default_factory=list)


class TamilGrammarAnalyzer:
    """
    Detailed Tamil grammar analyzer.

    Uses the rule-based morphological parser (617+ rules) to analyze
    Tamil words. Grammar information is extracted from the parser's
    output, NOT from hardcoded patterns.

    Provides:
    - Tense analysis (past, present, future)
    - Person analysis (first, second, third)
    - Number analysis (singular, plural)
    - Gender analysis (masculine, feminine, neuter)
    - Case analysis (8 Tamil cases / வேற்றுமை)
    """

    # Case information for display (from Tamil grammar)
    CASE_INFO = {
        1: {'name': 'Nominative', 'tamil': 'எழுவாய் வேற்றுமை', 'suffix': ''},
        2: {'name': 'Accusative', 'tamil': 'இரண்டாம் வேற்றுமை', 'suffix': 'ஐ'},
        3: {'name': 'Instrumental', 'tamil': 'மூன்றாம் வேற்றுமை', 'suffix': 'ஆல், ஒடு, ஓடு'},
        4: {'name': 'Dative', 'tamil': 'நான்காம் வேற்றுமை', 'suffix': 'கு, க்கு'},
        5: {'name': 'Ablative', 'tamil': 'ஐந்தாம் வேற்றுமை', 'suffix': 'இல், இலிருந்து'},
        6: {'name': 'Genitive', 'tamil': 'ஆறாம் வேற்றுமை', 'suffix': 'அது, உடைய, இன்'},
        7: {'name': 'Locative', 'tamil': 'ஏழாம் வேற்றுமை', 'suffix': 'இல், இடம்'},
        8: {'name': 'Vocative', 'tamil': 'விளி வேற்றுமை', 'suffix': 'ஏ, ஆ'},
    }

    def __init__(self, data_path: Optional[str] = None):
        """Initialize the grammar analyzer."""
        self._initialized = False
        self.data_path = data_path

        self.root_parser: Optional[TamilRootWordParser] = None
        self.verb_parser: Optional[VerbParser] = None
        self.noun_parser: Optional[NounParser] = None
        self.constant_table: Optional[TamilConstantTable] = None

    def initialize(self) -> None:
        """Initialize parsers and resources."""
        if self._initialized:
            return

        logger.debug("Initializing Tamil Grammar Analyzer...")

        self.constant_table = TamilConstantTable.get_instance(self.data_path)
        self.root_parser = TamilRootWordParser(self.data_path)
        self.verb_parser = VerbParser(self.data_path)
        self.noun_parser = NounParser(self.data_path)

        self._initialized = True
        logger.debug("Tamil Grammar Analyzer initialized.")

    def _ensure_initialized(self) -> None:
        """Ensure analyzer is initialized."""
        if not self._initialized:
            self.initialize()

    def analyze_word(self, word: str) -> WordAnalysis:
        """
        Perform detailed grammatical analysis of a word.

        Uses the rule-based morphological parser to extract grammar info.
        All grammar information comes from the parser's map_vals, NOT
        from hardcoded patterns.

        Args:
            word: Tamil word to analyze

        Returns:
            WordAnalysis with detailed grammar information
        """
        self._ensure_initialized()

        # Default values
        word_type = "unknown"
        word_type_tamil = "அறியப்படாதது"
        root = word
        suffixes = []
        grammar_info = []
        meaning_hints = []

        # Type code to name mapping
        type_map = {
            'V': ('verb', 'வினைச்சொல்'),
            'N': ('noun', 'பெயர்ச்சொல்'),
            'PR': ('pronoun', 'பிரதிப்பெயர்'),
            'PL': ('place', 'இடப்பெயர்'),
            'PRE': ('prefix', 'முன்னொட்டு'),
            'NU': ('number', 'எண்'),
            'OTHER': ('other', 'பிற'),
            'NA': ('unknown', 'அறியப்படாதது'),
        }

        # Use the rule-based parser
        try:
            wc_list = self.root_parser.create_single_instance(word)

            if wc_list:
                wc = wc_list[0]
                word_type_code = wc.get_type()

                if word_type_code in type_map:
                    word_type, word_type_tamil = type_map[word_type_code]

                # Get root and suffixes from parser
                splitted_list = wc.get_splitted_val_to_list()
                if splitted_list and splitted_list[0] not in ['[]', '']:
                    root = splitted_list[0]
                    # Handle root/meaning notation
                    if '/' in root:
                        parts = root.split('/')
                        root = parts[0]
                        if len(parts) > 1:
                            meaning_hints.append(parts[1])
                    suffixes = splitted_list[1:] if len(splitted_list) > 1 else []

                # Extract grammar info from parser's map_vals
                # This is where the 617+ rules provide the grammar info
                map_vals = wc.get_map_vals()
                if map_vals:
                    grammar_info = self._extract_grammar_from_map(map_vals)

                # Get additional info from raw value
                raw_value = wc.get_value()
                if raw_value:
                    hints = self._extract_hints_from_value(raw_value)
                    meaning_hints.extend(hints)

        except Exception as e:
            logger.error(f"Grammar analysis error for '{word}': {e}")

        return WordAnalysis(
            word=word,
            word_type=word_type,
            word_type_tamil=word_type_tamil,
            root=root,
            suffixes=suffixes,
            grammar=grammar_info,
            meaning_hints=meaning_hints
        )

    def _extract_grammar_from_map(self, map_vals: Dict) -> List[GrammarInfo]:
        """
        Extract grammar information from parser's map_vals.

        The parser rules populate map_vals with grammar info like:
        - Tense, Person, Number, Gender for verbs
        - Case markers for nouns
        """
        grammar = []

        for key, value in map_vals.items():
            if key in ['Type', 'Key', '']:
                continue

            # Try to categorize the grammar info
            category = self._categorize_grammar_key(key)
            if category:
                tamil_name = self._get_tamil_name(key, value)
                grammar.append(GrammarInfo(
                    category=category,
                    value=value,
                    tamil_name=tamil_name
                ))

        return grammar

    def _categorize_grammar_key(self, key: str) -> Optional[GrammarCategory]:
        """Categorize a grammar key from the parser."""
        key_lower = key.lower()

        tense_keys = ['tense', 'காலம்', 'past', 'present', 'future']
        person_keys = ['person', 'இடம்', 'first', 'second', 'third']
        number_keys = ['number', 'எண்', 'singular', 'plural']
        gender_keys = ['gender', 'பால்', 'masculine', 'feminine', 'neuter']
        case_keys = ['case', 'வேற்றுமை']

        if any(k in key_lower for k in tense_keys):
            return GrammarCategory.TENSE
        elif any(k in key_lower for k in person_keys):
            return GrammarCategory.PERSON
        elif any(k in key_lower for k in number_keys):
            return GrammarCategory.NUMBER
        elif any(k in key_lower for k in gender_keys):
            return GrammarCategory.GENDER
        elif any(k in key_lower for k in case_keys):
            return GrammarCategory.CASE

        # Default: return as MOOD for other grammar categories
        return GrammarCategory.MOOD

    def _get_tamil_name(self, key: str, value: str) -> str:
        """Get Tamil name for grammar info."""
        # Common Tamil grammar terms
        tamil_names = {
            'past': 'இறந்தகாலம்',
            'present': 'நிகழ்காலம்',
            'future': 'எதிர்காலம்',
            'first': 'தன்மை',
            'second': 'முன்னிலை',
            'third': 'படர்க்கை',
            'singular': 'ஒருமை',
            'plural': 'பன்மை',
            'masculine': 'ஆண்பால்',
            'feminine': 'பெண்பால்',
            'neuter': 'அஃறிணை',
        }
        return tamil_names.get(value.lower(), value)

    def _extract_hints_from_value(self, raw_value: str) -> List[str]:
        """Extract meaning hints from parser's raw value."""
        hints = []
        # Parse the value string for meaningful info
        if 'IgnoreList' in raw_value:
            pass  # Base word, no additional hints
        return hints

    def analyze_sentence(self, sentence: str) -> SentenceAnalysis:
        """
        Analyze a complete sentence.

        Args:
            sentence: Tamil sentence

        Returns:
            SentenceAnalysis with word-by-word analysis
        """
        self._ensure_initialized()

        # Split into words
        words = sentence.split()
        word_analyses = []

        for word in words:
            # Skip punctuation
            if word in '.,;:!?':
                continue
            analysis = self.analyze_word(word)
            word_analyses.append(analysis)

        # Determine sentence type
        sentence_type = self._detect_sentence_type(sentence, word_analyses)

        # Structure notes
        structure_notes = self._get_structure_notes(word_analyses)

        return SentenceAnalysis(
            sentence=sentence,
            words=word_analyses,
            sentence_type=sentence_type,
            structure_notes=structure_notes
        )

    def _detect_sentence_type(self, sentence: str,
                              analyses: List[WordAnalysis]) -> str:
        """Detect sentence type."""
        # Check for question markers
        if sentence.endswith('?') or 'ஆ' in sentence[-5:]:
            return 'question'

        # Check for command mood
        if analyses:
            last_word = analyses[-1]
            # Command forms often end in specific patterns
            if last_word.word.endswith(('உங்கள்', 'ஆய்', 'மின்')):
                return 'command'

        return 'statement'

    def _get_structure_notes(self, analyses: List[WordAnalysis]) -> List[str]:
        """Generate notes about sentence structure."""
        notes = []

        # Check word order (SOV is typical in Tamil)
        word_types = [a.word_type for a in analyses]

        if word_types:
            if 'verb' in word_types and word_types[-1] == 'verb':
                notes.append("Follows typical Tamil SOV (Subject-Object-Verb) order")

            # Count nouns and verbs
            noun_count = word_types.count('noun')
            verb_count = word_types.count('verb')

            if noun_count > 0:
                notes.append(f"Contains {noun_count} noun(s)")
            if verb_count > 0:
                notes.append(f"Contains {verb_count} verb(s)")

        return notes

    def get_case_info(self, case_number: int) -> Dict:
        """Get information about a specific case."""
        return self.CASE_INFO.get(case_number, {})

    def get_all_cases(self) -> Dict[int, Dict]:
        """Get all case information."""
        return self.CASE_INFO.copy()
