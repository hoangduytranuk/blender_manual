import sys
sys.path.append('/Users/hoangduytran/blender_manual/potranslate')

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
from common import DEBUG, DIC_LOWER_CASE


class CaseInsensitiveDict(dict):

    class Key(str):
        def __init__(self, key):
            str.__init__(key)

        def __hash__(self):
            k = self.lower()
            hash_value = hash(k)
            _(f'key:{k}, hash_value:{hash_value}')
            return hash_value

        def __eq__(self, other):
            local = self.lower()
            extern = self.lower()
            cond = (local == extern)
            _(f'local:{local} extern:{extern}')
            return cond

    def __init__(self, data=None):
        super(CaseInsensitiveDict, self).__init__()
        if data is None:
            data = {}
        for key, val in data.items():
            self[key] = val

    def __contains__(self, key):
        key = self.Key(key)
        is_there = super(CaseInsensitiveDict, self).__contains__(key)
        _(f'__contains__:{key}, is_there:{is_there}')
        return is_there

    def __setitem__(self, key, value):
        key = self.Key(key)
        super(CaseInsensitiveDict, self).__setitem__(key, value)

    def __getitem__(self, key):
        key = self.Key(key)
        return super(CaseInsensitiveDict, self).__getitem__(key)

    # def __setitem__(self, key, value):
    #     key = CaseInsensitiveKey(key)
    #     super(CaseInsensitiveDict, self).__setitem__(key, value)
    # def __getitem__(self, key):
    #     key = CaseInsensitiveKey(key)
    #     return super(CaseInsensitiveDict, self).__getitem__(key)


