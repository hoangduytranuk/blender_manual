print("Importing podocument.py, which includes TextBlock and TextBlockComponent")
import sys
import os
import copy
from bisect import bisect_left
from basefileio import BaseFileIO
from common import Common
from algorithms import Algo
#from rst_parser import RSTParser, RSTUnderlinedHeader, RSTTabbedHeader


class TextBlockComponent():
    def __init__(self, ID : str, document : object, block : object):
        self.ID : str = ID
        self.is_flat : bool = False
        self.text_list : list = []
        self.document : object = document
        self.block : object = block

    def __repr__(self):
        #return repr((self.comment, self.msgctxt, self.msgid, self.msgstr, self.is_flat))
        return os.linesep.join(self.text_list)

    def __cmp__(self, other) -> bool:
        if (other == None or not isinstance(other, TextBlockComponent)):
                return 1
        this_flat_text = self.flatText()
        other_flat_text = other.flatText()
        print("this_flat_text:[{}] -- other_flat_text:[{}]".format(this_flat_text, other_flat_text))
        if (this_flat_text == other_flat_text): return 0
        if (this_flat_text > other_flat_text): return 1
        if (this_flat_text < other_flat_text): return -1


    def __gt__(self, other : object) -> bool:
        return self.__cmp__(other) > 1

    def __eq__(self, other : object):
        return self.__cmp__(other) > 1

    def __lt__(self, other : object):
        return self.__cmp__(other) < 1

    def debugstr(self) -> str:
        text_list=[]
        text_list.append("ID:{}".format(self.ID))
        text_list.append("is_flat:{}".format(self.is_flat))

        text_list.append("text_list:{}".format(''.join(self.text_list)))
        text_list.append("document:{}".format(os.linesep.join(self.document.path)))

        return os.linesep.join(text_list)


    #transfer to this
    def copyContent(self, other : object) -> bool:
        if (other == None or not isinstance(other, TextBlockComponent)):
            return False

        self.ID = other.ID
        self.text_list = copy.deepcopy(other.text_list)
        return True


    def copyText(self, other) -> bool:
        if (other == None):
            return False
        self.setList(other.text_list);
        return True

    def isNone(self) -> bool:
        return (self.text_list == None)

    def isEmpty(self):
        return (self.isNone() or (self.text_list == []))

    def isConsideredEmpty(self):
        is_consider_empty = self.isEmpty() or (len(self.flatText()) == 0)
        return is_consider_empty

    def insertText(self, text):
        self.text_list.append(text)

    def setEmptyText(self):
        self.text_list.clear()
        self.text_list.append("")

    def len(self) -> int:
        if (self.isEmpty()):
            return 0
        else:
            return len(self.text_list)

    def clear(self):
        self.text_list.clear()

    def setID(self, ID : str):
        self.ID = ID

    def appendText(self, text:str) -> bool:
        if (text == None):
            return False

        is_first_line=(self.text_list == [])
        has_leading_space = text.startswith(Common.SPACE)
        append_text = text if (has_leading_space or is_first_line) else " {}".format(text)
        self.text_list.append(append_text)
        return True

    def getList(self):
        return self.text_list

    def setList(self, new_list : list):
        self.text_list.clear()
        self.text_list = list(new_list)

    def setText(self, new_text : str):
        self.text_list.clear()
        self.text_list.append(new_text)

    def setFlat(self):
        self.is_flat = True
        self.text_list[:]=[]
        self.text_list.append(self.flatText())

    def getFlatTextClone(self):
        copy_item : TextBlockComponent = self.clone()
        copy_item.is_flat = True
        copy_item.text_list.clear()
        copy_item.text_list.append(self.flatText())
        return copy_item

    def clone(self) -> object:
        dup = TextBlockComponent(self.ID)
        dup_text_list = copy.deepcopy(self.text_list)
        dup.text_list = dup_text_list
        dup.document = self.document
        dup.block = self.block
        return dup

    def stripID(self, text_line : str) -> [str, bool]:
        line1 : str =re.sub(self.ID, Common.RE_EMPTYSTR, text_line)
        is_empty : bool = (len(line1) == 0)
        return [line1 , is_empty]

    def nonFlatText(self) -> str:
        if (self.text_list == []):
            return None

        text_line = os.linesep.join(self.text_list)
        #print("text_line after joined: [{}]".format(text_line))
        return text_line

    def flatText(self) -> str:
        if (self.text_list == []):
            return None

        mlist : list =[]
        for(index, text_line) in enumerate(self.text_list):
            try:
                #print("flatText Before stripQuote:[{}]".format(text_line))
                txt_line = Common.stripQuote(text_line)
                #print("flatText After stripQuote:[{}]".format(txt_line))
                mlist.append(txt_line)
            except Exception as e:
                self.document.printTitleOnce()
                print("Exception: {}".format(e))
                print("SOMETHING WRONG text_line: {}".format(text_line))
                exit(1)
        text_line : str = ''.join(mlist)
        #print("text_line after joined: [{}]".format(text_line))
        return text_line

    def flatTextQuoted(self) -> str:
        if (self.text_list == []):
            return None

        flat_text = self.flatText()
        flat_text_quoted = "\"{}\"".format(flat_text)
        return flat_text_quoted

    def getTextWithID(self) -> str:
        return self.getComponentTextWithIDWithOption(is_flat=False)

    def trimTextList(self):
        strip_map = map(lambda each:each.strip(), self.text_list)
        new_text_list = list(strip_map)
        self.setList(new_text_list)

    def appendText(self, text:str):
        self.text_list.append(text)

    def removeText(self, text:str):
        self.trimTextList()
        self.text_list.remove(text)

    def hasText(self, text:str) -> bool:
        has_text = (self.flatText().find(text) >= 0)
        return has_text

    def getComponentTextWithID(self) -> str:
        return self.getComponentTextWithIDWithOption(is_flat=False)

    def getComponentTextWithIDFlat(self) -> str:
        return self.getComponentTextWithIDWithOption(is_flat=True)

    def getComponentTextWithIDWithOption(self, is_flat=False) -> str:
        if (self.text_list == []):
            return None

        is_debug = (self.ID == Common.MSGSTR)
        if (is_debug):
            print("text_list:{}".format(self.text_list))

        text_line = ""
        if (is_flat):
            text_line = self.flatText()
        else:
            text_line = os.linesep.join(self.text_list)

        is_quoted = (Common.QUOTED_STRING_RE.match(text_line) != None)
        if (not is_quoted):
            is_leading_quoted = text_line.startswith(Common.QUOTE)
            is_trailing_quoted = text_line.endswith(Common.QUOTE)
            if (not is_leading_quoted):
                text_line = "{}{}".format(Common.QUOTE, text_line)
            if (not is_trailing_quoted):
                text_line = "{}{}".format(text_line, Common.QUOTE)

        text_line = "{} {}".format(self.ID,text_line)
        return text_line


