#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Hoang Duy Tran <hoangduytran1960@gmail.com>
# Revision Date: 2020-02-02 09:59+0000
#
import hashlib
import os
import re
import sys
translate_po_path = os.path.join(os.environ['HOME'], 'blender_manual/potranslate')
local_lib_path = '/usr/local/lib/python3.7/site-packages'
sys.path.append( translate_po_path )
sys.path.append( local_lib_path )

import math
import locale
import datetime
from collections import OrderedDict, defaultdict
from pprint import pprint as PP
from time import gmtime, strftime, time
from pytz import timezone
from argparse import ArgumentParser
from pprint import pprint
from sphinx_intl import catalog as c
from babel.messages import pofile
from enum import Enum
# import chardet
from translation_finder import TranslationFinder
from reflink import RefList, TranslationState
from reftype import RefType
from common import Common as cm
from common import DEBUG
from ignore import Ignore as ig
from pprint import pprint
import json


INVERT_SEP='•'
TESTING = False
TESTING = True

def readJSON(file_path):
    with open(file_path) as in_file:
        dic = json.load(in_file, object_pairs_hook=OrderedDict)
    return dic

def writeJSON(file_path, data):
    with open(file_path, 'w+', newline='\n', encoding='utf8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

escape_char = re.compile(r'[\\\s]+')

def patternMatchOnly(pat, text):
    try:
        return_dict = {}
        # is_debug = ('Previous Component' in text)
        # if is_debug:
        #     _('DEBUG')
        for m in pat.finditer(text):
            original = ()
            # break_down = []

            s = m.start()
            e = m.end()
            orig = m.group(0)
            original = (s, e, orig)
            entry = {(s,e): orig}
            return_dict.update(entry)
    except Exception as e:
        _("patternMatchAll")
        _("pattern:", pat)
        _("text:", text)
        _(e)
    return return_dict

def patternMatchAllMatches(pat, text):
    try:
        return_dict = {}
        is_debug = ('Previous Component' in text)
        if is_debug:
            _('DEBUG')
        for m in pat.finditer(text):
            original = ()
            # break_down = []

            s = m.start()
            e = m.end()
            orig = m.group(0)
            original = (s, e, orig)
            entry = {(s,e): orig}
            return_dict.update(entry)

            for g in m.groups():
                if g:
                    i_s = orig.find(g)
                    ss = i_s + s
                    ee = ss + len(g)
                    v=(ss, ee, g)
                    # break_down.append(v)
                    entry = {(ss, ee): g}
                    return_dict.update(entry)
    except Exception as e:
        _("patternMatchAll")
        _("pattern:", pat)
        _("text:", text)
        _(e)
    return return_dict

class FoundRecord(OrderedDict):
    def __init__(self, filename):
        self.file_name = filename
    @property
    def filename(self):
        return self.file_name

    @filename.setter
    def filename(self, new_name):
        self.file_name = new_name

    def show(self):
        has_items = (len(self) > 0)
        if not has_items:
            return

        if self.file_name:
            print(f'file_name:{self.file_name}')
            print('-' * 80)

        for loc, line in self.items():
            print(f'{loc}: {line}')
        print()

    def addFound(self, loc, line):
        entry = {loc: line}
        self.update(entry)

    def reset(self):
        self.file_name = None
        self.clear()

class ShowFileName:
    def __init__(self):
        self.CURRENT_FILE_NAME = None
        self.FILE_NAME_SHOWED = False

    @property
    def fileName(self):
        return self.CURRENT_FILE_NAME

    @fileName.setter
    def fileName(self, name):
        if not name:
            self.CURRENT_FILE_NAME = name
            return

        is_debug = ('__init__' in name) and ('babel' in name)
        if is_debug:
            print('DEBUG')
        self.CURRENT_FILE_NAME = name

    @property
    def showed(self):
        return self.FILE_NAME_SHOWED

    @showed.setter
    def showed(self, value):
        self.FILE_NAME_SHOWED = value

    def reset(self):
        self.fileName = None
        self.showed = False

    def showFileName(self, extra=None):
        if not self.fileName:
            return

        if self.showed:
            return

        if extra:
            print(f'{extra} {self.fileName}')
        else:
            print(f'{self.fileName}')
        print("="*80)
        self.showed = True

fname_shower = ShowFileName()

def pp(object, stream=None, indent=1, width=80, depth=None, *args, compact=False):
    if DEBUG:
        file_name = fname_shower.fileName
        if file_name:
            print(f'file_name:{file_name}')
        pprint(object, stream=stream, indent=indent, width=width, depth=depth, *args, compact=compact)
        print('-' * 30)

def _(*args, **kwargs):
    if DEBUG:
        file_name = fname_shower.fileName
        if file_name:
            print(f'file_name:{file_name}')
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

class SortOrder(Enum):
    ALPHABET='A',
    ALPHABET_INVERT='AI',
    LENGTH='L',
    LENGTH_INVERT='LI'
    UNKNOWN = None

    # @classmethod
    # def asDict(cls):
    #     return {
    #         SortOrder.ALPHABET.value: SortOrder.ALPHABET,
    #         SortOrder.ALPHABET_INVERT.value: SortOrder.ALPHABET_INVERT,
    #         SortOrder.LENGTH.value: SortOrder.LENGTH,
    #         SortOrder.LENGTH_INVERT.value: SortOrder.LENGTH_INVERT,
    #             }
    #
    # @classmethod
    # def findType(cls, text):
    #     cls.asDict()[text]
    #     member : SortOrder = None
    #     for name, member in cls.__members__.items():
    #         value = member.value
    #         val = value[0]
    #         is_found = val.lower() == text.lower()
    #         if is_found:
    #             return member
    #     else:
    #         return cls.UNKNOWN

class FindFilesHasPattern:

    def __init__(self):
        self.basic_io = BasicIO()
        self.found_lines_dic = {}
        self.found_record: FoundRecord = None
        self.global_found_list = {}
        self.global_count = defaultdict(int)
        self.writing = False

    def setWriting(self, value: bool):
        old_value = self.writing
        self.writing = value
        print(f'setWriting: {old_value} => {self.writing}')

    def isWriting(self):
        print(f'isWriting: {self.writing}')
        return self.writing

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
            find_bracketed,
            bracket_pair_to_find,
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
            find_gettext,
            find_py_lib,
            find_src,
            case_sensitive,
            before_lines,
            after_lines,
            only_match,
            show_line_number,
            invert_match,
            testing_only,
            debugging,
            sort_order,
            marking,
            output_json
            ):


        self.is_po = False
        self.json_dic = {}
        self.output_json = (True if output_json else False)
        self.is_stdout_redirected = (not sys.stdout.isatty())
        self.find_file = (find_file if (find_file and os.path.isfile(find_file)) else None)
        self.find_po = (True if find_po else False)
        self.find_rst = (True if find_rst else False)
        self.find_py = (True if find_py else False)
        self.find_gettext = (True if find_gettext else False)
        self.find_py_lib = (True if find_py_lib else False)
        self.vipo_file = (True if vipo_file else False)
        self.find_src = (True if find_src else False)

        self.is_po = (self.find_po or self.find_gettext)

        self.from_line = (int(before_lines) if before_lines else -1)
        self.to_line = (int(after_lines) if after_lines else -1)
        self.only_match = (True if only_match else False)
        self.show_line_number = (True if show_line_number else False)
        self.invert_match = (True if invert_match else False)
        self.testing_only = (True if testing_only else False)
        self.sort_order = (SortOrder.__members__[sort_order] if sort_order in SortOrder.__members__ else SortOrder.UNKNOWN)
        self.is_marking = (True if marking else False)
        self.case_sensitive = (True if case_sensitive else False)

        self.debugging_path = None
        self.is_debugging = False
        DEBUG = False
        if debugging:
            self.is_debugging = True
            DEBUG = True
            self.debugging_path = debugging
            print(f'DEBUGGING: {DEBUG}, self.deubugging_path={self.debugging_path}')

        self.letter_case = self.getCase(lower_case, upper_case, capital_case, title_case)

        self.pattern_flag = (re.I if not self.case_sensitive else 0)
        #self.input_pattern = find_pattern

        self.find_pattern = None
        self.replace_pattern = None


        if find_pattern is not None:
            self.find_pattern = re.compile(r'{}'.format(find_pattern), flags=self.pattern_flag)

        if replace_pattern is not None:
            self.replace_pattern = replace_pattern

        self.find_pattern = re.compile(r'[\"]([^\"]+)[\"]')
        self.is_find_bracketed = (True if find_bracketed else False)
        self.bracket_pair = (bracket_pair_to_find if bracket_pair_to_find else None)
        self.open_bracket = None
        self.close_bracket = None
        if self.is_find_bracketed:
            try:
                # self.find_pattern = re.compile(r'\(.*?\)')
                self.open_bracket = (self.bracket_pair[0] if self.bracket_pair else '(')
                self.close_bracket = (self.bracket_pair[1] if self.bracket_pair else ')')

                if self.invert_match:
                    pat = fr'\{self.open_bracket}.*?\{self.close_bracket}'
                else:
                    pat = fr'\{self.open_bracket}(.*?)\{self.close_bracket}'
                self.find_pattern = re.compile(pat)
                # print(f'self.open_bracket:{self.open_bracket}; self.close_bracket:{self.close_bracket}')
            except Exception as e:
                pass


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



    def getAllMatchedWordFromLine(self, pattern, text_line):
        list_of_matches=[]
        for origin, breakdown in self.patternMatchAll(pattern, text_line):
            is_end = (origin is None)
            if is_end:
                break

            s, e, orig = origin
            list_of_matches.append(orig)
        return list_of_matches

    def findBracketted(self, txt):
        from pyparsing import nestedExpr

        # define parser
        parser = nestedExpr(self.open_bracket, self.close_bracket)("content")

        # search input string for matching keyword and following braced content
        matches = parser.searchString(txt)

        list_of_matches = (' '.join(map(str, sl)) for sl in matches)
        final_list = []
        for entry in list_of_matches:
            list_entry = ''.join(entry)
            string_entry = list_entry.replace('[', self.open_bracket)
            string_entry = string_entry.replace(']', self.close_bracket)
            string_entry = string_entry.replace('\'', '')
            final_list.append(string_entry)
        return final_list

    def getListOfFiles(self) -> list:
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

            if self.find_py_lib:
                py_dir = os.environ['PYTHONPATH']
                if py_dir and py_dir.endswith(':'):
                    py_dir = py_dir[:-1]

                py_dir_list = py_dir.split(':')
                for p_dir in py_dir_list:
                    _(f'p_dir:{p_dir}')
                    py_file_list = self.getFileList(p_dir, ".py")
                    _("py_file_list")
                    pp(py_file_list)
                    search_file_list.extend(py_file_list)

            if self.find_py:
                py_dir = os.environ['LOCAL_PYTHON_3']
                if py_dir:
                    _("py_dir:", py_dir)

                py_file_list = self.getFileList(py_dir, ".py")
                _("py_file_list")
                pp(py_file_list)
                search_file_list.extend(py_file_list)

            if self.find_gettext:
                gettext_dir = os.environ['BLENDER_MAN_EN']
                if gettext_dir:
                    gettext_dir = os.path.join(gettext_dir, "build/gettext")
                    _("gettext_dir:", gettext_dir)

                gettext_file_list = self.getFileList(gettext_dir, ".pot")
                _("gettext_file_list")
                pp(gettext_file_list)
                search_file_list.extend(gettext_file_list)

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

        if self.debugging_path:
            temp_list = []
            for f in search_file_list:
                is_debugging_file = (self.debugging_path in f)
                if is_debugging_file:
                    temp_list.append(f)
            search_file_list = temp_list
        pprint(search_file_list)
        return search_file_list

    def find(self):

        search_file_list = self.getListOfFiles()

        _(f'search_file_list:{search_file_list}')
        has_file = (len(search_file_list) > 0)
        if not has_file:
            _("No files to search! Terminate.")
            return


        is_po_only = (self.find_po and not (self.find_py or self.find_rst or self.find_src)) or self.vipo_file
        is_replace = ((self.replace_pattern is not None) and is_po_only) or (self.letter_case != LetterCase.NO_CHANGE)

        # _("SEARCHING:")
        for f in search_file_list:
            self.found_record = FoundRecord(f)
            if is_replace:
                self.replaceInPOFile(f)
            else:
                self.findPatternInFile(f)
            self.found_record.show()
            self.found_record.reset()

    def foundDataToDic(self, found_data):
        if not self.output_json:
            return

        is_list = isinstance(found_data, list)
        if is_list:
            for k in found_data:
                if not k.isascii():
                    continue

                v = ""
                entry = {k:v}
                # print(f'json_dic.update entry from list: {entry}')
                self.json_dic.update(entry)
        else:
            k = found_data
            if not k.isascii():
                return

            v = ""
            entry = {k:v}
            # print(f'json_dic.update entry from text: {entry}')
            self.json_dic.update(entry)

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
        added_count=0
        for index in range(from_line, to_line):
            text_line = data_list[index]
            is_added = False
            if self.only_match:
                if self.invert_match:
                    replaced_line=self.find_pattern.sub(INVERT_SEP, text_line)
                    match_list = replaced_line.split(INVERT_SEP)
                    match_text = "\n".join(match_list)
                else:
                    if self.is_find_bracketed:
                        found_list = self.findBracketted(text_line)
                    else:
                        found_list = self.find_pattern.findall(text_line)

                    if found_list:
                        self.foundDataToDic(found_list)
                        match_text = '; '.join(found_list)
                        is_added = True
                    else:
                        match_text = str(text_line)
            else:
                match_text = str(text_line)

            if not is_added:
                self.foundDataToDic(match_text)

            if self.is_marking and not self.is_stdout_redirected:
                match_text = self.markingText(index, text_line, self.find_pattern)

            entry = {index: match_text}
            self.found_record.update(entry)
            added_count += 1
            # self.found_lines_dic.update(entry)
            # _(entry)
        if added_count:
            entry = {-1 * index: '-' * 20}
            self.found_record.update(entry)


    def insertFoundIntoGlobalList(self, data_line):
        if self.invert_match:
            replaced_line=self.find_pattern.sub(INVERT_SEP, data_line)
            exc_list = replaced_line.split(INVERT_SEP)
            for txt in exc_list:
                hash_rec = hashlib.sha256(txt.encode('utf-8'))
                key = hash_rec.digest()
                entry = {key: txt}
                self.global_found_list.update(entry)
                self.global_count[txt] += 1
        else:
            temp_file_list = patternMatchAllMatches(self.find_pattern, data_line)
            for loc, txt in temp_file_list.items():
                hash_rec = hashlib.sha256(txt.encode('utf-8'))
                key = hash_rec.digest()
                entry = {key: txt}
                self.global_found_list.update(entry)
                self.global_count[txt] += 1

    def reportFind(self, data):
        data_list = data.split('\n')

        for line_no, data_line in enumerate(data_list):
            if self.invert_match:
                if self.only_match:
                    _('invert_match and only match')
                    replaced_line=self.find_pattern.sub(INVERT_SEP, data_line)
                    exc_list = replaced_line.split(INVERT_SEP)
                    is_found = (len(exc_list) > 0)
                else:
                    is_found = (self.find_pattern.search(data_line) is None)
            else:
                _('NOT invert')
                is_found = (self.find_pattern.search(data_line) is not None)

            if is_found:
                self.insertFoundIntoGlobalList(data_line)
                _(line_no, data_line)
                self.listingRange(data_list, line_no)

        # has_result = (len(self.found_lines_dic) > 0)
        # if has_result:
        #     fname_shower.showFileName(extra='reportFind: has_result=')
        #     if self.show_line_number:
        #         pp(self.found_lines_dic)
        #     else:
        #         f_name = fname_shower.fileName
        #         for k, v in self.found_lines_dic.items():
        #             if f_name:
        #                 print(f'{f_name}:{v}')
        #             else:
        #                 print(v)

    def poFileToDataBlock(self, file_path):
        po_cat = c.load_po(file_path)
        data_list = []
        for m in po_cat:
            k = m.id
            if not k:
                continue

            data_list.append(k)
        data_block = "\n".join(data_list)
        return data_block

    def findPatternInFile(self, file_path):
        if self.is_po:
            data = self.poFileToDataBlock(file_path)
        else:
            data = self.basic_io.readTextFile(file_path)

        found = self.find_pattern.search(data)
        is_found = True
        if not self.invert_match:
            is_found = bool(found)

        if is_found:
            #pp(found_list)
            self.reportFind(data)
            # _("Found in:", file_path)
            # _("-" * 80)

    def switchExistingTextsCase(self, txt):
        new_txt = str(txt)
        if self.letter_case == LetterCase.LOWER_CASE:
            new_txt = txt.lower()
        elif self.letter_case == LetterCase.UPPER_CASE:
            new_txt = txt.upper()
        elif self.letter_case == LetterCase.CAPITAL_CASE:
            first_letter = txt[0]
            first_letter = txt.upper()
            new_txt = first_letter + txt[1:]
        elif self.letter_case == LetterCase.TITLE_CASE:
            new_txt = txt.title()
        return new_txt

    def markingText(self, line_number, text_to_mark, pattern_to_find):
        text_marked = str(text_to_mark)
        loc_text_dict = patternMatchOnly(pattern_to_find, text_to_mark)
        reversed_loc_text_dict = list(reversed(list(loc_text_dict.items())))

        for loc, txt in reversed_loc_text_dict:
            s, e = loc
            left = text_marked[:s]
            right = text_marked[e:]
            mid = f'{bcolors.OKGREEN}{txt}{bcolors.ENDC}'
            text_marked = left + mid + right
            entry = {line_number: txt}
            self.found_record.update(entry)
        return text_marked

    def replaceInPOFile(self, file_path):
        changed = False
        change_case = (self.letter_case != LetterCase.NO_CHANGE)
        po_cat = c.load_po(file_path)
        unescaped_replace_pattern = escape_char.sub(' ', self.replace_pattern)
        for index, m in enumerate(po_cat):
            is_ignore = (index == 0)
            if is_ignore:
                continue

            old_translation = m.string
            has_translation = (old_translation and (len(old_translation) > 0 ))
            if not has_translation:
                continue

            new_translation = str(old_translation)
            report_old = str(old_translation)
            report_new = str(old_translation)

            has_changed = False
            found_list = patternMatchOnly(self.find_pattern, old_translation)
            reversed_found_list = sorted(list(found_list.items()), reverse=True)
            for loc, found_txt in reversed_found_list:
                self.global_count[found_txt] += 1
                s, e = loc
                left = old_translation[:s]
                right = old_translation[e:]

                if change_case:
                    mid = self.switchExistingTextsCase(found_txt)
                else:
                    # mid = self.replace_pattern
                    mid = unescaped_replace_pattern

                new_translation = left + mid + right
                has_changed = True
                if self.is_marking:
                    mid_old = f'{bcolors.OKGREEN}{found_txt}{bcolors.ENDC}'
                    mid_new = f'{bcolors.OKGREEN}{unescaped_replace_pattern}{bcolors.ENDC}'
                else:
                    mid_old = found_txt
                    mid_new = unescaped_replace_pattern

                report_old = report_old[:s] + mid_old + report_old[e:]
                report_new = report_new[:s] + mid_new + report_new[e:]

            if has_changed:
                # new_translation = escape_char.sub(' ', new_translation)
                m.string = new_translation
                changed = True

            is_shown = (has_changed or self.invert_match)
            if is_shown:
                self.found_record.addFound(m.lineno, f'Replaced:\nold msgstr \"{report_old}\"\nnew msgstr \"{report_new}\"')

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

    def tranRef(self, msg, is_keep_original, tran_finder):
        ref_list = RefList(msg=msg, keep_orig=is_keep_original, tf=tran_finder)
        ref_list.parseMessage()
        ref_list.translateRefList()
        tran = ref_list.getTranslation()
        return tran

    def patternMatchAllToDict(self, pat, text):
        matching_list = {}
        for m in pat.finditer(text):
            orig = m.group(0)
            s = m.start()
            e = m.end()
            k = (s, e)
            entry = {k: orig}
            matching_list.update(entry)
        return matching_list


    # def isConsidered(self, ref_type):
    #     is_keyboard = (ref_type == RefType.KBD.value)
    #     is_menu = (ref_type == RefType.MENUSELECTION.value)
    #     is_term = (ref_type == RefType.TERM.value)
    #     is_abbr = (ref_type == RefType.ABBR.value)
    #     is_gui = (ref_type == RefType.GUILABEL.value)
    #     is_term = (ref_type == RefType.TERM.value)
    #     is_ref = (ref_type == RefType.REF.value)
    #     return (is_keyboard or is_menu or is_term or is_abbr or is_gui or is_ref or is_term)

    find_pat_list = [
        # re.compile(r'[\(]+(.*?)[\)]+'), # ARCH_BRAKET_MULTI
        # re.compile(r"(?<!\w)\'([^\']+)(?:\b)\'"), # single quote
        # re.compile(r"(?<!\w)\*([^\*]+)(?:\b)\*"), # asterisk
        # re.compile(r'"(?<!\\")(.*?)"'),         # double quote
        # re.compile(r'[\`]*(:[^\:]+:)?[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]?'),
        # (cm.OSL_ATTRIB, RefType.OSL_ATTRIB),
        # OSL_ATTRIB(re.compile(r''), RefType.ARCH_BRACKET),

        (cm.AST_QUOTE, RefType.AST_QUOTE),
        (cm.DBL_QUOTE, RefType.DBL_QUOTE),
        (cm.SNG_QUOTE, RefType.SNG_QUOTE),
        (cm.RGBA, RefType.TEXT),
        (cm.GA_REF, RefType.GA),
        (re.compile(r'()'), RefType.ARCH_BRACKET),
    ]

    def isParsingRequired(self, txt):
        for p, ref_type in self.find_pat_list:
            if ref_type is RefType.ARCH_BRACKET:
                m = cm.getTextWithinBrackets('(', ')', txt, is_include_bracket=False)
            else:
                m = p.search(txt)

            is_required = (m is not None and len(m) > 0)
            if is_required:
                return True
        return False

    def translate_word_into_dict(self, k:str, dict_tf: TranslationFinder, dict_to_insert:OrderedDict, is_translating_ref=False):
        if is_translating_ref:
            cm.debugging(k)
            ref_list: RefList = None
            ref_list = RefList(msg=k, keep_orig=False, tf=dict_tf)
            ref_list.parseMessage()
            ref_list.translateRefList()
            trans = ref_list.getTranslation()
            is_ignore = (ref_list.isIgnore())
            is_fuzzy = (ref_list.isFuzzy())
        else:
            trans, is_fuzzy, is_ignore = dict_tf.translate(k)

        # # trans, is_fuzzy, is_ignore = dict_tf.translate(k)
        if is_ignore:
            print(f'IGNORED: {k}')
            return

        if not trans:
            trans = ""

        if not is_fuzzy:
            key = f'&&{k}'
            entry = {key: trans}
        else:
            entry = {k: trans}
        print(f'translate_word_into_dict translated entry:{entry}')
        dict_to_insert.update(entry)

    def extract_bracket_texts_from_gtx(self):

        def processingData(data):
            found_dict = {}
            data_lines = data.split('\n')
            for text_line in data_lines:
                remain_line = str(text_line)
                for p, ref_type in self.find_pat_list:
                    try:
                        if ref_type is RefType.ARCH_BRACKET:
                            found_items = cm.getTextWithinBrackets('(', ')', text_line, is_include_bracket=False)
                        else:
                            found_items = cm.patternMatchAllAsDictNoDelay(p, remain_line)
                        if not found_items:
                            continue

                        print(f'{p.pattern}')
                        for k, v in found_items.items():
                            item_ref_type = None
                            value_length = len(v)
                            if value_length == 3:
                                orig, sub_type, sub_txt = v
                                o_loc, o_txt = orig
                                r_loc, ref_type_txt = sub_type

                                item_ref_type = RefType.getRef(ref_type_txt)
                                blank_loc, blank_txt = orig
                                record_loc, record_txt = sub_txt
                            elif value_length == 2:
                                orig, sub_txt = v
                                o_loc, o_txt = orig

                                blank_loc, blank_txt = orig
                                record_loc, record_txt = sub_txt
                            elif value_length == 1:
                                orig = v[0]

                                blank_loc, blank_txt = orig
                                record_loc, record_txt = orig

                            # blank_str = (cm.FILLER_CHAR * len(blank_txt))
                            # blank_s, blank_e = blank_loc
                            # left = remain_line[:blank_s]
                            # right = remain_line[blank_e:]
                            # remain_line = left + blank_str + right

                            if not item_ref_type:
                                entry = {record_txt: ref_type}
                            else:
                                entry = {record_txt: item_ref_type}
                            print(f'entry:{entry} v:"{v}"')
                            found_dict.update(entry)
                    except Exception as e:
                        print(f'text_line:{text_line} ref_type:{ref_type} p:{p}')
                        print(e)
                        raise e

            temp_list = list(found_dict.items())
            new_dict_sorted = OrderedDict(temp_list)
            self.setWriting(False)
            return new_dict_sorted

        def testFindText():
            data = '''
:abbr:`API (Application Programming Interface)`
:abbr:`BSDF (Bidirectional Scattering Distribution Function)`
:abbr:`BSSRDF (Bidirectional subsurface scattering distribution function)`
:abbr:`CAD (Computer-Aided Design)`
:abbr:`CGI (Computer-Generated Imagery)`
like ''textures'' for instance
hold :kbd:`NumpadPlus` or :kbd:`Ctrl-MMB` or similar
see :doc:`Normals'
see :ref:`temp-dir` for details
this bracketed line  (will 'cause' some *translation* to be "done internally" or :kbd:`Ctrl-MMB` :menuselection:`View --> Show Curve Extremes` here).
this is the same thing as the *Playback Range* option of the :ref:`Timeline editor header <animation-editors-timeline-headercontrols>`
and optionally *Topology Mirror* if your mesh is not symmetric
visible if :menuselection:`View --> Show Curve Extremes` are enabled
which remains in *Pose Mode*
which you might call "sun", what do you think?
``INSERT(ATTRIB+XDATA)``
with components like "L", "R", "right", "left"
with holding :kbd:`Alt`'
            '''
            # data = "With the \"traditional\" representation of three bytes, like RGB(124, 255, 56), the multiplications give far too high results, like RGB(7316, 46410, 1848), that have to be normalized (brought back) by dividing them by 256 to fit in the range of (0 to 255)..."
            # data = "(will 'cause' some *translation* to be \"done internally\" or :kbd:`Ctrl-MMB` :menuselection:`View --> Show Curve Extremes` here)"
            # data = "see the :doc:`Particle Physics </physics/particles/emitter/physics/index>` page"
            # data = "Similar to regular *Established Ocean* however, waves will continue to grow with time creating sharper peaks (:abbr:`JONSWAP (JOint North Sea WAve Project)` and Pierson-Moskowitz method). An extra parameter is used to define the sharpness of these peaks."
            # data = "``(LW)POLYLINE``, ``(LW)POLYGON`` as ``POLYLINE`` curve if they have no bulges else as ``BEZIER`` curve."
            # data = "Index of the pose to apply (-2 for no change, -1 to use the active pose)."
            # data = "Refers to the general color decomposition resulting in *Y* (Luminance) and *C* (Chrominance) channels, whereas the chrominance is represented by: U = ( Blue minus Luminance ) and V = ( Red minus Luminance )."
            # data = ":menuselection:`Sidebar region --> Cursor`."
            # data = "like 'textures' for instance"
            # data = "``//render_`` becomes ``//render_####``, writing frames as ``//render_0001.png``"
            # data = "Refers to the general color decomposition resulting in *Y* (Luminance) and *C* (Chrominance) channels, whereas the chrominance is represented by: U = ( Blue minus Luminance ) and V = ( Red minus Luminance )."
            # data = "Constraints are a way to control an object's properties (e.g. its location, rotation, scale), using either plain static values (like the :doc:`\"limit\" ones </animation/constraints/transform/limit_location>`), or another object, called \"target\" (like e.g. the :doc:`\"copy\" ones </animation/constraints/transform/copy_location>`)."
            # data = "This example node tree does not use the Render Layer node. To produce this 2-second animation, no Blender scene information was used. This is an example of using Blender's powerful compositing abilities separate from its modeling and animation capabilities. (A Render Layer could be substituted for the Image layer, and the \"fade-network\" effect will still produce the same effect.)"
            found_dict = {}
            # home = os.environ['HOME']
            # test_file = os.path.join(home, 'findgettext_cleaned.log')
            # data_lines = []
            # with open(test_file) as f:
            #     data_lines = f.readlines()
            # data_lines = data.split('\n')
            # print('-' * 30)
            # print(f'File:{f}')
            # data = "Developer's `Ask Us Anything! <https://wiki.blender.org/wiki/Reference/AskUsAnything>`__"
            # data = "`Auto Face Map Widgets add-on <https://developer.blender.org/diffusion/BAC/browse/master/object_facemap_auto/>`__"
            # data = "``~/.blender/|BLENDER_VERSION|/config/startup.blend``"
            # data = "`Auto Face Map Widgets add-on <https://developer.blender.org/diffusion/BAC/browse/master/object_facemap_auto/>`__"
            # data = "`#docs <https://blender.chat/channel/docs>`__ For discussion related to Blender's documentation."
            # data = "You can also copy normals from another mesh using Mesh Data Transfer (:doc:`operator </scene_layout/object/editing/relations/transfer_mesh_data>` or :doc:`modifier </modeling/modifiers/modify/data_transfer>`)."
            # data = "Add a meta-rig structure from the :menuselection:`Add --> Armature` menu."
            # data = "This is also available through the :menuselection:`Pose --> Scale Envelope Distance` menu entry, which is only effective in *Envelope* visualization, even though it is always available..."
            data = "After creating your landscape mesh there's three main areas in the :ref:`ui-undo-redo-adjust-last-operation` panel to design your mesh."
            return processingData(data)

        def performActualFindSpecialTerms():
            found_dict = {}
            file_list = self.getListOfFiles()
            for f in file_list:
                data = self.poFileToDataBlock(f)
                data_lines = data.split('\n')
                print('-' * 30)
                print(f'File:{f}')
                so_far_dict = processingData(data)
                found_dict.update(so_far_dict)
            return found_dict

        def writeSortedDict (found_dict: dict):
            # return
            sorted_list = list(found_dict.items())
            sorted_list.sort()
            sorted_dict = OrderedDict(sorted_list)
            if DEBUG:
                for k, v in sorted_dict.items():
                    trans = (v if v and not (v == k) else "")
                    print(f'"{k}": "{trans}",')
                return

            home = os.environ['HOME']
            out_file = os.path.join(home, 'log.json')
            writeJSON(out_file, sorted_dict)

        def translateTheFoundDict(found_dict: dict) -> dict:
            tran_dict = {}
            tf = TranslationFinder()
            for k, ref_type in found_dict.items():
                try:
                    # cm.debugging(k)
                    is_a_link_path = cm.isLinkPath(k)
                    if is_a_link_path:
                        continue

                    print(f'try: k:[{k}]; ref_type:[{ref_type}]')
                    is_dbl_quote = (ref_type == RefType.DBL_QUOTE)
                    is_abbr = (ref_type == RefType.ABBR)
                    is_doc = (ref_type == RefType.DOC)
                    is_kbd = (ref_type == RefType.KBD)
                    is_math = (ref_type == RefType.MATH)
                    is_menu = (ref_type == RefType.MENUSELECTION)
                    is_mod = (ref_type == RefType.MOD)
                    is_ref = (ref_type == RefType.REF)
                    is_sup = (ref_type == RefType.SUP)
                    is_term = (ref_type == RefType.TERM)
                    is_ga = (ref_type == RefType.GA)
                    is_arched_bracket = (ref_type == RefType.ARCH_BRACKET)
                    is_osl_attrib = (ref_type == RefType.OSL_ATTRIB)

                    might_have_link = (is_doc or is_ref or is_term or is_mod or is_ga or is_abbr)

                    '''
                    :abbr:*
                    :doc:*
                    :kbd:*
                    :math:
                    :menuselection:*
                    :mod:*
                    :ref:*
                    :sup:
                    :term:*
                    '''
                    current_tran = tf.isInDict(k)
                    if current_tran:
                        print(f'translated: k:{k}, current_tran:{current_tran}')
                        continue

                    if is_menu:
                        print(f'<IS MENU>')
                        word_list = k.split('-->')
                        for word in word_list:
                            word = word.strip()
                            self.translate_word_into_dict(word,tf, tran_dict)
                        print(f'</IS MENU>')
                    elif is_kbd:
                        print(f'<IS KBD>')
                        trans, is_fuzzy, is_ignore = tf.translateKeyboard(k)
                        entry = {k: trans}
                        tran_dict.update(entry)
                        print(f'</IS KBD>')
                    elif is_abbr:
                        m = cm.ABBR_TEXT_ALL.findall(k)
                        if not m:
                            print(f'SOMETHING WRONG WITH ABBR: {k}, {ref_type}')
                            continue
                        abbr, word = m[0]
                        abbr_tran = tf.isInDict(abbr)
                        word_tran = tf.isInDict(word)
                        has_abbr_tran = bool(abbr)
                        has_word_tran = bool(word_tran)
                        is_ignore_entry = (has_abbr_tran and has_word_tran)
                        if not is_ignore_entry:
                            print(f'<IS ABBR>')
                            if not has_abbr_tran:
                                self.translate_word_into_dict(abbr, tf, tran_dict)
                            if not has_word_tran:
                                self.translate_word_into_dict(word, tf, tran_dict)
                            print(f'</IS ABBR>')
                    elif is_math or is_sup:
                        print(f'IGNORING type:{ref_type}: "{k}"')
                        pass
                    else:
                        m_ref = cm.END_WITH_REF.search(k)
                        is_end_with_ref = (m_ref is not None)
                        if is_end_with_ref:
                            found_dict = cm.findInvert(cm.END_WITH_REF, k)
                            for k, v in found_dict.items():
                                loc, txt = v
                                self.translate_word_into_dict(txt.strip(), tf, tran_dict, is_translating_ref=True)
                        else:
                            self.translate_word_into_dict(k, tf, tran_dict, is_translating_ref=True)
                except Exception as e:
                    print(f'ERROR! {k}, Reftype:{ref_type}')
                    print(e)
                    raise e
            tf.writeBackupDict()
            return tran_dict

        # if self.is_debugging:
        #     found_text_dict = testFindText()
        # else:
        #     found_text_dict = performActualFindSpecialTerms()

        found_text_dict = performActualFindSpecialTerms()
        temp_list = list(found_text_dict.items())
        sorted_list = sorted(temp_list, key=lambda x: len(x[0]), reverse=True)
        new_found_text_dict = OrderedDict(sorted_list)
        translated_dict = translateTheFoundDict(new_found_text_dict)
        writeSortedDict(translated_dict)
        print('Finished')
        exit(0)

    def run(self):
        # _("Hoang Duy Tran")
        self.extract_bracket_texts_from_gtx()
        # self.find()
        # if self.global_found_list:
        #     word_list = sorted(list(self.global_found_list.values()))
        #     if self.sort_order is SortOrder.ALPHABET_INVERT:
        #         word_list = sorted(word_list, reverse=True)
        #     elif self.sort_order is SortOrder.LENGTH:
        #         word_list = sorted(word_list, key=lambda x: len(x))
        #     elif self.sort_order is SortOrder.LENGTH_INVERT:
        #         word_list = sorted(word_list, key=lambda x: len(x), reverse=True)
        # 
        #     print('WORDLIST:')
        #     pp(self.global_found_list.values())
        #
        #     exit(0)
        # if self.json_dic:
        #     sorted_list = list(sorted(list(self.json_dic.items()), key=lambda x: len(x[0])))
        #     output_dict = OrderedDict(sorted_list)
        #     home_dir = os.environ['HOME']
        #     json_file = os.path.join(home_dir, 'find_text.json')
        #     writeJSON(json_file, output_dict)
            # pp(self.json_dic)

            # tf = TranslationFinder()
            # print('Output global_found_list - only printout if NOT translated:')
            # is_counting = False
            # is_first = True
            #
            # final_dict={}
            # for w in word_list:
            #     if is_first:
            #         print('FIRST')
            #         is_first = False
            #
            #     # trans = tf.isInListByDict(w, True)
            #     # trans = self.tranRef(w, False, tf)
            #     # if not trans:
            #     trans, is_marked, is_ignore = tf.translate(w)
            #     if is_ignore:
            #         print(f'IGNORED: {w}')
            #     if not is_marked:
            #         # print(f'COMPLETED: "{w}": "{trans}",')
            #         continue
            #
            #     if not trans:
            #         trans = ""
            #
            #     w = re.sub(r'"', '', w)
            #     entry = {w: trans}
            #     final_dict.update(entry)
                
                # count=1
                # if w in self.global_count:
                #     count = self.global_count[w]
                # # trans,_,_ = tf.translate(w)
                # if trans:
                #     w = re.sub(r'"', '', w)
                #     # trans = re.sub(r'"', '\\"', trans)
                #     if is_counting:
                #         print(f'"{w}": "{trans}", {count}')
                #     else:
                #         print(f'"{w}": "{trans}",')
                # else:
                #     if is_counting:
                #         print(f'"{w}": "", {count}')
                #     else:
                #         print(f'"{w}": "",')
            # PP(self.global_count)
            # PP(final_list)
        # home = os.environ['HOME']
        # out_file = os.path.join(home, 'log.json')
        # writeJSON(out_file, final_dict)




parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-p", "--pattern", dest="find_pattern", help="Pattern to find.")
parser.add_argument("-BR", "--bracket", dest="bracketed", help="Using brackets instead of pattern, provide a pair of brackets to find, default is '()'", action='store_const', const=True)
parser.add_argument("-BP", "--brk_pair", dest="bracket_pair", help="Bracket pair to find, includes in a group, starting and ending bracket, such as -BP '{}'.")
parser.add_argument("-R", "--replace_pattern", dest="replace_pattern", help="Pattern to replace. Only works with PO files and in msgstr entries. Not currently support INVERT match")

parser.add_argument("-CL", "--case_low", dest="case_lower", help="Replaced find pattern with lowercase version in PO tranlation string", action='store_const', const=True)
parser.add_argument("-CU", "--case_up", dest="case_upper", help="Replaced find pattern with uppercase version in PO tranlation string", action='store_const', const=True)
parser.add_argument("-CC", "--case_cap", dest="case_capital", help="Replaced find pattern with capital first character version in PO tranlation string", action='store_const', const=True)
parser.add_argument("-CT", "--case_title", dest="case_title", help="Replaced find pattern with title case (capitalised first character of each word) version in PO tranlation string", action='store_const', const=True)

parser.add_argument("-o", "--po", dest="find_po", help="Find in $BLENDER_MAN_VI/LC_MESSAGES.", action='store_const', const=True)
parser.add_argument("-r", "--rst", dest="find_rst", help="Find in $BLENDER_MAN_EN/manual.", action='store_const', const=True)
parser.add_argument("-s", "--src", dest="find_src", help="Find in $BLENDER_ae.", action='store_const', const=True)
parser.add_argument("-y", "--py", dest="find_py", help="Find in $LOCAL_PYTHON_3.", action='store_const', const=True)
parser.add_argument("-gtx", "--gettext", dest="find_gettext", help="Find in $LOCAL_PYTHON_3.", action='store_const', const=True)

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
parser.add_argument("-D", "--debug", dest="debugging", help="Print out messages as processing.")
parser.add_argument("-vi", "--vipo", dest="vipo_file", help="Find text in vi.po file, the latest version in $BLENDER_GITHUB", action='store_const', const=True)
parser.add_argument("-py", "--py_lib", dest="find_py_lib", help="Find text in source files, set in $PYTHONPATH", action='store_const', const=True)
parser.add_argument("-S", "--sort_order", dest="sort_order", help="Sort Order: A, AI, L, LI; This option only APPLIES to the global_found_list which is printed out at the end of the run. Noted that this global_found_list is a dictionary and only hold a SINGLE instance of found texts.")
parser.add_argument("-m", "--marking", dest="marking", help="Marking the matched parts in string for easier spotting while observing.", action='store_const', const=True)
parser.add_argument("-json", "--json", dest="output_json", help="Dumps all found instances as a dictionary, non-repeat, JSON format.", action='store_const', const=True)


args = parser.parse_args()

x = FindFilesHasPattern()
x.setVars(
    args.find_pattern,
    # '\*([^\*]+)\*', # star quotes
    # '"([^"]+)"', # double quotes
    # "'(?!(s|re|ll|t)?\s)([^']+)'(?!\S)", # single quote
    # "\(([^()]+)\)", # bracket     # ':kbd:`Shift-LMB` drag',
    args.bracketed,
    args.bracket_pair,
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
    args.find_gettext,
    args.find_py_lib,
    args.find_src,
    args.case_sensitive,
    args.before_lines,
    args.after_lines,
    args.only_match,
    args.show_line_number,
    args.invert_match,
    args.testing_only,
    args.debugging,
    args.sort_order,
    args.marking,
    args.output_json,
    )

x.run()
