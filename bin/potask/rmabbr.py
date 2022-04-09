from pprint import pprint as pp

from sphinx_intl import catalog as c
from potask_base import POTaskBase, POResultRecord
from ignore import Ignore as ig
from definition import Definitions as df, RefType
from common import Common as cm
from pattern_utils import PatternUtils as pu
from matcher import MatcherRecord
from reflist import RefList
import re

class RemoveAbbr(POTaskBase):
    GA_PATTERN_PARSER = re.compile(r'abbr:\`\([^\(\)]+', re.I)
    GA_PAT = re.compile(r'(?=(^|\b))`([^\`]+)?`__')
    GA_GROUPS = re.compile(r'`([^<>]+)\s[\-]{2}\s([^\<\>]+)\s(\<[^<>]+\>)`__')
    GA_WITHOUT_LINK = re.compile(r'`([^<>]+)\s[\-]{2}\s([^\<\>]+)`__')
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

    # def replaceTranslationsFromFile(self, tf: TranslationFinder):
    #     try:
    #         tran_data = c.load_po(self.tran_file)
    #         dict_ptr: NoCaseDict = tf.master_dic_list
    #
    #         for index, m in enumerate(tran_data):
    #             is_first = (index == 0)
    #             if is_first:
    #                 continue
    #
    #             tran_id = m.id
    #             lower_tran_id = tran_id.lower()
    #             tran_txt = m.string
    #
    #             has_tran = bool(tran_txt) and (len(tran_txt) > 0)
    #             if not has_tran:
    #                 continue
    #
    #             entry={lower_tran_id: tran_txt}
    #             dict_ptr.update(entry)
    #
    #     except Exception as e:
    #         print(e)
    #         raise e
    #
    # def checkTranslation(self, orig_txt):
    #     tran = self.tf.isInDict(orig_txt)
    #     return (orig_txt, tran)
    #
    # def checkAndRemoveTranslated(self):
    #     tran_list = list(map(self.checkTranslation, t_list))
    #     remove_list = []
    #     keep_list = []
    #     for (orig_txt, tran) in tran_list:
    #         if tran:
    #             remove_list.append(orig_txt)
    #         else:
    #             keep_list.append(orig_txt)
    #     print(f'removed: [{len(remove_list)}]')
    #     for txt in keep_list:
    #         msg = f'"{txt}",'
    #         print(msg)

    def checkAbbr(self, msgid, msgstr):
        def start_location_matching(check_entry):
            (chloc, chmm) = check_entry
            for (cor_loc, cor_mm) in start_location_matching.correct_abbrev_loc:
                (cs, ce) = cor_loc
                (chs, che) = chloc
                is_same = (cs-1 == chs)
                if not is_same:
                    return True
            return False

        tag_only_dict = pu.patternMatchAll(RemoveAbbr.GA_PATTERN_PARSER, msgstr)
        if not tag_only_dict:
            return False

        correct_abbrev_list = pu.patternMatchAll(df.ABBREV_PATTERN_PARSER, msgstr)
        tag_abbr_only_loc = [(loc, mm) for (loc, mm) in tag_only_dict.items()]
        correct_abbrev_loc = [(loc, mm) for (loc, mm) in correct_abbrev_list.items()]

        start_location_matching.correct_abbrev_loc = correct_abbrev_loc
        error_loc_list = list(filter(start_location_matching, tag_abbr_only_loc))
        if error_loc_list:
            print(f'msgid:[{msgid}]\nmsgstr:[{msgstr}]\n')
            pp(error_loc_list)
            print('============')
            return True
        else:
            return False

    def cleanAbbrevOfSymbolsLeadingAndTrailing(self, msgid, msgstr, abbrev_full_pattern=df.ABBREV_PATTERN_PARSER):
        correct_abbrev_list = pu.patternMatchAll(abbrev_full_pattern, msgstr)
        # print(correct_abbrev_list)
        mm: MatcherRecord = None
        corrected_list=[]
        for (loc, mm) in correct_abbrev_list.items():
            changing=False
            sub_entries = mm.getSubEntriesAsList()
            (abbrev_loc, abbrev_txt) = sub_entries[1]
            abbrev_orig_rec, abbrev_part, exp_part = cm.extractAbbr(abbrev_txt)

            abbrev_part_reduce = pu.patternMatchAll(df.NOT_SPECIAL_QUOTED_PATTERN, abbrev_part)
            if bool(abbrev_part_reduce):
                (ab_clean_loc, abbrev_clean_mm) = list(abbrev_part_reduce.items())[0]
                abbrev_part = abbrev_clean_mm.txt
                changing = True

            abbrev_expl_reduce = pu.patternMatchAll(df.NOT_SPECIAL_QUOTED_PATTERN, exp_part)
            if bool(abbrev_expl_reduce):
                (expl_clean_loc, expl_clean_mm) = list(abbrev_expl_reduce.items())[0]
                exp_part = expl_clean_mm.txt
                changing = True

            new_abbrev = f':abbr:`{abbrev_part} ({exp_part})`'
            corrected_list.append((loc, new_abbrev))

        corrected_list.sort(reverse=True)
        new_txt = str(msgstr)
        for (loc, new_abbrev_txt) in corrected_list:
            new_txt = cm.jointText(new_txt, new_abbrev_txt, loc)
        return new_txt

    def fixTranslatedTerm(self, msgid, msgstr):
        TERM_TXT = ':term:'
        REF_GENERIC = re.compile(r':\w+:(?!:)\`(?!\s)[^\`]+\S\`')
        CORRECTING_TERM = re.compile(r':term:\`([^\`]+)\s[\-]{2}\s([^\`]+)\s\<[^\>]+\>\`')
        has_term = (TERM_TXT in msgstr)
        if not has_term:
            return msgstr

        ref_dict = pu.patternMatchAll(CORRECTING_TERM, msgstr)
        if not bool(ref_dict):
            return msgstr

        mm: MatcherRecord = None
        new_msgstr = str(msgstr)
        fixing_entries = []
        for (loc, mm) in ref_dict.items():
            sub_list = mm.getSubEntriesAsList()
            (all_loc, all_txt) = sub_list[0]
            (vn_loc, vn_txt) = sub_list[1]
            (en_loc, en_txt) = sub_list[2]
            new_term = f'{vn_txt.title()} ({en_txt.title()})'
            new_loc = (vn_loc[0], en_loc[1])
            fixing_entry=(new_loc, new_term)
            fixing_entries.append(fixing_entry)

        fixing_entries.sort(reverse=True)
        for (loc, text) in fixing_entries:
            new_msgstr = cm.jointText(new_msgstr, text, loc)
            print(f'corrected: [{msgstr}] => [{new_msgstr}]')
        return new_msgstr

    def correctTerm(self, msgid, msgstr):
        # is_debug = (':abbr:`song phương (bilateral)`' in msgstr)
        # if is_debug:
        #     is_debug = True
        return self.fixTranslatedTerm(msgid, msgstr)

        ref_list = RefList(msgstr)
        ref_list.parseMessage(is_ref_only=True)
        if not bool(ref_list):
            return msgstr


        # for (loc, mm) in ref_list.items():
        #     is_debug = ('weasel words' in mm.txt)
        #     if is_debug:
        #         is_debug = True

        # term_only_list = list((loc, mm) for (loc, mm) in ref_list.items() if mm.type == RefType.TERM)
        # if not bool(term_only_list):
        #     return msgstr

        concerned_only_list = list((loc, mm) for (loc, mm) in ref_list.items() if mm.type == RefType.GA)
        if not bool(concerned_only_list):
            return msgstr

        print(f'msgid:[{msgid}]\nmsgstr:[{msgstr}]\n')
        print('++++++ concerned_only_list')
        pp(concerned_only_list)
        print('---------------------- concerned_only_list')
        new_entry_list={}
        for (loc, mm) in concerned_only_list:
            pu_list = pu.patternMatchAll(RemoveAbbr.GA_WITHOUT_LINK, mm.txt)
            for (pu_loc, pu_mm) in pu_list.items():
                sub_list = pu_mm.getSubEntriesAsList()
                pp(sub_list)
                or_loc, or_entry = sub_list[0]
                or_loc, vn_txt = sub_list[1]
                or_loc, en_txt = sub_list[2]
            if bool(pu_list):
                print('---------------------- pu_list')
            # pu_list = pu.patternMatchAll(RemoveAbbr.GA_GROUPS, mm.txt)
            # pu_mm: MatcherRecord = None
            # for (pu_loc, pu_mm) in pu_list.items():
            #     sub_list = pu_mm.getSubEntriesAsList()
            #     or_loc, or_entry = sub_list[0]
            #     or_loc, vn_txt = sub_list[1]
            #     or_loc, en_txt = sub_list[2]
            #     or_loc, link = sub_list[3]
            #     new_text = f'`{vn_txt} ({en_txt}) {link}`__'
            #     new_entry = {loc: new_text}
            #     new_entry_list.update(new_entry)
            #     pp(new_entry)
        new_msgstr = str(msgstr)
        new_entry_list = sorted(list(new_entry_list.items()), reverse=True)
        for (loc, new_term) in new_entry_list:
            new_msgstr = cm.jointText(new_msgstr, new_term, loc)

        # pp(pu_list)
        is_diff = (new_msgstr != msgstr)
        if is_diff:
            print('DIFF: xxxx')
            print(new_msgstr)
            print('xxxx')

        return new_msgstr


        #
        # # print(f'msgid:[{msgid}]\nmsgstr:[{msgstr}]\n')
        #
        # new_msgstr = str(msgstr)
        # mm: MatcherRecord = None
        # corrected_list = []
        # PART_SEP = re.compile(r'\s[\-]{2}\s')
        # LINK = re.compile(r'\<[^\<\>]+\>')
        # LINK_SEPARATOR = re.compile(r'([^\(\)]+)\s(\<[^\<\>]+\>)')

        # for (loc, mm) in concerned_only_list:
        new_term_list = []
        new_msgstr = str(msgstr)
        for (loc, mm) in process_list.items():
            # ref_type = mm.type
            # changing = False
            sub_entries = mm.getSubEntriesAsList()
            valid = (len(sub_entries) > 2)
            if not valid:
                continue

            is_debug = ('overview on ReStructuredText' in msgstr)
            if is_debug:
                is_debug = True

            (whole_term_loc, whole_term_txt) = sub_entries[0]
            (txt_loc, vn_txt) = sub_entries[1]
            (txt_loc, en_txt) = sub_entries[2]
            (txt_loc, link) = sub_entries[3]
            new_txt = f'`{vn_txt} ({en_txt}) {link}`__'

            new_term_list.append((loc, new_txt))

        #     part_list = PART_SEP.split(term_content_txt)
        #     has_parts = len(part_list) > 1
        #     if not has_parts:
        #         continue
        #
        #     link_list = LINK.search(mm.txt)
        #     has_link = (link_list is not None)
        #     if not has_link:
        #         continue
        #
        #     corrected_list.append((loc, mm, whole_term_txt, part_list))
        #
        # if bool(corrected_list):
        #     new_term_list=[]
        #     # print(f'msgid:[{msgid}]\nmsgstr:[{msgstr}]\n')
        #     for (loc, mm, whole_term_txt, part_list) in corrected_list:
        #         vn_txt = part_list[0]
        #         en_txt = part_list[1]
        #
        #         en_txt_loc, en_link_text_mm = list(pu.patternMatchAll(LINK_SEPARATOR, en_txt).items())[0]
        #         en_link_text_mm_sub_list = en_link_text_mm.getSubEntriesAsList()
        #         en_txt_loc, en_txt = en_link_text_mm_sub_list[1]
        #         link_loc, link = en_link_text_mm_sub_list[2]
        #
        #         new_term_txt = f':{ref_type.name.lower()}:`{vn_txt.title()} ({en_txt.title()}) {link}`'
        #
        #         # print(f'whole_term_txt:[{whole_term_txt}]')
        #         # print(f'vn_txt:[{vn_txt}]\nen_txt:[{en_txt}]\n')
        #         # pp(part_list)
        #         # new_term_txt = f'{ref_type.name}`{en_txt}` (*{vn_txt}*)'
        #         entry=(loc, new_term_txt)
        #         new_term_list.append(entry)
        #         pp(entry)
        #     print('----------------\n\n')
            new_term_list.sort(reverse=True)
            for (loc, new_term) in new_term_list:
                new_msgstr = cm.jointText(new_msgstr, new_term, loc)

        return new_msgstr

    def performTask(self):
        self.setFiles()
        # abbrev_pattern = df.ABBREV_PATTERN_PARSER

        msg_data = c.load_po(self.po_path)
        # c.dump_po(self.po_path, msg_data, line_width=4096)
        # return

        # self.tf = TranslationFinder()
        # use_external_translation = (self.tran_file is not None) and (os.path.isfile(self.tran_file))
        # if use_external_translation:
        #     self.replaceTranslationsFromFile(self.tf)

        changed = False
        # checkAndRemoveTranslated()
        for index, m in enumerate(msg_data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            if self.filter_ignored:
                is_ignored = (ig.isIgnored(msgid, is_debug=False))
                if is_ignored:
                    continue

            msgid = m.id
            msgstr = m.string

            # print(f'msgid:[{msgid}]\nmsgstr:[{msgstr}]\n\n')
            #
            # msgid = "*Material* modifier alters the base property with a new one taken from a given range mapped on the current material under the stroke"
            # msgstr = "Bộ điều chỉnh :abbr:`*Nguyên vật liệu* (*Material*)` cảnh báo :abbr:`tính chất nền (base property)` bằng một cái mới được lấy từ một phạm vi đã cho ánh xạ trên nguyên vật liệu hiện tại, dưới nét vẽ"

            # new_msgstr = self.cleanAbbrevOfSymbolsLeadingAndTrailing(msgid, msgstr)
            # new_msgstr = self.cleanAbbrevOfSymbolsLeadingAndTrailing(msgid, new_msgstr, abbrev_full_pattern=df.ABBREV_PATTERN_PARSER_COR)

            new_msgstr = self.correctTerm(msgid, msgstr)
            is_diff = (new_msgstr != msgstr)
            if not is_diff:
                continue

            # result = self.checkAbbr(msgid, msgstr)
            # if not result:
            #     continue
            # abbrev_match = abbrev_pattern.search(msgstr)
            # has_abbrev = (abbrev_match is not None)
            # if not has_abbrev:
            #     continue
            #
            # new_msgstr = cm.removeAbbr(msgstr)
            # if not new_msgstr:
            #     continue

            m.string = new_msgstr
            # r = POResultRecord(index+1, msgid, new_msgstr)
            r = POResultRecord(index + 1, msgid, msgstr, alternative_label="new_msgstr", alternative_tran=new_msgstr)
            self.append(r)

            changed = True

        is_save = (changed) and (self.opo_path)
        if is_save:
            c.dump_po(self.opo_path, msg_data, line_width=4069)
        else:
            self.showResult()



# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po

