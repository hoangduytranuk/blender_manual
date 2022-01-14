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

class PrintCurrentBrackets(POTaskBase):
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

# manual/glossary/index.rst

    def isThereBracket(self, txt):
        try:
            ref_list = RefList(msg=txt, keep_orig=False, tf=self.tf)
            ref_list.parseMessage(
                is_ref_only=True,
                include_brackets=True,
                pattern_list=df.no_bracket_pattern_list
            )

            brk_count = 0
            unparsed_dict = ref_list.local_ref_map.getUnmarkedPartsAsDict(removing_symbols=False, reversing=False)
            txt_list = []
            for loc, mm in unparsed_dict.items():
                mm_txt = mm.txt
                txt_list.append(mm_txt)

            text_without_ref = ' '.join(txt_list)
            bracket_list = df.ARCH_BRAKET_SINGLE.findall(text_without_ref)
            brk_count += len(bracket_list)

            return brk_count
        except Exception as e:
            df.LOG(e)
            return False

    def checkIfThereIsBrackets(self, msgid, msgstr):

        msgid_count = self.isThereBracket(msgid)
        msgstr_count = self.isThereBracket(msgstr)
        is_same_count = (msgid_count == msgstr_count)
        if not is_same_count:
            msgstr_list = (msgstr.split(' -- '))
            has_separator = (len(msgstr_list) > 1)
            is_repeated_intentionally = (msgid in msgstr_list)
            if is_repeated_intentionally:
                return True

        return is_same_count

    def checkIfThereIsTerm(self, txt):
        ref_list = RefList(msg=txt, keep_orig=False, tf=self.tf)
        ref_list.parseMessage(
            is_ref_only=True,
            include_brackets=True,
            # pattern_list=df.no_bracket_pattern_list
            pattern_list=df.no_bracket_and_quoted_pattern_list
        )

        unparsed_dict = ref_list.local_ref_map.getUnmarkedPartsAsDict(removing_symbols=False)

        # ga_list = pu.patternMatchAll(df.GA_REF, txt)
        for loc, mm in unparsed_dict.items():
            # is_term = (RefType.TERM.value in mm.txt)
            # is_ref = (RefType.REF.value in mm.txt)
            # is_doc = (RefType.DOC.value in mm.txt)
            is_ast_quoted = (df.AST_QUOTE.search(mm.txt) is not None)
            is_single_quote = (df.SNG_QUOTE.search(mm.txt) is not None)
            is_dbl_quote = (df.DBL_QUOTE.search(mm.txt) is not None)
            # is_considering = (is_term or is_ref or is_doc)
            is_considering = (is_ast_quoted or is_dbl_quote or is_single_quote)
            if is_considering:
                return True

            is_there_separator = (' -- ' in mm.txt)
            if is_there_separator:
                return True
        return False

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

            # is_debug = ('Prepare the area you would' in msgid)
            # if is_debug:
            #     print('Debug')

            has_tran = bool(msgstr)
            if not has_tran:
                continue

            # is_term = self.checkIfThereIsTerm(msgstr)
            # if not is_term:
            #     continue

            is_same_count = self.checkIfThereIsBrackets(msgid, msgstr)
            if is_same_count:
                continue

            changed = True
            r = POResultRecord(index + 1, msgid, msgstr)
            self.append(r)

        is_save = (changed) and (self.opo_path)
        if is_save:
            print(f'Dumping po data to: {self.opo_path}')
            # c.dump_po(self.opo_path, tran_file_data)
        else:
            self.showResult()

# -clrfuzzy -of /Users/hoangduytran/new_blender_manual.po