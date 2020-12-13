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
from babel.messages.catalog import Message
from babel.messages import pofile
from common import DEBUG
# , DIC_LOWER_CASE
from reftype import RefType
import operator as OP
from pprint import pprint

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

        super(NoCaseDict, self).__init__()
        if data is None:
            data = {}
        for key, val in data.items():
            self[key] = val
            # dd(f'__init__:[{key}], value:[{val}]')
        self.is_operational = True

    def __contains__(self, key):
        key = self.Key(key)
        is_there = super(NoCaseDict, self).__contains__(key)
        dd(f'__contains__:[{key}], is_there:{is_there}')
        return is_there

    def __setitem__(self, key, value):
        key = self.Key(key)
        super(NoCaseDict, self).__setitem__(key, value)
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
        self.master_dic_file = os.path.join(home_dir, "blender_manual/ref_dict_0006_0002.json")
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
        self.master_dic_list = None
        self.backup_dic_list = None
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
        def append_selective(cover_length, new_text, trans, selective_list, function_name):
            entry = (cover_length, new_text, trans, function_name)
            selective_list.append(entry)

        trans = None
        original_text = str(msg)
        selective_list = []
        try:
            for f, params in self.tran_find_func_list:
                txt, param1, param2 = params
                is_empty = not (param1 and param2)
                if is_empty:
                    new_text, trans, cover_length = f(msg)
                else:
                    new_text, trans, cover_length = f(msg, param1, param2)
                append_selective(cover_length, new_text, trans, selective_list, f.__name__)
            sorted_selective_list = list(sorted(selective_list, reverse=True))
            chosen_entry = sorted_selective_list[0]
            cover_length, new_text, trans, function_name = chosen_entry
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

            # sorted the list by text length (maximum covering distance goes first, key=0), that's reverse=True is for
            # filter function will check if the location is already in local location database or that location is ALREADY
            # covered (overlapped) by previous instances.
            filtered_translated_list = list(filter(filter_function, sorted(loc_translated_list, key=OP.itemgetter(0), reverse=True)))

            filtered_translated_list.sort(key=OP.itemgetter(1, 0))
            filtered_translated_list.reverse()

            for loc_covered_length, local_location, loc_dict_txt, loc_tran_txt in filtered_translated_list:
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
        covered_length = 0
        translation = str(text)
        # must masking after replacement, even entries are in local_dict, because definitions could overlapped (Vertex Group Weight/Clean Vertext Group for instance)
        for untran_txt, tran_txt in local_dict.items():
            cm.debugging(untran_txt)
            non_word_char_list = cm.NON_WORD_FIND.findall(untran_txt)
            has_none_word_char = (len(non_word_char_list) > 0)
            if has_none_word_char:
                p = r'%s' % (re.escape(untran_txt))
            else:
                p = r'\b%s\b' % (untran_txt)
            pat = re.compile(p, flags=re.I)
            found_dict = cm.patternMatchAllToDict(pat, masking_string)
            is_found = (len(found_dict) > 0)
            if not is_found:
                continue

            found_item_list = list(found_dict.items())
            for loc, dict_txt in found_item_list:
                empty_part = (cm.FILLER_CHAR * len(dict_txt))
                ss, ee = loc

                # update every instance found in the temp_translation with already found translation text
                txt_length = len(dict_txt)
                tran_dict_entry = (txt_length, loc, dict_txt, tran_txt)
                translated_list.append(tran_dict_entry)

                left = masking_string[:ss]
                right = masking_string[ee:]
                masking_string = left + empty_part + right

                # if the translation has provided fully then it's enough to get out
                loc, tester_left = cm.removingNonAlpha(left)
                loc, tester_right = cm.removingNonAlpha(right)
                is_translation_provided_fully = not (tester_left or tester_right)
                if is_translation_provided_fully:
                    # replacing dict into text and finish
                    print(f'FINISH EARLY: is_translation_provided_fully = TRUE')
                    temp_translation = translatedListToText(translated_list, translation, filerLocation)
                    print(f'translation:[{translation}]; temp_translation:[{temp_translation}]')
                    return temp_translation

        # for untranslated words, we will try to find definitions for each, using reductions
        # check to see if untranslated word
        has_translatable_characters = (re.search(r'[a-zA-Z]+', masking_string) is not None)
        if not has_translatable_characters:
            temp_translation = translatedListToText(translated_list, translation, filerLocation)
            return temp_translation

        un_tran_list = cm.findInvert(cm.FILLER_CHAR_PATTERN,
                                     masking_string,
                                     is_remove_empty=True,
                                     is_removing_surrounding_none_alphas=True)

        for k, v in un_tran_list.items():
            remain_loc, un_tran_txt = v
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
                txt_length = len(un_tran_txt)
                tran_dict_entry = (txt_length, remain_loc, un_tran_txt, tran_sub_text)
                translated_list.append(tran_dict_entry)

        # replacing dict into text and finish
        temp_translation = translatedListToText(translated_list, translation, filerLocation)
        has_translation = not (temp_translation == text)
        if not has_translation:
            return None
        else:
            return temp_translation

    def buildLocalTranslationDict(self, msg):
        translation = str(msg)
        loc_list = []
        translated_list = []
        untranslated_list = []
        local_translated_dict = {} # for quick, local translation

        # generate all possible combinations of string lengths
        loc_map_length_sorted_reverse = self.genmap(msg)

        dd(f'loc_map_length_sorted_reverse: {loc_map_length_sorted_reverse}')
        # translate them all if possible, store in local dict
        for loc, orig_sub_text in loc_map_length_sorted_reverse:
            is_ignore = (ig.isIgnored(orig_sub_text))
            if is_ignore:
                continue

            is_ok = 1
            # dd(f'blindTranslation: loc:{loc} orig_sub_text:{orig_sub_text}')
            tran_sub_text = self.isInDict(orig_sub_text)
            ss, ee = loc

            if not tran_sub_text:
                cleaned_loc, cleaned_orig_sub_text = cm.removingNonAlpha(orig_sub_text)
                temp_tran_sub_text = self.isInDict(cleaned_orig_sub_text)
                if temp_tran_sub_text:
                    cl_s, cl_e = cleaned_loc
                    cl_left = orig_sub_text[:cl_s]
                    cl_right = orig_sub_text[cl_e:]
                    tran_sub_text = cl_left + temp_tran_sub_text + cl_right

            if tran_sub_text:
                local_dict_entry = {orig_sub_text: tran_sub_text}
                local_translated_dict.update(local_dict_entry)

        # print('blindTranslation:')
        # print(f'msg: {msg}')
        # print(f'local_translated_dict:')
        # pprint(local_translated_dict)
        return local_translated_dict

    def blindTranslation(self, msg):
        cm.debugging(msg)
        if ig.isIgnored(msg):
            return None

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
        # if DIC_LOWER_CASE:
        #     k_lower = k.lower()
        #     is_same = (k_lower == k)
        #     if not is_same:
        #         entry = {k_lower: v}
        #         self.master_dic_list.update(entry)
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

            # dd("poCatToDic:", k, v)
            # if DIC_LOWER_CASE:
            #     #lower_k = (m.id.lower(), context.lower())
            #     lower_k = m.id.lower()
            #     is_same_key = (k == lower_k)
            #     if not is_same_key:
            #         lower_entry = {lower_k: v}
            #         po_cat_dic.update(lower_entry)

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

            return_dic = NoCaseDict(dic)
            # cm.testDict(return_dic)

        except Exception as e:
            dd("Exception occurs while performing loadJSONDic()")
            dd(e)
            return_dic = NoCaseDict()

        return return_dic

    def isInDict(self, msg, dic_to_use=None):
        search_dict = (dic_to_use if dic_to_use else self.master_dic)
        if not search_dict:
            msg = 'NO Dictionary is available. Stopped'
            print(msg)
            raise Exception(msg)

        is_found = (msg in search_dict)
        if is_found:
            tran = search_dict[msg]
            tran = cm.matchCase(msg, tran)
            dd(f'{msg} => {tran}')
        else:
            tran = None
        return tran

    # def trimAndFind(self, pattern, msg, dict_to_use=None):
    #     # Search to see if msg is trailling with punctuations and symbols which prevents the finding of translation
    #     # by chopping off trailing symbols, one at a time, and search in dict. Accumulate the count so at end, we know
    #     # how far on the 'msg' ending should we add to the translation
    #     count = 0
    #     temp_msg = str(msg)
    #     search_dict = (dict_to_use if dict_to_use else self.master_dic)
    #
    #     found = (temp_msg in search_dict)
    #
    #     m = pattern.search(temp_msg)
    #     tran = None
    #     while m and not found:
    #         m_group = m.group(0)
    #         temp_msg = pattern.sub("", temp_msg)
    #         count += 1
    #         found = (temp_msg in search_dict)
    #         if found:
    #             tran = search_dict[temp_msg]
    #             break
    #         m = pattern.search(temp_msg)
    #     return count, temp_msg, tran

    # def findAndTrimIfNeeded(self, msg, search_dict=None, is_patching_found=False):
    #     head_trimmer = ""
    #     tail_trimmer = ""
    #     head_count = 0
    #     tail_count = 0
    #     is_found_tran = False
    #     cover_length = 0
    #     tail_count, trimmed_msg, trans = self.trimAndFind(cm.TRAILING_WITH_PUNCT, msg,
    #                                                       dict_to_use=search_dict)
    #     is_found_tran = (trans and not trans == msg)
    #     if not is_found_tran:
    #         head_count, trimmed_msg, trans = self.trimAndFind(cm.HEADING_WITH_PUNCT, trimmed_msg,
    #                                                                   dict_to_use=search_dict)
    #     is_found_tran = (trans and not trans == msg)
    #     if not is_found_tran:
    #         tail_count, trimmed_msg, trans = self.trimAndFind(cm.TRAILING_WITH_PUNCT, msg,
    #                                                                   dict_to_use=search_dict)
    #         is_found_tran = (trans and not trans == msg)
    #         if not is_found_tran:
    #             head_count, trimmed_msg, trans = self.trimAndFind(cm.HEADING_WITH_PUNCT, trimmed_msg,
    #                                                                       dict_to_use=search_dict)
    #     if is_patching_found:
    #         if head_count:
    #             head_trimmer = msg[:head_count]
    #         if tail_count:
    #             tail_trimmer = msg[-tail_count:]
    #
    #     if is_found_tran:
    #         cover_length = len(msg)
    #         is_insert_head_trimmer = (head_trimmer and not trans.startswith(head_trimmer))
    #         if is_insert_head_trimmer:
    #             trans = head_trimmer + trans
    #         is_insert_tail_trimmer = (tail_trimmer and not trans.endswith(tail_trimmer))
    #         if is_insert_tail_trimmer:
    #             trans = trans + tail_trimmer
    #     else:
    #         trans = None
    #     return trimmed_msg, trans, cover_length

    def isInListByDict(self, msg, is_master):
        search_dic = (self.master_dic if is_master else self.backup_dic)
        return self.isInDict(msg, dic_to_use=search_dic)

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

            trans = self.isInDict(new_txt)
            if trans:
                cover_length = len(txt)
                return new_txt, trans, cover_length
        return txt, None, cover_length

    # def reduceFind(self, txt: str):
    #     if not txt:
    #         return txt, None
    #
    #     # new_txt, trans = self.removeStarAndEndingPunctuations(txt)
    #     # if not trans or (trans == txt):
    #     new_txt, trans, cover_length = self.translationByRemovingSymbols(txt)
    #     if not trans or (trans == txt):
    #         new_txt, trans, cover_length = self.translationByReplacingSymbolsWithSpaces(txt)
    #     if not trans or (trans == txt):
    #         new_txt, trans, cover_length = self.removeByPatternListAndCheck(txt, cm.common_suffix_sorted, cm.END_WORD)
    #     if not trans or (trans == txt):
    #         new_txt, tran, cover_length = self.removeByPatternListAndCheck(txt, cm.common_prefix_sorted, cm.START_WORD)
    #     if not trans or (trans == txt):
    #         new_txt, tran, cover_length = self.removeBothByPatternListAndCheck(txt, cm.common_prefix_sorted, cm.common_suffix_sorted)
    #     return new_txt, trans

    def insertTranslation(self, orig_str: str, orig_word: str, new_word: str, current_trans: str) -> str:
        is_valid = (orig_str and orig_word and new_word and current_trans)
        if not is_valid:
            return current_trans

        list_of_remain_loc = cm.locRemain(orig_word, new_word)
        new_tran = str(current_trans)
        for ss, ee in list_of_remain_loc:
            left = orig_word[:ss]
            right = orig_word[ee:]
            new_tran = left + current_trans + right
        trans = new_tran
        return trans

    def tryToFindTranslation(self, txt: str) -> str:
        cover_length = 0
        separator_list = [
            cm.SPACES,
            cm.SYMBOLS,
        ]

        new_text, trans, cover_length = self.findByReduction(txt)
        is_found_trans = (trans and not trans == txt)
        if is_found_trans:
            return txt, trans, cover_length

        translated_dict = {}
        translation = str(txt)
        for separator in separator_list:
            found_dict = cm.findInvert(separator, txt, is_remove_empty=True, is_removing_surrounding_none_alphas=True)
            if not found_dict:
                continue

            for k, v in found_dict.items():
                loc, orig_txt = v
                s, e = loc

                is_ignore = ig.isIgnored(orig_txt)
                if is_ignore:
                    continue

                new_text = str(orig_txt)
                trans = self.isInDict(orig_txt)
                is_found_trans = (trans and not trans == orig_txt)
                if not is_found_trans:
                    new_text, trans, cover_length = self.findByReduction(orig_txt)

                is_found_trans = (trans and not trans == orig_txt)
                if is_found_trans:
                    trans = self.insertTranslation(txt, orig_txt, new_text, trans)
                    translated_entry = {s: (loc, orig_txt, trans)}
                    translated_dict.update(translated_entry)

            for k, v in translated_dict.items():
                loc, orig_txt, trans = v
                s, e = loc
                left = translation[:s]
                right = translation[e:]
                translation = left + trans + right
                cover_length += len(orig_txt)

        return txt, translation, cover_length

    # def symbolsRemoval(self, txt):
    #     cover_length = 0
    #     match = cm.SYMBOLS.search(txt)
    #     has_hyphen = bool(match)
    #     if not has_hyphen:
    #         return txt, None, cover_length
    #
    #     len_of_txt = len(txt)
    #     pattern, trans, cover_length = self.removeStarAndEndingPunctuations(txt)
    #     if trans:
    #         cover_length = len_of_txt
    #         return pattern, trans, cover_length
    #     else:
    #         is_fuzzy, trans, cover_length = self.translateWordsAtSymbolBoundary(txt)
    #         if trans and not is_fuzzy:
    #             cover_length = len_of_txt
    #             return txt, trans, cover_length
    #         else:
    #             pattern, trans, cover_length = self.translationByRemovingSymbols(txt)
    #             if trans:
    #                 cover_length = len_of_txt
    #                 return pattern, trans, cover_length
    #             else:
    #                 pattern, trans, cover_length = self.translationByReplacingSymbolsWithSpaces(txt)
    #                 if trans:
    #                     cover_length = len_of_txt
    #                     return pattern, trans, cover_length
    #     return txt, None, cover_length

    def removeStarAndEndingPunctuations(self, txt):
        new_txt = cm.ENDS_PUNCTUAL_MULTI.sub('', txt)
        new_txt = cm.BEGIN_PUNCTUAL_MULTI.sub('', new_txt)

        cover_length = 0
        # dd(f'removeStarAndEndingPunctuations: {txt} => {new_txt}')

        is_ignore = ig.isIgnored(txt)
        if is_ignore:
            return txt, None

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

                if ig.isIgnored(test_text_more):
                    continue

                if ig.isIgnored(test_text_less):
                    continue

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
            tran = self.isInDict(test_text)
            if not tran:
                is_double_ending = (len(test_text) > 2) and (test_text[-1] == test_text[-2])
                if is_double_ending:
                    test_text = test_text[:-1]
                    tran = self.isInDict(test_text)

            if tran:
                cover_length = len(txt)
                return test_text, tran, cover_length
        return txt, None, cover_length

    def removeByPatternListAndCheck(self, txt, part_list, at):
        cover_length = 0
        txt_len = len(txt)
        tran = self.isInDict(txt)
        if tran:
            cover_length = txt_len
            return txt, tran, cover_length

        is_at_start = (at == cm.START_WORD)
        is_at_end = (at == cm.END_WORD)
        test_text = str(txt)
        if is_at_start:
            test_text = cm.NON_WORD_STARTING.sub("", test_text)
        elif is_at_end:
            test_text = cm.NON_WORD_ENDING.sub("", test_text)

        is_ignore = ig.isIgnored(test_text)
        if (is_ignore):
            return txt, None, cover_length

    # part_list = ['like', '-like']
        word_len = len(test_text)
        text_before_cutoff = str(test_text)
        # pp(part_list)
        for part in part_list:
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
                    cover_length = txt_len
                    if fix_tran:
                        tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                    return test_text, tran, cover_length

            tran = self.isInDict(test_text)
            if tran:
                cover_length = txt_len
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
                    cover_length = txt_len
                    if fix_tran:
                        tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                    return test_text, tran, cover_length
                else:
                    chopped_txt, tran = self.reduceDuplicatedEnding(test_text)
                    if tran:
                        cover_length = txt_len
                        tran = self.fixTranslationWithKnowsPrefixSuffixes(text_before_cutoff, tran, is_prefix=False)
                        return chopped_txt, tran, cover_length

            chopped_txt, tran = self.reduceDuplicatedEnding(text_before_cutoff)
            if tran:
                cover_length = txt_len
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




    # def findDictByRemoveCommonPrePostFixes(self, txt):
    #     new_txt, tran, cover_length = self.tryToFindTran(txt)
    #     if not tran:
    #         overall_cover_length = 0
    #         tran_txt = str(txt)
    #         # split into separated words, treat each independently
    #         # word_dict_list = cm.patternMatchAllToDict(cm.WORD_SEP, txt)
    #         word_dict_list = cm.patternMatchAllToDict(cm.SPACE_SEP_WORD, txt)
    #         tran_dic = {}
    #         for loc, word in word_dict_list.items():
    #             s, e = loc
    #             new_txt, tran, cover_length = self.tryToFindTran(word)
    #             replacement = (tran if tran else word)
    #             entry = {s: (s, e, replacement, cover_length)}
    #             tran_dic.update(entry)
    #
    #         sorted_tran_dic = sorted(list(tran_dic.items()), reverse=True)
    #         for k, entry in sorted_tran_dic:
    #             s, e, replacement, cover_length = entry
    #             left = tran_txt[:s]
    #             right = tran_txt[e:]
    #             tran_txt = left + replacement + right
    #             overall_cover_length += cover_length
    #         cover_length = overall_cover_length
    #         tran = tran_txt
    #     return new_txt, tran, cover_length


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

        # # dd("findTranslation:", msg)
        # ex_ga_msg = cm.EXCLUDE_GA.findall(msg)
        # if ex_ga_msg:
        #     # dd("findTranslation - ex_ga_msg", msg, ex_ga_msg)
        #     msg = ex_ga_msg[0]

        is_ignore = ig.isIgnored(msg)
        if (is_ignore):
            return None, is_ignore

        orig_msg = str(msg)
        trans = self.isInDict(orig_msg)

        has_tran = not (trans is None)
        has_len = (has_tran and (len(trans) > 0))
        has_translation = has_len and (trans != 'None')
        if has_translation:
            trans = cm.removeOriginal(msg, trans)
            trans = self.removeTheWord(trans)
        else:
            trans = None
        if trans is None:
            dd(f"NOT found: [{msg}]")
        return trans, is_ignore

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
            trans_word, is_ignore, weight = self.findTranslation(o_txt)
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
        try:
            is_fuzzy = False
            trans, is_ignore = self.findTranslation(msg)
            if is_ignore:
                return (None, False, is_ignore)

            if not trans:
                dd(f'calling blindTranslation')
                trans = self.blindTranslation(msg)
                is_fuzzy = True

            if trans:
                is_same = (trans == msg)
                if is_same:
                    trans = None
                else:
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
            for k, v in reversed(list(found_list.items())):
                loc, orig_txt = v
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
        for k, v in word_list.items():
            loc, word = v
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
        for k, v in word_list_dict.items():
            loc, orig_txt = v
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
