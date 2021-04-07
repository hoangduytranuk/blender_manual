import sys

sys.path.append('/usr/local/lib/python3.8/site-packages')
# sys.path.append('/Users/hoangduytran/blender_manual/potranslate')
# print(f'translation_finder sys.path: {sys.path}')

import hashlib
import io
import os
import re
import math as ma
from common import Common as cm, MatcherRecord
from common import dd, pp
from ignore import Ignore as ig
import json
from collections import OrderedDict, defaultdict
from sphinx_intl import catalog as c
# import numpy as np
from babel.messages.catalog import Message
from babel.messages import pofile
from common import DEBUG
# , DIC_LOWER_CASE
from reftype import RefType
import operator as OP
from pprint import pprint
# from stringmatch import StringMatch
from fuzzywuzzy import fuzz
# from pyphonetics import Soundex, Metaphone

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
class SentStructRecord():
    def __init__(self, struct_dict, dict_pat, dict_index, key, k_loc,  k_left, k_mid, k_right, tran, t_loc, t_left, t_mid, t_right, km_translated):
        self.struct_dict = struct_dict      # struct_dict: the reference to the dictionary where structure pattern is found
        self.dict_pat = dict_pat            # dict_pat: the structure pattern in the dictionary which key (msg) matched, hold here for reference
        self.dict_pat_index = dict_index    # index in the struct_dict, where the dict_pat is found

        self.key = key              # msg: the message contains the structured pattern, and needed to be translated
        self.k_loc = k_loc          # key: location of $$$
        self.kl_txt = k_left        # key: part before $$$
        self.km_txt = k_mid         # key: part where $$$ was, needed to be translated
        self.kr_txt = k_right       # key: part after $$$

        self.tran = tran            # tran: the message contains the structured pattern, with translated left/right
        self.t_loc = t_loc          # tran: location of $$$
        self.tl_txt = t_left        # tran: part before $$$
        self.tm_txt = t_mid         # tran: part where the place-holder ' $$$ ' was
        self.tr_txt = t_right       # tran: part after $$$
        self.km_translated = km_translated      # flag to indicate km has been translated

    def __repr__(self):
        sl = [
            ("struct_dict", self.struct_dict),
            ("dict_pat", self.dict_pat),
            ("dict_pat_index", self.dict_pat_index),
            ("key", self.key),
            ("k_loc", self.k_loc),
            ("kl_txt", self.kl_txt),
            ("km_txt", self.km_txt),
            ("kr_txt", self.kr_txt),
            ("tran", self.tran),
            ("t_loc", self.t_loc),
            ("tl_txt", self.tl_txt),
            ("tm_txt", self.tm_txt),
            ("tr_txt", self.tr_txt),
            ("km_translated", self.km_translated),
        ]
        string =  '; '.join(sl)
        return string

    def get_t_txt(self, is_non_tran=False):
        t_m = (self.km_txt if is_non_tran else self.tm_txt)
        l = []
        if self.tl_txt:
            l.append(self.tl_txt)
        l.append(t_m)
        if self.tr_txt:
            l.append(self.tr_txt)

        t = ' '.join(l)
        return t

    def getNonTranslated(self):
        t = self.get_t_txt(is_non_tran=True)
        return t

    def getTranslated(self):
        t = self.get_t_txt(is_non_tran=False)
        return t

class FuzzyExpVarRecord():

    def __init__(self, input_k=None, item_found=None, item_left=None, item_right=None, input_k_left=None, input_k_right=None):
        self.input_k_mid = None
        self.input_k_mid_loc = None
        self.input_k:str = input_k
        self.item_found:str = item_found
        self.item_left = item_left
        self.item_right = item_right
        # self.item_mid = self.findExpVarPart(item_found, item_left, item_right)

        self.input_k_left = input_k_left
        self.input_k_right = input_k_right
        self.input_k_mid , self.input_k_mid_loc = self.findExpVarPart(input_k, input_k_left, input_k_right)
        # self.input_k_mid = mid
        # self.input_k_mid_loc = loc
        dd(f'FuzzyExpVarRecord() - self.input_k_mid:[{self.input_k_mid}]; self.input_k_mid_loc:[{self.input_k_mid_loc}]')

    def findExpVarPart(self, input_str, input_left, input_right):
        is_valid = (input_str is not None) and (input_left is not None) and (input_right is not None)
        if not is_valid:
            return None

        left_length = len(input_left)
        right_length = len(input_right)
        input_length = len(input_str)
        input_left_end = input_right_end = input_length

        input_left_start = 0
        input_right_start = input_length
        if input_left:
            input_left_start = input_str.find(input_left)
            input_left_end = input_left_start + left_length

        if input_right:
            input_right_start = input_str.find(input_right)

        input_left_end = min(input_left_end, input_length-1)
        input_right_end = min(0, input_right_end)

        mid_part = input_str[input_left_end : input_right_start]
        stripped_mid = mid_part.strip()
        mid_loc, new_mid_part = cm.locRemain(mid_part, stripped_mid)
        return new_mid_part, mid_loc

class Key(str):
    def __init__(self, key):
        str.__init__(key)

    def __hash__(self):
        k = self.lower()
        key_len = len(k)
        k = (key_len, k)
        hash_value = hash(k)
        # dd(f'__hash__ key:[{k}], hash_value:{hash_value}')
        return hash_value

    def __eq__(self, other):
        local = self.lower()
        extern = other.lower()
        cond = (local == extern)
        # dd(f'__eq__ local:[{local}] extern:[{extern}]')
        return cond

    def __le__(self, other):
        local = self.lower()
        extern = other.lower()
        cond = (local < extern)
        # dd(f'__le__ local:[{local}] extern:[{extern}]')
        return cond

    def __gt__(self, other):
        local = self.lower()
        extern = other.lower()
        cond = (local > extern)
        # dd(f'__gt__ local:[{local}] extern:[{extern}]')
        return cond

class SenStructRecord():
    def __init__(self, txt, loc, left, mid, right):
        self.txt = txt
        self.loc = loc
        self.left = left
        self.mid = mid
        self.right = right

class SenStructDict(OrderedDict):
    def __init__(self, data=None):
        self.struct_list = {}
        self.k_start_list = []
        self.k_end_list = []

    def parseStruct(self, txt):
        m = cm.SENT_STRUCT_PAT.search(txt)
        s = m.start()
        e = m.end()
        left = txt[:s]
        right = txt[e:]
        mid = txt[s:e]
        loc = (s, e)
        sent_struct = SenStructRecord(txt, loc, left, mid, right)
        return sent_struct

    def __setitem__(self, key, value):
        lkey_key = Key(key)        
        super(SenStructDict, self).__setitem__(lkey_key, value)

        k_struct = self.parseStruct(key)
        v_struct = self.parseStruct(value)
        self.struct_list.update({k_struct: v_struct})

class TranslationEntry():
    def __init__(self, untran_txt=None, tran_txt=None, txt_loc=None, fuzzy_rate=None):
        self.untran_txt = untran_txt
        self.tran_txt = tran_txt
        self.loc = txt_loc
        self.fuzzy_rate = fuzzy_rate

class LocationObserver(OrderedDict):
    def __init__(self, msg, tran_finder=None):
        self.blank = str(msg)
        self.tf: TranslationFinder = tran_finder

    def translated(self, s: int, e: int):
        blk = (cm.FILLER_CHAR * (e - s))
        left = self.blank[:s]
        right = self.blank[e:]
        self.blank = left + blk + right

    def translatedLoc(self, loc: tuple):
        ss, ee = loc
        self.translated(ss, ee)

    def isTranslated(self, s: int, e: int):
        part = self.blank[s:e]
        is_dirty = (cm.FILLER_CHAR_PATTERN.search(part) is not None)
        return is_dirty

    def isTranslatedLoc(self, loc: tuple):
        s, e = loc
        return self.isTranslated(s, e)

    def isFullyTranslated(self):
        is_fully_done = (cm.FILLER_CHAR_ALL_PATTERN.search(self.blank) is not None)
        return is_fully_done

    def getUntranDict(self):
        untran_dict = cm.findInvert(cm.FILLER_CHAR_INVERT, self.blank)
        return untran_dict

    def translateLoc(self, loc: tuple):
        s, e = loc
        return self.translatePart(s, e)

    def translatePart(self, s: int, e: int):
        is_translated = self.isTranslated(s, e)
        if is_translated:
            return None

        txt = self.blank[s:e]
        is_ignore = ig.isIgnored(txt)
        if is_ignore:
            return None

        tran_sub_text, fuzzy_len, matching_ratio = self.tf.tryFuzzyTranlation(txt)
        if tran_sub_text:
            return tran_sub_text
        else:
            return None

    def translateLocByWords(self, loc: tuple):
        s, e = loc
        return self.translatePartByWords(s, e)

    def translatePartByWords(self, s: int, e: int):
        is_translated = self.isTranslated(s, e)
        if is_translated:
            return None

        txt = self.blank[s:e]
        is_ignore = ig.isIgnored(txt)
        if is_ignore:
            return None

        tran_sub_text = self.tf.translateWords(txt)
        if tran_sub_text:
            return tran_sub_text
        else:
            return None

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

        is_sent_struct = (cm.SENT_STRUCT_PAT.search(key) is not None)
        if is_sent_struct:
            entry={key: value}
            self.sentence_struct_dict.update(entry)
        
        # fuzz_metaphone = self.mtx.phonetics(key)
        # fuzz_entry = (fuzz_metaphone, key, value)
        # self.fuzzy_keys.append(fuzz_metaphone)
        # self.fuzzy_dict.append(fuzz_entry)

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

    def replaceTranRef(self, tran):
        is_finished = False
        new_tran = str(tran)
        last_found_ref=[]
        while not is_finished:
            matcher = cm.TRAN_REF_PATTERN.search(new_tran)
            is_finished = (matcher is None)
            if is_finished:
                break
            ref_found = matcher.group(0)
            is_seen_before = (ref_found in last_found_ref)
            if is_seen_before:
                raise ValueError(f'[{ref_found}] is occured again, SOMETHING IS WRONG in [{tran}]')
            else:
                last_found_ref.append(ref_found)

            has_ref = (ref_found in self)
            if not has_ref:
                continue

            tran_for_ref = self[ref_found]
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
            acceptable = (matched_ratio >= cm.FUZZY_ACCEPTABLE_RATIO)
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
                    acceptable = (matched_ratio >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)
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
            is_equal = (match_rat >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)
            if not is_equal:
                match_rat = wordFuzzyCompare(loc_item)
                is_equal = (match_rat >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)
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

        # def isTranRef(l_item):
        #     matcher = cm.TRAN_REF_PATTERN.search(l_item)
        #     is_tran_ref = (matcher is not None)
        #     if not is_tran_ref:
        #         return False, None, None
        #
        #     ss = matcher.start()
        #     ee = matcher.end()
        #     l_item_left = l_item[:ss].casefold()
        #     l_item_right = l_item[ee:].casefold()
        #
        #     is_k_started_same = (k[:ss].casefold() == l_item_left)
        #     is_k_ended_same = (k[ee:].casefold() == l_item_right)
        #
        #     is_match = (is_k_started_same and is_k_ended_same)
        #     if not is_match:
        #         return False, None, None
        #
        #     loc = (ss, ee)
        #     item_mid_part = l_item[ss:ee]
        #     k_mid_part = k[ss:ee]
        #     translation
        #     return is_match, l_item_left, l_item_right, mid_part, loc,

        def validate(item):
            item_part = item[:k_matching_length]
            is_found = (item_part.lower() == k_part.lower())
            if not is_found:
                return -1, None

            if is_k_single_word:
                item_len = len(item)
                acceptable = (item_len == k_length)
            else:
                is_tran_ref = (cm.TRAN_REF_PATTERN.search(item) is not None)
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
                is_found = (ratio >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)
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

        cm.debugging(k)
        k_length = len(k)
        k_word_list = k.split()
        k_word_count = len(k_word_list)
        is_k_single_word = (k_word_count == 1)

        k_matching_length = int(ma.ceil(k_length * 0.5))
        if not is_k_single_word:
            first_word = k_word_list[0]
            first_word_len = len(first_word)
            is_two_small = (first_word_len < 3)
            k_matching_length = int(ma.ceil(first_word_len * cm.MAX_FUZZY_TEST_LENGTH))
            if is_two_small:
                try:
                    second_word = k_word_list[1]
                    second_word_len = len(second_word)
                    k_matching_length = int(ma.ceil((first_word_len + second_word_len + 1) * cm.MAX_FUZZY_TEST_LENGTH))
                except Exception as e:
                    pass

        key_list = list(self.keys())
        subset = key_list
        max_k_length = int(k_length * cm.FUZZY_KEY_LENGTH_RATIO)
        k_part = k[:k_matching_length]
        subset = findListOfCandidates()
        found_candidates = (len(subset) > 0)
        if not found_candidates:
            return_tran = None
            rat = 0
            selected_item = None
            return return_tran, selected_item, rat, untran_word_dic

        matched_ratio, selected_item = subset[0]
        is_accepted = (matched_ratio >= cm.FUZZY_MODERATE_ACCEPTABLE_RATIO)
        if not is_accepted:
            perfect_match_percent = cm.matchTextPercent(k, selected_item)
            is_accepted = (perfect_match_percent > cm.FUZZY_PERFECT_MATCH_PERCENT)
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
            can_accept = (matched_ratio >= cm.FUZZY_ACCEPTABLE_RATIO)
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

        # def getFuzzyTranslationUsingStringMatch():
        #     # Application of StringMatch class, using default args
        #     titlematch = StringMatch(source_titles, target_titles)
        #     titlematch.tokenize()
        #     match_df = titlematch.match(output_fmt='dict')
        #
        #     k_set = [k]
        #     titlematch = StringMatch(subset, k_set)
        #     titlematch.tokenize()
        #     match_df = titlematch.match(output_fmt='dict')
        #     dd('match_df:')
        #     dd('-' * 80)
        #     for subset_index, v in match_df.items():
        #         _, matched_ratio = v[0]
        #         matched_ratio *= 100
        #         is_acceptable = (matched_ratio >= cm.AWESOME_COSSIM_FUZZY_ACCEPTABLE_RATIO)
        #         if is_acceptable:
        #             entry = (matched_ratio, subset[subset_index])
        #             selectable_list.append(entry)
        #             dd(entry)

        def compareExpressContruct(item, k):
            i_left, i_right, k_left, k_right = cm.splitExpVar(item, k)
            is_left_match = is_right_match = True
            left_ratio = right_ratio = 0
            has_left = bool(i_left and k_left)
            if has_left:
                left_ratio = fuzz.ratio(i_left, k_left)
                is_left_match = (left_ratio >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)

            has_right = bool(i_right and k_right)
            if has_right:
                right_ratio = fuzz.ratio(i_right, k_right)
                is_right_match = (right_ratio >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)

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
                is_sounded_similar = (calc_ratio >= cm.FUZZY_LOW_ACCEPTABLE_RATIO)

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
                        is_acceptable_ratio = (fuzzy_ratio > cm.FUZZY_VERY_LOW_ACCEPTABLE_RATIO)
                        if is_acceptable_ratio:
                            match_leading_count = getMatchingLeadingCount(item)
                            entry=(match_leading_count, fuzzy_ratio, item)
                            working_list.append(entry)
                    else:
                        break

                working_list.sort()
                working_list.reverse()
                for match_leading_count, temp_ratio, tem_text in working_list:
                    is_acceptable_ratio = (temp_ratio >= cm.FUZZY_ACCEPTABLE_RATIO)
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
        is_too_large_subset = (number_of_possible_fuzzy_entries > cm.MAX_FUZZY_LIST)
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


