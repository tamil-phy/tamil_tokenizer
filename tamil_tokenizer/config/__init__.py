"""Tamil tokenizer configuration module."""

from .constants import ConfigConstants, DEFAULT_FILE_PATHS
from .config_loader import ConfigLoader, ReadConfig
from .constant_table import TamilConstantTable

__all__ = [
    'ConfigConstants',
    'DEFAULT_FILE_PATHS',
    'ConfigLoader',
    'ReadConfig',
    'TamilConstantTable',
]
