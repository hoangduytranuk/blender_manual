import re
from definition import RefType, Definitions as df
from string_utils import StringUtils as st
from pattern_utils import PatternUtils as pu
from collections import OrderedDict
from matcher import MatcherRecord
from observer import LocationObserver

class RefAndBracketsParser(OrderedDict):
    def __init__(self, txt, location_observer=None, original_for_removal=None):
        self.msg = txt
        self.pattern_list = None
        self.local_obs: LocationObserver = location_observer
        self.item_list = None
        self.original_for_removal = original_for_removal

    def reset(self):
        self.pattern_list = None
        self.local_obs: LocationObserver = None
        self.item_list = None
        self.clear()

    def __repr__(self):
        string = '\n----RefAndBracketsParser start------'
        # string += "\nrecord:\n{!r}".format(self.__dict__)
        string += f'\nmsg:[{self.msg}]'
        string += f'\n[{self.local_obs}]'
        string += f'\n[{self.items()}]'
        string += '\n----RefAndBracketsParser end------\n'
        return string

    def __str__(self):
        return self.__repr__()

    def getItemByIndex(self, index: int, is_no_location=False):
        item_list = list(self.items())
        try:
            (loc, required_item) = item_list[index]
            if is_no_location:
                return (required_item)
            else:
                return (loc, required_item)
        except Exception as e:
            return (None)

    @classmethod
    def reproduce(cls, msg, loc_obs=None):
        return cls(msg, location_observer=loc_obs)

    def cleanupOverlapps(self):
        mm: MatcherRecord = None
        remove_list = []

        temp_obs = LocationObserver(self.msg)
        loc_list = self.keys()
        # only applicable for non-ref types, (ARCH_BRACKET AND TEXT)
        rm_overlapped_list = temp_obs.checkOverlappedLocList(loc_list)
        for loc in rm_overlapped_list:
            del self[loc]

    def setReftypeAndUsingSubTextLocation(self, dict_list: dict, ref_type: RefType):
        for main_loc, mm in dict_list.items():
            new_mm_list=[]
            mm_list_of_items = mm.getSubEntriesAsList()
            new_mm_list.append(mm_list_of_items[0])
            main_s, main_e = main_loc
            main_txt = mm.txt
            for index in range(1, len(mm_list_of_items)):
                is_type_field = (index == 1)
                (sub_s, sub_e), sub_txt = mm_list_of_items[index]
                # if is_type_field:
                #     try:
                #         sub_ref_type = RefType.getRef(sub_txt)
                #         actual_ref_type = (sub_ref_type if bool(sub_ref_type) else ref_type)
                #     except Exception as e:
                #         actual_ref_type = RefType.TEXT
                #     mm.type = actual_ref_type

                if sub_txt:
                    dist = (sub_e - sub_s)
                    ss = (sub_s - main_s)
                    ee = ss + dist
                    new_entry = ((ss, ee), sub_txt)
                else:
                    new_entry = ((sub_s, sub_e), sub_txt)
                new_mm_list.append(new_entry)
            mm.clear()
            mm.update(new_mm_list)

    def updateSelfOBS(self, location_list):
        for loc in location_list:
            self.local_obs.markLocAsUsed(loc)

    def makeMMForOriginal(self):
        msg_lower = self.msg.lower()
        orig_lower = self.original_for_removal.lower()
        removing_pattern = f'({orig_lower})'
        find_index = (msg_lower.find(removing_pattern))
        is_found = (find_index >= 0)
        if not is_found:
            return (None, None)

        s = find_index
        e = (find_index + len(removing_pattern))
        removing_part = self.msg[s:e]
         # =-1, e=-1, txt=None, matcher_record: re.Match =None, ref_type: RefType = RefType.TEXT, pattern=None):
        mm = MatcherRecord(s=s, e=e, txt=removing_part, ref_type=RefType.REMOVE_ORIGINAL)
        mm.addSubMatch(s, e, removing_part)
        loc = (s, e)
        entry = (loc, mm)
        return entry

    def getMatches(self, pat: re.Pattern, find_txt: str, ref: RefType, include_brackets=False):
        local_found_dict = {}
        try:
            is_remove_original = (ref == RefType.REMOVE_ORIGINAL) and (self.original_for_removal is not None)
            if is_remove_original:
                (loc, mm) = self.makeMMForOriginal()
                is_found = (loc is not None)
                if is_found:
                    local_found_dict.update({loc: mm})
            else:
                is_bracket = (ref == RefType.ARCH_BRACKET)
                if is_bracket:
                    local_found_dict = st.getTextWithinBrackets('<|(|{|[', ']|)|}|>', find_txt, is_include_bracket=include_brackets)
                else:
                    local_found_dict = pu.patternMatchAll(pat, find_txt, ref_type=ref, is_including_surrounding_symbols=include_brackets)
            is_found = (len(local_found_dict) > 0)
            if is_found:
                self.updateSelfOBS(local_found_dict.keys())
        except Exception as e:
            df.LOG(f'{e}; pat:[{pat}]; find_txt:[{find_txt}]; ref:[{ref}]; local_found_dict:[{local_found_dict}];', error=True)
            raise e
        return local_found_dict

    def findOnePattern(self, msg: str, pattern: re.Pattern, reftype: RefType, include_brackets=False):
        valid_msg = (msg is not None) and (len(msg) > 0)
        valid_pattern = (pattern is not None)
        valid = valid_msg and valid_pattern
        if not valid:
            return

        found_dict = OrderedDict()
        try:
            found_dict = self.getMatches(pattern, msg, reftype, include_brackets=include_brackets)
            if found_dict:
                is_debug = (reftype == RefType.SNG_QUOTE)
                if is_debug:
                    is_debug = True

                self.update(found_dict)
                self.breakupOBS()
                self.cleanupDup()
        except Exception as e:
            df.LOG(f'{e} msg:[{msg}]; found_dict:[{found_dict}]', error=True)
            raise e

    def findPattern(self, pattern_list: list, txt: str, include_brackets=False):
        # pattern_list.reverse()
        for index, item in enumerate(pattern_list):
            p, ref_type = item
            self.findOnePattern(txt, p, ref_type, include_brackets=include_brackets)

        return len(self)

    def getListOfRefType(self, request_list_of_ref_type):
        ref_list = [mm for (loc, mm) in self.items() if mm.type in request_list_of_ref_type]
        return ref_list

    def getUnparsedDict(self, unparsed_dict: dict):
        mm: MatcherRecord = None
        unparsed = OrderedDict()
        for uloc, mm in unparsed_dict.items():
            (ms, me) = mm.getMainLoc()
            mtxt = mm.getMainText()

            mm = MatcherRecord(s=ms, e=me, txt=mtxt)
            mm.addSubMatch(-1, -1, None)
            mm.addSubMatch(0, len(mtxt), mtxt)
            mm.type = RefType.TEXT
            entry = {uloc: mm}
            unparsed.update(entry)
        return unparsed

    def breakupOBS(self):
        '''
        Once parsed, sometimes, new patterns might cause some text containing FILLER_CHAR in it.
        This routine will break up at the FILLER_CHAR boundaries and create new RefType.TXT entry,
        updating the locations from the original locations, which is from self.msg, not the brokenup text.
        :return:
        '''
        def clone_one_entry(entry):
            mm: MatcherRecord = None
            (mm_loc, current_mm) = entry
            origin_loc = clone_one_entry.orig_loc
            new_mm = current_mm
            new_mm.type = RefType.TEXT
            new_mm.override(new_root_loc=origin_loc)

        mm: MatcherRecord = None
        all_breakup_list = []
        rm_list = []
        for (loc, mm) in self.items():
            txt_to_breakup = mm.txt
            pattern_to_breakup = df.FILLER_CHAR_PATTERN
            breakup_dict = pu.patternMatchAll(pattern_to_breakup, txt_to_breakup, ref_type=RefType.TEXT)
            has_been_broken = bool(breakup_dict)
            if not has_been_broken:
                continue

            print(f'SPLITTING UP: {mm}')
            rm_list.append(loc)
            clone_one_entry.orig_loc = loc
            clone_one_entry.orig_mm = mm
            breakup_one_item_list = list(map(clone_one_entry, breakup_dict.items()))
            all_breakup_list.extend(breakup_one_item_list)
            self.local_obs.markLocAsUsed(loc)
            exit(0)

        for loc in rm_list:
            del self[loc]

        all_breakup_dict = OrderedDict(all_breakup_list)
        self.update(all_breakup_dict)

    def breakByPunctuations(self, item_dict: dict):
        breakup_dict=OrderedDict()
        mm: MatcherRecord = None
        for (loc, mm) in item_dict.items():
            txt = mm.txt
            breakup_test = df.SIMPLE_PUNCTUATIONS.split(txt)
            has_breakup = len(breakup_test) > 1
            if not has_breakup:
                breakup_dict.update({loc: mm})
                continue

            break_up_one_dict = pu.findInvert(df.SIMPLE_PUNCTUATIONS, txt)
            bk_mm: MatcherRecord = None
            for (bk_loc, bk_mm) in break_up_one_dict.items():
                bk_mm.override(new_root_loc=loc)
                entry = {bk_mm.loc: bk_mm}
                breakup_dict.update(entry)
        return breakup_dict

    def sort(self, reverse=False, key=None):
        item_list = list(self.items())
        item_list.sort(key=key, reverse=reverse)
        dict = OrderedDict(item_list)
        self.clear()
        self.update(dict)

    def parseMessage(self, is_ref_only=False, include_brackets=False, pattern_list=None, breakup_obs=False, is_reverse=False):
        def getMatches(entry):
            pat: re.Pattern = entry[0]
            ref: RefType = entry[1]
            local_found_dict = {}
            try:
                is_remove_original = (ref == RefType.REMOVE_ORIGINAL) and (self.original_for_removal is not None)
                if is_remove_original:
                    (loc, mm) = self.makeMMForOriginal()
                    is_found = (loc is not None)
                    if is_found:
                        local_found_dict.update({loc: mm})
                else:
                    is_bracket = (ref == RefType.ARCH_BRACKET)
                    if is_bracket:
                        local_found_dict = st.getTextWithinBrackets('<|(|{|[', ']|}|)|>', self.local_obs.blank,
                                                                    is_include_bracket=include_brackets)
                    else:
                        local_found_dict = pu.patternMatchAll(pat, self.local_obs.blank, ref_type=ref,
                                                              is_including_surrounding_symbols=include_brackets)
                is_found = (len(local_found_dict) > 0)
                if is_found:
                    loc_list = list(local_found_dict.keys())
                    self.local_obs.markLocListAsUsed(loc_list)
                    self.update(local_found_dict)
                    # self.update(found_dict)
                    # self.breakupOBS()
                    # self.cleanupDup()
            except Exception as e:
                df.LOG(f'{e}; pat:[{pat}]; find_txt:[{self.local_obs.blank}]; ref:[{ref}]; local_found_dict:[{local_found_dict}];',
                       error=True)
                raise e
            return list(local_found_dict.items())

        is_inherited_local_obs = (self.local_obs is not None)
        if not is_inherited_local_obs:
            self.local_obs = LocationObserver(self.msg)

        actual_pattern_list = (pattern_list if pattern_list else df.pattern_list)
        self.pattern_list = actual_pattern_list

        found_list = list(map(getMatches, actual_pattern_list))
        # self.findPattern(actual_pattern_list, self.msg, include_brackets=include_brackets)
        if not is_ref_only:
            unparsed_dict = self.local_obs.getUnmarkedPartsAsDict()
            if not bool(unparsed_dict):
                return

            self.update(unparsed_dict)
            # breakup_dict = self.breakByPunctuations(unparsed_dict)
            # self.update(breakup_dict)
            # self.breakupOBS()

        num_items = len(self)
        is_ignore_sorting = (num_items < 2)
        if is_ignore_sorting:
            return

        temp_list = list(self.items())
        temp_list.sort(reverse=is_reverse)
        self.clear()
        self.update(temp_list)
        return self

    @classmethod
    def parseMsg(self, msg: str, is_ref_only=False, include_brackets=False, pattern_list=None):
        self.parseMessage(is_ref_only=True, include_brackets=include_brackets, pattern_list=pattern_list)
        return self

    def sortByLength(self, loc):
        return (loc[1] - loc[0])

    def cleanupDup(self):
        overall_loc = self.keys()
        temp_obs = LocationObserver(self.msg)
        overlapped_locs = temp_obs.checkOverlappedLocList(overall_loc)
        for loc in overlapped_locs:
            del self[loc]

    def parseMsgAndBrackets(self, msg: str, is_ref_only=False, include_brackets=False, pattern_list=None):
        def jointText(orig: str, tran: str, loc: tuple):
            backup = [str(orig), str(tran)]
            if not bool(tran):
                return orig

            s, e = loc
            left = orig[:s]
            right = orig[e:]
            new_str = left + tran + right
            return new_str


        def sortByStartLocation(item):
            (loc, mm) = item
            return loc[0]

        # overall_list = RefAndBracketsParser.reproduce(msg)
        # overall_list.parseMessage(is_ref_only=True, include_brackets=include_brackets, pattern_list=df.no_bracket_pattern_list)
        #
        # if not is_ref_only:
        #     bracket_list = RefAndBracketsParser.reproduce(overall_list.local_obs.blank, loc_obs=overall_list.local_obs)
        #     bracket_list.parseMessage(is_ref_only=is_ref_only, include_brackets=include_brackets, pattern_list=[(df.ARCH_BRAKET_SINGLE_FULL, RefType.ARCH_BRACKET)])
        #     overall_list.update(bracket_list)
        # sorted_dict = OrderedDict(sorted(list(overall_list.items()), reverse=False, key=sortByStartLocation))

        self.msg = msg
        self.parseMessage(is_ref_only=True, include_brackets=include_brackets, pattern_list=df.no_bracket_pattern_list)

        if not is_ref_only:
            self.parseMessage(is_ref_only=is_ref_only, include_brackets=include_brackets, pattern_list=[(df.ARCH_BRAKET_SINGLE_FULL, RefType.ARCH_BRACKET)])
        sorted_dict = OrderedDict(sorted(list(self.items()), reverse=False, key=sortByStartLocation))
        self.update(sorted_dict)
        return self

    def getBreakupSentenceList(self):
        def removeStartEnd(entry):
            m: MatcherRecord = None
            (loc, m) = entry
            (s, e) = loc
            txt = m.txt
            start_match = df.REMOVABLE_START.search(txt)
            can_remove_start = (start_match is not None)
            if can_remove_start:
                start_match_part = start_match.group(0)
                s += len(start_match_part)
                txt = txt[s:]

            end_match = df.REMOVABLE_END.search(txt)
            can_remove_end = (end_match is not None)
            if can_remove_end:
                end_match_part = end_match.group(0)
                e -= len(end_match_part)
                txt = txt[:e]

            m.txt = txt
            m.updateMasterLoc(s, e)
            entry = (loc, m)
            return entry

        self.parseMessage(is_ref_only=True, pattern_list=df.pattern_list_with_reserved, include_brackets=True, is_reverse=False)
        obs = self.local_obs
        punct_loc_dict = pu.patternMatchAll(df.BASIC_PUNCTUALS, obs.blank)
        obs = LocationObserver(self.msg)
        punct_loc_list  = punct_loc_dict.keys()
        obs.markLocListAsUsed(punct_loc_list)
        sent_dict = obs.getUnmarkedPartsAsDict(reversing=False)
        # trimmed_list = list(map(removeStartEnd, sent_dict.items()))
        # return_dict = OrderedDict(trimmed_list)
        return sent_dict

    def getTextStrippedNonAlpha(self):
        self.parseMessage(is_ref_only=True, pattern_list=df.pattern_list_with_reserved, include_brackets=True, is_reverse=False)
        obs = self.local_obs
        left = obs.getLeft()
        right = obs.getRight()
        is_left_ignoreable = (bool(left) and df.REMOVALBLE_SYMBOLS.search(left) is not None) or (len(left) == 0)
        is_right_ignoreable = (bool(right) and df.REMOVALBLE_SYMBOLS.search(right) is not None) or (len(right) == 0)
        is_only_one_ref = (len(self) == 1)
        is_drilldown_able = (is_left_ignoreable and is_right_ignoreable and is_only_one_ref)
        if is_drilldown_able:
            mm: MatcherRecord = None
            ref_list = list(self.items())
            (loc, mm) = ref_list[0]
            ref_type = mm.type
            is_unquotable = (ref_type in df.ref_type_unquoteable)
            if not is_unquotable:
                mid = obs.getMid()
                return mid
            else:
                self.reset()
                self.parseMessage(is_ref_only=True, pattern_list=df.pattern_list_with_reserved, include_brackets=False, is_reverse=False)
                obs = self.local_obs
                mid = obs.getMid()
        else:
            mid = obs.getMid()
        return mid

        # def trimItemText(txt: str, is_start=True):
        #     orig_coord = (0, len(txt))
        #     (s, e) = orig_coord
        #     pat: re.Pattern = (df.SYMB_STARTING if is_start else df.SYMB_ENDING)
        #     match: re.Match = pat.search(txt)
        #     has_match = (match is not None)
        #     if not has_match:
        #         loc = (s, e)
        #         return (loc, txt)
        #
        #     match_part = match.group(0)
        #     len_matched = len(match_part)
        #     if is_start:
        #         s += len_matched
        #         txt = txt[len_matched:]
        #     else:
        #         e -= len_matched
        #         txt = txt[:-len_matched]
        #     loc = (s, e)
        #     return (loc, txt)
        #
        # def getRemovableItems(item: ((int, int), MatcherRecord)):
        #     (loc, mm) = item
        #     txt = mm.txt
        #     type = mm.type
        #     is_ref = (type != RefType.TEXT)
        #     if is_ref:
        #         return (None, None)
        #
        #     is_removable = (df.SYMBOLS_ONLY.search(txt) is not None)
        #     if is_removable:
        #         return item
        #     else:
        #         return (None, None)
        #
        # self.parseMessage(is_ref_only=False, pattern_list=df.pattern_list_with_reserved, include_brackets=False, is_reverse=False)
        # ref_list = list(self.items())
        # removable_list = list(map(getRemovableItems, ref_list))
        # removable_items = [(x, y) for (x, y) in removable_list if (x is not None) and (y is not None)]
        # has_removeable_items = (len(removable_items) > 0)
        # if not has_removeable_items:
        #     (start_loc, new_msg) = trimItemText(self.msg, is_start=True)
        #     (end_loc, new_msg) = trimItemText(self.msg, is_start=False)
        #     (new_s, new_e) = (start_loc[0], end_loc[1])
        #     new_msg = self.msg[new_s: new_e]
        #     return ((new_s, new_e), new_msg)
        # else:
        #     removable_left_dict={}
        #     mm: MatcherRecord = None
        #     for (loc, mm) in removable_items:
        #         if (loc == None):
        #             break
        #         else:
        #             removable_left_dict.update({loc: mm})
        #     removable_left_list = list(removable_left_dict.items())
        #     removable_left_list.sort(reverse=True)
        #
        #     removable_items.reverse()
        #     removable_right_dict={}
        #     for (loc, mm) in removable_items:
        #         if (loc == None):
        #             break
        #         else:
        #             removable_right_dict.update({loc: mm})
        #     removable_right_list = list(removable_right_dict.items())
        #     removable_right_list.sort(reverse=True)
        #
        #     is_remove_right = (len(removable_right_list) > 0)
        #     is_remove_left = (len(removable_left_list) > 0)
        #     if is_remove_right:

        return ((0, len(self.msg)), self.msg)