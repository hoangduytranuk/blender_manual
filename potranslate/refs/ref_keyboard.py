from matcher import MatcherRecord
from definition import Definitions as df
from pattern_utils import PatternUtils as pu
from definition import TranslationState
from refs.ref_base import RefBase
import re

class RefKeyboard(RefBase):
    menu_sep_pat = re.compile(r'\s?[-]{2}>\s?')
    def getPattern(self):
        pat = re.compile(r':kbd:\`([^\`]+)\`', re.I)
        return pat

    def formatTranslation(self, mm: MatcherRecord):
        return mm

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (txt_loc, txt) = sub_list[1]

        tran = str(txt)
        kbd_dict = self.tf.kbd_dict
        is_changed = False
        result_dict = pu.patternMatchAll(df.KEYBOARD_SEP, txt)
        for sub_loc, sub_mm in result_dict.items():
            txt = sub_mm.txt
            has_dic = (txt in kbd_dict)
            if not has_dic:
                continue

            tr = kbd_dict[txt]
            if tr:
                tran = self.jointText(tran, tr, sub_loc)
                is_changed = True

        if not is_changed:
            return entry

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