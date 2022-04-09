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

from sphinx_intl import catalog as c
from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile

class CopyExistingTranslation:

    def __init__(self):
        self.po_path="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
        self.po_file_list = None
        self.sorted_master_dic = None

    def binarySearch(self, sorted_list, po_id):
        #found_item = Algo.binarySearch(self.block_list, msgid_entry, cmp=self.compareMSGID)

        ss_list = sorted_list
        lo = 0
        hi = len(ss_list)
        mid = -1
        while (lo < hi):
            mid = (lo + hi) // 2
            k = list(ss_list)[mid]
            ss_list_entry = k
            po_entry_msg = po_id
            #print("ss_list_entry:{} <=> po_entry_msg:{}\n".format(ss_list_entry, po_entry_msg))
            if (ss_list_entry == po_entry_msg):
                return mid
            elif (ss_list_entry < po_entry_msg):
                #print("lo = mid + 1")
                lo = mid + 1
            else:
                #print("hi = mid")
                hi = mid
        #print("Not found")
        #exit(0)
        return -1

    # def dump_po(self, filename, catalog):
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
        return po_file_list

    def docToDic(self, po_doc):
        dic={}
        for index, m in enumerate(po_doc):
            is_first_entry = (index == 0)
            if (is_first_entry):
                continue

            k = m.id
            v = m
            trans = m.string


            not_empty = (len(trans) > 0)
            if (not_empty and (len(k.split()) > 2)):
                id_first_2_word = k.split()[:2]
                trans_first_2_word = trans.split()[:2]
                is_trans_repeat_of_original = (id_first_2_word == trans_first_2_word)

                if (is_trans_repeat_of_original):
                    continue

            is_keyboard = (k.startswith(":kbd:"))
            if (is_keyboard):
                continue

            has_been_translated = (not_empty) and \
                                  (not trans.startswith("-- ")) and \
                                  (not trans.startswith(" -- ")) and \
                                      (k != trans)

            if (has_been_translated):
                dic.update({k:v})

        return dic

    def loadDictionary(self):
        master_dic={}
        self.po_file_list = self.getPOFileList()
        for po_file in self.po_file_list:
            po_doc = c.load_po(po_file)
            doc_dic = self.docToDic(po_doc)
            master_dic.update(doc_dic)

        return master_dic


    def updateDocument(self, doc, file_name):
        is_dirty = False
        for index, m in enumerate(doc):
            is_first_item = (index == 0)
            if (is_first_item):
                continue

            search_key = m.id
            if (search_key not in self.sorted_master_dic):
                #print("NOT IN DICTIONARY: search_key:{} of file: {}".format(search_key, file_name))
                continue

            v = self.sorted_master_dic.get(search_key)
            translated_string = v.string
            message_string = m.string

            has_id_in_string = (message_string.find(search_key) >= 0)
            has_translation_text = (message_string.find(" -- ") > 1)

            is_translated = (has_id_in_string and has_translation_text)
            if (is_translated):
                continue

            is_update = (translated_string != message_string)
            if (not is_update):
                continue

            old_mesage = str(m.string)
            m.string = translated_string
            print("Updating")
            print("msgid \"{}\"".format(m.id))
            print("msgstr \"{}\"".format(m.string))
            print("FROM : [{}]".format(old_mesage))
            is_dirty = True

        return is_dirty

    def run(self):
        master_dic = self.loadDictionary()
        self.sorted_master_dic = master_dic
        for po_file in self.po_file_list:
            po_doc = c.load_po(po_file)
            changed = self.updateDocument(po_doc, po_file)
            if (changed):
                print("Save changes to file:{}".format(po_file))
                print("=" * 80)
                #po_file = "/home/htran/test.po"
                self.dump_po(po_file, po_doc)



x = CopyExistingTranslation();
x.run()
