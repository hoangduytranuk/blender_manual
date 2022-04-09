import re

from cleanref.clean_ref_with_link import CleanRefWithLink
from cleanref.clean_ref_wrong_cases import CleanRefWrongCases
from cleanref.clean_ga_with_link import CleanGAWithLink
from sphinx_intl import catalog as c
from babel.messages import Catalog, Message
from matcher import MatcherRecord
from cleanref.clean_old_ref import CleanOldRefs
from cleanref.clean_fixed_ref import CleanFixedRefs
from cleanref.clean_titles import CleanTitles

from pattern_utils import PatternUtils as pu

class CleaningRefs():
    def __init__(self,
                 input_file=None,
                 output_to_file=None
                 ):
        self.input_file=input_file
        self.output_to_file=output_to_file

    def getListOfPOData(self):
        catalog = c.load_po(self.input_file)
        msg_list = list(catalog._messages.items())
        working_msglist = [msg for (id, msg) in msg_list]
        return (working_msglist, catalog)

    def performTask(self):
        import locale
        def sortName(name_txt):
            new_name = (name_txt.replace(' -- ', ''))
            return new_name

        def extractMsg(entry: tuple):
            mm: MatcherRecord = None
            (loc, mm) = entry
            return mm.txt

        (message_list, data) = self.getListOfPOData()
        # pat_txt = r"((?!:\s)[\`]+)?(:\w+:)?\`(?:\S)+[^\`]+(\`(?<!\s))+([_]+)?([\`]+)?"

        # pat_txt = r"([\`]+)?(:\w+:)?\`(?!\s)+[^\`]+\`(?!\s)+([_]+)?([\`]+)?"
        # pat_txt = r"([\`]+)?(:\w+:)?\`(?!\s)+[^\`]+\`([_]+)?([\`]+)?"
        # pat = re.compile(pat_txt)
        # m: Message = None
        # total_list=[]
        # for m in message_list:
        #     msgid = m.id
        #     is_empty = not bool(msgid)
        #     if is_empty:
        #         continue
        #
        #     msgstr = m.string
        #     id_list = pu.patternMatchAll(pat, msgid)
        #     str_list = pu.patternMatchAll(pat, msgstr)
        #     id_match_list = list(map(extractMsg, id_list.items()))
        #     if id_match_list:
        #         print(id_match_list)
        #     msgstr_match_list = list(map(extractMsg, str_list.items()))
        #     if msgstr_match_list:
        #         print(msgstr_match_list)
        #     total_list.extend(id_match_list)
        #     total_list.extend(msgstr_match_list)
        #
        # result_list = list(set(total_list))
        # result_list.sort()
        # for s in result_list:
        #     print(s)


        list_of_classes = [CleanOldRefs, CleanRefWithLink, CleanRefWrongCases, CleanGAWithLink, CleanFixedRefs]
        list_of_classes = [CleanTitles]
        # list_of_classes = [CleanOldRefs, CleanRefWithLink, CleanRefWrongCases, CleanGAWithLink, CleanFixedRefs]
        global_ref_list=[]
        (message_list, data) = self.getListOfPOData()
        is_changed = False
        for index, cl in enumerate(list_of_classes):
            is_debug = (index == 2)
            if is_debug:
                is_debug = True

            x = cl(
                input_file=self.input_file,
                output_to_file=self.output_to_file
            )
            x.message_list = message_list
            x.performTask()
            global_ref_list.extend(x.vn_ref_list)

            if x.is_changed:
                is_changed = True

        # global_ref_list = list(sorted(global_ref_list, key=sortName))
        mm: MatcherRecord = None
        for (mm) in global_ref_list:
            old_txt = mm.txt
            new_txt = mm.translation
            is_diff = (old_txt != new_txt)
            if is_diff:
                msg = f'old_txt:[{old_txt}]\nnew_txt:[{new_txt}]\n\n'
                print(msg)

        has_output_file = bool(self.output_to_file)
        is_write_changes = (is_changed and has_output_file)
        if is_write_changes:
            # msg = 'There are changes! Do you want to write (Y/n):'
            # confirm = input(msg)
            # is_cancel = (confirm.lower().startswith('n'))
            # if not is_cancel:
            #     exit(0)

            c.dump_po(self.output_to_file, data, line_width=4096)
