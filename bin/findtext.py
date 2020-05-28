#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Hoang Duy Tran <hoangduytran1960@gmail.com>
# Revision Date: 2020-02-02 09:59+0000
#
import os
import re
import sys
import math
import locale
import datetime
from time import gmtime, strftime, time
from pytz import timezone
from argparse import ArgumentParser
from pprint import pprint
from sphinx_intl import catalog as c
from babel.messages import pofile
from enum import Enum
import chardet

CURRENT_FILE_NAME = None
FILE_NAME_SHOWED = False
INVERT_SEP='•'
DEBUG = True

def setfilename(file_name):
    global CURRENT_FILE_NAME
    CURRENT_FILE_NAME = file_name

def showfilename():
    global FILE_NAME_SHOWED
    if not FILE_NAME_SHOWED:
        print(CURRENT_FILE_NAME)
        print("="*80)
        FILE_NAME_SHOWED=True

def resetfilenameshowed():
    global FILE_NAME_SHOWED
    FILE_NAME_SHOWED=False


def pp(object, stream=None, indent=1, width=80, depth=None, *args, compact=False):
    showfilename()
    if DEBUG:
        pprint(object, stream=stream, indent=indent, width=width, depth=depth, *args, compact=compact)
        print('-' * 30)

def _(*args, **kwargs):
    showfilename()
    if DEBUG:
        print(args, kwargs)
        print('-' * 30)

class LetterCase(Enum):
    NO_CHANGE="No Change",
    LOWER_CASE="Lower",
    UPPER_CASE="Upper",
    CAPITAL_CASE="Capital",
    TITLE_CASE="Title"

class ListPathEvent:
    def __init__(self):
        self.dirpath = None
        self.dirnames = None
        self.filenames = None

    def __repr__(self):
        l = []
        if (self.dirpath):
            for dir_path in self.dirpath:
                l.append(dir_path)

        if (self.dirnames):
            for dir_name in self.dirnames:
                l.append(dir_name)

        if (self.filenames):
            for file_name in self.filenames:
                l.append(file_name)
        return "".join(l)

    def setVars(self, dirpath, dirnames, filenames):
        self.dirpath = dirpath
        self.dirnames = dirnames
        self.filenames = filenames

    def run(self):
        pass

# -----------------------------------------------------------------------------
# findFileByExtension
# An instance of implementation of the ListPathEvent
# Find all files with matching extenion
# Calling it by x = findFileByExtension("rst")
# return the list of all files matching the provided extension
#
class findFileByExtension(ListPathEvent):

    def __init__(self, search_extension):
        self.search_extension  = search_extension
        self.result = []

    def run(self):
        for filename in self.filenames:
            is_valid = filename.lower().endswith(self.search_extension.lower())
            if (is_valid):
                entry=os.path.join(self.dirpath, filename)
                self.result.append(entry)

    def getModificationTime(self, name):
        path = os.path.join(self.dirpath, name)
        return os.path.getmtime(path)

    def getListSorted(self, key_function=None, is_reversed=False):
        #_("getListSorted:", self.result)
        #pp(self.result)
        #_("before sorted getListSorted")

        sorted_list = sorted(self.result, key=key_function, reverse=is_reversed)
        #pp(sorted_list)
        #_("after sorted getListSorted")
        return sorted_list

    def getListSortedModified(self, modified_within_last_n_seconds=0):
        select_list=[]
        time_now = time()
        for fname in self.result:
            use_time = (modified_within_last_n_seconds >= 0)
            if not use_time:
                select_list.append(fname)
            else:
                mtime = self.getModificationTime(fname)
                diff_time_second = time_now - mtime
                is_file_modified_within_requested_period = (diff_time_second <= modified_within_last_n_seconds)
                if is_file_modified_within_requested_period:
                    select_list.append(fname)

        return select_list


