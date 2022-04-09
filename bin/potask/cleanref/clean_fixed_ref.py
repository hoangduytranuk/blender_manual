import re
from babel.messages.catalog import Message
from matcher import MatcherRecord
from cleanref.clean_ref import CleanRef
from common import Common as cm
from collections import OrderedDict
from pattern_utils import PatternUtils as pu
from definition import Definitions as df

class CleanFixedRefs(CleanRef):
    msgstr_pattern = re.compile(r'([^\*\"\'\`]|^)(:\w+:\`+[^\`]+\`+(\_+)?)([^\*\"\'\`]|$)')
    msgid_pattern = re.compile(
        r'(([\*]+)((?:[\w])[^\*]+(?:[\w]))([\*]+))|'
        r'(([\"]+)((?:[\w])[^\"]+(?:[\w]))([\"]+))|'
        r'(([\']+)((?:[\w])[^\']+(?:[\w]))([\']+))|'
        r'(([\*]+)(:\w+:[`]+[^\`]+[`]+)([\*]+))|'
        r'(([\"]+)(:\w+:[`]+[^\`]+[`]+)([\"]+))|'
        r'(([\']+)(:\w+:[`]+[^\`]+[`]+)([\']+))'
    )

    def __init__(self,
                 input_file=None,
                 output_to_file=None
                 ):

        super().__init__(
                input_file=input_file,
                output_to_file=output_to_file)
        self.input_begin_quote = None
        self.input_end_quote = None
        self.is_continue_if_no_paring_found=False

    def getMsgstrPattern(self):
        return CleanFixedRefs.msgstr_pattern

    def getMsgidPattern(self):
        return CleanFixedRefs.msgid_pattern

    def getTextFunction(self, matcher_record: MatcherRecord):
        def model_ref_leading_trailing_no_link(sub_list: list):
            (loc, self.input_begin_quote) = sub_list[1]
            (self.ref_loc, self.ref_text) = sub_list[2]
            (enloc, self.input_end_quote) = sub_list[3]

        def model_ref_leading_no_trailing_no_link(sub_list: list):
            (self.ref_loc, self.ref_text) = sub_list[1]
            (enloc, self.input_end_quote) = sub_list[2]

        def model_ref_no_leading_with_trailing_no_link(sub_list: list):
            (enloc, self.input_begin_quote) = sub_list[1]
            (self.ref_loc, self.ref_text) = sub_list[2]

        def model_ref_no_leading_no_trailing_no_link(sub_list: list):
            (self.ref_loc, self.ref_text) = sub_list[0]

        sub_list = matcher_record.getSubEntriesAsList()
        sub_list_len = len(sub_list)
        (self.oloc, self.otxt) = sub_list[0]
        if sub_list_len >= 4:
            model_ref_leading_trailing_no_link(sub_list)
        elif sub_list_len < 4 and sub_list_len > 1:
            (loc, temp_txt) = sub_list[1]
            is_quoted = (CleanRef.ALL_QUOTES.search(temp_txt) is not None)
            if not is_quoted:
                model_ref_leading_no_trailing_no_link(sub_list)
            else:
                model_ref_no_leading_with_trailing_no_link(sub_list)
        elif sub_list_len == 1:
            model_ref_no_leading_no_trailing_no_link(sub_list)
        else:
            msg = f'CASES of ref have not cater for {sub_list}'            # raise RuntimeError(msg)

    def solveProblem(self,
                     msg: Message,
                     matcher_record: MatcherRecord,
                     ):

        self.old_text = str(matcher_record.txt)
        self.getTextFunction(matcher_record) # this will expand and fill data in __init__ function
        self.new_txt = self.formatOutput()
        matcher_record = self.finalizeOutput(matcher_record)
        return matcher_record

    def getRefLocation(self, mm: MatcherRecord):
        sub_list = mm.getSubEntriesAsList()
        try:
            sub_list_len = len(sub_list)
            if sub_list_len == 1:
                (self.ref_loc, self.ref_text) = sub_list[0]
            else:
                (self.ref_loc, self.ref_text) = sub_list[2]
            return self.ref_loc
        except Exception as e:

            msg = f'ERROR:[{mm}], {e}!'
            raise RuntimeError(msg)


    def formatOutput(self):
        def replaceASTWithDoubleQuote(entry: str):
            entry = entry.replace('*', '"')
            return entry

        def getPair(entry):
            (current, orig) = entry
            c_matcher = self.matcher_record
            current_txt = current.txt
            c_matcher_txt = c_matcher.txt
            is_same = (current_txt == c_matcher_txt)
            return is_same
        current: MatcherRecord = None

        is_debug = ('is the abbreviation for Non-Uniform Rational' in self.m.id)
        if is_debug:
            is_debug = True
        try:
            orig_record: MatcherRecord = None
            if not self.pair_prob_orig:
                raise RuntimeError('Empty pairing problem and original text!')

            [(current, orig_record)] = list(filter(getPair, self.pair_prob_orig))

            orig_sub_list = orig_record.getSubEntriesAsList()
            (oloc, otxt) = orig_sub_list[0]
            (oloc, self.begin_quote) = orig_sub_list[1]
            (oloc, self.orig_en_txt) = orig_sub_list[2]
            (oloc, self.end_quote) = orig_sub_list[3]
            msg = f'PAIR: {orig_record} {current}'
            print(msg)
        except Exception as e:
            self.begin_quote = ''
            self.orig_en_txt = self.en_txt
            self.end_quote = ''
            return None

        input_begin_quote = (self.input_begin_quote if self.input_begin_quote else '')
        input_end_quote = (self.input_end_quote if self.input_end_quote else '')
        orig_begin_quote = (self.begin_quote if self.begin_quote else '')
        orig_end_quote = (self.end_quote if self.end_quote else '')

        is_menu_selection = (':menuselection:' in self.matcher_record.txt)
        if is_menu_selection:
            is_debug = True

        list_of_rep = [input_begin_quote, input_end_quote, orig_begin_quote, orig_end_quote]
        [input_begin_quote, input_end_quote, orig_begin_quote, orig_end_quote] = list(map(replaceASTWithDoubleQuote, list_of_rep))

        is_start_same = input_begin_quote.strip() and (input_begin_quote == orig_begin_quote)
        is_end_same = input_end_quote.strip() and (input_end_quote == orig_end_quote)
        orig_begin_quote = ('' if is_start_same else orig_begin_quote)
        orig_end_quote = ('' if is_end_same else orig_end_quote)

        is_debug = ('MIP (Multum In Parvo' in self.ref_text)
        if is_debug:
            is_debug = True
        self.old_txt = self.ref_text
        self.new_txt = f'{input_begin_quote}{orig_begin_quote}{self.ref_text}{orig_end_quote}{input_end_quote}'
        # self.new_txt = f'{orig_begin_quote}{self.ref_text}{orig_end_quote}'
        self.begin_quote = None
        self.end_quote = None
        self.input_begin_quote = None
        self.input_end_quote = None
        return self.new_txt

    def assemble_result(self, matcher_record: MatcherRecord, overriding_loc=None):
        # ref_loc = self.ref_loc
        # super().assemble_result(matcher_record, overriding_loc=ref_loc)
        super().assemble_result(matcher_record, overriding_loc=None)