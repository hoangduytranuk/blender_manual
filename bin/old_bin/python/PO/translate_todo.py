import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage

class TranslateTODO(BlankMessage):
    replace_list = {
        r"\btodo\b" : "Nội dung cần viết thêm",
        "See :doc:" : "Xin xem thêm :doc:",
        r"\bSee\b" : "Xin xem",
        #r"\band\b" : "và",
        #r"\bor\b" : "hoặc",
        r"documentation" : "tài liệu"
                         }

    def replaceToDo(self, list_of_text_to_replace, replace_value, text_line, extra_msg) -> str:
        for found_word in list_of_text_to_replace:
            text_line = re.sub(found_word, replace_value, text_line)
        #print("changed text_line:{}".format(text_line))
        self.toBlockSetMSGSTR(text_line, extra_msg);

    def run(self):
        to_msgid : TextBlockComponent = self.to_block.msgid
        to_msgstr : TextBlockComponent = self.to_block.msgstr

        to_msgid_text : str = to_msgid.flatText()
        to_msgstr_text : str = to_msgstr.flatText()

        for key, value in self.replace_list.items():
            todo_msgid_list = re.findall(key, to_msgid_text, re.I)
            todo_msgstr_list = re.findall(key, to_msgstr_text, re.I)

            has_todo_in_msgid = (len(todo_msgid_list) > 0)
            has_todo_in_msgstr = (len(todo_msgstr_list) > 0)
            is_msgid_untranslated = to_msgstr.isConsideredEmpty()

            if (has_todo_in_msgstr):
                self.replaceToDo(todo_msgstr_list, value, to_msgstr_text, "TODO in MSGSTR")
            elif (has_todo_in_msgid and is_msgid_untranslated):
                self.replaceToDo(todo_msgid_list, value, to_msgid_text, "TODO in MSGID and Untranslated")
