import concurrent.futures

import os
import time
from collections import OrderedDict
from common import Common as cm, dd, pp, LocationObserver
from definition import Definitions as df, \
    SentStructMode as SMODE, \
    SentStructModeRecord as SMODEREC

from key import Key
from fuzzywuzzy import fuzz, process as fuzz_process
import operator as OP
import inspect as INP
import re
from ignore import Ignore as ig

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
        self.numerical_pat_list = []

        self.fuzzy_exp_var_chosen_record = None
        self.global_text_match = {}
        self.local_cache = {}
        self.local_keylist_cache = {}
        self.local_text_and_chosen_sent_struct_list = {}
        self.local_pattern_and_value_for_sent_struct_list = {}

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
        self.initNumericalPatternList()

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
            # dd(f'__getitem__:[{key}], value:[{value}]')
            return value
        except Exception as e:
            df.LOG(f'{e}', error=True)
            return None

    def createSentenceStructureDict(self):
        def sortingKeyFunction(item):
            (pattern, value_part) = item
            pattern_length = len(pattern)
            return pattern_length

        def isSentStruct(item):
            (k, v) = item
            is_sent_struct = (df.SENT_STRUCT_START_SYMB_PAT.search(k) is not None)
            # is_sent_struct = ('EQ(Edit' in k)
            return is_sent_struct

        def createDictEntry(data):
            (key, value) = data
            value = self.replaceTranRef(value)
            key_pattern = cm.creatSentRecogniserPattern(key)
            dict_sl_mm, dict_sl_word_list = cm.createSentRecogniserRecord(key)
            dict_tl_mm, dict_tl_word_list = cm.createSentRecogniserRecord(value)

            value = (key, dict_sl_word_list, dict_sl_mm, value, dict_tl_word_list, dict_tl_mm)
            entry = (key_pattern, value)
            return entry

        def sortSentStruct(item):
            (k, v) = item
            return (k)

        temp_dict={}
        temp_set = list(filter(isSentStruct, self.items()))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            found_results = executor.map(createDictEntry, temp_set)

        found_list = list(found_results)
        found_list.sort(key=sortingKeyFunction, reverse=True)

        temp_dict = OrderedDict(found_list)
        self.sentence_struct_dict = NoCaseDict(temp_dict)

    def get(self, k, default=None):
        return self[k] if k in self else default

    def getSentStructPattern(self, key):
        def validate_NUMBER_ONLY(args):
            smode_rec, interest_part, matched_part, extra_param = args
            valid = (df.NUMBERS.search(matched_part) is not None)
            return valid

        def validate_NO_FULL_STOP(args):
            smode_rec, interest_part, matched_part, extra_param = args
            valid = (df.FULLSTOP_IN_BETWEEN.search(matched_part) is None)
            return valid

        def validate_NO_PUNCTUATION(args):
            smode_rec, interest_part, matched_part, extra_param = args
            valid = (df.PUNCT_IN_BETWEEN.search(matched_part) is None)
            return valid

        def validate_MAX_UPTO(args):
            smode_rec, interest_part, matched_part, extra_param = args
            wc = cm.wordCount(matched_part)
            valid = (wc <= extra_param)
            return valid

        def validate_NO_CONJUNCTIVES(args):
            smode_rec, interest_part, matched_part, extra_param = args
            valid = (df.BASIC_CONJUNCTS.search(matched_part) is None)
            # if valid:
            #     grp = valid.groups()
            return valid

        def validate_EXCLUDE(args):
            smode_rec, interest_part, matched_part, extra_param = args

            ex_txt = smode_rec.smode_txt
            embs = df.CLAUSED_PART.search(ex_txt)
            ex_value = embs.group(1)
            pat = re.compile(ex_value, flags=re.I)

            strip_matched_part = matched_part.strip()
            match = pat.search(strip_matched_part)
            valid = (match is None)
            return valid

        def validate_EMBEDDED(args):
            smode_rec, interest_part, matched_part, extra_param = args
            valid = True
            for loc, txt in interest_part:
                is_leading_with_hyphen = (txt.startswith('-'))
                if is_leading_with_hyphen:
                    return False

            return valid

        def isMatchedStructMode(pat_matched_text_pair_list):
            is_ok_list=[]
            (s_mode_dict, input_txt_list, matcher_dict) = pat_matched_text_pair_list
            s_mode_dict_list = list(s_mode_dict.values())
            check_list = {
                SMODE.NUMBER_ONLY: validate_NUMBER_ONLY,
                SMODE.NO_FULL_STOP: validate_NO_FULL_STOP,
                SMODE.NO_PUNCTUATION: validate_NO_PUNCTUATION,
                SMODE.MAX_UPTO: validate_MAX_UPTO,
                SMODE.NO_CONJUNCTIVES: validate_NO_CONJUNCTIVES,
                SMODE.EMBEDDED_WITH: validate_EMBEDDED,
                SMODE.LEADING_WITH: validate_EMBEDDED,
                SMODE.TRAILING_WITH: validate_EMBEDDED,
                SMODE.EXCLUDE: validate_EXCLUDE,
            }

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

                    is_checking = (structure_mode in check_list)
                    if not is_checking:
                        continue

                    function = check_list[structure_mode]
                    args = (smode_rec, matcher_dict, matched_part, extra_param)
                    is_ok = function(args)
                    is_ok_list.append(is_ok)
                    if not is_ok:
                        df.LOG(f'function [{function.__name__}()] FAILED! matched_part:[{matched_part}], extra_param:[{extra_param}]')

            ok = (False not in is_ok_list)
            return ok

        def filterKeyByTextAndPattern(item):
            try:
                (txt, pattern, value) = item
                match = re.compile(pattern, flags=re.I).search(txt)
                return (match, pattern, value)
            except Exception as e:
                df.LOG(f'[{e}]; item:[{item}]')

        def filterByFuzzyCompare(item):
            (txt, pattern, matcher, value) = item
            orig_pat_txt = value[0]
            ratio = fuzz.ratio(txt, orig_pat_txt)
            return (ratio, txt, pattern, matcher, value)

        def findMatchingPattern(txt, pattern_list):
            map_args = [(txt, pattern, value) for (pattern, value) in pattern_list]
            with concurrent.futures.ThreadPoolExecutor() as executor:
                found_results = executor.map(filterKeyByTextAndPattern, map_args)

            found_list=[]
            for result in found_results:
                (matcher, pattern, value) = result
                if matcher:
                    found_list.append(result)
                    # df.LOG(f'FOUND: [{result}]')

            is_found = bool(found_list)
            if not is_found:
                return (None, None, None)

            # df.LOG(f'found_list:')
            # pp(found_list)

            map_args = [(txt, pattern, matcher, value) for (matcher, pattern, value) in found_list]
            with concurrent.futures.ThreadPoolExecutor() as executor:
                found_results = executor.map(filterByFuzzyCompare, map_args)


            found_result_list = list(found_results)
            found_result_list.sort(reverse=True)

            found_item = found_result_list[0]
            (ratio, txt, pattern, matcher, value) = found_item
            return_item = (pattern, matcher, value)

            df.LOG(f'SORTED found_results for [{key}]')
            pp(found_item)

            return return_item

        try:
            default_value = (None, None, None, None, None, None, None)
            # has_cached_key_value_set = (klower in self.local_text_and_chosen_sent_struct_list)
            # if has_cached_key_value_set:
            #     set_value = self.local_text_and_chosen_sent_struct_list[klower]
            #     (pat, value) = set_value
            #     return (pat, value)

            st_counter = time.perf_counter()
            (pattern, matcher, value) = findMatchingPattern(key, self.sentence_struct_dict.items())
            et_counter = time.perf_counter()
            p_time = (et_counter - st_counter)

            if not pattern:
                return (None, default_value)

            sent_sl_record = cm.createMatcherRecord(matcher)
            loc_text_list = sent_sl_record.getSubEntriesAsList()
            interest_part = loc_text_list[1:]
            if not interest_part:
                interest_part = loc_text_list
            list_of_dup_index = cm.getListOfDuplicatedLoc(interest_part)
            unique_parts = cm.removeDuplicationFromlistLocText(interest_part, list_of_dup_index)
            temp_dict = OrderedDict(unique_parts)

            matched_text_group = temp_dict.values()

            (dict_sl_txt, dict_sl_word_list, dict_sl_mm, dict_tl_txt, dict_tl_word_list, dict_tl_mm) = value
            s_mode_list = dict_sl_mm.smode
            pattern_and_matched_text_pair_list = (s_mode_list, matched_text_group, interest_part)
            # df.LOG(f'pattern_and_matched_text_pair_list:')
            # df.LOG('-' * 80)
            # pp(pattern_and_matched_text_pair_list)
            # df.LOG('-' * 80)
            try:
                is_accept = isMatchedStructMode(pattern_and_matched_text_pair_list)
            except Exception as e:
                is_accept = False

            if not is_accept:
                dd(f'FAILED VALIDATION:')
                dd(f'pattern: [{value[0]}]')
                return (None, default_value)

            sent_sl_record.clear()
            sent_sl_record.update(unique_parts)
            # cached_entry = {klower: (pattern, value)}
            # self.local_text_and_chosen_sent_struct_list.update(cached_entry)
            # return_value = (pattern, (dict_sl_txt, dict_sl_word_list, dict_sl_mm, dict_tl_txt, dict_tl_word_list, dict_tl_mm, sent_sl_record)
            return (pattern, (dict_sl_txt, dict_sl_word_list, dict_sl_mm, dict_tl_txt, dict_tl_word_list, dict_tl_mm, sent_sl_record))
        except Exception as e:
            df.LOG(f'{e};', error=True)
            raise e

    def isTranRefRequiredFurtherUnpack(self, word):
        matcher = df.TRAN_REF_PATTERN.search(word)
        return (matcher is not None)

    def replaceRefsForDict(self):
        temp_dict = {}
        for sl_txt, tl_txt in self.items():
            new_tl_txt = self.replaceTranRef(tl_txt)
            entry = {sl_txt: tl_txt}
            temp_dict.update(entry)
        self.clear()
        self.update(temp_dict)

    def replaceTranRef(self, tran):
        is_finished = False
        new_tran = str(tran)
        # df.LOG(f'[{new_tran}]')
        seen_list = {}
        while not is_finished:
            # 1. locate references in the translation text
            found_ref_dict = cm.patternMatchAll(df.TRAN_REF_PATTERN, new_tran)
            is_finished = (not bool(found_ref_dict))
            if is_finished:
                break

            # 2. locate translations for references found
            ref_tran_dict = {}
            found_ref_list = list(found_ref_dict.items())
            found_ref_list.sort(reverse=True)
            for ref_loc, ref_mm in found_ref_list:
                ref_found = ref_mm.txt
                dict_selected = self
                has_ref = (ref_found in dict_selected)
                if not has_ref:
                    has_ref = (ref_found in df.numeral_dict)
                    if not has_ref:
                        msg = f'REFERENCE [{ref_found}] has no translation for it! Translation: [{tran}]'
                        raise ValueError(msg)
                    else:
                        dict_selected = df.numeral_dict

                tran_for_ref = dict_selected[ref_found]
                entry = {ref_found: tran_for_ref}
                ref_tran_dict.update(entry)

            # 3. replace references with ref's translations
            for ref_found, tran_for_ref in ref_tran_dict.items():
                new_tran = new_tran.replace(ref_found, tran_for_ref)
            # df.LOG(f'[{new_tran}]')

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

    def initNumericalPatternList(self):
        for pat_txt, tran_txt in df.numeric_trans.items():
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
                iter = df.TRAN_REF_PATTERN.finditer(tran)
                for m in iter:
                    abbrev_txt = m.group(0)
                    try:
                        abbrev_tran_txt = df.numeral_dict[abbrev_txt]
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
            translation = f'{df.numeric_prefix} {translation} {df.numeric_postfix}'
            is_diff = (stripped_word != msg)
            if is_diff:
                translation = msg.replace(msg, stripped_word)
            dd(f'translateNumerics(): [{stripped_word}] => [{translation}]')
        return translation

    def simpleFuzzyTranslate(self, msg: str, acceptable_rate=df.FUZZY_ACCEPTABLE_RATIO):
        def getShorterKText():
            shorter_kword_list=[]
            for kword in k_word_list:
                possible_shorter_word = self.getByReduceKnownSuffix(kword)
                if not possible_shorter_word:
                    possible_shorter_word = kword
                shorter_kword_list.append(possible_shorter_word)
            possible_shorter_k = " ".join(shorter_kword_list)
            return possible_shorter_k

        def generateFoundListFromSelectedKeyList(txt_to_compare, possible_list):
            found_list = []
            for found_item in possible_list:
                ratio = fuzz.ratio(found_item, txt_to_compare)
                partial_ratio = fuzz.partial_ratio(found_item, txt_to_compare)
                entry = (ratio, partial_ratio, found_item)
                found_list.append(entry)

            if found_list:
                if is_k_single_word:
                    found_list.sort(key=OP.itemgetter(1, 0), reverse=True)
                else:
                    found_list.sort(key=OP.itemgetter(0, 1), reverse=True)
                selected_item = found_list[0]
                (ratio, partial_ratio, chosen_txt) = selected_item
                return_ratio = (partial_ratio if is_k_single_word else ratio)
                return_entry = (chosen_txt, return_ratio)
                return return_entry
            else:
                return None


        def simpleFindListOfCandidates(possible_text_list, accept_rate):
            found_list = []

            choice = generateFoundListFromSelectedKeyList(k, possible_text_list)
            if not choice:
                return found_list

            (txt, rat) = choice
            is_accepted = (rat >= accept_rate)
            if is_accepted:
                found_list.append(choice)
                return found_list

            shorter_k = getShorterKText()
            choice1 = choice
            choice2 = fuzz_process.extractOne(k, possible_text_list)

            has_both = (choice1 and choice2)
            has_one = (choice1 or choice2)
            has_none = not (choice1 or choice2)

            if has_none:
                return found_list

            if has_both:
                txt1, rat1 = choice1
                rat1 = fuzz.ratio(txt1, k)

                txt2, rat2 = choice2
                rat2 = fuzz.ratio(txt2, k)
                choice = (choice1 if (rat1 > rat2) else choice2)
            else: # has one
                choice = (choice1 if choice1 else choice2)

            # txt_choice, rat_choice = choice
            # rat_choice = fuzz.ratio(txt_choice, k)
            # choice = (txt_choice, rat_choice)
            #
            found_list.append(choice)
            return found_list

        def isKeyListTextValid(dict_item):
            is_same = (k == dict_item.lower())
            is_starts_with_k_part  = (dict_item.startswith(k_part))
            is_word_len_acceptable = (len(dict_item.split()) <= k_word_count * 1.5)
            key_len = len(dict_item)
            is_total_len_acceptable = (0.5 <= key_len <= k_length * 1.5)
            return is_same or (is_starts_with_k_part and is_word_len_acceptable and is_total_len_acceptable)

        def binSearchFunction(item):
            return item[:max_k_length]

        def simpleKeyListGetting():
            def findInRange(start_index, end_index, step):
                local_found=[]
                for i in range(start_index, end_index, step):
                    dict_item = dict_keys[i]
                    is_found = isKeyListTextValid(dict_item)
                    if is_found:
                        local_found.append(dict_item)
                    else:
                        dict_part = binSearchFunction(dict_item)
                        is_match = (dict_part == k_part)
                        if not is_match:
                            break
                        else:
                            continue
                return local_found

            found_list=[]
            dict_keys = self.local_keys
            index = cm.binarySearch(dict_keys, k, key=binSearchFunction)
            is_found = (index >= 0)
            if not is_found:
                return found_list

            dict_key_len = len(dict_keys)
            found_before = findInRange(index, 0, -1)
            found_after = findInRange(index+1, dict_key_len, 1)
            found_list.extend(found_before)
            found_list.extend(found_after)
            return found_list


        untran_word_dic = {}
        default_result = (None, None, 0, untran_word_dic)

        is_ref = cm.isRef(msg)
        if is_ref:
            return default_result

        if ig.isIgnored(msg):
            return default_result

        left, k, right = cm.getTextWithin(msg)
        k = k.lower()

        if ig.isIgnored(k):
            return default_result

        has_path_char = (df.PATH_CHAR.search(k) is not None)
        k_length = len(k)
        k_word_list = [x for x in df.COMMON_WORD_SEPS.split(k) if x]
        k_word_count = len(k_word_list)
        is_k_single_word = (k_word_count == 1)

        first_word = k_word_list[0]
        first_word_len = len(first_word)
        is_a_single_char_word = (first_word_len == 1)
        can_add_second_word = (is_a_single_char_word and k_word_count > 1)
        if can_add_second_word:
            word_list = k_word_list[:2]
            first_word = ' '.join(word_list)
            first_word_len = len(first_word)

        if is_k_single_word:
            max_k_length = int(first_word_len * 0.5)
        else:
            max_k_length = int(first_word_len * 0.8)
        max_k_length = max(1, min(max_k_length, len(first_word)))
        k_part = first_word[:max_k_length]

        # key_list = [x for x in self.local_keys if x.startswith(k_part)]
        is_cached = (k in self.local_keylist_cache)
        if is_cached:
            key_list = self.local_keylist_cache[k]
        else:
            # tic = time.perf_counter()
            key_list = simpleKeyListGetting()
            # tok = time.perf_counter()
            # taken = (tok - tic)
            self.local_keylist_cache.update({k: key_list})

        subset = simpleFindListOfCandidates(key_list, acceptable_rate)
        found_candidates = (len(subset) > 0)
        if not found_candidates:
            return default_result

        # matched_ratio, partial_ratio, selected_item  = subset[0]
        # is_accepted = (matched_ratio >= acceptable_rate)
        (selected_item, original_ratio) = subset[0]
        overall_ratio = fuzz.ratio(selected_item, k)
        is_matching = (original_ratio == overall_ratio)
        matched_ratio = (original_ratio if (is_k_single_word and not has_path_char) else overall_ratio)
        is_accepted = (matched_ratio > acceptable_rate)
        if not is_accepted:
            return default_result

        # matched_ratio, partial_ratio, selected_item = subset[0]
        # is_accepted = ((partial_ratio >= acceptable_rate) if is_k_single_word else (matched_ratio >= acceptable_rate))
        # if not is_accepted:
        #     perfect_match_percent = cm.matchTextPercent(k, selected_item)
        #     is_accepted = (perfect_match_percent > df.FUZZY_PERFECT_MATCH_PERCENT)
        #     if not is_accepted:
        #         return default_result

        translation_txt = self[selected_item]
        report_msg = f'found: [{selected_item}] => [{translation_txt}]'
        df.LOG(report_msg)
        try:
            loc, new_selected = cm.locRemain(msg, selected_item)
            translation = msg.replace(new_selected, translation_txt)
            untran_word_dic = cm.getRemainedWord(msg, new_selected)
        except Exception as e:
            # fname = INP.currentframe().f_code.co_name
            # dd(f'{fname}() {e}')
            dd(f'FAILED TO REPLACE: [{msg}] by [{selected_item}] with trans: [{translation_txt}], matched_ratio:[{matched_ratio}]')
            translation = translation_txt

            left, mid, right = cm.getTextWithin(msg)
            had_the_same_right = (right and translation.endswith(right))
            had_the_same_left = (left and translation.startswith(left))

            if left and not had_the_same_left:
                translation = left + translation

            if right and not had_the_same_right:
                translation = translation + right

            dd(f'SIMPLE PATCHING: left:[{left}] right:[{right}] trans: [{translation}]')
            untran_word_dic = cm.getRemainedWord(msg, selected_item)

        if translation:
            translation = self.replaceTranRef(translation)

        return (translation, selected_item, matched_ratio, untran_word_dic)

    def __delitem__(self, key):
        key = Key(key)
        # dd(f'__delitem__:[{key}]')
        try:
            super(NoCaseDict, self).__delitem__(key)
            if self.is_operational:
                self.is_dirty = True
        except Exception as e:
            df.LOG(f'{e};', error=True)

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

    def getByReduceKnownSuffix(self, txt):
        for replacement_word, ending_list in df.common_suffixes_replace_dict.items():
            for ending in ending_list:
                try:
                    has_ending = txt.endswith(ending)
                    if not has_ending:
                        continue

                    clipping_len = len(ending)
                    clipped_txt = txt[:-clipping_len]
                    is_found = (clipped_txt in self)
                    if is_found:
                        return clipped_txt

                    clipped_txt += replacement_word
                    is_found = (clipped_txt in self)
                    if is_found:
                        return clipped_txt
                except Exception as e:
                    df.LOG(f'{e}: replacement_word:[{replacement_word}] ending:[{ending}]; txt:[{txt}]')
        return None

    def findByChangeSuffix(self, txt):
        clipped_txt = self.getByReduceKnownSuffix(txt)
        tran = (self[clipped_txt] if clipped_txt else None)
        return clipped_txt, tran

    def singleOutputFuzzyTranslation(self, txt):
        try:
            tran, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(txt, acceptable_rate=df.FUZZY_MODERATE_ACCEPTABLE_RATIO )
            return tran
        except Exception as e:
            df.LOG(f'{e} [{txt}]')
            return None

    def tranByPartitioning(self, sl_txt):
        def markTranslated(txt_loc, sl_txt, tl_txt):
            ft_obs.markLocAsUsed(txt_loc)
            entry=(txt_loc, tl_txt)
            ft_translated_list.append(entry)

        def translateMap(the_map_entry):
            (loc, the_text) = the_map_entry
            tran = self.singleOutputFuzzyTranslation(the_text)
            return (loc, the_text, tran)

        ft_map = cm.genmap(sl_txt, using_pattern=df.SPACE_SEP_WORD_AND_FSLASH)
        ft_obs = LocationObserver(sl_txt)
        ft_translated_list = []
        part_txt = None
        df.LOG(sl_txt)
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                found_results = executor.map(translateMap, ft_map)

            ft_translation = str(sl_txt)
            found_result_list = list(found_results)
            for (ft_loc, ft_word, ft_tran) in found_result_list:
                if ft_obs.isCompletelyUsed():
                    break

                if ft_obs.isLocUsed(ft_loc):
                    continue

                df.LOG(f'found: {[{ft_word}]} => [{ft_tran}]')
                # dd(f'trying: [{ft_word}]')
                # part_txt = ft_word
                # ft_tran = self.singleOutputFuzzyTranslation(ft_word)
                if ft_tran:
                    # df.LOG(f'trying the [{ft_word}], found:[{ft_tran}]')
                    markTranslated(ft_loc, ft_word, ft_tran)
                else:
                    wc = len(ft_word.split())
                    is_single_word = (wc == 1)
                    if not is_single_word:
                        continue

                    ft_tran = self.translateBySlittingSymbols(ft_word, find_translation_function=self.singleOutputFuzzyTranslation)
                    if not ft_tran:
                        ft_tran = self.translateNumerics(ft_word)
                        if not ft_tran:
                            chopped_txt, ft_tran = self.findByChangeSuffix(ft_word)

                    if ft_tran:
                        markTranslated(ft_loc, ft_word, ft_tran)

            if ft_translated_list:
                ft_translated_list.sort(reverse=True)
                for ft_loc, ft_tran in ft_translated_list:
                    ft_translation = cm.jointText(ft_translation, ft_tran, ft_loc)

                is_translated = (ft_translation != sl_txt)
                return_tran = (ft_translation if is_translated else None)
            else:
                return_tran = None

        except Exception as e:
            return_tran = None
            df.LOG(f'{e}; [{sl_txt}] dealing with: [{part_txt}]', error=True)
        un_tran_list = ft_obs.getUnmarkedPartsAsDict()
        return return_tran, un_tran_list

    def singleOutputTranByPartitioning(self, txt):
        tran, untran_dict = self.tranByPartitioning(txt)
        return tran

    def translateBySlittingSymbols(self, input_txt, find_translation_function=None):
        df.LOG(f'[{input_txt}]')
        translation = str(input_txt)
        translated_list = {}
        selective_list = []

        try:
            obs = LocationObserver(input_txt)
            for pat in df.symbol_splitting_pattern_list:
                if obs.isCompletelyUsed():
                    break

                word_list = cm.splitWordAtToList(pat, input_txt)
                if not word_list:
                    continue

                for loc, txt in word_list:
                    if obs.isCompletelyUsed():
                        break

                    if obs.isLocUsed(loc):
                        continue

                    df.LOG(f'{loc} => {txt}')
                    trans_find_function = (self.singleOutputTranByPartitioning if not find_translation_function else find_translation_function)
                    try:
                        tran = trans_find_function(txt)
                    except Exception as ee:
                        df.LOG(f'{trans_find_function.__name__} [{ee}]; [{input_txt}]')
                        tran = None

                    is_translated = (tran and tran != txt)
                    if is_translated:
                        obs.markLocAsUsed(loc)
                        entry = {loc: tran}
                        translated_list.update(entry)

            if not translated_list:
                return None

            translated_list = list(translated_list.items())
            translated_list.sort(reverse=True)

            df.LOG('translated_list:')
            dd('-' * 40)
            pp(translated_list)
            dd('-' * 40)

            for loc, tran in translated_list:
                translation = cm.jointText(translation, tran, loc)

            is_translated = (translation != input_txt)
            if is_translated:
                df.LOG(f'input_txt:[{input_txt}]=>[{translation}]')
                return translation
            else:
                return None
        except Exception as e:
            df.LOG(f'{e} [{input_txt}]')
            return None

    def blindTranslate(self, txt):
        tran, un_tran_list = self.tranByPartitioning(txt)
        if not tran:
            tran = self.translateBySlittingSymbols(txt)
        return tran

    def translationByRemovingSymbols(self, txt: str) -> str:
        new_txt, subcount = df.SYMBOLS.subn('', txt)
        cover_length = 0
        if subcount > 0:
            is_ignore = ig.isIgnored(new_txt)
            if is_ignore:
                return txt, None, cover_length

            tran, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(new_txt)
            if tran:
                cover_length = len(txt)
                trans = tran.strip()
                matched_text = txt.strip()
                trans = txt.replace(matched_text, trans)
                return new_txt, trans, cover_length
        return txt, None, cover_length

    def translationByReplacingSymbolsWithSpaces(self, txt: str):
        new_txt, subcount = df.SYMBOLS.subn(' ', txt)
        cover_length = 0
        trans = None
        orig_txt = txt
        if subcount > 0:
            orig_txt = new_txt

        tran, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(orig_txt)
        if not tran:
            tran = self.translateWords(orig_txt)

        if tran:
            cover_length = len(txt)
            tran = tran.strip()
            matched_text = txt.strip()
            tran = txt.replace(matched_text, tran)
            return new_txt, tran, cover_length

        return txt, None, cover_length

    def translateWords(self, txt: str):
        word_list_dict = cm.findInvert(df.SYMBOLS, txt, is_reversed=True)
        temp_tran = str(txt)
        for loc, mm in word_list_dict.items():
            word = mm.txt
            tran, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(word)
            if tran:
                temp_tran = cm.jointText(temp_tran, tran, loc)
        has_tran = (temp_tran != txt)
        return (temp_tran if has_tran else None)


    def removeByPatternListAndCheck(self, txt, part_list, at):
        start_non_alpha, mid, end_non_alpha = cm.getTextWithin(txt)
        is_at_start = (at == df.START_WORD)
        is_at_end = (at == df.END_WORD)
        test_text = str(txt)
        cover_length = 0
        if is_at_start:
            test_text = df.NON_WORD_STARTING.sub("", test_text)
        elif is_at_end:
            test_text = df.NON_WORD_ENDING.sub("", test_text)

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
                test_text = df.NON_WORD_STARTING.sub("", test_text)
                # dd(f'removeByPatternListAndCheck: has_start: {part}; test_text:{test_text}')
            elif has_end:
                test_text = text_before_cutoff[:-part_len]
                test_text = df.NON_WORD_ENDING.sub("", test_text)
                # dd(f'removeByPatternListAndCheck: has_end: {part}; test_text:{test_text}')
            else:
                continue

            # this is to fix the 'hop' (should be hopping), and 'hope' (should be hoping)
            should_have_duplicated_ending = cm.shouldHaveDuplicatedEnding(part, test_text)
            if should_have_duplicated_ending:
                chopped_txt, tran = self.replaceEndings(part, test_text)
                not_ending_y = (chopped_txt and (chopped_txt not in df.verb_with_ending_y))
                not_ending_s = (chopped_txt and (chopped_txt not in df.verb_with_ending_s))
                fix_tran = (not_ending_y and not_ending_s)
                if tran:
                    cover_length = len(text_before_cutoff)
                    if fix_tran:
                        tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                    return test_text, tran, cover_length

            tran, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(test_text)
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
                                (chopped_txt not in df.verb_with_ending_y) and \
                                (chopped_txt not in df.verb_with_ending_s))
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

    def reduceDuplicatedEnding(self, txt):
        is_double_ending = (len(txt) > 2) and (txt[-1] == txt[-2])
        if is_double_ending:
            # dd(f'is_double_ending txt:{txt}')
            test_text = txt[:-1]
            trans, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(test_text)
            if trans:
                return test_text, trans
        return txt, None

    def replaceEndings(self, part, clipped_txt: str):
        def checkTranslationForText(test_text):
            trans, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(test_text)
            if trans:
                return test_text, trans, True

            chopped_txt, trans = self.reduceDuplicatedEnding(test_text)
            if trans:
                return chopped_txt, trans, True
            return test_text, None, False

        for replacement_word, ending_list in df.common_suffixes_replace_dict.items():
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
            tran, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(test_text)
            if not tran:
                is_double_ending = (len(test_text) > 2) and (test_text[-1] == test_text[-2])
                if is_double_ending:
                    test_text = test_text[:-1]
                    tran, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(test_text)

            if tran:
                cover_length = len(matched_text)
                return test_text, tran, cover_length
        return txt, None, cover_length

    def fixTranslationWithKnowsPrefixSuffixes(self, txt, trans, is_prefix=False):
        new_txt = str(trans)
        fix_translation_list = (df.common_prefix_translation if is_prefix else df.common_sufix_translation)
        for fix_term, (position, add_translation) in fix_translation_list:

            if is_prefix:
                has_fix_term = txt.startswith(fix_term)
            else:
                has_fix_term = txt.endswith(fix_term)

            if not has_fix_term:
                continue

            is_at_front = (position == df.START_WORD)
            is_at_end = (position == df.END_WORD)
            is_patching_front = (is_at_front and not new_txt.startswith(add_translation))
            is_patching_end = (is_at_end and not new_txt.endswith(add_translation))

            if is_patching_front:
                new_txt = add_translation + ' ' + new_txt
                return new_txt

            if is_patching_end:
                new_txt += ' ' + add_translation
                return new_txt
        return trans

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
            has_translation = (trans is not None)
            if not has_translation:
                return new_text, None, cover_length
            else:
                trans = cm.patchingBeforeReturn(start_non_alpha, end_non_alpha, trans, txt)
                dd(f'findByReduction: looking for: [{msg}] trans:[{trans}] function_name:[{function_name}]')
                return new_text, trans, cover_length
        except Exception as e:
            df.LOG(f'{e}; msg:{msg}', error=True)
            raise e