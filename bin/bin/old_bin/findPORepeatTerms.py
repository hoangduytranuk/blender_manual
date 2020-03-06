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

REPEAT_DOC_FILE="/home/htran/msgid_po_0002.po"
end_char_list=set(['.','!',')', ',', '>', ':','*','`',])
COMMENT_FLAG="#: "
class DefaultComparator:

    def compare(self, x, y):
        if (x == y):
            return 0
        elif (x < y):
            return 1
        else:
            return -1

class CollectCommonMSGID:
    def __init__(self):
        self.text_block : TextBlock = None;
        self.new_dict : dict = {}

    def setArgs(self, text_block : TextBlock):
        self.text_block = text_block
        
    def setDictionaryFile(self, dictionary_file):
        self.dic_file_name = dictionary_file

    def setNewDict(self, dictionary):
        self.new_dict = dictionary

    def getNewDict(self):
        return self.new_dict

    def fillNewDict(self):
        msgid = self.text_block.msgid
        msgstr = self.text_block.msgstr
        
        trans = msgstr.flatText()
        has_trans = (len(trans) > 0)
        if (has_trans):
            return
        
        key = msgid.flatText()        
        value = (self.new_dict.get(key))
        is_insert = (value == None)
        is_update = (not is_insert) and (value > 0)
        if (is_insert):
            self.new_dict.update({key:1})
        else:
            self.new_dict.update({key:value + 1})


    def run(self):
        self.fillNewDict()

    def hasItem(self):
        return (len(self.new_dict) > 0)


class ApplyDictionaryToPO:
    def __init__(self):
        self.vi_po_doc = None
        self.text_block = None;
        self.repeat_dict = None
        self.vi_po_dict = None
        self.comparator = DefaultComparator()

    def setArgs(self, text_block):
        self.text_block = text_block

    def setVIPODoc(self, vi_po_doc):
        self.vi_po_doc = vi_po_doc
        self.vi_po_dict = vi_po_doc.getDictionary()
        #print("vipo loaded: {}".format(len(self.vi_po_dict)))

    def setDictionary(self, dict):
        self.repeat_dict = dict
        #print("repeat_dic loaded: {}".format(len(self.repeat_dict)))

    def run(self):
        debug = False
        changed = False
        
        msgstr = self.text_block.msgstr
        msgstr_text = msgstr.flatText()

        has_translation = (len(msgstr_text) > 1)
        if (has_translation): return

        msgid = self.text_block.msgid
        msgid_text = msgid.flatText()
        document = self.text_block.document

        found_block = self.vi_po_doc.binarySearchText(msgid_text)
        has_value = (found_block != None)
        if (has_value):
            #value = (repeat_dict_value if (repeat_dict_value != None) else po_value)
            value = (found_block.msgstr.flatText())
            is_empty = (len(value) < 1)
            is_repeat = (msgid_text == value)
            is_ignore = (is_empty or is_repeat)
            if (is_ignore): return

            msgstr.setText(value)
            document.setDirty()
            document.printTitleOnce()
            print("added translation: {}=>\n{}".format(value, self.text_block.getTextWithID()))
            #exit(1)
            #return


