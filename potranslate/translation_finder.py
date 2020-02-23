import sys
sys.path.append('/Users/hoangduytran/PycharmProjects/potranslate')

from common import Common as cm
from common import _, pp
from ignore import Ignore as ig
import json
from collections import OrderedDict, defaultdict

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
        "Period": "Dấu Chấm (Period)",
        "PageDown": "Trang Xuống (PageDown)",
        "PageUp": "Trang Lên (PageUp)",
        "PgDown": "Trang Xuống (PgDown)",
        "PgUp": "Trang Lên (PgUp)",
        "OSKey": "Phím Hệ Điều hành (OSKey)",
        "MMB": "NCG (MMB)",
        "LMB": "NCT (LMB)",
        "RMB": "NCP (RMB)",
        "Pen": "Bút (Pen)"
    }

    def __init__(self):
        self.update_dic = 0
        self.update_po_file = None
        self.master_dic_file = "/Users/hoangduytran/Documents/po_dictionary_sorted_translated_0001_nodot.json"
        self.master_dic_backup_file = "/Users/hoangduytran/Documents/po_dictionary_sorted_translated_0002_new.json"
        self.master_dic_backup_list = defaultdict(OrderedDict)

        self.master_dic_list = self.loadJSONDic(file_name=self.master_dic_file)

        self.vipo_dic_path = "/Users/hoangduytran/blender_manual/gui/2.80/po/vi.po"
        self.vipo_dic_list = None # not used

        self.current_po_dir = "/Users/hoangduytran/blender_docs/locale/vi/LC_MESSAGES"
        self.json_dic_file = None

        #self.json_dic_list = self.loadJSONDic(file_name=self.json_dic_file)
        self.json_dic_list = {}
        self.current_po_path = None
        self.current_po_cat = None
        self.setupKBDDicList()

        self.dic_list = defaultdict(int) # for general purposes

    def poCatToDic(self, po_cat):
        po_cat_dic = defaultdict(OrderedDict)
        for index, m in enumerate(po_cat):
            context = (m.context if m.context else "")
            #print("context:{}".format(context))
            k = (m.id, context)
            lower_k = (m.id.lower(), context.lower())

            is_same_key = (k == lower_k)

            v = m
            entry={k:v}
            po_cat_dic.update(entry)
            #print("poCatToDic:", k, v)
            if not is_same_key:
                lower_entry = {lower_k:v}
                po_cat_dic.update(lower_entry)

        return po_cat_dic

    def setupKBDDicList(self):
        kbd_l_case = dict((k.lower(), v) for k,v in TranslationFinder.KEYBOARD_TRANS_DIC.items())
        TranslationFinder.KEYBOARD_TRANS_DIC.update(kbd_l_case)

    def writeJSONDic(self, dict_list=None, file_name=None):
        try:
            file_path = (self.master_dic_file if (file_name is None) else file_name)
            dic = (self.master_dic_list if (dict_list is None) else dict_list)

            dic = cm.removeLowerCaseDic(dic)

            with open(file_path, 'w', newline='\n', encoding='utf8') as out_file:
                json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
                # out_file.close()

        except Exception as e:
            _("Exception writeDictionary Length of read dictionary:{}".format(len(self.master_dic_list)))
            raise e

    def loadJSONDic(self, file_name=None):
        local_dic = None
        try:
            file_path = (self.json_dic_file if (file_name == None) else file_name)
            with open(file_path) as in_file:
                local_dic = json.load(in_file)
                if local_dic:
                    _("Loaded:{}".format(len(local_dic)))
                else:
                    raise Exception("dic [{}] is EMPTY. Not expected!", file_path)
        except Exception as e:
            _("Exception readDictionary Length of read dictionary:")
            _(e)
            raise e

        #local_dic = self.removeJSONDicNoTranslation(local_dic)
        dic_lower_set=dict((k.lower(),v) for k,v in local_dic.items())
        local_dic.update(dic_lower_set)
        _("after cleaned:{}".format(len(local_dic)))
        return local_dic

    def isInList(self, msg, find_list, is_lower=False):
        trans = None
        try:
            # is_debug = ("Mode" in msg)
            # if is_debug:
            #     print("DEBUG")
            #
            orig_msg = str(msg)
            if is_lower:
                msg = msg.lower()
            trans = find_list[msg]
            return trans
        except Exception as e:
            # if msg:
            #     print(msg)
            # if find_list:
            #     print("dic len={}".format(len(find_list)))
            # print("is_lower:", is_lower)
            #raise e
            return None

    def findTranslation(self, msg):
        trans = None

        orig_msg = str(msg)
        begin_with_punctuations = (cm.BEGIN_PUNCTUAL.search(msg) is not None)
        ending_with_punctuations = (cm.ENDS_PUNCTUAL.search(msg) is not None)
        if begin_with_punctuations:
            msg = cm.BEGIN_PUNCTUAL.sub("", msg)
        if ending_with_punctuations:
            msg = cm.ENDS_PUNCTUAL.sub("", msg)

        list_name = "self.master_dic_list"
        trans = self.isInList(msg, self.master_dic_list)
        if not trans:
            list_name = "self.master_dic_list LOWER"
            trans = self.isInList(msg, self.master_dic_list, is_lower=True)

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
        return trans

    def findTranslationByFragment(self, msg):
        orig_msg = str(msg)
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

        is_ignore = ig.isIgnored(msg)
        if is_ignore:
            return None, must_mark, is_ignore

        trans = self.findTranslation(msg)
        if not trans:
            trans = self.findTranslationByFragment(msg)
            must_mark = True
        return (trans, must_mark, is_ignore)

    def translateKeyboard(self, msg):
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

        return trans

    def removeIgnoredEntries(self, dic_list):
        valid = (dic_list is not None) and (len(dic_list) > 0)
        if not valid:
            return

        # hold keys to be removed
        blank_key=[]
        remove_key=[]
        for k, v in dic_list.items():
            is_ignore = (ig.isIgnored(k))
            if is_ignore:
                print("mark for removal:", k, v)
                remove_key.append(k)


            # remove null from v
            has_value = (v is not None)
            if not has_value:
                print("mark due to blanking value:", k, v)
                blank_key.append(k)

        for k in blank_key:
            print("actually blanking:", k)
            entry={k:""}
            dic_list.update(entry)

        # run through the keys and remove entry from the dic_list
        for k in remove_key:
            print("acutally removing:", k)
            del dic_list[k]



