from matcher import MatcherRecord
from pattern_utils import PatternUtils as pu
from definition import TranslationState
from refs.ref_base import RefBase

import re

class RefMenu(RefBase):
    menu_sep_pat = re.compile(r'\s?[-]{2}>\s?')
    def getPattern(self):
        pat = re.compile(r':menuselection:\`([^\`]+)\`', re.I)
        return pat

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (txt_loc, txt) = sub_list[1]
        text_dict = pu.findInvert(RefMenu.menu_sep_pat, txt)
        translated_list = list(map(self.translate, text_dict.items()))

        translated_list.sort(reverse=True)
        is_changed = False
        new_sub_txt = str(txt)
        for (sub_loc, sub_mm) in translated_list:
            has_tran = self.isTranslated(sub_mm)
            if not has_tran:
                continue

            is_changed = True
            new_sub_txt = self.jointText(new_sub_txt, sub_mm.translation, sub_loc)

        if not is_changed:
            return

        (os, oe) = oloc
        (ts, te) = txt_loc
        ns = ts - os
        ne = len(mm.txt) - (oe - te)
        new_loc = (ns, ne)

        new_tran = str(mm.txt)
        new_tran = self.jointText(new_tran, new_sub_txt, new_loc)
        mm.translation = new_tran
        mm.translation_state = TranslationState.ACCEPTABLE
        return entry