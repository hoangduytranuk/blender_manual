import re
from babel.messages.catalog import Message
from matcher import MatcherRecord
from cleanref.clean_ref import CleanRef
from common import Common as cm
from collections import OrderedDict

class CleanGAWithLink(CleanRef):
    msgstr_pattern = re.compile(r'([\*\"\']+)?\`([^\`\<\>\(\)]+)\s[-]{2}\s([^\`\<\>\(\)]+)(\s\<[^\`\<\>]+\>)?\`[_]+([\*\"\']+)?')
    msgid_pattern = re.compile(r'\`([^\`\<\>]+)(\s\<[^\`\<\>]+\>)?\`[_]+')

    def getMsgstrPattern(self):
        return CleanGAWithLink.msgstr_pattern

    def getMsgidPattern(self):
        return CleanGAWithLink.msgid_pattern

    def getTextFunction(self, matcher_record: MatcherRecord):
        sub_list = matcher_record.getSubEntriesAsList()

        index = 0
        (self.oloc, self.otxt) = sub_list[index]
        (self.vnloc, self.vn_txt) = sub_list[index + 1]
        is_all_quotes = (CleanRef.ALL_QUOTES.search(self.vn_txt) is not None)
        if is_all_quotes:
            index += 1
        (self.vnloc, self.vn_txt) = sub_list[index + 1]
        (self.enloc, self.en_txt) = sub_list[index + 2]
        self.has_link = len(sub_list) > index + 3
        if self.has_link:
            (self.lkloc, self.link_txt) = sub_list[index + 3]
        else:
            (self.lkloc, self.link_txt) = (None, None)

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
        is_debug = ('`Contacts`_' in self.m.id)
        if is_debug:
            is_debug = True

        self.is_gui_label = (CleanRef.is_gui_pattern.search(self.otxt) is not None)
        if self.has_link or self.is_gui_label:
            if self.has_link and self.is_link_changed:
                # new_arrangement = f'{en_txt} ({vn_txt}){link_txt}'
                if self.is_en_first:
                    new_arrangement = f'{self.orig_en_txt} ({self.vn_txt}){self.link_txt}'
                else:
                    new_arrangement = f'{self.vn_txt} ({self.orig_en_txt}){self.link_txt}'
            else:
                # new_arrangement = f'{en_txt} ({vn_txt})'
                if self.is_en_first:
                    new_arrangement = f'{self.orig_en_txt} ({self.vn_txt})'
                else:
                    new_arrangement = f'{self.vn_txt} ({self.orig_en_txt})'
            new_txt = cm.jointText(self.otxt, new_arrangement, self.new_loc)
            is_already_quoted = (new_txt.startswith(self.begin_quote))
            if not is_already_quoted:
                new_txt = f'{self.begin_quote}{new_txt}{self.end_quote}'
            self.reportIfRepeatQuoted(new_txt, self.begin_quote)
        else:
            is_translation_outside = (CleanRef.translation_outside_pattern.search(self.matcher_record.txt) is not None)
            if is_translation_outside:
                new_arrangement = cm.jointText(self.otxt, self.en_txt, self.new_loc)
                new_txt = f'{new_arrangement} (*{self.vn_txt}*)'
            else:
                new_arrangement = f'{self.vn_txt} ({self.orig_en_txt})'
                new_txt = cm.jointText(self.otxt, new_arrangement, self.new_loc)

        return new_txt
