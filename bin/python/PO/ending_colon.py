import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage
from common import Common as cm

class EndingColon(BlankMessage):

    def run(self):

        to_msgid : TextBlockComponent = self.to_block.msgid
        to_msgid_text : str = to_msgid.flatText()

        to_msgstr : TextBlockComponent = self.to_block.msgstr
        to_msgstr_text : str = to_msgstr.flatText()

        msgid_ending_colon = (to_msgid_text.endswith(cm.COLON))
        msgstr_ending_colon = (to_msgstr_text.endswith(cm.COLLON))

        change_msgstr = (not msgid_ending_colon) and (msgstr_ending_colon)
        change_msgid = (msgid_ending_colon) and (not msgstr_ending_colon)

        if (change_msgstr):
            self.to_block.msgstr
