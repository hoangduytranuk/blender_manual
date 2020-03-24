import sys
import os
from common import Common as cm

class RSTRSTTextBlock (Common):

    def __init__(self, document):
        self.document : object
        self.header : str = None
        self.text_list : list = []
        self.is_flat = False
        self.index = -1
        self.is_changed = False

    def isHeaderEmpty(self) -> bool:
        is_empty:bool = (self.header == None) or (len(self.header)  == 0):
        return is_empty
    
    def isTextEmpty(self) -> bool:
        is_empty:bool = (self.text_list == None) or (len(self.text_list)  == 0):
        return is_empty
        
    def __repr__(self):
        mylist=[]
        if (not self.isHeaderEmpty()):
            mylist.append(self.header)
            mylist.append(Common.NEWLINE)

        if (not self.isTextEmpty()):
            mylist.append(self.text_list)
            mylist.append(Common.NEWLINE)

        mylist.append(Common.NEWLINE)
        out_str = ''.join(mylist)
        return out_str

    def __gt__(self, other_block):
        try:
            if (other_block == None):
                return True;

            this_header : str = self.header
            other_header : str = other_block.header
            is_greater : bool = (this_header > other_header)
            return is_greater
        except:
            raise Exception("Unable to perform > comparison between {} and {}".format(self, other_block))

    def __eq__(self, other_block):
        try:
            if (other_block == None):
                return False;

            this_header : str = self.header
            other_header : str = other_block.header
            is_equal : bool = (this_header == other_header)
            return is_equal
        except:
            raise Exception("Unable to perform == comparison between {} and {}".format(self, other_block))

    def __lt__(self, other_block):
        try:
            if (other_block == None):
                return False;

            this_header : str = self.header
            other_header : str = other_block.header
            is_lesser : bool = (this_header < other_header)
            return is_lesser
        except:
            raise Exception("Unable to perform < comparison between {} and {}".format(self, other_block))

    def clone(self):
        dup = RSTTextBlock()
        dup.header  = copy.deepcopy(self.header)
        dup.text_list = copy.deepcopy(self.text_list)
        dup.document = self.document        
        dup.is_flat = self.is_flat
        dup.index = self.index
        dup.is_changed = self.is_changed        
        return dup

#    def __str__(self):

    def isEmpty(self):
        no_header = self.isHeaderEmpty()
        no_text_list = self.isTextEmpty()
        is_empty = (no_header and no_text_list and no_msgid and no_msgstr)
        return is_empty

    def blockToComponent(self, text_block, block_index):
        lines = text_block.split("\n")
        header= RSTTextBlockComponent(Common.COMMENT, self.document, self)
        text_list=RSTTextBlockComponent(Common.MSGCTXT, self.document, self)
        msgid=RSTTextBlockComponent(Common.MSGID, self.document, self)
        msgstr=RSTTextBlockComponent(Common.MSGSTR, self.document, self)
        current_ID=None
        line = str('')
        new_line = ""

        for(line_index, line) in enumerate(lines):
            new_line = line
            if (line.startswith(Common.RE_COMMENT_UNUSED)): continue
                
            if (line.startswith(Common.COMMENT)):
                current_ID = Common.COMMENT
                header.setID(Common.COMMENT)
                new_line = line

            if (line.startswith(Common.MSGCTXT)):
                current_ID = Common.MSGCTXT
                text_list.setID(Common.MSGCTXT)
                new_line1 = line.replace(Common.MSGCTXT, Common.SPACE)
                new_line2 = new_line1.replace(Common.QUOTE, Common.SPACE)
                new_line = new_line2.strip()

            if (line.startswith(Common.MSGID)):
                current_ID = Common.MSGID
                msgid.setID(Common.MSGID)
                new_line1 = line.replace(Common.MSGID, Common.SPACE)
                new_line2 = new_line1.replace(Common.QUOTE, Common.SPACE)
                new_line = new_line2.strip()
                #print("replaced: [{}] [{}] =>[{}]".format(Common.MSGID, Common.SPACE, new_line))

            if (line.startswith(Common.MSGSTR)):
                current_ID = Common.MSGSTR
                msgstr.setID(Common.MSGSTR)
                new_line1 = line.replace(Common.MSGSTR, Common.RE_EMPTYSTR)
                new_line2 = new_line1.replace(Common.QUOTE, Common.SPACE)
                new_line = new_line2.strip()

            if (current_ID == Common.COMMENT):
                header.text_list.append(new_line.strip())
            if (current_ID == Common.MSGCTXT):
                text_list.text_list.append(new_line.strip())
            if (current_ID == Common.MSGID):
                msgid.text_list.append(new_line.strip())
            if (current_ID == Common.MSGSTR):
                msgstr.text_list.append(new_line.strip())

        #print("new block:\nCOMMENT:{}\nMSGCTXT:{}\nMSGID:{}\nMSGSTR:{}".format(str(header), str(text_list), str(msgid), str(msgstr)))
        self.header = header
        self.text_list = text_list
        self.header = msgid
        self.msgstr = msgstr
        self.is_flat = False
        self.index = block_index

        #self.setComponents(header, text_list, msgid, msgstr, is_flat=False, index=block_index)

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
        ##self.header.setFlat()
        self.text_list.setFlat()
        self.header.setFlat()
        self.msgstr.setFlat()
        self.is_flat = True
        self.is_changed = True

    def copyContent(self, other):
        self.header.copyContent(other.header)
        self.text_list.copyContent(other.text_list)
        self.header.copyContent(other.msgid)
        self.msgstr.copyContent(other.msgstr)

    def copyContent(self, other, id_list):
        if (Common.COMMENT in id_list):
            self.header.copyContent(other.header)
        if (Common.MSGCTXT in id_list):
            self.text_list.copyContent(other.text_list)
        if (Common.MSGID in id_list):
            self.header.copyContent(other.msgid)
        if (Common.MSGSTR in id_list):
            self.msgstr.copyContent(other.msgstr)

    def clear(self):
        self.header.clear()
        self.text_list.clear()
        self.header.clear()
        self.msgstr.clear()
        
    def getTextWithID(self):
        text_list = []
        is_header_block = (self.index == 0)
        
        if (not self.isHeaderEmpty()):
            text_list.append(self.header.nonFlatText())
        if (not self.isHeaderEmpty()):
            text_list.append(self.header.getTextWithID())
        if (not self.msgstr.isEmpty()):
            text_list.append(self.msgstr.getTextWithID())
        
        text = os.linesep.join(text_list)
        return text

    def geBlocktTextWithIDFlat(self):
        text_list = []
        
        flat_msgid = self.header()
        is_header_block = (self.index == 0)
        
        if (not self.isHeaderEmpty()):
            text_list.append(self.header.nonFlatText())
        if (not self.isHeaderEmpty()):
            text_list.append(self.header.getComponentTextWithIDFlat())
        if (not self.msgstr.isEmpty()):
            text_list.append(self.msgstr.getComponentTextWithIDFlat())
        
        text = os.linesep.join(text_list)        
        return text

    def setMSGID(self, new_text):
        self.header.setText(new_text)

    def setMSGSTR(self, new_text):
        self.msgstr.setText(new_text)

    def init(self):
        self.header= RSTTextBlockComponent(Common.COMMENT, self.document, self)
        self.text_list=RSTTextBlockComponent(Common.MSGCTXT, self.document, self)
        self.header=RSTTextBlockComponent(Common.MSGID, self.document, self)
        self.msgstr=RSTTextBlockComponent(Common.MSGSTR, self.document, self)
        self.is_flat = False
        self.index = 0