class TextBlock (Common):

    def __init__(self, document):
        self.document = document
        self.comment = None
        self.msgctxt = None
        self.msgid = None
        self.msgstr = None
        self.is_flat = False
        self.index = -1
        self.is_changed = False
        self.is_fuzzy = False

    def setComponents(self,
                      document,
                      comment,
                      msgctxt,
                      msgid,
                      msgstr,
                      is_flat = False,
                      index = -1):
        self.comment = comment
        self.msgctxt = msgctxt
        self.msgid = msgid
        self.msgstr = msgstr
        self.is_flat = is_flat
        self.index = index
        self.document = document
        self.is_changed = False
        #print("setComponents:\n{} {} {} {}".format(str(self.comment), str(self.msgctxt), str(self.msgid), str(self.msgstr)))

    def __repr__(self):
        #return repr((self.comment, self.msgctxt, self.msgid, self.msgstr, self.is_flat))
        mylist=[]

        mylist.append(self.msgid.flatText())
        mylist.append(Common.NEWLINE)

        if (self.msgstr.isEmpty()):
            if (self.index == 0):
                mylist.append(self.msgstr.nonFlatText())
            else:
                mylist.append(self.msgstr.flatText())
            mylist.append(Common.NEWLINE)

        mylist.append(Common.NEWLINE)
        out_str = ''.join(mylist)
        return out_str

    def __compare__(self, other):
        if (other == None):
            return 1

        this_msgid = self.msgid.flatText()
        other_msgid = other.msgid.flatText()

        is_greater = (this_msgid > other_msgid)
        is_smaller = (this_msgid < other_msgid)
        if (is_greater):
            return -1
        if (is_smaller):
            return 1
        else:
            return 0

    def __gt__(self, other):
        return (self.__compare__(other) > 1)

    def __eq__(self, other):
        return (self.__compare__(other) == 0)

    def __lt__(self, other):
        return (self.__compare__(other) < 0)

    def clone(self):
        dup = TextBlock(self.document)
        dup.comment = self.comment
        dup.msgctxt = self.msgctxt
        dup.msgid = self.msgid
        dup.msgstr = self.msgstr
        dup.document = self.document
        dup.is_flat = self.is_flat
        dup.index = self.index
        dup.is_changed = self.is_changed
        return dup

