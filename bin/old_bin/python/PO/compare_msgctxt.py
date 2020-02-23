import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage
from common import Common as cm
from potextcomponent import TextBlockComponent

class CompareMSGCTXT (BlankMessage):

    def run(self):
        from_msgid : TextBlockComponent = self.from_block.msgid
        from_msgid_text : str = from_msgid.flatText()

        to_msgid : TextBlockComponent = self.to_block.msgid
        to_msgid_text : str = to_msgid.flatText()


        is_same_id = (from_msgid_text == to_msgid_text)
        from_has_msgctxt = is_same_id and (not self.from_block.msgctxt.isEmpty())
        to_has_msgctxt = is_same_id and (not self.to_block.msgctxt.isEmpty())

        both_has_msgctxt = (from_has_msgctxt and to_has_msgctxt)

        is_change_diff = is_change = is_change_copy_or_remove = False
        if (both_has_msgctxt):
            from_msgctxt_text = self.from_block.msgctxt.flatText()
            to_msgctxt_text = self.to_block.msgctxt.flatText()
            is_change_diff = (from_msgctxt_text != to_msgctxt_text)
        else:
            take_copy_from_from = (from_has_msgctxt and not to_has_msgctxt)
            remove_from_to = (not from_has_msgctxt and to_has_msgctxt)
            is_change_copy_or_remove = (take_copy_from_from or remove_from_to)

        is_change = (is_change_diff or is_change_copy_or_remove)
        if (is_change):
            self.change_count += 1

            if (is_change_diff or take_copy_from_from):
                self.to_block.msgctxt = self.from_block.msgctxt
            else:
                self.to_block.msgctxt.clear()

            self.to_block.document.printTitleOnce()
            print("CHANGED: {}\n{}\n".format(self.change_count, self.to_block.getTextWithID()))
            self.to_block.document.setDirty()

