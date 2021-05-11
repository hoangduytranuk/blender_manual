from enum import Enum
import re

class SentStructModeRecord:
    def __init__(self, smode_txt=None, smode=None, extra_param=None):
        self.smode_txt: str = smode_txt
        self.smode: SentStructModeRecord = smode
        self.extra_param = extra_param

class SentStructMode(Enum):
    ANY = re.compile(r'^.*$', re.I)
    POSITION_PRIORITY = re.compile(r'^pp$', re.I)
    ORDERED_GROUP = re.compile(r'^\d+$', re.I)
    NO_PUNCTUATION = re.compile(r'^np$', re.I)
    MAX_UPTO = re.compile(r'^mx$', re.I)
    NO_CONJUNCTIVES = re.compile(r'^nc$', re.I)
    NO_FULL_STOP = re.compile(r'^nfs$', re.I)

    @classmethod
    def getName(cls, string_value: str):
        for name, member in cls.__members__.items():
            is_any = (member == cls.ANY)
            if is_any:
                continue

            is_match = (member.value.search(string_value) is not None)
            if bool(is_match):
                return member
        return cls.ANY

class OverLappingState(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    BOTH = 3
    WITHIN = 4

class TranslationState(Enum):
    UNTRANSLATED = 0
    ACCEPTABLE = 1
    FUZZY = 2
    IGNORED = 3
    REMOVE = 4

class TextStyle(Enum):
    NORMAL = 0
    ITALIC = 1
    BOLD = 2
    BOX = 3
    RAW = 4

class RefType(Enum):
    PYTHON_FORMAT = "%"
    FUNCTION = "func"
    GA = "\`"
    BLANK_QUOTE = "§"
    ARCH_BRACKET = "()"
    ARCH_BRACKET_OPEN = "("
    ARCH_BRACKET_CLOSE = ")"
    AST_QUOTE = "*"
    DBL_AST_QUOTE = "**"
    DBL_QUOTE = "\""
    SNG_QUOTE = "'"
    MM = ":MM:"
    ABBR = ":abbr:"
    CLASS = ":class:"
    DOC = ":doc:"
    GUILABEL = ":guilabel:"
    KBD = ":kbd:"
    LINENOS = ":linenos:"
    MATH = ":math:"
    MENUSELECTION = ":menuselection:"
    MOD = ":mod:"
    METHOD = ":meth:"
    FUNC = ":func:"
    REF = ":ref:"
    SUP = ":sup:"
    TERM = ":term:"
    OSL_ATTRIB = "w:w"
    TEXT = "generic_text"
    FILLER = "filler"

    @classmethod
    def getRef(cls, string_value: str):
        for name, member in cls.__members__.items():
            if member.value == string_value:
                return member
        return None

'''
    ABBREV_TEXT_REVERSE = re.compile(r'([^\(]+)\s\(([^\)]+)\)')
    REF_TEXT_REVERSE = re.compile(r'([^\`]+)\s\-\-\s([^\<]+)(?<![\s])')
    MENU_TEXT_REVERSE = re.compile(r'(?!\s)([^\(\)\-\>]+)(?<!\s)')
'''
