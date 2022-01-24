import os
import re

from babel.messages.catalog import Message, Catalog
from sphinx_intl import catalog as c
from potask_base import POTaskBase, POResultRecord, loadJSONDic, writeJSONDic
from pattern_utils import PatternUtils as pu

from definition import Definitions as df, RefType
from common import Common as cm
from matcher import MatcherRecord
from nocasedict import NoCaseDict

from translation_finder import TranslationFinder
from nocasedict import NoCaseDict
from paragraph import Paragraph as PR
from ignore import Ignore as ig

class AbbrevRecord(object):
    def __init__(self, loc=None, full_txt=None, abbrev=None, exp=None):
        self.loc = loc
        self.orig_abbrev_txt = full_txt
        self.new_abbrev_txt = None
        self.abbrev = abbrev
        self.exp = exp

    def __repr__(self):
        msg = f'loc:{self.loc}\n'
        msg += f'orig_abbrev_txt:{self.orig_abbrev_txt}\n'
        msg += f'new_abbrev_txt:{self.new_abbrev_txt}\n'
        msg += f'abbrev:{self.abbrev}\n'
        msg += f'exp:{self.exp}\n'
        return msg


class AbbrevList(list):
    search_abbr = re.compile(r'(:abbr:\`.*?\)\`)')
    content_abbr = re.compile(r':abbr:[\`]([^\(\)]+)\s?\(([^\(\)]+)\)[\`]')

    def __init__(self, txt):
        self.txt = txt
        self.is_changed = False
        self.new_txt = None

    def parseText(self):
        mm: MatcherRecord = None
        l = pu.patternMatchAll(AbbrevList.search_abbr, self.txt)
        has_record = bool(l)
        if not has_record:
            return

        is_debug = ('Screen Space Ambient Occlusion' in self.txt)
        if is_debug:
            print('Debug')
            
        sub_txt: str = None
        for (loc, mm) in l.items():
            sub_txt = mm.txt
            sub_loc = mm.loc()
            try:
                rec = AbbrevRecord(loc=sub_loc, full_txt=sub_txt)
                ll = AbbrevList.content_abbr.findall(sub_txt)

                first_entry = ll[0]
                (rec.abbrev, rec.exp) = first_entry
                entry = (sub_loc, rec)
                self.append(entry)
            except Exception as e:
                print(f'Exception:[{e}]; sub_txt:[{sub_txt}], self.txt:[{self.txt}]')
                raise e

    def cleanRemoveInvalidPostSuffixesInText(self):
        def getStartEndSymb(txt):
            txt = txt.strip()  # remove spaces
            print(f'getStartEndSymb: [{txt}]')

            # is_debug = ('Dọn dẹp:' in txt)
            # if is_debug:
            #     print('debug')

            print(f'getStartEndSymb: USING SYMB_STARTING_MULTI search: [{txt}]')
            start_non_alpha = df.SYMB_STARTING_MULTI.search(txt)
            end_non_alpha = df.SYMB_ENDING_MULTI.search(txt)
            is_found = (start_non_alpha is not None) and (end_non_alpha is not None)
            if not is_found:
                return None, None, txt

            start_word = start_non_alpha.group(1)
            end_word = end_non_alpha.group(1)
            is_found = (bool(start_word) and bool(end_word))
            if not is_found:
                return None, None, txt

            is_same = (start_word == end_word)
            if not is_same:
                print(f'getStartEndSymb: USING SINGLE SYMB_STARTING search: [{txt}]')
                start_non_alpha = df.SYMB_STARTING.search(txt)
                end_non_alpha = df.SYMB_ENDING.search(txt)
                is_found = (bool(start_non_alpha) and bool(end_non_alpha))
                if not is_found:
                    return None, None, txt


            start_word = start_non_alpha.group(1)
            end_word = end_non_alpha.group(1)
            is_same = (start_word == end_word)
            if not is_same:
                is_parable_start = (df.PAIRABLE_BRACKETS.search(start_word) is not None)
                is_parable_end = (df.PAIRABLE_BRACKETS.search(end_word) is not None)
                is_parable = (is_parable_start and is_parable_end)
                if not is_parable:
                    err_msg = f'start symb:[{start_word}]\nis not as same as end\nsymb:[{end_word}];\nfor txt: [{txt}].\nTrying the next one.\n\n'
                    print(err_msg)
                    return None, None, txt
            mid_word = txt[len(start_word): -len(end_word)]
            return start_word, end_word, mid_word

        has_record = bool(self)
        if not has_record:
            # print(f'[{self.txt}]\nHas no abbrev!\n\n')
            return

        rec: AbbrevRecord = None
        for loc, rec in self:
            try:
                abbrev_start, abbrev_end, abbrev = getStartEndSymb(rec.abbrev)
                is_ignore = not bool(abbrev_start)
                if is_ignore:
                    continue

                exp_start, exp_end, exp = getStartEndSymb(rec.exp)
                has_abbrev_part = (bool(abbrev_start) and bool(abbrev_end))
                has_exp_part = (bool(exp_start) and bool(exp_end))
                is_colon = (bool(abbrev_start) and bool(abbrev_end)) and (df.COLON_CHAR_START.search(abbrev_start) and df.COLON_CHAR_END.search(abbrev_end))

                has_start_end = (has_abbrev_part or has_exp_part)
                is_path = ig.isLinkPath(abbrev)
                is_ignore = (not has_start_end) or is_colon
                if is_ignore:
                    err_msg = f'IGNORING this entry[{rec.orig_abbrev_txt}]. Don\'t appear to have start/end\n\n'
                    print(err_msg)
                    continue

                ref_type = (RefType.AST_QUOTE if (bool(abbrev_start) and (RefType.AST_QUOTE.value in abbrev_start)) else RefType.REF)
                is_omit_begin_and_end_symbols = (ref_type == RefType.AST_QUOTE)
                is_svn_command = ('svn' in abbrev) or ('svn' in exp)

                has_prompt = (df.EXPLANATION_PPROMPT.search(exp) is not None)
                is_exp_en = exp.isascii()
                is_abbrev_en = abbrev.isascii()

                abbrev_new_rec = None
                is_multi_start_end = (len(abbrev_start) > 1) and (len(abbrev_end) > 1)
                if is_omit_begin_and_end_symbols or is_multi_start_end:
                    abbrev_new_rec = f':abbr:`{abbrev} ({exp})`'
                elif is_exp_en or has_prompt or is_path or is_svn_command:
                    abbrev_new_rec = f'{abbrev_start}:abbr:`{abbrev} ({exp})`{abbrev_end}'
                elif is_abbrev_en:
                    abbrev_new_rec = f'{abbrev_start}:abbr:`{exp} ({abbrev})`{abbrev_end}'
                else:
                    err_msg = f'CONFUSED!!! abbrev:[{abbrev}] is_english:[{is_abbrev_en}] \nexp:[{exp}] is_english:[{is_exp_en}]\n\n'
                    print(err_msg)

                has_new_form = bool(abbrev_new_rec)
                if not has_new_form:
                    continue

                self.is_changed = True
                rec.new_abbrev_txt = abbrev_new_rec
                print(f'CHANGED: [{rec.orig_abbrev_txt}] => [{rec.new_abbrev_txt}]\n\n')
            except Exception as e:
                print(f'loc:[{loc}], rec:[{rec}]; e:[{e}]')
                raise e

    def getChangedText(self):
        if not self.is_changed:
            return self.txt

        is_debug = ('Screen Space Ambient Occlusion' in self.txt)
        if is_debug:
            print('Debug')

        self.sort(reverse=True)
        new_msg = str(self.txt)
        for (loc, rec) in self:
            has_new = (rec.new_abbrev_txt is not None)
            if not has_new:
                txt = rec.orig_abbrev_txt
            else:
                txt = rec.new_abbrev_txt
            new_msg = cm.jointText(new_msg, txt, loc)

        print(f'old_msg = [{self.txt}];\nnew_msg: [{new_msg}]\n\n')
        return new_msg

