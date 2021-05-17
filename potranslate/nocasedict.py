from collections import OrderedDict
from common import Common as cm, dd, pp, LocationObserver
from definition import Definitions as df, \
    SentStructMode as SMODE, \
    SentStructModeRecord as SMODEREC
from key import Key
from fuzzywuzzy import fuzz
from math import ceil
import operator as OP
import inspect as INP
import re
import time

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


        self.tran_find_func_list = [
            (self.translationByRemovingSymbols, ('txt', None, None)),              # (txt)
            (self.translationByReplacingSymbolsWithSpaces, ('txt', None, None)),   # (txt)
            (self.removeByPatternListAndCheck, ('txt', df.common_suffix_sorted, df.END_WORD)),               # (txt, cm.common_suffix_sorted, df.END_WORD)
            (self.removeByPatternListAndCheck, ('txt', df.common_suffix_sorted, df.START_WORD)),               # (txt, cm.common_prefix_sorted, df.START_WORD)
            (self.removeBothByPatternListAndCheck, ('txt', df.common_prefix_sorted, df.common_suffix_sorted)),           # (txt, cm.common_prefix_sorted, cm.common_suffix_sorted)
        ]

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
            fname = INP.currentframe().f_code.co_name
            dd(f'{fname}() {e}')
            return None

    def createSentenceStructureDict(self):
        def isSentStruct(item):
            (k, v) = item
            is_sent_struct = (df.SENT_STRUCT_START_SYMB in k)
            # is_sent_struct = (re.search(r'^the \$\{.*ing', k) is not None)
            # is_sent_struct = (df.ENDING_WITH.search(k) is not None)
            return is_sent_struct

        temp_dict={}
        temp_set = list(filter(isSentStruct, self.items()))
        # temp_set = [(x, y) for (x, y) in self.items() if df.SENT_STRUCT_START_SYMB in x]
        # temp_set = [(x, y) for (x, y) in self.items() if '${`' in x]
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

                    is_digits_only = (structure_mode == SMODE.NUMBER_ONLY)
                    if is_digits_only:
                        is_number = (df.NUMBERS.search(matched_part) is not None)
                        is_ok_list.append(is_number)
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

        def filterKeyChosenSet(pat_item):
            match = re.compile(pat_item, flags=re.I).search(key)
            is_found = (match is not None )
            return is_found

        try:
            klower = key.lower()
            has_cached_key_value_set = (klower in self.local_text_and_chosen_sent_struct_list)
            if has_cached_key_value_set:
                set_value = self.local_text_and_chosen_sent_struct_list[klower]
                (pat, value) = set_value
                return (pat, value)

            selective_match = []
            key_list = self.sentence_struct_dict.keys()
            # pat_list = [x for x in pat_list if 'i\\.e\\.' in x]
            chosen_key_list = list(filter(filterKeyChosenSet, key_list))

            if not chosen_key_list:
                value = (None, None, None, None, None, None)
                return (None, value)

            # list_of_sent_struct = list(self.sentence_struct_dict.items())
            for pat in chosen_key_list:
                value = self.sentence_struct_dict[pat]
                pattern = re.compile(pat, flags=re.I)
                # match_list = re.findall(pat, key)
                matcher_dict = cm.patternMatchAll(pattern, key)
                first_mm_record = list(matcher_dict.values())[0]
                loc_text_list = first_mm_record.getSubEntriesAsList()
                interest_part = loc_text_list[1:]
                unique_parts = cm.removeDuplicationFromlistLocText(interest_part)
                temp_dict = OrderedDict(unique_parts)

                matched_text_group = temp_dict.values()

                # matched_text_group = matcher.groups()
                (dict_sl_txt, dict_sl_word_list, dict_sl_mm, dict_tl_txt, dict_tl_word_list, dict_tl_mm) = value
                s_mode_list = dict_sl_mm.smode
                is_pattern_checking_mode = (SMODE.getName(pat) is not None)
                # if is_pattern_checking_mode:
                #     first_item = matched_text_group[0]
                #     new_group = [first_item]
                #     matched_text_group = new_group
                pattern_and_matched_text_pair_list = (s_mode_list, matched_text_group)
                try:
                    is_accept = isMatchedStructMode(pattern_and_matched_text_pair_list)
                except Exception as e:
                    is_accept = False

                if not is_accept:
                    continue

                match_rate = fuzz.ratio(dict_sl_txt, key)
                entry=(match_rate, pat, value)
                selective_match.append(entry)

            if not selective_match:
                value = (None, None, None, None, None, None)
                return (None, value)

            selective_match.sort(reverse=True)
            dd('-' * 80)
            pp(selective_match)
            dd('-' * 80)
            first_entry = selective_match[0]
            (match_rate, pat, value) = first_entry
            pattern = re.compile(pat, flags=re.I)

            cached_entry = {klower: (pattern, value)}
            self.local_text_and_chosen_sent_struct_list.update(cached_entry)

            return (pattern, value)
        except Exception as e:
            df.LOG(f'{e};')
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

        def simpleFindListOfCandidates():
            found_list = []
            for found_item in key_list:
                ratio = fuzz.ratio(found_item, k)
                entry = (ratio, found_item)
                found_list.append(entry)
            found_list.sort(reverse=True)
            if found_list:
                return [found_list[0]]
            else:
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

            before_items = dict_keys[index-10: index]
            after_items = dict_keys[index: index+10]
            test_item = dict_keys[index]
            dict_key_len = len(dict_keys)

            start_stop_at=None
            found_before = findInRange(index, 0, -1)
            found_after = findInRange(index+1, dict_key_len, 1)
            found_list.extend(found_before)
            found_list.extend(found_after)
            return found_list

        untran_word_dic = {}
        left, k, right = cm.getTextWithin(msg)
        k = k.lower()

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
        if is_k_single_word:
            max_k_length = int(first_word_len * 0.5)
        else:
            max_k_length = int(first_word_len * 0.8)
        k_part = first_word[:max_k_length]

        # key_list = [x for x in self.local_keys if x.startswith(k_part)]
        is_cached = (k in self.local_keylist_cache)
        if is_cached:
            key_list = self.local_keylist_cache[k]
        else:
            tic = time.perf_counter()
            # key_list = list(filter(isKeyListTextValid, self.local_keys))
            key_list = simpleKeyListGetting()
            tok = time.perf_counter()
            taken = (tok - tic)
            self.local_keylist_cache.update({k: key_list})
        # pp(key_list)

        subset = key_list

        # subset = findListOfCandidates()
        subset = simpleFindListOfCandidates()
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
            # fname = INP.currentframe().f_code.co_name
            # dd(f'{fname}() {e}')
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
                fname = INP.currentframe().f_code.co_name
                dd(f'{fname}() Unable to locate translation for {msg}')
                translation = None

        if translation:
            translation = self.replaceTranRef(translation)

        return translation, selected_item, matched_ratio, untran_word_dic

    def __delitem__(self, key):
        key = Key(key)
        # dd(f'__delitem__:[{key}]')
        try:
            super(NoCaseDict, self).__delitem__(key)
            if self.is_operational:
                self.is_dirty = True
        except Exception as e:
            df.LOG(f'{e};')

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

    def findByChangeSuffix(self, txt):
        def checkTranslationForText(test_text):
            trans, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate(test_text)
            if trans:
                return test_text, trans, True

            # chopped_txt, trans = self.reduceDuplicatedEnding(test_text)
            # if trans:
            #     return chopped_txt, trans, True
            return test_text, None, False

        for replacement_word, ending_list in df.common_suffixes_replace_dict.items():
            for ending in ending_list:
                has_ending = txt.endswith(ending)
                if not has_ending:
                    continue

                clipping_len = len(ending)
                clipped_txt = txt[:-clipping_len]
                clipped_txt += replacement_word

                is_found = (clipped_txt in self)
                if not is_found:
                    continue

                tran = self[clipped_txt]
                return clipped_txt, tran
        return None, None

    def tranByPartitioning(self, sl_txt):
        def markTranslated(txt_loc, sl_txt, tl_txt):
            ft_obs.markLocAsUsed(txt_loc)
            entry=(txt_loc, tl_txt)
            ft_translated_list.append(entry)

        fname = INP.currentframe().f_code.co_name
        ft_map = cm.genmap(sl_txt)
        ft_obs = LocationObserver(sl_txt)
        ft_translated_list = []
        try:
            ft_translation = str(sl_txt)
            for ft_loc, ft_word in ft_map:
                if ft_obs.isCompletelyUsed():
                    break

                if ft_obs.isLocUsed(ft_loc):
                    continue

                ft_tran, selected_item, matched_ratio, untran_word_dic = self.simpleFuzzyTranslate( ft_word, acceptable_rate=df.FUZZY_ACCEPTABLE_RATIO )
                if ft_tran:
                    markTranslated(ft_loc, ft_word, ft_tran)
                else:
                    wc = len(ft_word.split())
                    is_single_word = (wc == 1)
                    if not is_single_word:
                        continue

                    chopped_txt, ft_tran = self.findByChangeSuffix(ft_word)
                    if ft_tran:
                        markTranslated(ft_loc, ft_word, ft_tran)

            ft_translated_list.sort(reverse=True)
            for ft_loc, ft_tran in ft_translated_list:
                ft_translation = cm.jointText(ft_translation, ft_tran, ft_loc)

            is_translated = (ft_translation != sl_txt)
            return_tran = (ft_translation if is_translated else None)

            dd(f'{fname}() msg:[{sl_txt}] tran_sub_text:[{ft_translation}]')
        except Exception as e:
            return_tran = None
            df.LOG(f'{e};')
        un_tran_list = ft_obs.getUnmarkedPartsAsDict()
        return return_tran, un_tran_list

    def getTranBySlittingSymbols(self, input_txt):
        fname = INP.currentframe().f_code.co_name

        pattern_list = [
            df.NON_SPACE_SYMBOLS,
            df.SYMBOLS,
        ]
        translation = str(input_txt)
        translated_list = []
        selective_list = []

        tran, untran_dict = self.tranByPartitioning(input_txt)
        if tran:
            return tran

        for pat in pattern_list:
            word_list = cm.splitWordAtToList(pat, input_txt)
            if not word_list:
                continue

            for loc, txt in word_list:
                tran, untran_dict = self.tranByPartitioning(txt)
                is_translated = (tran != txt)
                if is_translated:
                    entry = (loc, tran)
                    translated_list.append(entry)

        translated_list.sort(reverse=True)
        for loc, tran in translated_list:
            translation = cm.jointText(translation, tran, loc)

        is_translated = (translation != input_txt)
        if is_translated:
            dd(f'{fname}(): input_txt:[{input_txt}]=>[{translation}]')
            return translation
        else:
            return None

    def blindTranslate(self, txt):
        tran, untran_dict = self.tranByPartitioning(txt)
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
            df.LOG(f'{e}; msg:{msg}')
            raise e