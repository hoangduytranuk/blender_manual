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

from action import BasicDocumentAction, DocumentAction
from pobase import POBasic
from algorithms import Algo

from argparse import ArgumentParser
import collections    
import json
import re
from langdetect import detect

import docutils.nodes
import docutils.parsers.rst
import docutils.utils

REPEAT_DOC_FILE="/home/htran/msgid_po.po"
end_char_list=set(['.','!',')', ',', '>', ':','*','`',])
COMMENT_FLAG="#: "
LANGUAGE_SEPARATOR=" -- "


class RSTVisitor(docutils.nodes.NodeVisitor):
    def visit_reference(self, node: docutils.nodes.reference) -> None:
        """Called for "reference" nodes."""
        print(node)
    
    def unknown_visit(self, node: docutils.nodes.Node) -> None:
        """Called for all other node types."""
        pass


class DefaultComparator:

    def compare(self, x, y):
        if (x == y):
            return 0
        elif (x < y):
            return -1
        else:
            return 1


class CheckAndIncludeMSGID:
    def __init__(self):
        self.vi_po_doc = None
        self.rst_doc = None
    
    def setArgs(self, text_block):
        self.text_block = text_block

    def setVIPODoc(self, vi_po_doc):
        self.vi_po_doc = vi_po_doc


    def reorganiseText(self, text_line):
        is_empty = (text_line == None or len(text_line.strip()) < 1)
        if (is_empty):
            return None
        
        index_of_sep = text_line.find(LANGUAGE_SEPARATOR)
        is_found = (index_of_sep > 0)
        if (not is_found):
            return None
        
        left_part = text_line[:index_of_sep]
        right_index = index_of_sep + len(LANGUAGE_SEPARATOR)
        right_part = text_line[right_index:]
        
        try:
            lang_code_left = detect(left_part)
            lang_code_right = detect(right_part)
        except Exception as e:
            return None
                    
        leading_part = (left_part if (lang_code_left == 'vi') else right_part)
        tailing_part = (right_part if (lang_code_right != 'vi') else left_part)
        is_same = (leading_part == tailing_part)
        if (is_same):
            return None
        
        reorganised_text = "{}{}{}".format(leading_part, LANGUAGE_SEPARATOR, tailing_part)
        return reorganised_text
        
    def run(self):
        msgstr = self.text_block.msgstr
        msgstr_flat_text = msgstr.flatText()

        has_translation = (len(msgstr_flat_text) > 1)
        if (not has_translation): return

        msgid = self.text_block.msgid
        msgid_flat_text = msgid.flatText()
        document = self.text_block.document

        reorganised_text = self.reorganiseText(msgstr_flat_text)
        
        is_changed = (reorganised_text != None and reorganised_text != msgstr_flat_text)        
        if (not is_changed): return
        
        
        document.printTitleOnce()
        print("Old:\n{}\n".format(self.text_block.getTextWithID()))
        msgstr.setText(reorganised_text)
        document.setDirty()
        print("New:\n{}\n".format(self.text_block.getTextWithID()))


class IncludeEnglish(BaseFileIO):
    def __init__(self):
        self.po_dir = None
        self.vi_po_path = None
        self.rst_dir = None
        
    def start(self, po_dir, rst_dir, vi_po_file):
        self.po_dir = po_dir
        self.rst_dir = rst_dir
        self.vi_po_path = vi_po_file

    def setHandlers(self, doc_handler, block_handler):
        self.docEventHandler = doc_handler
        self.blockEventHandler = block_handler
        self.docEventHandler.setCallBack(self.blockEventHandler)

    def ProcessingDir(self):

        getter = POBasic(self.po_dir, False)
        po_dir_list = getter.getSortedPOFileList()        
                
        for(index, po_file_path) in enumerate(po_dir_list):
            if (len(po_file_path) <= 0):
                continue
            
            self.vi_po_path = po_file_path
            self.ProcessingFile()

    def ProcessingFile(self):

        po_doc = Document(self.vi_po_path)
        po_doc.loadText()

        if ((self.docEventHandler != None) and isinstance(self.docEventHandler, DocumentAction)):
            self.docEventHandler.setArgs(po_doc)
            self.docEventHandler.run()

        #if (po_doc.isDirty()): print(po_doc)
        if (po_doc.isDirty()): po_doc.saveText()


    def run(self):
        # doc_x = BasicDocumentAction()
        # block_event_handler = CheckAndIncludeMSGID()
        # self.setHandlers(doc_x, block_event_handler)
        #
        # if (self.vi_po_path != None):
        #     self.ProcessingFile()
        # else:
        #     self.ProcessingDir()

        getter = POBasic(self.rst_dir, False)
        rst_dir_list : list = getter.getSortedRSTFileList()

        for (index, rst_file_path) in enumerate(rst_dir_list):
            if (len(rst_file_path) <= 0):
                continue

            self.vi_po_path = rst_file_path
            #self.ProcessingFile()
            self.walkRSTDoc(rst_file_path)

    def loadVIPO(self):
        vi_po_doc = Document(self.vi_po_path)
        vi_po_doc.loadText()
        vi_po_doc.sortDocumentInMSGID()
        return vi_po_doc


    def parseRST(self, text_read: str) -> docutils.nodes.document:
        parser = docutils.parsers.rst.Parser()
        components = (docutils.parsers.rst.Parser,)
        settings = docutils.frontend.OptionParser(components=components).get_default_values()
        document = docutils.utils.new_document('<rst-doc>', settings=settings)
        parser.parse(text_read, document)
        return document

    def walkRSTDoc(self, doc_path: str):
        load_text = self.readFile(doc_path)
        doc = self.parseRST(load_text)
        visitor = RSTVisitor(doc)
        doc.walk(visitor)
    

parser = ArgumentParser(
    description=""
    "Ensure that all MSGSTR entries containing \" -- \", with English/Vietnamese parts "
    "in if they are section titles, ie. \"Tiếng Việt -- Vietnamese\""
    , 
    epilog="If -p directory provided then process that first, else using the -v to process a single file."
    )
if (len(sys.argv) < 2):
    parser.print_usage()
    sys.exit(1)

parser.add_argument("-p", "--po", dest="po_dir", help="The PO directory from where all PO files are found.")
parser.add_argument("-r", "--rst", dest="rst_dir", help="The RST directory from where all RST files are found.")
parser.add_argument("-v", "--pofile", dest="po_file", help="Path to individual PO file to which all text with '--' separator between VN/EN are swapped.")
args = parser.parse_args()

#print("args: {}".format(args))


x = IncludeEnglish()
x.start(args.po_dir, args.rst_dir, args.po_file)
x.run()

