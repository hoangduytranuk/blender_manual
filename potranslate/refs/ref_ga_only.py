from matcher import MatcherRecord
from definition import TranslationState
from refs.ref_base import RefBase
from ignore import Ignore as ig

import re

class RefGA(RefBase):

    def getPattern(self):
        pat_txt = r'(?!=[:])[\`]+(\w[^\`\<\>]+\w)[\`]+(?=(\s|$))'
        pat = re.compile(pat_txt)
        return pat

    def formatTranslationSingle(self, orig: str, tran: str):
        is_tran = (tran is not None)
        orig = self.squareBracket(orig)
        if is_tran:
            tran = self.squareBracket(tran)

        if is_tran:
            new_txt = f'\\":abbr:`{tran} ({orig})`\\"'
        else:
            new_txt = f'":abbr:`({orig})`"'
        return new_txt

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (txt_loc, txt) = sub_list[1]

        is_ignore = ig.isIgnoredWord(txt)
        if is_ignore:
            return entry

        tran = self.translateSingle(txt)
        mm.translation = tran
        mm.translation_state = TranslationState.ACCEPTABLE
        return entry