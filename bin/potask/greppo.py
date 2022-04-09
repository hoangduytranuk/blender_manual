import os
import sys
import re
from potask_base import POTaskBase, POResultRecord
from ignore import Ignore as ig
from sphinx_intl import catalog as c
from babel.messages.catalog import Catalog, Message
from pathlib import Path
from pattern_utils import PatternUtils as pu
from matcher import MatcherRecord
from common import Common as cm
from reflist import RefList

class BCOLOR:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)

class GrepPO(POTaskBase):
    def __init__(self,
                 input_file=None,
                 output_to_file=None,
                 pattern=None,
                 negate_pattern=None,
                 pattern_id=None,
                 negate_pattern_id=None,
                 is_case_sensitive=None,
                 is_msgid=None,
                 is_msgstr=None,
                 is_display_msgid=None,
                 is_display_msgstr=None,
                 filter_ignored=None,
                 search_extensions=None,
                 po_location_pattern=None,
                 raw_search=None,
                 match_only=None
                 ):
        POTaskBase.__init__(
                self,
                input_file=input_file,
                output_to_file=output_to_file,
                pattern=pattern,
                negate_pattern=negate_pattern,
                pattern_id=pattern_id,
                negate_pattern_id=negate_pattern_id,
                is_case_sensitive=is_case_sensitive,
                is_msgid=is_msgid,
                is_msgstr=is_msgstr,
                is_display_msgid=is_display_msgid,
                is_display_msgstr=is_display_msgstr,
                filter_ignored=filter_ignored,
                search_extensions=search_extensions,
                po_location_pattern=po_location_pattern,
                raw_search=raw_search,
                match_only=match_only,
        )
        self.msgid = None
        self.msgstr = None
        self.p = self.np = self.pid = self.npid = self.locp = None


    # To test, just run a source ~/.bash_profile to update your current terminal.
    # Side note about the colors: The colors are preceded by an escape sequence \e and defined by a color value, composed of [style;color+m] and wrapped in an escaped [] sequence. eg.
    # red = \[\e[0;31m\]
    # bold red (style 1) = \[\e[1;31m\]
    # clear coloring = \[\e[0m\]

    def findInString(self, msg, p):
        has_p = bool(p) and isinstance(p, re.Pattern)
        has_messasge = bool(msg) and isinstance(msg, str)
        valid = (has_messasge) and (has_p)
        if not valid:
            return []

        match_dict = pu.patternMatchAll(p, msg)
        return match_dict

    def transformSearchResult(self, msg, match_list: dict):
        mm: MatcherRecord = None
        new_msg = str(msg)
        reversed_list = reversed(match_list.items())
        match_only_list=[]
        for (loc, mm) in reversed_list:
            # if not self.is_redirected:
            #     mm_txt = f'{BCOLOR.OKGREEN}{mm.txt}{BCOLOR.ENDC}'
            # else:
            mm_txt = mm.txt

            if self.match_only:
                match_only_list.append(mm_txt)
            else:
                cm.jointText(new_msg, mm_txt, loc)
        if self.match_only:
            new_msg = '\n'.join(match_only_list)
        return new_msg

    def findOneString(self, msg, p, alternate_p):
        is_debug = (':term:' in msg)
        if is_debug:
            is_debug = True

        has_p = bool(p) and isinstance(p, re.Pattern)
        has_alternate_p = bool(alternate_p) and isinstance(alternate_p, re.Pattern)
        has_messasge = bool(msg)
        valid = (has_messasge) and (has_p or has_alternate_p)
        if not valid:
            return []

        is_both = (has_p and has_alternate_p)
        is_p = (has_p and not has_alternate_p)
        is_alternate = (not has_p and has_alternate_p)
        match = alt_match = None
        # p = re.compile(r':term:`[^`]+')
        match_list = []
        if is_both:
            match = pu.patternMatchAll(p, msg)
            alt_match = pu.patternMatchAll(alternate_p, msg)
        elif is_p:
            match = pu.patternMatchAll(p, msg)
        elif is_alternate:
            alt_match = pu.patternMatchAll(alternate_p, msg)
        else:
            pass

        is_found = (match or alt_match)
        mm: MatcherRecord = None
        if is_found:
            if self.match_only:
                if match:
                    m_list = [mm.txt for (loc, mm) in match.items()]
                    match_list.extend(m_list)
                if alt_match:
                    m_list = [mm.txt for (loc, mm) in alt_match.items()]
                    match_list.extend(m_list)
            else:
                match_list.append(msg)
        return match_list

    def findSetByPattern(self, gen_pattern, id_pattern):
        match_list=[]
        find_on_id = (self.is_msgid or id_pattern)
        if find_on_id:
            m = self.findOneString(self.msgid, gen_pattern, id_pattern)
            match_list.extend(m)

        find_on_str = (self.is_msgstr or gen_pattern)
        if find_on_str:
            m = self.findOneString(self.msgstr, gen_pattern, id_pattern)
            match_list.extend(m)
        return match_list

    def setPattern(self):

        search_flag = (re.IGNORECASE if not self.is_case_sensitive else 0)
        self.p = (re.compile(self.pattern, flags=search_flag) if self.pattern else None)
        self.np = (re.compile(self.negate_pattern, flags=search_flag) if self.negate_pattern else None)
        self.pid = (re.compile(self.pattern_id, flags=search_flag) if self.pattern_id else None)
        self.npid = (re.compile(self.negate_pattern_id, flags=search_flag) if self.negate_pattern_id else None)
        self.locp = (re.compile(self.po_location_pattern, flags=search_flag) if self.po_location_pattern else None)

        has_no_pattern = not (self.p or self.np or self.pid or self.npid or self.locp)
        if has_no_pattern:
            msg = f'No pattern has been entered. Search requires at least ONE pattern specified'
            raise RuntimeError(msg)

        if self.is_msgid:
            search_id_valid = (self.p or self.pid or self.npid or self.locp)
            if not search_id_valid:
                msg = f'Intention to search on msgid and yet no patterns - positive or negative - were defined'
                raise RuntimeError(msg)

        if self.is_msgstr:
            search_str_valid = (self.p or self.np or self.locp)
            if not search_str_valid:
                msg = f'Intention to search on msgstr and yet no patterns - positive or negative - were defined'
                raise RuntimeError(msg)

    def grepTextInLine(self, index=0, text_line=None):
        if not text_line:
            return None

        if index < 0:
            return None

        match_list = self.findOneString(text_line, self.p, self.pid)
        is_found = (len(match_list) != 0)
        if not is_found:
            return None

        has_negated_pattern = (self.np or self.npid)
        if has_negated_pattern:
            negate_list = self.findOneString(text_line, self.np, self.npid)
            if negate_list:
                match_list.clear()

        is_found = (len(match_list) != 0)
        if not is_found:
            return None

        r = POResultRecord(index + 1, text_line, None, is_match_only=self.match_only)
        return r

    def grepPOFile(self):
        m: Message = None
        msg_data = c.load_po(self.po_path)
        for index, m in enumerate(msg_data):
            is_first_line = (index == 0)
            if is_first_line:
                continue

            is_fuzzy = bool(m.fuzzy)
            if is_fuzzy:
                continue

            self.msgid = m.id
            self.msgstr = m.string
            self.locations = m.locations

            # ref = RefList(self.msgstr)
            # ref.parseMessage(is_ref_only=True)
            # if not ref:
            #     continue
            # mm: MatcherRecord = None
            # for (loc, mm) in ref.items():
            #     print(mm.txt)
            # continue

            is_find_in_locations = (self.locp is not None)
            if is_find_in_locations:
                is_found_location = self.findInList(self.locp, self.locations)
                if not is_found_location:
                    continue

            if self.filter_ignored:
                is_ignored = (ig.isIgnored(self.msgid, is_debug=False))
                if is_ignored:
                    continue

            match_list = self.findSetByPattern(self.p, self.pid)
            is_found = (len(match_list) != 0)
            if not is_found:
                continue

            has_negated_pattern = (self.np or self.npid)
            if has_negated_pattern:
                negate_list = self.findSetByPattern(self.np, self.npid)
                for neg_entry in negate_list:
                    match_list.clear()

            is_found = (len(match_list) != 0)
            if not is_found:
                continue

            r = POResultRecord(index + 1, None, None, is_match_only=self.match_only)
            self.append(r)
            if self.match_only:
                r.msgid = match_list
                continue

            if self.is_msgid:
                r.msgid = self.msgid
                if self.is_display_msgstr:
                    r.msgstr = self.msgstr

            if self.is_msgstr:
                if self.is_display_msgid:
                    r.msgid = self.msgid
                r.msgstr = self.msgstr

    def isPOFile(self):
        po_ending = [".po", ".pot"]

        input_path: str = (self.po_path)
        input_path_lower = (input_path.lower())
        end_dot_index = input_path_lower.rfind(".")
        has_dot_end = (end_dot_index >= 0)
        if not has_dot_end:
            return False

        ext = input_path_lower[-end_dot_index:]
        return (ext in po_ending)

    def isSelectedFile(self, path, lower_accepted_endings=None):

        if not lower_accepted_endings:
            return True

        input_path: str = (path)
        input_path_lower = (input_path.lower())
        end_dot_index = input_path_lower.rfind(".")
        has_dot_end = (end_dot_index >= 0)
        if not has_dot_end:
            return False

        ext = input_path_lower[-end_dot_index:]
        return (ext in lower_accepted_endings)

    def listDirectory(self, from_path:str):
        base_path = Path(from_path)
        dir_list = base_path.glob('**/*.*')
        return sorted(dir_list)

    def grepDirectory(self):
        file_list = self.listDirectory(self.po_path)
        accepted_list=[]
        for path_entry in file_list:
            file_ext = path_entry.suffix
            is_interested_file = (file_ext in self.search_extensions)
            if not is_interested_file:
                continue

            path = str(path_entry)
            accepted_list.append(path)

        found_for_current_file=[]
        for path in accepted_list:
            with open(path, encoding='latin-1') as f:
                line_list = f.readlines()

            for index, line in enumerate(line_list):
                r = self.grepTextInLine(index, line)
                if r:
                    found_for_current_file.append(r)

            if found_for_current_file:
                r = POResultRecord(0, path, None, is_match_only=self.match_only)
                self.append(r)
                self.extend(found_for_current_file)
                found_for_current_file = []

    def rawSearchAFile(self):
        def locNotContain(search_loc):
            (sch_s, sch_e) = search_loc
            for neg_loc in locNotContain.negative_search_loc_list:
                (neg_s, neg_e) = neg_loc
                is_start_in = (sch_s in range(neg_s, neg_e))
                is_end_in = (sch_e in range(neg_s, neg_e))
                is_remove = (is_start_in or is_end_in)
                if is_remove:
                    return True
            return False

        def grepALine(text_line, positive_pattern, negative_pattern):
            positive_search = self.findInString(text_line, positive_pattern)
            if not positive_search:
                return None

            negative_search = self.findInString(text_line, negative_pattern)
            if negative_search:
                positive_search_loc_list = positive_search.keys()
                negative_search_loc_list = negative_search.keys()
                locNotContain.negative_search_loc_list = negative_search_loc_list
                remove_loc_list = list(filter(locNotContain, positive_search_loc_list))
                for rm_loc in remove_loc_list:
                    del positive_search[rm_loc]

            transformed_txt = self.transformSearchResult(text_line, positive_search)
            return transformed_txt

        with open(self.po_path, "r") as f:
            txt_lines = f.readlines()
        data = [x.strip() for x in txt_lines]

        msgid = re.compile(r'msgid\s')
        msgstr = re.compile(r'msgstr\s')
        between = re.compile(r'"\n"')
        for index, text_line in enumerate(data):
            text_line = msgid.sub("", text_line)
            text_line = msgstr.sub("", text_line)
            text_line = between.sub("", text_line)
            found_line = grepALine(text_line.strip(), self.p, self.np)
            if not bool(found_line):
                continue

            r = POResultRecord(index + 1, found_line, None, is_match_only=self.match_only)
            self.append(r)

    def performTask(self):
        # -rpl -ig -f /Users/hoangduytran/test_283_no_abbrev.po -of /Users/hoangduytran/test_283_no_abbrev_space_dot.po
        self.setPattern()
        # self.p = re.compile(r'(\s|^)([\*\'\"]+[^\*\'\"]+\S[\*\'\"]+)')

        is_directory = (os.path.isdir(self.po_path))
        if is_directory:
            if not is_directory:
                msg = f'{self.po_path} is NOT SUPPORTED. Exit!'
                raise RuntimeError(msg)

            self.grepDirectory()
        else:
            if self.isSelectedFile(['.po', '.pot']):
                self.setFiles()
                if self.raw_search:
                    self.rawSearchAFile()
                else:
                    self.grepPOFile()
            else:
                return

        self.showResult()

# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po
# -s -locp "vr_scene_inspection" -p "viewer" -mid -dstr -f /Users/hoangduytran/Dev/tran/blender_docs/locale/vi/LC_MESSAGES/blender_manual.po

