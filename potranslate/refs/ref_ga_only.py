from matcher import MatcherRecord
from definition import TranslationState, Definitions as df
from refs.ref_base import RefBase
from ignore import Ignore as ig

import re

class RefGA(RefBase):
    option_with_value = re.compile(r'[\-]+\w{3}(\s[\+\-]?\d)')
    def getPattern(self):
        return df.GA_ONLY
        # return df.ARCH_BRAKET_MULTI_SIMPLE



    def formatTranslationSingle(self, orig: str, tran: str):

        is_ignorable = ig.isIgnoreableText(orig)
        if is_ignorable:
            return None

        is_tran = (tran is not None)
        orig = self.squareBracket(orig)
        if is_tran:
            tran = self.squareBracket(tran)
            tran = self.extractAbbr(tran)
            is_option = (tran.startswith('-'))
            if is_option:
                tran = df.START_WORD_SYMBOLS.sub("", tran)

        # test_go_first = df.GA_GO_FIRST.search("PDT Command Line")
        is_orig_goes_first = (df.GA_GO_FIRST.search(orig) is not None)
        if is_orig_goes_first:
            if is_tran:
                new_txt = f'":abbr:`{orig} ({tran})`"'
            else:
                new_txt = f'":abbr:`{orig} ()`"'
        else:
            if tran:
                new_txt = f'":abbr:`{tran} ({orig})`"'
            else:
                new_txt = f'":abbr:`({orig})`"'
        return new_txt

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (txt_loc, txt) = sub_list[1]

        is_ignorable = ig.isIgnoreableText(txt)
        if is_ignorable:
            return entry

        tran = self.tf.isInDict(txt)
        has_tran = (tran is not None)
        if not has_tran:
            self.statTranslation(orig=txt)
            tran = ""

        tran = self.formatTranslationSingle(txt, tran)
        is_ignore = (tran is None)
        if is_ignore:
            return entry

        mm.translation = tran
        mm.translation_state = TranslationState.ACCEPTABLE
        self.statTranslation(matcher=mm)
        return entry