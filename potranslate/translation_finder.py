import os
import re
from definition import Definitions as df
from common import Common as cm, LocationObserver
from common import dd, pp
from ignore import Ignore as ig
import json
from collections import OrderedDict, defaultdict
from sphinx_intl import catalog as c
from definition import RefType, TranslationState
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

        self.numerical_pat_list = []
        self.initNumericalPatternList()
        self.loadDictionary()
        self.getDict().createSentenceStructureDict()

        self.struct_dict = self.getDict().sentence_struct_dict
        # pp(self.struct_dict)
        # is_in = ('a * b' in self.getDict())
        # dd('')

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
            translation = f'{df.numeric_prefix} {translation} {df.numeric_postfix}'
            is_diff = (stripped_word != msg)
            if is_diff:
                translation = msg.replace(msg, stripped_word)
            dd(f'translateNumerics(): [{stripped_word}] => [{translation}]')
        return translation

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
        self.getDict().local_keys.sort()
        # self.getDict().replaceRefsForDict()
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

        if not translated_dict:
            return None

        is_fully_translated = obs.isCompletelyUsed()
        if not is_fully_translated:
            untran_dict = obs.getUnmarkedPartsAsDict()
            for loc, mm in untran_dict.items():
                txt = mm.txt
                tran_sub_text = self.translateWords(txt)
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
                if not tran_sub_text:
                    tran_sub_text = self.translateNumerics(orig_sub_text)

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
        # # dd(f'blindTranslation() msg:[{msg}]')
        # # new_text, trans, cover_length = self.findByReduction(msg)
        # # is_found_trans = (trans and not trans == msg)
        # # if is_found_trans:
        # #     return trans
        #
        # local_translated_dict, local_untranslated_dic = self.buildLocalTranslationDict(msg)
        #
        # # use the translated (longest first) to replace all combination,
        # # translate by reduction for ones could not, to form the final translation for the variation
        # # translated_dic will be sorted in length by default.
        # # using safe translation length and unsafe translation length to sort so one with both highest values
        # # are floated on top once sorted. Pick the one at the top list, ignore the rest
        # translation = self.replacingUsingDic(local_translated_dict, local_untranslated_dic, msg)
        # return translation

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
        # new_msg = str(msg)
        # new_msg = df.HEADING_WITH_PUNCT_MULTI.sub('', new_msg)
        # new_msg = df.TRAILING_WITH_PUNCT_MULTI.sub('', new_msg)
        return new_msg

    def cleanBothEntries(self, msg, tran):
        new_msg = cm.removeLeadingTrailingSymbs(msg)
        new_tran = cm.removeLeadingTrailingSymbs(tran)
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
        kbd_l_case = dict((k.lower(), v) for k, v in df.KEYBOARD_TRANS_DIC.items())
        df.KEYBOARD_TRANS_DIC.update(kbd_l_case)

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
            df.LOG(f'{e}; Length of read dictionary:{len(dic)}', error=True)
            raise e

    def loadJSONDic(self, file_name=None):
        def sentStructKeyFunction(item):
            pat: re.Pattern = None
            value: tuple = None
            (pat, value) = item
            key = pat.pattern
            return key

        return_dic = None
        sent_struct_original_set = {}
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

            # temp_set = [(x, y) for (x, y) in dic.items() if df.SENT_STRUCT_START_SYMB in x]
            # sent_struct_original_set = OrderedDict(temp_set)
            #
            return_dic = NoCaseDict(dic)
            # return_dic.sentence_struct_dict = sent_struct_original_set
        except Exception as e:
            df.LOG(f'{e}; Exception occurs while performing loadJSONDic({file_path})', error=True)
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
        # is_ignore = ig.isIgnored(msg)
        # if is_ignore:
        #     return None

        left, mid, right = cm.getTextWithin(msg)
        is_quoted = (left and right) and ((left == right) or right.startswith(left))
        if is_quoted:
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
            left, mid, right = cm.getTextWithin(msg)
            is_quoted = (left and right) and (left == right)
            if is_quoted:
                return None
            else:
                msg = mid

            is_found = (msg in search_dict)
            if is_found:
                tran = search_dict[msg]
            else:
                tran = self.translateNumerics(msg)

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
            trans = cm.removeTheWord(trans)
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
        fname = INP.currentframe().f_code.co_name

        trans = None
        old_msg = str(msg)
        try:
            dd(f'{fname}() calling findTranslation [{msg}]')
            is_fuzzy = False
            trans, is_fuzzy, is_ignore = self.findTranslation(msg)
            if is_ignore:
                trans = None

            if not trans:
                dd(f'{fname}() calling tryFuzzyTranlation [{msg}]')
                trans, cover_length, matching_ratio = self.tryFuzzyTranlation(msg, )
                is_fuzzy = bool(trans)

            if not trans:
                dd(f'{fname}() calling SimpleBlindTranslation [{msg}]')
                trans = self.simpleBlindTranslation(msg)
                is_fuzzy = True

            if trans:
                dd(f'{fname}() calling removeTheWord [{trans}]')
                trans = cm.removeTheWord(trans)
                trans = cm.matchCase(msg, trans)
            return (trans, is_fuzzy, is_ignore)
        except Exception as e:
            df.LOG(f'{e}; msg:[{msg}], trans:[{trans}]', error=True)
            raise e

    def translateKeyboard(self, mm: MatcherRecord):
        msg = mm.getSubText()
        orig = str(msg)
        trans = str(msg)
        result_dict = cm.patternMatchAll(df.KEYBOARD_SEP, msg)
        for sub_loc, sub_mm in result_dict.items():
            txt = sub_mm.txt
            has_dic = (txt in self.kbd_dict)
            if not has_dic:
                continue

            tr = self.kbd_dict[txt]
            if tr:
                trans = cm.jointText(trans, tr, sub_loc)

        is_fuzzy = False
        is_ignore = False
        is_the_same = (orig == trans)
        if is_the_same:
            trans = None
            is_fuzzy = True
        main_txt = mm.getMainText()
        trans = cm.jointText(main_txt, trans, mm.getSubLoc())
        mm.setTranlation(trans, is_fuzzy, is_ignore)
        return True

    def checkIgnore(self, msg):
        is_pure_path = (df.PURE_PATH.search(msg) is not None)
        is_pure_ref = (df.PURE_REF.search(msg) is not None)
        is_api_ref = (df.API_REF.search(msg) is not None)
        is_keep = (ig.isKeep(msg))
        is_keep_contain = (ig.isKeepContains(msg))
        is_ignore = (is_pure_path or is_pure_ref or is_api_ref) and (not (is_keep or is_keep_contain))
        return is_ignore

    def translateQuoted(self, mm: MatcherRecord):
        def formatTran(current_untran, current_tran):
            starter = ("" if is_blank_quote else mm.getStarter())
            ender = ("" if is_blank_quote else mm.getEnder())

            explanation_part = f'({starter}{current_untran}{ender})'
            abbrev_part = f'{starter}{current_tran}{ender}'
            body = f'{abbrev_part} {explanation_part}'
            tran = f':abbr:`{body}`'
            return tran

        msg = mm.getSubText()
        is_blank_quote = (mm.type == RefType.BLANK_QUOTE)
        # is_fuzzy = False
        # is_ignore = self.checkIgnore(msg)
        # if is_ignore:
        #     return False

        tran, is_fuzzy, is_ignore = self.translate(msg)
        if is_ignore:
            return

        if not tran:
            tran = ""

        tran = self.removeAbbrevInTran(tran)
        tran = cm.removeOriginal(msg, tran)
        tran = formatTran(msg, tran)
        mm.setTranlation(tran, is_fuzzy, is_ignore)
        return True

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

    def translateRefWithLink(self, mm: MatcherRecord):
        def formatTran(current_untran, current_tran):
            ref_type: RefType = mm.type
            has_ref = bool(ref_type)
            has_valid_ref_type = (has_ref and isinstance(ref_type, RefType))
            is_text_type = (has_valid_ref_type and ref_type == RefType.TEXT)
            is_bracket_or_quote = (has_valid_ref_type and (df.BRACKET_OR_QUOTE_REF.search(ref_type.name) is not None))
            is_ignore_type = (is_text_type or is_bracket_or_quote)
            is_formatting = (not is_ignore_type)
            if not is_formatting:
                return current_tran

            new_tran = f'{current_tran} ({current_untran})'
            return new_tran

        formatted_tran = None
        is_fuzzy = is_ignore = False
        tran = None
        is_using_main = False
        msg = mm.getSubText()
        has_sub_text = bool(msg)
        if not has_sub_text:
            is_using_main = True
            msg = mm.getMainText()

        has_ref_link = (df.REF_LINK.search(msg) is not None)
        if not has_ref_link:
            tran, is_fuzzy, is_ignore = self.translate(msg)
            mm.setTranlation(tran, is_fuzzy, is_ignore)
        else:
            found_dict = cm.findInvert(df.REF_LINK, msg, is_reversed=True)
            for sub_loc, sub_mm in found_dict.items():
                sub_txt = sub_mm.getMainText()
                sub_tran, is_fuzzy, is_ignore = self.translate(sub_txt)
                sub_tran_formatted = formatTran(sub_txt, sub_tran)
                formatted_tran = cm.jointText(msg, sub_tran_formatted, sub_loc)
                tran = formatted_tran
                break
        if tran:
            main_txt = mm.getMainText()
            if is_using_main:
                sub_loc = mm.getMainLoc()
            else:
                sub_loc = mm.getSubLoc()
            if not formatted_tran:
                formatted_tran = formatTran(msg, tran)
            main_tran = cm.jointText(main_txt, formatted_tran, sub_loc)
            mm.setTranlation(main_tran, is_fuzzy, is_ignore)
        return bool(tran)

    def translateMenuSelection(self, mm: MatcherRecord):
        def formatAbbrevTran(current_untran, current_tran):
            has_abbr = cm.hasAbbr(current_tran)
            if has_abbr:
                abbr_orig, abbr_marker, abbr_exp = cm.extractAbbr(current_tran)
                return_tran = cm.removeOriginal(current_untran, abbr_exp)
                return return_tran
            else:
                return current_tran

        def translateMenuItem(loc_word_list):
            for loc, mnu_item_mm in loc_word_list.items():
                sub_txt: str = mnu_item_mm.txt

                left, mid, right = cm.getTextWithin(sub_txt)
                tran, is_fuzzy, is_ignore = self.translate(mid)

                has_left_right = (bool(left) or bool(right))
                valid_tran = (bool(tran) is not is_ignore)
                must_combine = (valid_tran and has_left_right)
                if must_combine:
                    tran = left + tran + right

                if is_ignore:
                    continue

                tran = formatAbbrevTran(sub_txt, tran)

                is_tran_valid = (tran and (tran != sub_txt))
                if is_tran_valid:
                    is_sub_text_bracketed = sub_txt.startswith('(') and sub_txt.endswith(')')
                    if is_sub_text_bracketed:
                        tran_txt = f"{tran} {sub_txt}"
                    else:
                        tran_txt = f"{tran} ({sub_txt})"
                else:
                    tran_txt = f"({sub_txt})"

                mnu_item_mm.setTranlation(tran_txt, is_fuzzy, is_ignore)

        msg = mm.getSubText()

        word_list = cm.findInvert(df.MENU_SEP, msg, is_reversed=True)
        translateMenuItem(word_list)

        mm_main_txt = mm.getMainText()
        trans = str(mm_main_txt)
        tran_state_list=[]
        for loc, mnu_item_mm in word_list.items():
            trans = cm.jointText(trans, mnu_item_mm.tl_txt, loc)
            tran_state_list.append(mnu_item_mm.translation_state)

        temp_tran_txt = mm.getSubText()
        word_list = list(word_list.items())
        for loc, mnu_item_mm in word_list:
            tran_txt = mnu_item_mm.tl_txt
            temp_tran_txt = cm.jointText(temp_tran_txt, tran_txt, loc)

        main_tran = mm.txt
        sub_loc = mm.getSubLoc()
        final_tran = cm.jointText(main_tran, temp_tran_txt, sub_loc)

        is_fuzzy = (TranslationState.FUZZY in tran_state_list)
        is_ignore = (TranslationState.IGNORED in tran_state_list)

        actual_ignore = ((not is_fuzzy) and is_ignore)
        mm.setTranlation(final_tran, is_fuzzy, actual_ignore)
        return True

    def removeAbbrevInTran(self, current_tran):
        if not current_tran:
            return None

        abbrev_mm = cm.patternMatch(df.ABBREV_PATTERN_PARSER, current_tran)
        if not abbrev_mm:
            return current_tran

        new_tran = str(current_tran)
        (abbr_loc, abbr_txt) = abbrev_mm.getSubEntryByIndex(0)
        abbrev_orig_rec, abbrev_part, exp_part = cm.extractAbbr(abbr_txt)
        new_tran = f'{abbrev_part} {exp_part}'
        # new_tran = cm.jointText(new_tran, exp_part, abbr_loc)
        return new_tran

    def translateAbbrev(self, mm: MatcherRecord) -> list:
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

        msg = mm.getSubText()
        tran_txt = str(msg)
        first_match_mm: MatcherRecord = None
        all_matches = cm.patternMatchAll(df.ABBR_TEXT, msg)
        if not all_matches:
            return False

        all_matches_list = list(all_matches.items())
        first_match = all_matches_list[0]
        first_match_loc, first_match_mm = first_match

        abbrev_loc, abbrev_explain_txt = first_match_mm.getSubEntryByIndex(1)
        tran, is_fuzzy, is_ignore = self.translate(abbrev_explain_txt)

        tran = self.removeAbbrevInTran(tran)
        valid = (tran and (tran != abbrev_explain_txt))
        if valid:
            translation = f"{abbrev_explain_txt}: {tran}"
        else:
            translation = f"{abbrev_explain_txt}: "

        tran_txt = cm.jointText(msg, translation, abbrev_loc)
        main_txt = mm.getMainText()
        sub_loc = mm.getSubLoc()
        final_tran = cm.jointText(main_txt, tran_txt, sub_loc)
        mm.setTranlation(final_tran, is_fuzzy, is_ignore)
        return True

    def translateOSLAttrrib(self, msg: str):
        if not msg:
            return None, False, False

        tran_txt = str(msg)
        is_fuzzy_list=[]
        is_ignore_list=[]
        word_list_dict = cm.findInvert(df.COLON_CHAR, tran_txt, is_reversed=True)
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
