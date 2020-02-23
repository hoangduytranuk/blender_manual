# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/htran/.local/lib/python3.6/site-packages')
sys.path.append('/home/htran/bin/python/PO')
sys.path.append('/home/htran/bin/python/base')
sys.path.append('/home/htran/bin/python/algorithm')
sys.path.append('/home/htran/bin/python/event')
# sys.path.append('/usr/lib/python36.zip')
# sys.path.append('/usr/lib/python3.6)
# sys.path.append('/usr/lib/python3.6/lib-dynload')
# sys.path.append('/usr/local/lib/python3.6/dist-packages')
# sys.path.append('/usr/lib/python3/dist-packages')
# sys.path.append('/usr/lib/python3.6/dist-packages')

import os
import io
import re
import json
import copy as cp
from common import Common as cm
from common import pp, DEBUG, _
from pobase import POBasic
import docutils
from docutils import nodes
from sphinx import addnodes, roles
from six import text_type
from sphinx.util.nodes import extract_messages, traverse_translatable_index
    # , extract_node
from distutils import log as logger
from sphinx_intl import catalog as c
from babel.messages import pofile
from babel.messages.catalog import Message, Catalog
from googletrans import Translator as GTR
from collections import defaultdict

#from Levenshtein import distance as DS
from markupsafe import Markup
try:
    import html
except ImportError:
    html = None

debug_max_file_count = 5
debug_current_file_count = 0

unescape = getattr(html, 'unescape', None)
if unescape is None:
    # HTMLParser.unescape is deprecated since Python 3.4, and will be removed
    # from 3.9.
    unescape = html_parser.HTMLParser().unescape


# sudo apt install python-pip python3-pip
# pip3 install googletrans
from googletrans import Translator

use_google_translate = False

# type: <class 'docutils.nodes.caption'>
# type: <class 'docutils.nodes.emphasis'>
# type: <class 'docutils.nodes.field_name'>
# type: <class 'docutils.nodes.image'>
# type: <class 'docutils.nodes.inline'>
# type: <class 'docutils.nodes.line'>
# type: <class 'docutils.nodes.literal'>
# type: <class 'docutils.nodes.math'>
# type: <class 'docutils.nodes.math_block'>
# type: <class 'docutils.nodes.paragraph'>
# type: <class 'docutils.nodes.reference'>
# type: <class 'docutils.nodes.rubric'>
# type: <class 'docutils.nodes.strong'>
# type: <class 'docutils.nodes.superscript'>
# type: <class 'docutils.nodes.term'>
# type: <class 'docutils.nodes.Text'>
# type: <class 'docutils.nodes.title'>

def isIgnored(msg):
    is_ignore_word = cm.isIgnoredWord(msg)
    is_dos_command = cm.isDosCommand(msg)
    is_ignore_start = cm.isIgnoredIfStartsWith(msg)
    is_ignore_path = cm.isFilePath(msg)

    is_ignore = (is_ignore_word or is_dos_command or is_ignore_start or is_ignore_path)
    #is_ignore = (is_ignore_word or is_dos_command or is_ignore_start)
    if is_ignore:
        # _("checking for ignore")
        dict_ignore = {"is_ignore_word": is_ignore_word,
                       "is_dos_command": is_dos_command,
                       "is_ignore_start": is_ignore_start,
                       "is_ignore_path": is_ignore_path
                       }
        pp(dict_ignore)
        for k, v in dict_ignore.items():
            if isinstance(v, bool) and (v == True):
                _(msg, ":", k)
    return is_ignore


