import re
import os
from babel.messages.catalog import Message
from matcher import MatcherRecord
from cleanref.clean_ref import CleanRef
from common import Common as cm
from collections import OrderedDict, defaultdict
from bracket import RefAndBracketsParser as PSER
from definition import Definitions as df

class CleanTitles(CleanRef):
    def cleanRepeatRefUnnessessarily(self, m: Message):

        word_count_dict = defaultdict(int)
        mid = m.id
        is_in_title_list = (mid in self.title_list)
        if not is_in_title_list:
            return None

        mstr = m.string
        has_translation = bool(mstr)
        if not has_translation:
            return None

        repeat_orig = f'({mid})'
        is_repeated = (repeat_orig in mstr)
        if is_repeated:
            return None

        id_ref_list = PSER(mid)
        id_ref_list.parseMessage(is_ref_only=True, pattern_list=df.no_bracket_pattern_list, include_brackets=True, is_reverse=False)
        has_ref = (bool(id_ref_list) and len(id_ref_list) > 0)
        if has_ref:
            return None

        # has_one_ref = len(id_ref_list) == 1
        # if not has_one_ref:
        #     return None
        #
        # idref_list = list(id_ref_list.items())
        # first_ref: MatcherRecord = None
        # (first_ref_loc, first_ref) = idref_list[0]
        # is_consider_type = (first_ref.type in df.complex_pattern_type_list)
        # if not is_consider_type:
        #     return None

        id_word_list = df.CHARACTERS.findall(mid)
        str_word_list = df.CHARACTERS.findall(mstr)

        is_debug = (':doc:`Move' in mid)
        if is_debug:
            is_debug = True

        for word in str_word_list:
            is_in = (word in id_word_list)
            word_count_dict[word] += (1 if is_in else 0)

        is_duplicate_more_than_once = False
        word_count_report = []
        for (word, count) in word_count_dict.items():
            if count > 1:
                word_count_report.append((word, count))
                is_duplicate_more_than_once = True

        if is_duplicate_more_than_once:
            debug = True
            msg = f'POSSIBLE:'
            msg += f'mid: {mid}\nmstr: {mstr}\n'
            msg += f'{word_count_report}\n\n'
            print(msg)
        return m

    def solve_each_message(self, msg: Message):
        return self.cleanRepeatRefUnnessessarily(msg)
