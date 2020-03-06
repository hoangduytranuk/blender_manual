#!/usr/bin/env python3
import sys
sys.path.append("/home/htran/bin/python/PO")
sys.path.append("/home/htran/bin/python/algorithm")
sys.path.append("/home/htran/bin/python/base")
sys.path.append("/home/htran/bin/python/event")


import os
from bisect import bisect_left
from basefileio import BaseFileIO
#from common import Common as cm
from podocument import Document
#from potextblock import TextBlock
#from blankmessage import BlankMessage
from diff_two_documents import DiffTwoDocumentAction

#from find_untranslated_section_title import FindUntranslatedSectionTitle
#from ending_colon import EndingColon
#from copy_msgid_to_msgstr import CopyMSGID_to_MSGSTR
#from set_fuzzy import SetFuzzy
#from remove_msgstr_if_same_with_msgid import RemoveMSGSTRIfSameWithMSGID
#from compare_msgctxt import CompareMSGCTXT
from compare_msgid import CompareMSGID

#from action import BasicTwoDocumentAction, TwoDocumentAction
from action import TwoDocumentAction
from pobase import POBasic
#from algorithms import Algo

from argparse import ArgumentParser
#import collections
#import json
import re
"""
Compare two vi.po files and possibly merge entries
"""
print(sys.path)

