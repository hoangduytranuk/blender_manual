#!/usr/bin/python3 -d
import sys
import os
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
import re


class RemoveComments(BaseFileIO):
    def __init__(self):
        self.po_dir = None

    def start(self, po_dir):
        self.po_dir = po_dir
        
    def removeCommentedLine(self, text_list):
        new_list=[]
        for (index, text_line) in enumerate(text_list):
            found = re.search(Common.RE_COMMENTED_LINE, text_line)
            if (found == None):
                new_list.append(text_line)
        return new_list

    def removeComments(self):

        getter = POBasic(self.po_dir, False)
        po_dir_list = getter.getSortedPOFileList()

        p = re.compile(Common.COMMENTED_LINE)
        update_count=0
        for(index, po_file_path) in enumerate(po_dir_list):
            if (len(po_file_path) <= 0):
                continue

            read_text = self.readFile(po_file_path)
            if (read_text == None):
                raise Exception("Unable to read text from file: {}".format(self.path))

            m = p.search(read_text)
            if (m == None):
                continue

            print("doc: {}".format(po_file_path))

            po_doc = Document(po_file_path)
            po_doc.loadText()
            po_doc.cleanupEmpties()

            print("po_doc: {}".format(po_doc.getTextWithIDFlat()))
            po_doc.saveText()
            update_count += 1
            #if (update_count > 2):
            #    return

            #self.writeListToFile("/home/htran/back.txt", po_doc)



            #if (po_doc.isDirty()): po_doc.saveText()

        #if (vi_po_doc.isDirty()): vi_po_doc.saveText()
        
            

parser = ArgumentParser()
parser.add_argument("-p", "--po", dest="po_dir", help="The PO directory from where repeat terms are extracted.")
args = parser.parse_args()

#print("args: {}".format(args))

x = RemoveComments()
x.start(args.po_dir)
x.removeComments()