class TranslationFinder:

    def __init__(self):
        self.update_dic = 0
        self.update_po_file = None
        self.master_dic_file = "/home/htran/po_dictionary_sorted_translated_0001_nodot.json"
        self.master_dic_backup_file = "/home/htran/po_dictionary_sorted_translated_0002.json"
        self.master_dic_backup_list = {}

        self.master_dic_list = self.loadJSONDic(file_name=self.master_dic_file)
        self.master_dic_list_updated = False

        self.vipo_dic_path = "/home/htran/blender_documentations/new_po/vi.po"
        self.vipo_dic_list = None # not used

        self.current_po_dir = "/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
        self.json_dic_file = "/home/htran/Documents/menuselection_new_dictionary_sorted_translated_0028.json"

        #self.json_dic_list = self.loadJSONDic(file_name=self.json_dic_file)
        self.json_dic_list = {}
        self.current_po_path = None
        self.current_po_cat = None
        self.ref_dic_list = {}
        self.ref_dic_file = "/home/htran/ref_dic_0002.json"

        self.setupKBDDicList()

        self.dic_list=defaultdict(int) # for general purposes


    def updateMasterBackup(self, msg, tran):
        entry={msg:tran}
        self.master_dic_backup_list.update(entry)

    def updateRefDic(self, msg, tran):
        entry={msg:tran}
        self.ref_dic_list.update(entry)

    def saveMasterBackup(self):
        has_record = (len(self.master_dic_backup_list) > 0)
        if has_record:
            dic_cat = c.load_po(self.vipo_dic_path)
            dic_list = self.poToDic(dic_cat)
            self.master_dic_backup_list.update(dic_list)
            self.writeJSONDic(dict_list=self.master_dic_backup_list, file_name=self.master_dic_backup_file)

    def saveRefDic(self):
        has_record = (len(self.ref_dic_list) > 0)
        if has_record:
            self.writeJSONDic(dict_list=self.ref_dic_list, file_name=self.ref_dic_file)

    def setupKBDDicList(self):
        kbd_l_case = dict((k.lower(), v) for k,v in cm.KEYBOARD_TRANS_DIC.items())
        cm.KEYBOARD_TRANS_DIC.update(kbd_l_case)

    def takeTheOldDefIn(self):
        p = re.compile(r'#(\d+)#')
        old_def_file="/home/htran/po_dictionary_sorted_translated_0001_old.json"
        old_def_list = self.loadJSONDic(file_name=old_def_file)

        update_list={}
        for k,v in self.master_dic_list.items():
            is_repeated = (not p.search(v) is None)
            is_in_old_def = (is_repeated and k in old_def_list)
            if is_in_old_def:
                old_v = old_def_list[k]
                is_old_repeated = (not p.search(old_v) is None)
                if not is_old_repeated:
                    entry = {k:old_v}
                    update_list.update(entry)
        can_update = (len(update_list) > 0)
        if can_update:
            self.master_dic_list.update(update_list)
            self.writeJSONDic(dict_list=self.master_dic_list, file_name=self.master_dic_backup_file)

    def calcEntries(self, file_name):
        dic_cat = c.load_po(file_name)
        for index, m in enumerate(dic_cat):
            is_first_line = (index == 0)
            if is_first_line:
                continue
            k = m.id
            v = m.string
            is_fuzzy = m.fuzzy

            # is_translated = (v is not None) and (len(v) > 0) and (not is_fuzzy)
            # if not is_translated:
            #     continue

            self.dic_list[k] += 1

    def removeUnusedEntriesFromMasterDict(self):
        po_cat = c.load_po(self.vipo_dic_path)
        po_dic_list = self.poToDic(po_cat)

        removed_dic_file="/home/htran/removed_dict.json"
        remove_count=0
        new_dic = {}
        removed_dic_list={}
        for k,v in self.master_dic_list.items():
            entry = {k: v}
            is_currently_used = (k in self.dic_list) or (k in po_dic_list)
            if is_currently_used:
                new_dic.update(entry)
            else:
                remove_count += 1
                removed_dic_list.update(entry)

        is_updated = (remove_count > 0)
        if is_updated:
            self.writeJSONDic(dict_list=new_dic, file_name=self.master_dic_backup_file)
            print("New file written to:", self.master_dic_backup_file)
            print("Removed entries written to:", removed_dic_file)
            self.writeJSONDic(dict_list=removed_dic_list, file_name=removed_dic_file)
            remove_count = len(removed_dic_list)
            print("Remove unused count:", remove_count)

    def calcDuplication(self, file_name):

        dic_cat = c.load_po(file_name)
        for index, m in enumerate(dic_cat):
            is_first_line = (index == 0)
            if is_first_line:
                continue
            k = m.id
            v = m.string
            is_fuzzy = m.fuzzy
            is_translated = (v is not None) and (len(v) > 0) and (not is_fuzzy) or (self.findTranslation(k) is not None)
            if is_translated:
                continue

            self.dic_list[k] += 1
            # is_in = (k in self.dic_list)
            # if not is_in:
            #     self.dic_list.update({k:1})
            # else:
            #     current_count = self.dic_list[k]
            #     self.dic_list.update({k: current_count + 1})

    # def mark and store translated (after correctd all entries in master dict)
    # remove entries no longer exists in text

    def translateAsReport(self, sorted_list):
        p=re.compile(r'#(\d+)#')
        save_sorted_dic = []
        for k, v in sorted_list:
            # current_trans = str(k)
            current_trans = self.findTranslation(k)
            has_link = False
            if current_trans:
                tran_links = cm.findListOfLinks(current_trans)
                has_link = (not cm.isPatternMatchListEmpty(tran_links))

            micro_translate_required = (current_trans is None) or (has_link)
            if micro_translate_required:
                current_trans, msg_links, tran_links, unconnected_entries = cm.translateMsg(k, current_trans)

            txt = (current_trans if current_trans is not None else k)
            is_repeated = (v > 1)

            txt = p.sub("", txt) # remove any previous #\d+# in txt
            txt_v = ("" if not is_repeated else "#{}#".format(v))
            entry = (k, txt, v)
            save_sorted_dic.append(entry)
            # if is_repeated:
            #     self.master_dic_list.update(entry)
            #     self.master_dic_list_updated = True
            # else:
            #     save_sorted_dic.update(entry)
        return save_sorted_dic

    def translateAndSaveEntriesFromPOFiles(self):
        has_data = (len(self.dic_list) > 0)
        if not has_data:
            return

        save_sorted_dic = self.translateAsReport(self.dic_list.items())
        sort_list = sorted(save_sorted_dic, key=lambda x: x[2])
        # for index, e in enumerate(sort_list):
        #     print(e)

        #save_sorted_dic = self.translateAsReport(sort_list)
        # for index, e in enumerate(save_sorted_dic.items()):
        #     print(e)

        # pp(save_sorted_dic)
        temp_file="/home/htran/temp.json"
        #self.writeJSONDic(dict_list=save_sorted_dic, file_name=self.json_dic_file)
        self.writeJSONDic(dict_list=sort_list, file_name=temp_file)
        #
        # if self.master_dic_list_updated:
        #     # for k, v in self.master_dic_list.items():
        #     #     is_the_same = (k == v)
        #     #     if is_the_same:
        #     #         v = "{}##".format(v)
        #     #     entry={k:v}
        #     #     self.master_dic_list.update(entry)
        #     self.writeJSONDic(dict_list=self.master_dic_list, file_name=self.master_dic_backup_file)

    def mergeTempWithJSONDic(self):
        temp_file = "/home/htran/temp.json"
        temp_dic = self.loadJSONDic(file_name=temp_file)
        json_dic = self.loadJSONDic(file_name=self.json_dic_file)

        rep_pat = re.compile(r'#(\d+)#')
        for k, v in json_dic.items():
            orig_v = rep_pat.sub("", v)
            is_not_tran = cm.isNotTranslated(k, orig_v)
            if is_not_tran:
                continue
            entry={k:v}
            print(entry)
            temp_dic.update(entry)
        self.update_master_dic(op="rm_lcase_master")
        #self.writeJSONDic(dict_list=temp_dic, file_name=temp_file)
        #print("Here")

    def reportDuplication(self):
        self.translateAndSaveEntriesFromPOFiles()
        #self.mergeTempWithJSONDic()

    def update_master_dic(self, op=None):

        def mergeDicsToMaster():
            # start_dic : dict = self.master_dic_list
            # print("len self.master_dic_list started:", len(self.master_dic_list))
            # start_dic.update(self.json_dic_list)
            # print("len self.master_dic_list after updated with json:", len(self.master_dic_list))
            po_cat = c.load_po(self.vipo_dic_path)
            po_dic_list = self.poToDic(po_cat)
            self.master_dic_list.update(po_dic_list)
            print("len self.master_dic_list after updated with vipo:", len(self.master_dic_list))

            u_case = cm.removeLowerCaseDic(self.master_dic_list)
            print("len self.master_dic_list after removed lcase:", len(u_case))
            self.writeJSONDic(dict_list=u_case, file_name=self.master_dic_file, remove_lcase=True)



        def removeLowerCaseEntries(dic_list, dic_file):
            u_case = cm.removeLowerCaseDic(dic_list)
            self.writeJSONDic(dict_list=u_case, file_name=dic_file)

        def updateFromAPOFile(file_name):
            if not file_name or len(file_name) == 0:
                return

            if not os.path.isfile(file_name):
                return

            is_update = (self.update_dic == 1)
            if not is_update:
                return

            dic_cat = c.load_po(file_name)
            for index, m in enumerate(dic_cat):
                is_first_line = (index == 0)
                if is_first_line:
                    continue

                v = m.string
                has_translation = not ((v is None) or (len(v) == 0))
                if not has_translation:
                    continue

                k = m.id
                k_lower=k.lower()
                v = self.simpleRemoveOriginal(k, v)
                v = self.simpleRemoveOriginal(k_lower, v)
                has_translation = not ((v is None) or (len(v) == 0))
                if not has_translation:
                    continue

                is_same = (k == v) or (k_lower == v) or cm.hasOriginal(k, v)
                if is_same:
                    continue

                entry = {k:v}
                self.master_dic_list.update(entry)
                entry = {k_lower:v}
                self.master_dic_list.update(entry)

        if op == 'from_po':
            updateFromAPOFile(self.update_po_file)
        elif op == 'rm_lcase_master':
            removeLowerCaseEntries(self.master_dic_list, self.master_dic_file)
        elif op == 'rm_lcase_external':
            removeLowerCaseEntries(self.json_dic_list, self.json_dic_file)
        elif op == 'merge_dics':
            mergeDicsToMaster()


    def JSONToMasterDic(self, json_dic):
        for k,v in json_dic.items():
            s = v.string
            self.master_dic_list.update({k:s})

    def poToDic(self, po_cat):
        dic_list={}
        for index, m in enumerate(po_cat):
            if index == 0:
                continue

            k = m.id
            v = m.string
            is_ignore = (m.fuzzy or (len(v) == 0))
            if is_ignore:
                continue

            k_lower = k.lower()
            v = self.simpleRemoveOriginal(k, v)

            dic_list.update({k:v})
            dic_list.update({k_lower: v})

        return dic_list

    def poToMasterDic(self, po_cat):
        dic_list = self.poToDic(po_cat)
        self.master_dic_list.update(dic_list)
        self.writeJSONDic(dict_list=self.master_dic_list, file_name=self.master_dic_file, remove_lcase=True)
        # print("Debug")

    def removeJSONDicNoTranslation(self, dic):
        dic_removable=[]
        for k,v in dic.items():
            has_translation = (len(v)>0)
            if not has_translation:
                dic_removable.append(k)

        try:
            for k in dic_removable:
                del dic[k]
        except KeyError:
            print("Key {} not found.".format(k))
        return dic

    def makeJSONLowerCaseDic(self, dic):
        lcase_dic={}
        for k,v in dic.items():
            lk = k.lower()
            lv = v
            lcase_dic.update({lk:lv})
        pp(lcase_dic)
        #exit(0)
        return lcase_dic

    def writeJSONDic(self, dict_list=None, file_name=None, remove_lcase=False):
        try:
            file_path = (self.master_dic_file if (file_name is None) else file_name)
            dic = (self.master_dic_list if (dict_list is None) else dict_list)

            u_dic = (cm.removeLowerCaseDic(dic) if remove_lcase else dic)
            with open(file_path, 'w', newline='\n', encoding='utf8') as out_file:
                json.dump(u_dic, out_file, ensure_ascii=False, sort_keys=True, indent=0, separators=(',', ': '))
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
                    if DEBUG:
                        _("Loaded:{}".format(len(local_dic)))
                else:
                    raise Exception("dic [{}] is EMPTY. Not expected!", file_path)
        except Exception as e:
            _("Exception readDictionary Length of read dictionary:")
            _(e)
            raise e

        local_dic = self.removeJSONDicNoTranslation(local_dic)
        dic_lower_set=dict((k.lower(),v) for k,v in local_dic.items())
        local_dic.update(dic_lower_set)
        if DEBUG:
            _("after cleaned:{}".format(len(local_dic)))
        return local_dic


    def loadTranslatedPO(self):
        all_po_dict={}
        all_po_dict_lower = {}
        getter = POBasic(self.current_po_dir, False)
        po_dir_list = getter.getSortedPOFileList()
        for(index, po_file_path) in enumerate(po_dir_list):
            if (len(po_file_path) <= 0):
                continue
            po_cat = c.load_po(po_file_path)

        # _("all_po_dict:")
        # pp(all_po_dict)
        # # exit(0)
        return all_po_dict, all_po_dict_lower

    def poCatToList(self, po_cat):
        l = []
        for index, m in enumerate(po_cat):
            k = m.id
            v = m
            l.append((k, v))
        return l

    def poCatToListLower(self, po_cat):
        l = []
        for index, m in enumerate(po_cat):
            k = m.id.lower()
            v = m
            l.append((k, v))
        return l

    def poCatDictLower(self, po_cat):
        l = {}
        for index, m in enumerate(po_cat):
            k = m.id.lower()
            v = m
            l.update({k: v})
        return l

    # __(sorted_lower_po_dic)

    def dump_po(self, filename, catalog):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        with io.open(filename, 'wb') as f:
            pofile.write_po(f, catalog, width=4096)

    def simpleRemoveOriginal(self, msg, trans):

        has_original_in_trans = (msg in trans)
        if not has_original_in_trans:
            msg, ga_state = cm.removeGA(msg)

        p = " -- {}".format(msg)
        p1 = "-- {}".format(msg)
        temp = str(trans)
        temp = temp.replace(p, "")
        temp = temp.replace(p1, "")
        return temp

    def removeOriginal(self, msg, trans):
        msg = re.escape(msg)
        p = r'\b{}\b'.format(msg)
        has_original = (re.search(p, trans, flags=re.I) != None)
        endings=("", "s", "es", "ies", "ed", "ing", "lly",)
        if has_original:
            for end in endings:
                p = r'-- {}{}'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            for end in endings:
                p = r'{}{} --'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            for end in endings:
                p = r'\\b{}{}\\b'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)
            trans = trans.strip()
            is_empty = (len(trans) == 0)
            if is_empty:
                trans = None

        return trans

    def isInList(self, msg, find_list, is_lower=False):
        trans = None
        try:
            orig_msg = str(msg)
            if is_lower:
                msg = msg.lower()
            trans = find_list[msg]

            has_translation = trans and (len(trans) > 0) and (trans != 'None')
            if has_translation:
                trans = trans.strip()
                trans = self.removeOriginal(msg, trans)
                trans = cm.matchCase(orig_msg, trans)
            return trans
        except Exception as e:
            # if msg:
            #     print(msg)
            # if find_list:
            #     print("dic len={}".format(len(find_list)))
            # print("is_lower:", is_lower)
            #raise e
            return None

    def findTranslationByFragment(self, msg):
        _("findTranslationByFragment", msg)
        if isIgnored(msg):
            return None

        #_("findTranslationByFragment:[{}]".format(msg))
        msg = unescape(msg)

        orig_msg = str(msg)

        has_ref_link = (cm.REF_LINKS.search(msg) != None)
        if has_ref_link:
            rs, re, msg, refuri = cm.removeRefLink(msg)

        trans_list = []
        trans = str(msg)
        for w_start, w_end, w_match_0, w_match_1 in cm.patternMatchAsList(cm.WORD_ONLY_FIND, msg):
            is_found = (w_match_0 != None)
            if not is_found:
                continue

            orig = (w_match_1 if w_match_1 else w_match_0)
            trans_word = trans_finder.findTranslation(orig)
            trans_word_entry = (w_start, w_end, orig, trans_word)
            trans_list.append(trans_word_entry)

        has_result = (len(trans_list) > 0)
        if not has_result:
            return None

        for w_start, w_end, orig, trans_word in reversed(trans_list):
            if trans_word:
                si = trans.find(orig, w_start, w_end)
                _("w_start", w_start, "si", si, "orig", orig)
                w_end = w_start + len(orig)
                st = trans[:si]
                se = trans[w_end:]
                trans = st + trans_word + se

        ref_entry = {msg: trans}
        self.ref_dic_list.update(ref_entry)

        is_changed = (trans != msg)
        if not is_changed:
            trans = None

        if trans and has_ref_link:
            #trans = "{} {}".format(trans, refuri)
            _("RESULT findTranslationByFragment: [{}] => [{}]".format(msg, trans))

        return trans

    def findTranslation(self, msg):
        trans = None

        orig_msg = str(msg)
        ending_with_punctuations = (cm.ENDS_PUNCTUAL.search(msg) is not None)
        if ending_with_punctuations:
            msg = cm.ENDS_PUNCTUAL.sub("", msg)

        list_name = "self.master_dic_list"
        trans = self.isInList(msg, self.master_dic_list)
        if not trans:
            list_name = "self.master_dic_list LOWER"
            trans = self.isInList(msg, self.master_dic_list, is_lower=True)
            if not trans:
                list_name = "cm.KEYBOARD_TRANS_DIC"
                trans = self.isInList(msg, cm.KEYBOARD_TRANS_DIC)
                if not trans:
                    list_name = "cm.KEYBOARD_TRANS_DIC LOWER"
                    trans = self.isInList(msg, cm.KEYBOARD_TRANS_DIC, is_lower=True)

        has_tran = not (trans is None)
        has_len = (has_tran and (len(trans) > 0))
        has_translation = has_len and (trans != 'None')
        if has_translation:
            trans = trans.strip()
            trans = self.removeOriginal(msg, trans)
            _("findTranslation in {} [{}] => [{}]".format(list_name, msg, trans))

            if ending_with_punctuations:
                trans = orig_msg.replace(msg, trans)
        else:
            trans = None

            # ref_entry = {msg:""}
            # self.ref_dic_list.update(ref_entry)

        return trans

    def translateText(self, msg : str):
        _("translateText input:", msg)
        #
        # list_of_functions = [
        #     self.transMenuselection,
        #     self.trans_keyboard,
        #     self.transRef,
        #     trans_finder.findTranslation,
        #     trans_finder.findTranslationByFragment
        # ]

        is_menu = (cm.MNU in msg)
        is_kbd = (cm.KBD in msg)
        is_ref = (cm.REF_KEYS.search(msg) != None)
        is_ref_with_no_keys = (cm.REF_LINK_WITHOUT_REFWORD.search(msg) != None)
        has_bracket = (cm.GA_BRACKETTED.search(msg) != None)

        clean_msg, ga_state = cm.removeGA(msg)
        _("clean_msg:", clean_msg)
        _("ga_state:", ga_state)
        if isIgnored(clean_msg):
            _("IGNORE", clean_msg)
            return None

        has_ga = (ga_state > 0)
        is_single_character = (has_ga and len(clean_msg) == 1) or (len(msg) == 1)
        if is_single_character:
            return None

        is_translated_by_fragment = False

        if is_ref and is_menu:
            _("0001")
            if has_ga:
                _("0001-0001")
                t = self.transMenuselection(clean_msg)
            else:
                _("0001-0002")
                t = self.transMenuselection(msg)
        elif is_ref and is_kbd:
            _("0002")
            if has_ga:
                _("0002-0001")
                t = self.trans_keyboard(clean_msg)
            else:
                _("0002-0002")
                t = self.trans_keyboard(msg)
        elif is_ref or is_ref_with_no_keys:
            _("0003")
            if has_ga:
                _("0003-0001")
                t = self.simpleTransRef(clean_msg)
            else:
                _("0003-0002")
                t = self.simpleTransRef(msg)
        else:
            _("0004")
            if has_ga:
                _("0004-0001")
                t = trans_finder.findTranslation(clean_msg)
            else:
                _("0004-0002")
                t = trans_finder.findTranslation(msg)

            if t and has_ga:
                t = "{} -- {}".format(t, clean_msg)
            elif (not t) and has_ga:
                rs, re, ref_text, refuri = cm.removeRefLink(clean_msg)
                has_ref_text = (len(ref_text) > 0)
                if has_ref_text:
                    t = "-- {}".format(clean_msg)
                else:
                    t = clean_msg
        if not t:
            _("0005")
            if has_ga:
                _("0005-0001")
                t = trans_finder.findTranslationByFragment(clean_msg)
                ref_entry = {clean_msg: ""}
            else:
                _("0005-0002")
                ref_entry = {msg: ""}
                t = trans_finder.findTranslationByFragment(msg)

            self.ref_dic_list.update(ref_entry)

        need_to_replace = (t and has_ga)
        if need_to_replace:
            t = msg.replace(clean_msg, t)


        if t:
            _("translateText output:", t)
        else:
            _("translateText output: NOTHING")
        _('*' * 80)
        return t

    # /home/htran/blender_documentations/blender_docs/build/rstdoc/addons/3d_view/3d_navigation.html
    def transMenuselection(self, msg):
        _("transMenuselection input:", msg)
        is_menu = (":menuselection:" in msg)
        if not is_menu:
            return None

        if isIgnored(msg):
            return None

        trans = None
        for w_start, w_end, w_match_0, w_match_1 in cm.patternMatchAsList(cm.TEXT_BETWEEN_REFS, msg):

            has_result = (w_match_0 != None)
            if not has_result:
                continue

            _("w_start, w_end, w_match_0, w_match_1")
            _(w_start, w_end, w_match_0, w_match_1)

            if isIgnored(w_match_1):
                continue

            if w_match_1:
                list_of_menu_items = cm.patternMatchAsList(cm.NOT_MENU_SEP, w_match_1)
                word_list = cm.patternCollectMatches(list_of_menu_items, position=[2])
                trans_list = self.translatePara(word_list)

                new_list_of_menu_item = []
                for i, e in enumerate(list_of_menu_items):
                    s, e, orig, p1 = e
                    tran = trans_list[i][1]
                    orig_s = orig.strip()
                    tran_s = tran.strip()
                    is_empty_orig = (len(orig_s) == 0)
                    is_empty_tran = (len(tran_s) == 0)
                    is_same = (orig_s == tran_s)
                    if is_same or (is_empty_orig and is_empty_tran):
                        continue
                    if (not (is_empty_orig or is_empty_tran)):
                        tran_txt = "{} ({})".format(tran_s, orig_s)
                    elif (not is_empty_orig and is_empty_tran):
                        tran_txt = "({})".format(orig_s)
                    else:
                        tran_txt = None

                    if (not tran_txt is None):
                        tran = orig.replace(orig_s, tran_txt)
                        new_entry = (s, e, orig, tran)
                        new_list_of_menu_item.append(new_entry)

                w_match_1_copy = str(w_match_1)
                for s, e, orig, trans in reversed(new_list_of_menu_item):
                    lead = w_match_1_copy[:s]
                    tail = w_match_1_copy[e:]
                    w_match_1_copy = lead + trans + tail
                _("FINAL {}".format(w_match_1_copy))

                w_match_0_copy = w_match_0.replace(w_match_1, w_match_1_copy)

                lead = msg[:w_start]
                tail = msg[w_end:]
                trans = lead + w_match_0_copy + tail
                break

        return trans


    def simpleTransRef(self, msg):

        _("simpleTransRef input:", msg)

        input_msg = str(msg)
        orig = str(msg)
        is_single_ga = cm.isSingleGA(msg)
        is_double_ga = cm.isDoubleGA(msg)
        has_ref_link = (cm.REF_LINKS.search(msg) != None)
        is_bracketed = (cm.WORD_INSIDE_BRAKET.search(msg) != None)
        has_ref_keyword = (cm.REF_KEYS.search(msg) != None)

        search_result, ga_state = cm.removeGA(msg)
        #_("DEBUG")

        if has_ref_keyword:
            s, e, orig, search_result = cm.patternMatchAsParts(cm.TEXT_BETWEEN_REFS, search_result)

        if has_ref_link:
            rs, re, search_result, refuri = cm.removeRefLink(search_result)
        elif is_bracketed:
            bs, be, orig, search_result = cm.patternMatchAsParts(cm.WORD_INSIDE_BRAKET, search_result)

        orig_text = (search_result if (search_result is not None) else orig)
        if isIgnored(orig_text):
            return None

        trans = trans_finder.findTranslation(orig_text)

        # if trans is None:
        #     msg_txt = (search_result if search_result else orig)

        # is_debug = ("grease-pencil-modifier-influence-filters" in input_msg)
        # if is_debug:
        #     print("DEBUG")

        if trans:
            trans = "{} -- {}".format(trans, orig_text)
        else:
            # see if this is a ref: grease-pencil-modifier-influence-filters
            word_list = orig_text.split()
            is_link = (len(word_list) == 1) and (word_list[0].count(cm.HYPHEN) > 1) # a rather crude way to guess this is a ref
            if not is_link:
                trans = "-- {}".format(orig_text)
            else:
                trans = orig_text

        if has_ref_link:
            orig_text = ("{} {}".format(orig_text, refuri) if (refuri not in orig_text) else orig_text)
            trans = "{} {}".format(trans, refuri)
        trans = input_msg.replace(orig_text, trans)

        # if trans and search_result:
        #     trans = "{} -- {}".format(trans, search_result)
        #     trans = input_msg.replace(search_result, trans)
        # elif trans and not search_result:
        #     trans = "{} -- {}".format(trans, orig)
        #     trans = input_msg.replace(orig, trans)
        # elif search_result:
        #     trans = "-- {}".format(search_result)
        #     trans = input_msg.replace(search_result, trans)
        # else:
        #     trans = "-- {}".format(orig)
        #     trans = input_msg.replace(orig, trans)

        _("RESULT simpleTransRef: ", trans)

        return trans

    def transRef(self, msg):
        _("transRef input:", msg)

        if isIgnored(msg):
            return None

        search_result = str(msg)
        orig = None
        trans = None

        trans = trans_finder.findTranslation(msg)
        if not trans:
            for w_start, w_end, orig, search_result in cm.patternMatchAsList(cm.TEXT_BETWEEN_REFS, msg):

                has_result = (search_result != None)
                if not has_result:
                    continue

                # _("w_start, w_end, w_match_0, search_result")
                # _(w_start, w_end, w_match_0, search_result)

                if isIgnored(search_result):
                    continue

                is_packed_ref = (cm.PACKED_REF.search(search_result) != None)
                # _("check for packed ref", search_result, is_packed_ref)
                if is_packed_ref:
                    # _("search_result", search_result, "is PACKED REF")
                    rs, re, orig, search_result = cm.patternMatchAsParts(cm.REF_PART, search_result)
                    has_result = (search_result != None)
                    if not has_result:
                        continue

                    is_abbrev = orig.startswith(':abbr:')
                    if is_abbrev:
                        bs, be, orig, search_result =  cm.patternMatchAsParts(cm.WORD_INSIDE_BRAKET, search_result)
                        # _("bs, be, orig, search_result")
                        # _(bs, be, orig, search_result)
                        has_result = (search_result != None)
                        if not has_result:
                            continue

            has_result = (search_result != None)
            if has_result:
                trans = trans_finder.findTranslation(search_result)
            else:
                search_result = msg
                trans = None

        is_debug = ('SSAO' in msg)
        if is_debug:
            _('DEBUG')

        if trans:
            trans = "{} -- {}".format(trans, search_result)
        elif self.ref_uri: # items without refuri is NOT SURE to repeat or not
            trans = "-- {}".format(trans, search_result)
        else:
            trans = None

        if trans:
            trans = msg.replace(search_result, trans)

        return trans

        #     # if trans:
        #     #     trans = "{} -- {}".format(trans, w_match_1)
        #     #     _("DUPLICATING ORIGINAL HERE!", trans)
        #     #     trans = msg[:w_start+1] + trans + msg[w_end-1:]
        #     #
        # return trans

    def trans_keyboard(self, msg):
        trans = None
        is_keyboard = (":kbd:" in msg)
        if not is_keyboard:
            return None

        if isIgnored(msg):
            return None

        if DEBUG:
            _("trans_keyboard input:", msg)

        orig_text = str(msg)
        for w_start, w_end, w_match_0, w_match_1 in cm.patternMatchAsList(cm.TEXT_BETWEEN_REFS, msg):

            has_result = (w_match_0 != None)
            if not has_result:
                continue

            if w_match_1:
                trans = cm.translateKeyboardDef(w_match_1)
                if trans:
                    orig_text = orig_text.replace(w_match_1, trans)
        return orig_text

    def translatePara(self, list_of_para):
        trans_list = []
        for item in list_of_para:
            list_of_text_only = cm.patternMatchAsList(cm.PARA_SEP, item)
            has_text_list_among_symbols = (not cm.isPatternMatchListEmpty(list_of_text_only))
            if has_text_list_among_symbols:
                _("list_of_text_only:")
                pp(list_of_text_only)
                _("0000")
                trans = str(item)
                translated_list = []
                for ts, te, t0, t1 in reversed(list_of_text_only):
                    tr0 = trans_finder.findTranslation(t0)
                    if not tr0:
                        tr0 = trans_finder.findTranslationByFragment(t0)

                    if tr0 is not None:
                        trans = trans[:ts] + tr0 + trans[te:]
                    else:
                        trans = trans[:ts] + t0 + trans[te:]
                _("result 0 =", item, trans)
            else:
                _("0001")
                trans = trans_finder.findTranslation(item)
                if not trans:
                    trans = trans_finder.findTranslationByFragment(item)
                trans = (trans if (not trans is None) else item)
                trans = item.replace(item, trans)
                _("result 1 =",item, trans)
            # _("finally","non_space_item:", non_space_item)
            # _("finally","trans:", trans)

            entry=(item, trans)
            trans_list.append(entry)
        #pp(trans_list)
        #exit(0)
        return trans_list

    def treatingText(self, node):
        is_text = isinstance(node, nodes.Text)
        if not is_text:
            return

        msg = node.astext()

        is_ignore = isIgnored(msg)
        if is_ignore:
            raise Exception("Ignored item")

        trans = None
        para_list = cm.patternMatchAsList(cm.PARA_SEP, msg)
        for s, e, par, w1 in para_list:
            tran = trans_finder.findTranslation(par)
            has_tran = (tran is not None) and (len(tran) > 0)
            if not has_tran:
                tran = trans_finder.findTranslationByFragment(par)
                txt = (tran if tran is not None else "")
                trans_finder.updateRefDic(par, txt)

        # has_raw_source = (self.raw_source) and (msg in self.raw_source)
        # is_ref = self.is_ref_node #(cm.REF_KEYS.search((self.raw_source if has_raw_source else msg)) != None)
        #
        # if has_raw_source:
        #     pass
        #     # if (':menuselection:' in self.raw_source):
        #     #     trans = self.transMenuselection(self.raw_source)
        #     # elif (':kbd:' in self.raw_source):
        #     #     trans = self.trans_keyboard(self.raw_source)
        #     # elif is_ref:
        #     #     #abbr get('explanation') CAD => Computer-Aided Design
        #     #     trans = self.transRef(self.raw_source)
        #     #     self.is_ref_node = False
        # if not trans:
        #     trans = self.translateText(msg)
        #
        # is_ignore = (msg == trans)
        # if is_ignore:
        #     raise Exception("Message and Translation are the same")
        #
        # #keep_original = (self.keep_original) and not (is_menu or is_kbd)
        # keep_original = (self.keep_original and not is_ref)
        # if trans:
        #     if keep_original:
        #         trans = "{} -- {}".format(trans, msg)
        # else:
        #     if keep_original:
        #         trans = "-- {}".format(msg)
        #
        # if has_raw_source:
        #     trans = self.raw_source.replace(msg, trans)
        #     msg = self.raw_source
        #
        #     # _("NO TRANSLATION:", "MSG:", msg, "TRANS", trans)
        # self.node_msg = msg
        # self.node_trans = trans
        #
        # start_index = self.current_msg.find(msg)
        # end_index = start_index + len(msg)
        #
        # # emsg = re.escape(msg)
        # # p = re.compile(r'{}'.format(emsg))
        #
        # new_entry = (start_index, end_index, msg, trans)
        # # self.node_trans_list.update(new_entry)
        # self.node_trans_list.append(new_entry)
        # node.translation = trans
        raise Exception("Completed")

