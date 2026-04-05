"""
Comprehensive stress test to probe flaws across all tokenization levels.
Tests: sentence, word, character, morpheme with diverse Tamil inputs.
"""

import sys
from tamil_tokenizer import TamilTokenizer, Token, TokenType

tok = TamilTokenizer()

PASS = 0
FAIL = 0
FLAWS = []

def check(test_id, condition, msg):
    global PASS, FAIL
    if condition:
        PASS += 1
    else:
        FAIL += 1
        FLAWS.append(f"[{test_id}] {msg}")
        print(f"  FAIL [{test_id}] {msg}")

def section(title):
    print(f"\n{'='*60}\n  {title}\n{'='*60}")

# ============================================================
# 1. SENTENCE TOKENIZATION
# ============================================================
section("SENTENCE TOKENIZATION")

# Basic splits
s1 = tok.sentence_tokenize("வணக்கம். நன்றி.")
check("S01", len(s1) == 2, f"Two sentences expected, got {len(s1)}: {[t.text for t in s1]}")

# No punctuation → one sentence
s2 = tok.sentence_tokenize("நான் தமிழ் படிக்கிறேன்")
check("S02", len(s2) == 1, f"Single sentence without punct, got {len(s2)}")

# Mixed punctuation
s3 = tok.sentence_tokenize("என்ன? ஏன்! சரி.")
check("S03", len(s3) == 3, f"3 sentences expected, got {len(s3)}: {[t.text for t in s3]}")

# Decimal should NOT break sentence
s4 = tok.sentence_tokenize("விலை 3.14 ரூபாய்.")
check("S04", len(s4) == 1, f"Decimal 3.14 should not break, got {len(s4)}: {[t.text for t in s4]}")

# Time with decimal
s5 = tok.sentence_tokenize("காலை 6.30 மணி. மாலை 5.00 மணி.")
check("S05", len(s5) == 2, f"Two time sentences, got {len(s5)}: {[t.text for t in s5]}")

# Empty / whitespace
check("S06", tok.sentence_tokenize("") == [], "Empty input should return []")
check("S07", tok.sentence_tokenize("   \n\t  ") == [], "Whitespace input should return []")

# Single character
s8 = tok.sentence_tokenize("அ")
check("S08", len(s8) == 1, f"Single char should be 1 sentence, got {len(s8)}")

# Multiple periods in a row (ellipsis-like)
s9 = tok.sentence_tokenize("அவன் வந்தான்... பின் சென்றான்.")
check("S09", len(s9) >= 1, f"Ellipsis handling, got {len(s9)}: {[t.text for t in s9]}")

# Sentence positions should not overlap
s10 = tok.sentence_tokenize("ஒன்று. இரண்டு. மூன்று.")
positions_ok = True
prev_end = -1
for t in s10:
    if t.start < prev_end or t.end <= t.start:
        positions_ok = False
    prev_end = t.end
check("S10", positions_ok, f"Sentence positions overlap: {[(t.start,t.end,t.text) for t in s10]}")

# Long paragraph
long_para = "தமிழ் பழமையான மொழி. இது இந்தியாவில் பேசப்படுகிறது. உலகில் பல நாடுகளிலும் உள்ளது. சங்க இலக்கியம் புகழ்பெற்றது. திருக்குறள் உலகப் பொதுமறை."
s11 = tok.sentence_tokenize(long_para)
check("S11", len(s11) == 5, f"5 sentences in paragraph, got {len(s11)}: {[t.text for t in s11]}")

# ============================================================
# 2. WORD TOKENIZATION
# ============================================================
section("WORD TOKENIZATION")

# Basic
w1 = tok.word_tokenize("அவன் வந்தான்.")
w1_texts = [t.text for t in w1]
check("W01", w1_texts == ["அவன்", "வந்தான்", "."], f"Basic word split: {w1_texts}")

# Numbers
w2 = tok.word_tokenize("100 ரூபாய்")
check("W02", w2[0].token_type == TokenType.NUMBER, f"100 should be NUMBER, got {w2[0].token_type}")

# Formatted number
w3 = tok.word_tokenize("5,595 பேர்")
check("W03", w3[0].text == "5,595" and w3[0].token_type == TokenType.NUMBER,
      f"Formatted number: {w3[0].text} / {w3[0].token_type}")

