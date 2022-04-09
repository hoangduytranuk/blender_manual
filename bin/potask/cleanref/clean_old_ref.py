import re
from babel.messages.catalog import Message
from matcher import MatcherRecord
from cleanref.clean_ref import CleanRef
from common import Common as cm
from collections import OrderedDict

class CleanOldRefs(CleanRef):
    msgstr_pattern = re.compile(r'(([\*\"\']+)([^\-\*\"\']+)\s[\-]{2}\s([^\-\*\"\']+)([\*\"\']+))|'
                                r'(([\*\"\']+)([^\*\"\'\`\:]+)([\*\"\']+)\s\(([^\(\)<>]+)\))')

    msgid_pattern = re.compile(r'([\*\"\']+)([^\*\"\']+)([\*\"\']+)')
    ignore_pattern = re.compile(r'^\*+\d+\.\w+\s+\-+\s+')

    def isIgnoreEntry(self, mm: MatcherRecord):
        is_ignore = (CleanOldRefs.ignore_pattern.search(mm.txt) is not None)
        if is_ignore:
            return True
        else:
            return False

    def getMsgstrPattern(self):
        return CleanOldRefs.msgstr_pattern

    def getMsgidPattern(self):
        return CleanOldRefs.msgid_pattern

    def getTextFunction(self, matcher_record: MatcherRecord):
        def withEndQuoteEarly(sub_list):
            (self.loc, self.begin_quote) = sub_list[1]
            (self.vnloc, self.vn_txt) = sub_list[2]
            (self.loc, self.end_quote) = sub_list[3]
            (self.enloc, self.en_txt) = sub_list[4]

        def withEndQuoteLate(sub_list):
            (self.loc, self.begin_quote) = sub_list[1]
            (self.vnloc, self.vn_txt) = sub_list[2]
            (self.enloc, self.en_txt) = sub_list[3]
            (self.loc, self.end_quote) = sub_list[4]

        # is_debug = ('*Chuyển Đổi Nhân Trước -- Convert Premul*' in self.matcher_record.txt)
        # if is_debug:
        #     is_debug = True

        sub_list = matcher_record.getSubEntriesAsList()
        (self.oloc, self.otxt) = sub_list[0]
        (loc, test_txt) = sub_list[3]
        is_early_quoted = (CleanRef.ALL_QUOTES.search(test_txt) is not None)
        if is_early_quoted:
            withEndQuoteEarly(sub_list)
        else:
            withEndQuoteLate(sub_list)

    def extract_orig_records(self):
        mm: MatcherRecord = None
        orig_dict = OrderedDict()
        for mm in self.orig_mm_list:
            sub_list = mm.getSubEntriesAsList()
            (oloc, orig_otxt) = sub_list[0]
            (enloc, orig_en_txt) = sub_list[1]
            has_link = (len(sub_list) > 2)
            if has_link:
                (olkloc, orig_link_txt) = sub_list[2]
            else:
                orig_link_txt = None

            entry = {(orig_en_txt.lower(), orig_en_txt.lower()): (orig_en_txt, orig_link_txt)}
            orig_dict.update(entry)
        return orig_dict

    def extract_orig_en_record(self, msg: Message):
        orig_dict = self.extract_orig_records()
        key = (self.en_txt.lower(), self.en_txt.lower())
        if key in orig_dict:
            (self.orig_en_txt, self.orig_link_txt) = orig_dict[key]

    def formatOutput(self):
        self.old_txt = self.matcher_record.txt
        self.new_txt = f':abbr:`{self.vn_txt} ({self.en_txt})`'
        has_quote = bool(self.begin_quote)
        if not has_quote:
            return self.new_txt

        is_astrisk = (self.begin_quote[0] == '*')
        self.begin_quote = ('"' if is_astrisk else self.begin_quote)
        self.new_txt = f'{self.begin_quote}:abbr:`{self.vn_txt} ({self.en_txt})`{self.begin_quote}'
        self.begin_quote = None
        return self.new_txt