trans_finder = TranslationFinder()

MNU_SEL = 'menuselection'
MNU_SEP = '-->'
CLASS = 'classes'
RAWTXT = 'rawtext'
DOC = 'doc' #:doc:`keyframe
STD_REF="std std-ref" #:ref:`easings
X_REF="xref std std-term" #:term:`walk cycle
BACKQUOTE="`"
TR_ED='translated'
def print_separator(output_path):
    _("docname:", output_path)
    _("-" * 30)

def print_result_list(result):
    pp(result)

# type: <class 'docutils.nodes.caption'>
# type: <class 'docutils.nodes.emphasis'>
# type: <class 'docutils.nodes.field_name'>
# type: <class 'docutils.nodes.image'>
# type: <class 'docutils.nodes.inline'>
# type: <class 'docutils.nodes.line'>
# type: <class 'docutils.nodes.literal'>
# type: <class 'docutils.nodes.math'>
# type: <class 'docutils.nodes.math_block'>
# type: <class 'docutils.nodes.paragraph'>
# type: <class 'docutils.nodes.reference'>
# type: <class 'docutils.nodes.rubric'>
# type: <class 'docutils.nodes.strong'>
# type: <class 'docutils.nodes.superscript'>
# type: <class 'docutils.nodes.term'>
# type: <class 'docutils.nodes.Text'>
# type: <class 'docutils.nodes.title'>

