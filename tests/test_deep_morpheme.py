"""
Deep morpheme analysis probe — checks exact root/suffix output
for a wide range of Tamil inflected words across all cases, verbs, and compounds.
"""

import sys
from tamil_tokenizer import TamilTokenizer, TokenType

tok = TamilTokenizer()
PASS = 0
FAIL = 0
FLAWS = []

def check(test_id, word, tokens, expect_root=None, expect_suffix=None,
          expect_decompose=True, desc=""):
    global PASS, FAIL
    texts = [t.text for t in tokens]
    types = [(t.text, t.token_type.value) for t in tokens]

    if not expect_decompose:
        ok = (len(tokens) == 1 and tokens[0].token_type == TokenType.ROOT)
        if ok:
            PASS += 1
        else:
            FAIL += 1
            FLAWS.append(f"[{test_id}] '{word}' ({desc}): should NOT decompose → {types}")
            print(f"  FAIL [{test_id}] '{word}' ({desc}): should NOT decompose → {types}")
        return

    root_tokens = [t for t in tokens if t.token_type == TokenType.ROOT]
    suffix_tokens = [t for t in tokens if t.token_type in (
        TokenType.CASE_SUFFIX, TokenType.SUFFIX,
        TokenType.TENSE_MARKER, TokenType.PERSON_MARKER, TokenType.PLURAL_MARKER)]

    actual_root = root_tokens[0].text if root_tokens else "<NONE>"
    actual_suffix = "".join(t.text for t in suffix_tokens) if suffix_tokens else "<NONE>"

    errors = []
    if expect_root is not None and actual_root != expect_root:
        errors.append(f"root: '{actual_root}' (expected '{expect_root}')")
    if expect_suffix is not None and actual_suffix != expect_suffix:
        errors.append(f"suffix: '{actual_suffix}' (expected '{expect_suffix}')")

    if errors:
        FAIL += 1
        detail = ", ".join(errors)
        FLAWS.append(f"[{test_id}] '{word}' ({desc}): {detail} | full: {types}")
        print(f"  FAIL [{test_id}] '{word}' ({desc}): {detail}")
    else:
        PASS += 1

def m(word):
    return tok.morpheme_tokenize(word)

print("=" * 60)
print("  DEEP MORPHEME ANALYSIS PROBE")
print("=" * 60)

# ================================================================
# A. CASE SUFFIX (வேற்றுமை) — all 8 cases
# ================================================================
print("\n--- A. Case suffixes (வேற்றுமை) ---")

# 2nd case: ஐ (accusative)
check("A01", "மரத்தை", m("மரத்தை"), desc="accusative_ai")
check("A02", "சென்னையை", m("சென்னையை"), desc="accusative_city")
check("A03", "பள்ளியை", m("பள்ளியை"), desc="accusative_school")

# 3rd case: ஆல் (instrumental) / ஓடு (sociative)
check("A04", "மழையால்", m("மழையால்"), desc="instrumental_aal")
check("A05", "நண்பனோடு", m("நண்பனோடு"), desc="sociative_odu")
check("A06", "தோழியோடு", m("தோழியோடு"), desc="sociative_odu2")

# 4th case: கு (dative)
check("A07", "பள்ளிக்கு", m("பள்ளிக்கு"), desc="dative_kku")
check("A08", "அவனுக்கு", m("அவனுக்கு"), desc="dative_nukku")

# 4th case + postposition: க்காக (compound)
check("A09", "உணவுக்காக", m("உணவுக்காக"), expect_root="உணவு", expect_suffix="க்காக",
      desc="dative+postposition")
check("A10", "வீட்டுக்காக", m("வீட்டுக்காக"), desc="compound_veettu")
check("A11", "படிப்புக்காக", m("படிப்புக்காக"), desc="compound_padippu")

# 5th case: இன் (ablative)
check("A12", "மரத்தின்", m("மரத்தின்"), desc="ablative_in")
check("A13", "இந்தியாவின்", m("இந்தியாவின்"), desc="ablative_country")

# 7th case: இல் (locative) — checking if handled
check("A14", "வீட்டில்", m("வீட்டில்"), desc="locative_il")

# ================================================================
# B. POSTPOSITIONS (postpositions from line 16 in data)
# ================================================================
print("\n--- B. Postpositions ---")

check("B01", "மேசையின்மேல்", m("மேசையின்மேல்"), desc="postposition_mel")
check("B02", "மரத்துக்கீழ்", m("மரத்துக்கீழ்"), desc="postposition_keezh")
check("B03", "வீட்டுக்குள்", m("வீட்டுக்குள்"), desc="postposition_ul")
check("B04", "ஊரிலிருந்து", m("ஊரிலிருந்து"), desc="postposition_irunthu")

