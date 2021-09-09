from collections import OrderedDict
from definition import Definitions as df, RefType
from matcher import MatcherRecord
import operator as OP

class LocationObserver(OrderedDict):
    def __init__(self, msg):
        self.blank = str(msg)
        self.marked_loc={}

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

    def getNoneAlphaPart(self, msg, is_start=True):
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

    def getTextWithinWithDiffLoc(self, msg, to_matcher_record=False):
        # should really taking bracket pairs into account () '' ** "" [] <> etc.. before capture
        left_part = self.getNoneAlphaPart(msg, is_start=True)
        right_part = self.getNoneAlphaPart(msg, is_start=False)
        ss = len(left_part)
        ee = (-len(right_part) if right_part else len(msg))
        mid_part = msg[ss:ee]
        length_ee = len(right_part)
        diff_loc = (ss, length_ee)

        main_record: MatcherRecord = None
        if to_matcher_record:
            ls=0
            le=ss
            ms=le
            me=ms + len(mid_part)
            rs=me
            re=rs + len(right_part)

            main_record=MatcherRecord(s=0, e=len(msg), txt=msg)
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

    def getTextWithin(self, msg):
        diff_loc, left, mid, right,_ = self.getTextWithinWithDiffLoc(msg)
        return left, mid, right

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

    def findInvert(self, pattern, text:str, is_reversed=False, is_removing_symbols=True):
        '''
        findInvert:
            Find list of words that are NOT matching the pattern.
            can use to find words amongst puntuations for instance.
            The routine uses internally declared FILLER_CHAR to mark the
            boundaries of unmatched words and then SPLIT at these boundaries
        :param pattern:
            the re.compile(d) pattern to use to find/replace
        :param text:
            the string of text that words are to be found
        :return:
            list of words that are NOT matching the pattern input
        '''

        is_string = isinstance(pattern, str)
        invert_required = False
        pat = pattern
        if is_string:
            # form the invert character pattern
            pat_string = r'(%s)(\w[^%s]+\w)(%s)' % (pattern, pattern, pattern)
            pat = compile(pat_string)
        else:
            invert_required = True

        found_list = []
        mm : MatcherRecord = None
        matched_dict = self.patternMatchAll(pat, text)
        if not invert_required:
            for mmloc, mm in matched_dict.items():
                mm.type = RefType.TEXT
                mm.pattern = pat
                loc, found_txt = mm.getOriginAsTuple()

                is_used = self.isLocUsed(loc)
                if is_used:
                    continue

                entry = (loc, mm)
                found_list.append(entry)
        else:
            # 2: extract location list
            loc_list = matched_dict.keys()

            # 3: extract invert locations, using the location list above
            invert_loc_list = []
            ws = we = 0
            for s, e in loc_list:
                we = s
                if (ws < we):
                    invert_loc_list.append((ws, we))
                ws = e
            we = len(text)
            if (ws < we):
                invert_loc_list.append((ws, we))

            # 4: using the invert location list, extract words, exclude empties.
            for ws, we in invert_loc_list:
                found_txt = text[ws:we]

                if is_removing_symbols:
                    left, mid, right = self.getTextWithin(found_txt)
                    is_empty = (not bool(mid))
                    if is_empty:
                        continue

                loc = (ws, we)
                is_used = self.isLocUsed(loc)
                if is_used:
                    continue

                mm = MatcherRecord(s=ws, e=we, txt=found_txt)
                mm.type = RefType.TEXT
                mm.pattern = pat
                entry = (loc, mm)
                found_list.append(entry)

        if is_reversed:
            found_list.sort(key=OP.itemgetter(0), reverse=True)

        return_dict = OrderedDict(found_list)
        # dd('findInvert() found_list:')
        # dd('-' * 30)
        # pp(return_dict)
        # dd('-' * 30)
        return return_dict

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
        is_already_marked = (loc in self.marked_loc)
        if is_already_marked:
            return

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

    def getUnmarkedPartsAsDict(self):
        untran_dict = self.findInvert(df.FILLER_PARTS, self.blank, is_reversed=True)
        return untran_dict

    def getRawUnmarkedPartsAsList(self):
        untran_dict = self.findInvert(df.FILLER_CHAR_PATTERN, self.blank, is_reversed=True, is_removing_symbols=False)
        txt_loc_list=[]
        for loc, txt_mm in untran_dict.items():
            entry=(loc, txt_mm.txt)
            txt_loc_list.append(entry)
        return txt_loc_list

    def getRawUnmarkedPartsAsDict(self):
        untran_dict = self.findInvert(df.FILLER_CHAR_PATTERN, self.blank, is_reversed=True, is_removing_symbols=False)
        return untran_dict
