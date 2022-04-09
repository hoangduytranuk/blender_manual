import math
import re
from enum import Enum
from definition import Definitions as df, RefType
# from fuzzywuzzy_src.build.fuzzywuzzy import fuzz
from fuzzywuzzy import fuzz
from pattern_utils import PatternUtils as pu
from matcher import MatcherRecord
from observer import LocationObserver
from itertools import chain
from get_text_within import GetTextWithin
from functools import reduce
from bracket import RefAndBracketsParser as PSER
from collections import OrderedDict, defaultdict


def jointText(orig: str, tran: str, loc: tuple):
    if not bool(tran):
        return orig

    s, e = loc
    left = orig[:s]
    right = orig[e:]
    new_str = left + tran + right
    return new_str


def removeText(orig: str, loc: tuple):
    s, e = loc
    left = orig[:s]
    right = orig[e:]
    new_str = left + right
    return new_str


class CaseAction(Enum):
    NONE = 0
    UPPER = 1
    TITLE = 2
    LOWER = 3
    SENTENCE = 4 # first Upper, then all lower
    MIXED = 5
    WITHOUT_UPPER = 6
    WITHOUT_TITLE = 7
    WITHOUT_LOWER = 8
    WITHOUT_MIXED = 9
    ORIGINAL = 10

    @classmethod
    def getMember(self, string_value: str):
        def compare(entry):
            (name, member) = entry
            is_found = (str(member.value) == string_value)
            return is_found

        if not hasattr(self, 'member_list'):
            member_list = [(name, member) for (name, member) in self.__members__.items()]
            setattr(self, 'member_list', member_list)

        found_list = list(filter(compare, self.member_list))
        if found_list:
            return found_list[0][1]
        else:
            return None

class CaseRecord(list):
    def __init__(self, txt: str,
                 matcher_record: MatcherRecord = None,
                 case_type: CaseAction = CaseAction.NONE,
                 ref_type: RefType = RefType.TEXT
                 ):

        self.case: CaseAction = case_type
        if bool(matcher_record):
            self.ref_type = matcher_record.type
            self.txt = matcher_record.txt
            self.s = matcher_record.s
            self.e = matcher_record.e
        else:
            self.ref_type: CaseAction = ref_type
            self.txt = txt
            self.s = -1
            self.e = -1


    def __repr__(self):
        string = ""
        try:
            string = f'\nloc:{(self.s, self.e)}'
            string += '\n----CaseRecord start------'
            string += "\nCaseRecord:\n{!r}".format(self.__dict__)
            string += '\n----CaseRecord end------\n'
        except Exception as e:
            pass
        return string

    @classmethod
    def loc(cls):
        return (cls.s, cls.e)

    @classmethod
    def setLoc(cls, new_loc):
        (cls.s, cls.e) = new_loc

    def transformText(self, case_required: CaseAction, preserve_case=None):
        new_txt: str = self.txt
        current_case = self.case
        is_preserved = (bool(preserve_case) and current_case == preserve_case)
        if is_preserved:
            return

        if case_required == CaseAction.TITLE:
            new_txt = new_txt.title()
            self.case = case_required
        elif case_required == CaseAction.UPPER:
            new_txt = new_txt.upper()
            self.case = case_required
        elif case_required == CaseAction.LOWER:
            new_txt = new_txt.lower()
            self.case = case_required
        self.txt = new_txt

