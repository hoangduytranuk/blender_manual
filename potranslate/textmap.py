# from common import Common as cm, dd, pp
from observer import LocationObserver
from definition import Definitions as df
from matcher import MatcherRecord
from ignore import Ignore as ig
from pattern_utils import PatternUtils as pu

class TextMap(list):
    def __init__(self, txt: str,  is_reverse=True, is_removing_symbols=False, using_pattern=None):
        self.msg = txt
        self.is_reverse=is_reverse
        self.is_removing_symbols=is_removing_symbols
        self.using_pattern=using_pattern
        self.actual_pattern = None
        self.matched_dict = None
        self.matched_list = None
        self.loc_dic = None
        self.obs = None
        self.ref_dict_list = None
        self.ignore_list={}
        self.dist_list=None
        self.sep_pattern=df.SYMBOLS

    def removeIgnoredEntries(self, input_list):
        loc_obs = LocationObserver(self.msg)
        non_ignore_list=[]
        for loc, txt in input_list:
            is_ignore = ig.isIgnored(txt)
            if is_ignore:
                entry = {loc: txt}
                self.ignore_list.update(entry)
                df.LOG(f'IGNORED:[{txt}]')
                loc_obs.markLocAsUsed(loc)

        for loc, txt in input_list:
            is_ignored = loc_obs.isLocUsed(loc)
            if is_ignored:
                continue
            entry = (loc, txt)
            non_ignore_list.append(entry)
        return non_ignore_list

    def genListOfDistance(self, max):
        dist_list = []
        for s in range(0, max):
            for e in range(0, max):
                is_valid = (s < e)
                if not is_valid:
                    continue

                distance = (e - s)
                entry = (distance, s, e)
                if entry not in dist_list:
                    dist_list.append(entry)
        return dist_list

    def sortGetWordLen(self, item):
        (loc, txt) = item
        wc = len(txt.split())
        txt_len = len(txt)
        return (txt_len, wc)

    def getWordListFromDistanceList(self, dist_list):
        loc_dict = {}
        for loc, mm in self.matched_list:
            entry = {loc: mm.txt}
            loc_dict.update(entry)

        for entry in dist_list:
            distance, from_index, to_index = entry
            start_loc, start_mm = self.matched_list[from_index]
            end_loc, end_mm = self.matched_list[to_index]

            ss1, ee1 = start_loc
            ss2, ee2 = end_loc

            fragment = self.msg[ss1: ee2]

            sub_loc = (ss1, ee2)
            entry = {sub_loc: fragment}
            loc_dict.update(entry)
        return loc_dict


    def genmap(self):
        part_list = []
        obs: LocationObserver = None
        self.obs = LocationObserver(self.msg)
        self.sep_pattern = (df.SPACE_WORD_SEP if not self.is_removing_symbols else df.SYMBOLS)
        self.actual_pattern = (self.using_pattern if self.using_pattern else self.sep_pattern)
        self.matched_dict = pu.patternMatchAll(self.actual_pattern, self.msg)
        self.matched_list = list(self.matched_dict.items())
        max = len(self.matched_dict)
        self.loc_dic = {}

        self.dist_list = self.genListOfDistance(max)
        self.dist_list.sort(reverse=self.is_reverse)

        self.loc_dic = self.getWordListFromDistanceList(self.dist_list)

        part_list = list(self.loc_dic.items())
        part_list.sort(key=self.sortGetWordLen, reverse=True)
        non_ignored_list = self.removeIgnoredEntries(part_list)

        return non_ignored_list