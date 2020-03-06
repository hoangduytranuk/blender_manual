import sys
sys.path.append("/home/htran/bin/python/PO")
from potextblock import TextBlock
class BlankMessage:
    def __init__(self):
        self.from_block = None;
        self.to_block = None;
        self.is_transfer_changes  = False
        self.change_count = 0
        #self.from_block

    def setTransferChanges(self):
        self.is_transfer_changes  = True

    def removeTransferChanges(self):
        self.is_transfer_changes  = False

    def setArgs(self, from_text_block : TextBlock, to_text_block : TextBlock):
        self.from_block = from_text_block
        self.to_block = to_text_block

    def toBlockSetMSGSTR(self, new_text, addition_msg=None):
        print("toBlockSetMSGSTR:")
        self.to_block.document.printTitleOnce()
        self.change_count += 1
        if (not addition_msg == None):
            print(addition_msg)
        print("FROM: {}\n{}".format(self.change_count, self.to_block.geBlocktTextWithIDFlat()))
        self.to_block.msgstr.setText(new_text)
        print("CHANGED TO: {}\n{}".format(self.change_count, self.to_block.geBlocktTextWithIDFlat()))
        self.to_block.document.setDirty()

    def toBlockSetMSGID(self, new_text, addition_msg=None):
        print("toBlockSetMSGID:")
        self.to_block.document.printTitleOnce()
        self.change_count += 1
        if (not addition_msg == None):
            print(addition_msg)
        print("FROM: {}\n{}".format(self.change_count, self.to_block.geBlocktTextWithIDFlat()))
        self.to_block.msgid.setText(new_text)
        print("CHANGED TO: {}\n{}".format(self.change_count, self.to_block.geBlocktTextWithIDFlat()))
        self.to_block.document.setDirty()

    def toBlockSetComment(self, comment,  addition_msg=None):
        print("toBlockSetComment:")
        self.to_block.document.printTitleOnce()
        self.change_count += 1
        if (not addition_msg == None):
            print(addition_msg)
        print("FROM: {}\n{}".format(self.change_count, self.to_block.geBlocktTextWithIDFlat()))
        self.to_block.comment.setText(comment)
        print("CHANGED TO: {}\n{}".format(self.change_count, self.to_block.geBlocktTextWithIDFlat()))
        self.to_block.document.setDirty()

    def toBlockSetFuzzy(self,  value,  addition_msg=None):
        print("toBlockSetFuzzy:")
        self.to_block.document.printTitleOnce()
        self.change_count += 1
        if (not addition_msg == None):
            print(addition_msg)
        print("FROM: {}\n{}".format(self.change_count, self.to_block.geBlocktTextWithIDFlat()))
        self.to_block.setFuzzyByValue(value)
        print("CHANGED TO: {}\n{}".format(self.change_count, self.to_block.geBlocktTextWithIDFlat()))
        self.to_block.document.setDirty()

def run(self):
        pass
