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
import os
import hashlib

"""
Run this line 

sphinx-intl update -p build/locale -l dd
findPOChanges.py -l $PWD/locale/dd/LC_MESSAGES -r $PWD/locale/vi/LC_MESSAGES

to find out if MSGID has been changed
"""

class CheckChanges(BaseFileIO):
    def __init__(self):
        self.left_dir : str = None
        self.right_dir : str = None
        self.is_fix : bool = False

    def setVars(self, left_dir : str, right_dir : str, is_fix : str):
        self.left_dir = left_dir
        self.right_dir = right_dir
        self.is_fix = (is_fix != None) and (is_fix.lower() == "true")

    def transferText(self, left_doc, right_doc, is_save=False):
        #print("left_doc:\n{}\n".format(left_doc))
        #print("right_doc:\n{}\n".format(right_doc))
        right_doc_clone : Document = right_doc.clone()
        right_doc_clone.sortDocumentInMSGID()

        for(index, left_text_block) in enumerate(left_doc.block_list):
            is_first_block = (index == 0)
            if (is_first_block): continue

            right_text_block = right_doc_clone.binarySearchMSGID(left_text_block)
            #print("right_text_block:{}".format(right_text_block))

            is_found = (right_text_block != None)
            if (not is_found):
                right_doc_clone.printTitleOnce()
                raise Exception("Block not found: [{}]".format(left_text_block.getTextWithID()))

            left_msgid_text = left_text_block.msgid.flatText()
            right_msgid_text = right_text_block.msgid.flatText()
            is_diff = (left_msgid_text != right_msgid_text)

            #print("left_msgid_text:{}, right_msgid_text:{}, is_diff:{}".format(left_msgid_text, right_msgid_text, is_diff))
            if (not is_diff):
                continue

            right_doc.printTitleOnce()
            print("Before: {}".format(right_text_block.getTextWithID()))
            right_text_block.msgid.setText(left_msgid_text)
            right_doc.setDirty()
            print("After: {}".format(right_text_block.getTextWithID()))

    def getMD5(self, text):
        m = hashlib.md5()
        m.update(text.encode('utf-8'))
        md5=m.hexdigest()
        return md5


    def compareDir(self):

        getter = POBasic(self.left_dir, False)
        left_dir_list = getter.getSortedPOFileListRelative()        

        #right_dir_list = self.getSortedPOFileList(self.right_dir, ".po")        
        #print("self.left_dir: {} left_dir_list: {}".format(self.left_dir, left_dir_list))        
        for(index, common_name) in enumerate(left_dir_list):                        
            #print("common_name: {} index: {}".format(common_name, index))

            #is_debug = (common_name.find("outliner") >= 0)
            #if (is_debug):
            #    print("common_name: {}".format(common_name))
                #exit(0)

            left_file_name=self.left_dir + common_name
            right_file_name=self.right_dir + common_name

            po_left = Document(left_file_name)
            po_left.loadText()
            is_there=os.path.isfile(right_file_name)
            
            # print("left_file_name: {} is_there: {}".format(left_file_name, is_there))
            # print("right_file_name: {} is_there: {}".format(right_file_name, is_there))
            # exit(1)
            if (is_there):
                po_right = Document(right_file_name)
                po_right.loadText()


                left_text = po_left.getAllMSGID()
                right_text = po_right.getAllMSGID()
                md5left = self.getMD5(left_text)
                md5right = self.getMD5(right_text)
                
                #if (is_debug):
                    #print("\n\n--------------\nleft_text:[{}]\n***********\nright_text:[{}], is_equal:{}\n----------------------------\n\n".format(po_left, po_right, md5left == md5right))
                    #exit(0)

                is_diff = (md5left != md5right)
                if (is_diff):
                    print("file: {}\nleft: {}\nright: {}\nis_diff: {}\nis_fix: {}".format(common_name, self.left_dir, self.right_dir, is_diff, self.is_fix))
                    if (self.is_fix):
                        self.transferText(po_left, po_right)
                        if (po_right.isDirty()):
                            print("Saving: {}".format(po_right.path))
                            #po_right.saveText()
                #print(line_sep)
            else:
                print("DOESN'T EXIST: {}".format(right_file_name))
            #return



parser = ArgumentParser()
parser.add_argument("-l", "--left_dir", dest="left_dir", help="The PO directory from which PO files are to be compared.")
parser.add_argument("-r", "--right_dir", dest="right_dir", help="The PO directory to which PO files are be compared with")
parser.add_argument("-f", "--fix", dest="is_fix", help="Fixing the difference or not: TRUE or FALSE")
args = parser.parse_args()

print("args: {}".format(args))

x = CheckChanges()
x.setVars(args.left_dir, args.right_dir, args.is_fix)
x.compareDir()