class CompareViPo(BaseFileIO):
    def __init__(self):
        self.from_vi_po = None
        self.to_vi_po = None
        self.out_vi_po = None
        self.is_compare_only = False

        self.docEventHandler = None
        self.blockEventHandler = None
        self.ignore_pattern_list = [
                "about/contribute/translations/add_language.po"
                ]
        self.is_case_sensitive = False

    def start(self, from_vi_po, to_vi_po, out_file, is_compare_only):
        self.from_vi_po = from_vi_po
        self.to_vi_po = to_vi_po
        self.out_vi_po = out_file
        self.is_compare_only = (True if (is_compare_only) else False)

    def setHandlers(self, doc_handler, block_handler):
        self.docEventHandler = doc_handler
        self.blockEventHandler = block_handler
        self.docEventHandler.setCallBack(self.blockEventHandler)

    def isIgnore(self, file_path) -> bool:
        has_ignore = (len(self.ignore_pattern_list) > 0)
        if (not has_ignore):
            return False

        is_ignore = False
        for ignore_pattern in self.ignore_pattern_list:
            if (self.is_case_sensitive):
                is_ignore = (re.search(ignore_pattern, file_path) != None)
            else:
                is_ignore = (re.search(ignore_pattern, file_path, re.I) != None)
            if (is_ignore):
                return True
        return False

    def processingFilePair(self):

        from_po_doc = to_po_doc = None

        has_from = (self.from_vi_po != None)
        has_to = (self.to_vi_po != None)

        #print("processingFilePair: has_from={}, has_to={}".format(has_from, has_to))

        if (has_from):
            from_po_doc = Document(self.from_vi_po)
            from_po_doc.loadPOText()
            #print(from_po_doc)

        if (has_to):
            to_po_doc = Document(self.to_vi_po)
            to_po_doc.loadPOText()
            #print(to_po_doc)

        if ((self.docEventHandler != None) and isinstance(self.docEventHandler, TwoDocumentAction)):
            self.docEventHandler.setArgs(from_po_doc, to_po_doc)
            self.docEventHandler.run()

        #if (po_doc.isDirty()): print(po_doc)
        if (has_to and to_po_doc.isDirty()):
            if (self.out_vi_po == None):
                print("Saving changes to:{}".format(to_po_doc.path))
                to_po_doc.saveText(out_path=None)
            else:
                print("Saving changes to otherfile:{}".format(self.out_vi_po))
                to_po_doc.saveText(out_path=self.out_vi_po)

    def binarySearchFile(self, path_entry : str, sorted_file_list : list):
        found_index = bisect_left(sorted_file_list, path_entry)
        hi = len(sorted_file_list)
        is_valid_index = (found_index >= 0) and (found_index < hi)
        if (is_valid_index):
            found_entry = sorted_file_list[found_index]
            is_found = (found_entry == path_entry)
            #print("list:{}\nsearching:{}, found_index:{}, found_entry:{}".format(sorted_file_list, path_entry, found_index, found_entry))
            #exit(1)

            if (is_found):
                return found_entry
        return None

    def loadPOFilesForProcessing(self):
        from_path = self.from_vi_po
        to_path = self.to_vi_po

        has_from = (from_path != None)
        has_to = (to_path != None)

        is_dir_mode = (has_from and os.path.isdir(self.from_vi_po)) or (has_to and os.path.isdir(self.to_vi_po))

        if (not is_dir_mode):
            print("File mode : from_file: {} to_file: {} ".format(self.from_vi_po, self.to_vi_po))
            self.processingFilePair()
        else:
            print("Dir mode : from_file: {} to_file: {} ".format(self.from_vi_po, self.to_vi_po))

            from_po_dir_list_sorted = None
            to_po_dir_list_sorted = None

            if (has_from):
                from_getter = POBasic(self.from_vi_po, False)
                from_po_dir_list_sorted = from_getter.getSortedPOFileListRelative()

            if (has_to):
                to_getter = POBasic(self.to_vi_po, False)
                to_po_dir_list_sorted = to_getter.getSortedPOFileListRelative()

            has_both = (has_from and has_to)
            if (has_both):
                for(index, from_vi_po_file) in enumerate(from_po_dir_list_sorted):
                    if (len(from_vi_po_file) <= 0):
                        continue

                    if (self.isIgnore(from_vi_po_file)):
                        continue

                    to_vi_po_file = self.binarySearchFile(from_vi_po_file, to_po_dir_list_sorted)
                    is_found = (to_vi_po_file != None)
                    if (not is_found):
                        print("self.binarySearchFile: from_vi_po_file:{} to_vi_po_file:{}".format(from_vi_po_file, to_vi_po_file))
                        continue

                    self.from_vi_po = os.path.join(from_path, from_vi_po_file)
                    self.to_vi_po = os.path.join(to_path, to_vi_po_file)
                    self.processingFilePair()

            elif (has_from):
                for(index, from_vi_po_file) in enumerate(from_po_dir_list_sorted):
                    if (len(from_vi_po_file) <= 0):
                        continue

                    if (self.isIgnore(from_vi_po_file)):
                        continue

                    self.from_vi_po = os.path.join(from_path, from_vi_po_file)
                    self.to_vi_po = None
                    self.processingFilePair()

            elif (has_to):
                for(index, to_vi_po_file) in enumerate(to_po_dir_list_sorted):
                    if (len(to_vi_po_file) <= 0):
                        continue

                    if (self.isIgnore(to_vi_po_file)):
                        continue

                    self.from_vi_po = None
                    self.to_vi_po = os.path.join(to_path, to_vi_po_file)
                    self.processingFilePair()

    def makeDictionary(self, po_path) -> dict:
        from_path = po_path
        has_path = (po_path != None) and (os.path.isdir(po_path))

        if (not has_path):
            return

        master_dict = {}
        print("makeDictionary from: {}".format(from_path))

        from_getter = POBasic(from_path, False)
        from_po_dir_list_sorted = from_getter.getSortedPOFileListRelative()

        for(index, to_vi_po_file) in enumerate(from_po_dir_list_sorted):
            if (len(to_vi_po_file) <= 0):
                continue

            to_vi_po = os.path.join(po_path, to_vi_po_file)
            po_doc = Document(to_vi_po)
            po_doc.loadPOText()
            translated_dict = po_doc.getDictionary()
            master_dict.update(translated_dict)

        print("number of dict items: {}".format(len(master_dict)))
        return master_dict


    def run(self):
        doc_x = DiffTwoDocumentAction()
        doc_x.setCompareOnly(self.is_compare_only)

        block_event_handler = None
        #block_event_handler = FindUntranslatedSectionTitle()
        #block_event_handler = DiffMSGID()
        block_event_handler = CompareMSGID()
        #block_event_handler = BlankMessage()
        #block_event_handler = TransferMSGSTR()
        #block_event_handler.setTransferChanges()
        #block_event_handler = CompareMSGCTXT()
        #block_event_handler = SetFuzzy()
        #block_event_handler = RemoveMSGSTRIfSameWithMSGID()
        #block_event_handler = CopyMSGID_to_MSGSTR()
        #block_event_handler = EndingColon()
        #block_event_handler = TransferDictionaryToMSGSTR()
        #block_event_handler = TranslateTODO()
        self.setHandlers(doc_x, block_event_handler)

        #dictionary = self.makeDictionary(self.to_vi_po)
        #block_event_handler.setDictionary(dictionary)

        self.loadPOFilesForProcessing()



parser = ArgumentParser()
parser.add_argument("-f", "--from", dest="from_po_vi", help="the source vi.po file")
parser.add_argument("-t", "--to", dest="to_po_vi", help="the target vi.po file")
parser.add_argument("-o", "--out", dest="out_po_vi", help="the actual file to write to")
parser.add_argument("-c", "--compare_only", dest="compare_only", help="Compare only to see if document pairs are different.", action='store_true')

args = parser.parse_args()

print("args: {}".format(args))

x = CompareViPo()
x.start(args.from_po_vi, args.to_po_vi, args.out_po_vi, args.compare_only)
x.run()