class ListTermsPO:
    def __init__(self):
        self.vi_po_doc = None
        self.text_block = None;
        self.comparator = DefaultComparator()
        self.new_dict:dict={}

    def setArgs(self, text_block):
        self.text_block = text_block

    def setVIPODoc(self, vi_po_doc):
        self.vi_po_doc = vi_po_doc
        #self.vi_po_dict = vi_po_doc.getDictionary()
        #print("vipo loaded: {}".format(len(self.vi_po_dict)))

    def getDict(self):
        return self.new_dict

    def setDictionary(self, dictionary):
        self.new_dict = dictionary
        #print("repeat_dic loaded: {}".format(len(self.repeat_dict)))

    def run(self):
        msgstr = self.text_block.msgstr
        msgstr_flat_text = msgstr.flatText()

        has_translation = (len(msgstr_flat_text) > 1)
        if (has_translation): return

        msgid = self.text_block.msgid
        msgid_flat_text = msgid.flatText()
        document = self.text_block.document
        
        end_char = msgid_flat_text[len(msgid_flat_text)-1:]
        is_ignore = (end_char in end_char_list)
        has_link = (msgid_flat_text.find("`") >= 0)
        
        k = msgid_flat_text
        if (has_link):
            v = "{} -- {}".format(k, k)            
        if (not is_ignore):
            v = " -- {}".format(k)
        else:
            v = "{}".format("")
            
        text_block = self.vi_po_doc.makeBlock(comment_text=COMMENT_FLAG+document.path, msgid_text=k, msgstr_text=v)
        self.new_dict.update({k:text_block})
            
        
        

