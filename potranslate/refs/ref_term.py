from matcher import MatcherRecord
from definition import TranslationState
from refs.ref_base import RefBase

import re

class RefTerm(RefBase):

    def getPattern(self):
        pat = re.compile(r':term:\`([^\`]+)\`', re.I)
        return pat

    def formatTranslationSingle(self, orig: str, tran: str):
        is_tran = (tran is not None)
        orig = self.squareBracket(orig)
        if is_tran:
            tran = self.squareBracket(tran)

        if is_tran:
            new_txt = f'{orig} ({tran})'
        else:
            new_txt = f'({orig})'
        return new_txt

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (txt_loc, txt) = sub_list[1]

        tran = self.tf.isInDict(txt)
        has_tran = (tran is not None)
        if not has_tran:
            return entry

        tran = self.extractAbbr(tran)
        (os, oe) = oloc
        (ts, te) = txt_loc
        ns = ts - os
        ne = len(mm.txt) - (oe - te)
        new_loc = (ns, ne)

        new_tran = f'{orig} (*{tran}*)'
        mm.translation = new_tran
        mm.translation_state = TranslationState.ACCEPTABLE
        return entry