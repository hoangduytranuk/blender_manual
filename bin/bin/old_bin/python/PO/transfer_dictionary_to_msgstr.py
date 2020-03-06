import sys
sys.path.append("/home/htran/bin/python/PO")
from blankmessage import BlankMessage

class TransferDictionaryToMSGSTR (BlankMessage):

    def setDictionary(self, dictionary : dict):
        self.dictionary = dictionary

    def fixDot(self, from_text:str, to_text:str) -> str:
        DOT="."

        is_from_ended_dot = from_text.endswith(DOT)
        is_to_ended_dot = to_text.endswith(DOT)
        is_change = (is_from_ended_dot and not is_to_ended_dot)

        if (not is_change):
            return to_text

        new_text = "{}{}".format(to_text, DOT)
        return new_text

    def run(self):
        valid_dict = (self.dictionary != None) and (len(self.dictionary) > 0)
        if (not valid_dict):
            return

        #print("Dictionary is VALID")
        to_msgid : TextBlockComponent = self.to_block.msgid
        to_msgstr : TextBlockComponent = self.to_block.msgstr

        is_untranslated = to_msgstr.isConsideredEmpty()

        #print("is_untranslated:{}\n{}".format(is_untranslated, self.to_block.getTextWithID()))
        if (not is_untranslated):
            return

        to_key : str = to_msgid.flatText()
        has_translation = (to_key in self.dictionary)
        if (not has_translation):
            find_all_list = re.findall(cm.RE_TODO, to_key, re.I)
            has_todo = len(find_all_list) > 0
            #print("has_todo:{}, to_key:{}".format(has_todo, to_key))
            if (has_todo):
                for found_word in find_all_list:
                    to_key = re.sub(found_word, cm.TODO_TRANSLATED, to_key)
                print("changed to_key:{}".format(to_key))
                self.toBlockSetMSGSTR(to_key);
            return

        dict_value = self.dictionary[to_key]
        dict_value_dotted_if_any = self.fixDot(to_key, dict_value)
        self.toBlockSetMSGSTR(dict_value_dotted_if_any);