class BasicIO:

    def writeTextFile(self, file_name, data):
        try:
            with open(file_name, "w+", encoding="utf-8") as f:
                f.write(data)
        except Exception as e:
            _("ERROR write data:", data)
            _("ERROR write file:", file_name)
            raise e

    def readTextFile(self, file_name):
        data=None
        try:
            with open(file_name, "r", encoding="utf-8", errors='replace') as f:
                data = f.read()
            return data
        except Exception as e:
            _("ERROR reading file:", file_name, e)
            raise e

    # -----------------------------------------------------------------------------
    # Common Utilities
    # base function to list path based on the condition and actions defined in the run routine of the callback function
    # remember the callback function must be an instance of ListPathEvent, so your function must inherit that
    def listDir(self, from_path : str, callback : object):
        for dirpath, dirnames, filenames in os.walk(str(from_path)):
            if dirpath.startswith("."): # hidden file or current dir '.', parent dir '..'
                continue

            valid_function = ((not callback is None) and (isinstance(callback, ListPathEvent)))
            if (valid_function):
                # _("calling back with:", dirpath, dirnames, filenames)
                callback.setVars(dirpath, dirnames, filenames)
                callback.run()

class FindFilesHasPattern:

    def __init__(self):
        self.basic_io = BasicIO()
        self.found_lines_dic = {}

    def getCase(self, lower_case, upper_case, capital_case, title_case):
        actual_case = LetterCase.NO_CHANGE
        if lower_case is not None:
            actual_case = LetterCase.LOWER_CASE
        elif upper_case is not None:
            actual_case = LetterCase.UPPER_CASE
        elif capital_case is not None:
            actual_case = LetterCase.CAPITAL_CASE
        elif title_case is not None:
            actual_case = LetterCase.TITLE_CASE
        else:
            actual_case = LetterCase.NO_CHANGE
        return actual_case

    def setVars(self,
            find_pattern,
            replace_pattern,
            lower_case,
            upper_case,
            capital_case,
            title_case,
            find_file,
            vipo_file,
            find_po,
            find_rst,
            find_py,
            find_src,
            case_sensitive,
            before_lines,
            after_lines,
            only_match,
            show_line_number,
            invert_match,
            testing_only,
            debugging
            ):
        self.find_file = (find_file if (find_file and os.path.isfile(find_file)) else None)
        self.find_po = (True if find_po else False)
        self.find_rst = (True if find_rst else False)
        self.find_py = (True if find_py else False)
        self.vipo_file = (True if vipo_file else False)
        self.find_src = (True if find_src else False)
                
        self.case_sensitive = (True if case_sensitive else False)
        DEBUG = (True if debugging else False)

        self.letter_case = self.getCase(lower_case, upper_case, capital_case, title_case)

        self.pattern_flag = (re.I if not self.case_sensitive else 0)
        #self.input_pattern = find_pattern
        if (find_pattern is not None):
            self.find_pattern = re.compile(r'{}'.format(find_pattern), flags=self.pattern_flag)
            self.txt_find_pattern = find_pattern
        else:
            self.find_pattern = None

        if (replace_pattern is not None):
            self.replace_pattern = replace_pattern
        else:
            self.replace_pattern = None

        self.from_line = (int(before_lines) if before_lines else -1)
        self.to_line = (int(after_lines) if after_lines else -1)
        self.only_match = (True if only_match else False)
        self.show_line_number = (True if show_line_number else False)
        self.invert_match = (True if invert_match else False)
        self.testing_only = (True if testing_only else False)

    def patternMatchAll(self, pat, text):
        try:
            # itor = pat.finditer(text)
            # _("itor", type(itor))
            # _("dir", dir(itor))

            for m in pat.finditer(text):
                original = ()
                break_down = []

                s = m.start()
                e = m.end()
                orig = m.group(0)
                original = (s, e, orig)

                for g in m.groups():
                    if g:
                        i_s = orig.find(g)
                        ss = i_s + s
                        ee = ss + len(g)
                        v=(ss, ee, g)
                        break_down.append(v)
                yield original, break_down

        except Exception as e:
            _("patternMatchAll")
            _("pattern:", pat)
            _("text:", text)
            _(e)
        return None, None

    # def finInvert(self, pattern, text):
    #     invert_list=[]
    #     pro_list=[]
    #     for orig, breakdown in self.patternMatchAll(pattern, text):
    #         pro_list.append(orig)
    #     is_empty = (len(pro_list) == 0)
    #     if is_empty:
    #         invert_list.append(text)
    #     else:
    #         max = len(text)
    #         inc_list=[]
    #         s = e = 0
    #         for ss, ee, ex_txt in pro_list:
    #             e = ss-1
    #             valid= (s < e) and (s >= 0) and (e <= max)
    #             if (valid):
    #                 inc_txt = text[s:e]
    #                 entry=(s, e, inc_txt)
    #                 inc_list.append(entry)
    #             s = ee+1
    #         e = max
    #         valid=(s < e) and (s >= 0) and (e <= max)
    #         if (valid):
    #             inc_txt = text[s:e]
    #             entry=(s, e, inc_txt)
    #             inc_list.append(entry)

    #     return invert_list

    def getAllMatchedWordFromLine(self, pattern, text_line):
        list_of_matches=[]
        for origin, breakdown in self.patternMatchAll(pattern, text_line):
            is_end = (origin is None)
            if is_end:
                break

            s, e, orig = origin
            list_of_matches.append(orig)
        return list_of_matches


    def find(self):

        po_file_list=None
        rst_file_list=None
        py_file_list=None
        search_file_list=[]

        if self.find_file:
            search_file_list.append(self.find_file)
        elif self.vipo_file:
            po_dir = os.environ['BLENDER_GITHUB']
            if po_dir:
                po_dir = os.path.join(po_dir, "gui/2.80/po")
                _("po_dir:", po_dir)

            po_file_list = self.getFileList(po_dir, ".po")
            _("po_file_list")
            pp(po_file_list)
            search_file_list.extend(po_file_list)
        else:
            if self.find_po:
                po_dir = os.environ['BLENDER_MAN_VI']
                if po_dir:
                    po_dir = os.path.join(po_dir, "LC_MESSAGES")
                    _("po_dir:", po_dir)

                po_file_list = self.getFileList(po_dir, ".po")
                _("po_file_list")
                pp(po_file_list)
                search_file_list.extend(po_file_list)

            if self.find_rst:
                rst_dir = os.environ['BLENDER_MAN_EN']
                if rst_dir:
                    rst_dir = os.path.join(rst_dir, "manual")
                    _("rst_dir:", rst_dir)

                rst_file_list = self.getFileList(rst_dir, ".rst")
                _("rst_file_list")
                pp(rst_file_list)
                search_file_list.extend(rst_file_list)

            if self.find_py:
                py_dir = os.environ['LOCAL_PYTHON_3']
                if py_dir:
                    _("py_dir:", py_dir)

                py_file_list = self.getFileList(py_dir, ".py")
                _("py_file_list")
                pp(py_file_list)
                search_file_list.extend(py_file_list)

            if self.find_src:
                src_dir = os.environ['BLENDER_SRC']
                if src_dir:
                    _("src_dir:", src_dir)

                py_list = self.getFileList(src_dir, ".py")
                cc_list = self.getFileList(src_dir, ".cc")
                cpp_list = self.getFileList(src_dir, ".cpp")
                c_list = self.getFileList(src_dir, ".c")
                h_list = self.getFileList(src_dir, ".h")
                #_("py_file_list")
                ##pp(py_file_list)
                #pp(py_list)
                #pp(cc_list)
                if py_list:
                    search_file_list.extend(py_list)
                if cc_list:
                    search_file_list.extend(cc_list)
                if cpp_list:
                    search_file_list.extend(cpp_list)
                if c_list:
                    search_file_list.extend(c_list)
                if h_list:
                    search_file_list.extend(h_list)

        _(f'search_file_list:{search_file_list}')
        has_file = (len(search_file_list) > 0)
        if not has_file:
            _("No files to search! Terminate.")
            return

        is_po_only = (self.find_po and not (self.find_py or self.find_rst or self.find_src)) or self.vipo_file
        is_replace = ((self.replace_pattern is not None) and is_po_only) or (self.letter_case != LetterCase.NO_CHANGE)

        # _("SEARCHING:")
        for f in search_file_list:
            #_("processing:", f, "for", self.find_pattern)
            setfilename(f)
            if is_replace:
                self.replaceInPOFile(f)
            else:
                self.findPatternInFile(f)
            resetfilenameshowed()

    def listingRange(self, data_list, found_index):
        has_from_line = (self.from_line >= 0)
        has_to_line = (self.to_line >= 0)

        max_lines = len(data_list)
        if has_from_line:
            min_range = [0, found_index - self.from_line]
            from_line = max(min_range)
            _("from_line", from_line)
        else:
            from_line = found_index
            _("from_line", from_line)

        if has_to_line:
            max_range = [found_index + self.to_line + 1, max_lines]
            to_line = min(max_range)
            _("to_line", to_line)
        else:
            max_range = [found_index + 1, max_lines]
            to_line = min(max_range)
            _("to_line", to_line)

        _("found_index", found_index, "from_line", from_line, "to_line", to_line)
        for index in range(from_line, to_line):
            text_line = data_list[index]
            if self.only_match:
                if self.invert_match:
                    replaced_line=self.find_pattern.sub(INVERT_SEP, text_line)
                    match_list = replaced_line.split(INVERT_SEP)
                else:
                    match_list = self.getAllMatchedWordFromLine(self.find_pattern, text_line)
                match_text = "\n".join(match_list)
            else:
                match_text = text_line

            entry = {index: match_text}
            self.found_lines_dic.update(entry)
            _(entry)


    def reportFind(self, data):
        data_list = data.split('\n')

        for line_no, data_line in enumerate(data_list):
            if self.invert_match:
                if self.only_match:
                    # print('invert_match and only match')
                    replaced_line=self.find_pattern.sub(INVERT_SEP, data_line)
                    exc_list = replaced_line.split(INVERT_SEP)
                    is_found = (len(exc_list) > 0)
                else:
                    # print('invert_match and normal')
                    is_found = (self.find_pattern.search(data_line) == None)
            else:
                # print('NOT invert')
                is_found = (self.find_pattern.search(data_line) != None)

            if is_found:
                #print(line_no, data_line)
                self.listingRange(data_list, line_no)

        has_result = (len(self.found_lines_dic) > 0)
        if has_result:
            showfilename()
            if self.show_line_number:
                pp(self.found_lines_dic)
            else:
                for k, v in self.found_lines_dic.items():
                    print(v)

    def findPatternInFile(self, file_path):
        data = self.basic_io.readTextFile(file_path)

        # flag = (re.I if self.case_sensitive else 0)

        #found_list = re.findall(self.find_pattern, data, flags=flag)
        found_list = self.find_pattern.findall(data)
        is_found = (len(found_list) > 0)
        if is_found:
            #pp(found_list)
            self.reportFind(data)
            # _("Found in:", file_path)
            # _("-" * 80)

    def switchExistingTextsCase(self, txt):
        #print("switchExistingTextsCase", txt, type(txt))

        changed_count = 0
        new_txt = str(txt)
        for orig, _ in self.patternMatchAll(self.find_pattern, txt):
            s, e, found_txt = orig
            orig_txt = str(found_txt)
            if self.letter_case == LetterCase.LOWER_CASE:
                found_txt = found_txt.lower()
            elif self.letter_case == LetterCase.UPPER_CASE:
                found_txt = found_txt.upper()
            elif self.letter_case == LetterCase.CAPITAL_CASE:
                first_letter = found_txt[0]
                first_letter = first_letter.upper()
                found_txt = first_letter + found_txt[1:]
            elif self.letter_case == LetterCase.TITLE_CASE:
                found_txt = found_txt.title()

            new_txt = new_txt[:s] + found_txt + new_txt[e:]
            is_changed = (found_txt != orig_txt)
            changed_count += (1 if is_changed else 0)
            #_("switchExistingTextsCase from:", txt, "=>", new_txt, changed_count)
        return new_txt, changed_count


    def replaceInPOFile(self, file_path):
        changed = False
        po_cat = c.load_po(file_path)
        for index, m in enumerate(po_cat):
            is_ignore = (index == 0)
            if is_ignore:
                continue

            old_translation = m.string
            has_translation = (old_translation and (len(old_translation) > 0 ))
            if not has_translation:
                continue

            is_changing_case = (self.letter_case != LetterCase.NO_CHANGE)
            if is_changing_case:
                new_translation, n_changed = self.switchExistingTextsCase(old_translation)
            else:
                new_translation, n_changed = re.subn(self.txt_find_pattern, self.replace_pattern, old_translation, flags=self.pattern_flag)
            has_changed = (n_changed > 0)
            if has_changed:
                m.string = new_translation
                changed = True
                showfilename()
                print("Replaced:")
                print(f'old msgstr \"{old_translation}\"')
                print(f'new msgstr \"{new_translation}\"')

        is_writing_changes = (changed and not self.testing_only)
        if is_writing_changes:
            c.dump_po(file_path, po_cat)
            _("Wrote changes to:", file_path)
            _("-" * 80)

    def getFileList(self, directory, extension):
        mod_file_list = []
        valid = (directory is not None) and (len(directory) > 0) and os.path.isdir(directory)
        if not valid:
            return mod_file_list

        modi_file_callback = findFileByExtension(extension)
        self.basic_io.listDir(directory, modi_file_callback)
        mod_file_list = modi_file_callback.getListSorted()
        return mod_file_list

    def run(self):
        # _("Hoang Duy Tran")
        self.find()


parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-p", "--pattern", dest="find_pattern", help="Pattern to find.")
parser.add_argument("-R", "--replace_pattern", dest="replace_pattern", help="Pattern to replace. Only works with PO files and in msgstr entries. Not currently support INVERT match")

parser.add_argument("-CL", "--case_low", dest="case_lower", help="Replaced find pattern with lowercase version in PO tranlation string", action='store_const', const=True)
parser.add_argument("-CU", "--case_up", dest="case_upper", help="Replaced find pattern with uppercase version in PO tranlation string", action='store_const', const=True)
parser.add_argument("-CC", "--case_cap", dest="case_capital", help="Replaced find pattern with capital first character version in PO tranlation string", action='store_const', const=True)
parser.add_argument("-CT", "--case_title", dest="case_title", help="Replaced find pattern with title case (capitalised first character of each word) version in PO tranlation string", action='store_const', const=True)

parser.add_argument("-o", "--po", dest="find_po", help="Find in $BLENDER_MAN_VI/LC_MESSAGES.", action='store_const', const=True)
parser.add_argument("-r", "--rst", dest="find_rst", help="Find in $BLENDER_MAN_EN/manual.", action='store_const', const=True)
parser.add_argument("-s", "--src", dest="find_src", help="Find in $BLENDER_ae.", action='store_const', const=True)
parser.add_argument("-y", "--py", dest="find_py", help="Find in $LOCAL_PYTHON_3.", action='store_const', const=True)
parser.add_argument("-c", "--case", dest="case_sensitive", help="Find with case sensitive.", action='store_const', const=True)
parser.add_argument("-A", "--after", dest="after_lines", help="Listing this number of lines AFTER the found lines as well.")
parser.add_argument("-B", "--before", dest="before_lines", help="Listing this number of line BEFORE the found lines as well.")
parser.add_argument("-f", "--file", dest="find_file", help="Find in a specific file only.")
parser.add_argument("-l", "--line", dest="show_line_number", help="Showing matched line number next to the found text.", action='store_const', const=True)
parser.add_argument("-v", "--invert_match", dest="invert_match", help="Invert match, find text DOESN'T match the input pattern.", action='store_const', const=True)
parser.add_argument("-O", "--only_match", dest="only_match", help="Listing only the matched part of the text.", action='store_const', const=True)
parser.add_argument("-t", "--testing_only", dest="testing_only",
                    help="Print out changes only, but DO NOT write changes. For examinations before commit changes. Only applicable with replacing translations in PO files.",
                    action='store_const', const=True)
parser.add_argument("-D", "--debug", dest="debugging", help="Print out messages as processing.", action='store_const', const=True)
parser.add_argument("-vi", "--vipo", dest="vipo_file", help="Find text in vi.po file, the latest version in $BLENDER_GITHUB", action='store_const', const=True)

args = parser.parse_args()

x = FindFilesHasPattern()
x.setVars(
    args.find_pattern,
    args.replace_pattern,
    args.case_lower,
    args.case_upper,
    args.case_capital,
    args.case_title,
    args.find_file,
    args.vipo_file,
    args.find_po,
    args.find_rst,
    args.find_py,
    args.find_src,
    args.case_sensitive,
    args.before_lines,
    args.after_lines,
    args.only_match,
    args.show_line_number,
    args.invert_match,
    args.testing_only,
    args.debugging,
    )

x.run()
