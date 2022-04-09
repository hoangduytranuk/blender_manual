from matcher import MatcherRecord
from definition import TranslationState
from refs.ref_base import RefBase

import re

class RefAbbr(RefBase):
    menu_sep_pat = re.compile(r'\s?[-]{2}>\s?')
    def getPattern(self):
        pat = re.compile(r':abbr:\`([^\`\(\)]+)\s\(([^\`\(\)]+)\)\`', re.I)
        return pat

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (abr_loc, txt) = sub_list[1]
        (txt_loc, txt) = sub_list[2]

        old_tran_01 = self.tf.isInDict(txt)
        has_tran = (old_tran_01 is not None)
        if not has_tran:
            return None

        tran = self.extractAbbr(old_tran_01)
        (os, oe) = oloc
        (ts, te) = txt_loc
        ns = ts - os
        ne = len(mm.txt) - (oe - te)
        new_loc = (ns, ne)

        new_tran = str(mm.txt)
        new_tran = self.jointText(new_tran, tran, new_loc)
        mm.translation = new_tran
        mm.translation_state = TranslationState.ACCEPTABLE
        return entry