# Punctuation types
w4 = tok.word_tokenize("வா! ஏன்? சரி, நன்றி.")
punct_texts = [t.text for t in w4 if t.token_type == TokenType.PUNCTUATION]
check("W04", set(punct_texts) >= {"!", "?", ",", "."}, f"Punct types: {punct_texts}")

# Position accuracy — token text should match source slice
text5 = "நான் பள்ளிக்கு சென்றேன்."
w5 = tok.word_tokenize(text5)
pos_ok = all(text5[t.start:t.end] == t.text for t in w5)
check("W05", pos_ok, f"Position mismatch: {[(t.text, text5[t.start:t.end]) for t in w5 if text5[t.start:t.end] != t.text]}")

# Content preservation — all non-whitespace should be in tokens
text6 = "தமிழ்நாடு இந்தியாவின் ஒரு மாநிலம்."
w6 = tok.word_tokenize(text6)
reconstructed = "".join(t.text for t in w6)
original_no_ws = text6.replace(" ", "")
check("W06", reconstructed == original_no_ws,
      f"Content lost: '{reconstructed}' vs '{original_no_ws}'")

# Empty/whitespace
check("W07", tok.word_tokenize("") == [], "Empty word tokenize should return []")
check("W08", tok.word_tokenize("   ") == [], "Whitespace word tokenize should return []")

# Mixed Tamil + English (if present)
w9 = tok.word_tokenize("hello உலகம்")
check("W09", len(w9) >= 2, f"Mixed Tamil/English, got {len(w9)}: {[t.text for t in w9]}")

# Consecutive punctuation
w10 = tok.word_tokenize("!!??")
check("W10", len(w10) == 4, f"Consecutive punct should be separate, got {len(w10)}: {[t.text for t in w10]}")

# Hyphenated / dash
w11 = tok.word_tokenize("தமிழ்-நாடு")
check("W11", len(w11) >= 2, f"Hyphenated word, got {len(w11)}: {[t.text for t in w11]}")

# Long sentence token count
text12 = "தமிழ் மொழி உலகின் மிகப் பழமையான மொழிகளில் ஒன்று என்பதை அனைவரும் அறிவர்."
w12 = tok.word_tokenize(text12)
check("W12", len(w12) >= 10, f"Long sentence should have >= 10 tokens, got {len(w12)}")

# ============================================================
# 3. CHARACTER TOKENIZATION
# ============================================================
section("CHARACTER TOKENIZATION")

# Basic vowels
c1 = tok.character_tokenize("அஆஇஈஉஊ")
c1_texts = [t.text for t in c1]
check("C01", len(c1) == 6 and all(t.token_type == TokenType.VOWEL for t in c1),
      f"6 vowels: {c1_texts}, types={[t.token_type.value for t in c1]}")

# All 12 vowels
c2 = tok.character_tokenize("அஆஇஈஉஊஎஏஐஒஓஔ")
check("C02", len(c2) == 12, f"12 vowels expected, got {len(c2)}")

# Pure consonants (மெய்)
c3 = tok.character_tokenize("க்ங்ச்ட்")
check("C03", len(c3) == 4 and all(t.token_type == TokenType.CONSONANT for t in c3),
      f"4 consonants: {[t.text for t in c3]}")

# Vowel-consonant (உயிர்மெய்)
c4 = tok.character_tokenize("கா")
check("C04", len(c4) == 1 and c4[0].token_type == TokenType.VOWEL_CONSONANT,
      f"கா should be 1 vowel_consonant: {[t.text for t in c4]}")

# Aytham
c5 = tok.character_tokenize("ஃ")
check("C05", len(c5) == 1 and c5[0].token_type == TokenType.SPECIAL, f"ஃ type: {c5[0].token_type}")

# Complex word: வணக்கம் = வ + ண + க் + க + ம்
c6 = tok.character_tokenize("வணக்கம்")
c6_texts = [t.text for t in c6]
check("C06", c6_texts == ["வ", "ண", "க்", "க", "ம்"],
      f"வணக்கம் letters: {c6_texts}")

# Two-part vowel signs: கொ, கோ, கௌ
c7_ko = tok.character_tokenize("கொ")
c7_koo = tok.character_tokenize("கோ")
c7_kau = tok.character_tokenize("கௌ")
check("C07a", len(c7_ko) == 1 and c7_ko[0].text == "கொ", f"கொ: {[t.text for t in c7_ko]}")
check("C07b", len(c7_koo) == 1 and c7_koo[0].text == "கோ", f"கோ: {[t.text for t in c7_koo]}")
check("C07c", len(c7_kau) == 1 and c7_kau[0].text == "கௌ", f"கௌ: {[t.text for t in c7_kau]}")

