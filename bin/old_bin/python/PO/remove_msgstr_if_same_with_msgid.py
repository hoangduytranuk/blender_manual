import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage
from common import Common as cm
from potextcomponent import TextBlockComponent

class RemoveMSGSTRIfSameWithMSGID(BlankMessage):

    def run(self):
        to_msgid : TextBlockComponent = self.to_block.msgid
        to_msgid_text : str = to_msgid.flatText()
        to_msgstr : TextBlockComponent = self.to_block.msgstr
        to_msgstr_text : str = to_msgstr.flatText()

        is_same = (to_msgstr_text == to_msgid_text)
        if (is_same):
            self.change_count += 1
            #print("from is fuzzy: {}\n".format(self.from_block.getTextWithID()))
            self.to_block.msgstr.setEmptyText()
            self.to_block.document.printTitleOnce()
            print("CHANGED: {}\n{}\n".format(self.change_count, self.to_block.getTextWithID()))
            self.to_block.document.setDirty()