class TranslationNodeVisitor(nodes.TreeCopyVisitor):
#class TranslationNodeVisitor(nodes.NodeVisitor):

    """Raise `nodes.NodeFound` if non-simple list item is encountered.

    Here 'simple' means a list item containing only a paragraph with a
    single reference in it.
    """
    def setVars(self, node, msg, trans):
        self.current_node = node
        self.current_msg = msg
        if trans:
            self.current_trans = trans
        else:
            self.current_trans = msg
        self.fuzzy_list = []
        self.is_fuzzy = False
        self.is_title_node = False
        self.tr = None
        self.ref_trans=[]
        self.node_msg = None
        self.raw_source = None
        self.node_trans = None
        self.node_trans_list=[]
        self.is_ref_node = False
        self.ref_uri = None




    def printNode(self, node, extra=None):
        if not DEBUG:
            return

        _('-'*50)
        if extra:
            _(extra)

        # _("self.current_msg:[{}]".format(self.current_msg))
        _("type:", type(node))
        if hasattr(node, 'children'):
            _("children:", node.children)

        #_("name:", type(node.name))
        _("pp node:")
        pp(node)
        if hasattr(node, 'astext'):
            msg = node.astext()
            msg = msg.strip()
            _("node text: [{}]".format(msg))

        if hasattr(node, 'rawsource'):
            _("rawsource: [{}]".format(node.rawsource))

        if hasattr(node, 'line'):
            _("line", node.line)

        _("")
        # _("dir:", dir(node))
        # _("len:", len(node))



    def getNodeMsg(self, node):
        msg = None
        has_rawsource = hasattr(node, 'rawsource')
        has_rawtext = ('rawtext' in node.attributes)
        if has_rawtext:
            msg = node.attributes['rawtext']
        elif has_rawsource:
            msg = node.rawsource
        else:
            msg = node.astext()
        self.raw_source = msg
        return msg

    def translate(self, node):
        if DEBUG:
            _("translate node input:", node.astext())
        msg = self.getNodeMsg(node)
        trans = trans_finder.translateText(msg)
        return trans

    def putTranslation(self, node):
        replace_translated_fragment = (self.node_msg and self.current_trans and self.node_trans)
        if replace_translated_fragment:
            node_msg = re.escape(self.node_msg)
            p_msg = r'{}'.format(node_msg)
            p = re.compile(p_msg)
            trans = node.rawsource
            for ts, te, m0, m1 in cm.patternMatchAsList(p, trans):
                has_result = (m0 != None)
                if not has_result:
                    continue

                trans = trans[:ts] + self.node_trans + trans[te:]

            self.current_trans = self.current_trans.replace(self.node_msg, trans)

        if self.current_trans and DEBUG:
            _("msgid", self.current_msg)
            _("msgstr", self.current_trans)

    def isRefNode(self, node):
        # class abbreviation(Inline, TextElement): pass
        # class acronym(Inline, TextElement): pass
        # class citation_reference(Inline, Referential, TextElement): pass
        # class emphasis(Inline, TextElement): pass
        # class footnote_reference(Inline, Referential, TextElement): pass
        # class literal(Inline, TextElement): pass
        # class math(Inline, TextElement): pass
        # class reference(General, Inline, Referential, TextElement): pass
        # class strong(Inline, TextElement): pass
        # class subscript(Inline, TextElement): pass
        # class substitution_reference(Inline, TextElement): pass
        # class superscript(Inline, TextElement): pass
        # class title_reference(Inline, TextElement): pass

        is_doc = (cm.DOC in node[cm.CLASS])
        is_menu = (cm.MNU in node[cm.CLASS])
        is_kbd = (cm.KBD in node[cm.CLASS])
        is_std_ref = (cm.STD_REF in node[cm.CLASS])
        is_x_ref = (cm.X_REF in node[cm.CLASS])
        is_gui_lab = (cm.GUI_LAB in node[cm.CLASS])

        is_ref = (is_doc or is_menu or is_kbd or is_std_ref or is_x_ref or is_gui_lab)
        return is_ref


    def setupNodeForTrans(self, node):
        self.raw_source = self.getNodeMsg(node)
        if DEBUG:
            _("RAW", self.raw_source, ":", type(node), node.astext())
        is_duplicated_already = self.isRefNode(node)
        self.is_ref_node = is_duplicated_already
        is_ignore = isIgnored(node.astext())
        self.keep_original = not ( is_ignore or is_duplicated_already)

        if self.is_ref_node:
            has_ref_uri = (cm.REF_URI in node.attributes)
            if has_ref_uri:
                self.ref_uri  = node.attributes[cm.REF_URI]
            else:
                self.ref_uri = None


    def default_departure(self, node):
        pass

    def default_visit(self, node):
        try:
            _("-"*50)
            trans_finder.treatingText(node)
            has_children = hasattr(node, 'children')
            if has_children:
                for child in node.children:
                    is_same_child = (child == node)
                    if not is_same_child:
                        trans_finder.treatingText(child)
        except Exception as e:
            self.node_msg = None
            self.node_trans = None
            self.keep_original = False

            # class 'docutils.nodes.emphasis' ##>
            # class 'docutils.nodes.image'>
            # class 'docutils.nodes.inline' ##>
            # class 'docutils.nodes.literal' ##>
            # class 'docutils.nodes.math'>
            # class 'docutils.nodes.reference' ##>
            # class 'docutils.nodes.strong' ##>
            # class 'docutils.nodes.Text'>

        # is_inline = isinstance(node, nodes.inline)
        # is_emphasis = isinstance(node, nodes.emphasis)
        # is_title = isinstance(node, nodes.title)
        # is_term = isinstance(node, nodes.term)
        # is_rubric = isinstance(node, nodes.rubric)
        # is_field_name = isinstance(node, nodes.field_name)
        # is_reference = isinstance(node, nodes.reference)
        # is_strong = isinstance(node, nodes.strong)

    def visit_title(self, node):
        _("visit_title", node.astext())
        self.setupNodeForTrans(node)
        #self.default_translation(node, keep_orig=True)

    def depart_title(self, node):
        _("depart_title", node.astext())

    def visit_term(self, node):
        _("visit_term", node.astext())
        self.setupNodeForTrans(node)

    def visit_rubric(self, node):
        _("visit_rubric", node.astext())
        self.setupNodeForTrans(node)

    def visit_field_name(self, node):
        _("visit_field_name", node.astext())
        #self.setupNodeForTrans(node)

    def visit_strong(self, node):
        _("visit_strong", node.astext())
        self.setupNodeForTrans(node)

    def visit_emphasis(self, node):
        _("visit_emphasis", node.astext())
        self.setupNodeForTrans(node)

    def visit_strong(self, node):
        _("visit_strong", node.astext())
        self.setupNodeForTrans(node)

    def depart_reference(self, node):
        msg = node.astext()
        _("depart_reference", msg)
        # is_debug = ('Editing' in msg)
        # if is_debug:
        #     _('DEBUG')
        # has_ref_uri = (cm.REF_URI in node.attributes)
        # if has_ref_uri:
        #     # ref = [#armature-editing-naming-conventions], actual form = :ref:`next page <armature-editing-naming-conventions>`
        #     refuri = node.attributes[cm.REF_URI]
        #     _('Attaching REFUIR', refuri)

    def visit_reference(self, node):
        _("visit_reference", node.astext())
        self.setupNodeForTrans(node)

    def depart_inline(self, node):
        _("visit_reference", node.astext())

    def visit_inline(self, node):
        _("visit_inline", node.astext())
        self.setupNodeForTrans(node)
        # is_doc = (cm.DOC in node[cm.CLASS])
        # is_menu = (cm.MNU in node[cm.CLASS])
        # is_kbd = (cm.KBD in node[cm.CLASS])
        # is_std_ref = (cm.STD_REF in node[cm.CLASS])
        # is_x_ref = (cm.X_REF in node[cm.CLASS])
        # is_gui_lab = (cm.GUI_LAB in node[cm.CLASS])
        #
        # accounted = (is_doc or is_menu or is_kbd or is_std_ref or is_x_ref or is_gui_lab)
        # if not accounted:
        #     _("NOT ACCOUNTED")
        # else:
        #     _("is_doc, is_menu, is_kbd, is_std_ref, is_x_ref, is_gui_lab")
        #     _(is_doc , is_menu , is_kbd , is_std_ref , is_x_ref , is_gui_lab)
        #     orig_msg = node.astext()
        #     _("text:", orig_msg)
        #     raw_source = self.getNodeMsg(node)
        #     if raw_source:
        #         _("raw_source:", raw_source)
        #     else:
        #         _("NO RAW")
        #     trans = None
        #     must_use_raw_source = (raw_source != orig_msg)
        #     if is_menu and must_use_raw_source:
        #         trans = self.transMenuselection(raw_source)
        #     elif is_kbd and must_use_raw_source:
        #         trans = self.trans_keyboard(raw_source)
        #     elif must_use_raw_source:
        #         trans = self.transRef(raw_source)
        #
        #     if trans:
        #         entry={raw_source:trans}
        #         self.node_trans_list.update(entry)
        #     #self.default_translation(orig_msg, keep_orig=True, raw=(raw_source if must_use_raw_source else None))


    def visit_literal(self, node):
        _("visit_literal", node.astext())
        self.setupNodeForTrans(node)
        # raw_source = self.getNodeMsg(node)
        # if raw_source:
        #     _("raw_source:", raw_source)
        # else:
        #     _("NO RAW")

    def depart_paragraph(self, node):
        return
        _("depart_paragraph", node.astext())
        msg = node.astext()
        raw_source = self.getNodeMsg(node)
        _("text:", msg)
        _("raw_source:", raw_source)
        trans = str(raw_source)
        for k,v in self.node_trans_list.items():
            trans = trans.replace(k, v)
        self.node_trans_list.clear()
        entry = {raw_source: trans}
        self.node_trans_list.update(entry)
        _('-'*80)
        pp(self.node_trans_list)
        _('-'*80)
        # #exit(0)

    def visit_paragraph(self, node):
        _("visit_paragraph", node.astext())
        # msg = node.astext()
        # _("text:", msg)
        # raw_source = self.getNodeMsg(node)
        # if raw_source:
        #     _("raw_source:", raw_source)
        # else:
        #     _("NO RAW")

        #self.default_translation(node)

    def visit_abbreviation(self, node):
        #:abbr: `POV(Point Of View)`
        _("visit_abbreviation", node.astext())
        self.setupNodeForTrans(node)
        # raw_source = ":abbr:`{} ({})`".format(node.astext(), node.get('explanation'))
        # expl = node.get('explanation')
        # trans = trans_finder.findTranslation(expl)
        # if trans:
        #     trans = "{} -- {}".format(expl, trans)
        # else:
        #     trans = "-- {}".format(expl)
        # trans = raw_source.replace(expl, trans)
        # entry = {raw_source:trans}
        # self.node_trans_list.update(entry)

    # def default_translation(self, node, keep_orig=False, raw=None):
    #     raw_source = None
    #     if raw:
    #         raw_source = raw
    #     else:
    #         raw_source = self.getNodeMsg(node)
    #
    #     orig = node.astext()
    #     trans = trans_finder.findTranslation(orig)
    #     if keep_orig:
    #         if trans:
    #             trans = "{} -- {}".format(orig, trans)
    #         else:
    #             trans = "-- {}".format(orig)
    #
    #     if trans:
    #         trans = raw_source.replace(orig, trans)
    #         entry = {raw_source:trans}
    #         self.node_trans_list.update(entry)

    def invisible_visit(self, node):
        # type: (nodes.Node) -> None
        """Invisible nodes should be ignored."""
        pass
