#!/usr/bin/python3 -d
"""
"""
import os
import sys
sys.path.append('/home/htran/bin/python/base')
sys.path.append('/home/htran/bin/python/PO')
sys.path.append('/home/htran/bin/python/event')
sys.path.append('/home/htran/bin/python/algorithm')
sys.path.append('/home/htran/bin/python')

from basefileio import BaseFileIO
from common import Common
from potextblock import TextBlock
from potextcomponent import TextBlockComponent
from podocument import Document

from action import BasicDocumentAction, DocumentAction, TwoDocumentAction
from pobase import POBasic
from algorithms import Algo

from argparse import ArgumentParser
import collections    
import json
import re
#from langdetect import detect

REPEAT_DOC_FILE="/home/htran/msgid_po.po"
class DefaultComparator:

    def compare(self, x, y) -> int:
        if (x == y):
            return 0
        elif (x < y):
            return -1
        else:
            return 1


class InsertDictionary:

    def __init__(self):
        self.po_doc: Document = None
        self.dict_doc: Document = None
        self.vipo_doc: Document = None
        self.text_block: TextBlock = None
        self.non_trans_p = re.compile(Common.RE_NONTRANS)
        self.has_kbd_p = re.compile(Common.RE_HA_KEYBOARD)
        self.my_list={}

    def setArgs(self, text_block: TextBlock):
        self.text_block: TextBlock = text_block

    def setDictionary(self, dict_doc: Document):
        self.dict_doc = dict_doc

    def setVIPODoc(self, vipo_doc: Document):
        self.vipo_doc = vipo_doc


    def run(self):

        has_dictionary = (self.dict_doc != None) and (not self.dict_doc.isEmpty())
        has_vipo = (self.vipo_doc != None) and (not self.vipo_doc.isEmpty())
        do_not_have_reference = (not has_dictionary) and (not has_vipo)

        if (do_not_have_reference):
            raise Exception("Doesn't have any dictionary reference sources or that they are empty.")

        document = self.text_block.document

        po_msgstr = self.text_block.msgstr
        po_msgstr_text = po_msgstr.flatText()

        is_debug = (po_msgstr_text.find("duplicate of this data-block") >= 0)
        if (is_debug):
            print("po_msgstr_text:{}".format(po_msgstr_text))
            exit(1)

        # keyboard_part = ""
        # m = self.has_kbd_p.match(po_msgstr_text)
        # has_kbd = (m != None)
        # if (has_kbd):
        #     index = po_msgstr_text.index(Common.COLLON)
        #     left_part = po_msgstr_text[:index]
        #     keyboard_part = po_msgstr_text[index:]
        #     term1 = left_part.strip().replace(" -- ", "")
        #     term = term1.strip().replace("-- ", "")
        # else:
        #     term1 = po_msgstr_text.strip().replace(" -- ", "")
        #     term = term1.strip().replace("-- ", "")
        #
        # is_ignore = (term in ignore_list)
        # if (is_ignore):
        #     return
        #
        # from_vipo = False
        # from_dict = False
        #
        # dict_entry = None
        # if (has_vipo):
        #     dict_entry = self.vipo_doc.binarySearchText(term)
        #     from_vipo = (dict_entry != None)
        #
        # is_check_dict = (not from_vipo and has_dictionary)
        # if (is_check_dict):
        #     dict_entry = self.dict_doc.binarySearchText(term)
        #     from_dict = (dict_entry != None)
        #
        # # if (is_debug):
        # #     print("[{}] from_vipo:{}, from_dict:{}".format(term, from_vipo, from_dict))
        # #     exit(1)
        #
        # found_translation = (dict_entry != None)
        #
        # if (not found_translation):
        #     return
        #
        # translation_term = dict_entry.msgstr.flatText()
        # is_ignore = (translation_term == term)
        # if (is_ignore):
        #     return
        #
        # if (from_vipo):
        #     document.printTitleOnce()
        #     #print("from:\n{}".format(self.text_block))
        #     has_keyboard = (len(keyboard_part) > 0)
        #     if (has_keyboard):
        #         is_insert_keyboard_part_for_translation = Common.isValidKeyboardShortCut(keyboard_part)
        #         if (is_insert_keyboard_part_for_translation):
        #             replace_text = "{} {} -- {} {}".format(translation_term, keyboard_part, term, keyboard_part)
        #         else:
        #             replace_text = "{} -- {} {}".format(translation_term, term, keyboard_part)
        #     else:
        #         replace_text = "{} -- {}".format(translation_term, term)
        #
        #     # if (is_debug):
        #     #     print("po_msgstr_text:[{}], keyboard:[{}], found_translation:{}, from_vipo:{}, from_dict:{}".format(
        #     #             term, keyboard_part, translation_term, from_vipo, from_dict))
        #     #     exit(1)
        #
        #     self.text_block.msgstr.setText(replace_text)
        #     document.setDirty()
        #     print("from VIPO:\n{}".format(self.text_block))
        # elif (from_dict):
        #     m = self.non_trans_p.match(translation_term)
        #     is_ignore = (m != None) or (len(translation_term) < 1)
        #     if (is_ignore):
        #         return
        #
        #     #print("find:[{}], trans:[{}]".format(term, translation_term))
        #     document.printTitleOnce()
        #     #print("from:\n{}".format(self.text_block))
        #     has_embedded_text = (translation_term.find(term) >= 0)
        #     if (has_embedded_text):
        #         replace_text = translation_term
        #     else:
        #         replace_text = "{} -- {}".format(translation_term, term)
        #     self.text_block.msgstr.setText(replace_text)
        #     document.setDirty()
        #     print("from DICT:\n{}".format(self.text_block))


