"""
Raw output dump for visual inspection + strict accuracy checks.
Prints every morpheme result so we can spot incorrect decompositions.
"""

import sys
from tamil_tokenizer import TamilTokenizer, TokenType

tok = TamilTokenizer()
PASS = 0
FAIL = 0
FLAWS = []

def report(test_id, word, tokens, expect_root=None, expect_suffix=None,
           expect_nodecomp=False, desc=""):
    global PASS, FAIL
    types_str = " + ".join(f"[{t.token_type.value}]'{t.text}'" for t in tokens)
    root = next((t.text for t in tokens if t.token_type == TokenType.ROOT), None)
    sfx_parts = [t.text for t in tokens if t.token_type in (
        TokenType.CASE_SUFFIX, TokenType.SUFFIX,
        TokenType.TENSE_MARKER, TokenType.PERSON_MARKER, TokenType.PLURAL_MARKER)]
    sfx = "".join(sfx_parts) if sfx_parts else None

    status = "OK"
    err = None

    if expect_nodecomp:
        if len(tokens) != 1 or tokens[0].token_type != TokenType.ROOT:
            status = "FAIL"
            err = f"should NOT decompose but got: {types_str}"
    elif expect_root is not None and root != expect_root:
        status = "FAIL"
        err = f"root '{root}' != expected '{expect_root}'"
    elif expect_suffix is not None and sfx != expect_suffix:
        status = "FAIL"
        err = f"suffix '{sfx}' != expected '{expect_suffix}'"

    icon = "✓" if status == "OK" else "✗"
    print(f"  {icon} [{test_id:6s}] {word:20s} → {types_str}")
    if err:
        print(f"           *** {err}")
        FAIL += 1
        FLAWS.append(f"[{test_id}] {word} ({desc}): {err}")
    else:
        PASS += 1

def m(w): return tok.morpheme_tokenize(w)

print("=" * 80)
print("  MORPHEME ACCURACY DUMP")
print("=" * 80)

# ── A. Exact case suffix assertions ───────────────────────────
print("\n─── Case Suffixes (exact) ───")

report("A01", "மரத்தை",       m("மரத்தை"),       expect_root="மரத்த", expect_suffix="ஐ",    desc="acc_ai")
report("A02", "பள்ளியை",     m("பள்ளியை"),     expect_root="பள்ளிய", expect_suffix="ஐ",    desc="acc_school")
report("A03", "நண்பனோடு",   m("நண்பனோடு"),   expect_root="நண்பன", expect_suffix="ஓடு",  desc="soc_odu")
report("A04", "பள்ளிக்கு",   m("பள்ளிக்கு"),   expect_root="பள்ளிக்", expect_suffix="கு",   desc="dat_kku")
report("A05", "மரத்தின்",     m("மரத்தின்"),     expect_root="மரத்த", expect_suffix="இன்",  desc="abl_in")
report("A06", "சென்னையை",   m("சென்னையை"),   expect_root="சென்னைய", expect_suffix="ஐ",  desc="acc_chennai")
report("A07", "உணவுக்காக",   m("உணவுக்காக"),   expect_root="உணவு", expect_suffix="க்காக",desc="dat_pp")
report("A08", "வீட்டுக்காக",   m("வீட்டுக்காக"),   desc="compound_veettu")
report("A09", "இந்தியாவின்",  m("இந்தியாவின்"),  desc="abl_india")
report("A10", "தோழியோடு",   m("தோழியோடு"),   desc="soc_friend")

# ── B. Postpositions ──────────────────────────────────────────
print("\n─── Postpositions ───")

report("B01", "மேசையின்மேல்",   m("மேசையின்மேல்"),   desc="on_table")
report("B02", "ஊரிலிருந்து",      m("ஊரிலிருந்து"),      desc="from_town")
report("B03", "அவர்களுக்காக",    m("அவர்களுக்காக"),    desc="for_them")
report("B04", "படிப்புக்காக",      m("படிப்புக்காக"),      desc="for_study")
report("B05", "பணத்துக்காக",     m("பணத்துக்காக"),     desc="for_money")

# ── C. Verbs ──────────────────────────────────────────────────
print("\n─── Verb forms (inspect decomposition) ───")

