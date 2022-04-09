import re
from babel.messages.catalog import Message
from matcher import MatcherRecord
from cleanref.clean_ref import CleanRef
from common import Common as cm
from definition import RefType

class CleanRefWithLink(CleanRef):
    msgstr_pattern = re.compile(r'([\*\"\']+)?(:\w+:)\`([^\`]+)\s[-]{2}\s([^\`\<]+)(\s\<[^\`\<\>]+\>)?\`([\*\"\']+)?')
    msgid_pattern = re.compile(r'((:\w+:)\`(([^\`\<\>]+)(\s\<[^\`\<\>]+\>)?)\`)|'
                               r'(([\*]+)((?:[\w])[^\*]+(?:[\w]))([\*]+))|'
                               r'(([\"]+)((?:[\w])[^\"]+(?:[\w]))([\"]+))|'
                               r'(([\']+)((?:[\w])[^\']+(?:[\w]))([\']+))'
                               )
    def getMsgstrPattern(self):
        return CleanRefWithLink.msgstr_pattern

    def getMsgidPattern(self):
        return CleanRefWithLink.msgid_pattern

    def getTextFunction(self, matcher_record: MatcherRecord):
        def has_quotes(sublist: list):
            (self.typeloc, self.begin_quote) = sub_list[1]
            (self.typeloc, self.type_txt) = sub_list[2]
            (self.vnloc, self.vn_txt) = sub_list[3]
            (self.enloc, self.en_txt) = sub_list[4]
            (self.typeloc, self.end_quote) = sub_list[5]

        def no_quotes(sublist: list):
            (self.typeloc, self.type_txt) = sub_list[1]
            (self.vnloc, self.vn_txt) = sub_list[2]
            (self.enloc, self.en_txt) = sub_list[3]

        def has_link(sublist: list):
            (self.typeloc, self.type_txt) = sub_list[1]
            (self.vnloc, self.vn_txt) = sub_list[2]
            (self.enloc, self.en_txt) = sub_list[3]
            (self.lkloc, self.link_txt) = sub_list[4]

        sub_list = matcher_record.getSubEntriesAsList()
        (self.oloc, self.otxt) = sub_list[0]
        (loc, temp_quote) = sub_list[1]
        is_quoted = (CleanRef.ALL_QUOTES.search(temp_quote) is not None)
        try:
            possibly_has_link = (len(sub_list) > 4)
            if possibly_has_link:
                (loc, temp_link) = sub_list[4]
                self.has_link = (CleanRef.REF_LINK.search(temp_link) is not None)
                if self.has_link:
                    has_link(sub_list)
                else:
                    debug=True
            elif is_quoted:
                has_quotes(sub_list)
            else:
                no_quotes(sub_list)

        except Exception as e:
            debug=True

    def findOriginalRefText(self):
        def compare(entry: tuple):
            (current_mm, orig_mm) = entry
            current_txt = self.matcher_record.txt
            current_mm_txt = current_mm.txt
            is_found = (current_mm_txt == current_txt)
            return is_found

        def extract_orig_ref_text(orig_mm: MatcherRecord):
            sub_list = orig_mm.getSubEntriesAsList()
            (oloc, otxt) = sub_list[0]
            (oloc, ref_type) = sub_list[1]
            (oloc, ref_txt) = sub_list[2]
            has_link = len(sub_list) > 3
            if has_link:
                (oloc, ref_link) = sub_list[3]
            return ref_txt
        current_mm: MatcherRecord = None
        orig_mm: MatcherRecord = None
        try:
            [(current_mm, orig_mm)] = list(filter(compare, self.pair_prob_orig))
            ref_txt = extract_orig_ref_text(orig_mm)
            return ref_txt
        except Exception as e:
            return None

    def formatOutput(self):
        self.old_txt = self.matcher_record.txt
        orig_ref_txt = self.findOriginalRefText()
        ref_type = (RefType.getRef(self.type_txt) if self.type_txt else None)
        is_term_or_ref = (ref_type) and ((ref_type == RefType.REF) or (ref_type == RefType.TERM))
        if is_term_or_ref:
            if self.has_link:
                self.new_txt = f'{self.type_txt}`{self.vn_txt} ({self.en_txt}) {self.link_txt}`'
            else:
                self.new_txt = f'{self.type_txt}`{self.en_txt}` (+{self.vn_txt}*)'

        if orig_ref_txt:
            new_arrangement = f'{self.vn_txt} ({self.orig_en_txt}){self.link_txt}'
        if self.has_link:
            new_arrangement = f'{self.vn_txt} ({self.orig_en_txt}){self.link_txt}'
        else:
            new_arrangement = f'{self.vn_txt} ({self.orig_en_txt})'

        self.new_txt = cm.jointText(self.otxt, new_arrangement, self.new_loc)
        is_quoted = bool(self.begin_quote)
        if is_quoted:
            is_already_quoted = (self.new_txt.startswith(self.begin_quote))
            if not is_already_quoted:
                self.new_txt = f'{self.begin_quote}{self.new_txt}{self.end_quote}'
                self.reportIfRepeatQuoted(self.new_txt, self.begin_quote)

        # self.is_gui_label = (CleanRef.is_gui_pattern.search(self.otxt) is not None)
        # if self.has_link or self.is_gui_label:
        #     if self.has_link and self.is_link_changed:
        #         # new_arrangement = f'{en_txt} ({vn_txt}){link_txt}'
        #         if self.is_en_first:
        #             new_arrangement = f'{self.orig_en_txt} ({self.vn_txt}){self.link_txt}'
        #         else:
        #             new_arrangement = f'{self.vn_txt} ({self.orig_en_txt}){self.link_txt}'
        #     else:
        #         # new_arrangement = f'{en_txt} ({vn_txt})'
        #         if self.is_en_first:
        #             new_arrangement = f'{self.orig_en_txt} ({self.vn_txt})'
        #         else:
        #             new_arrangement = f'{self.vn_txt} ({self.orig_en_txt})'
        #     new_txt = cm.jointText(self.otxt, new_arrangement, self.new_loc)
        #     is_already_quoted = (new_txt.startswith(self.begin_quote))
        #     if not is_already_quoted:
        #         new_txt = f'{self.begin_quote}{new_txt}{self.end_quote}'
        #     self.reportIfRepeatQuoted(new_txt, self.begin_quote)
        # else:
        #     new_txt = cm.jointText(self.otxt, self.en_txt, self.new_loc)
        #     is_translation_outside = (CleanRef.translation_outside_pattern.search(self.matcher_record.txt) is not None)
        #     if is_translation_outside:
        #         new_txt = f'{self.begin_quote}{new_txt}{self.end_quote}'
        #         new_txt = f'{new_txt} (*{self.vn_txt}*)'
        return self.new_txt

    def sovleProblem(self,
                     msg: Message,
                     matcher_record: MatcherRecord
                     ):
        return super().solveProblem(msg, matcher_record)

    def performTask(self):
        super().performTask()
