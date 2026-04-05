"""
Comprehensive benchmark data for Tamil Tokenizer test suite.

Covers diverse Tamil text categories:
- Simple sentences, compound sentences, complex literary text
- All 8 vibhakti (case) forms
- Verb tenses (past, present, future)
- Person/number markers
- Proper nouns, place names, numbers, mixed scripts
- Edge cases: empty, whitespace, punctuation-only, single characters
"""

# ============================================================
# SENTENCE TOKENIZATION BENCHMARK
# ============================================================

SENTENCE_CASES = [
    # (input_text, expected_sentence_count, description)
    ("அவன் வந்தான்.", 1, "single_sentence"),
    ("அவன் வந்தான். அவள் பார்த்தாள்.", 2, "two_sentences_period"),
    ("வணக்கம்! எப்படி இருக்கிறீர்கள்?", 2, "exclamation_and_question"),
    (
        "நான் பள்ளிக்கு சென்றேன். அங்கு நண்பர்களை சந்தித்தேன். மகிழ்ச்சியாக இருந்தது.",
        3,
        "three_sentences",
    ),
    (
        "என்ன செய்கிறாய்? நான் படிக்கிறேன். நீ வா!",
        3,
        "mixed_punctuation_endings",
    ),
    ("வணக்கம்", 1, "no_ending_punctuation"),
    (
        "திருவள்ளுவர் திருக்குறளை எழுதினார். அது 1330 குறள்களை கொண்டது. "
        "ஒவ்வொரு குறளும் இரண்டு அடிகளை கொண்டது.",
        3,
        "literary_reference",
    ),
    ("விலை 3.14 ரூபாய்.", 1, "decimal_number_not_sentence_break"),
    (
        "காலை 6.30 மணிக்கு எழுந்தேன். பின்னர் பள்ளிக்கு சென்றேன்.",
        2,
        "time_with_decimal",
    ),
]

# ============================================================
# WORD TOKENIZATION BENCHMARK
# ============================================================

WORD_CASES = [
    # (input_text, expected_words_list, description)
    ("அவன் வந்தான்.", ["அவன்", "வந்தான்", "."], "simple_sentence"),
    (
        "நான் தமிழ் படிக்கிறேன்.",
        ["நான்", "தமிழ்", "படிக்கிறேன்", "."],
        "present_tense",
    ),
    (
        "100 ரூபாய் கொடு.",
        ["100", "ரூபாய்", "கொடு", "."],
        "number_and_words",
    ),
    (
        "5,595 பேருக்கு உதவி செய்தனர்.",
        ["5,595", "பேருக்கு", "உதவி", "செய்தனர்", "."],
        "formatted_number",
    ),
    ("வணக்கம்!", ["வணக்கம்", "!"], "single_word_exclamation"),
    (
        "அ, ஆ, இ, ஈ.",
        ["அ", ",", "ஆ", ",", "இ", ",", "ஈ", "."],
        "single_letters_with_commas",
    ),
    (
        "தமிழ்நாடு இந்தியாவின் ஒரு மாநிலம்.",
        ["தமிழ்நாடு", "இந்தியாவின்", "ஒரு", "மாநிலம்", "."],
        "place_names",
    ),
]

# ============================================================
# CHARACTER TOKENIZATION BENCHMARK
# ============================================================