# Position continuity
c8 = tok.character_tokenize("தமிழ்நாடு")
pos_ok = (c8[0].start == 0 and
          all(c8[i].start == c8[i-1].end for i in range(1, len(c8))) and
          c8[-1].end == len("தமிழ்நாடு"))
check("C08", pos_ok, f"Position continuity: {[(t.text, t.start, t.end) for t in c8]}")

# Empty
check("C09", tok.character_tokenize("") == [], "Empty char tokenize should be []")

# Grantha letters (ஜ, ஷ, ஸ, ஹ)
c10 = tok.character_tokenize("ஜ்ஷ்ஸ்ஹ்")
check("C10", len(c10) == 4 and all(t.token_type == TokenType.CONSONANT for t in c10),
      f"Grantha consonants: {[t.text for t in c10]}, types={[t.token_type.value for t in c10]}")

# Consonant classification metadata
c11 = tok.character_tokenize("க்")
check("C11", c11[0].metadata.get("class_en") == "vallinam",
      f"க் should be vallinam: {c11[0].metadata}")

c12 = tok.character_tokenize("ங்")
check("C12", c12[0].metadata.get("class_en") == "mellinam",
      f"ங் should be mellinam: {c12[0].metadata}")

c13 = tok.character_tokenize("ய்")
check("C13", c13[0].metadata.get("class_en") == "idaiyinam",
      f"ய் should be idaiyinam: {c13[0].metadata}")

# Long word: சிங்கப்பூர்
c14 = tok.character_tokenize("சிங்கப்பூர்")
c14_texts = [t.text for t in c14]
check("C14", c14_texts == ["சி", "ங்", "க", "ப்", "பூ", "ர்"],
      f"சிங்கப்பூர் letters: {c14_texts}")

# Character-level via tokenize pipeline
c15 = tok.tokenize("தமிழ்.", level="character")
c15_types = [t.token_type for t in c15]
check("C15", TokenType.PUNCTUATION in c15_types and TokenType.CONSONANT in c15_types,
      f"Pipeline char tokenize: {[(t.text, t.token_type.value) for t in c15]}")

# ============================================================
# 4. MORPHEME TOKENIZATION
# ============================================================
section("MORPHEME TOKENIZATION")

def morph_check(test_id, word, exp_root=None, exp_suffix=None, min_tokens=None,
                should_decompose=True, description=""):
    """Helper for morpheme checks."""
    tokens = tok.morpheme_tokenize(word)
    texts = [t.text for t in tokens]
    types = [t.token_type for t in tokens]
    
    if min_tokens is not None:
        check(test_id + "_cnt", len(tokens) >= min_tokens,
              f"'{word}' ({description}): expected >= {min_tokens} tokens, got {len(tokens)}: {texts}")
    
    if should_decompose and exp_root is not None:
        root_tokens = [t for t in tokens if t.token_type == TokenType.ROOT]
        if root_tokens:
            check(test_id + "_root", root_tokens[0].text == exp_root,
                  f"'{word}' ({description}): root expected '{exp_root}', got '{root_tokens[0].text}'")
        else:
            check(test_id + "_root", False, f"'{word}' ({description}): no ROOT token found")
    
    if should_decompose and exp_suffix is not None:
        suffix_tokens = [t for t in tokens if t.token_type in (
            TokenType.CASE_SUFFIX, TokenType.SUFFIX, TokenType.TENSE_MARKER, TokenType.PERSON_MARKER)]
        suffix_text = "".join(t.text for t in suffix_tokens)
        check(test_id + "_sfx", suffix_text == exp_suffix,
              f"'{word}' ({description}): suffix expected '{exp_suffix}', got '{suffix_text}'")
    
    if not should_decompose:
        check(test_id + "_nodecomp", len(tokens) == 1 and tokens[0].token_type == TokenType.ROOT,
              f"'{word}' ({description}): should NOT decompose, got {texts} / {[t.value for t in types]}")
    
    return tokens

# --- Case suffix (வேற்றுமை) tests ---
print("\n--- Case suffixes ---")

# 2nd case (accusative): ஐ
morph_check("M01", "மரத்தை", description="accusative_ai")

# 3rd case (instrumental): ஆல்
morph_check("M02", "மழையால்", description="instrumental_aal")

