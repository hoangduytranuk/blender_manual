import math
import re
from enum import Enum
from definition import Definitions as df
from fuzzywuzzy import fuzz
from pattern_utils import PatternUtils as pu
from matcher import MatcherRecord
from observer import LocationObserver
from itertools import chain

class CaseAction(Enum):
    NONE = 0
    UPPER = 1
    TITLE = 2
    LOWER = 3
    SENTENCE = 4 # first Upper, then all lower
    MIXED = 5

class CaseRecord(list):
    def __init__(self, txt: str, matcher_record: MatcherRecord = None):
        self.txt = txt
        self.s = -1
        self.e = -1
        self.case: CaseAction = CaseAction.NONE
        if bool(matcher_record):
            self.txt = matcher_record.txt
            self.s = matcher_record.s
            self.e = matcher_record.e

    def __repr__(self):
        string = ""
        try:
            string = '\n----CaseRecord start------'
            string += "\nCaseRecord:\n{!r}".format(self.__dict__)
            string += '\n----CaseRecord end------\n'
        except Exception as e:
            pass
        return string

    @classmethod
    def loc(cls):
        return (self.s, self.e)

    @classmethod
    def setLoc(cls, new_loc):
        (self.s, self.e) = new_loc

    def transformText(self, case_required: CaseAction):
        new_txt: str = self.txt
        if case_required == CaseAction.TITLE:
            new_txt = new_txt.title()
        elif case_required == CaseAction.UPPER:
            new_txt = new_txt.upper()
        elif case_required == CaseAction.LOWER:
            new_txt = new_txt.lower()
        self.txt = new_txt

