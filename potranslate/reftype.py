from enum import Enum
class SentStructMode(Enum):
    ANY = ''
    NO_PUNCTUATION = 'np'
    MAX_UPTO = 'mx'
    NO_CONJUNCTIVES = 'nc'
    NO_FULL_STOP = 'nfs'

    @classmethod
    def getName(cls, string_value: str):
        for name, member in cls.__members__.items():
            if member.value == string_value:
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
