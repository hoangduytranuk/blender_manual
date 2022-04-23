from matcher import MatcherRecord
from definition import TranslationState, Definitions as df
from refs.ref_base import RefBase
from ignore import Ignore as ig
from pattern_utils import PatternUtils as pu

import re

class RefFunction(RefBase):
    function_name_separator = re.compile(r'\.')
    function_param_separator = re.compile(r'\,\s?')

    def getPattern(self):
        return df.FUNCTION

    def getTextForTranslate(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (fn_name_loc, function_name_txt) = sub_list[1]
        try:
            (fn_param_loc, function_param_txt) = sub_list[3]
        except Exception as e:
            function_param_txt = ""

        function_name_list = RefFunction.function_name_separator.split(function_name_txt)
        function_param_list = RefFunction.function_param_separator.split(function_param_txt)
        function_name_list.extend(function_param_list)
        return function_name_list

    def parse(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, txt) = sub_list[0]

        is_ignored = ig.isIgnoredWord(txt)
        if is_ignored:
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