#    def __str__(self):

    def isEmpty(self):
        no_comment = self.comment.isEmpty()
        no_msgctxt = self.msgctxt.isEmpty()
        no_msgid = self.msgid.isEmpty()
        no_msgstr = self.msgstr.isEmpty()
        is_empty = (no_comment and no_msgctxt and no_msgid and no_msgstr)
        return is_empty

    def removeTag(self, tag:str, text_line:str) -> str:
        txt_line = text_line.replace(tag, "")
        txt_line = txt_line.strip()
        return txt_line

    def blockToComponent(self, text_block, block_index):
        lines = text_block.split("\n")
        comment= TextBlockComponent(Common.COMMENT, self.document, self)
        msgctxt=TextBlockComponent(Common.MSGCTXT, self.document, self)
        msgid=TextBlockComponent(Common.MSGID, self.document, self)
        msgstr=TextBlockComponent(Common.MSGSTR, self.document, self)
        current_ID=None
        line = str('')
        new_line = ""

        for(line_index, line) in enumerate(lines):
            new_line = line
            if (line.startswith(Common.RE_COMMENT_UNUSED)): continue

            if (line.startswith(Common.COMMENT)):
                self.is_fuzzy = (line.lower().find(Common.FUZZY) >= 0)
                current_ID = Common.COMMENT
                comment.setID(Common.COMMENT)
                new_line = line

            if (line.startswith(Common.MSGCTXT)):
                current_ID = Common.MSGCTXT
                msgctxt.setID(Common.MSGCTXT)
                new_line = self.removeTag(Common.MSGCTXT, line)

            if (line.startswith(Common.MSGID)):
                current_ID = Common.MSGID
                msgid.setID(Common.MSGID)
                new_line = self.removeTag(Common.MSGID, line)

            if (line.startswith(Common.MSGSTR)):
                current_ID = Common.MSGSTR
                msgstr.setID(Common.MSGSTR)
                new_line = self.removeTag(Common.MSGSTR, line)


            if (current_ID == Common.COMMENT):
                comment.text_list.append(new_line)
            if (current_ID == Common.MSGCTXT):
                msgctxt.text_list.append(new_line)
            if (current_ID == Common.MSGID):
                msgid.text_list.append(new_line)
            if (current_ID == Common.MSGSTR):
                msgstr.text_list.append(new_line)

        self.comment = comment
        self.msgctxt = msgctxt
        self.msgid = msgid
        self.msgstr = msgstr
        self.is_flat = False
        self.index = block_index

        #self.setComponents(comment, msgctxt, msgid, msgstr, is_flat=False, index=block_index)

    def getFlatTextClone(self):
        copy_item = self.clone()
        #print("getFlatTextClone: copy_item {}".format(copy_item))
        copy_item.is_flat = True
        copy_item.flatComment()
        copy_item.flatMsgctxt()
        copy_item.flatMsgid()
        copy_item.flatMsgstr()
        #print("getFlatTextClone: copy_item flattened {}".format(copy_item))
        return copy_item

    def setFlatText(self):
        ##self.comment.setFlat()
        self.msgctxt.setFlat()
        self.msgid.setFlat()
        self.msgstr.setFlat()
        self.is_flat = True
        self.is_changed = True

    def setFuzzy(self) -> bool:
        if (not self.is_fuzzy):
            self.comment.appendText(Common.FUZZY)
            self.is_fuzzy = True
            return True
        return False

    def unsetFuzzy(self) -> bool:
        if (self.is_fuzzy):
            self.comment.removeText(Common.FUZZY)
            self.is_fuzzy = False
            return True
        return False


    def isFuzzy(self) -> bool:
        return self.is_fuzzy

    def copyContent(self, other):
        self.comment.copyContent(other.comment)
        self.msgctxt.copyContent(other.msgctxt)
        self.msgid.copyContent(other.msgid)
        self.msgstr.copyContent(other.msgstr)

    def copyContent(self, other, id_list):
        if (Common.COMMENT in id_list):
            self.comment.copyContent(other.comment)
        if (Common.MSGCTXT in id_list):
            self.msgctxt.copyContent(other.msgctxt)
        if (Common.MSGID in id_list):
            self.msgid.copyContent(other.msgid)
        if (Common.MSGSTR in id_list):
            self.msgstr.copyContent(other.msgstr)

    def clear(self):
        self.comment.clear()
        self.msgctxt.clear()
        self.msgid.clear()
        self.msgstr.clear()

    def getTextWithIDFlatOrNot(self, is_msgstr_flat):
        text_list = []
        text = self.comment.nonFlatText()
        if (text != None):
            text_list.append(text)

        text = self.msgctxt.nonFlatText()
        if (text != None):
            text_list.append(text)

        text = "{} {}".format(Common.MSGID, self.msgid)
        text_list.append(text)

        text = self.msgstr

        text = "{} {}".format(Common.MSGSTR, )
        text_list.append(text)

        text = os.linesep.join(text_list)
        return text

    def getBlockTextWithID(self):
        return self.getTextWithIDFlatOrNot(False)

    def geBlocktTextWithIDFlat(self):
        text_list = []

        flat_msgid = self.msgid.flatText()
        is_comment_block = (self.index == 0)

        if (not self.comment.isEmpty()):
            text_list.append(self.comment.nonFlatText())
        if (not self.msgctxt.isEmpty()):
            text_list.append(self.msgctxt.getComponentTextWithIDFlat())

        text_list.append(self.msgid.getComponentTextWithID())
        if (not self.msgstr.isEmpty()):
            text_list.append(self.msgstr.getComponentTextWithIDFlat())

        text = os.linesep.join(text_list)
        return text

    def setMSGID(self, new_text):
        self.msgid.setText(new_text)

    def setMSGSTR(self, new_text):
        self.msgstr.setText(new_text)

    def init(self):
        self.comment= TextBlockComponent(Common.COMMENT, self.document, self)
        self.msgctxt=TextBlockComponent(Common.MSGCTXT, self.document, self)
        self.msgid=TextBlockComponent(Common.MSGID, self.document, self)
        self.msgstr=TextBlockComponent(Common.MSGSTR, self.document, self)
        self.is_flat = False
        self.index = 0





