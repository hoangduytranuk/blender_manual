import copyreg
import os
import re

from babel.messages.catalog import Catalog, Message
from sphinx_intl import catalog as c
from potask_base import POTaskBase, POResultRecord
from translation_finder import TranslationFinder
from reflist import RefList
from definition import Definitions as df, RefType
from nocasedict import NoCaseDict
from paragraph import Paragraph as PR
from ignore import Ignore as ig
from pattern_utils import PatternUtils as pu
from common import Common as cm

class PrintTitledWords(POTaskBase):
    def __init__(self,
                 output_to_file=None,
                 translation_file=None
                 ):
        POTaskBase.__init__(
                self,
                output_to_file=output_to_file, # file to write the output to, while testing
                translation_file=translation_file # file blender_manual.po in locale/vi/LC_MESSAGES
        )
        self.tf = TranslationFinder(
            apply_case_matching_orig_txt=self.apply_case_matching_orig_txt
        )

    def isThereTitledWords(self, msgid: str, msgstr: str):
        def isFirstLetterUppercase(x):
            is_upper = (bool(x) and x[0].isupper())
            return is_upper

        def isInList(x, str_list):
            lower_x = x.lower()
            lower_x_without_the = cm.removeTheWord(lower_x)

            for tran_word in str_list:
                tran_lower = tran_word.lower()
                is_in = (lower_x_without_the in tran_lower) or (tran_lower in lower_x_without_the)
                if is_in:
                    return True

            return False

        def getRefList(msg_txt):
            ref_list = RefList(msg=msg_txt, keep_orig=False, tf=self.tf)
            ref_list.parseMessage(
                is_ref_only=True,
                include_brackets=True,
                pattern_list=df.no_bracket_pattern_list
            )
            return ref_list

        from itertools import groupby
        try:
            is_debug = ('Add, Subtract, Multiply, Screen' in msgid)
            if is_debug:
                print('Debug')

            id_ref_dict = getRefList(msgid)
            str_ref_dict = getRefList(msgstr)

            str_ref_list = []
            for loc, mm in str_ref_dict.items():
                txt = mm.txt
                str_ref_list.append(txt)

            punctuated_word = re.compile(f'[\W]+(\s+|\b|$)')
            unparsed_list = id_ref_dict.local_ref_map.getRawUnmarkedPartsAsList()
            breakup_by_punctuation_list = []
            for loc, txt in unparsed_list:
                has_punct = (punctuated_word.search(txt) is not None)
                if has_punct:
                    list_puncted_words = punctuated_word.split(txt)
                    txt_l = [x for x in list_puncted_words if bool(x.strip())]
                    breakup_by_punctuation_list.extend(txt_l)
                else:
                    breakup_by_punctuation_list.append(txt)

            groups = []
            for txt in breakup_by_punctuation_list:
                delim_list = txt.split()
                # for key, group in groupby(text_without_ref.split(), lambda x: x[0].isupper()):
                for key, group in groupby(delim_list, isFirstLetterUppercase):
                    if key:
                        groups.append(' '.join(list(group)))

            result_list = []
            for word in groups:
                is_in_str = isInList(word, str_ref_list)
                if is_in_str:
                    continue

                start = msgid.find(word)
                end = (start + len(word))
                entry = ((start, end), word)
                result_list.append(entry)

            return result_list
        except Exception as e:
            df.LOG(e)
            raise e


    def performTask(self):
        self.setFiles()
        home = os.environ['BLENDER_MAN_EN']
        default_tran_file = os.path.join(home, 'locale/vi/LC_MESSAGES/blender_manual.po')
        if not bool(self.tran_file):
            self.tran_file = default_tran_file

        changed = False
        m: Message = None
        tran_file_data = c.load_po(self.tran_file)
        for index, m in enumerate(tran_file_data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            auto_comment = m.auto_comments
            user_comment = m.user_comments
            locations = m.locations
            msgid = m.id
            is_fuzzy = m.fuzzy
            msgstr = m.string

            has_translation = bool(msgstr)
            if not has_translation:
                continue

            is_dup_intent = self.isDupIntentionally(msgid, msgstr)
            if is_dup_intent:
                continue

            # is_debug = ('Prepare the area you would' in msgid)
            # if is_debug:
            #     print('Debug')

            list_of_titled_words = self.isThereTitledWords(msgid, msgstr)
            has_titled_words = (len(list_of_titled_words) > 0)
            if not has_titled_words:
                continue

            changed = True
            r = POResultRecord(index + 1, msgid, msgstr, alternative_tran=list_of_titled_words, alternative_label="Titled Word List")
            self.append(r)

        is_save = (changed) and (self.opo_path)
        if is_save:
            print(f'Dumping po data to: {self.opo_path}')
            # c.dump_po(self.opo_path, tran_file_data)
        else:
            self.showResult()