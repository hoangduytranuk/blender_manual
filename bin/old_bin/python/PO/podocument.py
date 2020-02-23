import re
import sys
import os
import copy
from bisect import bisect_left
from basefileio import BaseFileIO
from common import Common as cm
from algorithms import Algo
from rst_parser import RSTParser, RSTUnderlinedHeader, RSTTabbedHeader
from potextblock import TextBlock

print("Importing podocument")

class MSGIDcomparator:
    def compare(self, block_x, block_y):
        try:
            # is_equal = (block_x == None) and (block_y == None)
            # is_left = (block_x != None) and (block_y == None)
            # is_right = (block_x == None) and (block_y != None)
            # #print("is_equal:{}, is_left:{}, is_right:{}".format(is_equal, is_left, is_right))
            #
            # if (is_equal):
            #     return 0
            #
            # if (is_left):
            #     return -1
            #
            # if (is_right):
            #     return 1

            # is_debug = block_y.msgid.flatText() == "Relative To"
            # if (is_debug):
            #      print("[{}] = [{}]".format(block_x, block_y))
            #      #exit(1)

            x_text = block_x.msgid.flatText()
            y_text = block_y.msgid.flatText()

            # if (is_debug):
            #     print("[{}] = [{}], is_equal:{}".format(block_x, block_y, x_text == y_text))
                #exit(1)

            is_empty_x = (len(x_text) < 1)
            is_empty_y = (len(y_text) < 1)
            is_ignore = (is_empty_x and is_empty_y)
            if (is_ignore):
                return -1

            if (x_text == y_text):
                return 0
            elif (x_text < y_text):
                return 1
            else:
                return -1
        except Exception as e:
            print("Exception: {}".format(e))
            print("block_x: {}".format(block_x))
            print("block_y: {}".format(block_y))
            return -1