class MSGIDcomparator:
   def compare(self, block_x : TextBlock, block_y : TextBlock):
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

   def getTextAsString(self, is_include_first_block : bool = False) -> str:
       output_str : str = ''
       size : int = len(self.block_list)

       for(index, block) in enumerate(self.block_list):
            is_last = (index >= size - 1)
            is_first_block = (index == 0)

            if (not is_include_first_block and is_first_block):
                continue

           # valid : bool = (block != None) and (isinstance(block, TextBlock))
           # if (not valid):
           #     return ""
            #is_last : bool = (index >= size-1)
            output_str += block.getBlockTextWithID()
            if (not is_last):
                output_str += Common.NEWLINE
                output_str += Common.NEWLINE

       return output_str

   def __repr__(self) -> str:
       return self.getTextAsString(is_include_first_block = True)

   def getTextBody(self) -> str:
       self.getTextAsString(is_include_first_block = False)

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
       #sorted_list = sorted(self.block_list, key=lambda x: x.msgid.flatText())
       self.block_list.sort()
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
       block_text : TextBlockComponent
       for(index, block) in enumerate(self.block_list):
           is_first_block = (index == 0)
           is_last = (index >= size-1)
           if (is_first_block):
               block_text  = block.getTextWithID()
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

   def loadPOText(self):
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

   def loadRSTText(self):
       read_text = self.readFile(self.path)
       current_read_text = str(read_text).strip()

       # need_to_change = self.isTextNeededToChange(self.current_read_text)
       # if (need_to_change is False):
       #     print("NO need changing")
       #     return
       if (current_read_text == None):
           raise Exception("Unable to read text from file: {}".format(self.path))

       my_line_list = current_read_text.split(Common.NEWLINE)

       list_funct = [
           RSTUnderlinedHeader(my_line_list),
           RSTTabbedHeader(my_line_list)
                     ]
       current_block : TextBlock = None
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