CHARACTER_CASES = [
    # (input_word, expected_letters, expected_types, description)
    (
        "அ",
        ["அ"],
        ["vowel"],
        "single_vowel",
    ),
    (
        "ஃ",
        ["ஃ"],
        ["special"],
        "aytham",
    ),
    (
        "க்",
        ["க்"],
        ["consonant"],
        "pure_consonant",
    ),
    (
        "க",
        ["க"],
        ["vowel_consonant"],
        "vowel_consonant_implicit_a",
    ),
    (
        "கா",
        ["கா"],
        ["vowel_consonant"],
        "vowel_consonant_aa",
    ),
    (
        "தமிழ்",
        ["த", "மி", "ழ்"],
        ["vowel_consonant", "vowel_consonant", "consonant"],
        "word_tamil",
    ),
    (
        "அஆஇஈஉஊ",
        ["அ", "ஆ", "இ", "ஈ", "உ", "ஊ"],
        ["vowel"] * 6,
        "six_vowels",
    ),
    (
        "க்ங்ச்",
        ["க்", "ங்", "ச்"],
        ["consonant"] * 3,
        "three_consonants",
    ),
    (
        "வணக்கம்",
        ["வ", "ண", "க்", "க", "ம்"],
        ["vowel_consonant", "vowel_consonant", "consonant", "vowel_consonant", "consonant"],
        "vanakkam",
    ),
    (
        "தமிழ்நாடு",
        ["த", "மி", "ழ்", "நா", "டு"],
        ["vowel_consonant", "vowel_consonant", "consonant", "vowel_consonant", "vowel_consonant"],
        "tamilnadu",
    ),
    (
        "கொ",
        ["கொ"],
        ["vowel_consonant"],
        "two_part_vowel_sign_ko",
    ),
    (
        "கோ",
        ["கோ"],
        ["vowel_consonant"],
        "two_part_vowel_sign_koo",
    ),
    (
        "பௌ",
        ["பௌ"],
        ["vowel_consonant"],
        "two_part_vowel_sign_pau",
    ),
]

# Consonant classification data
CONSONANT_CLASSES = [
    # (letter, expected_class_en)
    ("க்", "vallinam"),
    ("ச்", "vallinam"),
    ("ட்", "vallinam"),
    ("த்", "vallinam"),
    ("ப்", "vallinam"),
    ("ற்", "vallinam"),
    ("ங்", "mellinam"),
    ("ஞ்", "mellinam"),
    ("ண்", "mellinam"),
    ("ந்", "mellinam"),
    ("ம்", "mellinam"),
    ("ன்", "mellinam"),
    ("ய்", "idaiyinam"),
    ("ர்", "idaiyinam"),
    ("ல்", "idaiyinam"),
    ("ள்", "idaiyinam"),
    ("ழ்", "idaiyinam"),
    ("வ்", "idaiyinam"),
]

# ============================================================
# MORPHEME TOKENIZATION BENCHMARK
# ============================================================

# Case suffix (வேற்றுமை) tests — suffixes loaded from mainConstant.list
VETRUMAI_CASES = [
    # (input_word, expected_root, expected_suffix, description)
    ("பள்ளிக்கு", "பள்ளிக்", "கு", "dative_kku"),
    ("மரத்தின்", "மரத்த", "இன்", "ablative_in"),
    ("நண்பனோடு", "நண்பன", "ஓடு", "instrumental_odu"),
    ("சென்னை", "சென்ன", "ஐ", "accusative_ai"),
]

# Words that should NOT decompose (proper nouns, base forms)
NO_DECOMPOSITION_WORDS = [
    # (word, description)
    ("தமிழ்நாடு", "proper_noun_tamilnadu"),
    ("நன்றி", "word_nanri"),
    ("அவன்", "pronoun_he"),
]

# Morpheme tokenization of full sentences
MORPHEME_SENTENCE_CASES = [
    # (input_text, min_token_count, has_root, has_suffix_or_case, description)
    ("பள்ளிக்கு சென்றான்.", 3, True, True, "school_went"),
    ("அவன் வந்தான்.", 3, True, False, "he_came"),
    ("வீட்டில் இருந்தான்.", 3, True, True, "was_at_home"),
    ("நான் தமிழ் படிக்கிறேன்.", 4, True, False, "i_study_tamil"),
]

# ============================================================
# EDGE CASES
# ============================================================

EDGE_CASES_EMPTY = [
    # (input_text, description)
    ("", "empty_string"),
    ("   ", "whitespace_only"),
    ("\n\t", "tabs_and_newlines"),
]

EDGE_CASES_SPECIAL = [
    # (input_text, expected_token_count, description)
    (".", 1, "single_period"),
    ("...", 3, "ellipsis"),
    ("!?.", 3, "punctuation_only"),
    ("123", 1, "number_only"),
    ("1,234.56", 1, "formatted_decimal"),
]

