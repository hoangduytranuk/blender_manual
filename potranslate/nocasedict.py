from collections import OrderedDict
from common import Common as cm, dd, pp, LocationObserver
from definition import Definitions as df
from key import Key
from fuzzywuzzy import fuzz
from math import ceil
import operator as OP
import inspect as INP
import re
from reftype import SentStructMode as SMODE, SentStructModeRecord as SMODEREC

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
            self[key] = val
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
        self.local_keys.append(key.lower())
        if self.is_operational:
            self.is_dirty = True

    def __getitem__(self, key):
        key = Key(key)
        try:
            value = super(NoCaseDict, self).__getitem__(key)
            dd(f'__getitem__:[{key}], value:[{value}]')
            return value
        except Exception as e:
            fname = INP.currentframe().f_code.co_name
            dd(f'{fname} {e}')
            return None

    def createSentenceStructureDict(self):
        def tempDictKey(item):
            (pat, val) = item
            return pat.pattern

        temp_dict={}
        temp_set = [(x, y) for (x, y) in self.items() if df.SENT_STRUCT_START_SYMB in x]
        for key, value in temp_set:
            value = self.replaceTranRef(value)
            key_pattern = cm.creatSentRecogniserPattern(key)
            dict_sl_mm, dict_sl_word_list = cm.createSentRecogniserRecord(key)
            dict_tl_mm, dict_tl_word_list = cm.createSentRecogniserRecord(value)

            entry = {key_pattern: (key, dict_sl_word_list, dict_sl_mm, value, dict_tl_word_list, dict_tl_mm)}
            temp_dict.update(entry)
        temp_dict = OrderedDict(sorted(temp_dict.items()))
        self.sentence_struct_dict = NoCaseDict(temp_dict)

    def get(self, k, default=None):
        return self[k] if k in self else default

    def getSentStructPattern(self, key):
        def isMatchedStructMode(pat_matched_text_pair_list):
            is_ok_list=[]
            (s_mode_dict, input_txt_list) = pat_matched_text_pair_list
            s_mode_dict_list = list(s_mode_dict.values())
            for index, matched_part in enumerate(input_txt_list):
                smode_item = s_mode_dict_list[index]
                (dict_sl_txt, structure_mode_list) = smode_item
                is_txt_only = (structure_mode_list is None)
                if is_txt_only:
                    continue

                smode_rec: SMODEREC = None
                for smode_rec in structure_mode_list:
                    structure_mode = smode_rec.smode
                    extra_param = smode_rec.extra_param

                    is_any = (structure_mode == SMODE.ANY)
                    if is_any:
                        is_ok_list.append(True)
                        continue

                    is_position_priority = (structure_mode == SMODE.POSITION_PRIORITY)
                    if is_position_priority:
                        smode_rec.extra_param = df.SENT_STRUCT_POSITION_PRIORITY_WEIGHT
                        is_ok_list.append(True)
                        continue

                    is_ordered = (structure_mode == SMODE.ORDERED_GROUP)
                    if is_ordered:
                        is_ok_list.append(True)
                        continue

                    is_no_full_stop = (structure_mode == SMODE.NO_FULL_STOP)
                    if is_no_full_stop:
                        no_fullstop = (df.FULLSTOP_IN_BETWEEN.search(matched_part) is None)
                        is_ok_list.append(no_fullstop)
                        continue

                    is_no_punctuation = (structure_mode == SMODE.NO_PUNCTUATION)
                    if is_no_punctuation:
                        no_punct = (df.PUNCT_IN_BETWEEN.search(matched_part) is None)
                        is_ok_list.append(no_punct)
                        continue

                    is_max_upto = (structure_mode == SMODE.MAX_UPTO)
                    if is_max_upto:
                        wc = cm.wordCount(matched_part)
                        is_max_upto = (wc <= extra_param)
                        is_ok_list.append(is_max_upto)
                        continue

                    is_no_conjunctives = (structure_mode == SMODE.NO_CONJUNCTIVES)
                    if is_no_conjunctives:
                        no_conjunctives = (df.BASIC_CONJUNCTS.search(matched_part) is None)
                        is_ok_list.append(no_conjunctives)
                        continue

            ok = (False not in is_ok_list)
            return ok

        def getListOfPossibleKeys():
            selective_match=[]
            for pat, value in self.sentence_struct_dict.items():
                pattern_txt = pat.pattern
                rat = fuzz.ratio(pattern_txt, key)
                possible_entry = (rat, (pat, value))
                selective_match.append(possible_entry)
            selective_match.sort(reverse=True)
            if selective_match:
                rat, pat, value = selective_match[0]
                if pat.search(key):
                    return (pat, value)
                else:
                    return (None, None)
            else:
                return (None, None)

        try:
            selective_match = []
            list_of_sent_struct = list(self.sentence_struct_dict.items())
            for pat, value in list_of_sent_struct:
                matcher = re.search(pat, key, flags=re.I)

                is_match = (matcher is not None)
                if not is_match:
                    continue

                matched_text_group = matcher.groups()
                (dict_sl_txt, dict_sl_word_list, dict_sl_mm, dict_tl_txt, dict_tl_word_list, dict_tl_mm) = value
                s_mode_list = dict_sl_mm.smode
                pattern_and_matched_text_pair_list = (s_mode_list, matched_text_group)
                is_accept = isMatchedStructMode(pattern_and_matched_text_pair_list)
                if not is_accept:
                    continue

                match_rate = fuzz.ratio(dict_sl_txt, key)
                entry=(match_rate, pat, value)
                selective_match.append(entry)

            if selective_match:
                selective_match.sort(reverse=True)
                first_entry = selective_match[0]
                (match_rate, pat, value) = first_entry
                pattern = re.compile(pat, flags=re.I)
                return (pattern, value)
            else:
                value = (None, None, None, None, None, None)
                return (None, value)
        except Exception as e:
            fname = INP.currentframe().f_code.co_name
            dd(f'{fname} {e}')
            raise e

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

    def addCacheEntry(self, entry: tuple):
        self.local_cache.update(entry)

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

    def simpleFuzzyTranslate(self, msg: str, acceptable_rate=df.FUZZY_ACCEPTABLE_RATIO):
        def getItemPart(item_txt):
            item_word_list = item_txt.split()
            item_first_word = item_word_list[0]
            item_part = item_first_word[:max_k_length]
            return item_part

        def validate(item):
            item_part = getItemPart(item)
            is_found = (item_part.lower() == k_part.lower())
            if not is_found:
                return -1, None

            allowable_length = (k_length * (1 + df.MAX_FUZZY_TEST_LENGTH))
            if is_k_single_word:
                item_len = len(item)
                acceptable = (item_len <= allowable_length)
            else:

                word_count = len(item.split())
                item_word_count_is_greater_or_equal_k_word_count = (word_count >= k_word_count)
                item_word_count_is_smaller_than_allowable_k_word_count = (word_count <= allowed_k_word_count)
                acceptable =  (item_word_count_is_greater_or_equal_k_word_count
                               and
                               item_word_count_is_smaller_than_allowable_k_word_count)

            return_result = (1 if acceptable else 0)
            return return_result, item

        def findListOfCandidates():
            subset = []
            index = cm.binarySearch(key_list, k, key=getItemPart)
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
            found_list.sort(key=lambda x: len(x), reverse=True)

            for found_item in found_list:
                ratio = fuzz.ratio(found_item, k)
                is_found = (ratio >= df.FUZZY_LOW_ACCEPTABLE_RATIO)
                if not is_found:
                    continue

                entry = (ratio, found_item)
                subset.append(entry)

            subset.sort(reverse=True)
            return subset

        untran_word_dic = {}
        left, k, right = cm.getTextWithin(msg)
        k = k.lower()

        key_list = self.local_keys
        subset = key_list

        k_length = len(k)
        k_word_list = k.split()
        k_word_count = len(k_word_list)
        is_k_single_word = (k_word_count == 1)
        allowed_k_word_count = int(k_word_count * 1.7)

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

        first_word = k_word_list[0]
        first_word_len = len(first_word)
        max_k_length = int(first_word_len * df.FUZZY_KEY_LENGTH_RATIO)
        k_part = first_word[:max_k_length]
        subset = findListOfCandidates()
        found_candidates = (len(subset) > 0)
        if not found_candidates:
            return_tran = None
            rat = 0
            selected_item = None
            return return_tran, selected_item, rat, untran_word_dic

        matched_ratio, selected_item = subset[0]
        is_accepted = (matched_ratio >= acceptable_rate)
        if not is_accepted:
            perfect_match_percent = cm.matchTextPercent(k, selected_item)
            is_accepted = (perfect_match_percent > df.FUZZY_PERFECT_MATCH_PERCENT)
            # dd(f'simpleFuzzyTranslate(): perfect_match_percent:[{perfect_match_percent}] k:[{k}] => selected_item:[{selected_item}]; is_accepted:[{is_accepted}]')
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
            fname = INP.currentframe().f_code.co_name
            dd(f'{fname} {e}')
            dd(f'FAILED TO REPLACE: [{lower_msg}] by [{selected_item}] with trans: [{translation_txt}], matched_ratio:[{matched_ratio}]')
            can_accept = (matched_ratio >= acceptable_rate)
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

    def __delitem__(self, key):
        key = Key(key)
        # dd(f'__delitem__:[{key}]')
        try:
            super(NoCaseDict, self).__delitem__(key)
            if self.is_operational:
                self.is_dirty = True
        except Exception as e:
            fname = INP.currentframe().f_code.co_name
            dd(f'{fname} {e}')

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

    def blindTranslate(self, txt):
        dd(f'blindTranslate() : [{txt}]')
        txt_map = cm.genmap(txt)
        obs = LocationObserver(txt)
        resolved_list=[]
        for local_loc, local_txt in txt_map:
            tran, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(local_txt)
            if not tran:
                continue

            obs.markLocAsUsed(local_loc)
            entry=(local_loc, local_txt, tran)
            resolved_list.append(entry)

        if not resolved_list:
            return None

        un_tran_dic = obs.getUnmarkedPartsAsDict()
        translation = str(txt)
        for local_loc, local_txt, tran in resolved_list:
            translation = cm.jointText(translation, tran, local_loc)
        is_ok = (translation != txt)
        if is_ok:
            dd(f'blindTranslate() [{txt}]: [{translation}]')
            return translation, un_tran_dic
        else:
            dd(f'blindTranslate() FAILED TO FIND TRANSLATION FOR: [{txt}]')
            return None, un_tran_dic

