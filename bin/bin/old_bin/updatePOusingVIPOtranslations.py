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
from podocument import Document, MSGIDcomparator

from action import TransferTextBlockAction, TwoDocumentAction
from pobase import POBasic
from algorithms import Algo

from argparse import ArgumentParser
import threading

class FindAndUpdate(threading.Thread):
    def __init__(self, ID, search_list, from_block):
        threading.Thread.__init__(self)
        self.threadID = ID
        self.search_list = search_list
        self.from_block = from_block
        self.name = from_block.msgid.flatText()
        self.transferMSGSTR = TransferMSGSTR()
        self.compareMSGID = MSGIDcomparator()

    def run(self):
        to_block = Algo.binarySearch(self.search_list, self.from_block, cmp=self.compareMSGID)
        is_found = (to_block != None)
        if (not is_found):
            return None
        else:
            print("ID:{}\nfind\n[{}]\nfound\n[{}]".format(self.threadID, self.name, to_block))
            self.transferMSGSTR.setArgs(self.from_block, to_block)
            self.transferMSGSTR.run()
            ##print("looking for {}, found_index {} is_found {}".format(msgid_entry, i, is_found))
            #return found_item


class TransferTextDocument(TwoDocumentAction):

    def run(self):
        if ((self.callback == None) or not isinstance(self.callback, TransferTextBlockAction)):
            raise Exception("callback is either not provided or is not an instance of TransferTextBlockAction.")
        
        to_doc_sorted = self.to_doc.clone()
        to_doc_sorted.sortDocumentInMSGID()

        threads_for_doc=[]
        for(index, from_text_block) in enumerate(self.from_doc.block_list):
            is_first_block = (index == 0)
            if (is_first_block): continue

            find_and_update_thread = FindAndUpdate(index, to_doc_sorted.block_list, from_text_block)
            threads_for_doc.append(find_and_update_thread)
            # to_text_block = to_doc_sorted.binarySearchMSGID(from_text_block)
            # if (to_text_block == None):
            #     #from_text_block.document.printTitleOnce()
            #     #print("NOT THERE from_block:[{}]".format(from_text_block.getTextWithID()))
            #     continue
            #
            # #print("found: {} => {}".format(from_text_block, to_text_block))
            # self.callback.setArgs(from_text_block, to_text_block)
            # self.callback.run()

        for(index, thread_item) in enumerate(threads_for_doc):
            thread_item.start()

        for(index, thread_item) in enumerate(threads_for_doc):
            thread_item.join()


class TransferMSGSTR(TransferTextBlockAction):

    ignore_items = [
            'Blender',
            'ID',
            'OpenCL',
            'Gamma',
            'Alpha',
            'Z',
            'X',
            'Y',
            'UV',
            'Catmull-Rom',
            'Mitch',
            'Laplace',
            'Sobel',
            'Prewitt',
            'Kirsch',
            'DPI',
            'Iris',
            'Targa',            
        ]
    def run(self):
        is_wrong_block = (self.to_block.index == 0) or (self.from_block.index == 0)
        if (is_wrong_block): return
        
        from_msgid = self.from_block.msgid
        from_msgid_text = from_msgid.flatText()
        from_msgstr = self.from_block.msgstr
        from_msgstr_text = from_msgstr.flatText()
    
        to_msgid = self.to_block.msgid
        to_msgid_text = to_msgid.flatText()
        to_msgstr = self.to_block.msgstr
        to_msgstr_text = to_msgstr.flatText()
        
        is_to_repeat = (len(to_msgid_text) > 0) and (len(to_msgstr_text) > 0) and (to_msgid_text == to_msgstr_text)
        if (is_to_repeat):
            self.to_block.document.printTitleOnce()
            #print("REPEAT before change:\n[{}]\n".format(self.to_block.getTextWithID()))
            self.to_block.msgstr.setText("")
            self.to_block.document.setDirty()
            print("REPEAT changed:\n[{}]\n".format(self.to_block.getTextWithID()))
            return
        

        to_msgstr_has_text = (len(to_msgstr_text) > 0)
        from_msgstr_has_text = (len(from_msgstr_text) > 0)
        if (not from_msgstr_has_text): 
            return

        id_and_translation_repeat = (from_msgstr_has_text and (from_msgid_text == from_msgstr_text))        
        is_change = ((not to_msgstr_has_text) and (not id_and_translation_repeat))        
        if (is_change):
            self.to_block.document.printTitleOnce()
            #print("TRANSFER before change:\nfrom:\n[{}]\nto:[{}]\n".format(self.from_block.getTextWithID(), self.to_block.getTextWithID()))
            transfer_msgstr_text = "{} -- {}".format(from_msgstr_text, to_msgid_text)
            self.to_block.msgstr.setText(transfer_msgstr_text)
            self.to_block.document.setDirty()
            print("TRANSFER to:[{}]\n".format(self.to_block.getTextWithID()))
            #print("TRANSFER changed:\nfrom:\n[{}]\nto:[{}]\n".format(self.from_block.getTextWithID(), self.to_block.getTextWithID()))
            #print("from:{}, lineno:{}\nto:{}, lineno:{}\n".format(self.from_block, self.from_block.index, self.to_block, self.to_block.index))            

class TransferVIPOTranslation(BaseFileIO):
    def __init__(self):
        self.po_dir = None
        self.vi_po_path = None    

    #def getMD5(self, text):
        #m = hashlib.md5()
        #m.update(text.encode('utf-8'))
        #md5=m.hexdigest()
        #return md5

    def Start(self, po_dir, vi_po_path):
        self.po_dir = po_dir
        self.vi_po_path = vi_po_path
        

    def transferVIPOtranslation(self, callback = None):

        vi_po_doc = Document(self.vi_po_path)
        vi_po_doc.loadText()
        vi_po_doc.sortDocumentInMSGID()
        #print(vi_po_doc)
        #return

        getter = POBasic(self.po_dir, False)
        po_dir_list = getter.getSortedPOFileList()
                
        for(index, po_file_path) in enumerate(po_dir_list):
            if (len(po_file_path) <= 0):
                continue
            
            #print("{}\n{}".format(po_file_path, len(po_file_path) * "="))
            po_doc = Document(po_file_path)
            po_doc.loadText()

            if ((callback != None) and isinstance(callback, TwoDocumentAction)):
                callback.setArgs(vi_po_doc, po_doc)
                callback.run()

            if (po_doc.isDirty()):
                print("SAVING DOCUMENT: {}".format(po_doc.path))
                #po_doc.saveText()
            #if (po_doc.isDirty()): po_doc.saveText()

        #if (vi_po_doc.isDirty()): vi_po_doc.saveText()
        
            

parser = ArgumentParser()
parser.add_argument("-p", "--po", dest="po_dir", help="The PO directory from which PO files are to be changed.")
parser.add_argument("-v", "--vipo", dest="vi_po_path", help="The path of vi.po directory to which translation are taken from")
args = parser.parse_args()

#print("args: {}".format(args))

x = TransferVIPOTranslation()
x.Start(args.po_dir, args.vi_po_path)

doc_x = TransferTextDocument()
block_x = TransferMSGSTR()
doc_x.setCallBack(block_x)
x.transferVIPOtranslation(doc_x)