class SwapVietnameseEnglish:
    def __init__(self):
        self.po_doc : Document = None
        self.rst_doc : Document = None
        self.dict_doc : Document = None        
        self.change_count = 0
        
    def setArgs(self, text_block : TextBlock):
        self.text_block : TextBlock = text_block

    def setRSTDoc(self, rst_doc : Document):
        self.rst_doc = rst_doc

    def setDictionary(self, dict_doc : Document):
        self.dict_doc = dict_doc

    def setVIPODoc(self, vipo_doc: Document):
        self.vipo_doc = vipo_doc

    def reorganiseText(self, text_line : str):
        is_empty = (text_line == None or len(text_line.strip()) < 1)
        if (is_empty):
            return None
                
        index_of_sep = text_line.find(Common.LANGUAGE_SEPARATOR)
        is_found = (index_of_sep > 0)
        if (not is_found):
            return None
        
        left_part = text_line[:index_of_sep]
        right_index = index_of_sep + len(Common.LANGUAGE_SEPARATOR)
        right_part = text_line[right_index:]

        lang_code_left = None
        lang_code_right = None
        
        #try:
            #lang_code_left = detect(left_part)
            #lang_code_right = detect(right_part)
        #except Exception as e:
            #return None
                    
        leading_part = (left_part if (lang_code_left == 'vi') else right_part)
        tailing_part = (right_part if (lang_code_right != 'vi') else left_part)
        is_same = (leading_part == tailing_part)
        if (is_same):
            return None
        
        reorganised_text = "{}{}{}".format(leading_part, LANGUAGE_SEPARATOR, tailing_part)
        return reorganised_text


    def hasRSTEntry(self):
        msgid_text = self.text_block.msgid.flatText()
