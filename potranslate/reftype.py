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
    TEXT = "generic_text"
    FILLER = "filler"
'''
    ABBREV_TEXT_REVERSE = re.compile(r'([^\(]+)\s\(([^\)]+)\)')
    REF_TEXT_REVERSE = re.compile(r'([^\`]+)\s\-\-\s([^\<]+)(?<![\s])')
    MENU_TEXT_REVERSE = re.compile(r'(?!\s)([^\(\)\-\>]+)(?<!\s)')
'''
