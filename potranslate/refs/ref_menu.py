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

    def getTextForTranslate(self, entry):
        txt = self.getTextForTranslate(entry)
        text_dict = pu.findInvert(RefMenu.menu_sep_pat, txt)
        return list(text_dict.values())

    def parse(self, entry):
        from definition import Definitions as df
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]
        sub_mm: MatcherRecord = None

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (txt_loc, txt) = sub_list[1]
        try:
            text_dict = pu.findInvert(RefMenu.menu_sep_pat, txt)
            translated_list_temp = list(map(self.translate, text_dict.items()))
            translated_list = [x for x in translated_list_temp if x is not None]
            translated_list.sort(reverse=True)
        except Exception as e:
            df.LOG(f'{entry}\n{e}')
            raise e
        is_changed = False
        new_sub_txt = str(txt)
        for (sub_loc, sub_mm) in translated_list:
            has_tran = self.isTranslated(sub_mm)
            if not has_tran:
                self.statTranslation(orig=sub_mm.txt)
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
        self.statTranslation(matcher=mm)
        return entry