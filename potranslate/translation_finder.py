import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
sys.path.append('/Users/hoangduytran/blender_manual/potranslate')
# print(f'translation_finder sys.path: {sys.path}')

import io
import os
import re
from common import Common as cm
from common import _, pp
from ignore import Ignore as ig
import json
from collections import OrderedDict, defaultdict
from sphinx_intl import catalog as c
from babel.messages.catalog import Message
from babel.messages import pofile
from common import DEBUG
    # , DIC_LOWER_CASE
from reftype import RefType


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
            # _(f'key:{k}, hash_value:{hash_value}')
            return hash_value

        def __eq__(self, other):
            local = self.lower()
            extern = other.lower()
            cond = (local == extern)
            # _(f'local:{local} extern:{extern}')
            return cond

        def __le__(self, other):
            local = self.lower()
            extern = other.lower()
            cond = (local < extern)
            # _(f'local:{local} extern:{extern}')
            return cond

        def __gt__(self, other):
            local = self.lower()
            extern = other.lower()
            cond = (local > extern)
            # _(f'local:{local} extern:{extern}')
            return cond

    def __init__(self, data=None):
        super(NoCaseDict, self).__init__()
        if data is None:
            data = {}
        for key, val in data.items():
            self[key] = val

    def __contains__(self, key):
        key = self.Key(key)
        is_there = super(NoCaseDict, self).__contains__(key)
        # _(f'__contains__:{key}, is_there:{is_there}')
        return is_there

    def __setitem__(self, key, value):
        key = self.Key(key)
        super(NoCaseDict, self).__setitem__(key, value)

    def __getitem__(self, key):
        key = self.Key(key)
        try:
            return super(NoCaseDict, self).__getitem__(key)
        except Exception as e:
            print(e)
            keys = super(NoCaseDict, self).__dict__.keys()
            is_in = (key in keys)
            return is_in


    def __delitem__(self, key):
        key = self.Key(key)
        return super(NoCaseDict, self).__delitem__(key)

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
        new_set = self.getSetByWordCountInRange(word_count, word_count, first_word_list=first_word, is_reversed=is_reversed)
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
        # self.master_dic_file = "/Users/hoangduytran/Documents/po_dictionary_sorted_translated_0001_nodot.json"
        self.master_dic_file = "/Users/hoangduytran/blender_manual/ref_dict_0006.json"
        self.master_dic_backup_file = "/Users/hoangduytran/blender_manual/ref_dict_backup_0005.json"
        self.master_dic_test_file = "/Users/hoangduytran/ref_dict_test_0005.json"
        self.master_dic_backup_list = defaultdict(OrderedDict)

        self.master_dic_list = self.loadJSONDic(file_name=self.master_dic_file)
        # self.writeJSONDic(dict_list=self.master_dic_list, file_name=self.master_dic_test_file)
        self.master_dic_list_count = len(self.master_dic_list)

        test_word = 'January'
        test_again = (test_word in self.master_dic_list)
        if test_again:
            test_again_trans = self.master_dic_list[test_word]
            print(f'test_again_trans: {test_again_trans}')
        # exit(0)
        #
        self.vipo_dic_path = "/Users/hoangduytran/blender_manual/gui/2.80/po/vi.po"
        self.vipo_dic_list = None  # not used

        self.current_po_dir = "/Users/hoangduytran/blender_docs/locale/vi/LC_MESSAGES"
        self.json_dic_file = None

        #self.json_dic_list = self.loadJSONDic(file_name=self.json_dic_file)
        self.json_dic_list = {}
        self.current_po_path = None
        self.current_po_cat = None
        self.setupKBDDicList()

        self.dic_list = defaultdict(int)  # for general purposes
        self.last_backup_dict_stat = os.stat(self.master_dic_backup_file)

        # self.loadVIPOtoDic(self.master_dic_list, self.master_dic_file, is_testing=False)
        # self.loadVIPOtoBackupDic(self.master_dic_list, self.master_dic_file)

        # self.cleanDictList(self.master_dic_list)
        # self.updatePOUsingDic(self.vipo_dic_path, self.master_dic_list, is_testing=False)
        # exit(0)
        # self.updateDict()

    # def listDictRange(self, from_wc_range, to_wc_range):
    #     # keys = self.master_dic_list.keys()
    #     # output_l = []
    #     # for k in keys:
    #     #     wc = len(k.split())
    #     #     found = (wc >= from_wc_range) and (wc <= to_wc_range)
    #     #     if not found:
    #     #         continue
    #     #     v = self.master_dic_list[k]
    #     #     entry=(wc, k, v)
    #     #     output_l.append(entry)
    #     #     # print(f'wc:{wc}; k:{k}; v:{v}')
    #     # outp = sorted(output_l)
    #     # for l in outp:
    #     #     _, k, v = l
    #     #     entry=f'"{k}": "{v}",'
    #     #     print(entry)

    #     range_l = self.master_dic_list.getSetUpToWordCount(1)
    #     for k, v in range_l.items():
    #         entry=f'"{k}": "{v}",'
    #         print(entry)

    def genmap(self, msg):
        part_list = []
        loc_dic = cm.patternMatchAllToList(cm.SPACE_WORD_SEP, msg)
        loc_key = list(loc_dic.keys())

        max_len = len(loc_dic)
        has_only_one_item = (max_len == 1)
        step = 1
        is_finished = False
        while not is_finished:
            for i in range(0, max_len):
                l=[]
                for k in range(i, min(i+step, max_len)):
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
                t = msg[w_s : w_e]

                # print(f's location:{l}, text:{t}')

                entry = ((w_s, w_e), t)
                is_in = (entry in part_list)
                if not is_in:
                    part_list.append(entry)
            step += 1
            is_finish = (step > max_len)
            if is_finish:
                break

        sorted_partlist = sorted(part_list, key=lambda x: len(x[1]), reverse=True )
        return sorted_partlist

    def blindTranslation(self, msg):
        # remove overlapping distances in translation messages by projecting longest translated pieces of text
        # to create a shadow on a blank string. Smaller distances will find if their covering distance has been
        # 'shadowed' (marked) already or not, by examining the 'projected screen' (blank string).
        def removeOverlapped(loc_list, len):
            sample_str = (" " * len)
            marker = '¶'
            len_list = []

            # x[0] = start, x[1] = end, x[1]-x[0] = length of text
            # sort the location list in covering distance, reversed order, larger distance will be on top
            sorted_loc = sorted(loc_list, key=lambda x: x[1]-x[0], reverse=True )
            retain_l = []
            for loc in sorted_loc:
                substr = sample_str[loc[0]:loc[1]]
                is_overlapped = (marker in substr)
                if is_overlapped:
                    continue

                maker_substr = (marker * (loc[1] - loc[0]))
                left_part = sample_str[:loc[0]]
                right_part = sample_str[loc[1]:]
                sample_str = left_part + maker_substr + right_part
                retain_l.append(loc)
            return retain_l

        # removing unused locations (parts) that has been 'overlapped' by larger translated parts
        def cleanupTranslatedDic(retain_loc_list, translated_dict):
            new_translated_dic = []
            for entry in translated_dict:
                ss, ee, orig_sub_text, tran_sub_text = entry
                loc = (ss, ee)
                is_retain = (loc in retain_loc_list)
                if is_retain:
                    new_translated_dic.append(entry)
            return new_translated_dic

        # is_debug = ('developer.blender.org' in msg) or ('system' in msg)
        # if is_debug:
        #     _('DEBUG')
        loc_list=[]
        translated_dic = []
        # generate all possible combinations of string lengths
        loc_map_length_sorted_reverse = self.genmap(msg)

        # translate them all if possible
        for loc, orig_sub_text in loc_map_length_sorted_reverse:
            tran_sub_text = self.isInList(orig_sub_text)
            if not tran_sub_text:
                continue

            loc_list.append(loc)
            ss, ee = loc
            entry = (ss, ee, orig_sub_text, tran_sub_text)
            translated_dic.append(entry)

        # now removing overlapped ditances of translated message (start, end, orig_sub_text, translated_sub_text)
        retail_l = removeOverlapped(loc_list, len(msg))
        # reflect changes in location (removals/retains) in the translated dictionary
        retain_translated_dic = cleanupTranslatedDic(retail_l, translated_dic)

        # sorting in x[1]: end location of text, so the last record of text is used first
        sorted_translated = sorted(retain_translated_dic, key=lambda x: x[1], reverse=True)

        tran_msg = str(msg)
        remain_msg = str(msg) # keep a copy of what is remained, untranslated, so if wanted, can dump them in a dict
        for entry in sorted_translated:
            ss, ee, orig_sub_text, tran_sub_text = entry
            untran_subtext = tran_msg[ss:ee]
            is_same_subtext_and_replaceable = (orig_sub_text == untran_subtext)
            if not is_same_subtext_and_replaceable:
                continue

            # tran_sub_text = cm.matchCase(orig_sub_text, tran_sub_text)
            left = tran_msg[:ss]
            right = tran_msg[ee:]
            blank_str = (' ' * (ee - ss))
            remain_msg = remain_msg[:ss] + blank_str + remain_msg[ee:]
            tran_msg = left + tran_sub_text + right

        untranslated_word_list = remain_msg.split()
        self.addBackupDict(untranslated_word_list)
        return tran_msg

    def addBackupDict(self, msg_list):
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
                    print(error_msg)
                    k = entry
                    v = None
                self.addBackupDictEntry(k, v)
        elif is_tupple:
            k, v = msg_list
            self.addBackupDictEntry(k, v)
        elif is_string:
            self.addBackupDictEntry(msg_list, None)
        else:
            raise Exception(error_msg)

    def addBackupDictEntry(self, msg, tran):
        if ig.isIgnored(msg):
            return

        current_backup_dict_stat = os.stat(self.master_dic_backup_file)
        is_changed = (current_backup_dict_stat.st_mtime != self.last_backup_dict_stat.st_mtime)
        if is_changed:
            self.master_dic_backup_list = self.loadJSONDic(file_name=self.master_dic_backup_file)

        has_tran = (tran is not None)
        if has_tran:
            tran = cm.removeOriginal(msg, tran)
            entry = {msg: tran}
        else:
            entry = {msg: ""}
        self.master_dic_backup_list.update(entry)
        print(f'Added BACKUP dict:{entry}')

    def addMasterDict(self, msg, tran):
        if ig.isIgnored(msg):
            return

        has_tran = (tran is not None)
        if has_tran:
            tran = cm.removeOriginal(msg, tran)
            entry = {msg: tran}
        else:
            entry = {msg: ""}
        self.master_dic_list.update(entry)
        print(f'Added MASTER dict:{entry}')

    def writeBackupDict(self):
        is_changed = (len(self.master_dic_backup_list) > 0)
        if is_changed:
            self.writeJSONDic(dict_list=self.master_dic_backup_list, file_name=self.master_dic_backup_file)
            print(f'wrote BACKUP changes to: {self.master_dic_backup_file}')
            self.last_backup_dict_stat = os.stat(self.master_dic_backup_file)

    def writeMasterDict(self):
        current_count = len(self.master_dic_list)
        is_changed = (self.master_dic_list_count != current_count)
        if is_changed:
            self.writeJSONDic(dict_list=self.master_dic_list, file_name=self.master_dic_file)
            print(f'wrote MASTER changes to: {self.master_dic_file}')

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

    def reloadMasterDict(self):
        self.master_dic_list = self.loadJSONDic(file_name=self.master_dic_file)

    def saveMasterDict(self, to_file=None):
        file_path = (to_file if to_file else self.master_dic_file)
        self.writeJSONDic(dict_list=self.master_dic_list, file_name=file_path)


    def updateDict(self):
        from_file = '/Users/hoangduytran/blender_manual/ref_dict_0004.json'
        to_file = '/Users/hoangduytran/blender_manual/ref_dict_0005.json'
        new_file = '/Users/hoangduytran/blender_manual/ref_dict_0006.json'

        new_dic = NoCaseDict()
        ignore_dic = NoCaseDict()
        from_dict = self.loadJSONDic(file_name=from_file)
        to_dict = self.loadJSONDic(file_name=to_file)

        from_keys = list(sorted(from_dict.keys()))
        debug_text = '2.30 <https://archive.blender.org/development/release-logs/blender-230/>`__ -- October 2003'
        meet = 0
        for k in from_keys:
            # 'Popther panel for adding extra options'
            v, trimmed_k = self.findAndTrimIfNeeded(k, search_dict=new_dic, is_patching_found=False)
            if v:
                print(f'already in new_dic: k:{k}, trimmed_k:{trimmed_k}, v:{v}')
                continue

            is_debug = (debug_text.lower() in k.lower())
            if is_debug:
                meet += 1
                _('DEBUG')

            v, trimmed_k = self.findAndTrimIfNeeded(trimmed_k, search_dict=to_dict, is_patching_found=False)
            if not v:
                v, trimmed_k = self.findAndTrimIfNeeded(k, search_dict=to_dict, is_patching_found=False)

            if v:
                entry={trimmed_k: v}
                new_dic.update(entry)
                print(f'found entry:{entry}')
            else:
                v, trimmed_k = self.findAndTrimIfNeeded(k, search_dict=from_dict, is_patching_found=False)
                entry={trimmed_k: v}
                ignore_dic.update(entry)
                print(f'ignored entry:{entry}')

        to_keys = list(sorted(to_dict.keys()))
        for k in to_keys:
            v, trimmed_k = self.findAndTrimIfNeeded(k, search_dict=new_dic, is_patching_found=False)
            is_in_new_dict = not (v is None)
            if is_in_new_dict:
                print(f'ignored entry in to_dict:{entry}')
                continue

            is_debug = (debug_text.lower() in k.lower())
            if is_debug:
                meet += 1
                _('DEBUG')

            v, trimmed_k = self.findAndTrimIfNeeded(k, search_dict=to_dict, is_patching_found=False)
            entry={trimmed_k: v}
            new_dic.update(entry)
            print(f'added from to_file entry:{entry}')

        from_dict_len = len(from_dict)
        to_dict_len = len(to_dict)
        new_dict_len = len(new_dic)

        self.writeJSONDic(dict_list=new_dic, file_name=new_file)
        exit(0)

    def updateMasterDic(self, is_testing=True):
        from_dic_path = "/Users/hoangduytran/ref_dict_0002.json"
        from_dic_list = self.loadJSONDic(file_name=from_dic_path)
        changed_count = self.updateDicUsingDic(from_dic_list, self.master_dic_list)
        is_changed = (changed_count > 0)
        if is_changed:
            print("Changed:", changed_count)

        is_writing_changes = (is_changed and not is_testing)
        if is_writing_changes:
            print("Writing changes to:", self.master_dic_file)
            self.writeJSONDic(dict_list=self.master_dic_list, file_name=self.master_dic_file)

    def addEntry(self, msg, tran):

        entry = {msg: tran}
        print("addEntry - adding:", entry)
        # self.master_dic_list.update(entry)
        return True

    def loadVIPOtoDic(self, dict_to_update, file_name, is_testing=True):

        DIC_INCLUDE_LOWER_CASE_SET = False
        ignore = [
            "volume",
            "Volume",
        ]
        changed = False
        po_cat = c.load_po(self.vipo_dic_path)
        po_cat_dic = self.poCatToDic(po_cat)
        for k, v in po_cat_dic.items():
            is_ignore = (k in ignore)
            if is_ignore:
                continue

            # print("examine:", k, v)
            update = True
            is_in_old_dic = (k in dict_to_update)
            if is_in_old_dic:
                old_v = dict_to_update[k]
                is_same = (old_v == v)
                if is_same:
                    continue
            else:
                #print("NOT IN DIC:", k, v)
                entry = {k: v}
                dict_to_update.update(entry)
                if is_testing:
                    print("Updating entry:", entry)
                else:
                    changed = True

        if changed:
            _("Written to file:", file_name)
            self.writeJSONDic(dict_to_update, file_name=file_name)

    def replacePOText(self, po_file, rep_list, is_dry_run=True):
        _("replacePOText:", po_file, rep_list, is_dry_run)
        data = None
        with open(po_file, "r") as f:
            data = f.read()

        changed = False
        for k, v in rep_list.items():
            data, change_count = re.subn(k, v, data, flags=re.M)
            is_changed = (change_count > 0)
            if is_changed:
                _("CHANGED", change_count, k, "=>", v)
                changed = True

        if changed:
            _(data)
            _("file:", po_file)
            _("Data has changed:", change_count)
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
        #     _("cleanupPOFile - set_entry", set_entry)
        #     _("cleanupPOFile - string_entry", string_entry)
        #     m.string = ""
        #     changed = True
        if changed:
            _("cleanupPOFile", po_file)
            if (not is_dry_run):
                self.dump_po(po_file, po_cat)

    def cleanDictList(self, dic_list):
        remove_keys = []
        for k, v in dic_list.items():
            is_remove = (k is None) or (len(k) == 0) or ig.isIgnored(k)
            if is_remove:
                entry = {k: v}
                # _("cleanDictList removing:", entry)
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
            _("Replacing:", to_entry)
            _("With:", from_entry)
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
            _("updatePOUsingDic, from:", from_entry, "to:", to_entry)
            m.string = dic_v
            changed = True

        if changed and (not is_testing):
            self.dump_po(pofile, po_cat)

    def mergeVIPODict(self):
        po_cat = c.load_po(self.vipo_dic_path)
        po_dic = self.poCatToDic(po_cat)
        self.master_dic_list.update(po_dic)

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

            #context = (m.context if m.context else "")
            #_("context:{}".format(context))
            #k = (m.id, context)
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

            #_("poCatToDic:", k, v)
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
        try:
            file_path = (self.master_dic_file if (file_name is None) else file_name)
            dic = (self.master_dic_list if (dict_list is None) else dict_list)

            # if DIC_INCLUDE_LOWER_CASE_SET:
            #     dic = cm.removeLowerCaseDic(dic)

            with open(file_path, 'w+', newline='\n', encoding='utf8') as out_file:
                json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
                # out_file.close()

        except Exception as e:
            _("Exception writeDictionary Length of read dictionary:{}".format(len(self.master_dic_list)))
            raise e

    def loadJSONDic(self, file_name=None):
        return_dic = None
        try:
            file_path = (self.master_dic_file if (file_name is None) else file_name)
            dic = {}
            with open(file_path) as in_file:
                dic = json.load(in_file)

            test_word = 'January'
            test_again = (test_word in dic)
            if test_again:
                test_again_trans = dic[test_word]
                print(f'test_again_trans: {test_again_trans}')

            return_dic = NoCaseDict(dic)

        except Exception as e:
            _("Exception readDictionary Length of read dictionary:")
            _(e)
            raise e

        return return_dic

    def trimAndFind(self, pattern, msg, dict_to_use=None):
        # Search to see if msg is trailling with punctuations and symbols which prevents the finding of translation
        # by chopping off trailing symbols, one at a time, and search in dict. Accumulate the count so at end, we know
        # how far on the 'msg' ending should we add to the translation
        count = 0
        temp_msg = str(msg)
        search_dict = (dict_to_use if dict_to_use else self.master_dic_list)

        found = (temp_msg in search_dict)

        m = pattern.search(temp_msg)
        while m and not found:
            m_group = m.group(0)
            temp_msg = pattern.sub("", temp_msg)
            count += 1
            found = (temp_msg in search_dict)
            if found:
                break
            m = pattern.search(temp_msg)
        return count, found, temp_msg

    def findAndTrimIfNeeded(self, msg, search_dict=None, is_patching_found=False):
        head_trimmer = ""
        tail_trimmer = ""
        head_count = 0
        tail_count = 0
        is_found_tran = False
        is_debug = ('Transformation tools and widgets, soft bodies' in msg)
        if is_debug:
            _('DEBUG')

        tail_count, is_found_tran, trimmed_msg = self.trimAndFind(cm.TRAILING_WITH_PUNCT, msg, dict_to_use=search_dict)
        if not is_found_tran:
            head_count, is_found_tran, trimmed_msg = self.trimAndFind(cm.HEADING_WITH_PUNCT, trimmed_msg,
                                                                      dict_to_use=search_dict)

        if not is_found_tran:
            tail_count, is_found_tran, trimmed_msg = self.trimAndFind(cm.TRAILING_WITH_PUNCT, msg, dict_to_use=search_dict)
            if not is_found_tran:
                head_count, is_found_tran, trimmed_msg = self.trimAndFind(cm.HEADING_WITH_PUNCT, trimmed_msg,
                                                                          dict_to_use=search_dict)
        if is_patching_found:
            if head_count:
                head_trimmer = msg[:head_count]
            if tail_count:
                tail_trimmer = msg[-tail_count:]

        if is_found_tran:
            trans = search_dict[trimmed_msg]
            if head_trimmer:
                trans = head_trimmer + trans
            if tail_trimmer:
                trans = trans + tail_trimmer
        else:
            trans = None
        return trans, trimmed_msg

    # def dump_po(self, filename, catalog):
    #     dirname = os.path.dirname(filename)
    #     if not os.path.exists(dirname):
    #         os.makedirs(dirname)
    #
    #     # Because babel automatically encode strings, file should be open as binary mode.
    #     with io.open(filename, 'wb') as f:
    #         pofile.write_po(f, catalog, width=4096)
    #
    def isInList(self, msg, search_dict=None):
        trans = None

        dict_to_use = (search_dict if search_dict else self.master_dic_list)
        is_there = (msg in dict_to_use)
        if is_there:
            trans = dict_to_use[msg]
        else:
            trans, trimmed_msg = self.findAndTrimIfNeeded(msg, search_dict=dict_to_use, is_patching_found=True)
        return trans


    def findTranslation(self, msg):
        trans = None

        # # _("findTranslation:", msg)
        # ex_ga_msg = cm.EXCLUDE_GA.findall(msg)
        # if ex_ga_msg:
        #     # _("findTranslation - ex_ga_msg", msg, ex_ga_msg)
        #     msg = ex_ga_msg[0]

        is_ignore = ig.isIgnored(msg)
        if (is_ignore):
            return None, is_ignore

        orig_msg = str(msg)
        trans = self.isInList(msg)

        has_tran = not (trans is None)
        has_len = (has_tran and (len(trans) > 0))
        has_translation = has_len and (trans != 'None')
        if has_translation:
            trans = cm.removeOriginal(msg, trans)
            # trans = cm.matchCase(orig_msg, trans)

        else:
            trans = None
        if trans is None:
            _(f"NOT found: [{msg}]")
        return trans, is_ignore

    def findTranslationByFragment(self, msg):
        # orig_msg = str(msg)
        trans_list = []
        trans = str(msg)

        word_list = cm.WORD_ONLY_FIND.findall(msg)

        _(f'word_list: {word_list}')
        for origin, breakdown in cm.patternMatchAll(cm.WORD_ONLY_FIND, msg):
            is_end = (origin is None)
            if is_end:
                break

            o_s, o_e, o_txt = origin
            is_possessive = o_txt.endswith("'s")
            if is_possessive:
                o_txt = o_txt[:-2]
            trans_word, is_ignore = self.findTranslation(o_txt)
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

    def translate(self, msg):
        must_mark = False
        is_debug = ('the id for' in msg.lower())
        if is_debug:
            _('DEBUG')

        trans, is_ignore = self.findTranslation(msg)
        if is_ignore:
            return (None, False, is_ignore)

        if not trans:
            trans = self.blindTranslation(msg)
            must_mark = True
        return (trans, must_mark, is_ignore)

    def translateKeyboard(self, msg):
        orig = str(msg)
        trans = str(msg)

        for orig, breakdown in cm.patternMatchAll(cm.KEYBOARD_SEP, msg):
            s, e, txt = orig
            has_dic = (txt in TranslationFinder.KEYBOARD_TRANS_DIC)
            if not has_dic:
                continue

            tr = TranslationFinder.KEYBOARD_TRANS_DIC[txt]
            ll = trans[:s]
            rr = trans[e:]
            trans = ll + tr + rr

        is_the_same = (orig == trans)
        if is_the_same:
            trans = None
        return trans

    def checkIgnore(self, msg):
        is_pure_path = (cm.PURE_PATH.search(msg) is not None)
        is_pure_ref = (cm.PURE_REF.search(msg) is not None)
        is_api_ref = (cm.API_REF.search(msg) is not None)
        is_keep = (ig.isKeep(msg))
        is_keep_contain = (ig.isKeepContains(msg))
        is_ignore = (is_pure_path or is_pure_ref or is_api_ref) and (not(is_keep or is_keep_contain))
        return is_ignore

    def addExtraChar(self, msg, ref_type=None):
        char_tbl = {
            RefType.SNG_QUOTE:"'",
            RefType.DBL_QUOTE:'"',
            RefType.AST_QUOTE:'*'
        }

        insert_char = char_tbl[ref_type]
        if insert_char:
            msg = f'{insert_char}{msg}{insert_char}'
        return msg

    def translateQuoted(self, msg, is_reversed=False, ref_type=None):
        is_ignore = self.checkIgnore(msg)
        if is_ignore:
            return None

        tran, is_fuzzy, is_ignore = self.translate(msg)
        if is_ignore:
            return None

        tran_found = (tran is not None)

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
            tran = f":abbr:`{tran} ({msg})`"
        else:
            tran = f":abbr:`{msg} ({msg})`"
        print(f'translateQuoted: [{msg}] [{tran}]')
        # exit(0)
        return tran

    def translateRefWithLink(self, msg):  # for things like :doc:`something <link>`, and :term:`something <link>`

        is_ignore = self.checkIgnore(msg)
        if is_ignore:
            return None

        tran_txt = str(msg)
        has_ref_link = (cm.REF_LINK.search(msg) is not None)
        if has_ref_link:
            found_list = cm.findInvert(cm.REF_LINK, msg)
            for k, v in reversed(list(found_list.items())):
                s, e, orig_txt = v
                tran, is_fuzzy, is_ignore = self.translate(orig_txt)
                if is_ignore:
                    continue

                tran_found = (tran and tran != orig_txt)
                if tran_found:
                    tran = "{} -- {}".format(tran, orig_txt)
                else:
                    tran = "-- {}".format(orig_txt)
                tran_txt = tran_txt[:s] + tran + tran_txt[e:]
        else:
            orig_txt = msg
            tran, is_fuzzy, is_ignore = self.translate(orig_txt)
            if is_ignore:
                return None
            tran_found = (tran and tran != orig_txt)
            if tran_found:
                tran_txt = "{} -- {}".format(tran, orig_txt)
            else:
                tran_txt = "-- {}".format(orig_txt)
        return tran_txt

    def translateMenuSelection(self, msg):
        tran_txt = str(msg)
        word_list = cm.findInvert(cm.MENU_SEP, msg)
        for k, v in reversed(list(word_list.items())):
            s, e, orig = v
            tran, is_fuzzy, is_ignore = self.translate(orig)
            if is_ignore:
                continue

            is_tran_valid = (tran and (tran != orig))
            if is_tran_valid:
                entry = "{} ({})".format(tran, orig)
            else:
                entry = "({})".format(orig)
            tran_txt = tran_txt[:s] + entry + tran_txt[e:]

        return tran_txt

    def translateAbbrev(self, msg):
        tran_txt = str(msg)
        for orig, breakdown in cm.patternMatchAll(cm.ABBR_TEXT, tran_txt):
            os, oe, otxt = orig
            has_breakdown = (breakdown and len(breakdown) > 0)
            if not has_breakdown:
                continue

            for bs, be, btxt in breakdown:
                tran, is_fuzzy, is_ignore = self.translate(btxt)
                if is_ignore:
                    continue
                valid = (tran and (tran != btxt))
                if valid:
                    entry = "{} -- {}".format(btxt, tran)
                else:
                    entry = "-- {}".format(btxt)
                s = os + bs
                e = oe + be
                tran_txt = tran_txt[:s] + entry + tran_txt[e:]

        return tran_txt

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
                _("mark for removal:", k, v)
                remove_key.append(k)

            # remove null from v
            has_value = (v is not None)
            if not has_value:
                _("mark due to blanking value:", k, v)
                blank_key.append(k)

        for k in blank_key:
            _("actually blanking:", k)
            entry = {k: ""}
            dic_list.update(entry)

        # run through the keys and remove entry from the dic_list
        for k in remove_key:
            _("acutally removing:", k)
            del dic_list[k]