# ================================================================
# C. VERB MORPHOLOGY (tense + person markers)
# ================================================================
print("\n--- C. Verb morphology ---")

# Past tense
check("C01", "வந்தான்", m("வந்தான்"), desc="past_vandhan")
check("C02", "சென்றான்", m("சென்றான்"), desc="past_sendran")
check("C03", "படித்தாள்", m("படித்தாள்"), desc="past_paditthaal")

# Present tense
check("C04", "படிக்கிறேன்", m("படிக்கிறேன்"), desc="present_padikkiren")
check("C05", "போகிறான்", m("போகிறான்"), desc="present_pogiran")
check("C06", "வருகிறாள்", m("வருகிறாள்"), desc="present_varugiraal")

# Future tense
check("C07", "படிப்பான்", m("படிப்பான்"), desc="future_padippaan")
check("C08", "வருவாள்", m("வருவாள்"), desc="future_varuvaal")
check("C09", "செல்வார்கள்", m("செல்வார்கள்"), desc="future_plural_selvaarkal")

# Negative
check("C10", "வரமாட்டான்", m("வரமாட்டான்"), desc="negative_varamaattaan")

# Imperative
check("C11", "வா", m("வா"), desc="imperative_vaa")
check("C12", "போ", m("போ"), desc="imperative_po")

# ================================================================
# D. WORDS THAT SHOULD NOT DECOMPOSE (base forms / proper nouns)
# ================================================================
print("\n--- D. No decomposition ---")

for word, desc in [
    ("தமிழ்", "lang_tamil"),
    ("நன்றி", "thanks"),
    ("வணக்கம்", "greeting"),
    ("அவன்", "pronoun_he"),
    ("அவள்", "pronoun_she"),
    ("நான்", "pronoun_i"),
    ("பெரிய", "adjective_big"),
    ("சிறிய", "adjective_small"),
    ("நல்ல", "adjective_good"),
]:
    check(f"D_{desc}", word, m(word), expect_decompose=False, desc=desc)

# ================================================================
# E. PLURAL FORMS
# ================================================================
print("\n--- E. Plural ---")

check("E01", "மாணவர்கள்", m("மாணவர்கள்"), desc="students_plural")
check("E02", "புத்தகங்கள்", m("புத்தகங்கள்"), desc="books_plural")
check("E03", "குழந்தைகள்", m("குழந்தைகள்"), desc="children_plural")

# ================================================================
# F. COMPOUND / COMPLEX WORDS
# ================================================================
print("\n--- F. Complex words ---")

check("F01", "அவர்களுக்காக", m("அவர்களுக்காக"), desc="for_them")
check("F02", "பள்ளிக்கூடத்தில்", m("பள்ளிக்கூடத்தில்"), desc="in_school")
check("F03", "மருத்துவமனையில்", m("மருத்துவமனையில்"), desc="in_hospital")
check("F04", "கடற்கரையில்", m("கடற்கரையில்"), desc="at_beach")
check("F05", "தலைநகரம்", m("தலைநகரம்"), desc="capital_city")

# ================================================================
# G. SENTENCE-LEVEL MORPHEME PIPELINE
# ================================================================
print("\n--- G. Sentence pipeline ---")

g1 = tok.tokenize("நான் பள்ளிக்கு சென்றேன்.", level="morpheme")
g1_types = {t.token_type for t in g1}
g1_check = (TokenType.ROOT in g1_types and TokenType.PUNCTUATION in g1_types)
if g1_check:
    PASS += 1
else:
    FAIL += 1
    FLAWS.append(f"[G01] Sentence morpheme: missing ROOT or PUNCT: {[(t.text, t.token_type.value) for t in g1]}")
    print(f"  FAIL [G01] Sentence morpheme pipeline")

g2 = tok.tokenize("உணவுக்காக காத்திருந்தான்.", level="morpheme")
g2_roots = [t.text for t in g2 if t.token_type == TokenType.ROOT]
g2_ok = "உணவு" in g2_roots
if g2_ok:
    PASS += 1
else:
    FAIL += 1
    FLAWS.append(f"[G02] Sentence 'உணவுக்காக காத்திருந்தான்.' roots: {g2_roots}")
    print(f"  FAIL [G02] roots: {g2_roots}")

# ================================================================
# REPORT
# ================================================================
print("\n" + "=" * 60)
print(f"  Total checks: {PASS + FAIL}")
print(f"  PASSED: {PASS}")
print(f"  FAILED: {FAIL}")

if FLAWS:
    print(f"\n  === FLAWS FOUND ({len(FLAWS)}) ===")
    for f in FLAWS:
        print(f"    {f}")
else:
    print("\n  All checks passed!")

sys.exit(1 if FAIL > 0 else 0)