#        is_debug = (msgid_text.find("Min X/Y and Max X/Y") >= 0)
#        if (is_debug):
#            print("def run(self): self.text_block={}".format(self.text_block))
#            exit(1)
            
        found_rst_entry = self.rst_doc.binarySearchMSGID(self.text_block)
        is_found = (found_rst_entry != None)
        return [is_found, found_rst_entry]

    def isIgnored(self, found_rst_entry):
        document = self.text_block.document
        
        po_msgid_text = self.text_block.msgid.flatText()
        po_msgstr_text = self.text_block.msgstr.flatText()
        rst_msgid = found_rst_entry.msgid
        rst_msgid_text = rst_msgid.flatText()

        is_ignore_msgid = Common.isIgnored(po_msgid_text)
        is_ignore_start_with = Common.isIgnoredIfStartsWith(po_msgstr_text)

        is_included_po_msgid = Common.isMustIncludedKeyboardPart(po_msgid_text)
        is_included_rst_msgid = Common.isMustIncludedKeyboardPart(rst_msgid_text)
                        
        has_translation = (len(po_msgstr_text) > 0)        
        has_key_board_part = (is_included_po_msgid or is_included_rst_msgid)
        
        is_ignore = (
                    is_ignore_msgid or \
                     is_ignore_start_with or \
                     has_translation) and \
                    (not has_key_board_part)

#        is_debug = (po_msgid_text == "Opensubdiv")
#        if (is_debug):
#            print("po_msgid_text: [{}],  "
#                  "is_ignore_msgid:{}, " 
#                  "is_ignore_rst:{}, "
#                  "has_translation:{}, ".
#                  format(po_msgid_text,
#                         is_ignore_msgid,
#                         is_ignore_rst,
#                         has_translation
#                         ))
        if (not is_ignore):
            document.printTitleOnce()
            #print("NOT isIgnored - rst_msgid_text: {}, is_ignore_msgid:{}, is_ignore_start_with:{}, has_translation:{}, po_msgstr_text:{}".format(rst_msgid_text, is_ignore_msgid, is_ignore_start_with, has_translation, po_msgstr_text))
        return [is_ignore, rst_msgid_text]

    def hasDoneBefore(self):
        po_msgstr = self.text_block.msgstr
        po_msgstr_text = po_msgstr.flatText()
        
        is_done_before = (len(po_msgstr_text) > 0)

        return [is_done_before, po_msgstr_text]

    def hasTranslation(self, found_rst_entry):

        has_dict = (self.dict_doc != None)
        has_vipo = (self.vipo_doc != None)
        
        has_translation = False
        has_vipo_translation = False
        has_rst_entry = False
        dict_entry = None
        if (has_vipo):
            dict_entry = self.vipo_doc.binarySearchMSGID(found_rst_entry)
            has_vipo_translation = (dict_entry != None) and (not dict_entry.msgstr.isEmpty())
                 
        if (has_dict and (not has_translation)):
            dict_entry = self.dict_doc.binarySearchMSGID(found_rst_entry)
            has_rst_entry = (dict_entry != None)

        has_translation = (has_vipo_translation or has_rst_entry)
