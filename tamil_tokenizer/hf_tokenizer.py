"""
HuggingFace-compatible wrapper for TamilTokenizer.

Allows using the Tamil linguistic tokenizer (word/morpheme/character level)
as a drop-in replacement for BPE tokenizers in HuggingFace Transformers
fine-tuning pipelines.

Usage:
    from tamil_tokenizer import TamilHFTokenizer

    # Build vocabulary from your Tamil corpus
    tokenizer = TamilHFTokenizer(level="morpheme")
    tokenizer.build_vocab(["அவன் வந்தான்.", "அவள் பள்ளிக்கு சென்றாள்."])
    tokenizer.save_pretrained("./tamil_morpheme_tokenizer")

    # Load and use for fine-tuning
    tokenizer = TamilHFTokenizer.from_pretrained("./tamil_morpheme_tokenizer")
    encoded = tokenizer("அவன் வந்தான்.", return_tensors="pt")
"""

import json
import logging
import os
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

from transformers import PreTrainedTokenizer

from .tokenizer import TamilTokenizer, TokenType


# Default special tokens
SPECIAL_TOKENS = {
    "pad_token": "[PAD]",
    "unk_token": "[UNK]",
    "bos_token": "[BOS]",
    "eos_token": "[EOS]",
    "sep_token": "[SEP]",
    "cls_token": "[CLS]",
    "mask_token": "[MASK]",
}

VOCAB_FILENAME = "tamil_vocab.json"
CONFIG_FILENAME = "tamil_tokenizer_config.json"