class RSTParser:
    def __init__(self, my_line_list):
        self.my_line_list : list = my_line_list
        self.previous_line_index : int = 0
        self.current_text_block : list =[]
        self.current_block : TextBlock = None
        self.document : str = None
        self.text_line : str = None
        self.line_index : int = -1

    def setArgs(self, my_line_list):
        self.my_line_list = my_line_list

    def setTextLine(self, text_line):
        self.text_line = text_line

    def setDocument(self, document:object):
        self.document = document

    def setLineIndex(self, line_index):
        self.line_index = line_index

    def setPreviousLineIndex(self, prev_line_index):
        self.previous_line_index = prev_line_index

    def run(self) -> TextBlock:
        pass

    def addBlock(self, header_line) -> TextBlock:
        new_block = TextBlock(self.document)
        new_block.init()
        new_block.setMSGID(header_line)
        new_block.setMSGSTR("")
        return new_block

    def __repr__(self):
        content_list=[]

class RSTUnderlinedHeader(RSTParser):
    def __init__(self, my_line_list):
        super().__init__(my_line_list)
        self.is_underlined_p = re.compile(Common.RE_RST_UNDERLINED)
        self.is_alpha_p = re.compile(Common.RE_IS_ALPHA)

    def run(self) -> TextBlock:

        total_size = len(self.my_line_list)
        has_next_line = (self.line_index + 1 < total_size)
        if (not has_next_line):
            return None

        m4 = self.is_alpha_p.match(self.text_line)
        is_alpha = (m4 != None)

        next_line_index = self.line_index + 1
        next_line = self.my_line_list[next_line_index]

        m2 = self.is_underlined_p.match(next_line)
        is_next_line_underlined = (m2 != None)

        is_title_line = (is_alpha and is_next_line_underlined)
        if (is_title_line):
            #print("tabbed header_line:{}".format(self.text_line))
            return self.addBlock(self.text_line)
        else:
            return None

        # #print("text_line:{}".format(self.text_line))
        # m = self.underlined_p.match(self.text_line)
        # is_potential_header = (self.previous_line_index > 0) and (m != None)
        # #print("first_char: {} is_potential_header:{}".format(first_char, is_potential_header))
        # if (not is_potential_header):
        #     self.previous_line_index = self.line_index
        #     return None
        #
        # header_line : str = None
        # is_title_line = (self.previous_line_index >= 0) and (self.previous_line_index == self.line_index-1)
        # if (is_title_line):
        #     header_line = self.my_line_list[self.previous_line_index]
        #     #print("header_line:{}".format(header_line))
        #     return self.addBlock(header_line)
        # else:
        #     return None
        # #print("header_line:{} text_line:{}".format(header_line, self.text_line))


