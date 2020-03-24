import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage

class DiffMSGID (BlankMessage):
    def run(self):
        print("{}=>{}".format(self.from_block.msgid.flatText(), self.to_block.msgid.flatText()))
        has_left = (self.from_block != None) and (self.to_block == None)
        if (has_left):
            print("<=={}".format(self.from_block.getTextWithID()))
            return

        has_right = (self.from_block == None) and (self.to_block != None)
        if (has_right):
            print("==>{}".format(self.to_block.getTextWithID()))
            return

        is_diff = (self.from_block.msgid.flatText() != self.to_block.msgid.flatText())
        if (is_diff):
            print("{}<==>{}".format(self.from_block.getTextWithID(), self.to_block.getTextWithID()))
            return