class Document (BaseFileIO):
    def __init__(self, Path=None):
        self.path = Path
        self.block_list  = []
        self.translating_thread_list  = []
        self.compareMSGID = MSGIDcomparator()
        self.is_flat  = False
        self.is_changed  = False
        self.is_unique  = False
        self.is_sorted  = False
        self.title_printed  = False

    def __repr__(self) -> str:
        return self.getTextWithIDFlat()

    def getTextBody(self) -> str:
        self.getTextWithIDFlat()

    def msg(self, msg_text=None):
        patch_msg = (msg_text if (msg_text != None) else "")
        msg = ("{}:{}".format(patch_msg,self.path))
        print("{}\n{}".format(msg, len(msg) * "-"))

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

    def isEmpty(self):
        return (self.block_list == None) or (len(self.block_list) < 1)

    def sortDocumentInMSGID(self):
            sorted_list = sorted(self.block_list, key=lambda x: x.msgid.flatText())
            self.setList(sorted_list)
        #self.block_list.sort()
            self.is_sorted = True

    def sortDocumentInCOMMENT(self):
        def comment_sorter(block ) -> str:
            if ((block == None) or (not isinstance(block, TextBlock))):
                return ""

            #print("comment_sorter: {}".format(block))
            comment_text = block.comment.flatText()
            return comment_text

        #sorted_list = sorted(self.block_list, key=lambda x: x.comment.flatText())

        sorted_list  = sorted(self.block_list, key=comment_sorter)
        self.block_list.clear()
        self.block_list = list(sorted_list)
        self.is_sorted = True

    def binarySearchMSGID(self, msgid_entry):
        #found_item = Algo.binarySearch(self.block_list, msgid_entry, cmp=self.compareMSGID)
        found_index = bisect_left(self.block_list, msgid_entry)
        hi = len(self.block_list)
        is_valid_index = (found_index >= 0) and (found_index < hi)
        if (is_valid_index):
            found_entry = self.block_list[found_index]
            is_found = (found_entry == msgid_entry)
            if (is_found):
                return found_entry
        return None

    def binarySearchText(self, msgid_text):
        text_block = TextBlock(self)
        text_block.init()
        text_block.msgid.setText(msgid_text)
        found_item = Algo.binarySearch(self.block_list, text_block, cmp=self.compareMSGID)
        return found_item

    def isIn(self, msgid_entry):
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
        blocks = read_text.split(cm.RE_TWO_MORE_RETURN)
        print(blocks)
        return blocks

    def getTextWithIDFlat(self):
            output_str = ''
            size = len(self.block_list)

            block_text = None
            for(index, block) in enumerate(self.block_list):
                is_first_block = (index == 0)
                is_last = (index == size-1)
                if (is_first_block):
                    block_text  = block.getTextWithID()
                else:
                    block_text = block.geBlocktTextWithIDFlat()
                output_str += block_text
                if (not is_last):
                    output_str += cm.NEWLINE
                    output_str += cm.NEWLINE
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

        self.block_list = current_read_text.split(cm.NEWLINE)

    def loadPOText(self):
            read_text = self.readFile(self.path)
            current_read_text = str(read_text).strip()

            #need_to_change = self.isTextNeededToChange(self.current_read_text)
            # if (need_to_change is False):
            #     print("NO need changing")
            #     return

            if (current_read_text == None):
                raise Exception("Unable to read text from file: {}".format(self.path))

            ##block_p = r"(?P<block>^[#].*?)(?P<blank_line>\s{2})"
            #block_p = r"(^#.*\s)+"
            #p_list = re.findall(block_p, current_read_text, re.M)
            #print("p_list:{}".format(p_list))
            #exit(0)

            #print("current_read_text:{}".format(current_read_text))
            my_block_list = current_read_text.split(cm.RE_TWO_MORE_RETURN)
            for (block_index, current_text_block) in enumerate(my_block_list):
                text_block = TextBlock(self)
                text_block.blockToComponent(current_text_block, block_index)
                self.block_list.append(text_block)

    def loadRSTText(self):
        read_text = self.readFile(self.path)
        current_read_text = str(read_text).strip()

        # need_to_change = self.isTextNeededToChange(self.current_read_text)
        # if (need_to_change is False):
        #     print("NO need changing")
        #     return
        if (current_read_text == None):
            raise Exception("Unable to read text from file: {}".format(self.path))

        my_line_list = current_read_text.split(cm.NEWLINE)

        list_funct = [
            RSTUnderlinedHeader(my_line_list),
            RSTTabbedHeader(my_line_list)
                        ]
        current_block  = None
        for (line_index, raw_text_line) in enumerate(my_line_list):
            text_line = raw_text_line.rstrip()
            is_empty = (len(text_line) == 0)
            if (is_empty):
                [i.setPreviousLineIndex(-1) for i in list_funct]
                continue

            #rst_underline_header.setTextLine(text_line)
            [i.setTextLine(text_line)  for i in list_funct]
            [i.setLineIndex(line_index) for i in list_funct]
            [i.setDocument(self) for i in list_funct]

            for rst_func in list_funct:
                current_block = rst_func.run()
                if (current_block != None):
                    #print("current_block: {}".format(current_block))
                    self.block_list.append(current_block)

        if (current_block != None):
            self.block_list.append(current_block)


    def loadText(self):
        self.loadPOText()

    def saveText(self, out_path=None):
        text = str(self)
        text += (os.linesep if (not text.endswith(os.linesep)) else "")
        if (out_path == None):
            self.writeTextToFile(self.path, text)
            #pass
        else:
            self.writeTextToFile(out_path, text)
            #pass

    def clone(self):
        new_doc = Document(self.path)
        new_doc.is_flat = self.is_flat
        new_doc.block_list = copy.copy(self.block_list)
        new_doc.is_changed = self.is_changed
        new_doc.translating_thread_list = copy.copy(self.translating_thread_list)
        new_doc.title_printed = self.title_printed
        return new_doc


    def getDictionary(self) -> dict:
        dict = {}
        for (block_index, text_block) in enumerate(self.block_list):
            is_first_block = (block_index == 0)
            if (is_first_block):
                continue

            msgid = text_block.msgid
            msgstr = text_block.msgstr
            has_been_translated = (not msgstr.isConsideredEmpty())
            if (not has_been_translated):
                continue

            key = msgid.flatText()
            value = msgstr.flatText()
            dict.update({key:value})
        #print("loaded dictionary: {}".format(len(dict)))
        return dict

    def getDictionaryWithMSGIDAsKey(self) -> dict:
        dict = {}
        for (block_index, text_block) in enumerate(self.block_list):
            is_first_block = (block_index == 0)
            if (is_first_block):
                continue

            msgid = text_block.msgid
            msgstr = text_block.msgstr
            has_been_translated = (not msgstr.isConsideredEmpty())
            if (not has_been_translated):
                continue

            key = msgid.flatText()
            value = text_block
            dict.update({key:value})
        #print("loaded dictionary: {}".format(len(dict)))
        return dict

    def makeBlock(self, comment_text=None, msgctxt_text=None, msgid_text=None, msgstr_text=None, index=0):
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
        text_block  = self.makeBlock(comment_text, msgctxt_text, msgid_text, msgstr_text, index)
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
        new_dict = {}
        for (index, text_block) in enumerate(self.block_list):
            msgid = text_block.msgid
            k = msgid.flatText()
            v = text_block
            new_dict.update({k:v})
        return new_dict

    def mergeDoc(self, new_doc) -> dict:
        new_dict = {}
        for(index, block) in enumerate(self.block_list):
            try:
                k = block.msgid.flatText()
                v = block
                new_dict.update({k:v})
            except Exception as e:
                print("Exception {}".format(e))
                print("block:{}".format(block))
                print("[continue]")
                continue

        for(index, block) in enumerate(new_doc.block_list):
            try:
                k = block.msgid.flatText()
                v = block
                new_dict.update({k:v})
            except Exception as e:
                print("Exception {}".format(e))
                print("block:{}".format(block))
                print("[continue]")
                continue
        merged_list = new_dict.values()
        self.block_list=list(merged_list)

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
            is_ignore = (block_index == 0)
            if (is_ignore): continue

            msgid = text_block.msgid
            msgid_text = msgid.flatText()
            text_list.append(msgid_text)
        return os.linesep.join(text_list)

    def getTextOnly(self):
        text_list=[]
        for (block_index, text_block) in enumerate(self.block_list):
            is_ignore = (block_index == 0)
            if (is_ignore): continue

            text = str(text_block)
            text_list.append(text)
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

    def duplicateMSGIDToUntranslatedMSGSTR(self, title_list):
        is_empty = (title_list == None or len(title_list) < 1)
        if (is_empty):
            return False

        self.printTitleOnce()
        for (block_index, text_block) in enumerate(self.block_list):
            print("Processing block:{}".format(text_block.getTextWithID()))
            msgid = text_block.msgid
            id_text = msgid.flatText()
            id_text = cm.stripQuote(id_text)
            #print("msgid: {}".format(id_text))

            is_numeric = cm.isNumber(id_text)

            is_title = (id_text in title_list)
            is_ignore = cm.isIgnored(id_text)


            if (not is_title or is_ignore or is_numeric): continue

            msgstr = text_block.msgstr
            str_text = msgstr.flatText()
            str_text = cm.stripQuote(str_text)

            is_translated = (re.search("[\ ]?-- ", str_text) != None)
            inconsistent = (re.search(" - ", str_text) != None)

            #print("{}".format(self.getTextWithIDFlat()))

            if (is_translated): continue

            if (inconsistent):
                replace_text = re.sub(" - ", " -- ", str_text)
            else:
                if (len(str_text) > 0):
                    replace_text = "{} -- {}".format(str_text, id_text)
                else:
                    replace_text = "-- {}".format(id_text)

            print("-" * 80)
            print("OLD:{}\n".format(text_block.getTextWithID()))

            msgstr.setText(replace_text)
            self.setDirty()
            print("NEW:{}".format(text_block.getTextWithID()))
            #print("CHANGED:{}".format(self.getTextWithIDFlat()))

        if (self.isDirty()):
            temp_path = "/home/htran/temp.po"
            print("Saving Changes:{}".format(temp_path))
            self.saveText(out_path=temp_path)
            #print("Saving Changes:{}".format(self.path))
            #self.saveText()
            print("-" * 80)





