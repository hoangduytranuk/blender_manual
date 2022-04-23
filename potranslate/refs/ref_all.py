from matcher import MatcherRecord
from definition import TranslationState
from refs.ref_base import RefBase
from ignore import Ignore as ig
from definition import Definitions as df
import re

class RefAll(RefBase):
    # pattern_list_with_reserved = [
    #     (PYTHON_FORMAT, RefType.PYTHON_FORMAT),
    #     (SNG_QUOTE, RefType.SNG_QUOTE),
    #     (DBL_QUOTE, RefType.DBL_QUOTE),
    #     (AST_QUOTES, RefType.AST_QUOTE),
    #     (GA_DOUBLE_EMBEDDED_GA, RefType.GA_EMBEDDED_GA),
    #     (GA_SINGLE, RefType.SINGLE_GA),
    #     (GA_DOUBLE, RefType.DOUBLE_GA),
    #     (BLANK_QUOTE, RefType.BLANK_QUOTE),
    #     (ATTRIB_REF, RefType.ATTRIB),
    #     (GA_GENERIC_DOUBLE, RefType.GENERIC_DOUBLE_GA),
    #     (GA_GENERIC_SINGLE, RefType.GENERIC_SINGLE_GA),
    #     (REF_GENERIC, RefType.GENERIC_REF),
    #     (RESERVED_TXTS, RefType.RESERVED),
    #     (ARCH_BRAKET_SINGLE_FULL, RefType.ARCH_BRACKET),
    # ]
    def getPattern(self):
        # var = r'[\w\_\.\-]+'
        # param = r'(%s(\,(\s+)?)?)+' % (var)
        # multiple = r'^\w+\(s\)$'
        # ga_multi = r'([\`]+)?'
        # # funct = r'^%s(%s\((%s)?\))%s$' % (ga_multi, var, param, ga_multi)
        # funct = r'%s(%s\((%s[^\(\)]+)?\))%s' % (ga_multi, var, var, ga_multi)
        # funct_pat_txt = r'^%s$' % (funct)

        reserved_txt = [
            r'(e\.g\.)',
            r'(i\.e\.)',
            r'(etc\.)',
            r'((Ref|Irr|Mr|Dr|Ms|Fig|vs|GPU|GPL)\.)',
            r'(v\.v\.+)',
            r'({[^{}]+})',
            r'(\|[^\|]+\|)',
            r'(\%[\d\.dsf]+(\%+)?)',
            r'(@{[^{}@]+})',
            r'(![^!]+!)',
            # r'(\\?[\+\-]+)|(\?+)|(\_[\#]+)|([\%\º])',
            r'(\[([^\[\]]+)\])',
        ]
        reserved_txts = '|'.join(reserved_txt)

        BLANK_QUOTE_MARK = '§'
        blank_quote_txt = r'(?<!\w)(\%s)([^\%s]+)(?:\b)(\%s)' % (BLANK_QUOTE_MARK, BLANK_QUOTE_MARK, BLANK_QUOTE_MARK)  # BLANK_QUOTE
        python_format_txt = r'(?:\s|^)(\'?%\w\')(?:\W|$)'
        # ref_generic_txt = r'(:\w+:)?\`+(\w[^\`]+\w)\`+[_]+?'
        # pat_txt = r'(?<!\:)\`+((?=\w)[^\`<>]+(?<=\w))\`+'
        ref_generic_with_heading_txt = r':\w+:\`+((?=\w)[^`]+(?<![\s:]))\`+(\_+)?'
        ref_generic_no_heading_txt = r'(?<!\:)\`+((?!=[\s:])[^`]+(?<![\s:]))\`+(\_+)?'

        ast_generic = r'[\*]+((?=\w)[^\*].+?)[\*]+'
        # "*f*ake user**"
        # ast_special = r'(?<=\s)(([\*]((?=\w)(?!\*\*).+?)(?<!\s)[\*]{2,})(?=\s))'

        sng_generic = r'(?<!\w)[\']+((?=\w)[^\']+(?<=\w))[\']+'
        dbl_quoted_generic = r'[\"]+((?=\w)[^\"]+(?<=\w))[\"]+'
        pat_list = [
            df.funct_pat_txt,
            df.single_quote_txt,
            df.dbl_quote_txt,
            df.ast_quote_txt,
            ref_generic_with_heading_txt,
            ref_generic_no_heading_txt,    # REF_GENERIC
            ast_generic,
            sng_generic,
            dbl_quoted_generic,
        ]
        temp_list=[]
        for pat_txt in pat_list:
            pat_txt = r'(%s)' % (pat_txt)
            temp_list.append(pat_txt)

        pat_txt = r'|'.join(temp_list)
        pat = re.compile(pat_txt)
        return pat

    def getTextForTranslate(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        try:
            (txt_loc, txt) = sub_list[2]
        except Exception as e:
            try:
                (txt_loc, txt) = sub_list[1]
            except Exception as e:
                (oloc, txt) = sub_list[0]
        return txt

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        # (oloc, orig) = sub_list[0]
        msg = f'IGNORE_REF: {mm.getSubEntriesAsList()} {mm.type}'
        print(msg)
        return entry