from matcher import MatcherRecord
from definition import TranslationState
from refs.ref_base import RefBase
from ignore import Ignore as ig

import re

class RefGAWithBrackets(RefBase):

    def getPattern(self):
        pat_list = [
            r'(?<!(:))\`+(<([^`<>]+)>)\`+',
            r'(?<!(:))\`+([\-]+([^`]+\w))\`+',
            r'(?<!(:))\`+([\#]+(\w[^`]+\w))\`+',
            r'(?<!(:))\`+(\w[^`]+\w)\`+',
            r'"(\w[^"]+\w)"+',
            r"(?<!(\w))'(\w[^']+\w)'+",
        ]
        temp_list=[]
        for pat_txt in pat_list:
            pat_txt = r'(%s)' % (pat_txt)
            temp_list.append(pat_txt)

        pat_txt = '|'.join(temp_list)
        pat = re.compile(pat_txt)
        return pat

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (sub_loc, sub_txt) = sub_list[1]
        try:
            (txt_loc, txt) = sub_list[2]
        except Exception as e:
            (txt_loc, txt) = sub_list[1]

        is_empty_sub_txt = (sub_txt is None) or (bool(sub_txt) and len(sub_txt.strip()) == 0)
        is_empty_txt = (txt is None) or (bool(txt) and len(txt.strip()) == 0)
        is_empty = (is_empty_sub_txt or is_empty_txt)
        if is_empty:
            return entry

        is_ignore = ig.isIgnoredWord(sub_txt) or ig.isIgnoredWord(txt)
        if is_ignore:
            return entry

        tran = self.tf.isInDict(txt)
        has_tran = (tran is not None)
        if not has_tran:
            self.need_tran_list.append(txt)
            tran = ""

        tran = self.extractAbbr(tran)
        tran = self.squareBracket(tran)
        tran = self.removeOrig(txt, tran)

        is_single_quote = (mm.txt.startswith("'") and mm.txt.endswith("'"))
        quote = ('"' if not is_single_quote else "'")
        new_txt = f'\\{quote}:abbr:`{sub_txt} ({tran})`\\{quote}'
        mm.translation = new_txt
        mm.translation_state = TranslationState.ACCEPTABLE
        return entry