class RSTTabbedHeader(RSTParser):
    def __init__(self, my_line_list):
        super().__init__(my_line_list)
        self.tabbed_p = re.compile(Common.RE_LEADING_SPACES)
        self.is_underlined_p = re.compile(Common.RE_RST_UNDERLINED)
        self.rst_special_p = re.compile(Common.RE_RST_SPECIAL)
        self.is_alpha_p = re.compile(Common.RE_IS_ALPHA)
        self.dup_list={}

    def countLeadingSpace(self, text_line):
        trimmed = str(text_line).strip()
        count = len(text_line) - len(trimmed)
        return count

    def run(self) -> TextBlock:

        """
        Checking to see if

        current_line and below line has a difference in leading tabbulation (indentation)

        need to check if the line below is not for code

        :return:
        """

        total_size = len(self.my_line_list)
        has_next_line = (self.line_index + 1 < total_size)
        if (not has_next_line):
            return None

        next_line_index = self.line_index + 1
        line_below = self.my_line_list[next_line_index]

        leading_space_count_this_line = self.countLeadingSpace(self.text_line)
        leading_space_count_next_line = self.countLeadingSpace(line_below)

        is_next_line_underlined = Common.isUnderlined(line_below)
        is_ended_full_stop = Common.isEndedFullStop(self.text_line)

        is_ignored = Common.isIgnored(self.text_line)
        is_ignore_start = Common.isIgnoredIfStartsWith(self.text_line)
        is_ignore = (is_ignored or is_ignore_start)

        is_possible_title_line = (leading_space_count_this_line < leading_space_count_next_line) or \
                                    (is_next_line_underlined) and \
                                    (not is_ended_full_stop) and \
                                    (not is_ignore)

        is_title_line = False
        tile_text_line = self.text_line

        if (is_possible_title_line):

            trim_copy = tile_text_line.strip()

            is_keyboard = Common.isMustIncludedKeyboardPart(trim_copy)
            is_alpha = Common.isLeadingAlpha(trim_copy)
            is_in_ignore_startswith = Common.isIgnoredIfStartsWith(trim_copy)
            is_in_ignore_list = Common.isIgnored(trim_copy)
            is_in_duplist = (self.dup_list.get(trim_copy) != None)
            is_ended_with_fullstop = (trim_copy.endswith(Common.DOT))

            is_title_line = (is_keyboard or is_alpha) and \
                            (not is_in_ignore_startswith) and \
                            (not is_in_ignore_list) and \
                            (not is_in_duplist) and \
                            (not is_ended_with_fullstop)

#            is_debug = trim_copy.startswith("Min X/Y and Max X/Y")
#            if (is_debug):
#                 self.document.printTitleOnce()
#                 print("RSTTabbedHeader:[{}], is_title_line:{}".format(trim_copy, is_title_line))
#                 #exit(1)

            if (is_title_line):

                self.dup_list.update({trim_copy:trim_copy})
                #self.document.printTitleOnce()
                #print("title_line:{}".format(trim_copy))
                return self.addBlock(trim_copy)

        return None
        #print("header_line:{} text_line:{}".format(header_line, self.text_line))
