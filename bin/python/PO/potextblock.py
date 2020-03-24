print("Importing TextBlock")
import os
import re
from common import Common
from potextcomponent import TextBlockComponent

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
                self.is_fuzzy = (re.search(Common.FUZZY,  line,  re.I) != None)
#                if (self.is_fuzzy):
#                    print("blockToComponent FUZZY text_block:{}".format(text_block))
                current_ID = Common.COMMENT
                comment.setID(Common.COMMENT)

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
#        if (self.is_fuzzy):
#            print("blockToComponent IS_FUZZY: {}".format(self.getTextWithID()))


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

    def setFuzzyByValue(self,  value) -> bool:
        if (value):
            self.setFuzzy()
        else:
            self.unsetFuzzy()

    def setFuzzy(self) -> bool:
        if (not self.is_fuzzy):
            self.comment.appendText(Common.FUZZY)
            self.is_fuzzy = True
            return True
        return False

    def unsetFuzzy(self) -> bool:
        if (self.is_fuzzy):
            #print("unsetFuzzy Comment:{}".format(self.comment))
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

    def copyContentUsingIDList(self, other, id_list):
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

        text = self.msgid.getComponentTextWithID()
        text_list.append(text)

        if (is_msgstr_flat):
            text = self.msgstr.getComponentTextWithIDFlat()
            #print("is_msgstr_flat:{}".format(text))
        else:
            text = self.msgstr.nonFlatText()
            #print("NOT is_msgstr_flat:{}".format(text))

        if (text != None):
            text_list.append(text)

        #self.document.printTitleOnce()
        #print("getTextWithIDFlatOrNot: text_list={}, is_msgstr_flat={}".format(text_list, is_msgstr_flat))
        text = os.linesep.join(text_list)
        return text

    def getTextWithID(self):
        return self.getTextWithIDFlatOrNot(False)

    def geBlocktTextWithIDFlat(self):
        text_list = []

        #flat_msgid = self.msgid.flatText()
        #is_comment_block = (self.index == 0)

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
