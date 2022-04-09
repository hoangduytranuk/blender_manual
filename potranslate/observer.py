import re
from collections import OrderedDict
from definition import Definitions as df
from matcher import MatcherRecord

class LocationObserver(OrderedDict):
    symbol_txt = r'[\W]+'
    left_symbol = r'^(%s)' % (symbol_txt)
    right_symbol = r'(%s)$' % (symbol_txt)
    all_symbol_txt = r'^(%s)$' % (symbol_txt)
    SYMBOLS = re.compile(symbol_txt)
    LEFT_SYMBOLS = re.compile(left_symbol)
    RIGHT_SYMBOLS = re.compile(right_symbol)
    ALL_SYMBOLS = re.compile(all_symbol_txt)
    
    def __init__(self, msg):
        self.orig_msg = msg
        self.blank = str(msg)
        self.marked_loc={}

    def __repr__(self):
        string = ""
        try:
            string = '\n----LocationObserver start------'
            # string += "\nrecord:\n{!r}".format(self.__dict__)
            string += f'\nself.orig_msg: {self.orig_msg}'
            string += f'\nself.blank: {self.blank}'
            for (loc, txt) in self.marked_loc.items():
                string += f'\n[{loc}]: [{txt}]'
            string += '\n----LocationObserver end------\n'
        except Exception as e:
            pass
        return string

    @classmethod
    def reproduce(cls, msg):
        return cls(msg)

    def hasBlankedAreas(self):
        return (len(self.marked_loc) > 0)

    def hasLeftRight(self):
        return self.hasBlankedAreas()

    def getLocList(self):
        loc_list = list(self.marked_loc)
        loc_list.sort()
        return loc_list

    def getLeft(self):
        fill_char_index = self.blank.find(df.FILLER_CHAR)
        is_found = (fill_char_index >=0)
        if not is_found:
            return self.orig_msg
        else:
            e = max(0, fill_char_index)
            return self.orig_msg[:e]

    def getRight(self):
        fill_char_index = self.blank.rfind(df.FILLER_CHAR)
        is_found = (fill_char_index >=0)
        if not is_found:
            return self.orig_msg
        else:
            s = min(len(self.orig_msg), fill_char_index + 1)
            return self.orig_msg[s:]

    def stripNonAlphaBegin(self):
        orig_coord = (0, len(self.orig_msg))
        (s, e) = orig_coord
        left = self.getLeft()
        left_match = LocationObserver.LEFT_SYMBOLS.search(left)
        if left_match is not None:
            left_match_part = left_match.group(0)
            s = len(left_match_part)
            txt = self.orig_msg[s:e]
        loc = (s, e)
        return (loc, txt)

    def stripNonAlphaEnd(self):
        orig_coord = (0, len(self.orig_msg))
        (s, e) = orig_coord
        right = self.getRight()
        right_match = self.patternMatchAll(LocationObserver.RIGHT_SYMBOLS, right)
        if right_match is not None:
            right_match_part = right_match.group(0)
            e = max(0, e - len(right_match_part))
            txt = self.orig_msg[s:e]
        loc = (s, e)
        return (loc, txt)

    def getStrippedNonAlpha(self, txt: str):
        orig_coord = (0, len(txt))
        (s, e) = orig_coord
        (begin_loc, txt) = self.stripNonAlphaBegin(txt)
        s = begin_loc[0]
        (end_loc, txt) = self.stripNonAlphaEnd(txt)
        e = s + len(txt)
        loc = (s, e)
        return (loc, txt)

    def getMid(self):
        orig_coord = (0, len(self.orig_msg))
        (s, e) = orig_coord
        new_txt = str(self.orig_msg)

        left_stripped = False
        right_stripped = False

        left = self.getLeft()
        right = self.getRight()
        is_same = (left == right == self.orig_msg)
        if is_same:
            left = ""
            right = ""
            return (orig_coord, new_txt)

        left_match = LocationObserver.LEFT_SYMBOLS.search(left)
        right_match = LocationObserver.RIGHT_SYMBOLS.search(right)
        is_cut_left = (left_match is not None)
        is_cut_right = (right_match is not None)
        if is_cut_left:
            left_part = left_match.group(0)
            left_len = len(left_part)
            s += left_len
            new_txt = new_txt[left_len:]
        if is_cut_right:
            right_part = right_match.group(0)
            right_len = len(right_part)
            e -= right_len
            new_txt = new_txt[:-right_len]
        loc = (s, e)
        return (loc, new_txt)

    def patternMatchAll(self, pat, text):
        return_dict = OrderedDict()
        try:
            for m in pat.finditer(text):
                match_record = MatcherRecord(matcher_record=m)
                match_record.pattern = pat
                loc = match_record.getMainLoc()
                dict_entry = {loc: match_record}
                return_dict.update(dict_entry)
        except Exception as e:
            msg = f'pattern:[{pat}]\ntext:[{text}]\nException:[{e}]'
            raise RuntimeError(msg)
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

    def jointText(self, orig: str, tran: str, loc: tuple):
        backup = [str(orig), str(tran)]
        if not bool(tran):
            return orig

        s, e = loc
        left = orig[:s]
        right = orig[e:]
        new_str = left + tran + right
        return new_str

    def markAllLocAsKeep(self, loc_list: list):
        try:
            all_fill = (df.FILLER_CHAR * len(self.blank))
            loc_list.sort(reverse=True)
            for loc in loc_list:
                (s, e) = loc
                word = self.orig_msg[s: e]
                all_fill = self.jointText(all_fill, word, loc)
            self.blank = all_fill
        except Exception as e:
            pass

    def markLocListAsUsed(self, loc_list: list, filler_char=df.FILLER_CHAR):
        try:
            for loc in loc_list:
                self.markLocAsUsed(loc, filler_char=filler_char)
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

    def checkOverlappedLocList(self, loc_list):
        def sortByLength(loc):
            len = (loc[1] - loc[0])
            return len

        over_lapped_list=[]
        sorted_by_length = list(sorted(loc_list, reverse=True, key=sortByLength))
        for loc in sorted_by_length:
            is_taken = self.isLocUsed(loc)
            if is_taken:
                over_lapped_list.append(loc)
            else:
                self.markLocAsUsed(loc)

        return over_lapped_list

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

    def markAsUsed(self, s: int, e: int, filler_char=df.FILLER_CHAR):
        def insertMarkedLoc(ss: int, ee: int):
            loc = (ss, ee)
            marked_loc_entry = {loc: self.blank[ss:ee]}
            blk = (filler_char * (ee - ss))
            left = self.blank[:ss]
            right = self.blank[ee:]
            self.blank = left + blk + right
            self.marked_loc.update(marked_loc_entry)

        marking_request_loc = self.blank[s: e]
        not_filled_dict = self.patternMatchAll(df.NOT_FILLER_CHARS, marking_request_loc)
        for (loc, mm) in not_filled_dict.items():
            (ls, le) = loc
            (ns, ne) = (s + ls, s + le)
            insertMarkedLoc(ns, ne)

    def hasMarkedLoc(self):
        marked_loc_length = len(self.marked_loc)
        return (marked_loc_length > 0)

    def markLocAsUsed(self, loc: tuple, filler_char=df.FILLER_CHAR):
        ss, ee = loc
        self.markAsUsed(ss, ee, filler_char=filler_char)

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

    def getUnmarkedPartsAsDict(self, reversing=True, marking_off=True):
        unmarked_dict = self.patternMatchAll(df.NOT_FILLER_CHARS, self.blank)
        if reversing:
            try:
                if marking_off:
                    loc_list = unmarked_dict.keys()
                    self.markLocListAsUsed(loc_list)

                rev_dict_list = list(unmarked_dict.items())
                rev_dict_list.sort(reverse=reversing)
                return OrderedDict(rev_dict_list)
            except Exception as e:
                msg = f'[{self.orig_msg}], e:[{e}]'
                df.LOG(msg)
                raise RuntimeError(msg)
        else:
            return unmarked_dict

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
        return invert_dict