# --------------------------------------------------------------

gtr = GTR() #Google translator

def dump_po(filename, catalog):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # Because babel automatically encode strings, file should be open as binary mode.
    with io.open(filename, 'wb') as f:
        pofile.write_po(f, catalog, width=4096)

def isInRefList(reflist, entry):
    is_empty_list = (not reflist or len(reflist) == 0)
    if is_empty_list:
        return False

    is_empty_entry = (not entry or len(entry) == 0)
    if is_empty_entry:
        return False

    start_post_list = []
    end_post_list = []
    extract_list = []

    es, ee, eorig, eextract = entry
    for s, e, orig, extract in reflist:
        is_entry = (s == es) and (e == ee) and (orig == eorig) and (eextract == extract)
        if is_entry:
            continue

        start_post_list.append(s)
        end_post_list.append(e)
        extract_list.append(extract)

    # _("es, ee, eorig, eextract")
    # _(es, ee, eorig, eextract)
    #
    # __(start_post_list)
    # __(end_post_list)
    # __(orig_list)

    is_in = (es in start_post_list) and (ee in end_post_list) and (eextract in extract_list)
    # _("is_in", is_in)

    return is_in

def doctree_resolved(app, doctree, docname):

    debug_file = cm.debug_file
    if debug_file:
        is_debug_file = (debug_file in docname)
        if not is_debug_file:
            return

        print('{} [{}], looking for:[{}]'.format(docname, is_debug_file, debug_file))
        #exit(0)
        # if not is_debug_file:
        #     return


    # current_po_dir = "/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
    # current_po_file = "{}.po".format(docname)
    # current_po_path = os.path.join(current_po_dir, current_po_file)
    #
    # trans_finder.update_po_file = current_po_path
    # trans_finder.update_dic = 1
    # trans_finder.update_master_dic()
    # return

    # k = "Preparations"
    # v = "Chuẩn Bị"
    # k_lower = k.lower()
    #
    # is_in = (k in trans_finder.master_dic_list)
    # if not is_in:
    #     trans_finder.master_dic_list.update({k:v})
    #     trans_finder.master_dic_list.update({k_lower:v})
    #     is_in = (k in trans_finder.master_dic_list)
    #     print("debug")

    build_dir = "build/rstdoc"
    po_vi_dir = "locale/vi/LC_MESSAGES"

    po_file_path="{}.po".format(docname)
    local_path = os.path.dirname(os.path.abspath( __file__ ))
    blender_docs_path = os.path.dirname(local_path)

    rst_output_location = os.path.join(blender_docs_path, build_dir)
    output_path = os.path.join(rst_output_location, po_file_path)

    print_separator(output_path)

    cat = Catalog()
    visitor_inited = False
    visitor : TranslationNodeVisitor = None

    #p_file_name = "<h3>{}</h3>".format(output_path)
    #print(p_file_name)
    for node, msg in extract_messages(doctree):
        #msg = unescape(msg).strip()
        msg = msg.strip()

        if not visitor_inited:
            visitor = TranslationNodeVisitor(node.document)
            visitor_inited = True
            cm.visitor = visitor
            cm.trans_finder = trans_finder

        is_inline = isinstance(node, nodes.inline)
        is_emphasis = isinstance(node, nodes.emphasis)
        is_title = isinstance(node, nodes.title)
        is_term = isinstance(node, nodes.term)
        is_rubric = isinstance(node, nodes.rubric)
        is_field_name = isinstance(node, nodes.field_name)
        is_reference = isinstance(node, nodes.reference)
        is_strong = isinstance(node, nodes.strong)

        is_keep_original = (is_inline or
                            is_emphasis or
                            is_title or
                            is_term or
                            is_rubric or
                            is_field_name or
                            is_reference or
                            is_strong
                            )
        current_trans = trans_finder.findTranslation(msg)

        # visitor.setVars(node, msg, current_trans)
        # # visitor.setVars(node, msg, None)
        # try:
        #     node.walkabout(visitor)
        # except Exception as e:
        #     _(e)
        #     raise e


        current_trans, msg_links, tran_links, unconnected_entries = cm.translateMsg(msg, current_trans)
        #
        # # how to NOT repeat if all msg_links constituted to the same original message
        #
        # if is_keep_original and current_trans:
        #     has_encap_orig = cm.hasEncapOrigInTrans(msg, current_trans)
        #     is_keep_original = (not has_encap_orig)
        # elif not is_keep_original and current_trans:
        #     current_trans = trans_finder.simpleRemoveOriginal(msg, current_trans)
        #
        # if is_keep_original and current_trans:
        #     current_trans = "{} -- {}".format(current_trans, msg)
        # elif is_keep_original and not current_trans:
        #     current_trans = "-- {}".format(msg)
        #
        # _('-' * 80)
        # # insert into the Catalog here as Messages and print out to output file.
        # is_same = (msg == current_trans)
        # if not is_same:
        #     cm.reportHTMLTable(msg, current_trans, msg_links, tran_links)
        #     if not (unconnected_entries is None) and (len(unconnected_entries) > 0):
        #         cm.reportHTMLTable(msg, "", msg_links, unconnected_entries)
        # else:
        #     cm.reportHTMLTable(msg, "", msg_links, tran_links)
        #
        # trans_finder.updateMasterBackup(msg, current_trans)

        # if current_trans:
        #     cat.add(msg, string=current_trans)
        # else:
        #     cat.add(msg, string="")

        #replaceRefTrans(msg, current_trans, visitor, cat)

    # p_page = "<hr/>"
    # print(p_page)
    
    # print_separator(output_path)
    # cat_is_not_empty = (len(cat) > 0)
    # if cat_is_not_empty:
    #     dump_po(output_path, cat)

    # app.config.debug_current_file_count += 1
    # is_debug_max_reached = (app.config.debug_current_file_count > app.config.debug_max_file_count)
    # if is_debug_max_reached:
    #     exit(0)

