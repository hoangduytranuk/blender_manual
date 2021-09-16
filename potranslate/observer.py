from collections import OrderedDict
from definition import Definitions as df, RefType
from pattern_utils import PatternUtils as pu

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
        untran_dict = pu.findInvert(df.FILLER_PARTS, self.blank, is_reversed=True)
        return untran_dict

    def getRawUnmarkedPartsAsList(self):
        untran_dict = pu.findInvert(df.FILLER_CHAR_PATTERN, self.blank, is_reversed=True, is_removing_symbols=False)
        txt_loc_list=[]
        for loc, txt_mm in untran_dict.items():
            entry=(loc, txt_mm.txt)
            txt_loc_list.append(entry)
        return txt_loc_list

    def getRawUnmarkedPartsAsDict(self):
        untran_dict = pu.findInvert(df.FILLER_CHAR_PATTERN, self.blank, is_reversed=True, is_removing_symbols=False)
        return untran_dict