class TamilHFTokenizer(PreTrainedTokenizer):
    """
    HuggingFace PreTrainedTokenizer wrapper around TamilTokenizer.

    Replaces BPE with linguistically-motivated Tamil tokenization at
    word, morpheme, or character level.

    Args:
        level: Tokenization level - "word", "morpheme", or "character".
               "morpheme" is recommended as a BPE replacement for fine-tuning.
        vocab_file: Path to a pre-built vocabulary JSON file.
        data_path: Optional path to Tamil tokenizer data directory.
        min_frequency: Minimum token frequency to include in vocabulary
                       when building from corpus.
        **kwargs: Additional arguments passed to PreTrainedTokenizer.
    """

    vocab_files_names = {"vocab_file": VOCAB_FILENAME}
    model_input_names = ["input_ids", "attention_mask"]

    def __init__(
        self,
        level: str = "morpheme",
        vocab_file: Optional[str] = None,
        data_path: Optional[str] = None,
        min_frequency: int = 1,
        **kwargs,
    ):
        self._level = level
        self._min_frequency = min_frequency
        self._tamil_tokenizer = TamilTokenizer(data_path=data_path)

        # Initialize vocabulary
        self._token_to_id: OrderedDict = OrderedDict()
        self._id_to_token: OrderedDict = OrderedDict()

        # Load vocabulary from file if provided
        if vocab_file and os.path.isfile(vocab_file):
            self._load_vocab(vocab_file)

        # Ensure special tokens are set in kwargs
        for key, default_val in SPECIAL_TOKENS.items():
            if key not in kwargs:
                kwargs[key] = default_val

        super().__init__(**kwargs)

        # Make sure special tokens are in vocabulary
        self._ensure_special_tokens_in_vocab()

    def _ensure_special_tokens_in_vocab(self):
        """Add special tokens to vocabulary if not already present."""
        special_toks = [
            self.pad_token, self.unk_token, self.bos_token,
            self.eos_token, self.sep_token, self.cls_token, self.mask_token,
        ]
        for tok in special_toks:
            if tok and tok not in self._token_to_id:
                idx = len(self._token_to_id)
                self._token_to_id[tok] = idx
                self._id_to_token[idx] = tok

    def _load_vocab(self, vocab_file: str):
        """Load vocabulary from a JSON file."""
        with open(vocab_file, "r", encoding="utf-8") as f:
            vocab = json.load(f)
        self._token_to_id = OrderedDict(vocab)
        self._id_to_token = OrderedDict(
            {int(v): k for k, v in vocab.items()}
        )

    def _save_vocab(self, vocab_file: str):
        """Save vocabulary to a JSON file."""
        with open(vocab_file, "w", encoding="utf-8") as f:
            json.dump(self._token_to_id, f, ensure_ascii=False, indent=2)

    # ===================== Vocab Building =====================

    def build_vocab(
        self,
        texts: Union[List[str], str],
        min_frequency: Optional[int] = None,
        show_progress: bool = True,
    ) -> int:
        """
        Build vocabulary from a corpus of Tamil texts.

        This must be called before using the tokenizer for encoding,
        unless loading from a pre-built vocabulary.

        Args:
            texts: List of Tamil text strings, or path to a text file
                   (one sentence per line).
            min_frequency: Minimum token frequency to include. Overrides
                           the value set in __init__ if provided.
            show_progress: Print progress information.

        Returns:
            Vocabulary size (including special tokens).
        """
        if min_frequency is not None:
            self._min_frequency = min_frequency

        # Handle file path input
        if isinstance(texts, str) and os.path.isfile(texts):
            with open(texts, "r", encoding="utf-8") as f:
                texts = [line.strip() for line in f if line.strip()]

        # Count token frequencies
        token_freq: Dict[str, int] = {}
        total = len(texts)

        for i, text in enumerate(texts):
            if show_progress and (i + 1) % 10000 == 0:
                logger.info(f"  Processing {i + 1}/{total} texts...")
            tokens = self._tokenize_text(text)
            for tok in tokens:
                token_freq[tok] = token_freq.get(tok, 0) + 1

        # Reset vocabulary with special tokens first
        self._token_to_id = OrderedDict()
        self._id_to_token = OrderedDict()
        self._ensure_special_tokens_in_vocab()

        # Add tokens meeting frequency threshold, sorted by frequency
        sorted_tokens = sorted(
            token_freq.items(), key=lambda x: (-x[1], x[0])
        )
        for tok, freq in sorted_tokens:
            if freq >= self._min_frequency and tok not in self._token_to_id:
                idx = len(self._token_to_id)
                self._token_to_id[tok] = idx
                self._id_to_token[idx] = tok

        if show_progress:
            logger.info(f"  Vocabulary built: {len(self._token_to_id)} tokens "
                  f"(from {len(token_freq)} unique tokens, "
                  f"min_frequency={self._min_frequency})")

        return len(self._token_to_id)

    # ===================== Core Tokenizer Interface =====================

    @property
    def vocab_size(self) -> int:
        """Size of the vocabulary."""
        return len(self._token_to_id)

    def get_vocab(self) -> Dict[str, int]:
        """Returns the vocabulary as a dict of token to index."""
        return dict(self._token_to_id)

    def _tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text using the Tamil tokenizer at the configured level.

        Returns a list of token strings.
        """
        tokens = self._tamil_tokenizer.tokenize(text, level=self._level)
        return [t.text for t in tokens]

    def _tokenize(self, text: str, **kwargs) -> List[str]:
        """
        HuggingFace interface: tokenize text into subword strings.

        This is called by the PreTrainedTokenizer base class.
        """
        return self._tokenize_text(text)

    def _convert_token_to_id(self, token: str) -> int:
        """Convert a token string to its vocabulary ID."""
        return self._token_to_id.get(
            token, self._token_to_id.get(self.unk_token, 0)
        )

    def _convert_id_to_token(self, index: int) -> str:
        """Convert a vocabulary ID to its token string."""
        return self._id_to_token.get(index, self.unk_token)

    def convert_tokens_to_string(self, tokens: List[str]) -> str:
        """
        Convert a list of tokens back to a string.

        For Tamil, we join with spaces (word/morpheme level) or
        directly concatenate (character level).
        """
        if self._level == "character":
            return "".join(tokens)
        return " ".join(tokens)

    # ===================== Save / Load =====================

    def save_vocabulary(
        self,
        save_directory: str,
        filename_prefix: Optional[str] = None,
    ) -> Tuple[str]:
        """Save the vocabulary to a directory."""
        if not os.path.isdir(save_directory):
            os.makedirs(save_directory, exist_ok=True)

        prefix = f"{filename_prefix}-" if filename_prefix else ""
        vocab_path = os.path.join(save_directory, prefix + VOCAB_FILENAME)
        config_path = os.path.join(save_directory, prefix + CONFIG_FILENAME)

        # Save vocabulary
        self._save_vocab(vocab_path)

        # Save tokenizer config (level, min_frequency)
        config = {
            "level": self._level,
            "min_frequency": self._min_frequency,
            "vocab_size": len(self._token_to_id),
        }
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        return (vocab_path,)

    @classmethod
    def from_pretrained(cls, pretrained_path: str, **kwargs):
        """
        Load a TamilHFTokenizer from a directory.

        Args:
            pretrained_path: Path to directory containing saved tokenizer.
            **kwargs: Additional arguments.

        Returns:
            TamilHFTokenizer instance.
        """
        vocab_file = os.path.join(pretrained_path, VOCAB_FILENAME)
        config_file = os.path.join(pretrained_path, CONFIG_FILENAME)

        level = kwargs.pop("level", "morpheme")
        min_frequency = kwargs.pop("min_frequency", 1)

        if os.path.isfile(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
            level = config.get("level", level)
            min_frequency = config.get("min_frequency", min_frequency)

        if not os.path.isfile(vocab_file):
            raise FileNotFoundError(
                f"Vocabulary file not found at {vocab_file}. "
                f"Build vocabulary first with build_vocab()."
            )

        return cls(
            level=level,
            vocab_file=vocab_file,
            min_frequency=min_frequency,
            **kwargs,
        )

    # ===================== Convenience =====================

    @property
    def level(self) -> str:
        """The tokenization level (word, morpheme, or character)."""
        return self._level

    def __repr__(self) -> str:
        return (
            f"TamilHFTokenizer(level='{self._level}', "
            f"vocab_size={self.vocab_size})"
        )