class RepeatTerms(BaseFileIO):
    def __init__(self):
        self.po_dir = None
        self.docEventHandler = None
        self.blockEventHandler = None
        self.dictionary_file = None
        self.dictionary : dict = {}
        self.vi_po_path = None
        self.operation = "APPLY"

    def start(self, po_dir, dictionary_file, vi_po_file, operation):
        self.po_dir = po_dir
        self.dictionary_file = dictionary_file
        self.vi_po_path = vi_po_file
        self.operation = operation

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
            #if (po_doc.isDirty()): po_doc.saveText()


    def LIST(self):
        repeat_doc:Document = Document(REPEAT_DOC_FILE)
        repeat_doc.loadText()
        repeat_doc.setUnique()
        repeat_doc.setFlat()
        repeat_doc.sortDocumentInMSGID()

        print(repeat_doc)

        self.blockEventHandler.setVIPODoc(repeat_doc)        
        self.loadPOFilesForProcessing()
        
        new_dict : dict = self.blockEventHandler.getDict()
        #print(new_dict)
        #repeat_doc.mergeDict(new_dict)
        new_doc = repeat_doc.clone()
        new_doc.setDict(new_dict)

        print(new_doc)
        #old_dict = repeat_doc.toDict()
        #new_doc.mergeDict(old_dict)
        #new_doc.sortDocumentInCOMMENT()
        #repeat_doc.sortDocumentInCOMMENT()
        #print(new_doc)
        #print(repeat_doc)
        #repeat_doc.saveText()
        
    def EXTRACT(self):
        old_dict = self.loadRepeatItems()
        self.loadPOFilesForProcessing()
        new_dict = self.listRepeatItems(self.blockEventHandler.getNewDict())
        update_dict = self.duplidateTextIfNeeded(new_dict)
        new_dict = self.mergeDict(old_dict, update_dict)
        update_dict = self.insertTranslationFromVIPO(new_dict)
        print("{}".format(update_dict.items()))
        #self.saveRepeatItems(update_dict)

    def APPLY(self):
        old_dict = self.loadRepeatItems()
        vi_po_doc = self.loadVIPO()
        number = vi_po_doc.addDictionary(old_dict)
        #self.blockEventHandler.setDictionary(old_dict)
        self.blockEventHandler.setVIPODoc(vi_po_doc)
        self.loadPOFilesForProcessing()

    def VERIFY(self):
        old_dict = self.loadRepeatItems()
        vi_po_doc = self.loadVIPO()
        number = vi_po_doc.addDictionary(old_dict)
        #self.blockEventHandler.setDictionary(old_dict)
        self.blockEventHandler.setVIPODoc(vi_po_doc)
        self.loadPOFilesForProcessing()
        

    def run(self):
        doc_x = BasicDocumentAction()
        if (self.operation.startswith("E")):
            block_event_handler = CollectCommonMSGID()
            self.setHandlers(doc_x, block_event_handler)
            self.EXTRACT()
        elif (self.operation.startswith("A")):
            block_event_handler = ApplyDictionaryToPO()
            self.setHandlers(doc_x, block_event_handler)
            self.APPLY()
        elif (self.operation.startswith("V")): #VERIFY
            a=(1+1)
        elif (self.operation.startswith("L")): 
            block_event_handler = ListTermsPO()
            self.setHandlers(doc_x, block_event_handler)
            self.LIST()
        else: 
            return


    def loadVIPO(self):
        vi_po_doc = Document(self.vi_po_path)
        vi_po_doc.loadText()
        vi_po_doc.sortDocumentInMSGID()
        return vi_po_doc


    def insertTranslationFromVIPO(self, new_dict):
        changed = False
        vi_po_doc = self.loadVIPO()
        for key, value in new_dict.items():

            has_translation = (len(value) > 1)

            if (has_translation): continue

            dict_entry = TextBlock(vi_po_doc)
            dict_entry.init()
            dict_entry.setMSGID(key)
            dict_entry.setMSGSTR(value)


            found_block = vi_po_doc.binarySearchMSGID(dict_entry)
            is_found = (found_block != None)
            if (not is_found): continue

            #print("inserted: {}".format(found_block))
            #exit(1)

            translation_text = found_block.msgstr.flatText()
            new_dict.update({key:translation_text})
            changed = True
        return new_dict

    def loadRepeatItems(self):
        old_dict={}
        loaded_dic=None
        with open(self.dictionary_file, "r", encoding="utf-8") as f:
            loaded_dic = json.load(f)

        for (index, entry) in enumerate(loaded_dic):
            k,v = entry
            old_dict.update({k:v})
            #print("{}=>{}".format(k, v))
        return old_dict
        #for k,v in self.dict:
        #    print("{} = {}".format(k, v))

    def listRepeatItems(self, dict):
        data = {}
        for key, value in dict.items():
            if (value > 2):
                #print("{}:{}".format(key, value))
                value="$"
                data.update({key:value})
        return data

    def duplidateTextIfNeeded(self, dict):
        new_data={}
        for key, value in dict.items():            
            last_char = key[len(key)-1:]
            has_forbidden_char = (last_char in end_char_list)
            is_update = (not has_forbidden_char)
            if (is_update):
                value = "{} -- {}".format("", key)
            else:
                value = "$"
            new_data.update({key : value})
            #print("i:{} key:{} value:{}".format(index, key, value))
        return new_data

    def mergeDict(self, old_dic, new_dic):
        comp = DefaultComparator()
        for k,v in old_dic:
            new_dic.update({k:v})
        return new_dic

    def saveRepeatItems(self, dict):
        data_list = self.listRepeatItems(dict)
        data = self.duplidateTextIfNeeded(data_list)
        with open(self.dic_file_name, "w+", encoding="utf-8") as f:
            json.dump(data, f)


parser = ArgumentParser()
parser.add_argument("-p", "--po", dest="po_dir", help="The PO directory from where repeat terms are extracted.")
parser.add_argument("-d", "--dict", dest="dictionary_file", help="dictionary file to read/write from/to.")
parser.add_argument("-v", "--vipo", dest="vi_po", help="Path to file vi.po, with the available translation texts that can be used.")
parser.add_argument("-o", "--op", dest="operation", help="EXTRACT or APPLY; EXTRACT; VERIFY will get all repeated string from all PO files "
                                                         "and merge with the provided dictionary, at the same time find translations"
                                                         "in the vipo file and insert them into the dictionary list to store into the"
                                                         "dictionary file provided. APPLY will take the content of the "
                                                         "dictionary, assumed has been translated, and the vipo file, apply to every"
                                                         "msgid entry found. VERIFY will validate document's translations and print out" 
                                                         "differences - against the dictionary.")
args = parser.parse_args()

print("args: {}".format(args))

x = RepeatTerms()
x.start(args.po_dir, args.dictionary_file, args.vi_po, args.operation)
x.run()

