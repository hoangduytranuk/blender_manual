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
import langdetect

from sphinx_intl import catalog as c
from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile

class FindFuzzyEntries:
    from_dir = "blender_documentations/blender_docs/"
    to_dir="blender_documentations/github/blender_manual/blender_docs/"
    log_file_name="rsync_run.txt"
    def __init__(self):
        self.po_path="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"

    def dump_po(self, filename, catalog):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        with io.open(filename, 'wb') as f:
            pofile.write_po(f, catalog, width=0)

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
        print("msgid: [{}]".format(m.id))
        print("msgstr:[{}]".format(m.string))
        if (extra_message != None):
            print("{}".format(extra_message))

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


    def checkForFuzzy(self, doc, file_name):
        is_changed = False
        is_fuzzy = False
        for index, m in enumerate(doc):
            is_first_item = (index == 0)
            if (is_first_item):
                continue

            if (not m.fuzzy):
                continue


            is_fuzzy = True
            changed = self.resolveFuzzyIfPossible(m, doc, file_name)
            if (changed):
                is_changed = True
            #print("ID:{}\n".format(m.id))

        if (is_fuzzy):
            print("Fuzzy:{}".format(file_name))
            print("=" * 80)

        if (is_changed):
            #file_name="/home/htran/test_vi.po"
            self.dump_po(file_name, doc)

    def run(self):
        #exit(0)
        self.po_file_list = self.getPOFileList()
        for po_file in self.po_file_list:
            po_doc = c.load_po(po_file)
            self.checkForFuzzy(po_doc, po_file)

x = FindFuzzyEntries()
x.run()
