from matcher import MatcherRecord
from definition import TranslationState
from refs.ref_base import RefBase
from ignore import Ignore as ig

from definition import Definitions as df
from pattern_utils import PatternUtils as pu

import re

class RefBrackets(RefBase):

    def getPattern(self):
        # ast_quote_single_txt = r'[\*]((?!\s)[^\*]+(?<!\s))[\*]'
        pat_list = [
            r'[\<]([^\<\>]*)[\>]',
            r'[\[]([^\[\]]*)[\]]',
            r'[\|]([^\|]*)[\|]',
            r'[\(]([^\(\)]*)[\)]',
            r'[\{]([^\{\}]*)[\}]',
        ]
        temp_list = []
        for pat in pat_list:
            p_pat = r'(%s)' % (pat)
            temp_list.append(p_pat)

        pat_txt = '|'.join(temp_list)
        pat = re.compile(pat_txt)
        return pat

    def formatTranslationSingle(self, orig: str, tran: str):
        is_tran = (tran is not None)
        orig = self.squareBracket(orig)
        if is_tran:
            tran = self.squareBracket(tran)

        if is_tran:
            new_txt = f':abbr:`{tran} ({orig})`'
        else:
            new_txt = f':abbr:`({orig})`'
        return new_txt

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        pat = self.getPattern()
        sub_dict = pu.patternMatchAll(pat, mm.txt)
        try:
            sub_dict_list = list(sub_dict.items())
            (first_entry_loc, first_entry_mm) = sub_dict_list[0]
            sub_list = first_entry_mm.getSubEntriesAsList()
            (oloc, orig) = sub_list[0]
            try:
                (txt_loc, txt) = sub_list[1]
            except Exception as e:
                (txt_loc, txt) = sub_list[0]
        except Exception as e:
            df.LOG(f'{entry}\n{e}')
            raise e

        is_ignore = ig.isIgnoredWord(txt)
        if is_ignore:
            return entry

        tran = self.translateSingle(txt)
        has_tran = (tran is not None)
        if not has_tran:
            self.statTranslation(orig=txt)
        else:
            (os, oe) = oloc
            (ts, te) = txt_loc
            ns = ts - os
            ne = len(mm.txt) - (oe - te)
            new_loc = (ns, ne)

            new_tran = str(mm.txt)
            new_tran = self.jointText(new_tran, tran, new_loc)
            mm.translation = new_tran
            mm.translation_state = TranslationState.ACCEPTABLE
            self.statTranslation(matcher=mm)
        return entry