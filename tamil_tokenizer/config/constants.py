"""
Config Constants - Equivalent to ConfigConstants.java

This module defines constant names for configuration file keys.

Author: Rajamani David (Original Java)
Since: Oct 25, 2017
"""


class ConfigConstants:
    """
    Configuration file key constants.
    Used to reference files in allFileList.list configuration.
    """

    # Main constant file names
    MAIN_CONSTANT_FILE_NAME = "mainConstantFileName"
    TWIN_CONSTANT_FILE_NAME = "twinConstantFileName"
    VERB_CONSTANT_FILE_NAME = "verbConstantFileName"
    NOUN_CONSTANT_FILE_NAME = "nounConstantFileName"

    # Parse order file names
    PARSE_ORDER_FILE_NAME = "parseOrderFileName"
    TWIN_PARSE_ORDER_FILE_NAME = "twinParseOrderFileName"
    NOUN_PARSE_ORDER_FILE_NAME = "nounParseOrderFileName"
    VERB_PARSE_ORDER_FILE_NAME = "verbParseOrderFileName"

    # Ignore list file names
    IGNORE_LIST_FILE_NAME = "ignoreListFileName"
    IGNORE_VERB_LIST_FILE_NAME = "ignoreVerbListFileName"
    IGNORE_NOUN_LIST_FILE_NAME = "ignoreNounListFileName"
    IGNORE_OTHER_GRAMMAR_LIST_FILE_NAME = "ignoreOtherGrammarFileName"
    IGNORE_PERSON_LIST_FILE_NAME = "ignorePersonListFileName"
    IGNORE_PLACE_LIST_FILE_NAME = "ignorePlaceListFileName"

    # Unicode and parse map file names
    UNICODE_MAP_FILE_NAME = "unicodeFileName"
    MAIN_PARSE_MAP_FILE_NAME = "mainParseMapFileName"
    NOUN_PARSE_MAP_FILE_NAME = "nounParseMapFileName"
    VERB_PARSE_MAP_FILE_NAME = "verbParseMapFileName"

    # Other file names
    WORD_LIST_FILE_NAME = "wordListFileName"
    RESULT_FILE_NAME = "resultFileName"
    UNIQUE_LIST = "uniqueListFileName"
    PARSE_FILE_NAME = "parseFileName"
    SPECIAL_CHARACTER_FILE_NAME = "specialCharacterFileName"
    CONDITIONAL_FILE_NAME = "conditionalFileName"
    PREFIX_FILE_NAME = "preFixFileName"


# Default file paths relative to data directory
DEFAULT_FILE_PATHS = {
    ConfigConstants.MAIN_CONSTANT_FILE_NAME: "mainConstant.list",
    ConfigConstants.PARSE_ORDER_FILE_NAME: "parseOrder.list",
    ConfigConstants.MAIN_PARSE_MAP_FILE_NAME: "main_parse_map.list",
    ConfigConstants.IGNORE_VERB_LIST_FILE_NAME: "ignoreVerb.list",
    ConfigConstants.IGNORE_NOUN_LIST_FILE_NAME: "ignoreNoun.list",
    ConfigConstants.IGNORE_OTHER_GRAMMAR_LIST_FILE_NAME: "ignoreOtherGrammar.list",
    ConfigConstants.IGNORE_PERSON_LIST_FILE_NAME: "ignorePerson.list",
    ConfigConstants.IGNORE_PLACE_LIST_FILE_NAME: "ignorePlace.list",
    ConfigConstants.SPECIAL_CHARACTER_FILE_NAME: "specialCharacter.list",
    ConfigConstants.CONDITIONAL_FILE_NAME: "condition_rule.list",
    ConfigConstants.PREFIX_FILE_NAME: "prefix.list",
    ConfigConstants.WORD_LIST_FILE_NAME: "word.list",
    ConfigConstants.VERB_CONSTANT_FILE_NAME: "verbConstants.list",
    ConfigConstants.NOUN_CONSTANT_FILE_NAME: "nounConstants.list",
    ConfigConstants.VERB_PARSE_ORDER_FILE_NAME: "verbParseOrder.list",
    ConfigConstants.NOUN_PARSE_ORDER_FILE_NAME: "nounParseOrder.list",
    ConfigConstants.VERB_PARSE_MAP_FILE_NAME: "verb_parse_map.list",
    ConfigConstants.NOUN_PARSE_MAP_FILE_NAME: "noun_parse_map.list",
}
