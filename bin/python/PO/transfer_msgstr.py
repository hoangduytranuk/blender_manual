import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage

class TransferMSGSTR (BlankMessage):
    def run(self):
        from_msgid = self.from_block.msgid
        from_msgid_text = from_msgid.flatText()
        from_msgstr = self.from_block.msgstr
        from_msgstr_text = from_msgstr.flatText()


        to_msgid = self.to_block.msgid
        to_msgid_text = to_msgid.flatText()
        to_msgstr = self.to_block.msgstr
        to_msgstr_text = to_msgstr.flatText()

        is_same_id = (to_msgid_text == from_msgid_text)
        is_diff = is_same_id and (from_msgstr_text != to_msgstr_text)
        if (not is_diff): return

        self.toBlockSetMSGSTR(from_msgstr_text)
#
#        self.change_count += 1
#        #print("{}\n{}=>\n{}\n\n".format(self.change_count, self.from_block.getTextWithID(), self.to_block.getTextWithID()))
##        if (self.is_transfer_changes):
#
#        self.to_block.document.printTitleOnce()
#        self.to_block.msgstr = self.from_block.msgstr
#        #self.to_block.copyContent(self.from_block, id_list)
#        print("CHANGED: {} old msgstr:{}\n{}\n".format(self.change_count,to_msgstr_text, self.to_block.getTextWithID()))
#        self.to_block.document.setDirty()
