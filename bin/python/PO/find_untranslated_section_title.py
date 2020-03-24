import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage
from potextcomponent import TextBlockComponent
from common import Common as cm

class FindUntranslatedSectionTitle(BlankMessage):
    def run(self):

        to_msgid : TextBlockComponent = self.to_block.msgid
        to_msgid_text : str = to_msgid.flatText()

        to_msgstr : TextBlockComponent = self.to_block.msgstr
        to_msgstr_text : str = to_msgstr.flatText()

        #is_untranslated = (to_msgstr_text.startswith("\"--")) or (to_msgstr_text.startswith("\" --"))
        is_untranslated = (cm.SECTION_TITLE_RE.search(to_msgstr_text) != None)
        if (is_untranslated):
            self.change_count += 1
            self.to_block.document.printTitleOnce()
            print("{}".format(to_msgstr_text))

