from matcher import MatcherRecord
from definition import TranslationState, Definitions as df
from refs.ref_base import RefBase
from ignore import Ignore as ig
from get_text_within import GetTextWithin as gwt
import re

class RefDoubleAST(RefBase):

    def getPattern(self):
        return df.DBL_AST_QUOTES

    def formatTranslationSingle(self, orig: str, tran: str):
        is_tran = (tran is not None)
        orig = self.squareBracket(orig)
        if is_tran:
            tran = self.squareBracket(tran)
            tran = gwt.getTextMidOnly(tran)
        orig = gwt.getTextMidOnly(orig)

        if is_tran:
            new_txt = f'\\":abbr:`{orig} ({tran})`\\"'
        else:
            new_txt = f'":abbr:`{orig} ()`"'
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
        has_tran = (tran is not None)
        if not has_tran:
            self.statTranslation(orig=txt)
        else:
            mm.translation = tran
            mm.translation_state = TranslationState.ACCEPTABLE
            self.statTranslation(matcher=mm)
        return entry