#         if (has_translation):
#             document = (self.vipo_doc if (has_vipo_translation) else self.dict_doc)
#             document.printTitleOnce()
#             print("dict_entry: [{}]".format(dict_entry.getTextWithID()))

        return [has_translation, dict_entry]

    def ReplaceIfHasTranslation(self, dict_entry : TextBlock, rst_msgid_text : str):
        if (dict_entry == None):
            return
        
        document = self.text_block.document
        document.printTitleOnce()

        #print("ReplaceIfHasTranslation: dict_entry:{}".format(dict_entry))
        is_msgstr_empty = dict_entry.msgstr.isEmpty()
        if (is_msgstr_empty):
            dict_msgstr_text = rst_msgid_text
        else:
            dict_msgstr = dict_entry.msgstr
            dict_msgstr_text = dict_msgstr.flatText()

        po_text_msgid = self.text_block.msgid.flatText()
        po_text_msgstr = self.text_block.msgstr.flatText()

        is_repeat = (dict_msgstr_text == po_text_msgid)
        if (is_repeat):
            return

        #
        is_empty = len(dict_msgstr_text) < 1
        if (is_empty):
            dict_msgstr_text = rst_msgid_text

        translated_text = "-- {}".format(po_text_msgid)
        is_translated_text = (dict_msgstr_text.find(translated_text) >= 0)

        if (is_translated_text):
            replacing_text = dict_msgstr_text
        else:
            replacing_text = (dict_msgstr_text if Common.startWithHyphen(dict_msgstr_text) else "-- {}".format(dict_msgstr_text))

        #print("dict_msgstr_text:[{}], replacing_text:[{}]".format(dict_msgstr_text, replacing_text))

        self.text_block.msgstr.setText(replacing_text)
        document.setDirty()
        self.change_count += 1
        print("Using Dictionary:{}\n{}\n".format(self.change_count,self.text_block.getTextWithID()))


    def ReplaceIfDoNotHasTranslation(self, po_msgstr_text, rst_msgid_text):
        
        document = self.text_block.document

        is_repeat = (po_msgstr_text.find(rst_msgid_text) >= 0)
        if (is_repeat):
            return

        # is_alpha = Common.isLeadingAlpha(rst_msgid_text)
        # if (not is_alpha):
        #     return
        #
        #print("po_msgstr_text:[{}], rst_msgid_text:[{}]".format(po_msgstr_text, rst_msgid_text))

        is_leading_with_dash = Common.isLeadingWithHyphen(po_msgstr_text)
        replacing_text = (rst_msgid_text if (is_leading_with_dash) else "-- {}".format(rst_msgid_text))
        replacing_text = replacing_text.lstrip()
        #document.printTitleOnce()
        #print("po_msgstr_text:[{}], replacing_text:[{}]".format(po_msgstr_text, replacing_text))

        self.text_block.msgstr.setText(replacing_text)
        document.setDirty()
        self.change_count += 1
        print("New:{}\n{}\n".format(self.change_count, self.text_block.getTextWithID()))

    def ReorganiseReplaceText(self, po_msgstr_text):
        document = self.text_block.document
        # print("found po:{}, rst:{}".format(self.text_block, found_rst_entry))
        reorganised_text = self.reorganiseText(po_msgstr_text)
        is_changed = (reorganised_text != None and reorganised_text != po_msgstr_text)
        if (not is_changed):
            return

        document.printTitleOnce()
        # print("Old:\n{}\n".format(self.text_block.getTextWithID()))
        msgstr.setText(reorganised_text)
        document.setDirty()
        self.change_count += 1
        print("Reorganised:{}\n{}\n".format(self.change_count,self.text_block.getTextWithID()))

    def run(self):
        document = self.text_block.document
        is_found, found_rst_entry = self.hasRSTEntry()
        if (not is_found):
            return

        is_ignore, rst_msgid_text = self.isIgnored(found_rst_entry)
        if (is_ignore):
            #print("Ignoring: {}".format(rst_msgid_text))
            return
        
        is_done_before, po_msgstr_text = self.hasDoneBefore()

#        is_debug = (rst_msgid_text.find("Min X/Y and Max X/Y") >= 0)
#        if (is_debug):
#             print("rst_msgid_text:[{}], po_msgstr_text:[{}]".format(rst_msgid_text, po_msgstr_text))
#             exit(1)

        is_replacing = (not is_done_before)
        if (is_replacing):
            has_translation, dict_entry = self.hasTranslation(found_rst_entry)
            # if (is_debug):
            #     print("debug: dict_entry:[{}], found_rst_entry:[{}]".format(found_rst_entry, found_rst_entry))
            if (has_translation):
                self.ReplaceIfHasTranslation(dict_entry, rst_msgid_text)
            else:
                self.ReplaceIfDoNotHasTranslation(po_msgstr_text, rst_msgid_text)
        else:
            self.ReorganiseReplaceText(po_msgstr_text)