class CaseActionList:
    upper_pattern_txt = r'%s+' % (CaseAction.UPPER.value)
    UPPER_PAT = re.compile(upper_pattern_txt)

    lower_pattern_txt = r'%s+' % (CaseAction.LOWER.value)
    LOWER_PAT = re.compile(lower_pattern_txt)

    title_pattern_txt = r'%s+' % (CaseAction.TITLE.value)
    TITLE_PAT = re.compile(title_pattern_txt)

    list_of_patterns = [(UPPER_PAT, CaseAction.UPPER),
                        (LOWER_PAT, CaseAction.LOWER),
                        (TITLE_PAT, CaseAction.TITLE)
                        ]

    def __init__(self):
        self.loc = None
        self.txt: str = None
        self.case_converted_txt = None
        self.case_list: list[CaseAction] = []
        self.case_value_string: str = None
        self.sentence_list = []

    def __repr__(self):
        string = ""
        try:
            string = '\n----CaseActionList start------\n'
            string += "\nCaseActionList:\n{!r}".format(self.__dict__)
            string += '\n----CaseActionList end------\n'
        except Exception as e:
            pass
        return string

    def refresh(self):
        current_string = self.getText()
        other = CaseActionList.makeInstance(current_string)
        self.clone(other)

    def clone(self, other):
        self.loc = other.loc
        self.txt = other.txt
        self.case_converted_txt = other.case_converted_txt
        self.case_list = other.case_list
        self.case_value_string = other.case_value_string
        self.sentence_list = other.sentence_list

    def refreshUsingNewText(self, txt: str):
        if not bool(txt):
            return

        other = CaseActionList.makeInstance(txt)
        self.clone(other)

    @classmethod
    def reproduce(cls):
        return cls()

    @classmethod
    def jointText(self, orig: str, tran: str, loc: tuple):
        backup = [str(orig), str(tran)]
        if not bool(tran):
            return orig

        s, e = loc
        left = orig[:s]
        right = orig[e:]
        new_str = left + tran + right
        return new_str

    def isConsideringTheSame(self, other):
        is_same_begin_and_end = self.isSameBeginAndEnd(other)
        if not is_same_begin_and_end:
            return False

        this_string: str = self.case_value_string
        other_string: str = other.case_value_string

        this_first: str = this_string[0]
        other_first: str = other_string[0]

        list_of_first = [this_first, other_first]
        is_considering_same = (this_first == other_first) or \
                              ((str(CaseAction.LOWER.value) not in list_of_first) and \
                              (str(CaseAction.MIXED.value) not in list_of_first))

        other_string_title_to_upper = (other_string.replace(str(CaseAction.TITLE.value), str(CaseAction.UPPER.value)))
        other_string_upper_to_title = (other_string.replace(str(CaseAction.UPPER.value), str(CaseAction.TITLE.value)))

        normal_ratio = fuzz.partial_ratio(this_string, other_string)
        upper_ratio = fuzz.partial_ratio(this_string, other_string_title_to_upper)
        title_ratio = fuzz.partial_ratio(this_string, other_string_upper_to_title)

        is_same = (is_considering_same and normal_ratio > 80) or \
                  (is_considering_same and upper_ratio > 80) or \
                  (is_considering_same and title_ratio > 80)
        return is_same



    def checkCase(self, s1: str) -> CaseAction:
        def getWordsCase(word: str):
            chars_only = df.CHARACTERS.findall(word)
            tword = ' '.join(chars_only)

            is_numeric = tword.isnumeric()
            is_upper = tword.isupper()
            is_lower = tword.islower()
            is_title = tword.istitle()
            if is_numeric:
                return CaseAction.LOWER
            if is_upper:
                return CaseAction.UPPER
            elif is_title:
                return CaseAction.TITLE
            elif is_lower:
                return CaseAction.LOWER
            else:
                return CaseAction.NONE

        word_case = getWordsCase(s1)
        if not word_case is CaseAction.NONE:
            return word_case

        # alnum_only_list = df.CHARACTERS.findall(s1)
        # alnum_only_txt = ' '.join(alnum_only_list)
        temp_word = df.NON_SYMBOL_AND_SPACE.sub('', s1)
        word_case = getWordsCase(temp_word)
        if not word_case is CaseAction.NONE:
            return word_case

        # we have words like variable, ie. AutoMerge, mix case
        word_list = df.SEP_CASE.findall(s1)
        have_words = bool(word_list)
        if not have_words:
            return CaseAction.NONE


        first_word_case = getWordsCase(word_list[0])
        has_remain = len(word_list) > 1
        if has_remain:
            remain_word_list = (word_list[1:] if len(word_list)>1 else [])
            remain_cases = list(map(getWordsCase, remain_word_list))
            test_lower = list(map(lambda x: x == CaseAction.LOWER, remain_cases))
            test_upper = list(map(lambda x: x == CaseAction.UPPER, remain_cases))
            test_title = list(map(lambda x: x == CaseAction.TITLE, remain_cases))
            is_remain_lower = (False not in test_lower)
            is_remain_upper = (False not in test_upper)
            is_remain_title = (False not in test_title)

            is_word_title = (first_word_case == CaseAction.UPPER or first_word_case == CaseAction.TITLE) and is_remain_lower
            if is_word_title:
                return CaseAction.TITLE # should be MIXED, but haven't yet working out how to copy the mixed case over yet
            is_word_upper = (first_word_case == CaseAction.UPPER) and is_remain_upper
            if is_word_upper:
                return CaseAction.UPPER
            is_word_lower = (first_word_case == CaseAction.LOWER) and is_remain_lower
            if is_word_lower:
                return CaseAction.LOWER
            return CaseAction.MIXED
        else:
            return first_word_case

        # is_first_tile = (first_word.istitle() or first_word.isupper())
        # is_remain_lower = (remain.islower())
        # is_remain_title = (remain.istitle() or remain.isupper())
        # if is_first_tile and is_remain_lower:
        #     return CaseAction.TITLE
        # elif is_first_tile and remain.istitle():
        #     return CaseAction.TITLE
        # elif not is_first_tile:
        #     return CaseAction.LOWER
        # else:
        #     return CaseAction.NONE

    def isSetenceCase(self):
        try:
            case_list = self.getListOfCases()
            first_word_rec = self.case_list[0]
            first_word_txt = first_word_rec.txt
            first_word_case = case_list[0]

            is_first_tile = (first_word_case == CaseAction.TITLE) or (len(first_word_txt) == 1 and first_word_case == CaseAction.UPPER)
            remainder_list = (case_list[1:] if len(case_list) > 1 else [])
            is_remainder_lower = not ((CaseAction.TITLE in remainder_list) or (CaseAction.UPPER in remainder_list))
            return (is_first_tile and is_remainder_lower)
        except Exception as e:
            return False

    def toSentenceCase(self):
        try:
            changed = False
            case_record: CaseRecord = None
            for index, case_record in enumerate(self.case_list):
                is_first = (index == 0)
                is_already_upper = (case_record.case != CaseAction.LOWER)
                is_change = (is_first and not is_already_upper)
                if not is_change:
                    continue

                case_record.transformText(CaseAction.TITLE)
                case_record.case = CaseAction.TITLE
                changed = True
            if changed:
                self.refresh()
            return True
        except Exception as e:
            return False

    def allToACase(self, chosen_case: CaseAction):
        try:
            case_record: CaseRecord = None
            for index, case_record in enumerate(self.case_list):
                case_record.transformText(chosen_case)
                case_record.case = chosen_case
            self.refresh()
            return True
        except Exception as e:
            return False

    def isAllTheSameCase(self, chosen_case: CaseAction):
        def isTitle(case_action):
            return (case_action == CaseAction.TITLE or case_action == CaseAction.UPPER)

        try:
            orig_case_list = self.getListOfCases()
            if chosen_case == CaseAction.TITLE:
                test_case_list = list(map(isTitle, orig_case_list))
            else:
                test_case_list = list(map(lambda x: x == chosen_case, orig_case_list))
            return (False not in test_case_list)
        except Exception as e:
            return False

    def ensureAfterFullStopUpperCase(self):
        full_stop_loc_list = pu.patternMatchAll(df.FULL_STOP_IN_SENTENCE, self.txt)
        if not bool(full_stop_loc_list):
            return

        changed = False
        mm: MatcherRecord = None
        case_record: CaseRecord = None
        list_of_case_record_needed_to_be_titled_case = []
        fs_loc_list = full_stop_loc_list.keys()
        for fs_loc in fs_loc_list:
            word_after_full_stop = None
            for index, case_record in enumerate(self.case_list):
                is_less = (case_record.loc < fs_loc)
                if is_less:
                    continue
                else:
                    # the first one that is greater than full_stop location
                    word_after_full_stop = (index, case_record)
                    break

            if bool(possible_loc_of_word_after_full_stop):
                list_of_case_record_needed_to_be_titled_case.append(word_after_full_stop)

        for (index, case_record) in list_of_case_record_needed_to_be_titled_case:
            case_record.transformText(CaseAction.TITLE)
            changed = True

        if changed:
            self.refresh()

    def copyRepeatedWordsOver(self, from_cal):
        try:
            changed = False
            from_clist = from_cal.case_list
            to_clist = self.case_list
            f_case_record: CaseRecord = None
            t_case_record: CaseRecord = None
            for f_case_record in from_clist:
                for t_case_record in to_clist:
                    is_same_word = (f_case_record.txt.lower() == t_case_record.txt.lower())
                    is_case_diff = (f_case_record.case != t_case_record.case)
                    is_correct = (is_same_word and is_case_diff)
                    if not is_correct:
                        continue

                    t_case_record.txt = f_case_record.txt
                    changed = True

            if changed:
                self.refresh()

        except Exception as e:
            msg = f'cal_from:{from_clist}\ncal_to:{to_clist}\nexception:{e}'
            df.LOG(msg)

    def wordMacherToCaseRecord(self, item):
        mm: MatcherRecord = None
        (loc, mm) = item
        case_rec = CaseRecord(None, matcher_record=mm)
        case_rec.case = self.checkCase(case_rec.txt)
        return case_rec

    def sentenceToCaseActionList(self, s1:str):
        def caseValueAsString(case_record: CaseRecord):
            return str(case_record.case.value)

        sep_list = pu.patternMatchAll(df.SPACE_GA_SEP, s1)
        loc_list = sep_list.keys()

        obs = LocationObserver(s1)
        obs.markLocListAsUsed(loc_list)
        word_dict = obs.getUnmarkedPartsAsDict(reversing=False)

        case_list_of_sentence: list[CaseRecord] = None
        x:CaseRecord = None
        case_list_of_one_sentence = list(map(self.wordMacherToCaseRecord, word_dict.items()))
        case_value_as_list = list(map(caseValueAsString, case_list_of_one_sentence))
        case_values_as_str = ''.join(case_value_as_list)

        return (s1, case_list_of_one_sentence, case_values_as_str)

    def matcherDictRecordToCaseAction(self, item):
        mm: MatcherRecord = None
        (loc, mm) = item
        (s1, case_list_of_one_sentence, case_values_as_str) = self.sentenceToCaseActionList(mm.txt)
        new_case_list_action = CaseActionList.reproduce()
        new_case_list_action.loc = loc
        new_case_list_action.txt = mm.txt
        new_case_list_action.case_list = case_list_of_one_sentence
        new_case_list_action.case_value_string = case_values_as_str
        return new_case_list_action

    def toCaseList(self):
        # first keep the record of overall text
        (txt, case_list, case_value_as_str) = self.sentenceToCaseActionList(self.txt)

        # second, break up sentences and see if they have
        sentence_dict = pu.findInvert(df.PUNCTUATION_WITHOUT_GA_TAG_FINDER, self.txt, is_removing_symbols=True)
        break_down_sentence_case_action_list = list(map(self.matcherDictRecordToCaseAction, sentence_dict.items()))
        self.loc = (0, len(self.txt))
        self.case_list = case_list
        self.sentence_list = break_down_sentence_case_action_list
        self.case_value_string = case_value_as_str

    def caseValueStr(self, case_list:list):
        try:
            s1_value_as_str_list = ''.join([str(x.value) for x in case_list])
            return s1_value_as_str_list
        except Exception as e:
            return []

    @classmethod
    def makeInstance(self, s1: str):
        cal_s1 = self.reproduce()
        cal_s1.txt = s1
        cal_s1.toCaseList()
        return cal_s1

    @classmethod
    def isBothMatched(self, s1: str, s2: str):
        is_valid = bool(s1) and bool(s2)
        if not is_valid:
            return False

        cal_s1 = self.makeInstance(s1)
        cal_s2 = self.makeInstance(s2)

        part_ratio = fuzz.partial_ratio(cal_s1.case_value_string, cal_s2.case_value_string)
        acceptable_ratio = (part_ratio > 80)

        first_word_case_s1 = cal_s1.case_list[0]
        first_word_case_s2 = cal_s2.case_list[0]

        is_both_first_word_same_case = (first_word_case_s1 == first_word_case_s2)

        is_first_word_case_diff = not (is_both_first_word_same_case)
        is_first_s1_lower = (first_word_case_s1 == CaseAction.LOWER)
        is_first_s2_lower = (first_word_case_s1 == CaseAction.LOWER)
        is_considering_compatable = is_first_word_case_diff and (is_first_s1_lower or is_first_s2_lower)

        is_acceptable = (is_both_first_word_same_case or is_considering_compatable) and acceptable_ratio
        return (is_acceptable, cal_s1, cal_s2)

    def convertCase(self, case_required: CaseAction, s1: str) -> str:
        def map_case(item):
            mm: MatcherRecord = None
            (loc, mm) = item
            new_txt: str = mm.txt
            if case_required == CaseAction.TITLE:
                new_txt = new_txt.title()
            elif case_required == CaseAction.UPPER:
                new_txt = new_txt.upper()
            elif case_required == CaseAction.LOWER:
                new_txt = new_txt.lower()
            elif case_required == CaseAction.SENTENCE:
                is_start = (map_case.current_s == -1) and (map_case.current_s == -1)
                if is_start:
                    new_txt = new_txt.title()
                else:
                    new_txt = new_txt.lower()
                (map_case.current_s, map_case.current_e) = loc

            mm.txt = new_txt
            (map_case.current_s, map_case.current_e) = loc

        map_case.current_s = -1
        map_case.current_e = -1

        list_word = list(map(map_case, pu.patternMatchAll(df.CHARACTERS, s1).items()))
        new_txt = str(s1)
        mm: MatcherRecord = None
        list_word.sort(reverse=True)
        for (loc, mm) in list_word:
            new_word = mm.txt
            new_txt = self.jointText(new_txt, new_word, loc)
        return new_txt

    def caseWeight(self, other):
        s1_value_as_str_list = self.case_value_string
        s2_value_as_str_list = other.case_value_string
        diff_ratio = fuzz.partial_ratio(s1_value_as_str_list, s2_value_as_str_list)
        return diff_ratio

    def enforceLegalLowercase(self, from_case_action_list):
        def lowercaseByChosenPattern(pattern: re.Pattern):
            old_txt = self.getText()
            new_txt = str(old_txt)
            first_word_case = from_case_action_list.case_list[0].case
            parts = pu.patternMatchAll(pattern, new_txt)
            mm: MatcherRecord= None
            mm_loc: tuple(int, int) = None
            mm_txt: str = None
            for (loc, mm) in parts.items():
                (s, e) = loc
                (mm_loc, mm_txt) = mm.getOriginAsTuple()
                lower_mm_txt = mm_txt

                leading_part = new_txt[0: s]
                leading_part_has_value = bool(leading_part)
                can_ignore_leading_part = leading_part_has_value and (df.SYMBOLS_ONLY.search(leading_part) is not None)

                is_first_1 = (s == 0) and not leading_part_has_value
                is_first_2 = (s > 0) and can_ignore_leading_part
                is_first = (is_first_1 or is_first_2)
                if is_first:
                    current_first_word_case = from_case_action_list.case_list[0].case
                    current_first_word_case = self.checkCase(mm_txt)
                    is_case_same = (first_word_case == current_first_word_case)
                    if is_case_same:
                        continue

                    is_current_lower = (current_first_word_case == CaseAction.LOWER)
                    is_target_lower = (first_word_case == CaseAction.LOWER)
                    is_compatible = not (is_current_lower and is_target_lower)
                    if is_compatible:
                        continue

                    lower_mm_txt = mm_txt.lower()
                else:
                    lower_mm_txt = mm_txt.lower()
                mm.txt = lower_mm_txt
            reverse_list = list(parts.items())
            reverse_list.sort(reverse=True)
            for (loc, mm) in reverse_list:
                new_txt = self.jointText(new_txt, mm.txt, loc)
            is_changed = (old_txt != new_txt)
            if is_changed:
                return new_txt
            else:
                return None

        new_txt = lowercaseByChosenPattern(df.GA_REF_PART)
        self.refreshUsingNewText(new_txt)

        new_txt = lowercaseByChosenPattern(df.ALL_WORDS_SHOULD_BE_LOWER)
        self.refreshUsingNewText(new_txt)
        return self.getText()

    def isSentence(self):
        is_first_title = (self.case_list[0] == CaseAction.TITLE)

        has_remainder = (len(self.case_list) > 1)
        is_remainder_lower = (has_remainder) \
                             and not bool(list(filter(lambda x: x is not CaseAction.LOWER, self.case_list[1:])))
        is_sentence = (is_first_title and is_remainder_lower)
        return is_sentence

    def isAllUpper(self):
        is_all_upper = not bool(list(filter(lambda x: x is not CaseAction.UPPER, self.case_list)))
        return is_all_upper

    def isAllLower(self):
        is_all_lower = not bool(list(filter(lambda x: x is not CaseAction.LOWER, self.case_list)))
        return is_all_lower

    def isAllTitle(self):
        is_all_title = not bool(list(filter(lambda x: x is CaseAction.LOWER or x is CaseAction.UPPER, self.case_list)))
        return is_all_title

    def caseValueStringToPercentages(self, case_value_string: str):
        '''
        Runs through the case_value_string (ie. '2333312332223333' etc..)
        then produce the percentage of length, plus the location where it happens,
        so later, these perentages, in sequence, can be applied to a new string, regardless of its length
        thus appearing to MIRROR the range of CASE. This is a BEST GUESS, cannot be ACCURATE.
        '''
        def find_case_action_match(case_pattern_entry):
            list_of_actions = []
            mm: MatcherRecord = None
            (pattern, case_action_required) = case_pattern_entry
            match_dict = pu.patternMatchAll(pattern, case_value_string)
            for (loc, mm) in match_dict.items():
                percent = len(mm.txt) / len(case_value_string)
                entry = (loc, percent, pattern, case_action_required)
                list_of_actions.append(entry)
            return list_of_actions

        # very likely this list will contain sub-lists for each case, each group
        list_of_match_percentages = list(map(find_case_action_match, CaseActionList.list_of_patterns))

        # remove sub-lists for each case
        overall_list_of_match_percentages = list(chain.from_iterable(list_of_match_percentages))

        # sort by locations, so it lies with the same natural order of case_records in case_list
        overall_list_of_match_percentages.sort()
        return overall_list_of_match_percentages

    def percentToRangeOfIndexAndAction(self, list_of_percentages, target_str: str):

        target_str_cal = CaseActionList.makeInstance(target_str)

        list_of_case_action = []
        number_of_words = len(target_str_cal.case_list)
        start_index = end_index = 1
        for entry in list_of_percentages:
            (loc, percent, pattern, case_action_required) = entry
            affect_length = percent * number_of_words

            end_index = min(start_index + int(math.floor(affect_length)), number_of_words)
            valid = (start_index <= end_index) and (start_index <= number_of_words) and (end_index <= number_of_words)
            if not valid:
                continue

            entry = (start_index-1, end_index-1, case_action_required)
            list_of_case_action.append(entry)
            start_index = min(end_index + 1, number_of_words)
        return (list_of_case_action, target_str_cal)

    def getText(self, action_to_perform = None):
        def case_record_to_sortable_entry(case_rec: CaseRecord):
            loc = (case_rec.s, case_rec.e)
            return (loc, case_rec)

        new_txt = str(self.txt)
        case_record: CaseRecord = None
        sortable_list = list(map(case_record_to_sortable_entry, self.case_list))
        sortable_list.sort(reverse=True)

        for loc, case_record in sortable_list:
            if action_to_perform:
                action_to_perform(case_record)
            txt = case_record.txt
            new_txt = self.jointText(new_txt, txt, loc)
        return new_txt

    def transformBasedOnCaseValueString(self, target_str: str) -> str:
        list_of_match_percentages = self.caseValueStringToPercentages(self.case_value_string)
        (list_of_case_action, target_cal) = self.percentToRangeOfIndexAndAction(list_of_match_percentages, target_str)
        for index, (start_index, end_index, case_action_required) in enumerate(list_of_case_action):
            for i in range(start_index, end_index+1):
                case_record: CaseRecord = target_cal.case_list[i]
                case_record.transformText(case_action_required)
                # print(case_record.txt)
        return (target_cal.getText(), target_cal)

    @classmethod
    def genListOfDistance(self, max):
        dist_list = []
        for s in range(0, max):
            for e in range(0, max):
                is_valid = (s < e)
                if not is_valid:
                    continue

                distance = (e - s)
                # entry = (distance, s, e)
                entry = (s, e)
                if entry not in dist_list:
                    dist_list.append(entry)
        dist_list.sort()
        return dist_list

    def isSameBeginAndEnd(self, other):
        this_string = self.getText()
        other_string = other.getText()
        left_from, mid_from, right_from = self.getTextWithin(this_string)
        left_to, mid_to, right_to = self.getTextWithin(other_string)
        is_equal = (left_from == left_to) and (right_from == right_to)
        return is_equal

    def enforceBeginAndEnd(self, other):
        this_string = self.getText()
        other_string = other.getText()
        left_from, mid_from, right_from = self.getTextWithin(this_string)
        left_to, mid_to, right_to = self.getTextWithin(other_string)

        is_equal = (left_from == left_to) and (right_from == right_to)
        if is_equal:
            return False

        new_this_string = (left_to + mid_from + right_to)
        new_case_action = CaseActionList.makeInstance(new_this_string)
        self.clone(new_case_action)
        return True

    def enforceFirstWordCase(self, other):
        try:
            first_this_record: CaseRecord = self.case_list[0]
            first_other_record: CaseRecord = other.case_list[0]
            first_this_record.transformText(first_other_record.case)
            self.refresh()
            return True
        except Exception as e:
            return False

    def getListOfCases(self):
        x: CaseRecord = None
        case_list = [x.case for x in self.case_list]
        return case_list


    @classmethod
    def matchCase(self, from_str: str, to_str: str):
        valid = bool(from_str.strip()) and bool(to_str.strip())
        if not valid:
            return to_str

        cal_from = CaseActionList.makeInstance(from_str)
        cal_to = CaseActionList.makeInstance(to_str)

        is_same = cal_from.isConsideringTheSame(cal_to)
        if is_same:
            # df.LOG(f'[{from_str}] [{to_str}]: is_same: {is_same}')
            return to_str

        if cal_from.isSetenceCase():
            cal_to.toSentenceCase()
        if cal_from.isAllTheSameCase(CaseAction.TITLE):
            cal_to.allToACase(CaseAction.TITLE)
        if cal_from.isAllTheSameCase(CaseAction.LOWER):
            cal_to.allToACase(CaseAction.LOWER)
        if cal_from.isAllTheSameCase(CaseAction.UPPER):
            cal_to.allToACase(CaseAction.UPPER)

        cal_to.enforceFirstWordCase(cal_from)
        cal_to.enforceLegalLowercase(cal_from)
        cal_to.enforceBeginAndEnd(cal_from)
        cal_to.copyRepeatedWordsOver(cal_from)
        cal_to.enforceBeginAndEnd(cal_from)

        return cal_to.getText()

        (new_to_txt, cal_to) = cal_from.transformBasedOnCaseValueString(to_str)

        changed = cal_from.fixSpecialCases(cal_to)
        if changed:
            new_to_txt = cal_to.getText()

        first_word_from_record: CaseRecord = cal_from.case_list[0]
        first_word_from_case = first_word_from_record.case
        result_txt = cal_from.enforceLegalLowercase(new_to_txt, first_word_case=first_word_from_case)
        final_txt = cal_from.enforceBeginAndEnd(from_str, result_txt)
        return final_txt
        # mirror case based on the rise and fall of the case values,
        # working out the range from root, mirror the range to target, by stretching and scaling to match

    def getNoneAlphaPart(self, msg: str, is_start=True):
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

    def getTextWithinWithDiffLoc(self, msg:str, to_matcher_record=False):
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

    def getTextWithin(self, msg: str):
        diff_loc, left, mid, right, _ = self.getTextWithinWithDiffLoc(msg)
        return left, mid, right