class CorrectAbbreviations(POTaskBase):
    def __init__(self,
                 input_file=None,
                 output_to_file=None
                 ):
        POTaskBase.__init__(
                self,
                input_file=input_file,
                output_to_file=output_to_file
        )
        self.tf = None
        self.en_word_list = None
        self.master_dict: NoCaseDict = None

    def updatePO(self, data):
        m: Message = None
        for index, m in enumerate(data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            msgid = m.id
            msgstr = m.string

            abbrev_list = AbbrevList(msgstr)
            abbrev_list.parseText()
            abbrev_list.cleanRemoveInvalidPostSuffixesInText()
            new_msgstr = abbrev_list.getChangedText()
            m.string = new_msgstr
        return data

    def updateJSON(self, data: dict):
        # This WILL remove all @{} compression -- which is GOOD actually, for the time being
        for index, (msgid, msgstr) in enumerate(data.items()):
            actual_msgstr = self.master_dict.get(msgid)
            err_msg = f'msgid:[{msgid}]\n'
            err_msg += f'msgstr:[{actual_msgstr}]\n\n'
            print(f'parsing: [{index+1}]; {err_msg}')

            abbrev_list = AbbrevList(actual_msgstr)
            abbrev_list.parseText()
            abbrev_list.cleanRemoveInvalidPostSuffixesInText()
            new_msgstr = abbrev_list.getChangedText()
            new_entry = {msgid: new_msgstr}
            data.update(new_entry)
            print(f'[{new_entry}]')
            print('-------------------\n')
        return data

    def correctCaseAndDotEnding(self, data):
        m: Message = None
        dot = '.'
        space = ' '
        colon = ':'

        changed = False
        for index, m in enumerate(data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            msgid:str = m.id
            msgstr:str = m.string

            has_translation = bool(msgstr)
            is_ignore = (not has_translation) or (has_translation and msgstr.startswith(':'))
            if is_ignore:
                continue

            msgstr = msgstr.strip()

            id_first_char = msgid[0]
            msg_first_char = msgstr[0]
            is_id_upper_first = id_first_char.istitle()
            is_msgstr_upper_first = msg_first_char.istitle()
            is_change_first_letter_case = (is_id_upper_first and not is_msgstr_upper_first)
            if is_change_first_letter_case:
                remainder = msgstr[1:]
                new_msgstr = msg_first_char.title() + remainder
                msgstr: str = new_msgstr
                changed = True

            id_ends_with_dot = (msgid.endswith(dot))
            str_ends_with_dot = (msgstr.endswith(dot))
            id_ends_with_space = (msgid.endswith(space))

            is_add_ending = (id_ends_with_dot and not str_ends_with_dot)
            is_remove_ending = (not id_ends_with_dot and str_ends_with_dot)

            if is_add_ending:
                msgstr = f'{msgstr}{dot}'
                changed = True
            if is_remove_ending:
                msgstr = msgstr[:-1]
                changed = True
            if id_ends_with_space:
                msgstr = f'{msgstr} '

            if changed:
                m.string = msgstr

        return data

    def performTask(self):
        from utils import DEBUG
        DEBUG=True
        self.tf = TranslationFinder()
        self.master_dict = self.tf.getDict()

        self.setFiles()

        (path, extension) = os.path.splitext(self.po_path)
        is_po = (extension == '.po')
        is_json = (extension == '.json')

        msg_data = None
        if is_po:
            msg_data = c.load_po(self.po_path)
        if is_json:
            msg_data = loadJSONDic(self.po_path)

        if not bool(msg_data):
            raise f'Input file self.po_path IS EMPTY, or NOT supported. Only PO or JSON files are supported!'

        if is_po:
            # msg_data = self.updatePO(msg_data)
            msg_data = self.correctCaseAndDotEnding(msg_data)
            if bool(self.opo_path):
                c.dump_po(self.opo_path, msg_data)

        elif is_json:
            msg_data = self.updateJSON(msg_data)
            if bool(self.opo_path):
                writeJSONDic(msg_data, self.opo_path)