report("C01", "வந்தான்",       m("வந்தான்"),       desc="past_he_came")
report("C02", "வந்தாள்",       m("வந்தாள்"),       desc="past_she_came")
report("C03", "வந்தார்கள்",    m("வந்தார்கள்"),    desc="past_they_came")
report("C04", "சென்றான்",      m("சென்றான்"),      desc="past_he_went")
report("C05", "சென்றாள்",      m("சென்றாள்"),      desc="past_she_went")
report("C06", "படித்தேன்",      m("படித்தேன்"),      desc="past_i_read")
report("C07", "படிக்கிறேன்",   m("படிக்கிறேன்"),   desc="pres_i_read")
report("C08", "போகிறான்",      m("போகிறான்"),      desc="pres_he_goes")
report("C09", "வருகிறாள்",     m("வருகிறாள்"),     desc="pres_she_comes")
report("C10", "படிப்பான்",      m("படிப்பான்"),      desc="fut_he_reads")
report("C11", "வருவாள்",       m("வருவாள்"),       desc="fut_she_comes")
report("C12", "செல்வார்கள்",   m("செல்வார்கள்"),   desc="fut_they_go")
report("C13", "வரமாட்டான்",    m("வரமாட்டான்"),    desc="neg_he_wont_come")
report("C14", "எழுதினான்",     m("எழுதினான்"),     desc="past_he_wrote")
report("C15", "பேசுகிறார்",     m("பேசுகிறார்"),     desc="pres_he_speaks_hon")

# ── D. No-decomposition words (strict) ────────────────────────
print("\n─── No-decomposition (strict) ───")

no_decomp = [
    ("தமிழ்", "lang"), ("நன்றி", "thanks"), ("வணக்கம்", "greeting"),
    ("அவன்", "he"), ("அவள்", "she"), ("நான்", "i"), ("நீ", "you"),
    ("பெரிய", "big"), ("சிறிய", "small"), ("நல்ல", "good"),
    ("ஒன்று", "one"), ("இரண்டு", "two"), ("மூன்று", "three"),
    ("வா", "come_imp"), ("போ", "go_imp"),
]
for word, desc in no_decomp:
    report(f"D_{desc:8s}", word, m(word), expect_nodecomp=True, desc=desc)

# ── E. Plural forms ───────────────────────────────────────────
print("\n─── Plural forms ───")

report("E01", "மாணவர்கள்",     m("மாணவர்கள்"),     desc="students")
report("E02", "புத்தகங்கள்",    m("புத்தகங்கள்"),    desc="books")
report("E03", "குழந்தைகள்",    m("குழந்தைகள்"),    desc="children")
report("E04", "நாடுகள்",        m("நாடுகள்"),        desc="countries")
report("E05", "வீடுகள்",        m("வீடுகள்"),        desc="houses")

# ── F. Complex / long words ───────────────────────────────────
print("\n─── Complex words ───")

report("F01", "பள்ளிக்கூடத்தில்",  m("பள்ளிக்கூடத்தில்"),  desc="in_school")
report("F02", "மருத்துவமனையில்",   m("மருத்துவமனையில்"),   desc="in_hospital")
report("F03", "கடற்கரையில்",       m("கடற்கரையில்"),       desc="at_beach")
report("F04", "செய்தித்தாள்",       m("செய்தித்தாள்"),       desc="newspaper")
report("F05", "அரசியலமைப்பு",      m("அரசியலமைப்பு"),      desc="constitution")
report("F06", "தலைநகரம்",          m("தலைநகரம்"),          desc="capital")
report("F07", "பேருந்து",           m("பேருந்து"),           desc="bus")
report("F08", "விமானநிலையம்",      m("விமானநிலையம்"),      desc="airport")
report("F09", "சுற்றுச்சூழல்",      m("சுற்றுச்சூழல்"),      desc="environment")
report("F10", "தொலைக்காட்சி",      m("தொலைக்காட்சி"),      desc="television")

# ── G. Sentence-level morpheme ────────────────────────────────
print("\n─── Sentence pipeline ───")

sents = [
    "நான் பள்ளிக்கு சென்றேன்.",
    "உணவுக்காக காத்திருந்தான்.",
    "அவள் வீட்டுக்காக பாடுபட்டாள்.",
    "குழந்தைகள் விளையாடுகிறார்கள்.",
    "மழையால் வெள்ளம் வந்தது.",
]
for i, sent in enumerate(sents):
    tokens = tok.tokenize(sent, level="morpheme")
    parts = " | ".join(f"[{t.token_type.value}]'{t.text}'" for t in tokens)
    print(f"  G{i+1:02d}: {sent}")
    print(f"       → {parts}")