# 4th case (dative): கு / க்கு
morph_check("M03", "பள்ளிக்கு", description="dative_kku")

# 4th case + postposition (compound): க்காக (our recent fix)
morph_check("M04", "உணவுக்காக", exp_root="உணவு", exp_suffix="க்காக",
            description="dative+postposition_kaaga")

# 5th case (ablative): இன், இல், இருந்து
morph_check("M05", "மரத்தின்", description="ablative_in")

# 6th case (possessive): அது
morph_check("M06", "அவனது", description="possessive_athu")

# 7th case (locative): இல்
morph_check("M07", "வீட்டில்", description="locative_il")

# Postposition: மேல்
morph_check("M08", "மேசையின்மேல்", description="postposition_mel")

# Postposition: கீழ்
morph_check("M09", "மரத்துக்கீழ்", description="postposition_keezh")

# --- compound suffix with sandhi (expanded from our fix) ---
print("\n--- Compound sandhi suffixes ---")
morph_check("M10", "வீட்டுக்காக", description="compound_veettu_kaaga")
morph_check("M11", "படிப்புக்காக", description="compound_padippu_kaaga")
morph_check("M12", "பணத்துக்காக", description="compound_panathu_kaaga")

# --- No-decomposition words ---
print("\n--- No-decomposition ---")
morph_check("M20", "தமிழ்நாடு", should_decompose=False, description="proper_noun")
morph_check("M21", "நன்றி", should_decompose=False, description="base_word")
morph_check("M22", "அவன்", should_decompose=False, description="pronoun")
morph_check("M23", "வணக்கம்", should_decompose=False, description="greeting")

# --- Root always present ---
print("\n--- Root always present ---")
for word in ["வந்தான்", "போகிறான்", "படிப்பான்", "நல்ல", "பெரிய", "சிறிய", "அழகான"]:
    tokens = tok.morpheme_tokenize(word)
    roots = [t for t in tokens if t.token_type == TokenType.ROOT]
    check(f"M30_{word}", len(roots) >= 1, f"'{word}': no ROOT token")

# --- Token types must be valid morpheme types ---
print("\n--- Valid morpheme types ---")
valid_morph_types = {
    TokenType.ROOT, TokenType.SUFFIX, TokenType.CASE_SUFFIX,
    TokenType.TENSE_MARKER, TokenType.PERSON_MARKER, TokenType.PLURAL_MARKER
}
for word in ["பள்ளிக்கு", "உணவுக்காக", "வந்தான்"]:
    tokens = tok.morpheme_tokenize(word)
    for t in tokens:
        check(f"M40_{word}_{t.text}", t.token_type in valid_morph_types,
              f"'{word}': unexpected type {t.token_type} for '{t.text}'")

# --- Empty ---
check("M50", tok.morpheme_tokenize("") == [], "Empty morpheme should return []")
check("M51", tok.morpheme_tokenize("   ") == [], "Whitespace morpheme should return []")

# --- Sentence-level morpheme pipeline ---
print("\n--- Sentence-level morpheme pipeline ---")
m60 = tok.tokenize("அவன் வந்தான்.", level="morpheme")
m60_types = {t.token_type for t in m60}
check("M60", TokenType.ROOT in m60_types, f"Sentence morpheme should have ROOT: {[(t.text, t.token_type.value) for t in m60]}")
check("M61", TokenType.PUNCTUATION in m60_types, f"Sentence morpheme should have PUNCTUATION")

# Multiple case forms of same base
print("\n--- Multiple case forms ---")
forms = {
    "பள்ளிக்கு": "dative",
    "பள்ளியை": "accusative",
    "பள்ளியில்": "locative",
    "பள்ளியோடு": "sociative",
}
for form, desc in forms.items():
    tokens = tok.tokenize(form, level="morpheme")
    check(f"M70_{desc}", len(tokens) >= 1, f"'{form}' ({desc}) failed to tokenize")

# ============================================================
# 5. CROSS-LEVEL CONSISTENCY
# ============================================================
section("CROSS-LEVEL CONSISTENCY")

# tokenize_to_strings should match tokenize texts
text = "அவன் பள்ளிக்கு சென்றான்."
for level in ["sentence", "word", "character", "morpheme"]:
    strs = tok.tokenize_to_strings(text, level=level)
    tokens = tok.tokenize(text, level=level)
    token_texts = [t.text for t in tokens]
    check(f"X01_{level}", strs == token_texts,
          f"tokenize_to_strings vs tokenize mismatch at level={level}")