class CaseActionList:

    ignoreable = ['-', '+', '%']
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
        self.case_value = -1
        self.ref_list: PSER = None
        self.prefixed_case_type_dict = {}

    def __repr__(self):
        string = ""
        try:
            string = '\n----CaseActionList start------\n'
            string += "\nCaseActionList:\n{!r}".format(self.__dict__)
            string += '\n----CaseActionList end------\n'
        except Exception as e:
            pass
        return string

    def caseValue(self):
        return int(self.case_value_string)

    @classmethod
    def getCaseRecordWords(self, case_record_list):
        case_record: CaseRecord = None
        word_list = [case_record.txt for case_record in case_record_list]
        return word_list

    def putCaseRecordWords(self, new_word_list: list):
        def function_put_word(new_word: str, current_case_record: CaseRecord):
            current_case_record.txt = new_word
            return current_case_record

        has_same_length = len(new_word_list) == len(self.case_list)
        if not has_same_length:
            report_msg = f'putCaseRecordWords() Replacing word list MUST have the same length as the local case_list'
            raise RuntimeError(report_msg)

        case_record: CaseRecord = None
        done_list = list(map(function_put_word, new_word_list, self.case_list))
        return done_list

    def refresh(self):
        current_string = self.getText()
        is_same = (self.txt == current_string)
        if not is_same:
            other = CaseActionList.makeInstance(current_string)
            self.clone(other)

    def clone(self, other):
        self.loc = other.loc
        self.txt = other.txt
        self.case_converted_txt = other.case_converted_txt
        self.case_list = other.case_list
        self.case_value_string = other.case_value_string

    def refreshUsingNewText(self, txt: str):
        if not bool(txt):
            return

        other = CaseActionList.makeInstance(txt)
        self.clone(other)

    @classmethod
    def reproduce(cls):
        return cls()

    def isConsideringTheSame(self, other):
        is_same_begin_and_end = self.isSameBeginAndEnd(other)
        if not is_same_begin_and_end:
            return False

        this_string: str = self.case_value_string
        other_string: str = other.case_value_string
        is_same = (this_string == other_string)
        if is_same:
            return True

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

    def toListOfCaseRecord(self, s1: str, origin_loc=None, original_for_removal=None) -> CaseAction:
        def getWordsCase(entry):
            loc: tuple(int, int) = entry[0]
            mm: MatcherRecord = entry[1]

            is_numeric = mm.txt.isnumeric()
            is_upper = mm.txt.isupper()
            is_lower = mm.txt.islower()
            is_title = mm.txt.istitle()
            case_act = CaseAction.NONE
            if is_numeric:
                case_act = CaseAction.LOWER
            elif is_upper:
                case_act = CaseAction.UPPER
            elif is_title:
                case_act = CaseAction.TITLE
            elif is_lower:
                case_act = CaseAction.LOWER

            case_rec = CaseRecord(mm.txt, matcher_record=mm, case_type=case_act)
            return case_rec

        def getCaseValue(case_record: CaseRecord):
            return str(case_record.case.value)

        def parsingRefs(entry):
            orig_txt = parsingRefs.orig_txt
            loc: tuple(int, int) = entry[0]
            mm: MatcherRecord = entry[1]
            txt_loc = loc
            word_list_without_symbols = pu.patternMatchAll(df.CHARACTERS, orig_txt, ref_type=type, loc=txt_loc, using_origin_loc=origin_loc)
            has_word_list = (len(word_list_without_symbols) > 0)
            if not has_word_list:
                return []
            case_list = list(map(getWordsCase, word_list_without_symbols.items()))
            return case_list

        def getCaseListExcluded(entry):
            key_case_action = entry[0]
            excluded_case_action = entry[1]

            def exclude_case_action(case_record: CaseRecord):
                is_excluded = (case_record.case == excluded_case_action)
                return not is_excluded

            excluded_list = list(filter(exclude_case_action, self.case_list))
            valid = len(excluded_list) > 0
            if not valid:
                return (key_case_action, None)

            case_action_excluded_list = [case_record.case for case_record in excluded_list]
            return (key_case_action, case_action_excluded_list)

        def composePrefixCaseDict(length):
            case_all_list = [case_record.case for case_record in self.case_list]
            original_case_entry = [(CaseAction.ORIGINAL, case_all_list)]
            dict_of_cases = OrderedDict(original_case_entry)

            exluded_action_list = [
                (CaseAction.WITHOUT_UPPER, CaseAction.UPPER),
                (CaseAction.WITHOUT_MIXED, CaseAction.MIXED)
            ]
            excluded_list = list(map(getCaseListExcluded, exluded_action_list))
            accepted_list = [(key, cal) for (key, cal) in excluded_list if bool(cal)]
            exc_dict_of_cases = OrderedDict(accepted_list)
            dict_of_cases.update(exc_dict_of_cases)
            return dict_of_cases

        ref_list = PSER(s1, original_for_removal=original_for_removal)
        is_debug = (len(ref_list) > 0)
        if is_debug:
            is_debug = True

        ref_list.parseMessage(is_ref_only=True, pattern_list=df.pattern_list_complex)
        obs = ref_list.local_obs
        text_dict = obs.getUnmarkedPartsAsDict(reversing=False)

        parsingRefs.orig_txt = s1
        case_list_of_list = list(map(parsingRefs, text_dict.items()))
        case_list = [x for y in case_list_of_list for x in y]
        has_case_list = (len(case_list) > 0)
        if not has_case_list:
            return
        # # word_list = pu.patternMatchAll(df.CHARACTERS, s1)
        # # case_value_list = list(map(getWordsCase, word_list.items()))
        # case_value_list = list(map(getWordsCase, word_list.items()))
        case_value_string_list = list(map(getCaseValue, case_list))

        case_value_string = ''.join(case_value_string_list)
        case_value = int(case_value_string)
        self.case_list = case_list
        self.case_value_string = case_value_string
        self.case_value = case_value
        self.prefixed_case_type_dict = composePrefixCaseDict(len(self.case_list))

    def toSentenceCase(self, cal_from, preserve_case=None):
        def transform(index, case_record):

            is_first = (index == 0)
            if is_first:
                case_record.transformText(CaseAction.TITLE, preserve_case=preserve_case)
            else:
                case_record.transformText(CaseAction.LOWER, preserve_case=preserve_case)
            return case_record

        index_list = list(range(0, len(self.case_list)))
        transformed_list = list(map(transform, index_list, self.case_list))
        return transformed_list

    def allToACase(self, chosen_case: CaseAction, preserve_case=None):
        case_record: CaseRecord = None
        for case_record in self.case_list:
            case_record.transformText(chosen_case, preserve_case=preserve_case)

    @classmethod
    def replaceRepeatedText(self, repeated_text: str, target_txt: str):
        replaced_part = f'({repeated_text})'
        replaced_part_lower = replaced_part.lower()
        target_txt_lower = target_txt.lower()

        has_replaced_part = (replaced_part_lower in target_txt_lower)
        if not has_replaced_part:
            return target_txt

        new_txt = str(target_txt)
        index = target_txt_lower.find(replaced_part_lower)
        loc = (index, index + len(replaced_part))
        new_txt = jointText(new_txt, replaced_part, loc)
        return new_txt

    def copyRepeatedWordsOver(self, from_cal):
        def pairingRecords(from_case_record: CaseRecord):
            last_index = pairingRecords.last_index[0]
            max_index = pairingRecords.max_index
            this_word_list = self.case_list[last_index:]
            this_case_record: CaseRecord = None
            for index, this_case_record in enumerate(this_word_list):
                this_txt = this_case_record.txt
                from_txt = from_case_record.txt
                this_txt_lower = this_txt.lower()
                from_txt_lower = from_txt.lower()

                is_same_case_sensitive = (this_txt == from_txt)
                is_same_case_insensitive = (this_txt_lower == from_txt_lower)
                is_need_swap = is_same_case_insensitive and (not is_same_case_sensitive)
                if not is_need_swap:
                    continue

                this_case_record.txt = from_case_record.txt

                next_index = min(last_index + index + 1, max_index)
                pairingRecords.last_index.clear()
                pairingRecords.last_index.append(next_index)
                return (this_case_record, from_case_record)
            else:
                return (None, None)

        def sortListByLoc(mm: MatcherRecord):
            return mm.s

        try:
            pairingRecords.last_index = [0]
            pairingRecords.max_index = len(self.case_list)
            pair_list = list(map(pairingRecords, from_cal.case_list))
            replaced_list = [(from_mm, this_mm) for (from_mm, this_mm) in pair_list if (from_mm is not None) and (this_mm is not None)]
            has_changed = len(replaced_list) > 0
            return has_changed
        except Exception as e:
            msg = f'cal_from:{from_cal.txt}\ncal_to:{self.txt}\nexception:{e}'
            df.LOG(msg)
            return False

    def caseValueStr(self, case_list:list):
        try:
            s1_value_as_str_list = ''.join([str(x.value) for x in case_list])
            return s1_value_as_str_list
        except Exception as e:
            return []

    @classmethod
    def makeInstance(self, s1: str, using_origin_loc=None, original_for_removal=None):
        cal = self.reproduce()
        cal.txt = s1
        cal.toListOfCaseRecord(s1, origin_loc=using_origin_loc, original_for_removal=original_for_removal)
        return cal

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
            new_txt = jointText(new_txt, new_word, loc)
        return new_txt

    def caseWeight(self, other):
        s1_value_as_str_list = self.case_value_string
        s2_value_as_str_list = other.case_value_string
        diff_ratio = fuzz.partial_ratio(s1_value_as_str_list, s2_value_as_str_list)
        return diff_ratio

    def enforceLegalLowercase(self, from_case_action_list):
        def isWordPartOfAnExpression(avoid_lower_term: str, current_word: str, current_word_index: int):
            current_word_lower = current_word.lower()
            is_possible = (current_word_lower in avoid_lower_term)
            if not is_possible:
                return False

            avoid_lower_term_word_list = avoid_lower_term.split()
            avoid_lower_term_len = len(avoid_lower_term_word_list)
            try:
                prev_part_list = word_list[current_word_index - avoid_lower_term_len + 1: current_word_index + 1]
                prev_part = ' '.join(prev_part_list)
                prev_part = prev_part.lower()
                is_avoid = (prev_part == avoid_lower_term)
                if is_avoid:
                    return True
            except Exception as e:
                prev_part = None

            try:
                next_part_list = word_list[current_word_index: current_word_index + avoid_lower_term_len]
                next_part = ' '.join(next_part_list)
                next_part = next_part.lower()
                is_avoid = (next_part == avoid_lower_term)
                if is_avoid:
                    return True
            except Exception as e:
                next_part = None
            return False

        def toLowerCase(index: int, case_record:CaseRecord):
            pattern_check: re.Pattern = toLowerCase.pattern_check

            is_first = (case_record.s == 0)
            txt = case_record.txt

            # is_debug_list = ['đối', 'với']
            # is_debug = (txt.lower() in is_debug_list)
            # if is_debug:
            #     is_debug = True

            match = pattern_check.search(txt)
            is_lowerable = (match is not None)
            if not is_lowerable:
                return case_record

            is_forbid = False
            for avoid_term in df.words_should_avoid_forced_lower_list:
                is_avoid = isWordPartOfAnExpression(avoid_term, txt, index)
                if is_avoid:
                    is_forbid = True
                    break

            can_lower = not (is_first or is_forbid)
            if can_lower:
                case_record.txt = txt.lower()
                return case_record
            else:
                return None

        def lowercaseByChosenPattern(pattern: re.Pattern):
            index_range = list(range(0, len(self.case_list)))
            toLowerCase.pattern_check = pattern
            result_list = list(map(toLowerCase, index_range, self.case_list))
            return result_list

        def lowercaseByExpression(pattern: re.Pattern):
            def toLower(entry):
                loc = entry[0]
                mm: MatcherRecord = entry[1]
                mm.translation = mm.txt.lower()
                return entry

            current_txt = ' '.join(word_list)
            match_dict = pu.patternMatchAll(df.ALL_PHRASES_SHOULD_BE_LOWER, current_txt)
            has_phrases = len(match_dict) > 0
            if not has_phrases:
                return False

            lowered_list = list(map(toLower, match_dict.items()))
            lowered_list.sort(reverse=True)
            new_txt = str(current_txt)
            for (loc, mm) in lowered_list:
                lower_txt = mm.translation
                new_txt = jointText(new_txt, lower_txt, loc)
            new_word_list = new_txt.split()
            self.putCaseRecordWords(new_word_list)
            return True

        word_list = CaseActionList.getCaseRecordWords(self.case_list)
        result_list = lowercaseByChosenPattern(df.ALL_WORDS_SHOULD_BE_LOWER)
        filter_done_list = [case_record for case_record in result_list if (case_record is not None)]
        has_changed = len(filter_done_list) > 0

        lowercaseByExpression(df.ALL_PHRASES_SHOULD_BE_LOWER)

        return has_changed

    def isSentence(self):
        def checkIfItIsSentence(list_of_cases):
            is_one_word = (len(list_of_cases) < 2)
            is_first_case_title = False
            is_all_rest_lower = False
            try:
                first_case = list_of_cases[0]
                is_first_case_title = (first_case == CaseAction.TITLE)
                rest_case = list_of_cases[1:]
                lower_rest = [(case == CaseAction.LOWER) for case in rest_case]
                is_all_rest_lower = not (False in lower_rest)
            except Exception as e:
                pass
            if is_one_word:
                is_sentence = False
            else:
                is_sentence = (is_first_case_title and is_all_rest_lower)
            return is_sentence

        orig = self.prefixed_case_type_dict[CaseAction.ORIGINAL]
        is_sentence = checkIfItIsSentence(orig)
        if not is_sentence:
            has_key = (CaseAction.WITHOUT_UPPER in self.prefixed_case_type_dict)
            if not has_key:
                is_sentence = False
            else:
                no_upper_list = self.prefixed_case_type_dict[CaseAction.WITHOUT_UPPER]
                is_sentence = checkIfItIsSentence(no_upper_list)
        return is_sentence

    def isAllUpper(self):
        orig = self.prefixed_case_type_dict[CaseAction.ORIGINAL]
        boolean_list = [(case == CaseAction.UPPER) for case in orig]
        is_all_upper = not (False in boolean_list)
        return is_all_upper

    def isAllLower(self):
        orig = self.prefixed_case_type_dict[CaseAction.ORIGINAL]
        boolean_list = [(case == CaseAction.LOWER) for case in orig]
        is_all_lower = not (False in boolean_list)
        return is_all_lower

    def isAllTitle(self):
        orig = self.prefixed_case_type_dict[CaseAction.ORIGINAL]
        boolean_list = [(case == CaseAction.TITLE) for case in orig]
        is_all_title = not (False in boolean_list)
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
        def sortCaseList(case_rec: CaseRecord):
            loc = (case_rec.s, case_rec.e)
            return (loc)

        has_case_list = bool(self.case_list) and len(self.case_list) > 0
        if not has_case_list:
            return self.txt

        new_txt = str(self.txt)
        case_record: CaseRecord = None
        reverse_case_list= sorted(self.case_list, key=sortCaseList, reverse=True)

        for case_record in reverse_case_list:
            if action_to_perform:
                action_to_perform(case_record)
            txt = case_record.txt
            loc = (case_record.s, case_record.e)
            new_txt = jointText(new_txt, txt, loc)
        is_valid = (new_txt.lower() == self.txt.lower())
        if not is_valid:
            msg = f'getText() self.txt:{self.txt}\nnew_txt:{new_txt}\n\n'
            raise RuntimeError(f'ERROR replacing text!\n{msg}')
        else:
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

        left_from, mid_from, right_from = self.getInputMargins(this_string)
        left_to, mid_to, right_to = other.getInputMargins(other_string)
        is_equal = (left_from == left_to) and (right_from == right_to)
        return is_equal

    def getInputMargins(self, input_msg: str):
        input_ref_list = PSER(input_msg)
        input_ref_list.parseMessage(is_ref_only=True)
        input_obs = LocationObserver(input_msg)
        input_loc_list = [loc for (loc, mm) in input_ref_list.items()]
        input_obs.markLocListAsUsed(input_loc_list)

        left_input = input_obs.getLeft()
        right_input = input_obs.getRight()
        (mid_loc, mid) = input_obs.getMid()
        is_same = (left_input == right_input == mid)
        if is_same:
            left_input = ""
            right_input = ""

        return left_input, mid, right_input

    def enforceBeginAndEnd(self, other):
        this_string = self.getText()
        other_string = other.getText()

        left_from, mid_from, right_from = other.getInputMargins(other_string)
        left_to, mid_to, right_to = self.getInputMargins(this_string)
        is_equal = (left_from == left_to) and (right_from == right_to)
        if is_equal:
            return False

        can_ignore = (bool(left_from) and left_from[0] in CaseActionList.ignoreable)
        if can_ignore:
            return False

        new_this_string = f'{left_from}{mid_to}{right_from}'
        new_case_action = CaseActionList.makeInstance(new_this_string)
        self.clone(new_case_action)
        return True

    def enforceFirstWordCase(self, other):
        try:
            first_this_record: CaseRecord = self.case_list[0]
            if other:
                first_other_record: CaseRecord = other.case_list[0]
                other_case = first_other_record.case
            else:
                other_case = CaseAction.TITLE

            is_upper = (other_case == CaseAction.UPPER) or (other_case == CaseAction.TITLE)
            is_set_title = (is_upper and first_this_record.case == CaseAction.LOWER)

            if is_set_title:
                first_this_record.transformText(CaseAction.TITLE)
            else:
                first_this_record.transformText(other_case)
            self.refresh()
            return True
        except Exception as e:
            return False

    def getListOfCases(self):
        x: CaseRecord = None
        case_list = [x.case for x in self.case_list]
        return case_list

    def fix_abbr(self, cal_from):
        msgid = cal_from.getText
        msgstr = m.string

        strip_symbs = '"\'*'
        found_dict = pu.patternMatchAll(df.GA_REF_PART, msgstr)
        is_found = bool(found_dict)
        if not is_found:
            return
            is_debug = ('--app-template' in msgid)
            if is_debug:
                is_debug = True

            valid_ending = False
            mm: MatcherRecord = None
            (loc, mm) = list(found_dict.items())[0]
            print(f'{loc}\n{mm.getSubEntriesAsList()}\n\n')
            sub_entry_list = mm.getSubEntriesAsList()
            ending_loc = None
            ending = None
            sub_entry_len = len(sub_entry_list)
            if sub_entry_len == 4:
                o_loc, orig = sub_entry_list[0]
                mis_entry_loc, mis_entry = sub_entry_list[1]
                abbrev_loc, abbrev = sub_entry_list[2]
                expl_loc, expl = sub_entry_list[3]
                chosen_loc = mis_entry_loc
            elif sub_entry_len == 5:
                o_loc, orig = sub_entry_list[0]
                start_loc, start_char = sub_entry_list[1]
                is_start = (len(start_char) == 1)
                if is_start:
                    mis_entry_loc, mis_entry = sub_entry_list[2]
                    abbrev_loc, abbrev = sub_entry_list[3]
                    expl_loc, expl = sub_entry_list[4]
                    chosen_loc = mis_entry_loc
                else:
                    mis_entry_loc, mis_entry = sub_entry_list[1]
                    abbrev_loc, abbrev = sub_entry_list[2]
                    expl_loc, expl = sub_entry_list[3]
                    ending_loc, ending = sub_entry_list[4]
                    chosen_loc = mis_entry_loc
                    valid_ending = ending.startswith(')`')
            elif sub_entry_len == 6:
                o_loc, orig = sub_entry_list[0]
                s_loc, starter = sub_entry_list[1]
                mis_entry_loc, mis_entry = sub_entry_list[2]
                abbrev_loc, abbrev = sub_entry_list[3]
                expl_loc, expl = sub_entry_list[4]
                ending_loc, ending = sub_entry_list[5]
                chosen_loc = o_loc
                valid_ending = ending.startswith(')`')

            abbrev = abbrev.strip(strip_symbs)
            expl = expl.strip(strip_symbs)
            if valid_ending:
                recon = f':abbr:`{abbrev} ({expl}{ending}'
            else:
                recon = f':abbr:`{abbrev} ({expl})`'
            recon = recon.replace(f'({abbrev}', '')

            # print(f'{loc}: [{orig}]=>[{recon}]')
            (ls, le) = loc
            is_start = (ls == 0)
            if not is_start:
                is_leading_with_a_space = (msgstr[ls-1] == ' ')
                if not is_leading_with_a_space:
                    recon = f' {recon}'

            new_msgstr = cm.jointText(msgstr, recon, loc)
            new_msgstr = new_msgstr.replace(':abbr:`abbr:`', ':abbr:`')
            new_msgstr = new_msgstr.replace('- :abbr:`', ':abbr:`')

            m.string = new_msgstr
            changed = True
            print(f'[{msgid}]\n[{msgstr}]\nNEW:[{new_msgstr}]\n******************\n\n')

    def breakUpSentenceAndCase(self, cal_from):
        def title_first(cal: CaseActionList):
            case_list = cal.case_list
            has_case_list = (bool(case_list) and len(case_list) > 0)
            if not has_case_list:
                return cal

            first_case_record: CaseRecord = case_list[0]
            first_case_record.transformText(CaseAction.TITLE)
            cal.refresh()
            return cal

        def makeCaseActionList(entry):
            loc = entry[0]
            mm: MatcherRecord = entry[1]
            txt = mm.txt
            cal = self.makeInstance(txt)
            return cal

        def extractEndLocLocation(loc):
            (x, y) = loc
            return (y, y+1)

        full_stop_pat_txt = r'(?=\S)(\.)(?=(\s|$))'
        FULL_STOP = re.compile(full_stop_pat_txt)

        orig_txt = self.getText()
        working_txt = str(orig_txt)

        temp_sentence_dict = pu.patternMatchAll(FULL_STOP, working_txt)
        has_sentences = len(temp_sentence_dict) > 0
        if not has_sentences:
            return

        loc_list = list(temp_sentence_dict.keys())
        actual_loc_list=list(map(extractEndLocLocation, loc_list))
        obs = LocationObserver(orig_txt)
        obs.markLocListAsUsed(actual_loc_list)
        sentence_dict = obs.getUnmarkedPartsAsDict(reversing=False)

        list_of_cals_for_all_sentences = list(map(makeCaseActionList, sentence_dict.items()))
        list_of_first_uppercased_cals = list(map(title_first, list_of_cals_for_all_sentences))
        overall_text_list = [cal.getText() for cal in list_of_first_uppercased_cals]
        new_txt = ' '.join(overall_text_list)
        new_cal = self.makeInstance(new_txt)
        self.clone(new_cal)

    def toCaseOf(self, from_cal):
        def isMatching(letter: str):
            target_action:CaseAction = isMatching.target
            value_str = str(target_action.value)
            return (letter == value_str)

        def calcFrequency(case_action: CaseAction):
            isMatching.target = case_action
            freq_list = list(filter(isMatching, fr_case_string))
            return len(freq_list)

        def transposeCase(case_rec: CaseRecord, case_action_value: str):
            the_case: CaseAction = CaseAction.getMember(case_action_value)
            case_rec.transformText(the_case)
            return case_rec

        def sortByCount(entry):
            (count, case_action) = entry
            return count

        fr_case_string = from_cal.case_value_string
        upper_cnt = calcFrequency(CaseAction.UPPER)
        lower_cnt = calcFrequency(CaseAction.LOWER)
        title_cnt = calcFrequency(CaseAction.TITLE)
        mixed_cnt = calcFrequency(CaseAction.MIXED)
        count_list = [
            (upper_cnt, CaseAction.UPPER),
            (lower_cnt, CaseAction.LOWER),
            (title_cnt, CaseAction.TITLE),
            (mixed_cnt, CaseAction.MIXED),
            ]
        count_list.sort(key=sortByCount, reverse=True)
        major_case = count_list[0]
        (count, majority_case) = major_case

        transposed_list = list(map(transposeCase, self.case_list, fr_case_string))
        new_txt = self.getText()
        return new_txt

    @classmethod
    def matchCase(self, from_str: str, to_str: str, matching_from_begin_end=False):
        class TrimRecord:
            def __init__(self, to_string, memorise_cutoff=False):
                self.removed_location = -1
                self.is_trimmed = False
                self.new_string = to_string
                self.to_string_lower = None
                self.memorise_cutoff = memorise_cutoff
                self.list_of_upper_case_words: dict = None

            def trimOffRepeated(self):
                from_part = f'{(from_str)}'
                from_part_lower = from_part.lower()
                self.to_string_lower = to_str.lower()

                from_part_index = (self.to_string_lower.find(from_part_lower))
                from_part_len = len(from_part)
                to_part_index = from_part_index + from_part_len

                is_trimmed = False
                is_removed_original = (from_part_index >= 0)
                if is_removed_original:
                    left_part = to_str[:from_part_index]
                    right_part = to_str[to_part_index:]
                    self.new_string = (left_part + right_part)
                    self.is_trimmed = True
                    self.removed_location = (from_part_index, to_part_index)

                return self.new_string

            def removeUpperCaseWords(self, txt: str):
                upper_case_dict = pu.patternMatchAll(df.UPPER_CASE_WORDS, txt)
                has_upper_words = (len(upper_case_dict) > 0)
                if not has_upper_words:
                    return txt

                upper_case_loc = list(upper_case_dict.keys())
                new_txt = str(txt)
                for loc in upper_case_loc:
                    new_txt = removeText(new_txt, loc)
                return new_txt

            def rejoinTrimmedString(self):
                new_txt = self.new_string
                from_part_index = self.removed_location[0]
                left = new_txt[:from_part_index]
                right = new_txt[from_part_index:]
                new_txt = (left + from_str + right)

                is_same = (new_txt.lower() == self.to_string_lower)
                if not is_same:
                    report_msg = f'Function matchCase() DO NOT work correctly:\nold:{to_str}\nnew:{new_txt}'
                    raise RuntimeError(report_msg)
                return new_txt

        # from_str = "Rules of thumb for choosing an SRID"
        # to_str = "Quy luật thông thường để lựa chọn một SRID (Rules of thumb for choosing an SRID)"
        # from_str = "Scene Animation for Preview Images"
        # to_str = "Hoạt Họa Cảnh đối với các Hình Ảnh Duyệt Thảo (Scene Animation for Preview Images)"

        valid = bool(from_str.strip()) and bool(to_str.strip())
        if not valid:
            return to_str

        ignore_starter = '@{'
        is_ignore = from_str.startswith(ignore_starter)
        if is_ignore:
            return to_str

        cal_from = CaseActionList.makeInstance(from_str)
        has_cal_from = bool(cal_from.case_list)
        if not has_cal_from:
            return to_str

        cal_to = CaseActionList.makeInstance(to_str, original_for_removal=from_str)
        debub_txt = self.getCaseRecordWords(cal_to.case_list)
        has_cal_to = bool(cal_to.case_list)
        if not has_cal_to:
            return to_str

        if cal_from.isSentence():
            cal_to.toSentenceCase(cal_from, preserve_case=CaseAction.UPPER)
        elif cal_from.isAllTitle():
            cal_to.allToACase(CaseAction.TITLE, preserve_case=CaseAction.UPPER)
        elif cal_from.isAllLower():
            cal_to.allToACase(CaseAction.LOWER, preserve_case=CaseAction.UPPER)
        else:
            cal_to.allToACase(CaseAction.TITLE, preserve_case=CaseAction.UPPER)

        debub_txt = self.getCaseRecordWords(cal_to.case_list)
        current_txt = cal_to.getText()

        cal_to.enforceLegalLowercase(cal_from)
        debub_txt = self.getCaseRecordWords(cal_to.case_list)
        current_txt = cal_to.getText()
        cal_to.copyRepeatedWordsOver(cal_from)
        debub_txt = self.getCaseRecordWords(cal_to.case_list)
        current_txt = cal_to.getText()
        cal_to.breakUpSentenceAndCase(cal_from)
        debub_txt = self.getCaseRecordWords(cal_to.case_list)
        current_txt = cal_to.getText()
        if matching_from_begin_end:
            cal_to.enforceBeginAndEnd(cal_from)
            debub_txt = self.getCaseRecordWords(cal_to.case_list)
            current_txt = cal_to.getText()

        from_txt = cal_from.getText()
        new_txt = cal_to.getText()
        changed_txt = CaseActionList.replaceRepeatedText(from_txt, new_txt)
        return changed_txt


