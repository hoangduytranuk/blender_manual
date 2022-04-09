from matcher import MatcherRecord
from definition import TranslationState
from refs.ref_base import RefBase
from ignore import Ignore as ig

import re

class RefWithInternalLink(RefBase):

    def getPattern(self):
        pat = re.compile(r'\`([^\`\<\>]+)\`_', re.I)
        return pat

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (txt_loc, txt) = sub_list[1]

        is_ignore = ig.isIgnoredWord(txt)
        if is_ignore:
            return entry

        tran = self.tf.isInDict(txt)
        has_translation = (tran is not None)
        if not has_translation:
            return entry

        tran = self.extractAbbr(tran)
        tran = self.squareBracket(tran)

        (os, oe) = oloc
        (ts, te) = txt_loc
        ns = ts - os
        ne = len(mm.txt) - (oe - te)
        new_loc = (ns, ne)

        new_tran = f'{orig} (*{tran}*)'
        mm.translation = new_tran
        mm.translation_state = TranslationState.ACCEPTABLE
        return entry