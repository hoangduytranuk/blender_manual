import re
from collections import OrderedDict
from definition import Definitions as df
from matcher import MatcherRecord

class LocationObserver(OrderedDict):
    def __init__(self, msg):
        self.orig_msg = msg
        self.blank = str(msg)
        self.marked_loc={}

    def patternMatchAll(self, pat, text):
        return_dict = {}
        try:
            for m in pat.finditer(text):
                match_record = MatcherRecord(matcher_record=m)
                match_record.pattern = pat
                loc = match_record.getMainLoc()
                dict_entry = {loc: match_record}
                return_dict.update(dict_entry)
        except Exception as e:
            pass
            # df.LOG(e)
        return return_dict

    def markIgnoredAsUsed(self, ignore_dict):
        try:
            is_dict = isinstance(ignore_dict, dict)
            if not is_dict:
                return

            valid = (ignore_dict is not None) and (len(ignore_dict) > 0)
            if not valid:
                return

            for loc, txt in ignore_dict.items():
                s = self.blank.find(txt)
                is_found = (s >= 0)
                if not is_found:
                    continue

                e = len(txt)
                loc = (s, s + e)
                self.markLocAsUsed(loc)

        except Exception as e:
            df.LOG(f'{e}')

    def markLocListAsUsed(self, loc_list: list):
        try:
            for loc in loc_list:
                self.markLocAsUsed(loc)
        except Exception as e:
            pass

    def getTextAt(self, s: int, e: int):
        try:
            txt = self.blank[s:e]
            return txt
        except Exception as e:
            return None

    def getTextAtLoc(self, loc):
        (s, e) = loc
        return self.getTextAt(s, e)

    def isOverlapped(self, loc, is_on_left=False):
        '''
        Check to see if a location is overlapped on the left/right side
        :param loc: location to be test
        :is_on_left: boolean value, indicating to check on left, if True, else check on right
        :return:
            True if location is used and overlapped
            False if location it NOT USED, or not overlapped
        '''
        if not self.isLocUsed(loc):
            return False

        ls, le = loc
        try:
            if is_on_left:
                current_char = self.blank[ls]
                left_char = self.blank[ls - 1]
            else:
                current_char = self.blank[le]
                left_char = self.blank[le + 1]
            is_ovrlap = (current_char == df.FILLER_CHAR) and (left_char == df.FILLER_CHAR)
            return is_ovrlap
        except Exception as e:
            return False

    def isUsableLoc(self, loc):
        '''
        Check to see if a loc is used and is contained within, but not overlapped either on left or right
        :param loc: location to be tested
        :return:
            True if location is used and not overlapped left or right
            False if location it NOT USED, or is overlapped on left or on right
        '''
        if not self.isLocUsed(loc):
            return True

        is_left_ovrlap = self.isOverlapped(loc, is_on_left=True)
        is_right_ovrlap = self.isOverlapped(loc, is_on_left=False)
        ok = not (is_left_ovrlap or is_right_ovrlap)
        return ok

    def getTextAtLoc(self, loc: tuple):
        (s, e) = loc
        return self.getTextAt(s, e)

    def markListAsUsed(self, loc_list:list):
        for loc in loc_list:
            self.markLocAsUsed(loc)

    def markAsUsed(self, s: int, e: int):
        loc = (s, e)
        marked_loc_entry = {loc: self.blank[s:e]}
        blk = (df.FILLER_CHAR * (e - s))
        left = self.blank[:s]
        right = self.blank[e:]
        self.blank = left + blk + right
        self.marked_loc.update(marked_loc_entry)

    def hasMarkedLoc(self):
        marked_loc_length = len(self.marked_loc)
        return (marked_loc_length > 0)

    def markLocAsUsed(self, loc: tuple):
        ss, ee = loc
        self.markAsUsed(ss, ee)

    def isPartlyUsed(self, s: int, e: int):
        part = self.blank[s:e]
        is_dirty = (df.FILLER_PARTS.search(part) is not None)
        is_fully_used = (df.FILLER_CHAR_ALL_PATTERN.search(part) is not None)
        return (is_dirty and not is_fully_used)

    def isLocPartlyUsed(self, loc: tuple):
        s, e = loc
        return self.isPartlyUsed(s, e)

    def isLocFullyUsed(self, loc: tuple):
        s, e = loc
        return self.isFullyUsed(s, e)

    def isFullyUsed(self, s:int, e:int):
        part = self.blank[s:e]
        is_all_used = (df.FILLER_CHAR_ALL_PATTERN.search(part) is not None)
        return is_all_used

    def isUsed(self, s: int, e: int):
        part = self.blank[s:e]
        is_dirty = (df.FILLER_PARTS.search(part) is not None)
        return is_dirty

    def isLocUsed(self, loc: tuple):
        s, e = loc
        return self.isUsed(s, e)

    def isCompletelyUsed(self):
        is_fully_done = (df.FILLER_CHAR_ALL_PATTERN.search(self.blank) is not None)
        return is_fully_done

    def getUnmarkedPartsAsDict(self, reversing=True):
        untran_dict = self.patternMatchAll(df.NOT_FILLER_CHARS, self.blank)
        if reversing:
            return reversed(untran_dict)
        else:
            return untran_dict

    def findInvert(self, pattern: re.Pattern, is_reverse=False, is_removing_symbol=False):
        def getNoneAlphaPart(msg, is_start=True):
            if not msg:
                return ""

            non_alnum_part = ""
            if is_start:
                non_alpha = df.START_WORD_SYMBOLS.search(msg)
            else:
                non_alpha = df.END_WORD_SYMBOLS.search(msg)

            if non_alpha:
                non_alnum_part = non_alpha.group(0)
            return non_alnum_part

        def getTextWithinWithDiffLoc(msg, to_matcher_record=False):
            # should really taking bracket pairs into account () '' ** "" [] <> etc.. before capture
            left_part = getNoneAlphaPart(msg, is_start=True)
            right_part = getNoneAlphaPart(msg, is_start=False)
            ss = len(left_part)
            ee = (-len(right_part) if right_part else len(msg))
            mid_part = msg[ss:ee]
            length_ee = len(right_part)
            diff_loc = (ss, length_ee)

            main_record: MatcherRecord = None
            if to_matcher_record:
                ls = 0
                le = ss
                ms = le
                me = ms + len(mid_part)
                rs = me
                re = rs + len(right_part)

                main_record = MatcherRecord(s=0, e=len(msg), txt=msg)
                if left_part:
                    main_record.addSubMatch(ls, le, left_part)
                    test_txt = left_part[ls: le]
                else:
                    main_record.addSubMatch(-1, -1, None)
                if mid_part:
                    main_record.addSubMatch(ms, me, mid_part)
                    test_txt = left_part[ms: me]
                else:
                    main_record.addSubMatch(ls, re, msg)
                if right_part:
                    main_record.addSubMatch(rs, re, right_part)
                    test_txt = left_part[rs: re]
                else:
                    main_record.addSubMatch(-1, -1, None)

            return diff_loc, left_part, mid_part, right_part, main_record

        def getTextWithin(msg):
            diff_loc, left, mid, right, _ = getTextWithinWithDiffLoc(msg)
            return left, mid, right

        self.blank = str(self.orig_msg)
        forward_search_dict = self.patternMatchAll(pattern, self.blank)
        used_loc_list = forward_search_dict.keys()
        self.markLocListAsUsed(used_loc_list)

        invert_dict = self.getUnmarkedPartsAsDict(reversing=is_reverse)

        mm: MatcherRecord = None
        if is_removing_symbol:
            new_mm_dict = OrderedDict()
            for (loc, mm) in invert_dict.items():
                try:
                    left, mid, right = getTextWithin(mm.txt)
                    if not bool(mid):
                        continue

                    (s, e) = loc
                    mm.txt = mid
                    mm.s = (s + len(left))
                    mm.e = (e - len(right))
                    loc = (mm.s, mm.e)
                    new_entry = {loc: mm}
                    new_mm_dict.update(new_entry)
                except Exception as e:
                    msg = f'mm:{mm} e:[{e}]'
                    raise RuntimeError(msg)

            invert_dict = new_mm_dict
        return invert_dict