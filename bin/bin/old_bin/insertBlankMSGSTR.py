#!/usr/bin/python3 -d
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

class InsertBlankMSG:
    def __init__(self):
        self.vi_po_doc = None
        self.text_block = None;

    def setArgs(self, text_block):
        self.text_block = text_block

    def run(self):
        doc = self.text_block.document
        
        is_insert = self.text_block.msgstr.isEmpty()
        #print("{}:{}".format(self.text_block, is_insert))
        if (is_insert):
            doc.printTitleOnce()
            #print("from:{}".format(self.text_block))
            self.text_block.msgstr.setEmptyText()
            doc.setDirty()
            print("to:{}".format(self.text_block.getTextWithID()))
        

class InsertBlankMSGSTR(BaseFileIO):
    def __init__(self):
        self.po_dir = None
        self.docEventHandler = None
        self.blockEventHandler = None

    def start(self, po_dir):
        self.po_dir = po_dir

    def setHandlers(self, doc_handler, block_handler):
        self.docEventHandler = doc_handler
        self.blockEventHandler = block_handler
        self.docEventHandler.setCallBack(self.blockEventHandler)

    def loadPOFilesForProcessing(self):

        getter = POBasic(self.po_dir, False)
        po_dir_list = getter.getSortedPOFileList()        
                
        for(index, po_file_path) in enumerate(po_dir_list):
            if (len(po_file_path) <= 0):
                continue
            
            #print("{}\n{}".format(po_file_path, len(po_file_path) * "="))
            po_doc = Document(po_file_path)
            po_doc.loadText()

            if ((self.docEventHandler != None) and isinstance(self.docEventHandler, DocumentAction)):
                self.docEventHandler.setArgs(po_doc)
                self.docEventHandler.run()

            #if (po_doc.isDirty()): print(po_doc)
            #if (po_doc.isDirty()): print("Saving: {}".format(po_doc.path))
            if (po_doc.isDirty()): 
                po_doc.saveText()
                po_doc.msg("")
                key = input("Press any key to continue, Ctrl+C to break")


    def run(self):
        doc_x = BasicDocumentAction()
        block_event_handler = InsertBlankMSG()
        self.setHandlers(doc_x, block_event_handler)
        self.loadPOFilesForProcessing()


parser = ArgumentParser()
parser.add_argument("-p", "--po", dest="po_dir", help="The PO directory from where .po files are found.")
args = parser.parse_args()

print("args: {}".format(args))

x = InsertBlankMSGSTR()
x.start(args.po_dir)
x.run()

