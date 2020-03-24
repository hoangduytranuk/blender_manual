import sys
import os
import copy
from bisect import bisect_left
from basefileio import BaseFileIO
from common import Common
from podocument import TextBlock, TextBlockComponent
from algorithms import Algo



class MSGIDcomparator:
    def compare(self, block_x, block_y):
        x_text = block_x.msgid.flatText()
        y_text = block_y.msgid.flatText()
        if (x_text == y_text):
            return 0
        elif (x_text < y_text):
            return -1
        else:
            return 1

class Document (Common, BaseFileIO):
    def __init__(self, Path=None):
        self.path : str = Path
        self.block_list : list = []
        self.translating_thread_list : list = []
        self.compareMSGID = MSGIDcomparator()
        self.is_flat : bool = False
        self.is_changed : bool = False
        self.is_unique : bool = False
        self.is_sorted : bool = False
        self.title_printed : bool = False

    def __repr__(self) -> str:
        output_str : str = ''
        size : int = len(self.block_list)
        for(index, block) in enumerate(self.block_list):

            # valid : bool = (block != None) and (isinstance(block, TextBlock))
            # if (not valid):
            #     return ""
            try:
                is_last : bool = (index >= size-1)
                output_str += block.getTextWithID()
                if (not is_last):
                    output_str += Common.NEWLINE
                    output_str += Common.NEWLINE
            except Exception as e:
                print(block)
                print(e)

        return output_str

    def printTitleOnce(self):
        if (not self.title_printed):
            print("{}\n{}".format(self.path, len(self.path) * "="))
            self.title_printed = True

    def setChanged(value):
        self.is_changed = Value

    def setDirty(self):
        self.is_changed = True

    def clearDirty(self):
        self.is_changed = False

    def isDirty(self):
        return (self.is_changed)

    def sortDocumentInMSGID(self):
        #sorted_list = sorted(self.block_list, key=lambda x: x.msgid.flatText())
        sorted_list : list = sorted(self.block_list)
        self.block_list.clear()
        self.block_list = list(sorted_list)
        self.is_sorted = True

    def sortDocumentInCOMMENT(self):
        def comment_sorter(block : TextBlock) -> str:
            if ((block == None) or (not isinstance(block, TextBlock))):
                return ""

            #print("comment_sorter: {}".format(block))
            comment_text = block.comment.flatText()
            return comment_text

        #sorted_list = sorted(self.block_list, key=lambda x: x.comment.flatText())

        sorted_list : list = sorted(self.block_list, key=comment_sorter)
        self.block_list.clear()
        self.block_list = list(sorted_list)
        self.is_sorted = True

    def binarySearchMSGID(self, msgid_entry : TextBlock):
        found_item = Algo.binarySearch(self.block_list, msgid_entry, cmp=self.compareMSGID)
        return found_item

    def binarySearchText(self, msgid_text):
        text_block = TextBlock(self)
        text_block.init()
        text_block.msgid.setText(msgid_text)
        found_item = Algo.binarySearch(self.block_list, text_block, cmp=self.compareMSGID)
        return found_item

    def isIn(self, msgid_entry : TextBlock):
        if (self.is_sorted):
            found_index = Algo.isIn(self.block_list, msgid_entry, cmp=self.compareMSGID)
            is_found = (found_index >= 0)
            return is_found
        else:
            is_found = (msgid_entry in self.block_list)
            return is_found


    def setPath(self, new_path=None):
        self.path = new_path

    def setFlat(self):
        for(index, text_block) in enumerate(self.block_list):
            text_block.setFlatText()

    def splitFileIntoBlocks(self, read_text):
        #print(read_text)
        blocks = read_text.split(Common.RE_TWO_MORE_RETURN)
        print(blocks)
        return blocks

    def getTextWithIDFlat(self):
        output_str = ''
        size = len(self.block_list)
        for(index, block) in enumerate(self.block_list):
            is_first_block = (index == 0)
            is_last = (index >= size-1)
            if (is_first_block):
                block_text = block.getTextWithID()
            else:
                block_text = block.geBlocktTextWithIDFlat()
            output_str += block_text
            if (not is_last):
                output_str += Common.NEWLINE
                output_str += Common.NEWLINE
        return output_str

    def cleanupEmpties(self):
        remove_count=0
        new_block_list = []
        for(index, block) in enumerate(self.block_list):
            if (not block.isEmpty()):
                new_block_list.append(block)
            else:
                remove_count += 1
        #print("Removed: {}".format(remove_count))
        self.block_list.clear()
        self.block_list = list(new_block_list)


    def getList(self):
        return self.block_list

    def setList(self, new_list):
        self.block_list.clear()
        self.block_list = list(new_list)

    def loadTextAsList(self):
        read_text = self.readFile(self.path)
        current_read_text = str(read_text).strip()

        if (current_read_text == None):
            raise Exception("Unable to read text from file: {}".format(self.path))

        self.block_list = current_read_text.split(Common.NEWLINE)


    def loadText(self):
        read_text = self.readFile(self.path)
        current_read_text = str(read_text).strip()

        # need_to_change = self.isTextNeededToChange(self.current_read_text)
        # if (need_to_change is False):
        #     print("NO need changing")
        #     return
        if (current_read_text == None):
            raise Exception("Unable to read text from file: {}".format(self.path))

        my_block_list = current_read_text.split(Common.RE_TWO_MORE_RETURN)
        for (block_index, current_text_block) in enumerate(my_block_list):
            text_block = TextBlock(self)
            text_block.blockToComponent(current_text_block, block_index)
            self.block_list.append(text_block)


    def saveText(self):
        text = str(self)
        text += (os.linesep if (not text.endswith(os.linesep)) else "")
        #self.path = "/home/htran/change.txt"
        self.writeTextToFile(self.path, text)

    def clone(self):
        new_doc = Document(self.path)
        new_doc.is_flat = self.is_flat
        new_doc.block_list = copy.copy(self.block_list)
        new_doc.is_changed = self.is_changed
        new_doc.translating_thread_list = copy.copy(self.translating_thread_list)
        new_doc.title_printed = self.title_printed
        return new_doc


    def getDictionary(self):
        dict = {}
        for (block_index, text_block) in enumerate(self.block_list):
            msgid = text_block.msgid
            msgstr = text_block.msgstr
            key = msgid.flatText()
            value = msgstr.flatText()
            dict.update({key:value})
        #print("loaded dictionary: {}".format(len(dict)))
        return dict

    def makeBlock(self, comment_text=None, msgctxt_text=None, msgid_text=None, msgstr_text=None, index=0) -> TextBlock:
        text_block = TextBlock(self)
        text_block.init()
        if (comment_text != None):
            text_block.comment.setText(comment_text)
        if (msgctxt_text != None):
            text_block.msgctxt.setText(msgctxt_text)
        if (msgid_text != None):
            text_block.msgid.setText(msgid_text)
        if (msgstr_text != None):
            text_block.msgstr.setText(msgstr_text)
        text_block.index = index
        return text_block

    def insertText(self, comment_text=None, msgctxt_text=None, msgid_text=None, msgstr_text=None, index=0, is_forced=False, is_unique=False):
        text_block : TextBlock = self.makeBlock(comment_text, msgctxt_text, msgid_text, msgstr_text, index)
        if (is_forced):
            self.block_list.append(text_block)
            self.isDirty()
        else:
            if (is_unique):
                is_in = self.isIn(text_block)
                #is_in = (text_block in self.block_list)
            else:
                is_in = False
            if (not is_in):
                self.block_list.append(text_block)
                self.isDirty()

    def toDict(self) -> dict:
        new_dict : dict = {}
        for (index, text_block) in enumerate(self.block_list):
            msgid = text_block.msgid
            k = msgid.flatText()
            v = text_block
            new_dict.update({k:v})
        return new_dict

    def mergeDict(self, new_dict:dict) -> dict:
        is_empty = (new_dict == None or len(new_dict) < 1)
        if (is_empty): return

        current_dict = self.toDict()
        for (k, v) in enumerate(new_dict.items()):
            current_dict.update({k:v})

        self.setDict(current_dict)
        return current_dict

    def setDict(self, dictionary: dict):
        values = list(dictionary.values())
        self.block_list = values

    def addDictionary(self, dictionary:dict):
        is_empty = (dictionary == None or len(dictionary) < 1)
        if (is_empty): return

        old_len = len(self.block_list)
        for k,v in dictionary.items():
            self.insertText(msgid_text=k, msgstr_text=v, is_unique=True)

        if (self.is_sorted):
            self.sortDocumentInMSGID()

        new_len = len(self.block_list)
        number_inserted = (new_len - old_len)

        return number_inserted

    def getAllMSGID(self):
        text_list=[]
        for (block_index, text_block) in enumerate(self.block_list):
            msgid = text_block.msgid
            msgid_text = msgid.flatText()
            text_list.append(msgid_text)
        return os.linesep.join(text_list)

    def setUnique(self):
        self.ensureUniqueness()
        self.is_unique = True

    def ensureUniqueness(self):
        dict_list={}
        for (block_index, text_block) in enumerate(self.block_list):
            msgid = text_block.msgid
            k = msgid.flatText()
            v = text_block
            dict_list.update({k:v})

        new_block_list = list(dict_list.values())
        self.block_list = new_block_list
