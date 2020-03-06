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

from action import BasicTwoDocumentAction, TwoDocumentAction, TransferTextBlockAction
from pobase import POBasic
from algorithms import Algo

from argparse import ArgumentParser
import re
import os

class TransferMSGID_MSGSTR_If_Diff(TransferTextBlockAction):

    def run(self):
        to_doc = self.to_block.document
        
        from_msgid = self.from_block.msgid
        from_msgid_text = from_msgid.flatText()
        from_msgstr = self.from_block.msgstr
        from_msgstr_text = from_msgstr.flatText()
    
        to_msgid = self.to_block.msgid
        to_msgid_text = to_msgid.flatText()
        to_msgstr = self.to_block.msgstr
        to_msgstr_text = to_msgstr.flatText()
        
        is_diff_msgid = (from_msgid_text != to_msgid_text)
        is_diff_msgstr = (from_msgstr_text != to_msgstr_text)
        #print("from_msgid_text:[{}], to_msgid_text:[{}], is_diff_msgid:[{}]".format(from_msgid_text, to_msgid_text, is_diff_msgid))
        #print("from_msgid_text:[{}], to_msgid_text:[{}], is_diff_msgid:[{}]".format(from_msgstr_text, to_msgstr_text, is_diff_msgstr))
        if (is_diff_msgid):
            from_list : list = self.from_block.msgid.getList()
            self.to_block.msgid.setList(from_list)
            to_doc.setDirty()
            
        if (is_diff_msgstr):
            from_list : list = self.from_block.msgstr.getList()
            self.to_block.msgstr.setList(from_list)
            to_doc.setDirty()
            
        is_changed = (is_diff_msgid or is_diff_msgstr)
        if (is_changed):
            to_doc.printTitleOnce()
            print("{}".format(self.to_block))
        

class TransferContentOfPO(BaseFileIO):
    def __init__(self):
        self.from_dir = None
        self.to_dir = None

    def start(self, from_dir, to_dir):
        self.from_dir = from_dir
        self.to_dir = to_dir

    def setHandlers(self, doc_handler, block_handler):
        self.docEventHandler = doc_handler
        self.blockEventHandler = block_handler
        self.docEventHandler.setCallBack(self.blockEventHandler)

    def loadPOFilesForProcessing(self):
        
        getter : POBasic = POBasic(self.from_dir, False)
        from_po_dir_list : list = getter.getSortedPOFileList()

        from_dir_len : int =len(self.from_dir)
        #to_dir_len : int =len(self.to_dir)
        
        for(index, from_po_path) in enumerate(from_po_dir_list):
            is_ignore_dir : bool = (from_po_path == ".") or (from_po_path == "..")
            if (is_ignore_dir):
                continue
            
            common_part:str = from_po_path[from_dir_len:]
            is_leading_with_sep = common_part.startswith(os.sep)
            if (is_leading_with_sep):
                common_part = common_part[1:]
            
            to_po_path = os.path.join(self.to_dir, common_part)
            is_to_exists = os.path.exists(to_po_path)
            if (not is_to_exists):
                print("Target file doesn't exist: {}".format(to_po_path))
                continue

            from_po_doc = Document(from_po_path)
            to_po_doc = Document(to_po_path)
            from_po_doc.loadText()                        
            to_po_doc.loadText()            

            
            from_msgid = from_po_doc.getTextOnly()
            to_msgid = from_po_doc.getTextOnly()
            is_diff = (from_msgid != to_msgid)
            
            print("FROM:{}\n\nTO:{}\nis_diff:{}".format(from_msgid, to_msgid, is_diff))
            
            if (not is_diff): continue
            
        
            #print("{}\n{}".format(from_po_path, to_po_path))
            

            
            print("FROM:{}\n\nTO:{}".format(from_po_doc, to_po_doc))
            #exit(1)
#            if ((self.docEventHandler != None) and isinstance(self.docEventHandler, TwoDocumentAction)):
#                self.docEventHandler.setArgs(from_po_doc, to_po_doc)
#                self.docEventHandler.run()
#
#            if (to_po_doc.isDirty()):
#                print("SAVING DOCUMENT: {}".format(to_po_doc.path))
                #to_po_doc.saveText()
            #if (to_po_doc.isDirty()): to_po_doc.saveText()        


    def run(self):
        doc_x = BasicTwoDocumentAction()
        block_event_handler = TransferMSGID_MSGSTR_If_Diff()
        self.setHandlers(doc_x, block_event_handler)
        
        self.loadPOFilesForProcessing()



parser = ArgumentParser()
parser.add_argument("-f", "--from", dest="from_dir", help="the source po dir")
parser.add_argument("-t", "--to", dest="to_dir", help="the target po dir")
args = parser.parse_args()

#print("args: {}".format(args))

x = TransferContentOfPO()
x.start(args.from_dir, args.to_dir)
x.run()