class TranslationFinder:
    KEYBOARD_TRANS_DIC = {
        r'\bWheelUp\b': "Lăn Bánh Xe về Trước (WheelUp)",
        r'\bWheelDown\b': "Lăn Bánh Xe về Sau (WheelDown)",
        r'\bWheel\b': 'Bánh Xe (Wheel)',
        "NumpadPlus": "Dấu Cộng (+) Bàn Số (NumpadPlus)",
        "NumpadMinus": "Dấu Trừ (-) Bàn Số (NumpadMinus)",
        "NumpadSlash": "Dấu Chéo (/) Bàn Số (NumpadSlash)",
        "NumpadDelete": "Dấu Xóa/Del Bàn Số (NumpadDelete)",
        "NumpadPeriod": "Dấu Chấm (.) Bàn Số (NumpadPeriod)",
        "Numpad0": "Số 0 Bàn Số (Numpad0)",
        "Numpad1": "Số 1 Bàn Số (Numpad1)",
        "Numpad2": "Số 2 Bàn Số (Numpad2)",
        "Numpad3": "Số 3 Bàn Số (Numpad3)",
        "Numpad4": "Số 4 Bàn Số (Numpad4)",
        "Numpad5": "Số 5 Bàn Số (Numpad5)",
        "Numpad6": "Số 6 Bàn Số (Numpad6)",
        "Numpad7": "Số 7 Bàn Số (Numpad7)",
        "Numpad8": "Số 8 Bàn Số (Numpad8)",
        "Numpad9": "Số 9 Bàn Số (Numpad9)",
        "Spacebar": "Dấu Cách (Spacebar)",
        r'\bDown\b': "Xuống (Down)",
        r'\bUp\b': "Lên (Up)",
        r'\bComma\b': "Dấu Phẩy (Comma)",
        r'\bMinus\b': "Dấu Trừ (Minus)",
        r'\bPlus\b': "Dấu Cộng (Plus)",
        "Left": "Trái (Left)",
        "=": "Dấu Bằng (=)",
        "Equals": "Dấu Bằng (=)",
        "Right": "Phải (Right)",
        "Backslash": "Dấu Chéo Ngược (Backslash)",
        r'\bSlash\b': "Dấu Chéo (Slash)",
        "AccentGrave": "Dấu Huyền (AccentGrave)",
        "Delete": "Xóa (Delete)",
        "Period": "Dấu Chấm (Period)",
        "Comma": "Dấu Phẩy (Comma)",
        "PageDown": "Trang Xuống (PageDown)",
        "PageUp": "Trang Lên (PageUp)",
        "PgDown": "Trang Xuống (PgDown)",
        "PgUp": "Trang Lên (PgUp)",
        "OSKey": "Phím Hệ Điều Hành (OSKey)",
        "Slash": "Dấu Chéo (Slash)",
        "Minus": "Dấu Trừ (Minus)",
        "Plus": "Dấu Cộng (Plus)",
        "Down": "Xuống (Down)",
        "Up": "Lên (Up)",
        "MMB": "NCG (MMB)",
        "LMB": "NCT (LMB)",
        "RMB": "NCP (RMB)",
        "Pen": "Bút (Pen)"
    }

    KEYBOARD_TRANS_DIC_PURE = {
        "OSKey": "Phím Hệ Điều Hành (OSKey)",
        "WheelUp": "Lăn Bánh Xe về Trước (WheelUp)",
        "WheelDown": "Lăn Bánh Xe về Sau (WheelDown)",
        "Wheel": "Bánh Xe (Wheel)",
        "NumpadPlus": "Dấu Cộng (+) Bàn Số (NumpadPlus)",
        "NumpadMinus": "Dấu Trừ (-) Bàn Số (NumpadMinus)",
        "NumpadSlash": "Dấu Chéo (/) Bàn Số (NumpadSlash)",
        "NumpadDelete": "Dấu Xóa/Del Bàn Số (NumpadDelete)",
        "NumpadPeriod": "Dấu Chấm (.) Bàn Số (NumpadPeriod)",
        "NumpadAsterisk": "Dấu Sao (*) Bàn Số (NumpadAsterisk)",
        "Numpad0": "Số 0 Bàn Số (Numpad0)",
        "Numpad1": "Số 1 Bàn Số (Numpad1)",
        "Numpad2": "Số 2 Bàn Số (Numpad2)",
        "Numpad3": "Số 3 Bàn Số (Numpad3)",
        "Numpad4": "Số 4 Bàn Số (Numpad4)",
        "Numpad5": "Số 5 Bàn Số (Numpad5)",
        "Numpad6": "Số 6 Bàn Số (Numpad6)",
        "Numpad7": "Số 7 Bàn Số (Numpad7)",
        "Numpad8": "Số 8 Bàn Số (Numpad8)",
        "Numpad9": "Số 9 Bàn Số (Numpad9)",
        "Spacebar": "Dấu Cách (Spacebar)",
        "Down": "Xuống (Down)",
        "Up": "Lên (Up)",
        "Comma": "Dấu Phẩy (Comma)",
        "Minus": "Dấu Trừ (Minus)",
        "Plus": "Dấu Cộng (Plus)",
        "Left": "Trái (Left)",
        "=": "Dấu Bằng (=)",
        "Equals": "Dấu Bằng (=)",
        "Right": "Phải (Right)",
        "Backslash": "Dấu Chéo Ngược (Backslash)",
        "Slash": "Dấu Chéo (Slash)",
        "AccentGrave": "Dấu Huyền (AccentGrave)",
        "Delete": "Xóa (Delete)",
        "Period": "Dấu Chấm (Period)",
        "PageDown": "Trang Xuống (PageDown)",
        "PageUp": "Trang Lên (PageUp)",
        "PgDown": "Trang Xuống (PgDown)",
        "PgUp": "Trang Lên (PgUp)",
        "OSKey": "Phím Hệ Điều Hành (OSKey)",
        "MMB": "NCG (MMB)",
        "LMB": "NCT (LMB)",
        "RMB": "NCP (RMB)",
        "Pen": "Bút (Pen)"
    }

    numeric_prefix = 'hằng/lần thứ/bộ/bậc'
    numeric_postfix = 'mươi/lần/bậc'
    numeral_dict = {
        '@{1t}': 'ức',
        '@{1b}': 'tỉ',
        '@{1m}': 'triệu',
        '@{1k}': 'nghìn',
        '@{1h}': 'trăm',
        '@{10}': 'chục/mươi/mười',
        '@{0}': 'không/vô/mươi',
        '@{1}': 'một/nhất/đầu tiên',
        '@{2}': 'hai/nhì/nhị/phó/thứ/giây đồng hồ',
        '@{3}': 'ba/tam',
        '@{4}': 'bốn/tứ/tư',
        '@{5}': 'năm/lăm/nhăm/Ngũ',
        '@{6}': 'Sáu/Lục',
        '@{7}': 'Bảy/Thất',
        '@{8}': 'Số tám/bát',
        '@{9}': 'Chín/cửu',
    }

    numeric_trans = {
        'a|an': '@{1} con/cái/thằng',
        'zero|none|empty|nullary': '@{0}',
        'one|first|monuple|unary': '@{1}',
        'two|second|couple|binary': '@{2}',
        'three|third|triple|ternary': '@{3}',
        'four(th)?|quadruple|Quaternary': '@{4}',
        'five|fifth|quintuple|Quinary': '@{5}',
        'six(th)?|sextuple|Senary': '@{6}',
        'seven(th)?|septuple|Septenary': '@{7}',
        'eight(th)?|octa|octal|octet|octuple|Octonary': '@{8}',
        'nine(th)?|nonuple|Novenary|nonary': '@{9}',
        'ten(th)?|decimal|decuple|Denary': '@{10}',
        'eleven(th)?|undecuple|hendecuple': 'Mười @{1}',
        'twelve(th)?|doudecuple': 'Mười @{2}',
        'thirteen(th)?|tredecuple': 'Mười @{3}',
        'fourteen(th)?|quattuordecuple': 'Mười @{4}',
        'fifteen(th)?|quindecuple': 'Mười @{5}',
        'sixteen(th)?|sexdecuple': 'Mười @{6}',
        'seventeen(th)?|septendecuple': 'Mười @{7}',
        'eighteen(th)?|octodecuple': 'Mười @{8}',
        'nineteen(th)?|novemdecuple': 'Mười @{9}',
        '(twent(y|ie(s|th))+?)|vigintuple': '@{2} @{10}',
        '(thirt(y|ie(s|th))+?)|trigintuple': '@{3} @{10}',
        '(fort(y|ie(s|th))+?)|quadragintuple': '@{4} @{10}',
        '(fift(y|ie(s|th))+?)|quinquagintuple': '@{5} @{10}',
        '(sixt(y|ie(s|th))+?)|sexagintuple': '@{6} @{10}',
        '(sevent(y|ie(s|th))+?)|septuagintuple': '@{7} @{10}',
        '(eight(y|ie(s|th))+?)|octogintuple': '@{8} @{10}',
        '(ninet(y|ie(s|th))+?)|nongentuple': '@{9} @{10}',
        '(hundred(s|th)?)|centuple': '@{1h}',
        '(thousand(s|th)?)|milluple': '@{1k}',
        'million(s|th)?': '@{1m}',
        'billion(s|th)?': '@{1t}',
        'trillion(s|th)?': '@{1t}',
    }


    def __init__(self):
        self.update_dic = 0
        self.update_po_file = None
        home_dir = os.environ['BLENDER_GITHUB']
        self.master_dic_file = os.path.join(home_dir, "ref_dict_0006_0002.json")
        self.master_dic_backup_file = os.path.join(home_dir, "ref_dict_backup_0005_0001.json")
        self.master_dic_test_file = os.path.join(home_dir, "ref_dict_test_0005.json")

        self.vipo_dic_path = os.path.join(home_dir, "gui/2.80/po/vi.po")
        self.vipo_dic_list = None  # not used

        self.current_po_dir = os.path.join(home_dir, "../blender_docs/locale/vi/LC_MESSAGES")
        self.json_dic_file = None

        # self.json_dic_list = self.loadJSONDic(file_name=self.json_dic_file)
        self.json_dic_list = {}
        self.current_po_path = None
        self.current_po_cat = None
        self.setupKBDDicList()

        self.dic_list = None
        self.master_dic_list: NoCaseDict = None
        self.backup_dic_list: NoCaseDict = None
        self.kbd_dict = None

        self.tran_find_func_list = [
            (self.translationByRemovingSymbols, ('txt', None, None)),              # (txt)
            (self.translationByReplacingSymbolsWithSpaces, ('txt', None, None)),   # (txt)
            # self.symbolsRemoval,                            # (new_txt)
            (self.removeByPatternListAndCheck, ('txt', cm.common_suffix_sorted, cm.END_WORD)),               # (txt, cm.common_suffix_sorted, cm.END_WORD)
            (self.removeByPatternListAndCheck, ('txt', cm.common_suffix_sorted, cm.START_WORD)),               # (txt, cm.common_prefix_sorted, cm.START_WORD)
            (self.removeBothByPatternListAndCheck, ('txt', cm.common_prefix_sorted, cm.common_suffix_sorted)),           # (txt, cm.common_prefix_sorted, cm.common_suffix_sorted)
            # output: new_txt, trans, cover_length
            # ------------------------------------
            # self.findDictByRemoveCommonPrePostFixes,        # (txt)
            # self.findAndTrimIfNeeded,                       # (msg, is_patching_found=True)
            # ------------------------------------
            # self.removeStarAndEndingPunctuations,           # (txt)
        ]

        self.numerical_pat_list = []
        self.initNumericalPatternList()
        self.loadDictionary()
        self.struct_dict = self.getDict().sentence_struct_dict
        # pp(self.struct_dict)

    def initNumericalPatternList(self):
        for pat_txt, tran_txt in TranslationFinder.numeric_trans.items():
            pattern_text = r'\b(%s)\b' % (pat_txt)
            pat = re.compile(pattern_text, flags=re.I)
            entry=(pat, tran_txt)
            self.numerical_pat_list.append(entry)

    def translateNumerics(self, msg:str):
        def pat_search(local_en_txt):
            for pat, tran in self.numerical_pat_list:
                m = pat.search(local_en_txt)
                is_matching = (m is not None)
                if is_matching:
                    return tran
            return None

        def find_tran(en_txt):
            try:
                tran = pat_search(en_txt)
                iter = cm.TRAN_REF_PATTERN.finditer(tran)
                for m in iter:
                    abbrev_txt = m.group(0)
                    try:
                        abbrev_tran_txt = TranslationFinder.numeral_dict[abbrev_txt]
                        tran = tran.replace(abbrev_txt, abbrev_tran_txt)
                    except Exception as e:
                        pass
                return tran
            except Exception as e:
                return None

        is_single_word = (len(msg.split()) == 1)
        if not is_single_word:
            return None

        loc, stripped_word = cm.removingNonAlpha(msg)
        translation = find_tran(stripped_word)
        if translation:
            translation = f'{TranslationFinder.numeric_prefix} {translation} {TranslationFinder.numeric_postfix}'
            is_diff = (stripped_word != msg)
            if is_diff:
                translation = msg.replace(msg, stripped_word)
            dd(f'translateNumerics(): [{stripped_word}] => [{translation}]')
        return translation

    def findByReduction(self, msg):
        def append_selective(cover_length, new_text_length, new_text, trans, selective_list, function_name):
            entry = (cover_length, new_text_length, new_text, trans, function_name)
            selective_list.append(entry)

        trans = None
        original_text = str(msg)
        selective_list = []
        try:
            start_non_alpha, mid, end_non_alpha = cm.getTextWithin(msg)
            for f, params in self.tran_find_func_list:
                f_name = f.__name__
                dd(f'findByReduction(): trying function:[{f_name}]')
                txt, param1, param2 = params
                is_empty = not (param1 or param2)
                if is_empty:
                    new_text, trans, cover_length = f(msg)
                else:
                    new_text, trans, cover_length = f(msg, param1, param2)
                new_text_length = len(new_text) # the least cut off the better
                append_selective(cover_length, new_text_length, new_text, trans, selective_list, f_name)
            sorted_selective_list = list(sorted(selective_list, key=OP.itemgetter(0, 1), reverse=True))
            chosen_entry = sorted_selective_list[0]
            cover_length, new_text_length, new_text, trans, function_name = chosen_entry

            trans = cm.patchingBeforeReturn(start_non_alpha, end_non_alpha, trans, txt)
            dd(f'findByReduction: looking for: [{msg}] trans:[{trans}] function_name:[{function_name}]')
        except Exception as e:
            print(f'findByReduction() msg:{msg}')
            print(e)
            raise e
        return new_text, trans, cover_length

    @property
    def master_dic(self):
        # dd(f'master_dic - get length: {len(self.master_dic_list)}')
        return self.master_dic_list

    @master_dic.setter
    def master_dic(self, dic):
        is_change = (self.master_dic_list is not None) and (dic is None)
        if is_change:
            raise Exception('master dic is changed to None')
        self.master_dic_list = dic

    @property
    def backup_dic(self):
        # dd(f'backup_dic - get length: {len(self.backup_dic_list)}')
        return self.backup_dic_list

    @backup_dic.setter
    def backup_dic(self, dic):
        is_change = (self.backup_dic_list is not None) and (dic is None)
        if is_change:
            raise Exception('backup dic is changed to None')
        self.backup_dic_list = dic

    def loadDictionary(self):
        self.reloadChosenDict(is_master=True)
        self.reloadChosenDict(is_master=False)
        self.kbd_dict = NoCaseDict(TranslationFinder.KEYBOARD_TRANS_DIC_PURE)
        self.master_dic_list.fuzzy_keys.sort()
        self.master_dic_list.fuzzy_dict.sort(key=lambda x: x[0])

    def flatPOFile(self, file_path):
        data_cat = c.load_po(file_path)
        c.dump_po(file_path, data_cat)

    def genmap(self, msg):
        def genListOfDistance(max):
            dist_list = []
            for s in range(0, max):
                for e in range(0, max):
                    is_valid = (s < e)
                    if not is_valid:
                        continue

                    entry = (s, e)
                    if entry not in dist_list:
                        dist_list.append(entry)
            return dist_list

        part_list = []
        matched_dict = cm.patternMatchAll(cm.SPACE_WORD_SEP, msg)
        matched_list = list(matched_dict.items())
        max = len(matched_dict)
        loc_dic = {}
        try:
            start_mm: MatcherRecord = None
            end_mm: MatcherRecord = None
            dist_list = genListOfDistance(max)
            dist_list.sort(reverse=True)
            for dist in dist_list:
                from_index, to_index = dist
                start_loc, start_mm = matched_list[from_index]
                end_loc, end_mm = matched_list[to_index]

                ss1, ee1 = start_loc
                ss2, ee2 = end_loc
                sentence = msg[ss1: ee2]

                sub_loc = (ss1, ee2)
                entry = {sub_loc: sentence}
                loc_dic.update(entry)
        except Exception as e:
            raise e

        part_list = list(loc_dic.items())
        # sort out by the number of spaces (indicating word counts) rather than by common string length
        part_list.sort(key=lambda x: (x[1].count(' '), len(x[1])), reverse=True)    # this is how to sort with multi keys, in brackets
        # part_list.sort(key=lambda x: (x[1].count(' ')), reverse=True)
        dd('genmap():')
        dd('-' * 80)
        pp(part_list)
        dd('-' * 80)
        dd(f'for []{msg}')
        return part_list

    def translateBreakupSentences(self, msg):
        if not msg:
            return msg

        count_untranslated = 0
        count_translated = 0
        translation = str(msg)
        result_list = OrderedDict()
        text_list = cm.patternMatchAll(cm.COMMON_SENTENCE_BREAKS, msg)
        for loc, mm in text_list.items():
            (s, e), t = mm.getOriginAsTuple()
            tran = self.isInDict(t)
            count_translated += (1 if tran else 0)
            count_untranslated += (1 if not tran else 0)
            text_entry = ((t, tran) if tran else (t, ""))
            entry = {loc: text_entry}
            result_list.update(entry)

        for loc, text_entry in result_list.items():
            s, e = loc
            orig, tran = text_entry
            left = translation[:s]
            right = translation[e:]
            middle = (tran if tran else orig)
            translation = left + middle + right

        return translation, count_translated, count_untranslated


    def replacingUsingDic(self, local_dict_list: list, un_tran_dict: dict, text: str) -> str:
        def translateUntranslatedList(untran_dict: dict):
            for remain_loc, un_tran_txt in untran_dict.items():
                is_ignore = ig.isIgnored(un_tran_txt)
                if is_ignore:
                    print(f'replacingUsingDic: IGNORING: un_tran_txt:[{un_tran_txt}]')
                    continue

                try:
                    # cm.debugging(un_tran_txt)
                    _, tran_sub_text, covered_length = self.tryToFindTranslation(un_tran_txt)
                except Exception as e:
                    print(f'replacingUsingDic() findByReduction: un_tran_txt:[{un_tran_txt}]')
                    print(e)
                    raise e

                has_tran = (tran_sub_text and not (tran_sub_text == un_tran_txt))
                if has_tran:
                    matching_ratio = 100
                    cover_length = len(un_tran_txt)
                    tran_dict_entry = (matching_ratio, cover_length, remain_loc, un_tran_txt, tran_sub_text)
                    local_dict_list.append(tran_dict_entry)

        location_database = []
        dd(f'replacingUsingDic(): text:[{text}]')
        dd('local_dict entering: -----------------')
        pp(local_dict_list)
        dd('-----------------')

        translation = str(text)
        has_untranslated_items = bool(un_tran_dict)
        if has_untranslated_items:
            try:
                translateUntranslatedList(un_tran_dict)
            except Exception as e:
                print(e)
                raise e

        local_dict_list.sort(key=OP.itemgetter(0), reverse=True)    # sort by matching ratio
        local_dict_list.sort(key=OP.itemgetter(2), reverse=True)    # sort by location
        local_dict = OrderedDict([(loc, (un_tran_txt, tran)) for matching_ratio, cover_length, loc, un_tran_txt, tran in local_dict_list])

        # replacing dict into text and finish
        temp_translation = self.translatedListToText(local_dict, translation)
        has_translation = not (temp_translation == text)
        if not has_translation:
            dd(f'replacingUsingDic(): text:[{text}]')
            print(f'NO translation')
            return None
        else:
            dd(f'replacingUsingDic(): text:[{text}]')
            dd(f'temp_translation:[{temp_translation}]')
            return temp_translation

    def getSentStruct(self, msg):
        def fuzzy_compare_part(part, txt, is_start=False):
            try:
                if not part:
                    return 100

                w_count = len(part.split())
                txt_list = txt.split()
                txt_part_list = (txt_list[:w_count] if is_start else txt_list[-w_count:])
                txt_part = ' '.join(txt_part_list)
                rat = fuzz.ratio(part, txt_part)
                return rat
            except Exception as e:
                return 0

        def split_txt(s_count, e_count, txt):
            word_list = txt.split()
            w_len = len(word_list)
            left = right = mid = ''
            if s_count:
                left = word_list[:s_count]
                left = ' '.join(left)

            if e_count:
                right = word_list[-e_count:]
                right = ' '.join(right)
                mid = word_list[s_count: -e_count]
            else:
                e_count = w_len
                mid = word_list[s_count: e_count]

            mid = ' '.join(mid)
            return left, mid, right

        selective_list = []

        for index, struct_pat in enumerate(self.struct_dict.keys()):
            m = cm.SENT_STRUCT_PAT.search(struct_pat)
            s = m.start()
            e = m.end()
            left = struct_pat[:s]
            right = struct_pat[e:]

            left_rat = fuzzy_compare_part(left, msg, is_start=True)
            right_rat = fuzzy_compare_part(right, msg, is_start=False)
            is_acceptable_left = (left_rat >= cm.FUZZY_ACCEPTABLE_RATIO)
            is_acceptable_right = (right_rat >= cm.FUZZY_ACCEPTABLE_RATIO)
            is_found = (is_acceptable_left and is_acceptable_right)
            if not is_found:
                continue

            rat = fuzz.ratio(struct_pat, msg)
            selective_entry = (rat, left, right, struct_pat, (s, e))
            selective_list.append(selective_entry)

        is_found = bool(selective_list)
        if not is_found:
            return None

        selective_list.sort(reverse=True)
        selective_entry = selective_list[0]


        rat, left, right, struct_pat, k_loc = selective_entry

        s_wcount = len(left.split())
        e_wcount = len(right.split())
        k_left, k_mid, k_right = split_txt(s_wcount, e_wcount, msg)

        has_puncts = (cm.BASIC_PUNCTUALS.search(k_mid) is not None)
        if has_puncts:
            return None

        dd(f'getSentStruct(), found: [{selective_entry}] for [{msg}]')

        tran = self.struct_dict[struct_pat]
        m = cm.SENT_STRUCT_PAT.search(tran)
        ts = m.start()
        te = m.end()
        t_loc = (ts, te)
        left = tran[:ts]
        right = tran[te:]
        s_wcount = len(left.split())
        e_wcount = len(right.split())
        t_left, t_mid, t_right = split_txt(s_wcount, e_wcount, tran)

        k_mid_tran = self.simpleBlindTranslation(k_mid)
        if k_mid_tran:
            dd(f'getSentStruct(), found translation for: [{k_mid}] => [{k_mid_tran}]')
            t_mid = k_mid_tran

        # self, struct_dict, dict_pat, dict_index, k_loc, key, k_left, k_mid, k_right, tran, t_loc, t_left, t_mid, t_right):
        sent_struct = SentStructRecord(
            self.struct_dict,
            struct_pat,
            index,
            msg, k_loc, k_left, k_mid, k_right,
            tran, t_loc, t_left, t_mid, t_right,
            bool(k_mid_tran)
        )
        return sent_struct

    def translatedListToText(self, loc_translated_dict: dict, current_translation) -> str:
        '''
        :param loc_translated_dict:
            dictionary hold records of translated text, in following format
                {loc: (untran_txt, tran_text)}
        :param current_translation:
            initially will be untranslated text
        '''
        orig = str(current_translation)
        observer = LocationObserver(current_translation)


        loc_translated_list = list(loc_translated_dict.items())
        loc_translated_list.sort(reverse=True)

        dd(f'translatedListToText(): txt:[{current_translation}]')
        dd('-----------------')
        pp(loc_translated_list)
        dd('-----------------')

        for loc, v in loc_translated_list:
            is_translated = observer.isTranslatedLoc(loc)
            if is_translated:
                continue

            orig_txt, loc_tran_txt = v
            s, e = loc
            loc_left = current_translation[:s]
            loc_right = current_translation[e:]
            current_translation = loc_left + loc_tran_txt + loc_right

            observer.translatedLoc(loc)
            is_fully_translated = observer.isFullyTranslated()
            if is_fully_translated:
                break

        dd(f'translatedListToText: original [{orig}]')
        dd(f'translatedListToText: translated [{current_translation}]')
        return current_translation

    def simpleBlindTranslation(self, msg):
        translated_dict = OrderedDict()
        map = self.genmap(msg)
        observer = LocationObserver(msg, tran_finder=self)

        for loc, txt in map:
            is_fully_translated = observer.isFullyTranslated()
            if is_fully_translated:
                break

            tran_sub_text = observer.translateLoc(loc)
            if tran_sub_text:
                entry = {loc: (txt, tran_sub_text)}
                translated_dict.update(entry)

        if not translated_dict:
            return None

        untran_dict = observer.getUntranDict()
        observer = LocationObserver(msg, tran_finder=self)
        for loc, txt in untran_dict.items():
            is_fully_translated = observer.isFullyTranslated()
            if is_fully_translated:
                break

            tran_sub_text = observer.translateLocByWords(loc)
            if tran_sub_text:
                entry = {loc: (txt, tran_sub_text)}
                translated_dict.update(entry)

        trans = self.translatedListToText(translated_dict, str(msg))
        has_tran = (trans and (trans != msg))
        if has_tran:
            return trans
        else:
            return None

    def tryFuzzyTranlation(self, msg):
        search_dict: NoCaseDict = self.getDict()
        tran_sub_text = search_dict.findCache(msg)

        is_not_found = isinstance(tran_sub_text, bool)
        if is_not_found:
            return None, len(msg), 0

        if tran_sub_text:
            return tran_sub_text, len(msg), 100

        search_dict: NoCaseDict = None
        has_abbrev = False
        tran_sub_text, fuzzy_text, search_dict, matching_ratio, untran_word_dic = self.isInDictFuzzy(msg)
        if bool(tran_sub_text):
            has_abbrev = (cm.ABBREV_PATTERN_PARSER.search(tran_sub_text) is not None)
        if untran_word_dic and not has_abbrev:
            untran_word_list = list(untran_word_dic.items())
            untran_word_list.sort(reverse=True)
            for loc, un_tran_word in untran_word_list:
                tran_word_text, fuzzy_word_text, search_dict, matching_word_ratio, untran_sub_word_dic = self.isInDictFuzzy(un_tran_word)
                if tran_word_text:
                    tran_sub_text = tran_sub_text.lower().replace(un_tran_word, tran_word_text)

        has_translation = (bool(tran_sub_text) and bool(fuzzy_text))
        fuzzy_len = (len(fuzzy_text) if has_translation else 0)
        if has_translation:
            search_dict.addCache(msg, tran_sub_text)
            dd(f'tryFuzzyTranlation: found: [{tran_sub_text}], matching_ratio:[{matching_ratio}]')
            return tran_sub_text, fuzzy_len, matching_ratio
        else:
            search_dict.addCache(msg, False)
            # dd(f'tryFuzzyTranlation: UNABLE TO FIND: [{msg}]')
            return None, fuzzy_len, 0

    def fillBlank(self, ss, ee, blanker):
        blank_len = (ee - ss)
        blank_str = (cm.FILLER_CHAR * blank_len)
        blank_left = blanker[:ss]
        blank_right = blanker[ee:]
        blanker = blank_left + blank_str + blank_right
        return blanker

    def buildLocalTranslationDict(self, msg):

        local_translated_dict = [] # for quick, local translation
        loc_map = self.genmap(msg)
        observer = LocationObserver(msg)

        for loc, orig_sub_text in loc_map:
            is_translated = observer.isTranslatedLoc(loc)
            if is_translated:
                continue

            is_ignore = ig.isIgnored(orig_sub_text)
            if is_ignore:
                observer.translatedLoc(loc)
                is_fully_translated = observer.isFullyTranslated()
                if is_fully_translated:
                    break
                else:
                    continue

            tran_sub_text = None
            # cm.debugging(orig_sub_text)
            sent_struct = self.getSentStruct(orig_sub_text)
            is_tran_sent_struct = bool(sent_struct)
            if is_tran_sent_struct:
                is_tran = sent_struct.km_translated
                tran_sub_text = (sent_struct.getTranslated() if is_tran else sent_struct.getNonTranslated())

            if not tran_sub_text:
                tran_sub_text = self.isInDict(orig_sub_text)
                if not tran_sub_text:
                    tran_sub_text, cover_length, matching_ratio = self.tryFuzzyTranlation(orig_sub_text)
                    if not tran_sub_text:
                        tran_sub_text = self.translateNumerics(orig_sub_text)

            if tran_sub_text:
                matching_ratio = 100
                cover_length = len(orig_sub_text)
                local_dict_entry = (matching_ratio, cover_length, loc, orig_sub_text, tran_sub_text)
                local_translated_dict.append(local_dict_entry)

                observer.translatedLoc(loc)
                is_fully_translated = observer.isFullyTranslated()
                if is_fully_translated:
                    break

        untran_dict = observer.getUntranDict()
        local_translated_dict.sort(key=OP.itemgetter(2, 0, 1), reverse=True)
        return local_translated_dict, untran_dict

    def blindTranslation(self, msg):
        # dd(f'blindTranslation() msg:[{msg}]')
        # new_text, trans, cover_length = self.findByReduction(msg)
        # is_found_trans = (trans and not trans == msg)
        # if is_found_trans:
        #     return trans

        local_translated_dict, local_untranslated_dic = self.buildLocalTranslationDict(msg)

        # use the translated (longest first) to replace all combination,
        # translate by reduction for ones could not, to form the final translation for the variation
        # translated_dic will be sorted in length by default.
        # using safe translation length and unsafe translation length to sort so one with both highest values
        # are floated on top once sorted. Pick the one at the top list, ignore the rest
        translation = self.replacingUsingDic(local_translated_dict, local_untranslated_dic, msg)
        return translation

    def addDictEntry(self, msg_list, is_master=False):
        if not msg_list:
            return
        error_msg = f'addBackupDict: Invalid msg_list data type\n[{msg_list}]: {type(msg_list)}.\nExpecting dict, list, tupple(orig_txt, tran_txt), or string ONLY!'
        is_dic = (type(msg_list) == dict)
        is_list = (type(msg_list) == list)
        is_tupple = (type(msg_list) == tuple)
        is_string = (type(msg_list) == str)
        is_valid = (is_dic or is_list or is_tupple or is_string)
        if not is_valid:
            raise Exception(error_msg)
        if is_dic:
            for k, v in msg_list.items():
                self.addBackupDictEntry(k, v)
        elif is_list:
            for entry in msg_list:
                try:
                    k, v = entry
                except Exception as e:
                    print(e, error_msg)
                    k = entry
                    v = None
                if is_master:
                    self.addMasterDict(k, v)
                else:
                    self.addBackupDictEntry(k, v)
        elif is_tupple:
            k, v = msg_list
            if is_master:
                self.addMasterDict(k, v)
            else:
                self.addBackupDictEntry(k, v)
        elif is_string:
            raise Exception(error_msg)
            # if is_master:
            #     self.addMasterDict(k, v)
            # else:
            #     self.addBackupDictEntry(k, v)
        else:
            raise Exception(error_msg)

    def getHeadAndTailPuncts(self, msg):
        if not msg:
            return '', ''

        msg_head = msg_trail = None

        msg_trail = cm.TRAILING_WITH_PUNCT_MULTI.search(msg)
        if msg_trail:
            msg_trail = msg_trail.group(0)
        else:
            msg_trail = ''

        msg_head = cm.HEADING_WITH_PUNCT_MULTI.search(msg)
        if msg_head:
            msg_head = msg_head.group(0)
        else:
            msg_head = ''

        return msg_head, msg_trail

    def cleanOneEntry(self, msg):
        if not msg:
            return msg

        new_msg = cm.removeLeadingTrailingSymbs(msg)
        # new_msg = str(msg)
        # new_msg = cm.HEADING_WITH_PUNCT_MULTI.sub('', new_msg)
        # new_msg = cm.TRAILING_WITH_PUNCT_MULTI.sub('', new_msg)
        return new_msg

    def cleanBothEntries(self, msg, tran):

        new_msg = cm.removeLeadingTrailingSymbs(msg)
        new_tran = cm.removeLeadingTrailingSymbs(tran)

        # print(f'cleanBothEntries: msg:[{msg}]; tran:[{tran}]')
        #
        # cut_head_len = cut_tail_len = 0
        # msg_head, msg_trail = self.getHeadAndTailPuncts(msg)
        # print(f'msg_head:[{msg_head}]; msg_trail:[{msg_trail}]')
        #
        # tran_head, tran_trail = self.getHeadAndTailPuncts(tran)
        # print(f'tran_head:[{tran_head}]; tran_trail:[{tran_trail}]')
        #
        # cut_head_is_required = (msg_head and tran_head)
        # if cut_head_is_required:
        #     need_adjust = (len(msg_head) != len(tran_head))
        #     if need_adjust:
        #         cut_head_len = min(len(msg_head), len(tran_head))
        #     else:
        #         cut_head_len = len(msg_head)
        #
        # cut_tail_is_required = (msg_trail and tran_trail)
        # if cut_tail_is_required:
        #     need_adjust = (len(msg_trail) != len(tran_trail))
        #     if need_adjust:
        #         cut_tail_len = min(len(msg_trail), len(tran_trail))
        #     else:
        #         cut_tail_len = len(msg_trail)
        #
        # print(f'cut_head_len:[{cut_head_len}]; cut_tail_len:[{cut_tail_len}]')
        #
        # trim_head = (cut_head_len > 0)
        # trim_trail = (cut_tail_len > 0)
        # if trim_head:
        #     new_msg = new_msg[cut_head_len:]
        #     new_tran = new_tran[cut_head_len:]
        #     print(f'trim_head -- new_msg:[{new_msg}]; new_tran:[{new_tran}]')
        #
        # if trim_trail:
        #     new_msg = new_msg[:-cut_tail_len]
        #     new_tran = new_tran[:-cut_tail_len]
        #     print(f'trim_trail -- new_msg:[{new_msg}]; new_tran:[{new_tran}]')
        #
        # print(f'cleanBothEntries return -- new_msg:[{new_msg}]; new_tran:[{new_tran}]')
        return new_msg, new_tran

    def addEntryToChosenDict(self, msg, tran, dicfile_path, dict_list, indicator=''):
        tran = cm.cleanSlashesQuote(tran)
        msg = cm.cleanSlashesQuote(msg)

        has_tran = (tran is not None)
        if has_tran:
            tran = cm.removeOriginal(msg, tran)
            msg, tran = self.cleanBothEntries(msg, tran)
        else:
            msg = self.cleanOneEntry(msg)
            tran = ""

        is_in = (msg in dict_list)
        if not is_in:
            msg, tran = self.cleanBothEntries(msg, tran)
            is_in = (msg in dict_list)

        if is_in:
            current_tran = dict_list[msg]
            is_diff = (current_tran != tran)
            if is_diff:
                del dict_list[msg]
            else:
                return

        entry = {msg: tran}
        dict_list.update(entry)
        print(f'Added dict:[{msg}], [{tran}] to {indicator} file: [{dicfile_path}] ')

    def addMasterDict(self, msg, tran):
        self.addEntryToChosenDict(msg, tran, self.master_dic_file, self.master_dic, indicator='MASTER')

    def addBackupDictEntry(self, msg, tran):
        # dd('DEBUG')
        self.addEntryToChosenDict(msg, tran, self.master_dic_backup_file, self.backup_dic, indicator='BACKUP')

    def writeChosenDict(self, is_master=False):
        if is_master:
            self.writeMasterDict()
        else:
            self.writeBackupDict()

    def writeDict(self, dic_file, dic_list, indicator=''):
        self.writeJSONDic(dict_list=dic_list, file_name=dic_file)

    def writeBackupDict(self):
        dict_stat = self.writeDict(self.master_dic_backup_file, self.backup_dic, indicator='BACKUP')

    def writeMasterDict(self):
        dict_stat = self.writeDict(self.master_dic_file, self.master_dic, indicator='MASTER')

    def getKeyboardOriginal(self, text):
        # kbd_def_val = list(TranslationFinder.KEYBOARD_TRANS_DIC.values())
        orig_txt = str(text)
        for k, kbd_val in TranslationFinder.KEYBOARD_TRANS_DIC_PURE.items():
            is_in_text = (kbd_val in text)
            if is_in_text:
                text = text.replace(kbd_val, k)

            k_pattern = f' ({k})'
            is_in_text = (k_pattern in text)
            if is_in_text:
                text = text.replace(k_pattern, k)

            text = text.replace('()', '')
        return text

    def reloadChosenDict(self, is_master=True):
        if is_master:
            dd(f'reloadChosenDict:{self.master_dic_file}')
            self.master_dic = self.loadJSONDic(file_name=self.master_dic_file)
            if not self.master_dic:
                self.master_dic = {}
        else:
            dd(f'reloadChosenDict:{self.master_dic_backup_file}')
            self.backup_dic = self.loadJSONDic(file_name=self.master_dic_backup_file)
            if not self.backup_dic:
                self.backup_dic = {}

    def saveMasterDict(self, to_file=None):
        file_path = (to_file if to_file else self.master_dic_file)
        self.writeJSONDic(dict_list=self.master_dic, file_name=file_path)

    # def updateDict(self):
    #     from_file = '/Users/hoangduytran/blender_manual/ref_dict_0004.json'
    #     to_file = '/Users/hoangduytran/blender_manual/ref_dict_0005.json'
    #     new_file = '/Users/hoangduytran/blender_manual/ref_dict_0006.json'
    #
    #     new_dic = NoCaseDict()
    #     ignore_dic = NoCaseDict()
    #     from_dict = self.loadJSONDic(file_name=from_file)
    #     to_dict = self.loadJSONDic(file_name=to_file)
    #
    #     # sorting so the smaller keys get in first, avoiding duplications by the longer keys, ie. with ending '.' or ':'
    #     from_keys = list(sorted(from_dict.keys(), key=lambda x: len(x)))
    #     # debug_text = '2.30 <https://archive.blender.org/development/release-logs/blender-230/>`__ -- October 2003'
    #     meet = 0
    #     for k in from_keys:
    #         # 'Popther panel for adding extra options'
    #         trimmed_k, v, cover_length = self.findAndTrimIfNeeded(k, search_dict=new_dic, is_patching_found=False)
    #         if v:
    #             print(f'already in new_dic: k:{k}, trimmed_k:{trimmed_k}, v:{v}')
    #             continue
    #
    #         trimmed_k, v, cover_length  = self.findAndTrimIfNeeded(trimmed_k, search_dict=to_dict, is_patching_found=False)
    #         if not v:
    #             trimmed_k, v, cover_length = self.findAndTrimIfNeeded(k, search_dict=to_dict, is_patching_found=False)
    #
    #         if v:
    #             entry = {trimmed_k: v}
    #             new_dic.update(entry)
    #             print(f'found entry:{entry}')
    #         else:
    #             trimmed_k, v, cover_length = self.findAndTrimIfNeeded(k, search_dict=from_dict, is_patching_found=False)
    #             entry = {trimmed_k: v}
    #             ignore_dic.update(entry)
    #             print(f'ignored entry:{entry}')
    #
    #     to_keys = list(sorted(to_dict.keys(), key=lambda x: len(x)))
    #     for k in to_keys:
    #         trimmed_k, v, cover_length = self.findAndTrimIfNeeded(k, search_dict=new_dic, is_patching_found=False)
    #         is_in_new_dict = not (v is None)
    #         if is_in_new_dict:
    #             print(f'ignored entry in to_dict:{entry}')
    #             continue
    #
    #         trimmed_k, v, cover_length  = self.findAndTrimIfNeeded(k, search_dict=to_dict, is_patching_found=False)
    #         entry = {trimmed_k: v}
    #         new_dic.update(entry)
    #         print(f'added from to_file entry:{entry}')
    #
    #     from_dict_len = len(from_dict)
    #     to_dict_len = len(to_dict)
    #     new_dict_len = len(new_dic)
    #
    #     self.writeJSONDic(dict_list=new_dic, file_name=new_file)
    #     exit(0)

    def updateMasterDic(self, is_testing=True):
        from_dic_path = "/Users/hoangduytran/ref_dict_0002.json"
        from_dic_list = self.loadJSONDic(file_name=from_dic_path)
        changed_count = self.updateDicUsingDic(from_dic_list, self.master_dic)
        is_changed = (changed_count > 0)
        if is_changed:
            print("Changed:", changed_count)

        is_writing_changes = (is_changed and not is_testing)
        if is_writing_changes:
            print("Writing changes to:", self.master_dic_file)
            self.writeJSONDic(dict_list=self.master_dic, file_name=self.master_dic_file)

    def addEntry(self, msg, tran):

        entry = {msg: tran}
        print("addEntry - adding:", entry)
        # self.master_dic_list.update(entry)
        return True

    def updateDictUsingPOFile(self, po_file, is_master=False):
        self.loadVIPOtoDic(po_file, is_master, is_testing=False)
        if is_master:
            self.writeMasterDict()
        else:
            self.writeBackupDict()

    def loadVIPOtoDic(self, po_filename, is_master=False, is_testing=True):

        if not po_filename:
            return

        is_file_there = os.path.isfile(po_filename)
        if not is_file_there:
            return

        DIC_INCLUDE_LOWER_CASE_SET = False
        ignore = [
            "volume",
        ]

        changed_count = 0
        changed = False
        po_cat = c.load_po(po_filename)
        po_cat_dic = self.poCatToDic(po_cat)
        for k, v in po_cat_dic.items():
            is_ignore = (k.lower() in ignore)
            if is_ignore:
                continue

            self.addDictEntry((k, v), is_master)

    def replacePOText(self, po_file, rep_list, is_dry_run=True):
        dd("replacePOText:", po_file, rep_list, is_dry_run)
        data = None
        with open(po_file, "r") as f:
            data = f.read()

        changed = False
        for k, v in rep_list.items():
            data, change_count = re.subn(k, v, data, flags=re.M)
            is_changed = (change_count > 0)
            if is_changed:
                dd("CHANGED", change_count, k, "=>", v)

        if changed:
            dd(data)
            dd("file:", po_file)
            dd("Data has changed:", change_count)
            if not is_dry_run:
                with open(po_file, "w", encoding="utf-8") as f:
                    f.write(data)

    def cleanupPOFile(self, po_file, is_dry_run=True):

        po_cat = c.load_po(po_file)
        changed = False
        word_only = re.compile(r'([\w]+)')
        c.dump_po(po_file, po_cat)

        # for m in po_cat:
        #     k = m.id
        #     v = m.string
        #     has_v = (v is not None) and (len(v) > 0)
        #     if not has_v:
        #         continue

        #     is_k_empty = (len(k) == 0)
        #     if not is_k_empty:
        #         continue

        # m.flags.add('fuzzy')
        # changed = True
        # k_list = word_only.findall(k)
        # v_list = word_only.findall(v)
        # k_set = set(k_list)
        # v_set = set(v_list)

        # is_fuzzy = m.fuzzy
        # is_cleanable = (len(k_set) == len(v_set)) and (k_set == v_set) or is_fuzzy
        # if is_cleanable:
        #     if m.fuzzy:
        #         m.flags = set() # clear the fuzzy flags

        #     set_entry=(k_set, v_set)
        #     string_entry=(k, v)
        #     dd("cleanupPOFile - set_entry", set_entry)
        #     dd("cleanupPOFile - string_entry", string_entry)
        #     m.string = ""
        #     changed = True
        if changed:
            dd("cleanupPOFile", po_file)
            if (not is_dry_run):
                self.dump_po(po_file, po_cat)

    def cleanDictList(self, dic_list):
        remove_keys = []
        for k, v in dic_list.items():
            is_remove = (k is None) or (len(k) == 0) or ig.isIgnored(k)
            if is_remove:
                entry = {k: v}
                # dd("cleanDictList removing:", entry)
                remove_keys.append(k)
        for k in remove_keys:
            del dic_list[k]

    def updateDicUsingDic(self, source_dict, target_dict):
        target_change_count = 0
        for k, source_v in source_dict.items():

            is_in_target = (k in target_dict)
            if is_in_target:
                target_v = target_dict[k]
                is_same_v = (source_v == target_v)
                if is_same_v:
                    continue

            from_entry = {k: source_v}
            to_entry = {k: target_v}
            target_dict.update(from_entry)
            dd("Replacing:", to_entry)
            dd("With:", from_entry)
            target_change_count += 1
        return target_change_count

    def updatePOUsingDic(self, pofile, dic, is_testing=True):
        ignore = [
            "Volume",
        ]
        po_cat = c.load_po(pofile)
        changed = False
        for m in po_cat:
            k = m.id

            is_k_empty = (len(k) == 0)
            if is_k_empty:
                continue

            if k in ignore:
                continue

            is_in_dict = (k in dic)
            if not is_in_dict:
                continue

            po_v = m.string
            dic_v = dic[k]

            is_value_diff = (po_v != dic_v)
            if not is_value_diff:
                continue

            from_entry = {k: po_v}
            to_entry = {k: dic_v}
            dd("updatePOUsingDic, from:", from_entry, "to:", to_entry)
            m.string = dic_v
            changed = True

        if changed and (not is_testing):
            self.dump_po(pofile, po_cat)

    def mergeVIPODict(self):
        po_cat = c.load_po(self.vipo_dic_path)
        po_dic = self.poCatToDic(po_cat)
        self.master_dic.update(po_dic)

    def addEntryToDic(self, k, v, dict_list, keep_orig=False):
        valid = (k is not None) and \
                (len(k) > 0) and \
                (v is not None) and \
                (len(v) > 0)
        if not valid:
            return False

        if keep_orig:
            repeat_form = f'{v} -- {k}'
            normal_form = v
            has_original_in_tran = (k in v)
            if has_original_in_tran:
                v = normal_form
            else:
                v = repeat_form

        entry = {k: v}
        dict_list.update(entry)
        return True

    def loadPOAsDic(self, po_path):
        po_cat = c.load_po(po_path)
        po_dic = self.poCatToDic(po_cat)
        return po_dic, po_cat

    def poCatToDic(self, po_cat):
        po_cat_dic = defaultdict(OrderedDict)
        for index, m in enumerate(po_cat):
            is_first_entry = (index == 0)
            if is_first_entry:
                continue

            # context = (m.context if m.context else "")
            # dd("context:{}".format(context))
            # k = (m.id, context)
            k = m.id
            # is_ignore = (ig.isIgnored(k))
            # if is_ignore:
            #     continue

            v = m.string
            has_translation = (not m.fuzzy) and (v is not None) and (len(v) > 0)
            if not has_translation:
                continue

            entry = {k: v}
            po_cat_dic.update(entry)
        return po_cat_dic

    def setupKBDDicList(self):
        kbd_l_case = dict((k.lower(), v) for k, v in TranslationFinder.KEYBOARD_TRANS_DIC.items())
        TranslationFinder.KEYBOARD_TRANS_DIC.update(kbd_l_case)

    def writeJSONDic(self, dict_list=None, file_name=None):
        dic = {}
        try:
            if not file_name:
                return

            if not dict_list:
                return

            is_non_case_dic = isinstance(dict_list, NoCaseDict)
            if is_non_case_dic:
                dict: NoCaseDict = dict_list
                is_dirty = dict.is_dirty
                if not is_dirty:
                    return
            #
            # if not os.path.isfile(file_name):
            #     return

            file_path = (self.master_dic_file if (file_name is None) else file_name)
            dic = (self.master_dic if (dict_list is None) else dict_list)

            with open(file_path, 'w+', newline='\n', encoding='utf8') as out_file:
                json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            dd("Exception writeDictionary Length of read dictionary:{}".format(len(dic)))
            raise e

    def loadJSONDic(self, file_name=None):
        return_dic = None
        try:
            if not file_name:
                dd(f'loadJSONDic - file_name is None.')
                return return_dic

            if not os.path.isfile(file_name):
                dd(f'loadJSONDic - file_name:{file_name} cannot be found!')
                return return_dic

            file_path = (self.master_dic_file if (file_name is None) else file_name)
            dic = {}
            with open(file_path) as in_file:
                # dic = json.load(in_file, object_pairs_hook=NoCaseDict)
                dic = json.load(in_file)
            length = len(dic)
            dd(f'loadJSONDic - loaded dic, length:{length}')
            lcase_dict = {}
            for k, v in dic.items():
                entry = {k.lower(): v}
                lcase_dict.update(entry)
            dict_list = list(lcase_dict.items())
            sorted_dict_list = list(sorted(dict_list))
            temp_dict = OrderedDict(sorted_dict_list)
            return_dic = NoCaseDict(temp_dict)
            # cm.testDict(return_dic)

        except Exception as e:
            dd("Exception occurs while performing loadJSONDic()")
            dd(e)
            return_dic = NoCaseDict()

        return return_dic

    def getDict(self, local_dict=None):
        search_dict = (local_dict if local_dict else self.master_dic)
        if not search_dict:
            msg = 'isInDict() NO Dictionary is available. Stopped'
            print(msg)
            raise Exception(msg)
        return search_dict

    def isInDictFuzzy(self, msg, dic_to_use=None):
        untran_word_dic = {}
        # cm.debugging(msg)
        matched_text = msg
        search_dict = self.getDict(local_dict=dic_to_use)
        tran_sub_text = search_dict.findCache(msg)

        is_not_found = isinstance(tran_sub_text, bool)
        if is_not_found:
            return None, matched_text, search_dict, 0, untran_word_dic

        if tran_sub_text:
            return tran_sub_text, matched_text, search_dict, 100, untran_word_dic

        if not search_dict:
            msg = 'isInDictFuzzy(): NO Dictionary is available. Stopped'
            print(msg)
            raise Exception(msg)

        is_ignore = (not msg) or ig.isIgnored(msg)
        if is_ignore:
            return None, matched_text, search_dict, 0, untran_word_dic

        is_found = (msg in search_dict)
        if is_found:
            tran = search_dict[msg]
            matched_text = msg
            matching_ratio = 100.0
        else:
            tran, matched_text, matching_ratio, untran_word_dic = search_dict.simpleFuzzyTranslate(msg)

        if tran:
            tran = search_dict.replaceTranRef(tran)
            tran = cm.matchCase(msg, tran)
            cm.debugging(msg)
            dd(f'isInDictFuzzy: [{msg}] => [{tran}]')
        else:
            tran = None
        return tran, matched_text, search_dict, matching_ratio, untran_word_dic


    def isInDict(self, msg, dic_to_use=None):
        tran = None
        is_ignore = ig.isIgnored(msg)
        if is_ignore:
            return None

        search_dict = self.getDict(local_dict=dic_to_use)
        tran_sub_text = search_dict.findCache(msg)

        is_not_found = isinstance(tran_sub_text, bool)
        if is_not_found:
            return None

        if tran_sub_text:
            return tran_sub_text

        left = right = ""
        is_found = (msg in search_dict)
        if is_found:
            tran = search_dict[msg]
        else:
            tran = self.translateNumerics(msg)

        if not tran:
            msg_length = len(msg)
            left, stripped_msg, right = cm.getTextWithin(msg)
            is_already_done = (left == "" and right == "")
            if is_already_done:
                return None

            is_ignore = (not stripped_msg) or (ig.isIgnored(stripped_msg))
            if is_ignore:
                return None

            is_found = (stripped_msg in search_dict)
            if is_found:
                tran = search_dict[stripped_msg]
            else:
                tran = self.translateNumerics(stripped_msg)

        if tran:
            tran = search_dict.replaceTranRef(tran)
            tran = cm.matchCase(msg, tran)
            tran = left + tran + right
            dd(f'isInDict(): [{msg}] => [{tran}]')
        else:
            tran = None
        return tran

    def isInListByDict(self, msg, is_master):
        search_dic = (self.master_dic if is_master else self.backup_dic)
        tran = self.isInDict(msg, dic_to_use=search_dic)
        return tran

    def translationByRemovingSymbols(self, txt: str) -> str:
        new_txt, subcount = cm.SYMBOLS.subn('', txt)
        cover_length = 0
        if subcount > 0:
            is_ignore = ig.isIgnored(new_txt)
            if is_ignore:
                return txt, None, cover_length

            trans = self.isInDict(new_txt)
            if trans:
                cover_length = len(txt)
                trans = trans.strip()
                matched_text = txt.strip()
                trans = txt.replace(matched_text, trans)
                return new_txt, trans, cover_length
        return txt, None, cover_length

    def translateWords(self, txt: str):
        word_list_dict = cm.findInvert(cm.SYMBOLS, txt)
        temp_tran = str(txt)
        for loc, word in word_list_dict.items():
            tran_sub_text, matched_text, matching_ratio = self.tryFuzzyTranlation(word)
            if tran_sub_text:
                ss, ee = loc
                left = temp_tran[:ss]
                right = temp_tran[ee:]
                temp_tran = left + tran_sub_text + right
        has_tran = (temp_tran != txt)
        return (temp_tran if has_tran else None)

    def translationByReplacingSymbolsWithSpaces(self, txt: str):
        new_txt, subcount = cm.SYMBOLS.subn(' ', txt)
        cover_length = 0
        trans = None
        orig_txt = txt
        if subcount > 0:
            orig_txt = new_txt

        # there might be multiple spaced words here, must try to retain original symbols
        is_ignore = ig.isIgnored(orig_txt)
        if is_ignore:
            return txt, None, cover_length

        trans = self.isInDict(orig_txt)
        if not trans:
            trans = self.translateWords(orig_txt)

        if trans:
            cover_length = len(txt)
            trans = trans.strip()
            matched_text = txt.strip()
            trans = txt.replace(matched_text, trans)
            return new_txt, trans, cover_length

        return txt, None, cover_length

    def tryToFindTranslation(self, txt: str) -> str:
        cover_length = 0
        separator_list = [
            cm.SPACES,
            cm.SYMBOLS,
        ]
        selective_list = []

        input_txt = str(txt)
        sent_struct = self.getSentStruct(txt)
        is_tran_sent_struct = bool(sent_struct)
        if is_tran_sent_struct:
            txt = sent_struct.km_txt

        new_text, trans, cover_length = self.findByReduction(txt)
        is_found_trans = (trans and not trans == txt)
        if is_found_trans:
            if is_tran_sent_struct:
                sent_struct.tm_txt = trans
                txt = input_txt
                trans = sent_struct.getTranslated()

            return txt, trans, cover_length

        for separator in separator_list:
            temp_masking_text = str(txt)
            found_dict = cm.findInvert(separator, txt, is_removing_surrounding_none_alphas=True)
            if not found_dict:
                continue

            translated_dict = {}
            translation = str(txt)
            for loc, orig_txt in found_dict.items():
                s, e = loc

                is_ignore = ig.isIgnored(orig_txt)
                if is_ignore:
                    continue

                new_text = str(orig_txt)
                trans = self.isInDict(orig_txt)
                if not trans:
                    tran_sub_text, matched_text, matching_ratio = self.tryFuzzyTranlation(orig_txt)
                else:
                    matched_text = orig_txt

                if trans:
                    cover_length = len(matched_text)

                if not trans:
                    new_text, trans, cover_length = self.findByReduction(orig_txt)

                is_found_trans = (trans and not trans == orig_txt)
                if is_found_trans:
                    trans = cm.insertTranslation(orig_txt, new_text, trans)
                    translated_entry = {loc: (orig_txt, trans)}
                    translated_dict.update(translated_entry)

            for loc, v in translated_dict.items():
                orig_txt, trans = v
                s, e = loc
                left = translation[:s]
                right = translation[e:]
                translation = left + trans + right
                cover_length += len(orig_txt)

                empty_string = (' ' * len(orig_txt))
                temp_masking_text = temp_masking_text[:s] + empty_string + temp_masking_text[e:]

            entry = (cover_length, txt, translation)
            selective_list.append(entry)

            loc, test_masking_text = cm.removingNonAlpha(temp_masking_text)
            is_finish_loop = (len(test_masking_text) == 0)
            if is_finish_loop:      # no need to carry on to the next variance of separator
                break

        if not selective_list:
            txt = input_txt
            if is_tran_sent_struct:
                translation = sent_struct.getNonTranslated()
                cover_length = len(input_txt)
            else:
                translation = None
                cover_length = 0
        else:
            sorted_selective_list = list(sorted(selective_list, reverse=True))
            chosen_entry = sorted_selective_list[0]
            cover_length, txt, translation = chosen_entry

            if is_tran_sent_struct:
                sent_struct.tm_txt = translation
                txt = input_txt
                translation = sent_struct.getTranslated()
                cover_length = len(input_txt)

        return txt, translation, cover_length

    def removeStarAndEndingPunctuations(self, txt):
        new_txt = cm.ENDS_PUNCTUAL_MULTI.sub('', txt)
        new_txt = cm.BEGIN_PUNCTUAL_MULTI.sub('', new_txt)

        cover_length = 0
        # dd(f'removeStarAndEndingPunctuations: {txt} => {new_txt}')

        trans = self.isInDict(new_txt)
        if trans:
            cover_length = len(txt)
            dd(f'removeStarAndEndingPunctuations: FOUND {new_txt} => {trans}')
        return new_txt, trans, cover_length

    def fixTranslationWithKnowsPrefixSuffixes(self, txt, trans, is_prefix=False):
        new_txt = str(trans)
        # pp(cm.common_sufix_translation)
        fix_translation_list = (cm.common_prefix_translation if is_prefix else cm.common_sufix_translation)
        for fix_term, (position, add_translation) in fix_translation_list:

            if is_prefix:
                has_fix_term = txt.startswith(fix_term)
            else:
                has_fix_term = txt.endswith(fix_term)

            if not has_fix_term:
                continue

            is_at_front = (position == cm.START_WORD)
            is_at_end = (position == cm.END_WORD)
            is_patching_front = (is_at_front and not new_txt.startswith(add_translation))
            is_patching_end = (is_at_end and not new_txt.endswith(add_translation))

            # dd(f'fixTranslationWithKnowsSuffixes: is_patching_front:{is_patching_front} is_patching_end:{is_patching_end} ')
            # dd(f'txt:{txt}; fix_term:{fix_term}; position:{position}')
            if is_patching_front:
                # dd(f'is_patching_front: add_translation={add_translation}')
                # dd(f'is_patching_front: Befor adding; new_txt={new_txt}')
                new_txt = add_translation + ' ' + new_txt
                # dd(f'is_patching_front: new_txt={new_txt}')
                return new_txt

            if is_patching_end:
                # dd(f'is_patching_end: add_translation={add_translation}')
                new_txt += ' ' + add_translation
                # dd(f'is_patching_end: new_txt={new_txt}')
                return new_txt
        return trans

    def reduceDuplicatedEnding(self, txt):
        is_double_ending = (len(txt) > 2) and (txt[-1] == txt[-2])
        if is_double_ending:
            # dd(f'is_double_ending txt:{txt}')
            test_text = txt[:-1]
            trans = self.isInDict(test_text)
            if trans:
                return test_text, trans
        return txt, None

    def replaceEndings(self, part, clipped_txt: str):
        def checkTranslationForText(test_text):
            trans = self.isInDict(test_text)
            if trans:
                return test_text, trans, True

            chopped_txt, trans = self.reduceDuplicatedEnding(test_text)
            if trans:
                return chopped_txt, trans, True
            return test_text, None, False

        if ig.isIgnored(clipped_txt):
            return None, None

        for replacement_word, ending_list in cm.common_suffixes_replace_dict.items():
            for ending in ending_list:
                part_matched = (part == ending)
                if not part_matched:
                    continue

                p = r'%s$' % ending
                test_text_less, less_rep_count = re.subn(p, '', clipped_txt)
                test_text_with, with_rep_count = re.subn(p, ending, clipped_txt)
                test_text_more = (clipped_txt + replacement_word)

                test_text, trans, has_translation = checkTranslationForText(test_text_more)
                if has_translation:
                    return test_text, trans

                has_ending_and_text_has_changed = (less_rep_count > 0) or (with_rep_count > 0)
                if has_ending_and_text_has_changed:
                    test_text, trans, has_translation = checkTranslationForText(test_text_less)
                    if has_translation:
                        return test_text, trans

                    test_text, trans, has_translation = checkTranslationForText(test_text_with)
                    if has_translation:
                        return test_text, trans

        return None, None

    def removeBothByPatternListAndCheck(self, txt, prefix_list, suffix_list):
        cover_length = 0
        suffixed_list = []
        for part in suffix_list:
            part_len = (len(part))
            has_suffix = (txt.endswith(part))
            if not has_suffix:
                continue

            test_text = txt[:-part_len]
            suffixed_list.append(test_text)

        prefixed_list = []
        for suffixed_word in suffixed_list:
            for part in prefix_list:
                part_len = (len(part))
                has_prefix = (txt.startswith(part))
                if not has_prefix:
                    continue

                test_text = suffixed_word[part_len:]
                prefixed_list.append(test_text)

        for test_text in prefixed_list:
            matched_text = test_text
            tran = self.isInDict(test_text)
            if not tran:
                is_double_ending = (len(test_text) > 2) and (test_text[-1] == test_text[-2])
                if is_double_ending:
                    test_text = test_text[:-1]
                    tran = self.isInDict(test_text)

            if tran:
                cover_length = len(matched_text)
                return test_text, tran, cover_length
        return txt, None, cover_length

    def removeByPatternListAndCheck(self, txt, part_list, at):


        cover_length = 0
        tran = self.isInDict(txt)
        if tran:
            cover_length = len(txt)
            return txt, tran, cover_length

        start_non_alpha, mid, end_non_alpha = cm.getTextWithin(txt)
        is_at_start = (at == cm.START_WORD)
        is_at_end = (at == cm.END_WORD)
        test_text = str(txt)
        cover_length = 0
        if is_at_start:
            test_text = cm.NON_WORD_STARTING.sub("", test_text)
        elif is_at_end:
            test_text = cm.NON_WORD_ENDING.sub("", test_text)

        word_len = len(test_text)
        text_before_cutoff = str(test_text)
        # pp(part_list)
        for part in part_list:
            cover_length = 0
            part_len = len(part)
            if part_len >= word_len:
                break

            has_start = is_at_start and (text_before_cutoff.startswith(part))
            has_end = is_at_end and (text_before_cutoff.endswith(part))
            # if 'r' in part:
            #     dd(f'removeByPatternListAndCheck: part: {part}; test_text:{test_text}; has_start:{has_start}; has_end:{has_end}')
            if has_start:
                test_text = text_before_cutoff[part_len:]
                test_text = cm.NON_WORD_STARTING.sub("", test_text)
                # dd(f'removeByPatternListAndCheck: has_start: {part}; test_text:{test_text}')
            elif has_end:
                test_text = text_before_cutoff[:-part_len]
                test_text = cm.NON_WORD_ENDING.sub("", test_text)
                # dd(f'removeByPatternListAndCheck: has_end: {part}; test_text:{test_text}')
            else:
                continue

            # this is to fix the 'hop' (should be hopping), and 'hope' (should be hoping)
            should_have_duplicated_ending = cm.shouldHaveDuplicatedEnding(part, test_text)
            if should_have_duplicated_ending:
                chopped_txt, tran = self.replaceEndings(part, test_text)
                fix_tran = bool((chopped_txt) and \
                                (chopped_txt not in cm.verb_with_ending_y) and \
                                (chopped_txt not in cm.verb_with_ending_s))
                if tran:
                    cover_length = len(text_before_cutoff)
                    if fix_tran:
                        tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                    return test_text, tran, cover_length

            tran = self.isInDict(test_text)
            if tran:
                cover_length = len(test_text)
                if has_end:
                    # dd('has_end')
                    tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                elif has_start:
                    # dd('has_start')
                    tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=True)
                return test_text, tran, cover_length
            else:
                fix_tran = True
                chopped_txt, tran = self.replaceEndings(part, test_text)
                fix_tran = bool((chopped_txt) and \
                                (chopped_txt not in cm.verb_with_ending_y) and \
                                (chopped_txt not in cm.verb_with_ending_s))
                if tran:
                    cover_length = len(text_before_cutoff)
                    if fix_tran:
                        tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                    return test_text, tran, cover_length
                else:
                    chopped_txt, tran = self.reduceDuplicatedEnding(test_text)
                    if tran:
                        cover_length = len(text_before_cutoff)
                        tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                        return chopped_txt, tran, cover_length

            chopped_txt, tran = self.reduceDuplicatedEnding(text_before_cutoff)

            if tran:
                cover_length = len(text_before_cutoff)
                if is_at_end:
                    tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                elif is_at_start:
                    tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                return test_text, tran, cover_length

        return txt, None, cover_length

    def removeInfixAndCheck(self, txt, infix_list):
        # 1. generate a list of patterns with infix being removed or replaced by spaces
        # 2. sort patterns list using the accending order of number of replacements, so the entry with least changes goes first,
        #   the entry with most changes goes last
        # 3. running through the pattern list and check to see which produce a result
        has_infix = False
        for infix in infix_list:
            if (infix in txt):
                has_infix = True
        if not has_infix:
            return txt, None

    def isNonGATranslatedFully(self, msg, trans):
        is_ga = (cm.GA_PATTERN_PARSER.search(msg) is not None)
        if is_ga:
            return True

        is_ga = (cm.GA_PATTERN_PARSER.search(trans) is not None)
        if is_ga:
            return True

        orig_word_list = msg.split()
        for word in orig_word_list:
            is_ignored = ig.isIgnored(word)
            if is_ignored:
                continue
            is_in_trans = (word in trans)
            if is_in_trans:
                return False
        return True

    def findTranslation(self, msg):
        trans = None
        is_fuzzy = False
        is_ignore = ig.isIgnored(msg)
        if (is_ignore):
            return None, is_fuzzy, is_ignore

        orig_msg = str(msg)
        trans = self.isInDict(orig_msg)
        is_found = (trans is not None) and not (trans == orig_msg)
        # if not is_found:
        #     print('trying fuzzy')
        #     trans = self.isInDict(msg, find_fuzzy=True)
        #     print(f'result of isInDect find_fuzzy=True :[{orig_msg}] => [{trans}]')
        #     is_fuzzy = True

        has_tran = not (trans is None)
        has_len = (has_tran and (len(trans) > 0))
        has_translation = has_len and (trans != 'None')
        if has_translation:
            # print(f'result of isInDict:[{orig_msg}] => [{trans}] => is_found: [{is_found}]')
            trans = cm.removeOriginal(msg, trans)
            trans = self.removeTheWord(trans)
        else:
            trans = None
        if trans is None:
            dd(f"NOT found: [{msg}]")
        return trans, is_fuzzy, is_ignore

    def findTranslationByFragment(self, msg):
        # orig_msg = str(msg)
        trans_list = []
        trans = str(msg)

        word_list = cm.WORD_ONLY_FIND.findall(msg)

        dd(f'word_list: {word_list}')
        result_dict = cm.patternMatchAll(cm.WORD_ONLY_FIND, msg)
        for loc, mm in result_dict.items():
            (o_s, o_e), o_txt = mm.getOriginAsTuple()
            is_possessive = o_txt.endswith("'s")
            if is_possessive:
                o_txt = o_txt[:-2]
            trans_word, is_fuzzy, is_ignore = self.findTranslation(o_txt)
            if is_ignore:
                continue

            if is_possessive:
                trans_word = f'của {trans_word}'
            trans_word_entry = (o_s, o_e, o_txt, trans_word)
            trans_list.append(trans_word_entry)

        has_result = (len(trans_list) > 0)
        if not has_result:
            return None

        for s, e, orig, trans_word in reversed(trans_list):
            if trans_word:
                st = trans[:s]
                se = trans[e:]
                trans = st + trans_word + se

        return trans

    def removeTheWord(self, trans):
        try:
            trans = cm.THE_WORD.sub("", trans)
        except Exception as e:
            pass
        return trans

    def translate(self, msg):
        trans = None
        old_msg = str(msg)
        try:
            sent_struct = self.getSentStruct(msg)
            is_tran_sent_struct = bool(sent_struct)
            if is_tran_sent_struct:
                msg = sent_struct.km_txt

            dd(f'calling findTranslation')
            is_fuzzy = False
            trans, is_fuzzy, is_ignore = self.findTranslation(msg)
            if is_ignore:
                trans = None
                if is_tran_sent_struct:
                    is_ignore = False
                    trans = sent_struct.getNonTranslated()
                return (trans, False, is_ignore)

            if not trans:
                dd(f'calling tryFuzzyTranlation')
                trans, cover_length, matching_ratio = self.tryFuzzyTranlation(msg)
                is_fuzzy = bool(trans)

            if not trans:
                dd(f'calling blindTranslation')
                trans = self.blindTranslation(msg)
                is_fuzzy = True

            if trans:
                is_same = (trans == msg)
                if is_same:
                    trans = None
                    if is_tran_sent_struct:
                        trans = sent_struct.getNonTranslated()
                else:
                    if is_tran_sent_struct:
                        sent_struct.tm_txt = trans
                        trans = sent_struct.getTranslated()

                    dd(f'calling removeTheWord')
                    trans = self.removeTheWord(trans)
                    trans = cm.matchCase(msg, trans)
            return (trans, is_fuzzy, is_ignore)
        except Exception as e:
            print(f'ERROR: {e} - msg:[{msg}], trans:[{trans}]')
            raise e

    def translateKeyboard(self, msg):
        orig = str(msg)
        trans = str(msg)
        cm.debugging(msg)
        result_dict = cm.patternMatchAll(cm.KEYBOARD_SEP, msg)
        for loc, mm in result_dict.items():
            (s, e), txt = mm.getOriginAsTuple()
            # has_dic = (txt in TranslationFinder.KEYBOARD_TRANS_DIC)
            has_dic = (txt in self.kbd_dict)
            if not has_dic:
                continue

            # tr = TranslationFinder.KEYBOARD_TRANS_DIC[txt]
            tr = self.kbd_dict[txt]
            ll = trans[:s]
            rr = trans[e:]
            trans = ll + tr + rr

        is_fuzzy = False
        is_ignore = False
        is_the_same = (orig == trans)
        if is_the_same:
            trans = None
            is_fuzzy = True
        return trans, is_fuzzy, is_ignore

    def checkIgnore(self, msg):
        is_pure_path = (cm.PURE_PATH.search(msg) is not None)
        is_pure_ref = (cm.PURE_REF.search(msg) is not None)
        is_api_ref = (cm.API_REF.search(msg) is not None)
        is_keep = (ig.isKeep(msg))
        is_keep_contain = (ig.isKeepContains(msg))
        is_ignore = (is_pure_path or is_pure_ref or is_api_ref) and (not (is_keep or is_keep_contain))
        return is_ignore

    def addExtraChar(self, msg, ref_type=None):
        char_tbl = {
            RefType.SNG_QUOTE: "'",
            RefType.DBL_QUOTE: '"',
            RefType.AST_QUOTE: '*'
        }

        insert_char = char_tbl[ref_type]
        if insert_char:
            msg = f'{insert_char}{msg}{insert_char}'
        return msg

    def translateQuoted(self, msg, is_reversed=False, ref_type=None):
        is_fuzzy = False
        is_ignore = self.checkIgnore(msg)
        if is_ignore:
            return None, is_fuzzy, is_ignore

        tran, is_fuzzy, is_ignore = self.translate(msg)
        tran_found = (tran is not None)
        if not tran_found:
            return None, False, False

        if is_ignore:
            return None, is_fuzzy, is_ignore

        abbr_str = RefType.ABBR.value
        has_abbr = (abbr_str in tran)
        if has_abbr:
            return tran, is_fuzzy, is_ignore

        orig_msg = str(msg)
        ex_ga_msg = cm.EXCLUDE_GA.findall(msg)
        if (len(ex_ga_msg) > 0):
            msg = ex_ga_msg[0]

        msg = cm.replaceArchedQuote(msg)
        msg = self.addExtraChar(msg, ref_type=ref_type)
        if tran_found:
            orig_tran = str(tran)
            ex_ga_msg = cm.EXCLUDE_GA.findall(tran)
            if (len(ex_ga_msg) > 0):
                tran = ex_ga_msg[0]

            tran = cm.replaceArchedQuote(tran)
            tran = self.addExtraChar(tran, ref_type=ref_type)
            tran = f"{abbr_str}`{tran} ({msg})`"
        else:
            tran = f"{abbr_str}`{msg} ({msg})`"
        return tran, is_fuzzy, is_ignore

    def recomposeAbbrevTranslation(self, msg, tran):
        has_tran = (tran and not tran is None)
        if not has_tran:
            return tran

        has_abbr = (cm.ABBREV_CONTENT_PARSER.search(tran) is not None)
        if not has_abbr:
            return tran

        abbrev_orig_rec, abbrev_part, exp_part = cm.extractAbbr(tran)
        print(f'abbrev_orig_rec:{abbrev_orig_rec} abbrev_part:{abbrev_part} exp_part:{exp_part}')
        loc, orig = abbrev_orig_rec
        s, e = loc
        left = tran[:s]
        right = tran[e:]
        tran = left + f'{abbrev_part}: {exp_part}' + right
        tran = cm.removeOriginal(msg, tran)
        return tran

    def translateRefWithLink(self, msg: str, ref_type: RefType):  # for things like :doc:`something <link>`, and :term:`something <link>`
        def formValue(loc_orig, loc_tran):
            if not tran:                
                loc_value = f"{orig_txt} ()"
            else:
                loc_value = f"{orig_txt} ({tran})"
            return loc_value

        ref_is_fuzzy = False
        ref_is_ignore = self.checkIgnore(msg)
        if ref_is_ignore:
            return None, ref_is_fuzzy, ref_is_ignore

        tran_txt = str(msg)

        has_ref_link = (cm.REF_LINK.search(msg) is not None)
        if has_ref_link:
            found_list = cm.findInvert(cm.REF_LINK, msg)
            for loc, orig_txt in reversed(list(found_list.items())):
                s, e = loc
                tran, is_fuzzy, is_ignore = self.translate(orig_txt)
                if is_ignore:
                    continue

                if is_fuzzy:
                    ref_is_fuzzy = True

                tran_found = (tran and tran != orig_txt)
                if tran_found:
                    tran_txt = tran
                    # solving the problem :term:`:abbr:`something (explanation)``
                    # tran = self.recomposeAbbrevTranslation(orig_txt, tran)
                    is_abbrev = (cm.ABBREV_PATTERN_PARSER.search(tran) is not None)
                    if not is_abbrev:
                        tran = formValue(orig_txt, tran)
                else:
                    tran = formValue(orig_txt, tran)
                tran_txt = tran_txt[:s] + tran + tran_txt[e:]
        else:
            orig_txt = msg
            tran, ref_is_fuzzy, ref_is_ignore = self.translate(orig_txt)
            if ref_is_ignore:
                return None, ref_is_fuzzy, ref_is_ignore

            tran_found = (tran and tran != orig_txt)
            if tran_found:
                tran_txt = tran
                # tran = self.recomposeAbbrevTranslation(orig_txt, tran)
                is_abbrev = (cm.ABBREV_PATTERN_PARSER.search(tran) is not None)
                if not is_abbrev:
                    tran_txt = formValue(orig_txt, tran)
            else:
                tran_txt = formValue(orig_txt, tran)
        return tran_txt, ref_is_fuzzy, ref_is_ignore

    def translateMenuSelection(self, msg):
        men_is_fuzzy = False
        men_is_ignore = False
        tran_txt = str(msg)
        fuzzy_count = 0
        ignore_count = 0
        word_list = cm.findInvert(cm.MENU_SEP, msg)
        word_count = len(word_list)
        for loc, word in word_list.items():
            s, e = loc
            tran, is_fuzzy, is_ignore = self.translate(word)
            fuzzy_count += (1 if is_fuzzy else 0)
            ignore_count += (1 if is_ignore else 0)
            if is_ignore:
                continue

            has_abbr = cm.hasAbbr(tran)
            if has_abbr:
                abbr_orig, abbr_marker, abbr_exp = cm.extractAbbr(tran)
                loc, abbr_txt = abbr_marker
                orig_loc, orig_txt = abbr_orig
                os, oe = orig_loc
                left = tran[:os]
                right = tran[oe:]
                tran = left + abbr_txt + right
                dd('debug translateMenuSelection hasAbbr')

            is_tran_valid = (tran and (tran != word))
            if is_tran_valid:
                entry = f"{tran} ({word})"
            else:
                entry = f"({word})"

            left = tran_txt[:s]
            right = tran_txt[e:]
            tran_txt = left + entry + right

        men_is_fuzzy = (fuzzy_count > 0)
        men_is_ignore = (ignore_count == word_count)

        return tran_txt, men_is_fuzzy, men_is_ignore

    def translateAbbrev(self, msg: str) -> list:
        '''
            translateAbbrev: Routine to parse abbreviation entry, such as:
            :abbr:`JONSWAP (JOint North Sea WAve Project)`.
            The routine will capture the part within brackets and translating
            that part, rejoins the translation with original text:
            'JONSWAP (JOint North Sea WAve Project -- <translation part>)'
        :param msg:
            text which contains the part within grave accents (GA), ie.
            JONSWAP (JOint North Sea WAve Project)
        :return:
            'JONSWAP (JOint North Sea WAve Project -- <translation part>)' if has translationm, else
            'JONSWAP (JOint North Sea WAve Project -- <translation part>)'
        '''
        tran_txt = str(msg)
        all_matches = cm.patternMatchAll(cm.ABBR_TEXT, msg)
        if not all_matches:
            return None, False, False

        is_fuzzy_list = []
        is_ignore_list = []
        mm: MatcherRecord = None
        all_matches_list = list(all_matches.items())
        first_match = all_matches_list[0]
        loc, mm = first_match

        (ss, ee), orig = mm.getOriginAsTuple()
        first_entry = mm.getSubEntryByIndex(0)
        loc, abbrev_explain_txt = first_entry

        tran, is_fuzzy, is_ignore = self.translate(abbrev_explain_txt)
        is_fuzzy_list.append(is_fuzzy)
        is_ignore_list.append(is_ignore)

        if is_ignore:
            return None, False, False

        valid = (tran and (tran != abbrev_explain_txt))
        if valid:
            entry = f"{abbrev_explain_txt} -- {tran}"
        else:
            entry = f"{abbrev_explain_txt} -- "
        tran_txt = tran_txt[:s] + entry + tran_txt[e:]

        some_ignore = (True in is_ignore_list)
        some_not_ignore = (False not in is_ignore_list)
        some_fuzzy = (True not in is_fuzzy_list)

        is_ignore = some_ignore and not (some_not_ignore or some_fuzzy)
        is_fuzzy = (True in is_fuzzy_list)
        return tran_txt, is_fuzzy, is_ignore

    def translateOSLAttrrib(self, msg: str):
        if not msg:
            return None, False, False

        tran_txt = str(msg)
        is_fuzzy_list=[]
        is_ignore_list=[]
        word_list_dict = cm.findInvert(cm.COLON_CHAR, tran_txt)
        word_list_count = len(word_list_dict)
        for loc, orig_txt in word_list_dict.items():
            s, e = loc
            tran, is_fuzzy, is_ignore = self.translate(orig_txt)
            is_fuzzy_list.append(is_fuzzy)
            is_ignore_list.append(is_ignore)
            has_tran = (tran and tran != orig_txt)
            if has_tran:
                left = tran_txt[:s]
                right = tran_txt[e:]
                tran_txt = left + tran + right

        has_tran = (tran_txt != msg)
        if not has_tran:
            tran_txt = f'{msg} -- '
            return None, False, False
        else:
            is_fuzzy = (True in is_fuzzy_list)
            is_ignore = (not is_fuzzy) and (True in is_ignore_list) and (False not in is_ignore_list)
            tran_txt = f'{msg} ({tran_txt})'
            return tran_txt, is_fuzzy, is_ignore

    def removeIgnoredEntries(self, dic_list):
        valid = (dic_list is not None) and (len(dic_list) > 0)
        if not valid:
            return

        # hold keys to be removed
        blank_key = []
        remove_key = []
        for k, v in dic_list.items():
            is_ignore = (ig.isIgnored(k))
            if is_ignore:
                dd("mark for removal:", k, v)
                remove_key.append(k)

            # remove null from v
            has_value = (v is not None)
            if not has_value:
                dd("mark due to blanking value:", k, v)
                blank_key.append(k)

        for k in blank_key:
            dd("actually blanking:", k)
            entry = {k: ""}
            dic_list.update(entry)

        # run through the keys and remove entry from the dic_list
        for k in remove_key:
            dd("acutally removing:", k)
            del dic_list[k]