class TranslationFinder:

    KEYBOARD_TRANS_DIC = {
        r"\bWheelUp\b": "Lăn Bánh Xe về Trước (WheelUp)",
        r"\bWheelDown\b": "Lăn Bánh Xe về Sau (WheelDown)",
        r"\bWheel\b": "Bánh Xe (Wheel)",
        "NumpadPlus": "Dấu Cộng (+) Bàn Số (NumpadPlus)",
        "NumpadMinus": "Dấu Trừ (-) Bàn Số (NumpadMinus)",
        "NumpadSlash": "Dấu Chéo (/) Bàn Số (NumpadSlash)",
        "NumpadDelete": "Dấu Xóa/Del Bàn Số (NumpadDelete)",
        "NumpadPeriod": "Dấu Chấm (.) Bàn Số (NumpadDelete)",
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
        r"\bDown\b": "Xuống (Down)",
        r"\bUp\b": "Lên (Up)",
        r"\bComma\b": "Dấu Phẩy (Comma)",
        r"\bMinus\b": "Dấu Trừ (Minus)",
        r"\bPlus\b": "Dấu Cộng (Plus)",
        "Left": "Trái (Left)",
        "=": "Dấu Bằng (=)",
        "Right": "Phải (Right)",
        "Backslash": "Dấu Chéo Ngược (Backslash)",
        r"\bSlash\b": "Dấu Chéo (Slash)",
        "AccentGrave": "Dấu Huyền (AccentGrave)",
        "Delete": "Xóa (Delete)",
        "Period": "Dấu Chấm (Period)",
        "Comma": "Dấu Phẩy (Comma)",
        "PageDown": "Trang Xuống (PageDown)",
        "PageUp": "Trang Lên (PageUp)",
        "PgDown": "Trang Xuống (PgDown)",
        "PgUp": "Trang Lên (PgUp)",
        "OSKey": "Phím Hệ Điều hành (OSKey)",
        "Slash": "Dấu Chéo (Slash)",
        "Backslash": "Dấu Chéo Ngược (Backslash)",
        "Minus": "Dấu Trừ (Minus)",
        "Plus": "Dấu Cộng (Plus)",
        "Down": "Xuống (Down)",
        "Up": "Lên (Up)",
        "MMB": "NCG (MMB)",
        "LMB": "NCT (LMB)",
        "RMB": "NCP (RMB)",
        "Pen": "Bút (Pen)"
    }

    def __init__(self):
        self.update_dic = 0
        self.update_po_file = None
        # self.master_dic_file = "/Users/hoangduytran/Documents/po_dictionary_sorted_translated_0001_nodot.json"
        self.master_dic_file = "/Users/hoangduytran/blender_manual/ref_dict_0003.json"
        # self.master_dic_backup_file = "/Users/hoangduytran/ref_dict_0003.json"
        #self.master_dic_file = "/Users/hoangduytran/ref_dict_0002.json"
        self.master_dic_backup_list = defaultdict(OrderedDict)

        self.master_dic_list = self.loadJSONDic(file_name=self.master_dic_file)
        test_again = ('make' in self.master_dic_list)
        if test_again:
            test_again_trans = (self.master_dic_list['make'])
            _(f'test_again_trans: make = {test_again_trans}')

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

        # self.loadVIPOtoDic(self.master_dic_list, self.master_dic_file, is_testing=False)
        # self.loadVIPOtoBackupDic(self.master_dic_list, self.master_dic_file)

        # self.cleanDictList(self.master_dic_list)
        # self.updatePOUsingDic(self.vipo_dic_path, self.master_dic_list, is_testing=False)
        # exit(0)

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
        if DIC_LOWER_CASE:
            k_lower = k.lower()
            is_same = (k_lower == k)
            if not is_same:
                entry = {k_lower: v}
                self.master_dic_list.update(entry)
        return True

    def loadPOAsDic(self, po_path):
        po_cat = c.load_po(po_path)
        po_dic = self.poCatToDic(po_cat)
        return po_dic

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
            if DIC_LOWER_CASE:
                #lower_k = (m.id.lower(), context.lower())
                lower_k = m.id.lower()
                is_same_key = (k == lower_k)
                if not is_same_key:
                    lower_entry = {lower_k: v}
                    po_cat_dic.update(lower_entry)

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

            with open(file_path, 'w', newline='\n', encoding='utf8') as out_file:
                json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
                # out_file.close()

        except Exception as e:
            _("Exception writeDictionary Length of read dictionary:{}".format(len(self.master_dic_list)))
            raise e

    def loadJSONDic(self, file_name=None):
        local_dic = None
        try:
            file_path = (self.master_dic_file if (file_name is None) else file_name)
            dic = None
            with open(file_path) as in_file:
                dic = json.load(in_file)

            if DIC_LOWER_CASE:
                lower_dic = {}
                if dic:
                    for k, v in dic.items():
                        entry = {k.lower(): v}
                        # _(entry)
                        lower_dic.update(entry)
                dic = lower_dic
        except Exception as e:
            _("Exception readDictionary Length of read dictionary:")
            _(e)
            raise e

        return dic
        # return insensitive_dic

    # def dump_po(self, filename, catalog):
    #     dirname = os.path.dirname(filename)
    #     if not os.path.exists(dirname):
    #         os.makedirs(dirname)
    #
    #     # Because babel automatically encode strings, file should be open as binary mode.
    #     with io.open(filename, 'wb') as f:
    #         pofile.write_po(f, catalog, width=4096)
    #
    def isInList(self, msg, is_lower=False):
        trans = None

        try:
            if is_lower:
                msg = msg.lower()
            trans = self.master_dic_list[msg]
            # _(f'isInList:[{msg}], {is_lower}, [{trans}]')
            return trans
        except Exception as e:
            # if msg:
            #     _(msg)
            # _("is_lower:", is_lower)
            #raise e
            return None

    def findTranslation(self, msg):
        trans = None

        # _("findTranslation:", msg)
        ex_ga_msg = cm.EXCLUDE_GA.findall(msg)
        if (len(ex_ga_msg) > 0):
            # _("findTranslation - ex_ga_msg", msg, ex_ga_msg)
            msg = ex_ga_msg[0]

        is_ignore = ig.isIgnored(msg)
        if (is_ignore):
            return None

        orig_msg = str(msg)
        msg, begin_with_punctuations, ending_with_punctuations = cm.beginAndEndPunctuation(msg, is_single=True)
        trans = self.isInList(msg, is_lower=True)
        has_tran = (trans is not None)
        if not has_tran:
            msg, begin_with_punctuations, ending_with_punctuations = cm.beginAndEndPunctuation(msg, is_single=False)
            trans = self.isInList(msg, is_lower=True)

        has_tran = not (trans is None)
        has_len = (has_tran and (len(trans) > 0))
        has_translation = has_len and (trans != 'None')
        if has_translation:
            trans = trans.strip()
            trans = cm.removeOriginal(msg, trans)
            trans = cm.matchCase(orig_msg, trans)

            if ending_with_punctuations or begin_with_punctuations:
                trans = orig_msg.replace(msg, trans)
        else:
            trans = None
        if trans is None:
            _(f"NOT found: [{msg}]")
        return trans

    def findTranslationByFragment(self, msg):
        # orig_msg = str(msg)
        trans_list = []
        trans = str(msg)

        for origin, breakdown in cm.patternMatchAll(cm.WORD_ONLY_FIND, msg):
            is_end = (origin is None)
            if is_end:
                break

            o_s, o_e, o_txt = origin
            trans_word = self.findTranslation(o_txt)
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

        trans = self.findTranslation(msg)
        if not trans:
            trans = self.findTranslationByFragment(msg)
            must_mark = True
        return (trans, must_mark)

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

    def translateQuoted(self, msg, is_reversed=False):
        is_ignore = self.checkIgnore(msg)
        if is_ignore:
            return None

        tran, is_fuzzy = self.translate(msg)
        tran_found = (tran is not None)

        orig_msg = str(msg)
        ex_ga_msg = cm.EXCLUDE_GA.findall(msg)
        if (len(ex_ga_msg) > 0):
            msg = ex_ga_msg[0]

        if tran_found:
            orig_tran = str(tran)
            ex_ga_msg = cm.EXCLUDE_GA.findall(tran)
            if (len(ex_ga_msg) > 0):
                tran = ex_ga_msg[0]

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
                tran, is_fuzzy = self.translate(orig_txt)
                tran_found = (tran and tran != orig_txt)
                if tran_found:
                    tran = "{} -- {}".format(tran, orig_txt)
                else:
                    tran = "-- {}".format(orig_txt)
                tran_txt = tran_txt[:s] + tran + tran_txt[e:]
        else:
            orig_txt = msg
            tran, is_fuzzy = self.translate(orig_txt)
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
            tran, is_fuzzy = self.translate(orig)
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
                tran, is_fuzzy = self.translate(btxt)
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
