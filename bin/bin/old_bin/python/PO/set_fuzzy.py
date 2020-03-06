import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage
from common import Common as cm
from potextcomponent import TextBlockComponent

class SetFuzzy(BlankMessage):

    def run(self):
        from_msgid : TextBlockComponent = self.from_block.msgid
        from_msgid_text : str = from_msgid.flatText()

        to_msgid : TextBlockComponent = self.to_block.msgid
        to_msgid_text : str = to_msgid.flatText()

        is_same_id=(from_msgid_text == to_msgid_text)

        is_from_fuzzy = (is_same_id and self.from_block.isFuzzy())
        is_to_fuzzy = (is_same_id and self.to_block.isFuzzy())

        is_set_to_fuzzy = (is_from_fuzzy and not is_to_fuzzy)
        is_remove_to_fuzzy = (not is_from_fuzzy and is_to_fuzzy)

        if (is_set_to_fuzzy):
            is_changed = self.to_block.setFuzzy()
            if (is_changed):
                self.change_count += 1
                #print("from is fuzzy: {}\n".format(self.from_block.getTextWithID()))
                self.to_block.document.printTitleOnce()
                print("CHANGED: {}\n{}\n".format(self.change_count, self.to_block.getTextWithID()))
                self.to_block.document.setDirty()

        if (is_remove_to_fuzzy):
            is_changed = self.to_block.unsetFuzzy()
            if (is_changed):
                self.change_count += 1
                #print("from is fuzzy: {}\n".format(self.from_block.getTextWithID()))
                self.to_block.document.printTitleOnce()
                print("CHANGED: {}\n{}\n".format(self.change_count, self.to_block.getTextWithID()))
                self.to_block.document.setDirty()

#        is_from_fuzzy = self.from_block.isFuzzy()
#        is_to_fuzzy = self.to_block.isFuzzy()
#        is_change = is_same_id and (is_from_fuzzy and not is_to_fuzzy)
#
#        if (is_from_fuzzy or is_to_fuzzy):
#            print("{}\n{}=>\n{}\n\n".format(self.from_block.getTextWithID(), self.to_block.getTextWithID()))
#
#        if (is_change):
#            self.to_block.setFuzzy()
#            self.to_block.document.printTitleOnce()
#            print("CHANGED: {}\n{}\n".format(self.change_count, self.to_block.getTextWithID()))
#            self.to_block.document.setDirty()
