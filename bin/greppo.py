import os
import re
from potask_base import POTaskBase, POResultRecord
from ignore import Ignore as ig
from sphinx_intl import catalog as c
from pathlib import Path

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
                 search_extensions=None
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
                search_extensions=search_extensions
        )
        self.msgid = None
        self.msgstr = None
        self.p = self.np = self.pid = self.npid = None

    def findOneString(self, msg, p, alternate_p):
        is_both = (p and alternate_p)
        is_p = (p and not alternate_p)
        is_alternate = (not p and alternate_p)
        match = alt_match = None

        match_list = []
        if is_both:
            match = p.search(msg)
            alt_match = alternate_p.search(msg)
        elif is_p:
            match = p.search(msg)
        elif is_alternate:
            alt_match = alternate_p.search(msg)
        else:
            pass

        is_found = (match or alt_match)
        if is_found:
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

        has_no_pattern = not (self.p or self.np or self.pid or self.npid)
        if has_no_pattern:
            msg = f'No pattern has been entered. Search requires at least ONE pattern specified'
            raise RuntimeError(msg)

        if self.is_msgid:
            search_id_valid = (self.p or self.pid or self.npid)
            if not search_id_valid:
                msg = f'Intention to search on msgid and yet no patterns - positive or negative - were defined'
                raise RuntimeError(msg)

        if self.is_msgstr:
            search_str_valid = (self.p or self.np)
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

        r = POResultRecord(index + 1, text_line, None)
        return r


    def grepPOFile(self):
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

            r = POResultRecord(index + 1, None, None)
            self.append(r)

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
                r = POResultRecord(0, path, None)
                self.append(r)
                self.extend(found_for_current_file)
                found_for_current_file = []

    def performTask(self):
        # -rpl -ig -f /Users/hoangduytran/test_283_no_abbrev.po -of /Users/hoangduytran/test_283_no_abbrev_space_dot.po
        self.setPattern()
        is_directory = (os.path.isdir(self.po_path))
        if is_directory:
            if not is_directory:
                msg = f'{self.po_path} is NOT SUPPORTED. Exit!'
                raise RuntimeError(msg)

            self.grepDirectory()
        else:
            if self.isSelectedFile(['.po', '.pot']):
                self.setFiles()
                self.grepPOFile()
            else:
                return

        self.showResult()

# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po

