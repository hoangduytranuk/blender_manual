import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage

class CompareMSGID (BlankMessage):
    def run(self):
        from_msgid = self.from_block.msgid
        from_msgid_text = from_msgid.flatText()
        from_msgstr = self.from_block.msgstr
        from_msgstr_text = from_msgstr.flatText()
        #from_comment = self.from_block.comment.flatText()
        from_fuzzy = self.from_block.isFuzzy()

        to_msgid = self.to_block.msgid
        to_msgid_text = to_msgid.flatText()
        to_msgstr = self.to_block.msgstr
        to_msgstr_text = to_msgstr.flatText()
        #to_comment = self.to_block.comment.flatText()
        to_fuzzy = self.to_block.isFuzzy()

        is_msgstr_diff = (from_msgid_text == to_msgid_text) and (from_msgstr_text != to_msgstr_text)
        #is_msgid_diff = (from_msgid_text != to_msgid_text)
        #is_comment_diff = (from_comment != to_comment)
        is_fuzzy_diff = (from_fuzzy != to_fuzzy)

        #is_diff = (is_msgid_diff or is_comment_diff)
        is_diff = (is_msgstr_diff or is_fuzzy_diff)
        if (not is_diff): return

        if (is_fuzzy_diff):
            self.to_block.setFuzzy()
#        if (is_comment_diff):
#            self.toBlockSetComment(self.from_block.comment)
#        if (is_msgid_diff):
#            self.toBlockSetMSGID(from_msgid_text)

        #print("{} => {}".format(from_comment, to_comment))
        print("-" * 80)
        self.toBlockSetMSGSTR(from_msgstr_text)
