import sys

sys.path.append('/usr/local/lib/python3.8/site-packages')
# sys.path.append('/Users/hoangduytran/blender_manual/potranslate')
# print(f'translation_finder sys.path: {sys.path}')

import hashlib
import io
import os
import re
from common import Common as cm
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
# from pyphonetics import Soundex

class CaseInsensitiveDict(dict):
    """Basic case insensitive dict with strings only keys."""

    proxy = {}

    def __init__(self, data):
        if not data:
            return
        self.proxy = dict((k.lower(), k) for k in data)
        for k in data:
            self[k] = data[k]

    def __contains__(self, k):
        return k.lower() in self.proxy

    def __delitem__(self, k):
        key = self.proxy[k.lower()]
        super(CaseInsensitiveDict, self).__delitem__(key)
        del self.proxy[k.lower()]

    def __getitem__(self, k):
        key = self.proxy[k.lower()]
        return super(CaseInsensitiveDict, self).__getitem__(key)

    def get(self, k, default=None):
        return self[k] if k in self else default

    def __setitem__(self, k, v):
        super(CaseInsensitiveDict, self).__setitem__(k, v)
        self.proxy[k.lower()] = k


class NoCaseDict(OrderedDict):
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

    def __init__(self, data=None):
        self.is_dirty = False
        self.is_operational = False
        self.local_keys = []

        super(NoCaseDict, self).__init__()
        if data is None:
            data = {}
        for key, val in data.items():
            self[key.lower()] = val
            # dd(f'__init__:[{key}], value:[{val}]')
        self.is_operational = True

    def __contains__(self, key):
        key = self.Key(key)
        is_there = super(NoCaseDict, self).__contains__(key)
        dd(f'__contains__:[{key}], is_there:{is_there}')
        return is_there

    def __setitem__(self, key, value):
        lkey_key = self.Key(key)
        super(NoCaseDict, self).__setitem__(lkey_key, value)
        if self.is_operational:
            self.is_dirty = True

    def __getitem__(self, key):
        key = self.Key(key)
        try:
            value = super(NoCaseDict, self).__getitem__(key)
            # dd(f'__getitem__:[{key}], value:[{value}]')
            return value
        except Exception as e:
            dd(f'Exception __getitem__:{e}')
            return None

    def get(self, k, default=None):
        return self[k] if k in self else default

    def fuzzyTranslate(self, msg, ratio):

        def getFuzzyTranslationUsingStringMatch():
            # Application of StringMatch class, using default args
            titlematch = StringMatch(source_titles, target_titles)
            titlematch.tokenize()
            match_df = titlematch.match(output_fmt='dict')

            k_set = [k]
            titlematch = StringMatch(subset, k_set)
            titlematch.tokenize()
            match_df = titlematch.match(output_fmt='dict')
            dd('match_df:')
            dd('-' * 80)
            for subset_index, v in match_df.items():
                _, matched_ratio = v[0]
                matched_ratio *= 100
                is_acceptable = (matched_ratio >= cm.AWESOME_COSSIM_FUZZY_ACCEPTABLE_RATIO)
                if is_acceptable:
                    entry = (matched_ratio, subset[subset_index])
                    selectable_list.append(entry)
                    dd(entry)

        def compareString(item, test_length):

            item_len = len(item)

            # has_fuzzy_any = cm.FUZZY_ANY_PART_PATTERN.search(item)
            # if not has_fuzzy_any:
            item_test_length = min(item_len, test_length)
            item_part = item[:item_test_length]
            is_equal = (item_part == k_part)
            if is_equal:
                return 0
            elif item_part < k_part:
                return -1
            else:
                return 1
            # else:
            #     item_word_list = item.split(cm.FUZZY_ANY_PART)
            #     item_left_part = item_word_list[0].strip()
            #     item_right_part = item_word_list[1].strip()
            #
            #     item_left_part_word_list = item_left_part.split()
            #     item_right_part_word_list = item_right_part.split()
            #     item_left_wc = len(item_left_part_word_list)
            #     item_right_wc = len(item_right_part_word_list)
            #
            #     try:
            #         k_word_list = k.split()
            #         k_left_part = k_word_list[:item_left_wc]
            #         k_right_part = k_word_list[item_right_wc:]
            #         k_mid_part = k_word_list[item_left_wc:item_right_wc]
            #
            #         compare_left_ratio = fuzz.ratio(item_left_part, k_left_part)
            #         compare_right_ratio = fuzz.ratio(item_right_part, k_right_part)
            #         is_same = (compare_left_ratio == cm.FUZZY_ACCEPTABLE_RATIO) and (compare_right_ratio == cm.FUZZY_ACCEPTABLE_RATIO)
            #         if is_same:
            #             return 0
            #         elif item_left_part < k_left_part:
            #             return -1
            #         else:
            #             return 1
            #     except Exception as e:
            #
            # return False

        def binarySearchStartIndex(k_list, test_length):
            lo = 0
            hi = len(k_list)-1
            while lo < hi:
                mid = (lo + hi) // 2
                item = k_list[mid]
                value = compareString(item, test_length)
                is_equal = (value == 0)
                if is_equal:
                    return mid
                elif value < 0:
                    lo = mid + 1
                else:
                    hi = mid
            return -1

        def reduceListSize(k_list, start_index, test_length):
            new_list=[]
            hi = len(k_list)-1
            for i in range(start_index, -1, -1):
                item = k_list[i]
                value = compareString(item, test_length)
                is_equal = (value == 0)
                if is_equal:
                    start_index = i
                else:
                    acceptable_ratio = fuzz.ratio(item, k)
                    is_acceptable = (acceptable_ratio >= ratio)
                    if is_acceptable:
                        continue
                    else:
                        print(f'reduceListSize: going back on found list, looking for: [{k}];  stopping at: [{item}]')
                        break

            for i in range(start_index, hi):
                lo = i+1
                item = k_list[i]
                value = compareString(item, test_length)
                is_equal = (value == 0)
                if is_equal:
                    new_list.append(item)
                else:
                    acceptable_ratio = fuzz.ratio(item, k)
                    is_acceptable = (acceptable_ratio >= ratio)
                    if is_acceptable:
                        continue
                    else:
                        return new_list
            return new_list

        # print(f'fuzzyTranslation, looking for: [{msg}]')
        # cm.debugging(msg)
        selectable_list=[]

        loc, k = cm.removingNonAlpha(msg.lower())
        k_length = len(k)
        k_half_length = (k_length // 2)
        k_part = None
        key_list = list(self.keys())
        # subset = list(filter(filter_function, key_list))
        subset = key_list
        max_k_length = int(k_length * cm.FUZZY_KEY_LENGTH_RATIO)
        min_test_length = min(cm.MAX_FUZZY_TEST_LENGTH, max_k_length)
        for test_length in range(min_test_length, k_length):
            k_test_length = min(k_length, test_length)
            k_part = k[:k_test_length]

            s_index = binarySearchStartIndex(subset, test_length)
            if s_index >= 0:
                subset = reduceListSize(subset, s_index, test_length)
            else:
                break

        if not subset:
            return None, None

        number_of_possible_fuzzy_entries = len(subset)
        is_too_large_subset = (number_of_possible_fuzzy_entries > cm.MAX_FUZZY_LIST)
        if is_too_large_subset:
            return None, None

        for selected in subset:
            ratio = fuzz.ratio(selected, k)
            entry=(ratio, selected)
            selectable_list.append(entry)

        if not selectable_list:
            return None, None

        selectable_list.sort(reverse=True)

        dd(f'selectable_list: ')
        dd('-' * 80)
        pp(selectable_list)
        dd('-' * 80)

        first_entry = selectable_list[0]
        accepted_ratio, word_selected = first_entry
        is_acceptable = (accepted_ratio >= ratio)
        if not is_acceptable:
            dd(f'looking for:[{k}]; first_entry:[{first_entry}], UNACCEPTABLE, ratio demanded is higher than: [{ratio}]')
            return None, None

        tran = self[word_selected]
        tran = cm.insertTranslation(msg.lower(), word_selected, tran)

        dd(f'looking for:[{k}]; first_entry:[{first_entry}] => tran:[{tran}]')
        dd('-' * 80)
        # covered_length = len(word_selected)

        return tran, word_selected

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
        "WheelUp": "Lăn Bánh Xe về Trước (WheelUp)",
        "WheelDown": "Lăn Bánh Xe về Sau (WheelDown)",
        "Wheel": "Bánh Xe (Wheel)",
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
        "Down": "Xuống (Down)",
        "Up": "Lên (Up)",
        "Comma": "Dấu Phẩy (Comma)",
        "Minus": "Dấu Trừ (Minus)",
        "Plus": "Dấu Cộng (Plus)",
        "Left": "Trái (Left)",
        "=": "Dấu Bằng (=)",
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

    def __init__(self):
        self.update_dic = 0
        self.update_po_file = None
        home_dir = os.environ['HOME']
        home_dir = os.path.join(home_dir, 'Dev/tran')
        self.master_dic_file = os.path.join(home_dir, "blender_manual/ref_dict_0006_0001.json")
        self.master_dic_backup_file = os.path.join(home_dir, "blender_manual/ref_dict_backup_0005_0001.json")
        self.master_dic_test_file = os.path.join(home_dir, "blender_manual/ref_dict_test_0005.json")

        self.vipo_dic_path = os.path.join(home_dir, "blender_manual/gui/2.80/po/vi.po")
        self.vipo_dic_list = None  # not used

        self.current_po_dir = os.path.join(home_dir, "blender_docs/locale/vi/LC_MESSAGES")
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

        self.loadDictionary()

    def findByReduction(self, msg):
        def append_selective(cover_length, new_text_length, new_text, trans, selective_list, function_name):
            entry = (cover_length, new_text_length, new_text, trans, function_name)
            selective_list.append(entry)

        trans = None
        original_text = str(msg)
        selective_list = []
        try:
            #
            # trans = self.isInDict(msg, find_fuzzy=True)
            # if trans:
            #     return msg, trans, len(msg)

            for f, params in self.tran_find_func_list:
                txt, param1, param2 = params
                is_empty = not (param1 or param2)
                if is_empty:
                    new_text, trans, cover_length = f(msg)
                else:
                    new_text, trans, cover_length = f(msg, param1, param2)
                new_text_length = len(new_text) # the least cut off the better
                append_selective(cover_length, new_text_length, new_text, trans, selective_list, f.__name__)
            sorted_selective_list = list(sorted(selective_list, key=OP.itemgetter(0, 1), reverse=True))
            chosen_entry = sorted_selective_list[0]
            cover_length, new_text_length, new_text, trans, function_name = chosen_entry
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
        cm.testDict(self.master_dic_list)

        keylist = list(self.master_dic_list.keys())
        for k in keylist:
            is_treat = k.startswith('treat')
            if is_treat:
                print(k)

    def flatPOFile(self, file_path):
        data_cat = c.load_po(file_path)
        c.dump_po(file_path, data_cat)

    def genmap(self, msg):
        part_list = []
        loc_dic = cm.patternMatchAllToDict(cm.SPACE_WORD_SEP, msg)
        # loc_dic = cm.patternMatchAllToDict(cm.WORD_SEP, msg)
        loc_key = list(loc_dic.keys())

        max_len = len(loc_dic)
        has_only_one_item = (max_len == 1)
        step = 1
        is_finished = False
        while not is_finished:
            for i in range(0, max_len):
                l = []
                for k in range(i, min(i + step, max_len)):
                    loc = loc_key[k]
                    # print(f'step:{step}; i:{i}; k:{k}, loc:{loc}')
                    l.append(loc_key[k])

                w_s = sys.maxsize
                w_e = -1
                for loc in l:
                    ss, ee = loc
                    is_remember_start_loc = (ss < w_s)
                    if is_remember_start_loc:
                        w_s = ss
                    is_remember_end_loc = (ee > w_e)
                    if is_remember_end_loc:
                        w_e = ee
                t = msg[w_s: w_e]

                # print(f's location:{l}, text:{t}')

                entry = ((w_s, w_e), t)
                is_in = (entry in part_list)
                if not is_in:
                    part_list.append(entry)
            step += 1
            is_finish = (step > max_len)
            if is_finish:
                break

        sorted_partlist = sorted(part_list, key=lambda x: len(x[1]), reverse=True)
        return sorted_partlist

    def translateBreakupSentences(self, msg):
        if not msg:
            return msg

        count_untranslated = 0
        count_translated = 0
        translation = str(msg)
        result_list = OrderedDict()
        text_list = cm.patternMatchAllToDict(cm.COMMON_SENTENCE_BREAKS, msg)
        for loc, t in text_list.items():
            tran, matched_text = self.isInDict(t)
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


    def replacingUsingDic(self, local_dict: dict, text: str) -> str:
        location_database = []
        def filerLocation(item):
            loc_covered_length, local_location, loc_dict_txt, loc_tran_txt = item
            if not location_database:
                location_database.append(local_location)
                return True
            else:
                l_s, l_e = local_location
                for current_loc in location_database:
                    c_s, c_e = current_loc
                    is_within_current = (l_s >= c_s) and (l_e <= c_e)
                    if is_within_current:
                        return False
                location_database.append(local_location)
                return True

        def translatedListToText(loc_translated_list: list, current_translation, filter_function) -> str:

            loc_translated_list.sort(key=OP.itemgetter(1), reverse=True)

            for loc_covered_length, local_location, loc_dict_txt, loc_tran_txt in loc_translated_list:
                loc_ss, loc_ee = local_location
                loc_left = current_translation[:loc_ss]
                loc_right = current_translation[loc_ee:]
                current_translation = loc_left + loc_tran_txt + loc_right
                is_finish = not (loc_left or loc_right)
                if is_finish:
                    break
            return current_translation

        masking_string = str(text)
        translated_list = []
        translation = str(text)
        # must masking after replacement, even entries are in local_dict, because definitions could overlapped (Vertex Group Weight/Clean Vertext Group for instance)
        for covered_length, loc, untran_txt, tran_txt in local_dict:
            # update every instance found in the temp_translation with already found translation text
            ss, ee = loc
            masking_string_part = masking_string[ss:ee]
            is_translated = (cm.FILLER_CHAR_ALL_PATTERN.search(masking_string_part) is not None)
            if is_translated:
                continue

            empty_part = (cm.FILLER_CHAR * covered_length)
            left = masking_string[:ss]
            right = masking_string[ee:]
            masking_string = left + empty_part + right

        # for untranslated words, we will try to find definitions for each, using reductions
        # check to see if untranslated word
        has_translatable_characters = (cm.TRANSLATABLE_CHARACTERS.search(masking_string) is not None)
        if not has_translatable_characters:
            temp_translation = translatedListToText(local_dict, translation, filerLocation)
            return temp_translation

        un_tran_list = cm.findInvert(cm.FILLER_CHAR_PATTERN,
                                     masking_string,
                                     is_removing_surrounding_none_alphas=True)

        for remain_loc, un_tran_txt in un_tran_list.items():
            is_ignore = ig.isIgnored(un_tran_txt)
            if is_ignore:
                print(f'replacingUsingDic: IGNORING: un_tran_txt:[{un_tran_txt}]')
                continue

            try:
                _, tran_sub_text, covered_length = self.tryToFindTranslation(un_tran_txt)
            except Exception as e:
                print(f'replacingUsingDic() findByReduction: un_tran_txt:[{un_tran_txt}]')
                print(e)
                raise e

            has_tran = (tran_sub_text and not (tran_sub_text == un_tran_txt))
            if has_tran:
                cover_length = len(un_tran_txt)
                tran_dict_entry = (cover_length, remain_loc, un_tran_txt, tran_sub_text)
                local_dict.append(tran_dict_entry)

        # replacing dict into text and finish
        temp_translation = translatedListToText(local_dict, translation, filerLocation)
        has_translation = not (temp_translation == text)
        if not has_translation:
            return None
        else:
            return temp_translation

    def tryFuzzyTranlation(self, msg):
        msg_len = len(msg)
        num_msg_word = (len(msg.split()))
        last_trial_fuzzy_text = None
        for acceptable_ratio in range(cm.FUZZY_ACCEPTABLE_RATIO, cm.MAX_FUZZY_ACCEPTABLE_RATIO, cm.FUZZY_RATIO_INCREMENT):
            print(f'tryFuzzyTranlation: looking for: [{msg}]; trying at acceptable_ratio: [{acceptable_ratio}]')
            tran_sub_text, fuzzy_text = self.isInDict(msg, find_fuzzy=True, ratio=acceptable_ratio)
            has_translation = (bool(tran_sub_text) and bool(fuzzy_text))
            fuzzy_len = (len(fuzzy_text) if has_translation else 0)
            fuzzy_percent = (fuzzy_len / msg_len * 100)
            inc_percentage = 0
            if has_translation:
                inc_percentage = cm.wordInclusiveLevel(msg, fuzzy_text)
            is_all_fuzzy_text_included = (inc_percentage >= cm.MAX_FUZZY_ACCEPTABLE_RATIO)
            is_fuzzy_percent_acceptable = (fuzzy_percent >= cm.FUZZY_ACCEPTABLE_RATIO)
            is_acceptable_len = (has_translation and is_all_fuzzy_text_included and is_fuzzy_percent_acceptable)
            if is_acceptable_len:
                print(f'tryFuzzyTranlation: looking for: [{msg}] found and accept: [{tran_sub_text}] trying at acceptable_ratio: [{acceptable_ratio}]')
                return tran_sub_text, fuzzy_len
            else:
                no_tranlation = (not has_translation)
                first_trial_and_no_translation = no_tranlation and (acceptable_ratio == cm.FUZZY_ACCEPTABLE_RATIO)
                is_fuzzy_text_repeated = has_translation and (bool(last_trial_fuzzy_text) and fuzzy_text == last_trial_fuzzy_text)
                no_need_to_go_further = first_trial_and_no_translation or is_fuzzy_text_repeated
                if no_need_to_go_further:
                    if no_tranlation:
                        print(f'tryFuzzyTranlation: looking for: [{msg}] no translation, STOP!')
                    else:
                        print(f'tryFuzzyTranlation: looking for: [{msg}] text found is REPEATED, STOP! ')
                    break
                last_trial_fuzzy_text = fuzzy_text
                print(f'tryFuzzyTranlation: repeat loop')
        return None, 0
        # is_check_fuzzy_text = and (fuzzy_text != msg)
        # if is_check_fuzzy_text:
        #     un_tran_word_dict = cm.findUntranslatedWords(msg, fuzzy_text)

    def buildLocalTranslationDict(self, msg):

        def loc_filter_function(item):
            i_loc, i_txt = item
            i_s, i_e = i_loc
            for d_loc in done_loc:
                d_s, d_e = d_loc
                is_done = (i_s >= d_s) and (i_e <= d_e)
                if is_done:
                    return False
            return True

        local_translated_dict = [] # for quick, local translation

        # generate all possible combinations of string lengths
        loc_map = self.genmap(msg)
        dd(f'buildLocalTranslationDict() loc_map: {loc_map}')
        # translate them all if possible, store in local dict
        cm.debugging(msg)
        blank_msg = str(msg)
        done_loc = []
        finished = False
        i = 0
        while not finished:
            finished = (len(loc_map) == 0)
            if finished:
                break

            loc, orig_sub_text = loc_map.pop(0)
            tran_sub_text, matched_text = self.isInDict(orig_sub_text)

            if not tran_sub_text:
                tran_sub_text, matched_text = self.tryFuzzyTranlation(orig_sub_text)

            if tran_sub_text:
                cover_length = len(matched_text)
                done_loc.append(loc)
                local_dict_entry = (cover_length, loc, orig_sub_text, tran_sub_text)
                local_translated_dict.append(local_dict_entry)
                loc_map = list(filter(loc_filter_function, loc_map)) # removing parts that are shadowed by translated area, avoid repeating unnecessarily

        local_translated_dict.sort(key=OP.itemgetter(1,2), reverse=True)
        return local_translated_dict

    def blindTranslation(self, msg):
        # cm.debugging(txt)
        new_text, trans, cover_length = self.findByReduction(msg)
        is_found_trans = (trans and not trans == msg)
        if is_found_trans:
            return trans

        local_translated_dict = self.buildLocalTranslationDict(msg)

        # use the translated (longest first) to replace all combination,
        # translate by reduction for ones could not, to form the final translation for the variation
        # translated_dic will be sorted in length by default.
        # using safe translation length and unsafe translation length to sort so one with both highest values
        # are floated on top once sorted. Pick the one at the top list, ignore the rest
        translation = self.replacingUsingDic(local_translated_dict, msg)
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
            if is_master:
                self.addMasterDict(k, v)
            else:
                self.addBackupDictEntry(k, v)
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
                changed = Tprefixrue

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

    def isInDict(self, msg, dic_to_use=None, find_fuzzy=False, ratio=cm.FUZZY_ACCEPTABLE_RATIO):
        tran = None
        matched_text = msg
        search_dict = (dic_to_use if dic_to_use else self.master_dic)
        if not search_dict:
            msg = 'NO Dictionary is available. Stopped'
            print(msg)
            raise Exception(msg)

        msg_length = len(msg)
        stripped_msg = msg.strip()
        if ig.isIgnored(stripped_msg):
            return None, matched_text

        is_found = (stripped_msg in search_dict)
        if is_found:
            tran = search_dict[stripped_msg]

        is_find_fuzzy = (find_fuzzy and not is_found)
        if is_find_fuzzy:
            tran, matched_text = search_dict.fuzzyTranslate(stripped_msg, ratio)

        # cm.debugging(msg)
        if tran:
            tran = msg.replace(stripped_msg, tran)
            tran = cm.matchCase(msg, tran)
            dd(f'isInDict: {msg} => {tran}')
        else:
            tran = None
        return tran, matched_text

    def isInListByDict(self, msg, is_master):
        search_dic = (self.master_dic if is_master else self.backup_dic)
        tran, matched_text = self.isInDict(msg, dic_to_use=search_dic)
        return tran

    def translationByRemovingSymbols(self, txt: str) -> str:
        new_txt, subcount = cm.SYMBOLS.subn('', txt)
        cover_length = 0
        if subcount > 0:
            is_ignore = ig.isIgnored(new_txt)
            if is_ignore:
                return txt, None, cover_length

            trans, matched_text = self.isInDict(new_txt)
            if trans:
                cover_length = len(matched_text)
                return new_txt, trans, cover_length
        return txt, None, cover_length

    def translationByReplacingSymbolsWithSpaces(self, txt: str) -> str:
        new_txt, subcount = cm.SYMBOLS.subn(' ', txt)
        cover_length = 0
        if subcount > 0:
            # there might be multiple spaced words here, must try to retain original symbols
            is_ignore = ig.isIgnored(new_txt)
            if is_ignore:
                return txt, None, cover_length

            trans, matched_text = self.isInDict(new_txt)
            if trans:
                cover_length = len(matched_text)
                return new_txt, trans, cover_length
        return txt, None, cover_length

    def tryToFindTranslation(self, txt: str) -> str:
        cover_length = 0
        separator_list = [
            cm.SPACES,
            cm.SYMBOLS,
        ]
        selective_list = []

        # cm.debugging(txt)
        new_text, trans, cover_length = self.findByReduction(txt)
        is_found_trans = (trans and not trans == txt)
        if is_found_trans:
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

                cm.debugging(orig_txt)
                is_ignore = ig.isIgnored(orig_txt)
                if is_ignore:
                    continue

                new_text = str(orig_txt)
                trans, matched_text = self.isInDict(orig_txt)
                if not trans:
                    tran_sub_text, matched_text = self.tryFuzzyTranlation(orig_txt)

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

        sorted_selective_list = list(sorted(selective_list, reverse=True))
        chosen_entry = sorted_selective_list[0]
        cover_length, txt, translation = chosen_entry
        return txt, translation, cover_length

    def removeStarAndEndingPunctuations(self, txt):
        new_txt = cm.ENDS_PUNCTUAL_MULTI.sub('', txt)
        new_txt = cm.BEGIN_PUNCTUAL_MULTI.sub('', new_txt)

        cover_length = 0
        # dd(f'removeStarAndEndingPunctuations: {txt} => {new_txt}')

        trans, matched_text = self.isInDict(new_txt)
        if trans:
            cover_length = len(matched_text)
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
            trans, matched_text = self.isInDict(test_text)
            if trans:
                return test_text, trans
        return txt, None

    def replaceEndings(self, part, clipped_txt: str):
        def checkTranslationForText(test_text):
            trans, matched_text = self.isInDict(test_text)
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
            tran, matched_text = self.isInDict(test_text)
            if not tran:
                is_double_ending = (len(test_text) > 2) and (test_text[-1] == test_text[-2])
                if is_double_ending:
                    test_text = test_text[:-1]
                    tran, matched_text = self.isInDict(test_text)

            if tran:
                cover_length = len(matched_text)
                return test_text, tran, cover_length
        return txt, None, cover_length

    def removeByPatternListAndCheck(self, txt, part_list, at):
        cover_length = 0
        tran, matched_text = self.isInDict(txt)
        if tran:
            cover_length = len(matched_text)
            return txt, tran, cover_length

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

            tran, matched_text = self.isInDict(test_text)
            if tran:
                cover_length = len(matched_text)
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
        trans, matched_text = self.isInDict(orig_msg)
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
            print(f'result of isInDict:[{orig_msg}] => [{trans}] => is_found: [{is_found}]')
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
        for origin, breakdown in cm.patternMatchAll(cm.WORD_ONLY_FIND, msg):
            is_end = (origin is None)
            if is_end:
                break

            o_s, o_e, o_txt = origin
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
        try:
            dd(f'calling findTranslation')
            is_fuzzy = False
            trans, is_fuzzy, is_ignore = self.findTranslation(msg)
            if is_ignore:
                return (None, False, is_ignore)

            if not trans:
                dd(f'calling tryFuzzyTranlation')
                trans, cover_length = self.tryFuzzyTranlation(msg)
                is_fuzzy = bool(trans)

            if not trans:
                dd(f'calling blindTranslation')
                trans = self.blindTranslation(msg)
                is_fuzzy = True

            if trans:
                is_same = (trans == msg)
                if is_same:
                    trans = None
                else:
                    dd(f'calling removeTheWord')
                    trans = self.removeTheWord(trans)
            return (trans, is_fuzzy, is_ignore)
        except Exception as e:
            print(f'ERROR: {e} - msg:[{msg}], trans:[{trans}]')
            raise e

    def translateKeyboard(self, msg):
        orig = str(msg)
        trans = str(msg)

        for orig, breakdown in cm.patternMatchAll(cm.KEYBOARD_SEP, msg):
            s, e, txt = orig
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
                    # solving the problem :term:`:abbr:`something (explanation)``
                    tran = self.recomposeAbbrevTranslation(orig_txt, tran)
                    tran = f"{tran} -- {orig_txt}"
                else:
                    tran = f"-- {orig_txt}"
                tran_txt = tran_txt[:s] + tran + tran_txt[e:]
        else:
            orig_txt = msg
            tran, ref_is_fuzzy, ref_is_ignore = self.translate(orig_txt)
            if ref_is_ignore:
                return None, ref_is_fuzzy, ref_is_ignore

            tran_found = (tran and tran != orig_txt)
            if tran_found:
                tran = self.recomposeAbbrevTranslation(orig_txt, tran)
                tran_txt = f"{tran} -- {orig_txt}"
            else:
                tran_txt = f" -- {orig_txt}"
        return tran_txt, ref_is_fuzzy, ref_is_ignore

    def translateMenuSelection(self, msg):
        men_is_fuzzy = False
        men_is_ignore = False
        tran_txt = str(msg)
        word_list = cm.findInvert(cm.MENU_SEP, msg)
        for loc, word in word_list.items():
            s, e = loc
            tran, is_fuzzy, is_ignore = self.translate(word)
            if is_ignore:
                men_is_fuzzy = is_fuzzy
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
        all_matches = cm.patternMatchAllAsDictNoDelay(cm.ABBR_TEXT, msg)
        if not all_matches:
            return None, False, False

        return_list = []
        tran = str(msg)
        is_fuzzy_list = []
        is_ignore_list = []
        matched_list = all_matches.values()
        for item_list in matched_list:
            list_length = len(item_list)
            has_sub_item = (list_length > 1)
            if has_sub_item:
                loc, abbrev_explain_txt = item_list[1]
            else:
                loc, abbrev_explain_txt = item_list[0]

            s, e = loc
            tran, is_fuzzy, is_ignore = self.translate(abbrev_explain_txt)
            is_fuzzy_list.append(is_fuzzy)
            is_ignore_list.append(is_ignore)

            if is_ignore:
                continue

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