EDGE_CASES_SINGLE_CHAR = [
    # (input_char, expected_type, description)
    ("அ", "word", "single_vowel_as_word"),
    ("க", "word", "single_consonant_as_word"),
]

# ============================================================
# CLI TEST DATA
# ============================================================

CLI_TEST_CASES = [
    # (args_list, expected_in_output, description)
    (
        ["அவன் வந்தான்."],
        "Tokenization Level: word",
        "default_word_table",
    ),
    (
        ["அவன் வந்தான்.", "--level", "character"],
        "Tokenization Level: character",
        "character_table",
    ),
    (
        ["அவன் வந்தான். அவள் பார்த்தாள்.", "--level", "sentence"],
        "Tokenization Level: sentence",
        "sentence_table",
    ),
    (
        ["பள்ளிக்கு", "--level", "morpheme"],
        "Tokenization Level: morpheme",
        "morpheme_table",
    ),
    (
        ["அவன் வந்தான்.", "--format", "json"],
        '"type": "word"',
        "json_format",
    ),
    (
        ["அவன் வந்தான்.", "--format", "text"],
        "அவன்",
        "text_format",
    ),
    (
        ["--version"],
        "Tamil Tokenizer",
        "version_flag",
    ),
]

# ============================================================
# PERFORMANCE BENCHMARK CORPUS
# ============================================================

BENCHMARK_CORPUS_SHORT = "அவன் வந்தான்."

BENCHMARK_CORPUS_MEDIUM = (
    "தமிழ் மொழி உலகின் மிகப் பழமையான மொழிகளில் ஒன்று. "
    "இது இந்தியாவின் தமிழ்நாடு மாநிலத்தின் ஆட்சி மொழி. "
    "இலங்கை மற்றும் சிங்கப்பூரிலும் ஆட்சி மொழியாக உள்ளது."
)

BENCHMARK_CORPUS_LONG = (
    "திருவள்ளுவர் எழுதிய திருக்குறள் தமிழ் இலக்கியத்தின் மிக முக்கியமான நூல் ஆகும். "
    "இது அறம், பொருள், இன்பம் என்ற மூன்று பிரிவுகளாக பிரிக்கப்பட்டுள்ளது. "
    "ஒவ்வொரு பிரிவும் பல அதிகாரங்களைக் கொண்டது. "
    "ஒவ்வொரு அதிகாரமும் பத்து குறள்களை கொண்டுள்ளது. "
    "மொத்தம் 1330 குறள்கள் உள்ளன. "
    "இந்நூல் பல மொழிகளில் மொழிபெயர்க்கப்பட்டுள்ளது. "
    "தமிழர்கள் இதை மிகவும் போற்றுகின்றனர். "
    "பள்ளிகளில் கட்டாயமாக கற்பிக்கப்படுகிறது. "
    "வாழ்வியல் நெறிகளை எளிமையாக கூறும் இந்நூல் காலத்தை வென்றது. "
    "உலகப் பொதுமறை என்று இதை அழைக்கின்றனர்."
)

# Diverse Tamil sentences for comprehensive testing
DIVERSE_SENTENCES = [
    "வணக்கம், எப்படி இருக்கிறீர்கள்?",
    "நான் நேற்று சென்னைக்கு போனேன்.",
    "குழந்தைகள் பள்ளிக்கூடத்தில் விளையாடுகிறார்கள்.",
    "தமிழ்நாட்டின் தலைநகரம் சென்னை ஆகும்.",
    "அவர்கள் நாளை வருவார்கள்.",
    "இந்த புத்தகம் மிகவும் சுவாரசியமானது.",
    "கடலோரத்தில் அலைகள் மோதுகின்றன.",
    "பாரதியார் தமிழின் மிகச் சிறந்த கவிஞர்.",
    "மழை பெய்தால் வெள்ளம் வரும்.",
    "அரசு மருத்துவமனையில் இலவச சிகிச்சை அளிக்கப்படுகிறது.",
]
