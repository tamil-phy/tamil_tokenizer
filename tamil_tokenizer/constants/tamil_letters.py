"""
Tamil Unicode Constants - Equivalent to TamilConstants.java

This module contains all Tamil Unicode character constants, letter classifications,
and pattern arrays used throughout the NLP system.

Author: Tamil Arasan
Since: May 2, 2017
"""

from typing import List, Dict
import re


class TamilConstants:
    """
    Tamil language constants including Unicode values for all Tamil characters,
    letter classifications (வல்லினம், மெல்லினம், இடையினம்), and grammatical patterns.
    """

    # ==================== Independent Vowels (உயிரெழுத்து) ====================
    UYIR_EZHUTHU: List[int] = [
        0x0B85,  # அ TAMIL LETTER A
        0x0B86,  # ஆ TAMIL LETTER AA
        0x0B87,  # இ TAMIL LETTER I
        0x0B88,  # ஈ TAMIL LETTER II
        0x0B89,  # உ TAMIL LETTER U
        0x0B8A,  # ஊ TAMIL LETTER UU
        0x0B8E,  # எ TAMIL LETTER E
        0x0B8F,  # ஏ TAMIL LETTER EE
        0x0B90,  # ஐ TAMIL LETTER AI
        0x0B92,  # ஒ TAMIL LETTER O
        0x0B93,  # ஓ TAMIL LETTER OO
        0x0B94,  # ஔ TAMIL LETTER AU
        0x0B83,  # ஃ TAMIL SIGN VISARGA
    ]

    # ==================== Consonants (உயிர்மெய்யெழுத்து) ====================
    UYIRMEY_EZHUTHU: List[int] = [
        0x0B95,  # க TAMIL LETTER KA
        0x0B99,  # ங TAMIL LETTER NGA
        0x0B9A,  # ச TAMIL LETTER CA
        0x0B9C,  # ஜ TAMIL LETTER JA
        0x0B9E,  # ஞ TAMIL LETTER NYA
        0x0B9F,  # ட TAMIL LETTER TTA
        0x0BA3,  # ண TAMIL LETTER NNA
        0x0BA4,  # த TAMIL LETTER TA
        0x0BA8,  # ந TAMIL LETTER NA
        0x0BA9,  # ன TAMIL LETTER NNNA
        0x0BAA,  # ப TAMIL LETTER PA
        0x0BAE,  # ம TAMIL LETTER MA
        0x0BAF,  # ய TAMIL LETTER YA
        0x0BB0,  # ர TAMIL LETTER RA
        0x0BB1,  # ற TAMIL LETTER RRA
        0x0BB2,  # ல TAMIL LETTER LA
        0x0BB3,  # ள TAMIL LETTER LLA
        0x0BB4,  # ழ TAMIL LETTER LLLA
        0x0BB5,  # வ TAMIL LETTER VA
        0x0BB6,  # ஶ TAMIL LETTER SHA
        0x0BB7,  # ஷ TAMIL LETTER SSA
        0x0BB8,  # ஸ TAMIL LETTER SA
        0x0BB9,  # ஹ TAMIL LETTER HA
    ]

    # ==================== Pure Consonants (மெய்யெழுத்து) ====================
    MEY_EZHUTHU: List[str] = [
        "\u0B95\u0BCD",  # க் TAMIL LETTER KA
        "\u0B99\u0BCD",  # ங் TAMIL LETTER NGA
        "\u0B9A\u0BCD",  # ச் TAMIL LETTER CA
        "\u0B9C\u0BCD",  # ஜ் TAMIL LETTER JA
        "\u0B9E\u0BCD",  # ஞ் TAMIL LETTER NYA
        "\u0B9F\u0BCD",  # ட் TAMIL LETTER TTA
        "\u0BA3\u0BCD",  # ண் TAMIL LETTER NNA
        "\u0BA4\u0BCD",  # த் TAMIL LETTER TA
        "\u0BA8\u0BCD",  # ந் TAMIL LETTER NA
        "\u0BA9\u0BCD",  # ன் TAMIL LETTER NNNA
        "\u0BAA\u0BCD",  # ப் TAMIL LETTER PA
        "\u0BAE\u0BCD",  # ம் TAMIL LETTER MA
        "\u0BAF\u0BCD",  # ய் TAMIL LETTER YA
        "\u0BB0\u0BCD",  # ர் TAMIL LETTER RA
        "\u0BB1\u0BCD",  # ற் TAMIL LETTER RRA
        "\u0BB2\u0BCD",  # ல் TAMIL LETTER LA
        "\u0BB3\u0BCD",  # ள் TAMIL LETTER LLA
        "\u0BB4\u0BCD",  # ழ் TAMIL LETTER LLLA
        "\u0BB5\u0BCD",  # வ் TAMIL LETTER VA
        "\u0BB6\u0BCD",  # ஶ் TAMIL LETTER SHA
        "\u0BB7\u0BCD",  # ஷ் TAMIL LETTER SSA
        "\u0BB8\u0BCD",  # ஸ் TAMIL LETTER SA
        "\u0BB9\u0BCD",  # ஹ் TAMIL LETTER HA
    ]

    # ==================== Individual Vowel Constants ====================
    அ = 0x0B85
    ஆ = 0x0B86
    இ = 0x0B87
    ஈ = 0x0B88
    உ = 0x0B89
    ஊ = 0x0B8A
    எ = 0x0B8E
    ஏ = 0x0B8F
    ஐ = 0x0B90
    ஒ = 0x0B92
    ஓ = 0x0B93
    ஔ = 0x0B94
    ஃ = 0x0B83

    # ==================== Vowel Signs (Dependent Vowels) ====================
    ஆ_EXT = 0x0BBE  # ா TAMIL VOWEL SIGN AA
    இ_EXT = 0x0BBF  # ி TAMIL VOWEL SIGN I
    ஈ_EXT = 0x0BC0  # ீ TAMIL VOWEL SIGN II
    உ_EXT = 0x0BC1  # ு TAMIL VOWEL SIGN U
    ஊ_EXT = 0x0BC2  # ூ TAMIL VOWEL SIGN UU
    எ_EXT = 0x0BC6  # ெ TAMIL VOWEL SIGN E
    ஏ_EXT = 0x0BC7  # ே TAMIL VOWEL SIGN EE
    ஐ_EXT = 0x0BC8  # ை TAMIL VOWEL SIGN AI
    ஒ_EXT = 0x0BCA  # ொ TAMIL VOWEL SIGN O
    ஓ_EXT = 0x0BCB  # ோ TAMIL VOWEL SIGN OO
    ஔ_EXT = 0x0BCC  # ௌ TAMIL VOWEL SIGN AU
    ஃ_EXT = 0x0BCD  # ் TAMIL SIGN VIRAMA (pulli)

    # ==================== Individual Consonant Constants ====================
    க = 0x0B95
    ங = 0x0B99
    ச = 0x0B9A
    ஜ = 0x0B9C
    ஞ = 0x0B9E
    ட = 0x0B9F
    ண = 0x0BA3
    த = 0x0BA4
    ந = 0x0BA8
    ன = 0x0BA9
    ப = 0x0BAA
    ம = 0x0BAE
    ய = 0x0BAF
    ர = 0x0BB0
    ற = 0x0BB1
    ல = 0x0BB2
    ள = 0x0BB3
    ழ = 0x0BB4
    வ = 0x0BB5
    ஶ = 0x0BB6
    ஷ = 0x0BB7
    ஸ = 0x0BB8
    ஹ = 0x0BB9

    # ==================== Pure Consonant String Constants ====================
    க் = "\u0B95\u0BCD"
    ங் = "\u0B99\u0BCD"
    ச் = "\u0B9A\u0BCD"
    ஜ் = "\u0B9C\u0BCD"
    ஞ் = "\u0B9E\u0BCD"
    ட் = "\u0B9F\u0BCD"
    ண் = "\u0BA3\u0BCD"
    த் = "\u0BA4\u0BCD"
    ந் = "\u0BA8\u0BCD"
    ன் = "\u0BA9\u0BCD"
    ப் = "\u0BAA\u0BCD"
    ம் = "\u0BAE\u0BCD"
    ய் = "\u0BAF\u0BCD"
    ர் = "\u0BB0\u0BCD"
    ற் = "\u0BB1\u0BCD"
    ல் = "\u0BB2\u0BCD"
    ள் = "\u0BB3\u0BCD"
    ழ் = "\u0BB4\u0BCD"
    வ் = "\u0BB5\u0BCD"
    ஶ் = "\u0BB6\u0BCD"
    ஷ் = "\u0BB7\u0BCD"
    ஸ் = "\u0BB8\u0BCD"
    ஹ் = "\u0BB9\u0BCD"

    # ==================== Dependent Vowels Array ====================
    D_VOWELS: List[int] = [
        0x0BBE,  # ா TAMIL VOWEL SIGN AA
        0x0BBF,  # ி TAMIL VOWEL SIGN I
        0x0BC0,  # ீ TAMIL VOWEL SIGN II
        0x0BC1,  # ு TAMIL VOWEL SIGN U
        0x0BC2,  # ூ TAMIL VOWEL SIGN UU
        0x0BC6,  # ெ TAMIL VOWEL SIGN E
        0x0BC7,  # ே TAMIL VOWEL SIGN EE
        0x0BC8,  # ை TAMIL VOWEL SIGN AI
        0x0BCA,  # ொ TAMIL VOWEL SIGN O
        0x0BCB,  # ோ TAMIL VOWEL SIGN OO
        0x0BCC,  # ௌ TAMIL VOWEL SIGN AU
        0x0BCD,  # ் TAMIL SIGN VIRAMA
    ]

    # Single part dependent vowels
    D1_VOWELS: List[int] = [
        0x0BBE,  # ா
        0x0BBF,  # ி
        0x0BC0,  # ீ
        0x0BC1,  # ு
        0x0BC2,  # ூ
        0x0BC6,  # ெ
        0x0BC7,  # ே
        0x0BC8,  # ை
        0x0BCD,  # ்
    ]

    # Two part dependent vowels
    D2_VOWELS: List[int] = [
        0x0BCA,  # ொ (0BC6 + 0BBE)
        0x0BCB,  # ோ (0BC7 + 0BBE)
        0x0BCC,  # ௌ (0BC6 + 0BD7)
    ]

    # ==================== All Extension Characters ====================
    ALL_EXT: List[int] = [
        0x0BBE, 0x0BBF, 0x0BC0, 0x0BC1, 0x0BC2, 0x0BC6,
        0x0BC7, 0x0BC8, 0x0BCA, 0x0BCB, 0x0BCC, 0x0BCD
    ]

    # ==================== Letter Classifications ====================
    # வல்லினம் மெய் (Hard consonants)
    VALLINAM_MEY: List[str] = [க், ச், ட், த், ப், ற்]

    # மெல்லினம் மெய் (Soft consonants)
    MELLINAM_MEY: List[str] = [ங், ஞ், ண், ந், ம், ன்]

    # இடையினம் மெய் (Medium consonants)
    IDAIYINAM_MEY: List[str] = [ய், ர், ல், வ், ழ், ள்]

    # வல்லினம் (Hard consonant bases)
    VALLINAM: List[int] = [க, ச, ட, த, ப, ற]

    # மெல்லினம் (Soft consonant bases)
    MELLINAM: List[int] = [ங, ஞ, ண, ந, ம, ன]

    # இடையினம் (Medium consonant bases)
    IDAIYINAM: List[int] = [ய, ர, ல, வ, ழ, ள]

    # ==================== Vowel Classifications ====================
    # குற்றெழுத்து (Short vowels)
    KUTR_EZHUTHU: List[int] = [அ, இ, உ, எ, ஒ]

    # நெட்டெழுத்து (Long vowels)
    NETT_EZHUTHU: List[int] = [ஆ, ஈ, ஊ, ஐ, ஏ, ஓ, ஔ]

    # சுட்டெழுத்து (Demonstrative letters)
    SUTT_EZHUTHU: List[int] = [அ, இ, உ]

    # ==================== Word Ending Patterns ====================
    # ஒற்று மெய்யெழுத்து முடிகிறதா
    OTRU_MEY_EZHUTHU_MUDIKIRATHA: List[str] = [க், ச், த், ப், ந், ய்]

    # வல்லினம் மெய்யெழுத்து முடிகிறதா
    VALLINAM_MEY_EZHUTHU_MUDIKIRATHA: List[str] = [க், ச், ட், த், ப், ற்]

    # வல்லினம் மெய்யெழுத்து வ் to ற் முடிகிறதா
    VALLINAM_MEY_EZHUTHU_V_TO_RR_MUDIKIRATHA: List[str] = [க், ச், ட், த், ப், வ், ற்]
    VALLINAM_MEY_V_TO_RR: List[str] = [க், ச், ட், த், ப், வ், ற்]  # Alias

    # கடை மெய்யெழுத்து (Word-ending consonants)
    KADAI_MEY_EZHUTHU: List[str] = [ஞ், ண், ந், ம், ன், ய், ர், ல், வ், ழ், ள்]

    # மெய்யெழுத்தில் முடிகிறதா (All pure consonants for word ending check)
    MEY_EZHUTHU_MUDIKIRATHA: List[str] = [
        க், ங், ச், ஜ், ஞ், ட், ண், த், ந், ன், ப், ம், ய், ர், ற், ல், ள், ழ், வ், ஶ், ஷ், ஸ், ஹ்
    ]

    # உயிரெழுத்தில் முடிகிறதா
    UYIR_EZHUTHU_MUDIKIRATHA: List[int] = [அ, ஆ, இ, ஈ, உ, ஊ, எ, ஏ, ஐ, ஒ, ஓ, ஔ]

    # கடையெழுத்தில் முடியாது
    KADAI_EZHUTHIL_MUDIYATHU: List[int] = [அ, ஆ, இ, ஈ, உ, ஊ, எ, ஏ, ஐ, ஒ, ஓ, ஔ, எ_EXT]

    # ==================== First Letter Patterns ====================
    MUDHAL_EZHUTHU: List[int] = [
        அ, ஆ, இ, ஈ, உ, ஊ, எ, ஏ, ஐ, ஒ, ஓ, ஔ,
        க, ச, ஞ, த, ந, ப, ம, ய, வ, ஜ, ஷ, ஸ, ஹ
    ]

    # ==================== Tense Markers ====================
    # இறந்தகால உறுபுபா (Past tense markers)
    IRANTHA_KALA_URUPUPA: List[str] = [ந் + த், த் + த்]

    # ==================== Question Letters ====================
    # வினாயெழுத்து
    VINA_EZHUTHU: List[str] = [chr(ஆ), "\u0BAF\u0BBE", chr(ஓ), chr(எ), chr(ஏ)]  # யா

    # முன் வினாயெழுத்து
    MUN_VINA_EZHUTHU: List[str] = ["\u0BAF\u0BBE", chr(எ), chr(ஏ)]  # யா

    # கடை வினாயெழுத்து
    KADAI_VINA_EZHUTHU: List[int] = [0x0BCB, 0x0BBE]

    # முன் எழுத்து
    MUN_EZHUTHU: List[int] = [க, ச, த, ப, ங, ஞ, ந, ம, ய, வ]

    # ==================== Sandhi Patterns ====================
    # ய நிலை மொழியின் ஈறு
    YA_NILAI_MOZHIYIN_IRU: List[int] = [இ, ஈ, ஐ, ஓ]

    # வ நிலை மொழியின் ஈறு
    VA_NILAI_MOZHIYIN_IRU: List[int] = [அ, ஆ, உ, ஊ, எ, ஏ, ஒ, ஔ]

    # ==================== Consonant Clusters ====================
    # இனவெழுத்து
    INA_EZHUTHU: List[str] = ["ங்க", "ஞ்ச", "ண்ட", "ந்த", "ம்ப", "ன்ற"]

    # உடனிலை மெய்ம்மயக்கம்
    UDAN_NILAI_MEY_MAYAKKAM: List[str] = [
        "க்க்", "ங்ங்", "ச்ச்", "ஞ்ஞ்", "ட்ட்", "ண்ண்",
        "த்த்", "ந்ந்", "ப்ப்", "ம்ம்", "ய்ய்", "ல்ல்",
        "வ்வ்", "ள்ள்", "ற்ற்", "ன்ன்"
    ]

    # ==================== Suffix Pattern Strings ====================
    யா = "\u0BAF\u0BBE"

    # Ending patterns (used in suffix matching)
    இருந்து = "ிருந்து"
    நின்று = "ின்று"
    இடம் = "ிடம்"
    உடன் = "ுடன்"

    த்த்தில்முடிகிறதா = "த்த்"
    ந்த்தில்முடிகிறதா = "ந்த்"
    ற்வில்முடிகிறதா = "ற்"
    உவில்முடிகிறதா = "உ"
    அதுவில்முடிகிறதா = "அத்உ"
    அன்வில்முடிகிறதா = "அன்"
    அர்ரில்முடிகிறதா = "அர்"
    அள்லில்முடிகிறதா = "அள்"
    க்அள்லில்முடிகிறதா = "க்அள்"
    என்ற்உல்முடிகிறதா = "என்ற்உ"
    ஆக்இற்வில்முடிகிறதா = "ஆக்இற்"
    இன்லில்முடிகிறதா = "இன்"
    ய்லில்முடிகிறதா = "ய்"
    இய்லில்முடிகிறதா = "இய்"
    இல்முடிகிறதா = "இல்"
    ஆல்லில்முடிகிறதா = "ஆல்"
    அல்லில்முடிகிறதா = "அல்"
    ஒல்இலில்முடிகிறதா = "ஒல்இ"
    க்இலில்முடிகிறதா = "க்இ"
    வ்இலில்முடிகிறதா = "வ்இ"
    இவில்முடிகிறதா = "இ"
    உம்மில்முடிகிறதா = "உம்"
    உல்லில்முடிகிறதா = "உல்"
    இர்உந்த்உமுடிகிறதா = "இர்உந்த்உ"
    த்ஆன்முடிகிறதா = "த்ஆன்"

    # ==================== Character Series (வரிசை) ====================
    # க வரிசை
    KA_VARISAI: List[str] = ["க்", "க", "கா", "கி", "கீ", "கு", "கூ", "கெ", "கே", "கை", "கொ", "கோ", "கௌ"]

    # ச வரிசை
    CA_VARISAI: List[str] = ["ச்", "ச", "சா", "சி", "சீ", "சு", "சூ", "செ", "சே", "சை", "சொ", "சோ", "சௌ"]

    # ட வரிசை
    TA_VARISAI: List[str] = ["ட்", "ட", "டா", "டி", "டீ", "டு", "டூ", "டெ", "டே", "டை", "டொ", "டோ", "டௌ"]

    # த வரிசை
    THA_VARISAI: List[str] = ["த்", "த", "தா", "தி", "தீ", "து", "தூ", "தெ", "தே", "தை", "தொ", "தோ", "தௌ"]

    # ப வரிசை
    PA_VARISAI: List[str] = ["ப்", "ப", "பா", "பி", "பீ", "பு", "பூ", "பெ", "பே", "பை", "பொ", "போ", "பௌ"]

    # ற வரிசை
    RA_VARISAI: List[str] = ["ற்", "ற", "றா", "றி", "றீ", "று", "றூ", "றெ", "றே", "றை", "றொ", "றோ", "றௌ"]

    # ய வரிசை
    YA_VARISAI: List[str] = ["ய்", "ய", "யா", "யி", "யீ", "யு", "யூ", "யெ", "யே", "யை", "யொ", "யோ", "யௌ"]

    # ர வரிசை
    RA2_VARISAI: List[str] = ["ர்", "ர", "ரா", "ரி", "ரீ", "ரு", "ரூ", "ரெ", "ரே", "ரை", "ரொ", "ரோ", "ரௌ"]

    # ல வரிசை
    LA_VARISAI: List[str] = ["ல்", "ல", "லா", "லி", "லீ", "லு", "லூ", "லெ", "லே", "லை", "லொ", "லோ", "லௌ"]

    # வ வரிசை
    VA_VARISAI: List[str] = ["வ்", "வ", "வா", "வி", "வீ", "வு", "வூ", "வெ", "வே", "வை", "வொ", "வோ", "வௌ"]

    # ழ வரிசை
    ZHA_VARISAI: List[str] = ["ழ்", "ழ", "ழா", "ழி", "ழீ", "ழு", "ழூ", "ழெ", "ழே", "ழை", "ழொ", "ழோ", "ழௌ"]

    # ள வரிசை
    LA2_VARISAI: List[str] = ["ள்", "ள", "ளா", "ளி", "ளீ", "ளு", "ளூ", "ளெ", "ளே", "ளை", "ளொ", "ளோ", "ளௌ"]

    # ங வரிசை
    NGA_VARISAI: List[str] = ["ங்", "ங", "ஙா", "ஙி", "ஙீ", "ஙு", "ஙூ", "ஙெ", "ஙே", "ஙை", "ஙொ", "ஙோ", "ஙௌ"]

    # ஞ வரிசை
    NYA_VARISAI: List[str] = ["ஞ்", "ஞ", "ஞா", "ஞி", "ஞீ", "ஞு", "ஞூ", "ஞெ", "ஞே", "ஞை", "ஞொ", "ஞொ", "ஞௌ"]

    # ண வரிசை
    NA_VARISAI: List[str] = ["ண்", "ண", "ணா", "ணி", "ணீ", "ணு", "ணூ", "ணெ", "ணே", "ணை", "ணொ", "ணோ", "ணௌ"]

    # ந வரிசை
    NDA_VARISAI: List[str] = ["ந்", "ந", "நா", "நி", "நீ", "நு", "நூ", "நெ", "நே", "நை", "நொ", "நௌ", "நௌ"]

    # ம வரிசை
    MA_VARISAI: List[str] = ["ம்", "ம", "மா", "மி", "மீ", "மு", "மூ", "மெ", "மே", "மை", "மொ", "மோ", "மௌ"]

    # ன வரிசை
    NA2_VARISAI: List[str] = ["ன்", "ன", "னா", "னி", "னீ", "னு", "னூ", "னெ", "னே", "னை", "னொ", "னோ", "னௌ"]

    @classmethod
    def get_vallinam_varisai(cls) -> List[str]:
        """Get all வல்லின வரிசை characters"""
        result = []
        result.extend(cls.KA_VARISAI)
        result.extend(cls.CA_VARISAI)
        result.extend(cls.TA_VARISAI)
        result.extend(cls.THA_VARISAI)
        result.extend(cls.PA_VARISAI)
        result.extend(cls.RA_VARISAI)
        return result

    @classmethod
    def get_idaiyinam_varisai(cls) -> List[str]:
        """Get all இடையின வரிசை characters"""
        result = []
        result.extend(cls.YA_VARISAI)
        result.extend(cls.RA2_VARISAI)
        result.extend(cls.LA_VARISAI)
        result.extend(cls.VA_VARISAI)
        result.extend(cls.ZHA_VARISAI)
        result.extend(cls.LA2_VARISAI)
        return result

    @classmethod
    def get_mellinam_varisai(cls) -> List[str]:
        """Get all மெல்லின வரிசை characters"""
        result = []
        result.extend(cls.NGA_VARISAI)
        result.extend(cls.NYA_VARISAI)
        result.extend(cls.NA_VARISAI)
        result.extend(cls.NDA_VARISAI)
        result.extend(cls.MA_VARISAI)
        result.extend(cls.NA2_VARISAI)
        return result
