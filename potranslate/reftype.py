from enum import Enum

class RefType(Enum):
    GA = "\`"
    ARCH_BRACKET = "()"
    AST_QUOTE = "*"
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