# tokenize_to_dicts should have correct keys
dicts = tok.tokenize_to_dicts("வணக்கம்.", level="word")
for d in dicts:
    check(f"X02_{d['text']}", all(k in d for k in ("text", "type", "start", "end", "metadata")),
          f"Dict missing keys: {d.keys()}")

# Invalid level should raise ValueError
try:
    tok.tokenize("test", level="invalid")
    check("X03", False, "Invalid level should raise ValueError")
except ValueError:
    check("X03", True, "")

# ============================================================
# 6. EDGE CASES & ROBUSTNESS
# ============================================================
section("EDGE CASES & ROBUSTNESS")

# Single Tamil character at each level
for level in ["word", "character", "morpheme"]:
    try:
        result = tok.tokenize("அ", level=level)
        check(f"E01_{level}", len(result) >= 1, f"Single char at {level}: {result}")
    except Exception as e:
        check(f"E01_{level}", False, f"Single char crashed at {level}: {e}")

# Only punctuation
e2 = tok.word_tokenize("...")
check("E02", len(e2) == 3, f"'...' should give 3 punct tokens, got {len(e2)}: {[t.text for t in e2]}")

# Only numbers
e3 = tok.word_tokenize("12345")
check("E03", e3[0].token_type == TokenType.NUMBER, f"Number-only type: {e3[0].token_type}")

# Very long word (stress)
long_word = "செய்" * 50
try:
    result = tok.character_tokenize(long_word)
    check("E04", len(result) > 0, "Long word char tokenize should not crash")
except Exception as e:
    check("E04", False, f"Long word crashed: {e}")

# Unicode edge: ZWNJ / ZWJ characters
try:
    result = tok.word_tokenize("தமிழ்\u200cநாடு")
    check("E05", len(result) >= 1, f"ZWNJ handling: {[t.text for t in result]}")
except Exception as e:
    check("E05", False, f"ZWNJ crashed: {e}")

# Repeated punctuation
try:
    result = tok.word_tokenize("!!!")
    check("E06", len(result) == 3, f"'!!!' should be 3 tokens: {[t.text for t in result]}")
except Exception as e:
    check("E06", False, f"Repeated punct crashed: {e}")

# Mixed script (Tamil + numerals + English)
try:
    result = tok.word_tokenize("2024 ஆம் year")
    check("E07", len(result) >= 3, f"Mixed script: {[t.text for t in result]}")
except Exception as e:
    check("E07", False, f"Mixed script crashed: {e}")

# Sentence with only spaces between sentences
s_e8 = tok.sentence_tokenize("ஒன்று.இரண்டு.")
check("E08", len(s_e8) == 2, f"No-space sentences: {len(s_e8)}: {[t.text for t in s_e8]}")

# ============================================================
# 7. DIVERSE REAL-WORLD SENTENCES
# ============================================================
section("DIVERSE REAL-WORLD SENTENCES (no-crash)")

diverse = [
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
    "திருவள்ளுவர் எழுதிய திருக்குறள் 1330 குறள்களை கொண்டது.",
    "சிலப்பதிகாரம் தமிழின் ஐம்பெருங்காப்பியங்களில் ஒன்று.",
    "நான் என் நண்பர்களுடன் கடற்கரைக்கு சென்றேன்.",
    "அவள் தினமும் காலையில் ஓடுவாள்.",
    "இந்திய அரசியலமைப்புச் சட்டம் 1950 ஆம் ஆண்டு நடைமுறைக்கு வந்தது.",
]

for i, sent in enumerate(diverse):
    for level in ["sentence", "word", "character", "morpheme"]:
        try:
            result = tok.tokenize(sent, level=level)
            check(f"D{i:02d}_{level}", len(result) >= 1,
                  f"'{sent[:30]}...' at {level}: got 0 tokens")
        except Exception as e:
            check(f"D{i:02d}_{level}", False,
                  f"'{sent[:30]}...' CRASHED at {level}: {e}")

# ============================================================
# REPORT
# ============================================================
section("FINAL REPORT")
print(f"\n  Total checks: {PASS + FAIL}")
print(f"  PASSED: {PASS}")
print(f"  FAILED: {FAIL}")

if FLAWS:
    print(f"\n  === FLAWS FOUND ({len(FLAWS)}) ===")
    for f in FLAWS:
        print(f"    {f}")
else:
    print("\n  All checks passed!")

sys.exit(1 if FAIL > 0 else 0)
