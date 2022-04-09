#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""

import sys
sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
sys.path.append("/home/htran/bin/python/PO")
sys.path.append("/home/htran/bin")

import re
import os
import io
import json
import langdetect
import threading
import time

from sphinx_intl import catalog as c
from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile

loc = threading.Lock()

DEBUG=False
class FillTranslation:
    from_dir = "/home/htran/blender_documentations/blender_docs/"
    to_dir="blender_documentations/github/blender_manual/blender_docs/"
    dic_file="/home/htran/menuselection_new_dictionary_sorted_translated_0027.json"
    dic_list={}
    dic_list_updated=False

    exclude_files=[
        "getting_started/help.po",
        "render/freestyle/parameter_editor/line_style/tabs.po",
        "data_system/files/media/image_formats.po"
        ]
    def __init__(self):
        self.po_path="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
        self.doc_path = None
        self.po_path = FillTranslation.from_dir

        self.file_name_printed = False
        self.new_text = None



    def writeDictionary(self, dict_list=None, file_name=None):
        try:
            file_path = (FillTranslation.dic_file if (file_name == None) else file_name)
            dic = (FillTranslation.dic_list if (dict_list == None) else dict_list)
            #print("Length of write dictionary:{}".format(len(dic)))
            #print("dictionary:{}".format(dic))
            print("writeDictionary:{}".format(file_path))
            if (DEBUG): return
            with open(file_path, 'w', newline='\n', encoding='utf8') as out_file:
                json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
                out_file.close()
        except Exception as e:
            print("Exception writeDictionary Length of read dictionary:{}".format(len(FillTranslation.dic_list)))
            raise e


    def readDictionary(self, file_name=None):
        try:
            file_path = (FillTranslation.dic_file if (file_name == None) else file_name)
            print("readDictionary:{}, current size:{}".format(file_path, len(FillTranslation.dic_list)))
            with open(file_path) as in_file:
                FillTranslation.dic_list = json.load(in_file)
                print("Loaded:{}".format(len(FillTranslation.dic_list)))
                in_file.close()
        except Exception as e:
            print("Exception readDictionary Length of read dictionary:{}".format(len(FillTranslation.dic_list)))
            raise e

    def printFileNameOnce(self, file_name, extra_message=None):
        if (self.file_name_printed):
            return
        if (extra_message == None):
            msg = "{}".format(file_name)
        else:
            msg = "{}; {}".format(extra_message, file_name)

        print(msg)
        print("." * 80)
        self.file_name_printed = True

    def resetFileNamePrinted(self):
        self.file_name_printed = False

    def printMessageEntry(self, m, extra_message=None):
        if (extra_message != None):
            print("{}".format(extra_message))
        print("msgid: [{}]".format(m.id))
        print("msgstr:[{}]".format(m.string))

    # def dump_po(self, filename, catalog):
    #     print("dump_po - writting to:{}".format(filename))
    #     print("-" * 80)
    #     if (DEBUG): return
    #     dirname = os.path.dirname(filename)
    #     if not os.path.exists(dirname):
    #         os.makedirs(dirname)
    #
    #     # Because babel automatically encode strings, file should be open as binary mode.
    #     with io.open(filename, 'wb') as f:
    #         pofile.write_po(f, catalog, width=0)

    def getPOFileList(self):
        po_file_list=[]
        for dirpath, dirnames, filenames in os.walk(self.po_path):
            for filename in filenames:
                po_file = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(po_file)
                #basename = relpath(base, self.po_path)
                is_po_file = (ext == ".po")
                #print("po_file:{}, extension:{}, is_po_file:{}".format(po_file, ext, is_po_file))
                if (is_po_file):
                    po_file_list.append(po_file)

        return sorted(po_file_list)

    def CheckLanguage(self, text):
        # identifier.set_languages(DETECT_LANGUAGES)
        try:
            langs = langdetect.detect_langs(text)
        except UnicodeDecodeError:
            langs = langdetect.detect_langs(text.decode("utf-8"))

        sorted_lang = sorted(langs)
        for lang in langs:
            prob = lang.prob
            lang = lang.lang
            is_very_probable = (prob > 0.50)
            if (is_very_probable):
                return lang

        return None

    def getReplaceText(self, m):
        replace = m.id
        is_subtitle = (m.string.find(" -- ") >= 0)
        if (is_subtitle):
            replace = " -- {}".format(m.id)
        return replace

    def printMessageEntry(self, m, extra_message=None):
        if (extra_message != None):
            print("{}".format(extra_message))

        print("msgid: [{}]".format(m.id))
        print("msgstr:[{}]".format(m.string))

    def resolveFuzzyIfPossible(self, m, doc, file_name):
        trans = m.string
        lang = self.CheckLanguage(trans)
        is_found_lang = (lang != None)
        if (is_found_lang):
            is_vietnamese = (lang == 'vi')
            if (is_vietnamese):
                self.printMessageEntry(m, extra_message="Vietnamese, NOT CHANGED")
                print("-" * 50)
                return False

        #self.printMessageEntry(m, extra_message="English or OTHERWISE, before changes")
        m.string = self.getReplaceText(m)
        m.flags = set([]) #clear fuzzy flag for the message entry
        #print("-" * 20)
        #self.printMessageEntry(m, extra_message="English or OTHERWISE, AFTER changed")
        #print("-" * 50)
        return True


    def updateDictionary(self, m, file_name):
        en = m.id
        vi = m.string

        is_same_with_en = (vi == en)
        if (is_same_with_en):
            return

        is_fuzzy = (m.fuzzy)
        if (is_fuzzy):
            return

        has_menuselection = (re.search(r":menuselection:", en) != None)
        if (has_menuselection):
            return

        has_keyboard = (re.search(r":kbd:", en) != None)
        if (has_keyboard):
            return

        is_subtitle = (vi.find(en) > 0)
        if (not is_subtitle):
            return
        else:
            #1. only have " -- "
            is_not_translated = (re.search(r"^[ ]*-- ", vi) != None)
            if (is_not_translated):
                return

            self.printFileNameOnce(file_name)
            part_list = vi.split("--")
            #print("part_list:{}".format(part_list))

            vi = part_list[0].strip()

            dic_en = "({})".format(en)
            self.dic_list.update({dic_en:vi})
            print("Added Dictionary:[{}]:[{}]".format(dic_en, vi))
        self.dic_list_updated = True

    def FindAndFill(self, doc, file_name):
        is_changed = False
        for index, m in enumerate(doc):
            is_first_item = (index == 0)
            if (is_first_item):
                continue

            en = m.id
            vi = m.string
            has_translation = (vi != None) and (len(vi) > 0)

            dic_en = "({})".format(en)
            if (not dic_en in FillTranslation.dic_list):
                self.updateDictionary(m, file_name)
                #self.printMessageEntry(m, extra_message="Not in dictionary. IGNORE")
                #self.printFileNameOnce(file_name)
                continue

            dic_vi = FillTranslation.dic_list[dic_en]
            rep = "{} -- {}".format(dic_vi, en)
            if (has_translation):
                is_done_already = (rep == vi)
                if (is_done_already):
                    #self.printMessageEntry(m, extra_message="Done already! IGNORE")
                    #self.printFileNameOnce(file_name)
                    continue

            self.printMessageEntry(m, extra_message="BEFORE")
            m.string = rep
            is_changed = True
            self.printMessageEntry(m, extra_message="CHANGED TO")
            if (m.fuzzy):
                m.fuzzy = set([])

        if (is_changed):
            #file_name="/home/htran/test_vi.po"
            self.dump_po(file_name, doc)

    def isExcluded(self, file_name):
        for x in self.exclude_files:
            is_exclude = (re.search(x, file_name) != None)
            if (is_exclude):
                return True
        return False

    def run(self):
        with lock_():
            self.readDictionary()

        #self.writeDictionary()
        #exit(0)
        self.dic_list_updated = False
        self.po_file_list = self.getPOFileList()
        for po_file in self.po_file_list:
            if (self.isExcluded(po_file)):
                continue

            po_doc = c.load_po(po_file)
            self.FindAndFill(po_doc, po_file)
            self.resetFileNamePrinted()

        if (self.dic_list_updated):
            self.writeDictionary()


x = FillTranslation()
x.run()