def config_inited(app, config):
    reportHTMLHead()

# doctree_resolved(app, doctree, docname):
def doctree_resolved_calcitem(app, doctree, docname):

    debug_file = cm.debug_file
    if debug_file:
        is_debug_file = (debug_file in docname)
        if not is_debug_file:
            return

    #trans_finder.mergeTempWithJSONDic()
    #exit(0)

    current_po_dir = "/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
    current_po_file = "{}.po".format(docname)
    current_po_path = os.path.join(current_po_dir, current_po_file)
    #trans_finder.calcDuplication(current_po_path)
    #trans_finder.calcEntries(current_po_path)


    for node, msg in extract_messages(doctree):
        #msg = unescape(msg).strip()
        msg = msg.strip()
        trans_finder.dic_list[msg] += 1

def build_finished_calcitem(app, exeption):
    trans_finder.reportDuplication()
    #trans_finder.removeUnusedEntriesFromMasterDict()

def builder_inited(app):
    # rm_lcase_external for json file

    trans_finder.takeTheOldDefIn()
    #trans_finder.update_master_dic(op='rm_lcase_master')
    #trans_finder.update_master_dic(op='rm_lcase_external')
    #trans_finder.update_master_dic(op='merge_dics')
    exit(0)
    #pass

def build_finished(app, exeption):

    #trans_finder.writeJSONDic(dict_list=trans_finder.master_dic_backup_list, file_name=trans_finder.master_dic_backup_file)
    #trans_finder.writeJSONDic(dict_list=trans_finder.master_dic_list, file_name=trans_finder.master_dic_file)
    #reportHTMLTail()
    #trans_finder.saveMasterBackup()
    trans_finder.saveRefDic()

def setup(app):

    cm.trans_finder = trans_finder


    # trans_finder.update_dic = 1
    # trans_finder.update_dic = 0
    # trans_finder.update_po_file = "/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES/about/contribute/install/linux.po"
    # app.connect('builder-inited', builder_inited)
    # app.connect('source-read', source_read)
    # app.connect('config-inited', config_inited)

    app.connect('doctree-resolved', doctree_resolved)
    # app.connect('build-finished', build_finished)

    #app.connect('doctree-resolved', doctree_resolved_calcitem)
    #app.connect('build-finished', build_finished_calcitem)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

#sphinx-build -t builder_html -b gettext  -j "8" manual build/locale

#!/usr/bin/python3



from sphinx.cmd.build import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