# ── H. Word tokenization accuracy ────────────────────────────
print("\n─── Word tokenization edge cases ───")

word_cases = [
    ("தமிழ்நாடு சென்னை", ["தமிழ்நாடு", "சென்னை"], "two_words"),
    ("1,234.56 ரூபாய்", ["1,234.56", "ரூபாய்"], "decimal_number"),
    ("\"வணக்கம்\"", ['"', "வணக்கம்", '"'], "quoted_word"),
    ("அ, ஆ, இ", ["அ", ",", "ஆ", ",", "இ"], "letters_with_commas"),
]
for text, expected, desc in word_cases:
    tokens = tok.word_tokenize(text)
    actual = [t.text for t in tokens]
    ok = actual == expected
    icon = "✓" if ok else "✗"
    print(f"  {icon} [W_{desc:20s}] '{text}' → {actual}")
    if ok:
        PASS += 1
    else:
        FAIL += 1
        FLAWS.append(f"[W_{desc}] expected {expected}, got {actual}")

# ── I. Character tokenization accuracy ────────────────────────
print("\n─── Character tokenization edge cases ───")

char_cases = [
    ("கொள்ளை", ["கொ", "ள்", "ளை"], "kollai"),
    ("பொருள்", ["பொ", "ரு", "ள்"], "porul"),
    ("கௌரவம்", ["கௌ", "ர", "வ", "ம்"], "kauravam"),
    ("ஸ்ரீ", ["ஸ்", "ரீ"], "sri"),
    ("க்ஷ", ["க்", "ஷ"], "ksha"),
]
for word, expected, desc in char_cases:
    tokens = tok.character_tokenize(word)
    actual = [t.text for t in tokens]
    ok = actual == expected
    icon = "✓" if ok else "✗"
    print(f"  {icon} [C_{desc:12s}] '{word}' → {actual}")
    if not ok:
        print(f"           expected: {expected}")
    if ok:
        PASS += 1
    else:
        FAIL += 1
        FLAWS.append(f"[C_{desc}] '{word}': expected {expected}, got {actual}")

# ── J. Sentence tokenization edge cases ───────────────────────
print("\n─── Sentence tokenization edge cases ───")

sent_cases = [
    ("ஒன்று.இரண்டு.", 2, "no_space_between"),
    ("அவன் வந்தான்... பின் சென்றான்.", None, "ellipsis"),
    ("என்ன? ஏன்? எப்போது? எங்கே?", 4, "four_questions"),
    ("விலை ₹3.50 ஆகும்.", 1, "currency_decimal"),
    ("", 0, "empty"),
    ("   ", 0, "whitespace"),
    ("வா", 1, "single_word_no_punct"),
]
for text, expected_count, desc in sent_cases:
    tokens = tok.sentence_tokenize(text)
    actual = len(tokens)
    if expected_count is not None:
        ok = actual == expected_count
        icon = "✓" if ok else "✗"
        print(f"  {icon} [S_{desc:22s}] '{text[:40]}' → {actual} sentences")
        if not ok:
            print(f"           expected {expected_count}, texts: {[t.text for t in tokens]}")
            FAIL += 1
            FLAWS.append(f"[S_{desc}] expected {expected_count} sentences, got {actual}: {[t.text for t in tokens]}")
        else:
            PASS += 1
    else:
        print(f"  ? [S_{desc:22s}] '{text[:40]}' → {actual} sentences: {[t.text for t in tokens]}")

# ================================================================
# FINAL REPORT
# ================================================================
print("\n" + "=" * 80)
print(f"  Total checks: {PASS + FAIL}")
print(f"  PASSED: {PASS}")
print(f"  FAILED: {FAIL}")

if FLAWS:
    print(f"\n  ╔══ FLAWS FOUND ({len(FLAWS)}) ══╗")
    for i, f in enumerate(FLAWS, 1):
        print(f"  ║ {i}. {f}")
    print(f"  ╚{'═' * 40}╝")
else:
    print("\n  ★ All checks passed!")

sys.exit(1 if FAIL > 0 else 0)
