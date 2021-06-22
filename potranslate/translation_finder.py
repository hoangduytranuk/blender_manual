import os
import re
import time

from definition import Definitions as df
from common import Common as cm, LocationObserver
from common import dd, pp
from ignore import Ignore as ig
from collections import OrderedDict, defaultdict
from sphinx_intl import catalog as c
import operator as OP
from nocasedict import NoCaseDict
from matcher import MatcherRecord
import inspect as INP

class TranslationEntry():
    def __init__(self, untran_txt=None, tran_txt=None, txt_loc=None, fuzzy_rate=None):
        self.untran_txt = untran_txt
        self.tran_txt = tran_txt
        self.loc = txt_loc
        self.fuzzy_rate = fuzzy_rate

class TranslationFinder:
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


        self.loadDictionary()


        st_time = time.perf_counter()
        self.getDict().createSentenceStructureDict()
        ed_time = time.perf_counter()
        p_time = (ed_time - st_time)
        self.struct_dict = self.getDict().sentence_struct_dict
        # pp(self.struct_dict)
        # is_in = ('a * b' in self.getDict())
        # dd('')

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
        self.kbd_dict = NoCaseDict(df.KEYBOARD_TRANS_DIC_PURE)

    def flatPOFile(self, file_path):
        data_cat = c.load_po(file_path)
        c.dump_po(file_path, data_cat)

    def translateBreakupSentences(self, msg):
        if not msg:
            return msg

        count_untranslated = 0
        count_translated = 0
        translation = str(msg)
        result_list = OrderedDict()
        text_list = cm.patternMatchAll(df.COMMON_SENTENCE_BREAKS, msg)
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
            for remain_loc, un_tran_mm in untran_dict.items():
                un_tran_txt = un_tran_mm.txt
                is_ignore = ig.isIgnored(un_tran_txt)
                if is_ignore:
                    print(f'replacingUsingDic: IGNORING: un_tran_txt:[{un_tran_txt}]')
                    continue

                try:
                    # cm.debugging(un_tran_txt)
                    _, tran_sub_text, covered_length = self.tryToFindTranslation(un_tran_txt)
                except Exception as e:
                    df.LOG(f'{e} un_tran_txt:[{un_tran_txt}]', error=True)
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
                df.LOG(f'{e}', error=True)
                raise e

        local_dict_list.sort(key=OP.itemgetter(0), reverse=True)    # sort by matching ratio
        local_dict_list.sort(key=OP.itemgetter(2), reverse=True)    # sort by location
        local_dict = OrderedDict([(loc, (un_tran_txt, tran)) for matching_ratio, cover_length, loc, un_tran_txt, tran in local_dict_list])

        # replacing dict into text and finish
        temp_translation = self.translatedListToText(local_dict, translation)
        has_translation = not (temp_translation == text)
        if not has_translation:
            dd(f'replacingUsingDic(): text:[{text}]')
            return None
        else:
            dd(f'replacingUsingDic(): text:[{text}]')
            dd(f'temp_translation:[{temp_translation}]')
            return temp_translation

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
            is_translated = observer.isLocUsed(loc)
            if is_translated:
                continue

            orig_txt, loc_tran_txt = v
            s, e = loc
            loc_left = current_translation[:s]
            loc_right = current_translation[e:]
            current_translation = loc_left + loc_tran_txt + loc_right

            observer.markLocAsUsed(loc)
            is_fully_translated = observer.isCompletelyUsed()
            if is_fully_translated:
                break

        dd(f'translatedListToText: original [{orig}]')
        dd(f'translatedListToText: translated [{current_translation}]')
        return current_translation

    def simpleBlindTranslation(self, msg):
        translated_dict = OrderedDict()
        map = cm.genmap(msg)
        obs = LocationObserver(str(msg))
        dic = self.getDict()
        for loc, txt in map:
            is_fully_translated = obs.isCompletelyUsed()
            if is_fully_translated:
                break

            is_used = obs.isLocUsed(loc)
            if is_used:
                continue

            orig_txt = obs.getTextAtLoc(loc)

            tran_sub_text, fuzzy_len, matching_ratio = self.tryFuzzyTranlation(orig_txt)
            if tran_sub_text:
                obs.markLocAsUsed(loc)
                entry = {loc: (txt, tran_sub_text)}
                translated_dict.update(entry)

        is_fully_translated = obs.isCompletelyUsed()
        if not is_fully_translated:
            untran_dict = obs.getUnmarkedPartsAsDict()
            for loc, mm in untran_dict.items():
                txt = mm.txt
                tran_sub_text = dic.translateBySlittingSymbols(txt)
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
            has_abbrev = (df.ABBREV_PATTERN_PARSER.search(tran_sub_text) is not None)
        if untran_word_dic and not has_abbrev:
            untran_word_list = list(untran_word_dic.items())
            untran_word_list.sort(reverse=True)
            for loc, un_tran_mm in untran_word_list:
                un_tran_word = un_tran_mm.txt
                tran_word_text, fuzzy_word_text, search_dict, matching_word_ratio, untran_sub_word_dic = self.isInDictFuzzy(un_tran_word)
                if tran_word_text:
                    tran_sub_text = tran_sub_text.lower().replace(un_tran_word, tran_word_text)

        fuzzy_len = (len(fuzzy_text) if fuzzy_text else 0)
        fname = INP.currentframe().f_code.co_name
        if tran_sub_text:
            tran_sub_text = self.getDict().replaceTranRef(tran_sub_text)
            search_dict.addCache(msg, tran_sub_text)
            dd(f'{fname}() msg:[{msg}] tran_sub_text:[{tran_sub_text}] [{matching_ratio}]')
            return tran_sub_text, fuzzy_len, matching_ratio
        else:
            search_dict.addCache(msg, False)
            dd(f'{fname}() UNABLE TO FIND msg:[{msg}]')
            return None, fuzzy_len, 0

    def fillBlank(self, ss, ee, blanker):
        blank_len = (ee - ss)
        blank_str = (df.FILLER_CHAR * blank_len)
        blank_left = blanker[:ss]
        blank_right = blanker[ee:]
        blanker = blank_left + blank_str + blank_right
        return blanker

    def buildLocalTranslationDict(self, msg):

        local_translated_dict = [] # for quick, local translation
        loc_map = cm.genmap(msg)
        observer = LocationObserver(msg)

        for loc, orig_sub_text in loc_map:
            is_translated = observer.isLocUsed(loc)
            if is_translated:
                continue

            is_ignore = ig.isIgnored(orig_sub_text)
            if is_ignore:
                observer.markLocAsUsed(loc)
                is_fully_translated = observer.isCompletelyUsed()
                if is_fully_translated:
                    break
                else:
                    continue

            tran_sub_text = self.isInDict(orig_sub_text)
            if not tran_sub_text:
                tran_sub_text, cover_length, matching_ratio = self.tryFuzzyTranlation(orig_sub_text)

            if tran_sub_text:
                matching_ratio = 100
                cover_length = len(orig_sub_text)
                local_dict_entry = (matching_ratio, cover_length, loc, orig_sub_text, tran_sub_text)
                local_translated_dict.append(local_dict_entry)

                observer.markLocAsUsed(loc)
                is_fully_translated = observer.isCompletelyUsed()
                if is_fully_translated:
                    break

        untran_dict = observer.getUnmarkedPartsAsDict()
        local_translated_dict.sort(key=OP.itemgetter(2, 0, 1), reverse=True)
        return local_translated_dict, untran_dict

    def blindTranslation(self, msg):
        tran = self.getDict().blindTranslate(msg)
        return tran

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
                    df.LOG(f'{e}', error=True)
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
        else:
            raise ValueError(error_msg)

    def getHeadAndTailPuncts(self, msg):
        if not msg:
            return '', ''

        msg_head = msg_trail = None

        msg_trail = df.TRAILING_WITH_PUNCT_MULTI.search(msg)
        if msg_trail:
            msg_trail = msg_trail.group(0)
        else:
            msg_trail = ''

        msg_head = df.HEADING_WITH_PUNCT_MULTI.search(msg)
        if msg_head:
            msg_head = msg_head.group(0)
        else:
            msg_head = ''

        return msg_head, msg_trail

    def cleanOneEntry(self, msg):
        if not msg:
            return msg

        new_msg = cm.removeLeadingTrailingSymbs(msg)
        return new_msg

    def cleanBothEntries(self, msg, tran):
        new_msg = cm.removeLeadingTrailingSymbs(msg)
        new_tran = cm.removeLeadingTrailingSymbs(tran)
        return new_msg, new_tran

    def addEntryToChosenDict(self, msg, tran, dicfile_path, dict_list, indicator=''):
        tran = cm.cleanSlashesQuote(tran)
        msg = cm.cleanSlashesQuote(msg)

        # has_tran = (tran is not None)
        # if has_tran:
        #     tran = cm.removeOriginal(msg, tran)
        #     msg, tran = self.cleanBothEntries(msg, tran)
        # else:
        #     msg = self.cleanOneEntry(msg)
        #     tran = ""
        #
        # is_in = (msg in dict_list)
        # if not is_in:
        #     msg, tran = self.cleanBothEntries(msg, tran)
        #     is_in = (msg in dict_list)
        #
        # if is_in:
        #     current_tran = dict_list[msg]
        #     is_diff = (current_tran != tran)
        #     if is_diff:
        #         del dict_list[msg]
        #     else:
        #         return

        if not tran:
            tran = ""
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
        cm.writeJSONDic(dict_list=dic_list, file_name=dic_file)

    def writeBackupDict(self):
        dict_stat = self.writeDict(self.master_dic_backup_file, self.backup_dic, indicator='BACKUP')

    def writeMasterDict(self):
        dict_stat = self.writeDict(self.master_dic_file, self.master_dic, indicator='MASTER')

    def getKeyboardOriginal(self, text):
        # kbd_def_val = list(KEYBOARD_TRANS_DIC.values())
        orig_txt = str(text)
        for k, kbd_val in df.KEYBOARD_TRANS_DIC_PURE.items():
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
        file_path = (self.master_dic_file if is_master else self.master_dic_backup_file)
        df.LOG(f'reloadChosenDict:{file_path}')

        dic = cm.loadJSONDic(file_name=file_path)

        # st_time = time.perf_counter()
        ncase_dic = NoCaseDict(dic)
        # ed_time = time.perf_counter()
        # p_time = (ed_time - st_time)
        ncase_dic.local_keys.sort()
        if is_master:
            self.master_dic = ncase_dic
        else:
            self.backup_dic = ncase_dic

    def saveMasterDict(self, to_file=None):
        file_path = (to_file if to_file else self.master_dic_file)
        cm.writeJSONDic(dict_list=self.master_dic, file_name=file_path)

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
        kbd_l_case = dict((k.lower(), v) for k, v in df.KEYBOARD_TRANS_DIC.items())
        df.KEYBOARD_TRANS_DIC.update(kbd_l_case)

    def getDict(self, local_dict=None):
        search_dict = (local_dict if local_dict else self.master_dic)
        if not search_dict:
            msg = 'isInDict() NO Dictionary is available. Stopped'
            print(msg)
            raise Exception(msg)
        return search_dict

    def isInDictFuzzy(self, msg, dic_to_use=None):
        fname = INP.currentframe().f_code.co_name

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
            dd(msg)
            raise Exception(msg)

        is_matcher = isinstance(msg, MatcherRecord)
        if is_matcher:
            dd('debug')
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
            if not tran:
                tran = search_dict.blindTranslate(msg)

        if tran:
            # tran = search_dict.replaceTranRef(tran)
            tran = cm.matchCase(msg, tran)
            # cm.debugging(msg)
            dd(f'{fname}() [{msg}] => [{tran}]')
        else:
            dd(f'{fname}() Unable to find translation for: [{msg}]')
            tran = None
        return tran, matched_text, search_dict, matching_ratio, untran_word_dic


    def isInDict(self, msg, dic_to_use=None):
        tran = None

        is_ref = cm.isRef(msg)
        if is_ref:
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
            left, mid, right = cm.getTextWithin(msg)
            is_found = (mid in search_dict)
            if is_found:
                tran = search_dict[mid]

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

    def tryToFindTranslation(self, txt: str) -> str:
        cover_length = 0
        separator_list = [
            df.SPACES,
            df.SYMBOLS,
        ]
        selective_list = []

        input_txt = str(txt)

        new_text, trans, cover_length = self.findByReduction(txt)
        is_found_trans = (trans and not trans == txt)
        if is_found_trans:
            return txt, trans, cover_length

        for separator in separator_list:
            temp_masking_text = str(txt)
            found_dict = cm.findInvert(separator, txt, is_reversed=True)
            if not found_dict:
                continue

            translated_dict = {}
            translation = str(txt)
            for loc, mm in found_dict.items():
                orig_txt = mm.txt
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
            translation = None
            cover_length = 0
        else:
            sorted_selective_list = list(sorted(selective_list, reverse=True))
            chosen_entry = sorted_selective_list[0]
            cover_length, txt, translation = chosen_entry

        return txt, translation, cover_length

    def isNonGATranslatedFully(self, msg, trans):
        is_ga = (df.GA_PATTERN_PARSER.search(msg) is not None)
        if is_ga:
            return True

        is_ga = (df.GA_PATTERN_PARSER.search(trans) is not None)
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
        else:
            trans = None
        if trans is None:
            dd(f"NOT found: [{msg}]")
        return trans, is_fuzzy, is_ignore

    def findTranslationByFragment(self, msg):
        # orig_msg = str(msg)
        trans_list = []
        trans = str(msg)

        word_list = df.WORD_ONLY_FIND.findall(msg)

        dd(f'word_list: {word_list}')
        result_dict = cm.patternMatchAll(df.WORD_ONLY_FIND, msg)
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

    def translate(self, msg):
        trans = None
        old_msg = str(msg)
        try:
            df.LOG(f'calling findTranslation [{msg}]')
            is_fuzzy = False
            trans, is_fuzzy, is_ignore = self.findTranslation(msg)
            if is_ignore:
                return (None, False, True)

            is_single_char = (len(msg) < 2)
            if is_single_char:
                return (None, False, True)

            # if not trans:
            #     self.addBackupDictEntry(msg, None)

            if not trans:
                df.LOG(f'calling tryFuzzyTranlation [{msg}]')
                trans, cover_length, matching_ratio = self.tryFuzzyTranlation(msg, )
                is_fuzzy = bool(trans)

            # if not trans:
            #     df.LOG(f'calling SimpleBlindTranslation [{msg}]')
            #     trans = self.simpleBlindTranslation(msg)
            #     is_fuzzy = True

            return (trans, is_fuzzy, is_ignore)
        except Exception as e:
            df.LOG(f'{e}; msg:[{msg}], trans:[{trans}]', error=True)
            return (None, False, True)

    def checkIgnore(self, msg):
        is_pure_path = (df.PURE_PATH.search(msg) is not None)
        is_pure_ref = (df.PURE_REF.search(msg) is not None)
        is_api_ref = (df.API_REF.search(msg) is not None)
        is_keep = (ig.isKeep(msg))
        is_keep_contain = (ig.isKeepContains(msg))
        is_ignore = (is_pure_path or is_pure_ref or is_api_ref) and (not (is_keep or is_keep_contain))
        return is_ignore

    def recomposeAbbrevTranslation(self, msg, tran):
        has_tran = (tran and not tran is None)
        if not has_tran:
            return tran

        has_abbr = (df.ABBREV_CONTENT_PARSER.search(tran) is not None)
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
