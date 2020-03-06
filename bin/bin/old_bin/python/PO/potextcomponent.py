print("Importing TextBlockComponent")
import re
#import sys
import os
import copy

#from blocktype import BlockType
from common import Common as cm


class TextBlockComponent():
    def __init__(self, ID , document , block ):
        self.ID  = ID
        self.is_flat  = False
        self.text_list  = []
        self.document  = document
        self.block  = block

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


    def __gt__(self, other ) -> bool:
        return self.__cmp__(other) > 1

    def __eq__(self, other ):
        return self.__cmp__(other) > 1

    def __lt__(self, other ):
        return self.__cmp__(other) < 1

    def debugstr(self) -> str:
        text_list=[]
        text_list.append("ID:{}".format(self.ID))
        text_list.append("is_flat:{}".format(self.is_flat))

        text_list.append("text_list:{}".format(''.join(self.text_list)))
        text_list.append("document:{}".format(os.linesep.join(self.document.path)))

        return os.linesep.join(text_list)


    #transfer to this
    def copyContent(self, other ) -> bool:
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

    def setID(self, ID ):
        self.ID = ID

    def appendText(self, text:str) -> bool:
        if (text == None):
            return False

        is_first_line=(self.text_list == [])
        has_leading_space = text.startswith(cm.SPACE)
        append_text = text if (has_leading_space or is_first_line) else " {}".format(text)
        self.text_list.append(append_text)
        return True

    def getList(self):
        return self.text_list

    def setList(self, new_list ):
        self.text_list.clear()
        self.text_list = list(new_list)

    def setText(self, new_text ):
        self.text_list.clear()
        self.text_list.append(new_text)

    def setFlat(self):
        self.is_flat = True
        self.text_list[:]=[]
        self.text_list.append(self.flatText())

    def getFlatTextClone(self):
        copy_item  = self.clone()
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

    def stripID(self, text_line ) -> [str, bool]:
        line1  =re.sub(self.ID, cm.RE_EMPTYSTR, text_line)
        is_empty  = (len(line1) == 0)
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

        mlist  =[]
        for(index, text_line) in enumerate(self.text_list):
            try:
                #print("flatText Before stripQuote:[{}]".format(text_line))
                txt_line = cm.stripQuote(text_line)
                #print("flatText After stripQuote:[{}]".format(txt_line))
                mlist.append(txt_line)
            except Exception as e:
                self.document.printTitleOnce()
                print("Exception: {}".format(e))
                print("SOMETHING WRONG text_line: {}".format(text_line))
                exit(1)
        text_line  = ''.join(mlist)
        text_line = "{}{}{}".format(cm.QUOTE, text_line, cm.QUOTE)
        #print("text_line after joined: [{}]".format(text_line))
        return text_line

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

        text_line = ""
        if (is_flat):
            text_line = self.flatText()
        else:
            text_line = os.linesep.join(self.text_list)

        text_line = "{} {}".format(self.ID,text_line)
        return text_line
