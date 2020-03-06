#!/usr/bin/python3 -d
import sys
sys.path.append('/home/htran/bin/python/base')
sys.path.append('/home/htran/bin/python/PO')
sys.path.append('/home/htran/bin/python/event')
sys.path.append('/home/htran/bin/python/algorithm')

from basefileio import BaseFileIO
from common import Common
from potextblock import TextBlock
from potextcomponent import TextBlockComponent
from podocument import Document

from pobase import POBasic
from algorithms import Algo

from argparse import ArgumentParser


class CheckChanges(BaseFileIO):
    def __init__(self):
        self.target_dir = None

    def Start(self, target_dir):
        self.target_dir = target_dir

    def listMSGID(self):
        getter_from = POBasic(self.target_dir, False)
        target_dir_list = getter_from.getSortedPOFileList()
        for(index, file_name) in enumerate(target_dir_list):            
            po_doc = Document(file_name)            
            po_doc.loadText()            
            po_doc.printTitleOnce()
            print("{}\n\n".format(po_doc.getTextWithIDFlat()))
            #exit(1)
            #print("{}\n\n".format(po_doc.getTextWithIDFlat()))
            



parser = ArgumentParser()
parser.add_argument("-d", "--dir", dest="target_dir", help="The PO directory from which PO files are search and find.")
args = parser.parse_args()

#print("args: {}".format(args))

x = CheckChanges()
x.Start(args.target_dir)
x.listMSGID()

