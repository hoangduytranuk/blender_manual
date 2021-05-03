from collections import OrderedDict
from common import Common as cm, dd, pp
from definition import Definitions as df
from key import Key
from fuzzywuzzy import fuzz
from math import ceil
import operator as OP
import re

# class CaseInsensitiveDict(dict):
#     """Basic case insensitive dict with strings only keys."""
#
#     proxy = {}
#
#     def __init__(self, data):
#         if not data:
#             return
#         self.proxy = dict((k.lower(), k) for k in data)
#         for k in data:
#             self[k] = data[k]
#
#     def __contains__(self, k):
#         return k.lower() in self.proxy
#
#     def __delitem__(self, k):
#         key = self.proxy[k.lower()]
#         super(CaseInsensitiveDict, self).__delitem__(key)
#         del self.proxy[k.lower()]
#
#     def __getitem__(self, k):
#         key = self.proxy[k.lower()]
#         return super(CaseInsensitiveDict, self).__getitem__(key)
#
#     def get(self, k, default=None):
#         return self[k] if k in self else default
#
#     def __setitem__(self, k, v):
#         super(CaseInsensitiveDict, self).__setitem__(k, v)
#         self.proxy[k.lower()] = k

class NoCaseDict(OrderedDict):
    def __init__(self, data=None):
        self.is_dirty = False
        self.is_operational = False
        self.local_keys = []
        # self.sdx = Soundex()
        # self.mtx = Metaphone()
        self.fuzzy_keys = []
        self.fuzzy_dict = []
        self.fuzzy_exp_var_chosen_record = None
        self.global_text_match = {}
        self.local_cache = {}
        self.local_cache_timer = -1
        self.local_cache_timer_started = False
        self.sentence_struct_dict = {}

        super(NoCaseDict, self).__init__()
        if data is None:
            data = {}
        for key, val in data.items():
            self[key.lower()] = val
            # dd(f'__init__:[{key}], value:[{val}]')
        self.is_operational = True

    def __contains__(self, key):
        key = Key(key)
        is_there = super(NoCaseDict, self).__contains__(key)
        # dd(f'__contains__:[{key}], is_there:{is_there}')
        return is_there

    def __setitem__(self, key, value):
        lkey_key = Key(key)
        super(NoCaseDict, self).__setitem__(lkey_key, value)

        matcher = df.SENT_STRUCT_PAT.search(key)
        is_sentence_structure = (matcher is not None)
        if is_sentence_structure:
            # print(f'SENT_STRUCT_PAT: {key} => {value}')
            entry=cm.creatSentRecogniserPatternRecordPair(key, (value, matcher))
            self.sentence_struct_dict.update(entry)
            # print(f'{entry}')

        if self.is_operational:
            self.is_dirty = True

    def __getitem__(self, key):
        key = Key(key)
        try:
            value = super(NoCaseDict, self).__getitem__(key)
            dd(f'__getitem__:[{key}], value:[{value}]')
            return value
        except Exception as e:
            dd(f'Exception __getitem__:{e}')
            return None

    def get(self, k, default=None):
        return self[k] if k in self else default

    def getSentStructPattern(self, key):
        from reftype import SentStructMode as SMODE
        from matcher import MatcherRecord as MR

        def isMatchedStructMode(mm_record, matched_part):
            structure_mode = mm_record.smode
            is_required_further_checking = (structure_mode != SMODE.ANY)
            if not is_required_further_checking:
                return True

            is_no_punctuation = (structure_mode == SMODE.NO_PUNCTUATION)
            if is_no_punctuation:
                no_punct = (df.PUNCT_IN_BETWEEN.search(matched_part) is None)
                return no_punct

            is_one_word = (structure_mode == SMODE.ONE_WORD_ONLY)
            if is_one_word:
                wc = cm.wordCount(matched_part)
                return (wc == 1)

            is_maximum_two_words = (structure_mode == SMODE.MAXIMUM_TWO)
            if is_maximum_two_words:
                wc = cm.wordCount(matched_part)
                return (wc <= 2)
                # print(f'is_maximum_two_words')

            is_no_conjunctives = (structure_mode == SMODE.NO_CONJUNCTIVES)
            if is_no_conjunctives:
                print(f'is_no_conjunctives')

            return False

        selective_match = []
        for pat, value in self.sentence_struct_dict.items():
            matcher = pat.search(key)

            is_match = (matcher is not None)
            if not is_match:
                continue

            (dict_sl_key, dict_tl_value, dict_tl_mm_record, dict_tl_list) = value
            any_recog_pat = cm.createSentRecogniserAnyPattern(dict_sl_key)
            m = any_recog_pat.search(key)
            grp_list = m.groups()
            matched_part = m.group(1)
            # (dict_tl_txt, tl_matcher) = dict_tl_value
            # groups = matcher.groups()

            is_accept = isMatchedStructMode(dict_tl_mm_record, matched_part)
            if not is_accept:
                continue

            match_rate = fuzz.ratio(dict_sl_key, key)
            entry=(match_rate, pat, value)
            selective_match.append(entry)

        if selective_match:
            selective_match.sort(reverse=True)
            first_entry = selective_match[0]
            (match_rate, pat, value) = first_entry
            return (pat, value)
        else:
            value = (None, None, None, None)
            return (None, value)

    def replaceTranRef(self, tran):
        is_finished = False
        new_tran = str(tran)
        last_found_ref=[]
        while not is_finished:
            matcher = df.TRAN_REF_PATTERN.search(new_tran)
            is_finished = (matcher is None)
            if is_finished:
                break
            ref_found = matcher.group(0)
            is_seen_before = (ref_found in last_found_ref)
            if is_seen_before:
                raise ValueError(f'[{ref_found}] is occured again, SOMETHING IS WRONG in [{tran}]')
            else:
                last_found_ref.append(ref_found)

            dict_selected = self
            has_ref = (ref_found in self)
            if not has_ref:
                has_ref = (ref_found in df.numeral_dict)
                if not has_ref:
                    continue
                else:
                    dict_selected = df.numeral_dict

            tran_for_ref = dict_selected[ref_found]
            new_tran = new_tran.replace(ref_found, tran_for_ref)

        return new_tran

    def clearCache(self):
        self.local_cache.clear()

    def addCache(self, item, result):
        entry = {item: result}
        self.local_cache.update(entry)

    def findCache(self, item):
        try:
            result = self.local_cache[item]
            return result
        except Exception as e:
            return None

    def isInCache(self, item):
        return (item in self.local_cache)

    def simpleFuzzyTranslate(self, msg: str):
        def comparePartial(from_item, to_item):

            # matched_length = cm.getLeadingMatchCount(from_item, to_item)
            matched_ratio = fuzz.ratio(from_item, to_item)
            acceptable = (matched_ratio >= df.FUZZY_ACCEPTABLE_RATIO)
            if acceptable:
                return matched_ratio

            from_item_word_list = from_item.split()
            from_item_word_list_length = len(from_item_word_list)
            to_item_word_list = to_item.split()
            to_item_word_list_length = len(to_item_word_list)
            allowed_number_of_words = (from_item_word_list_length * 1.5)

            total_match_ratio = 0
            if is_k_single_word:
                allowed_from_word_length = (k_word_count * 1.5)
                to_item_word_length = len(from_item)
                is_acceptable_word_count = (to_item_word_length <= allowed_from_word_length) and (allowed_from_word_length >= allowed_from_word_length // 2)
            else:
                is_acceptable_word_count = (to_item_word_list_length <= allowed_number_of_words)

            if not is_acceptable_word_count:
                return 0

            matched_list = [] # for debugging purposes
            try:
                for from_index, from_word in enumerate(from_item_word_list):
                    to_word = to_item_word_list[from_index]
                    matched_ratio = fuzz.ratio(from_word, to_word)
                    acceptable = (matched_ratio >= df.FUZZY_LOW_ACCEPTABLE_RATIO)
                    if acceptable:
                        total_match_ratio += (matched_ratio / from_item_word_list_length)
                        entry = (matched_ratio, from_word, to_word)
                        matched_list.append(entry)
            except Exception as e:
                pass

            acceptable = (total_match_ratio >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)
            # if is_k_single_word:
            #     acceptable = (total_match_ratio >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)
            # else:
            #     line_acceptable_total_ration = (total_match_ratio / to_item_word_list_length * 0.80)
            #     acceptable = (line_acceptable_total_ration > cm.FUZZY_LOW_ACCEPTABLE_RATIO)
            if acceptable:
                return total_match_ratio
            else:
                return 0

        def wordFuzzyCompare(item_txt: str):
            word_list = item_txt.split()
            word_list_count = len(word_list)
            total_matched_ratio = 0.0
            try:
                for index, i_word in enumerate(word_list):
                    k_word = k_word_list[index]
                    match_rat = fuzz.ratio(i_word, k_word)
                    total_matched_ratio += (match_rat / word_list_count)
            except Exception as e:
                pass

            int_total_rat = int(total_matched_ratio)
            return int_total_rat

        def fuzzyCompareString(loc_item):
            match_rat = fuzz.ratio(loc_item, k)
            is_equal = (match_rat >= df.FUZZY_LOW_ACCEPTABLE_RATIO)
            if not is_equal:
                match_rat = wordFuzzyCompare(loc_item)
                is_equal = (match_rat >= df.FUZZY_LOW_ACCEPTABLE_RATIO)
            if is_equal:
                return 0, match_rat
            elif loc_item < k:
                return -1, match_rat
            else:
                return 1, match_rat

        def linearSearch(k_list):
            rat_list = []
            for i, item in enumerate(k_list):
                value, match_rat = fuzzyCompareString(item)
                entry = (match_rat, i, item)
                rat_list.append(entry)
            rat_list.sort(reverse=True)
            dd(f'linearSearch(): rat_list sorted:')
            dd('---------')
            pp(rat_list)
            dd('---------')
            first_item = rat_list[0]
            return first_item

        def binarySearchStartIndex(k_list):
            looking_for = k # for debugging purposes
            lo = 0
            hi = len(k_list)-1
            selective_list=[]
            while lo < hi:
                mid = (lo + hi) // 2
                item = k_list[mid]
                item_part = item[:k_matching_length]
                is_equal = (item_part == k_part)
                if is_equal:
                    return mid

                # if not is_equal:
                #     value, match_rat = fuzzyCompareString(item)
                #     can_look_around = (match_rat > 50)
                #     # match_rat = fuzz.ratio(item, k)
                #     is_equal = (match_rat >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)
                #     if is_equal:
                #         return mid
                #     elif can_look_around:
                #         max_back = max(mid - 100, 0)
                #         max_forth = min(mid + 100, hi)
                #         rate, i, found_item = linearSearch(k_list[max_back:max_forth])
                #         actual_rate = fuzz.ratio(found_item, looking_for)
                #         is_equal = (actual_rate >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)
                #         if is_equal:
                #             index = max_back + i
                #             test_item = k_list[index] # for debugging purposes
                #             return index
                #         elif value < 0:
                #             lo = mid + 1
                #         else:
                #             hi = mid
                #     elif value < 0:
                #         lo = mid + 1
                #     else:
                #         hi = mid
                elif item < k:
                    lo = mid + 1
                else:
                    hi = mid
            return -1

        def validate(item):
            item_part = item[:k_matching_length]
            is_found = (item_part.lower() == k_part.lower())
            if not is_found:
                return -1, None

            if is_k_single_word:
                item_len = len(item)
                acceptable = (item_len == k_length)
            else:
                is_tran_ref = (df.TRAN_REF_PATTERN.search(item) is not None)
                word_count = len(item.split())
                acceptable = (word_count >= k_word_count) and (word_count < int(k_word_count * 1.5))

            return_result = (1 if acceptable else 0)
            # if acceptable:
            #     dd(f'simpleFuzzyTranslate(), validate(): looking for: [{k_part}] => found: [{item}]')
            return return_result, item

        def findListOfCandidates():

            subset = []
            index = binarySearchStartIndex(key_list)
            is_found = (index >= 0)
            if not is_found:
                return subset

            found_list = []
            ss = index
            ee = index
            # dd(f'simpleFuzzyTranslate(): start index: [{index}]')
            for i in range(index-1, 0, -1):
                item = key_list[i]
                cond, found_item = validate(item)
                is_break = (cond == -1)
                if is_break:
                    # dd(f'simpleFuzzyTranslate(): traverse backward, stopped at: [{i}], item:[{item}]')
                    break
                is_accepted = (cond == 1)
                if is_accepted:
                    found_list.append(item)
            ss = i
            # dd(f'simpleFuzzyTranslate(): backward to index: [{i}]')
            for i in range(index, len(key_list)):
                item = key_list[i]
                cond, found_item = validate(item)
                is_break = (cond == -1)
                if is_break:
                    # dd(f'simpleFuzzyTranslate(): traverse forward, stopped at: [{i}], item:[{item}]')
                    break
                is_accepted = (cond == 1)
                if is_accepted:
                    found_list.append(item)
            ee = i
            # dd(f'simpleFuzzyTranslate(): forward to index: [{i}]')
            found_list.sort(key=lambda x: len(x), reverse=True)
            # if found_list:
            #     pas
            # dd('Range looking at:')
            # dd('---------')
            # k_list_len = len(key_list)
            # # ss = min(ss+1, k_list_len)
            # # ee = max(0, ee-1)
            # examine_part = key_list[ss:ee]
            # dd(f'looking for: [{msg}]')
            # pp(examine_part)
            # dd('---------')
            # dd(f'simpleFuzzyTranslate(): found_list:')
            # dd('---------')
            # dd(f'looking for: [{msg}]')
            # pp(found_list)
            # dd('---------')

            for found_item in found_list:
                # matched_length = comparePartial(k, found_item)
                ratio = fuzz.ratio(found_item, k)
                is_found = (ratio >= df.FUZZY_LOW_ACCEPTABLE_RATIO)
                if not is_found:
                    # perfect_match_percent = cm.matchTextPercent(k, found_item)
                    # is_accepted = (perfect_match_percent > cm.FUZZY_PERFECT_MATCH_PERCENT)
                    # dd(f'simpleFuzzyTranslate(): perfect_match_percent:[{perfect_match_percent}] k:[{k}] => found_item:[{found_item}]')
                    # if not is_accepted:
                    #     dd('simpleFuzzyTranslate(): perfect_match_percent TOO LOW, IGNORED')
                    #     continue
                    continue

                entry = (ratio, found_item)
                subset.append(entry)

            subset.sort(reverse=True)
            # dd(f'simpleFuzzyTranslate(): subset:')
            # dd('---------')
            # dd(f'looking for: [{msg}]')
            # pp(subset)
            # dd('---------')

            return subset

        untran_word_dic = {}
        left, k, right = cm.getTextWithin(msg)
        k = k.lower()

        key_list = list(self.keys())
        subset = key_list

        k_length = len(k)
        k_word_list = k.split()
        k_word_count = len(k_word_list)
        is_k_single_word = (k_word_count == 1)

        k_matching_length = int(ceil(k_length * 0.5))
        if not is_k_single_word:
            first_word = k_word_list[0]
            first_word_len = len(first_word)
            is_two_small = (first_word_len < 3)
            k_matching_length = int(ceil(first_word_len * df.MAX_FUZZY_TEST_LENGTH))
            if is_two_small:
                try:
                    second_word = k_word_list[1]
                    second_word_len = len(second_word)
                    k_matching_length = int(ceil((first_word_len + second_word_len + 1) * df.MAX_FUZZY_TEST_LENGTH))
                except Exception as e:
                    pass

        max_k_length = int(k_length * df.FUZZY_KEY_LENGTH_RATIO)
        k_part = k[:k_matching_length]
        subset = findListOfCandidates()
        found_candidates = (len(subset) > 0)
        if not found_candidates:
            return_tran = None
            rat = 0
            selected_item = None
            return return_tran, selected_item, rat, untran_word_dic

        matched_ratio, selected_item = subset[0]
        is_accepted = (matched_ratio >= df.FUZZY_MODERATE_ACCEPTABLE_RATIO)
        if not is_accepted:
            perfect_match_percent = cm.matchTextPercent(k, selected_item)
            is_accepted = (perfect_match_percent > df.FUZZY_PERFECT_MATCH_PERCENT)
            dd(f'simpleFuzzyTranslate(): perfect_match_percent:[{perfect_match_percent}] k:[{k}] => selected_item:[{selected_item}]; is_accepted:[{is_accepted}]')
            if not is_accepted:
                return_tran = None
                rat = 0
                selected_item = None
                return return_tran, selected_item, rat, untran_word_dic

        translation_txt = self[selected_item]
        lower_msg = msg.lower()
        try:
            loc, new_selected = cm.locRemain(lower_msg, selected_item)
            translation = lower_msg.replace(new_selected, translation_txt)
            untran_word_dic = cm.getRemainedWord(lower_msg, new_selected)
        except Exception as e:
            dd(e)
            dd(f'FAILED TO REPLACE: [{lower_msg}] by [{selected_item}] with trans: [{translation_txt}], matched_ratio:[{matched_ratio}]')
            can_accept = (matched_ratio >= df.FUZZY_ACCEPTABLE_RATIO)
            if can_accept:
                translation = translation_txt

                left, mid, right = cm.getTextWithin(lower_msg)
                had_the_same_right = (right and translation.endswith(right))
                had_the_same_left = (left and translation.startswith(left))

                if left and not had_the_same_left:
                    translation = left + translation

                if right and not had_the_same_right:
                    translation = translation + right

                dd(f'SIMPLE PATCHING: left:[{left}] right:[{right}] trans: [{translation}]')
                untran_word_dic = cm.getRemainedWord(lower_msg, selected_item)
            else:
                translation = None

        return translation, selected_item, matched_ratio, untran_word_dic


    def fuzzyTranslate(self, msg):

        def compareExpressContruct(item, k):
            i_left, i_right, k_left, k_right = cm.splitExpVar(item, k)
            is_left_match = is_right_match = True
            left_ratio = right_ratio = 0
            has_left = bool(i_left and k_left)
            if has_left:
                left_ratio = fuzz.ratio(i_left, k_left)
                is_left_match = (left_ratio >= df.FUZZY_LOW_ACCEPTABLE_RATIO)

            has_right = bool(i_right and k_right)
            if has_right:
                right_ratio = fuzz.ratio(i_right, k_right)
                is_right_match = (right_ratio >= df.FUZZY_LOW_ACCEPTABLE_RATIO)

            is_equal = (has_left or has_right) and (is_left_match and is_right_match)
            if is_equal:
                return 0, (left_ratio + right_ratio) // 2
            elif item < k:
                return -1, -1
            else:
                return 1, 1

        def compareString(item, test_length, is_fuzzy=False):
            item_has_expr_contruct = False
            if is_fuzzy:
                calc_ratio = fuzz.ratio(item, k)
                is_sounded_similar = (calc_ratio >= df.FUZZY_LOW_ACCEPTABLE_RATIO)

                if is_sounded_similar:
                    return 0, calc_ratio
                elif item < k:
                    return -1, calc_ratio
                else:
                    return 1, calc_ratio
            else:
                item_len = len(item)
                item_test_length = min(item_len, test_length)
                item_part = item[:item_test_length]
                is_equal = (item_part == k_part)
                if is_equal:
                    calc_ratio = fuzz.ratio(item, k)
                    return 0, calc_ratio
                elif item_part < k_part:
                    return -1, 0
                else:
                    return 1, 0

        def binarySearchStartIndex(k_list, test_length):
            lo = 0
            hi = len(k_list)-1
            while lo < hi:
                mid = (lo + hi) // 2
                item = k_list[mid]
                value, _ = compareString(item, test_length)
                is_equal = (value == 0)
                if is_equal:
                    dd(f'FOUND MID index [{mid}]')
                    return mid
                elif value < 0:
                    lo = mid + 1
                else:
                    hi = mid
            return -1

        def reduceListSize(k_list, start_index, test_length):
            def loopList(kk_list, s_index, is_backward=True):
                i = s_index
                is_finished = False
                list_len = len(kk_list)
                while not is_finished:
                    item = k_list[i]
                    i += (-1 if is_backward else 1)
                    is_finished = (i <= -1) or (i > list_len)
                    if is_finished:
                        break

                    value, fuzzy_ratio = compareString(item, test_length)
                    is_acceptable = (value == 0)
                    if is_acceptable:
                        is_acceptable_ratio = (fuzzy_ratio > df.FUZZY_VERY_LOW_ACCEPTABLE_RATIO)
                        if is_acceptable_ratio:
                            match_leading_count = getMatchingLeadingCount(item)
                            entry=(match_leading_count, fuzzy_ratio, item)
                            working_list.append(entry)
                    else:
                        break

                working_list.sort()
                working_list.reverse()
                for match_leading_count, temp_ratio, tem_text in working_list:
                    is_acceptable_ratio = (temp_ratio >= df.FUZZY_ACCEPTABLE_RATIO)
                    if is_acceptable_ratio:
                        entry = (match_leading_count, temp_ratio, tem_text)
                        is_in_new_list = (entry in new_list)
                        if not is_in_new_list:
                            new_list.append(entry)
                    else:
                        return

            new_list=[]
            working_list=[]
            # item = k_list[start_index]
            # value, fuzzy_ratio = compareString(item, test_length, is_fuzzy=True)
            # entry = (fuzzy_ratio, item)
            # new_list.append(entry)

            hi = len(k_list)-1
            # moving back, insert new record in the process
            loopList(k_list, start_index-1, is_backward=True)
            loopList(k_list, start_index, is_backward=False)
            return new_list

        def getMostLikelyItem():

            subset.sort(key=OP.itemgetter(0,1), reverse=True)

            dd(f'selectable_list: [{msg}]')
            dd('-' * 80)
            pp(subset)
            dd('-' * 80)

            first_entry = subset[0]
            match_leading_count, first_entry_ratio, first_text_selected = first_entry

            similar_ratio_list = []
            for index, ent in enumerate(subset):
                match_leading_count, rat, selected_entry = ent
                is_similar = (rat == first_entry_ratio)
                if is_similar:
                    sequence_matching_ratio = fuzz.partial_ratio(selected_entry, k)
                    similar_entry=(match_leading_count, sequence_matching_ratio, selected_entry)
                    similar_ratio_list.append(similar_entry)

            similar_ratio_list.sort(reverse=True)
            first_entry = similar_ratio_list[0]
            match_leading_count, first_entry_ratio, first_text_selected = first_entry

            dd(f'fuzzyTranslation, getMostLikelyItem(): looking for:[{k}]; first_entry:[{first_entry}]')
            return first_entry_ratio, first_text_selected

        def getMatchingLeadingCount(txt):
            match_count = 0
            for index, c in enumerate(txt):
                try:
                    k_c = k[index]
                    is_same = (c == k_c)
                    if is_same:
                        match_count += 1
                    else:
                        break
                except Exception as e:
                    break

            return match_count

        # print(f'fuzzyTranslation, looking for: [{msg}]')
        k = msg.lower()
        k_length = len(k)
        k_word_count = len(k.split())

        key_list = list(self.keys())
        # subset = list(filter(filter_function, key_list))
        subset = key_list

        k_part = k[:2]
        s_index = binarySearchStartIndex(key_list, 2)
        if s_index >= 0:
            subset = reduceListSize(key_list, s_index, 2)

        if not subset:
            return None, None, 0

        number_of_possible_fuzzy_entries = len(subset)
        is_too_large_subset = (number_of_possible_fuzzy_entries > df.MAX_FUZZY_LIST)
        if is_too_large_subset:
            return None, None, 0

        matching_ratio, first_text_selected = getMostLikelyItem()
        word_selected_list = first_text_selected.split()
        word_selected_list_count = len(word_selected_list)
        is_less_than_required = (word_selected_list_count < k_word_count)
        if is_less_than_required:
            return None, first_text_selected, 0

        tran = self[first_text_selected]
        tran = cm.insertTranslation(msg.lower(), first_text_selected, tran)
        #
        # dd('-' * 80)
        # # covered_length = len(word_selected)
        # can_reduce_further = (len(subset) > 1)
        dd(f'fuzzyTranslation: looking for:[{k}]; first_text_selected:[{first_text_selected}] => tran:[{tran}]')
        return tran, first_text_selected, matching_ratio

    def __delitem__(self, key):
        key = self.Key(key)
        # dd(f'__delitem__:[{key}]')
        try:
            super(NoCaseDict, self).__delitem__(key)
            if self.is_operational:
                self.is_dirty = True
        except Exception as e:
            dd(f'__delitem__ Exception :{e}')


    def getSetByWordCountInRange(self, from_count, to_count, first_word_list=None, is_reversed=False):
        new_set = NoCaseDict()
        if is_reversed:
            key_list = reversed(list(self.keys()))
        else:
            key_list = list(self.keys())

        for k in key_list:
            wc = len(k.split())
            is_selectable = (wc >= from_count) and (wc <= to_count)
            if not is_selectable:
                continue

            if first_word_list:
                firt_word = k.split()[0]
                match_first_char = (firt_word in first_word_list)
                if not match_first_char:
                    continue

            started = True
            v = self[k]
            entry = {k: v}
            new_set.update(entry)

        return new_set

    def getSetByWordCount(self, word_count, first_word=None, is_reversed=False):
        new_set = self.getSetByWordCountInRange(word_count, word_count, first_word_list=first_word,
                                                is_reversed=is_reversed)
        return new_set

    def getSetUpToWordCount(self, word_count, first_word=None, is_reversed=False):
        new_set = self.getSetByWordCountInRange(1, word_count, first_word_list=first_word, is_reversed=is_reversed)
        return new_set