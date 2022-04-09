import re
from babel.messages.catalog import Message
from matcher import MatcherRecord
from cleanref.clean_ref import CleanRef
from common import Common as cm
from collections import OrderedDict

class CleanRefWrongCases(CleanRef):
    msgstr_pattern = re.compile(r'([\*\"\']+)?(:\w+:)\`([^\`\<\>\(\)]+)\s\(([^\`\<\>\(\)]+)\)(\s\<[^\`\<\>]+\>)?\`([\*\"\']+)?')
    msgid_pattern = re.compile(r'(:\w+:)\`([^\`\<\>]+)(\s\<[^\`\<\>]+\>)?\`|[\*]([^\*]+)[\*]|[\"]([^\"]+)[\"]|[\']([\']+)[\']')
    def getMsgstrPattern(self):
        return CleanRefWrongCases.msgstr_pattern

    def getMsgidPattern(self):
        return CleanRefWrongCases.msgid_pattern

    def getTextFunction(self, matcher_record: MatcherRecord):
        sub_list = matcher_record.getSubEntriesAsList()
        index = 0
        (self.oloc, self.otxt) = sub_list[index]
        (self.typeloc, self.type_txt) = sub_list[index + 1]
        is_all_quotes = (CleanRef.ALL_QUOTES.search(self.type_txt) is not None)
        if is_all_quotes:
            index += 1
        (self.typeloc, self.type_txt) = sub_list[index + 1]
        (self.vnloc, self.vn_txt) = sub_list[index + 2]
        (self.enloc, self.en_txt) = sub_list[index + 3]
        self.has_link = len(sub_list) > index + 4
        if self.has_link:
            (self.lkloc, self.link_txt) = sub_list[index + 4]
        else:
            (self.lkloc, self.link_txt) = (None, None)

    def formatOutput(self):
        deb_p = re.compile('adding extra options', re.I)
        is_debug = (deb_p.search(self.m.id) is not None)
        if is_debug:
            is_debug = True
        if self.has_link and self.is_link_changed:
            # new_arrangement = f'{en_txt} ({vn_txt}){link_txt}'
            if self.is_en_first:
                new_arrangement = f'{self.orig_en_txt} ({self.vn_txt}){self.link_txt}'
            else:
                new_arrangement = f'{self.vn_txt} ({self.orig_en_txt}){self.link_txt}'
        else:
            # new_arrangement = f'{en_txt} ({vn_txt}'
            if self.is_en_first:
                new_arrangement = f'{self.orig_en_txt} ({self.vn_txt}'
            else:
                new_arrangement = f'{self.vn_txt} ({self.orig_en_txt}' # the pattern group excluded the brackets, so brackets are still in the original text
        new_txt = cm.jointText(self.otxt, new_arrangement, self.new_loc)
        is_already_quoted = (new_txt.startswith(self.begin_quote))
        if not is_already_quoted:
            new_txt = f'{self.begin_quote}{new_txt}{self.end_quote}'
        self.reportIfRepeatQuoted(new_txt, self.begin_quote)
        msg = f'WRONG_CASE:msg:{self.m.id}\norig_en:{self.orig_en_txt}\nold_txt:{self.otxt}\nnew_txt:{new_txt}'
        print(msg)
        return new_txt

    def extract_orig_en_record(self, msg: Message):
        orig_dict = self.extract_orig_records()
        key = (self.type_txt.lower(), self.en_txt.lower())
        is_in = (key in orig_dict)
        if is_in:
            (self.orig_en_txt, self.orig_link_txt) = orig_dict[key]
        else:
            key = (self.en_txt.lower(), self.en_txt.lower())
            is_in = (key in orig_dict)
            if is_in:
                (self.orig_en_txt, self.orig_link_txt) = orig_dict[key]
                print(f'self.orig_en_txt: {self.orig_en_txt}')
                print(f'self.orig_link_txt: {self.orig_link_txt}')

    def extract_orig_records(self):
        mm: MatcherRecord = None
        orig_dict = OrderedDict()
        for mm in self.orig_mm_list:
            sub_list = mm.getSubEntriesAsList()
            (oloc, orig_otxt) = sub_list[0]

            num_lines = len(sub_list)
            is_quoted = (num_lines == 2)
            if is_quoted:
                (oloc, orig_en_txt) = sub_list[1]
                orig_type_txt = orig_en_txt
            else:
                (typeloc, orig_type_txt) = sub_list[1]
                (oloc, orig_en_txt) = sub_list[2]
                # except Exception as e:
                #     is_debug = True

            has_link = (len(sub_list) > 3)
            if has_link:
                (oloc, orig_link_txt) = sub_list[3]
            else:
                orig_link_txt = None

            entry = {(orig_type_txt.lower(), orig_en_txt.lower()): (orig_en_txt, orig_link_txt)}
            orig_dict.update(entry)
        return orig_dict
