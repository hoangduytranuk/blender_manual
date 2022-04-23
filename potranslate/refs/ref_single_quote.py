from matcher import MatcherRecord
from definition import TranslationState, Definitions as df
from refs.ref_base import RefBase
from ignore import Ignore as ig

import re

class RefSingleQuote(RefBase):

    def getPattern(self):
        return df.SINGLE_QUOTE

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        try:
            sub_list = mm.getSubEntriesAsList()
            (oloc, orig) = sub_list[0]
            (txt_loc, txt) = sub_list[1]
        except Exception as e:
            df.LOG(f'{entry}\n{e}')
            raise e

        is_ignore = ig.isIgnoredWord(txt)
        if is_ignore:
            return entry

        tran = self.translateSingle(txt)
        has_translation = (tran is not None)
        if not has_translation:
            self.statTranslation(orig=txt)
            tran = f'({txt})'

        tran = f":abbr:`{tran}`"
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