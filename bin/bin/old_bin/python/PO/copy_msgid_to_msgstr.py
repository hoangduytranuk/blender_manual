import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage
from common import Common as cm
from potextcomponent import TextBlockComponent

class CopyMSGID_to_MSGSTR(BlankMessage):

    def run(self):

        to_msgid : TextBlockComponent = self.to_block.msgid
        to_msgid_text : str = to_msgid.flatText()

        to_msgstr : TextBlockComponent = self.to_block.msgstr
        to_msgstr_text : str = to_msgstr.flatText()

        has_percentage = (to_msgid_text.find(cm.PERCENTAGE) >= 0)
        has_star_char = (to_msgid_text.find(cm.STAR) >= 0)
        has_blend_file = (to_msgid_text.find(cm.BLEND_FILE) >= 0)
        has_digits = (re.match(cm.RE_NUMBER, to_msgid_text) != None)
        has_brackets = (re.search(cm.RE_BRACKET, to_msgid_text, flags=re.DOTALL) != None)
        has_brackets = (re.search(cm.RE_BRACKET, to_msgid_text) != None)
        has_xxx = (re.match(cm.RE_XXX, to_msgid_text) != None)
        has_dotdot = (re.match(cm.RE_DOTDOT, to_msgid_text) != None)
        has_xray = (re.match(cm.RE_XRAY, to_msgid_text) != None)
        has_dd = (re.match(cm.RE_DD, to_msgid_text) != None)
        has_ref = (re.match(cm.RE_REF, to_msgid_text) != None)
        has_menu = (re.match(cm.RE_MENU, to_msgid_text) != None)
        has_url = (re.match(cm.RE_URL, to_msgid_text) != None)
        #has_mouse_button = (re.match(cm.RE_MOUSE_BUTTON, to_msgid_text) != None)
        has_doc = (re.match(cm.RE_DOC, to_msgid_text) != None)

        #has_hyphen = (re.match(cm.RE_HYPHEN, to_msgid_text) != None)


        has_colon = (to_msgid_text.find(":") >= 0)

        has_copy_char = (
                        has_percentage or
                         #has_star_char or
                         #has_blend_file or
                         has_colon or
                         #has_brackets or
                         has_xxx or
                         #has_dotdot or
                         #has_xray or
                         #has_dd or
                         #has_ref or
                         #has_menu or
                         #has_url or
                         has_url
                         #has_mouse_button or
                         #has_doc
                         )

        is_empty_msgstr = (self.to_block.msgstr.isConsideredEmpty())

        #is_copy = (is_empty_msgstr)
        is_copy = (has_copy_char and is_empty_msgstr)

#        is_debug = (to_msgid_text.find("+X") >= 0)
#        if (is_debug):
#            print("TO_BLOCK: {}\n{}\nhas_copy_char:{}\nis_empty_msgstr:{}\nis_copy:{}".format(self.change_count, self.to_block.getTextWithID(), has_copy_char, is_empty_msgstr, is_copy))
#            print("to_msgid_text:[{}]".format(to_msgid_text))
#            print("to_msgstr_text:[{}]".format(to_msgstr_text))

        if (not is_copy): return

        self.change_count += 1
        self.to_block.document.printTitleOnce()

        self.to_block.msgstr.setText( self.to_block.msgid.flatText())
        print("CHANGED: {}\n{}\n".format(self.change_count, self.to_block.getTextWithID()))
        self.to_block.document.setDirty()