class SwapPosition(BaseFileIO):
    def __init__(self):
        self.po_dir = None
        self.rst_dir = None
        self.vipo_path = None
        self.dictionary_path = None
        self.vipo_doc = None
        self.dictionary_doc = None
        self.out_vi_po = None

    def start(self, po_dir, rst_path, vipo_path, dictionary_path, out_file):
        self.po_dir = po_dir
        self.rst_dir = rst_path
        self.vipo_path = vipo_path
        self.dictionary_path = dictionary_path
        self.out_vi_po = out_file

    def setHandlers(self, doc_handler, block_handler):
        self.docEventHandler = doc_handler
        self.blockEventHandler = block_handler
        self.docEventHandler.setCallBack(self.blockEventHandler)


    def fixPath(self, old_path : str) -> str:
        new_path = old_path
        do_not_has_sep = (not old_path.endswith(os.sep))
        if (do_not_has_sep):
            new_path = old_path + os.sep
        return new_path
    
    def changeExtension(self, old_file, from_ext:str, to_ext:str) -> str:
        new_file = old_file
        left, mid, right = old_file.rpartition(Common.DOT)
        #print("left:{}, mid:{}, right:{}".format(left, mid, right))
        is_found = (right in from_ext)
        if (is_found):                        
            new_file = left + to_ext
        return new_file
        
    def loadDictionary(self):
        if (self.vipo_path != None):
            self.vipo_doc = Document(self.vipo_path)
            self.vipo_doc.loadText()
            self.vipo_doc.sortDocumentInMSGID()

        if (self.dictionary_path != None):
            self.dictionary_doc = Document(self.dictionary_path)
            self.dictionary_doc.loadText()
            self.dictionary_doc.sortDocumentInMSGID()



        # has_dictionary = (self.vipo_doc != None) or (self.dictionary_doc != None)
        # if (not has_dictionary):
        #     return
        #
        # is_merging = (self.vipo_doc != None) and (self.dictionary_doc != None)
        # if (not is_merging):
        #     dict_doc = (self.vipo_doc if (self.vipo_doc != None) else self.dictionary_doc)
        #     self.dictionary_doc = dict_doc
        #     return
        #
        # #merging both
        # self.dictionary_doc.mergeDoc(self.vipo_doc)
        # #print(self.dictionary_doc)
        # #exit(1)
        
    def ProcessingDir(self):

        po_dir = self.fixPath(self.po_dir)
        rst_dir = self.fixPath(self.rst_dir)

        getter = POBasic(po_dir, False)
        po_dir_list = getter.getSortedPOFileListRelative()        
            
        for(index, po_file_path) in enumerate(po_dir_list):
            if (len(po_file_path) <= 0):
                continue

            po_full_path = os.path.join(po_dir, po_file_path)
            po_doc : Document = Document(po_full_path)
            po_doc.loadText()
            #print(po_doc)
            #exit(1)

            rst_file = self.changeExtension(po_file_path, Common.PO_EXT, Common.RST_EXT)
            rst_full_path = os.path.join(rst_dir, rst_file)
            #print("po_full_path:{}, rst_full_path:{}".format(po_full_path, rst_full_path))
            is_rst_file_there = os.path.exists(rst_full_path)
            
            #print("file: {} is_rst_file_there:{}".format(rst_full_path, is_rst_file_there))
            if (not is_rst_file_there):
                print("NON-EXISTENCE File: {}".format(rst_full_path))
                continue
            #exit(1)
            rst_doc : Document = Document(rst_full_path)
            rst_doc.loadRSTText()
            if (rst_doc.isEmpty()): continue

            rst_doc.sortDocumentInMSGID()
            #rst_doc.printTitleOnce()
            #print(rst_doc)
            #if (index > 3):
            #exit(1)

            self.ProcessingTwoDoc(rst_doc, po_doc)

    def ProcessingTwoDoc(self, rst_doc:Document, po_doc:Document):

        self.blockEventHandler.setRSTDoc(rst_doc)
        self.blockEventHandler.setRSTDoc(rst_doc)
        if ((self.docEventHandler != None) and isinstance(self.docEventHandler, DocumentAction)):
            self.docEventHandler.setArgs(po_doc)
            self.docEventHandler.run()

        #if (po_doc.isDirty()): print(po_doc)
        if (po_doc.isDirty()):
            if (self.out_vi_po == None):
                print("Saving changes to:{}".format(po_doc.path))
                po_doc.saveText(out_path=None)
            else:
                print("Saving changes to otherfile:{}".format(self.out_vi_po))
                po_doc.saveText(out_path=self.out_vi_po)
            
            #print("Saving document:{}".format(po_doc.path))
            #po_doc.saveText()
            #key_input = input("Press anykey to continue")
            

    def ProcessingSingleDoc(self, po_doc:Document):

        if ((self.docEventHandler != None) and isinstance(self.docEventHandler, DocumentAction)):
            self.docEventHandler.setArgs(po_doc)
            self.docEventHandler.run()

        if (po_doc.isDirty()):
            if (self.out_vi_po == None):
                print("Saving changes to:{}".format(po_doc.path))
                po_doc.saveText(out_path=None)
            else:
                print("Saving changes to otherfile:{}".format(self.out_vi_po))
                po_doc.saveText(out_path=self.out_vi_po)
            
            #print("Saving document:{}".format(po_doc.path))
            #po_doc.saveText()


    def ProcessingWithDictionary(self):
        po_dir = self.fixPath(self.po_dir)
        getter = POBasic(po_dir, False)
        po_dir_list = getter.getSortedPOFileListRelative()

        for (index, po_file_path) in enumerate(po_dir_list):
            if (len(po_file_path) <= 0):
                continue

            po_full_path = os.path.join(po_dir, po_file_path)
            po_doc: Document = Document(po_full_path)
            po_doc.loadText()

            self.ProcessingSingleDoc(po_doc)

    def run(self):
        
        self.loadDictionary()
        doc_x = BasicDocumentAction()

        has_rst = (self.rst_dir != None)
        if (has_rst):
            block_event_handler = SwapVietnameseEnglish()
            block_event_handler.setDictionary(self.dictionary_doc)
            block_event_handler.setVIPODoc(self.vipo_doc)
            self.setHandlers(doc_x, block_event_handler)

            self.ProcessingDir()
        else:
            block_event_handler = InsertDictionary()
            block_event_handler.setDictionary(self.dictionary_doc)
            block_event_handler.setVIPODoc(self.vipo_doc)
            self.setHandlers(doc_x, block_event_handler)

            self.ProcessingWithDictionary()

            #my_dict = block_event_handler.my_list
            #my_list = my_dict.keys()
            #sorted_list = sorted(my_list)
            #print(os.linesep.join(sorted_list))


        #if (self.rst_dir != None):
            #self.ProcessingFile()
        #else:
            #self.ProcessingDir()


    def loadVIPO(self):
        vi_po_doc = Document(self.rst_dir)
        vi_po_doc.loadText()
        vi_po_doc.sortDocumentInMSGID()
        return vi_po_doc


parser = ArgumentParser(
    description=""
    "Ensure that all MSGSTR entries containing \" -- \", with English/Vietnamese parts are "
    "swapped so Vietnamese is leading and English is trailing, eg."
    " \"Vietnamese -- Tiếng Việt\""
    " becomes "
    "\"Tiếng Việt -- Vietnamese\""
    , 
    epilog="If -p directory provided then process that first, else using the -v to process a single file."
    )
if (len(sys.argv) < 2):
    parser.print_usage()
    sys.exit(1)

parser.add_argument("-p", "--po", dest="po_dir", help="The PO directory from where all PO files are found.")
parser.add_argument("-r", "--rst", dest="rst_dir", help="The RST directory from where all RST files are found.")
parser.add_argument("-v", "--vipo", dest="vipo_file", help="The RST directory from where all RST files are found.")
parser.add_argument("-d", "--dict", dest="dic_file", help="The RST directory from where all RST files are found.")
parser.add_argument("-o", "--out", dest="out_po_vi", help="the actual file to write to")

args = parser.parse_args()

print("args: {}".format(args))


x = SwapPosition()
x.start(args.po_dir, args.rst_dir, args.vipo_file, args.dic_file, args.out_po_vi)
x.run()

