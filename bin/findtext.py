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
from ignore import Ignore as ig
import json


INVERT_SEP='•'
# DEBUG = True
DEBUG = False
TESTING = False
# TESTING = True

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
        DEBUG = (True if debugging else False)

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
        is_debug = ('ray' in msg)
        if is_debug:
            _('DEBUG')

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

    def translate_word_into_dict(self, k:str, dict_tf: TranslationFinder, dict_to_insert:OrderedDict, is_translating_ref=False):
        if is_translating_ref:
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
        print(f'translated entry:{entry}')
        dict_to_insert.update(entry)

    def extract_bracket_texts_from_gtx(self):
        find_pat_list = [
            # re.compile(r'[\(]+(.*?)[\)]+'), # ARCH_BRAKET_MULTI
            # re.compile(r"(?<!\w)\'([^\']+)(?:\b)\'"), # single quote
            # re.compile(r"(?<!\w)\*([^\*]+)(?:\b)\*"), # asterisk
            # re.compile(r'"(?<!\\")(.*?)"'),         # double quote
            # re.compile(r'[\`]*(:[^\:]+:)?[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]?'),

            (cm.AST_QUOTE, RefType.AST_QUOTE),
            (cm.DBL_QUOTE, RefType.DBL_QUOTE),
            (cm.SNG_QUOTE, RefType.SNG_QUOTE),
            (cm.GA_REF, RefType.GA),
            (cm.RGBA, RefType.TEXT),
            (re.compile(r''), RefType.ARCH_BRACKET),
        ]

        def testFindText():
            # data = '''
            # like ''textures'' for instance
            # hold :kbd:`NumpadPlus` or :kbd:`Ctrl-MMB` or similar
            # see :doc:`Normals'
            # see :ref:`temp-dir` for details
            # this bracketed line  (will 'cause' some *translation* to be "done internally" or :kbd:`Ctrl-MMB` :menuselection:`View --> Show Curve Extremes` here).
            # this is the same thing as the *Playback Range* option of the :ref:`Timeline editor header <animation-editors-timeline-headercontrols>`
            # and optionally *Topology Mirror* if your mesh is not symmetric
            # visible if :menuselection:`View --> Show Curve Extremes` are enabled
            # which remains in *Pose Mode*
            # which you might call "sun", what do you think?
            # ``INSERT(ATTRIB+XDATA)``
            # with components like "L", "R", "right", "left"
            # with holding :kbd:`Alt`'
            # '''
            # data = "With the \"traditional\" representation of three bytes, like RGB(124, 255, 56), the multiplications give far too high results, like RGB(7316, 46410, 1848), that have to be normalized (brought back) by dividing them by 256 to fit in the range of (0 to 255)..."
            # # data = "(will 'cause' some *translation* to be \"done internally\" or :kbd:`Ctrl-MMB` :menuselection:`View --> Show Curve Extremes` here)"
            # data = "see the :doc:`Particle Physics </physics/particles/emitter/physics/index>` page"
            data = "Similar to regular *Established Ocean* however, waves will continue to grow with time creating sharper peaks (:abbr:`JONSWAP (JOint North Sea WAve Project)` and Pierson-Moskowitz method). An extra parameter is used to define the sharpness of these peaks."
            data = ":menuselection:`Sidebar region --> Cursor`."
            data = "``(LW)POLYLINE``, ``(LW)POLYGON`` as ``POLYLINE`` curve if they have no bulges else as ``BEZIER`` curve."
            data = "Index of the pose to apply (-2 for no change, -1 to use the active pose)."
            data = "Refers to the general color decomposition resulting in *Y* (Luminance) and *C* (Chrominance) channels, whereas the chrominance is represented by: U = ( Blue minus Luminance ) and V = ( Red minus Luminance )."
            # data = "like 'textures' for instance"
            data = "``//render_`` becomes ``//render_####``, writing frames as ``//render_0001.png``"
            data = "Refers to the general color decomposition resulting in *Y* (Luminance) and *C* (Chrominance) channels, whereas the chrominance is represented by: U = ( Blue minus Luminance ) and V = ( Red minus Luminance )."
            data = "Constraints are a way to control an object's properties (e.g. its location, rotation, scale), using either plain static values (like the :doc:`\"limit\" ones </animation/constraints/transform/limit_location>`), or another object, called \"target\" (like e.g. the :doc:`\"copy\" ones </animation/constraints/transform/copy_location>`)."
            data = '''
:abbr:`API (Application Programming Interface)`
:abbr:`BSDF (Bidirectional Scattering Distribution Function)`
:abbr:`BSDF (Bidirectional scattering distribution function)`
:abbr:`BSSRDF (Bidirectional subsurface scattering distribution function)`
:abbr:`CAD (Computer-Aided Design)`
:abbr:`CGI (Computer-Generated Imagery)`
:abbr:`CPU (Central Processing Unit)`
:abbr:`CUDA (Compute Unified Device Architecture)`
:abbr:`DLS (Damped Least Square)`
:abbr:`DTP (DeskTop Publishing)`
:abbr:`DoF (Depth of Field)`
:abbr:`FOV (Field of View)`
:abbr:`FPS (Frames Per Second)`
:abbr:`GCN (Graphics Core Next)`
:abbr:`GPU (Graphic Processing Unit, also known as Graphics Card)`
:abbr:`GPU (Graphics Processing Unit)`
:abbr:`GTAO (Ground Truth Ambient Occlusion)`
:abbr:`HDMI (High Definition Media Interface)`
:abbr:`HDR (High Dynamic Range)`
:abbr:`HMDs (Head-Mounted Displays)`
:abbr:`IES (Illuminating Engineering Society of North America)`
:abbr:`IES (Illuminating Engineering Society)`
:abbr:`IO (Input/Output)`
:abbr:`IPO (InterPOlated)`
:abbr:`JONSWAP (JOint North Sea WAve Project)`
:abbr:`LDR (Low Dynamic Range)`
:abbr:`NDOF (N-Degrees of Freedom)`
:abbr:`OSA (Oversampling)`
:abbr:`OpenCL (Open Computing Language)`
:abbr:`PBR (Physically Based Rendering)`
:abbr:`POV (Point Of View)`
:abbr:`RGB (Red, Green, Blue)`
:abbr:`RNG (Random Number Generator)`
:abbr:`SAE (Society of Automobile Engineers)`
:abbr:`SDLS (Selective Damped Least Square)`
:abbr:`SSAO (Screen Space Ambient Occlusion)`
:abbr:`SSR (Screen Space Reflection)`
:abbr:`TL;DR (Too long; didn't read.)`
:abbr:`UI (User Interface)`
:abbr:`VR (Virtual Reality)`
:abbr:`VSE (Video Sequence Editor)`
:abbr:`WDAS (Walt Disney Animation Studios)`
:abbr:`enum (enumeration)`
:class:`blender_api:bpy.types.KeyMapItem`
:class:`blender_api:bpy.types.KeyMapItems.new`
:class:`blender_api:bpy.types.KeyMap`
:class:`blender_api:bpy.types.KeyMaps.new`
:class:`blender_api:bpy.types.Menu`
:class:`blender_api:bpy.types.Operator`
:class:`blender_api:mathutils.Vector`
:doc:`/about/contribute/build/index`
:doc:`/about/contribute/guides/markup_guide`
:doc:`/about/contribute/guides/writing_guide`
:doc:`/about/contribute/install/index`
:doc:`/about/contribute/translations/add_language`
:doc:`/addons/development/is_key_free`
:doc:`/addons/index`
:doc:`/addons/interface/brush_menus`
:doc:`/addons/lighting/sun_position`
:doc:`/advanced/blender_directory_layout`
:doc:`/advanced/index`
:doc:`/advanced/scripting/index`
:doc:`/animation/actions`
:doc:`/animation/armatures/bones/properties/bendy_bones`
:doc:`/animation/armatures/properties/bone_groups`
:doc:`/animation/armatures/properties/display`
:doc:`/animation/constraints/index`
:doc:`/animation/constraints/relationship/follow_path`
:doc:`/animation/constraints/transform/copy_location`
:doc:`/animation/drivers/drivers_panel`
:doc:`/animation/index`
:doc:`/animation/keyframes/keying_sets`
:doc:`/animation/markers`
:doc:`/animation/shape_keys/shape_keys_panel`
:doc:`/compositing/index`
:doc:`/compositing/types/color/index`
:doc:`/compositing/types/distort/plane_track_deform`
:doc:`/compositing/types/input/rgb`
:doc:`/copyright`
:doc:`/editors/dope_sheet/action`
:doc:`/editors/file_browser`
:doc:`/editors/graph_editor/channels`
:doc:`/editors/image/editing`
:doc:`/editors/image/image_settings`
:doc:`/editors/image/navigating`
:doc:`/editors/index`
:doc:`/editors/uv/navigating`
:doc:`/files/blend/open_save`
:doc:`/files/data_blocks`
:doc:`/files/index`
:doc:`/files/linked_libraries/index`
:doc:`/files/media/image_formats`
:doc:`/getting_started/about/index`
:doc:`/getting_started/configuration/defaults`
:doc:`/getting_started/configuration/index`
:doc:`/getting_started/help`
:doc:`/getting_started/installing/index`
:doc:`/grease_pencil/index`
:doc:`/interface/annotate_tool`
:doc:`/interface/controls/nodes/introduction`
:doc:`/interface/controls/templates/color_picker`
:doc:`/interface/controls/templates/data_block`
:doc:`/interface/controls/templates/operator_search`
:doc:`/interface/index`
:doc:`/interface/keymap/introduction`
:doc:`/interface/undo_redo`
:doc:`/interface/window_system/areas`
:doc:`/modeling/curves/curve_display`
:doc:`/modeling/index`
:doc:`/modeling/meshes/editing/face/extrude_faces`
:doc:`/modeling/meshes/editing/mesh/transform/skin_resize`
:doc:`/modeling/meshes/editing/vertex/connect_vertex_path`
:doc:`/modeling/meshes/properties/custom_data`
:doc:`/modeling/meshes/tools/extrude_manifold`
:doc:`/modeling/meshes/tools/spin`
:doc:`/modeling/meshes/uv/unwrapping/seams`
:doc:`/modeling/meshes/uv/workflows/layout`
:doc:`/modeling/meshes/uv/workflows/udims`
:doc:`/modeling/modifiers/deform/curve`
:doc:`/modeling/modifiers/deform/lattice`
:doc:`/modeling/modifiers/generate/array`
:doc:`/modeling/modifiers/generate/booleans`
:doc:`/modeling/modifiers/generate/multiresolution`
:doc:`/modeling/modifiers/generate/skin`
:doc:`/modeling/modifiers/generate/triangulate`
:doc:`/modeling/modifiers/generate/wireframe`
:doc:`/modeling/modifiers/modify/normal_edit`
:doc:`/modeling/modifiers/modify/weighted_normal`
:doc:`/movie_clip/index`
:doc:`/movie_clip/masking/index`
:doc:`/movie_clip/tracking/clip/properties/stabilization/index`
:doc:`/physics/cloth/settings/physical_properties`
:doc:`/physics/fluid/type/effector`
:doc:`/physics/fluid/type/flow`
:doc:`/physics/index`
:doc:`/physics/particles/emitter/display`
:doc:`/physics/rigid_body/properties/dynamics`
:doc:`/render/cameras`
:doc:`/render/cycles/material_settings`
:doc:`/render/eevee/materials/nodes_support`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/alpha/along_stroke`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/alpha/crease_angle`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/alpha/curvature_3d`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/alpha/distance_from_camera`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/alpha/distance_from_object`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/alpha/material`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/alpha/noise`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/alpha/tangent`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/color/along_stroke`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/color/crease_angle`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/color/curvature_3d`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/color/distance_from_camera`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/color/distance_from_object`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/color/material`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/color/noise`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/color/tangent`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/2d_offset`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/2d_transform`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/backbone_stretcher`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/bezier_curve`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/blueprint`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/guiding_lines`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/perlin_noise_1d`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/perlin_noise_2d`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/polygonization`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/sampling`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/simplification`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/sinus_displacement`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/spatial_noise`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/geometry/tip_remover`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/thickness/along_stroke`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/thickness/calligraphy`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/thickness/crease_angle`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/thickness/curvature_3d`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/thickness/distance_from_camera`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/thickness/distance_from_object`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/thickness/material`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/thickness/noise`
:doc:`/render/freestyle/parameter_editor/line_style/modifiers/thickness/tangent`
:doc:`/render/index`
:doc:`/render/output/metadata`
:doc:`/render/shader_nodes/converter/math`
:doc:`/render/shader_nodes/converter/rgb_to_bw`
:doc:`/render/shader_nodes/converter/shader_to_rgb`
:doc:`/render/shader_nodes/input/attribute`
:doc:`/render/shader_nodes/input/texture_coordinate`
:doc:`/render/shader_nodes/shader/glossy`
:doc:`/render/shader_nodes/shader/hair_principled`
:doc:`/render/shader_nodes/shader/hair`
:doc:`/render/shader_nodes/vector/mapping`
:doc:`/render/workbench/options`
:doc:`/scene_layout/index`
:doc:`/scene_layout/object/editing/transform/control/axis_locking`
:doc:`/scene_layout/object/editing/transform/move`
:doc:`/scene_layout/object/editing/transform/rotate`
:doc:`/scene_layout/object/editing/transform/scale`
:doc:`/scene_layout/object/properties/display`
:doc:`/sculpt_paint/index`
:doc:`/sculpt_paint/sculpting/tool_settings/dyntopo`
:doc:`/sculpt_paint/sculpting/tools/blob`
:doc:`/sculpt_paint/sculpting/tools/boundary`
:doc:`/sculpt_paint/sculpting/tools/box_trim`
:doc:`/sculpt_paint/sculpting/tools/clay_strips`
:doc:`/sculpt_paint/sculpting/tools/clay`
:doc:`/sculpt_paint/sculpting/tools/cloth_filter`
:doc:`/sculpt_paint/sculpting/tools/cloth`
:doc:`/sculpt_paint/sculpting/tools/crease`
:doc:`/sculpt_paint/sculpting/tools/draw_sharp`
:doc:`/sculpt_paint/sculpting/tools/draw`
:doc:`/sculpt_paint/sculpting/tools/edit_face_set`
:doc:`/sculpt_paint/sculpting/tools/elastic_deform`
:doc:`/sculpt_paint/sculpting/tools/fill`
:doc:`/sculpt_paint/sculpting/tools/flatten`
:doc:`/sculpt_paint/sculpting/tools/grab`
:doc:`/sculpt_paint/sculpting/tools/inflate`
:doc:`/sculpt_paint/sculpting/tools/lasso_trim`
:doc:`/sculpt_paint/sculpting/tools/layer`
:doc:`/sculpt_paint/sculpting/tools/line_project`
:doc:`/sculpt_paint/sculpting/tools/mask`
:doc:`/sculpt_paint/sculpting/tools/mesh_filter`
:doc:`/sculpt_paint/sculpting/tools/multiplane_scrape`
:doc:`/sculpt_paint/sculpting/tools/nudge`
:doc:`/sculpt_paint/sculpting/tools/pinch`
:doc:`/sculpt_paint/sculpting/tools/pose`
:doc:`/sculpt_paint/sculpting/tools/rotate`
:doc:`/sculpt_paint/sculpting/tools/scrape`
:doc:`/sculpt_paint/sculpting/tools/simplify`
:doc:`/sculpt_paint/sculpting/tools/slide_relax`
:doc:`/sculpt_paint/sculpting/tools/smooth`
:doc:`/sculpt_paint/sculpting/tools/snake_hook`
:doc:`/sculpt_paint/sculpting/tools/thumb`
:doc:`/sculpt_paint/texture_paint/index`
:doc:`/sculpt_paint/weight_paint/tool_settings/options`
:doc:`/troubleshooting/index`
:doc:`/troubleshooting/recover`
:doc:`/video_editing/index`
:doc:`2D Layers </grease_pencil/properties/layers>`
:doc:`2D Stabilization </movie_clip/tracking/clip/properties/stabilization/index>`
:doc:`3D Cursor </editors/3dview/3d_cursor>`
:doc:`3D Painting </sculpt_paint/texture_paint/index>`
:doc:`3D Viewport </editors/3dview/index>`
:doc:`3D Viewport Alignment </editors/3dview/navigate/align>`
:doc:`3D Viewport Camera Navigation </editors/3dview/navigate/camera_view>`
:doc:`3D Viewport clipping </editors/3dview/sidebar>`
:doc:`3D cursor </editors/3dview/3d_cursor>`
:doc:`AOV Output </render/shader_nodes/output/aov>`
:doc:`Action </animation/actions>`
:doc:`Action </editors/dope_sheet/action>`
:doc:`Action Editor </editors/dope_sheet/action>`
:doc:`Actions </animation/actions>`
:doc:`Active Spline </modeling/curves/properties/active_spline>`
:doc:`Adaptive Subdivision </render/cycles/object_settings/adaptive_subdiv>`
:doc:`Add-on Directory </advanced/blender_directory_layout>`
:doc:`Add-ons </editors/preferences/addons>`
:doc:`Adjustment Layer </video_editing/sequencer/strips/adjustment>`
:doc:`Advanced Transformations </scene_layout/object/editing/transform/index>`
:doc:`Airbrush Stroke Method </sculpt_paint/brush/stroke>`
:doc:`Alembic </files/import_export/alembic>`
:doc:`Alembic Importer </files/import_export/alembic>`
:doc:`Align </editors/3dview/navigate/align>`
:doc:`Alpha Over </video_editing/sequencer/strips/effects/alpha_over_under_overdrop>`
:doc:`Ambient Occlusion </render/shader_nodes/input/ao>`
:doc:`Animation & Rigging </animation/index>`
:doc:`Animation & Rigging </animation/introduction>`
:doc:`Animation </animation/index>`
:doc:`Animation </grease_pencil/animation/tools>`
:doc:`Animation </render/output/animation>`
:doc:`Animation tools </grease_pencil/animation/tools>`
:doc:`Annotate Tool </interface/annotate_tool>`
:doc:`Annotations </interface/annotate_tool>`
:doc:`Appending and Linking </files/linked_libraries/index>`
:doc:`Applying Images to UVs </modeling/meshes/uv/applying_image>`
:doc:`Areas </interface/window_system/areas>`
:doc:`Armature </animation/armatures/index>`
:doc:`Armature </animation/armatures/introduction>`
:doc:`Armature </animation/armatures/properties/index>`
:doc:`Armature </modeling/modifiers/deform/armature>`
:doc:`Armature Deform </animation/armatures/skinning/parenting>`
:doc:`Armature Modifier </modeling/modifiers/deform/armature>`
:doc:`Armature Posing section </animation/armatures/posing/bone_constraints/inverse_kinematics/spline_ik>`
:doc:`Armature chapter </animation/armatures/posing/bone_constraints/index>`
:doc:`Armature modifier </modeling/modifiers/deform/armature>`
:doc:`Audio Waveforms </video_editing/sequencer/strips/sound>`
:doc:`Auto Save </troubleshooting/recover>`
:doc:`Auto Smooth </modeling/meshes/structure>`
:doc:`Auto run </advanced/scripting/security>`
:doc:`Axis Locking </scene_layout/object/editing/transform/control/axis_locking>`
:doc:`Background </render/shader_nodes/shader/background>`
:doc:`Bake the Cache </physics/fluid/type/domain/cache>`
:doc:`Basic Transformations </scene_layout/object/editing/transform/introduction>`
:doc:`Bendy Bones </animation/armatures/bones/properties/bendy_bones>`
:doc:`Bevel </modeling/modifiers/generate/bevel>`
:doc:`Bevel Edges </modeling/meshes/editing/edge/bevel>`
:doc:`Bevel Modifier </modeling/modifiers/generate/bevel>`
:doc:`Bevel Operation </modeling/meshes/editing/edge/bevel>`
:doc:`Blend-files Previews </files/blend/previews>`
:doc:`Blur node </compositing/types/filter/blur_node>`
:doc:`Boids </physics/particles/emitter/physics/boids>`
:doc:`Boids Particles </physics/particles/emitter/physics/boids>`
:doc:`Bokeh Blur </compositing/types/filter/bokeh_blur>`
:doc:`Bokeh Image </compositing/types/input/bokeh_image>`
:doc:`Bone </animation/armatures/bones/index>`
:doc:`Bone </animation/armatures/bones/properties/index>`
:doc:`Bone Constraints </animation/armatures/posing/bone_constraints/index>`
:doc:`Bone Edit Mode </animation/armatures/bones/selecting>`
:doc:`Bone Groups </animation/armatures/properties/bone_groups>`
:doc:`Bone Structure </animation/armatures/bones/structure>`
:doc:`Boolean Modifier </modeling/modifiers/generate/booleans>`
:doc:`Box Mask </compositing/types/matte/box_mask>`
:doc:`Brush </grease_pencil/modes/sculpting/tool_settings/brush>`
:doc:`Brush </grease_pencil/modes/weight_paint/tool_settings/brush>`
:doc:`Brush </physics/dynamic_paint/brush>`
:doc:`Brush </sculpt_paint/brush/brush>`
:doc:`Brush Falloff </sculpt_paint/brush/falloff>`
:doc:`Brush Settings </sculpt_paint/sculpting/tool_settings/brush_settings>`
:doc:`Building </about/contribute/build/linux>`
:doc:`Building </about/contribute/build/macos>`
:doc:`Building </about/contribute/build/windows>`
:doc:`Cache </video_editing/sequencer/properties/proxy_cache>`
:doc:`Cache File </modeling/modifiers/modify/mesh_sequence_cache>`
:doc:`Camera </render/cameras>`
:doc:`Camera Settings </render/cameras>`
:doc:`Camera View </editors/3dview/navigate/camera_view>`
:doc:`Camera settings </render/cameras>`
:doc:`Canvas </physics/dynamic_paint/canvas>`
:doc:`Child Of constraint </animation/constraints/relationship/child_of>`
:doc:`Children </physics/particles/emitter/children>`
:doc:`Clamp To </animation/constraints/tracking/clamp_to>`
:doc:`Clamp To Constraint </animation/constraints/tracking/clamp_to>`
:doc:`Clear Origin </scene_layout/object/editing/clear>`
:doc:`Cloth </physics/cloth/index>`
:doc:`Cloth Brush </sculpt_paint/sculpting/tools/cloth>`
:doc:`Cloth Simulation </physics/cloth/index>`
:doc:`Cloth Solver </physics/cloth/index>`
:doc:`Cloth objects </physics/cloth/index>`
:doc:`Collection </scene_layout/collections/collections>`
:doc:`Collection </scene_layout/collections/index>`
:doc:`Collection </scene_layout/collections/introduction>`
:doc:`Collection Instance </scene_layout/object/properties/instancing/collection>`
:doc:`Collection Instancing </scene_layout/object/properties/instancing/collection>`
:doc:`Collections </scene_layout/collections/collections>`
:doc:`Collections </scene_layout/collections/index>`
:doc:`Collision Physics </physics/collision>`
:doc:`Collision panel </physics/collision>`
:doc:`Collisions </physics/soft_body/collision>`
:doc:`Color Balance Node </compositing/types/color/color_balance>`
:doc:`Color Generator </video_editing/sequencer/strips/color>`
:doc:`Color Key </compositing/types/matte/color_key>`
:doc:`Color Management and Exposure </render/color_management>`
:doc:`Color Nodes </render/shader_nodes/color/index>`
:doc:`Color Ramp </compositing/types/converter/color_ramp>`
:doc:`Color Spill Node </compositing/types/matte/color_spill>`
:doc:`Color picker </interface/controls/templates/color_picker>`
:doc:`Color ramps </interface/controls/templates/color_ramp>`
:doc:`Command Line </advanced/command_line/arguments>`
:doc:`Command Line Arguments </advanced/command_line/arguments>`
:doc:`Command Line Window </advanced/command_line/introduction>`
:doc:`Composite Node </compositing/types/output/composite>`
:doc:`Compositing </compositing/index>`
:doc:`Compositing </compositing/introduction>`
:doc:`Compositing Nodes </compositing/index>`
:doc:`Compositor </compositing/index>`
:doc:`Compositor </compositing/introduction>`
:doc:`Compositor </compositing/types/input/image>`
:doc:`Configuring Hardware </getting_started/configuration/hardware>`
:doc:`Console window </advanced/command_line/introduction>`
:doc:`Converter Nodes </render/shader_nodes/converter/index>`
:doc:`Copy Scale </animation/constraints/transform/copy_scale>`
:doc:`Copy Transforms </animation/constraints/transform/copy_transforms>`
:doc:`Corner Pin </compositing/types/distort/corner_pin>`
:doc:`Cryptomatte Node </compositing/types/matte/cryptomatte>`
:doc:`Cursor </sculpt_paint/brush/cursor>`
:doc:`Curve </modeling/curves/introduction>`
:doc:`Curve </modeling/curves/properties/index>`
:doc:`Curve Deform </modeling/modifiers/deform/curve>`
:doc:`Curve Edit Mode </modeling/curves/selecting>`
:doc:`Curve Editing </modeling/curves/editing/index>`
:doc:`Curve Editing </modeling/curves/properties/geometry>`
:doc:`Curve Modifier </modeling/modifiers/deform/curve>`
:doc:`Curve Object </modeling/curves/index>`
:doc:`Curve modifier </modeling/modifiers/deform/curve>`
:doc:`Curves </modeling/curves/index>`
:doc:`Curves </modeling/curves/properties/geometry>`
:doc:`Curves </modeling/curves/properties/shape>`
:doc:`Curves Node </compositing/types/color/hue_correct>`
:doc:`Curves Node </compositing/types/color/rgb_curves>`
:doc:`Curves Primitives </modeling/curves/primitives>`
:doc:`Custom Limit </render/eevee/lighting>`
:doc:`Cycles </render/cameras>`
:doc:`Cycles </render/cycles/gpu_rendering>`
:doc:`Cycles </render/cycles/index>`
:doc:`Cycles </render/cycles/render_settings/index>`
:doc:`Cycles </render/materials/index>`
:doc:`Cycles Debug </editors/preferences/experimental>`
:doc:`Cycles Render Baking </render/cycles/baking>`
:doc:`Cycles render passes </render/layers/passes>`
:doc:`Cycles specific settings </render/cycles/light_settings>`
:doc:`Cycles specific settings </render/cycles/material_settings>`
:doc:`Damped Track </animation/constraints/tracking/damped_track>`
:doc:`Damped Track Constraint </animation/constraints/tracking/damped_track>`
:doc:`Damped Track constraint </animation/constraints/tracking/damped_track>`
:doc:`Data System </files/introduction>`
:doc:`Data System chapter </files/data_blocks>`
:doc:`Data Transfer </scene_layout/object/editing/relations/transfer_mesh_data>`
:doc:`Data Transfer Modifier </modeling/modifiers/modify/data_transfer>`
:doc:`Data-blocks </files/data_blocks>`
:doc:`Debug Panel </render/cycles/render_settings/debug>`
:doc:`Decimate Modifier </modeling/modifiers/generate/decimate>`
:doc:`Deform </animation/armatures/bones/properties/deform>`
:doc:`Deform Modifier </modeling/modifiers/deform/mesh_deform>`
:doc:`Denoising </render/layers/denoising>`
:doc:`Denoising node </compositing/types/filter/denoise>`
:doc:`Depth Order </grease_pencil/properties/strokes>`
:doc:`Dilate Node </compositing/types/filter/dilate_erode>`
:doc:`Dilate/Erode Node </compositing/types/filter/dilate_erode>`
:doc:`Disk Cache </physics/particles/emitter/cache>`
:doc:`Displace </modeling/modifiers/deform/displace>`
:doc:`Displace Modifier </modeling/modifiers/deform/displace>`
:doc:`Displacement </render/materials/components/displacement>`
:doc:`Displacement </render/shader_nodes/vector/displacement>`
:doc:`Display panel page </animation/armatures/properties/display>`
:doc:`Domain </physics/fluid/type/domain/index>`
:doc:`Domain object </physics/fluid/type/domain/index>`
:doc:`Dope Sheet </editors/dope_sheet/grease_pencil>`
:doc:`Dope Sheet </editors/dope_sheet/index>`
:doc:`Dope Sheet </editors/dope_sheet/introduction>`
:doc:`Double Edge Mask </compositing/types/matte/double_edge_mask>`
:doc:`Downloading Blender </getting_started/installing/index>`
:doc:`Draw Brush </grease_pencil/modes/draw/tool_settings/brushes/draw_brush>`
:doc:`Draw Mode </grease_pencil/modes/draw/index>`
:doc:`Draw Mode </grease_pencil/modes/draw/introduction>`
:doc:`Draw Tool </grease_pencil/modes/draw/tool_settings/draw>`
:doc:`Draw tool </grease_pencil/modes/draw/tools>`
:doc:`Drawing Plane </grease_pencil/modes/draw/drawing_planes>`
:doc:`Drawing Planes </grease_pencil/modes/draw/drawing_planes>`
:doc:`Drivers </animation/drivers/index>`
:doc:`Drivers Editor </editors/drivers_editor>`
:doc:`Drivers editor </editors/drivers_editor>`
:doc:`Drivers panel </animation/drivers/drivers_panel>`
:doc:`Dynamic Context Menu </addons/interface/context_menu>`
:doc:`Dyntopo panel </sculpt_paint/sculpting/tool_settings/dyntopo>`
:doc:`Edge Split </modeling/modifiers/generate/edge_split>`
:doc:`Edge Split Modifier </modeling/modifiers/generate/edge_split>`
:doc:`Edit Mode </animation/armatures/bones/selecting>`
:doc:`Edit Mode </grease_pencil/modes/edit/introduction>`
:doc:`Edit Mode </modeling/index>`
:doc:`Edit Mode </modeling/meshes/properties/vertex_groups/assigning_vertex_group>`
:doc:`Edit Mode </modeling/meshes/selecting/index>`
:doc:`Editing </about/contribute/editing>`
:doc:`Editing Normals </modeling/meshes/editing/mesh/normals>`
:doc:`Editing Preferences </editors/preferences/editing>`
:doc:`Editing UVs </modeling/meshes/uv/editing>`
:doc:`Editing tools </grease_pencil/modes/edit/tools>`
:doc:`Editors </editors/index>`
:doc:`Eevee </render/eevee/index>`
:doc:`Eevee </render/eevee/limitations>`
:doc:`Eevee specific settings </render/eevee/lighting>`
:doc:`Eevee specific settings </render/eevee/materials/settings>`
:doc:`Effector </physics/fluid/type/effector>`
:doc:`Ellipse Mask </compositing/types/matte/ellipse_mask>`
:doc:`Emission </render/shader_nodes/shader/emission>`
:doc:`Emission panel </physics/particles/emitter/emission>`
:doc:`Emission shader </render/shader_nodes/shader/emission>`
:doc:`Empty </modeling/empties>`
:doc:`Erase Brush </grease_pencil/modes/draw/tool_settings/brushes/erase_brush>`
:doc:`Erase Tool </grease_pencil/modes/draw/tool_settings/erase>`
:doc:`External </sculpt_paint/texture_paint/tool_settings/options>`
:doc:`Extrude Along Normals </modeling/meshes/editing/face/extrude_faces_normal>`
:doc:`Extrude Manifold </modeling/meshes/tools/extrude_manifold>`
:doc:`F-Curve </editors/graph_editor/fcurves/index>`
:doc:`F-Curve </editors/graph_editor/fcurves/introduction>`
:doc:`F-Curve </editors/graph_editor/fcurves/properties>`
:doc:`F-Curve Modifiers </editors/graph_editor/fcurves/modifiers>`
:doc:`F-Curves </editors/graph_editor/fcurves/index>`
:doc:`F-Curves </editors/graph_editor/fcurves/introduction>`
:doc:`F-Curves </editors/graph_editor/introduction>`
:doc:`FBX </addons/import_export/scene_fbx>`
:doc:`FBX Importer </addons/import_export/scene_fbx>`
:doc:`Face Set </sculpt_paint/sculpting/editing/face_sets>`
:doc:`Falloff </sculpt_paint/brush/falloff>`
:doc:`Field Weights panel </physics/particles/emitter/force_field>`
:doc:`File </editors/preferences/file_paths>`
:doc:`File Browser </editors/file_browser>`
:doc:`File Preferences </editors/preferences/file_paths>`
:doc:`Fill Brush </grease_pencil/modes/draw/tool_settings/brushes/fill_brush>`
:doc:`Fill tool </grease_pencil/modes/draw/tool_settings/fill>`
:doc:`Flow </physics/fluid/type/flow>`
:doc:`Fluid Domain </physics/fluid/type/domain/index>`
:doc:`Fluid Flow </physics/forces/force_fields/types/fluid_flow>`
:doc:`Fluid Simulator </physics/fluid/index>`
:doc:`Fluid simulation </physics/fluid/index>`
:doc:`Follow Path </animation/constraints/relationship/follow_path>`
:doc:`Follow Path Constraint </animation/constraints/relationship/follow_path>`
:doc:`Follow Path constraint </animation/constraints/relationship/follow_path>`
:doc:`Font </modeling/texts/introduction>`
:doc:`Force Field </physics/forces/force_fields/index>`
:doc:`Force Field Page </physics/forces/force_fields/index>`
:doc:`Force Fields </physics/forces/force_fields/index>`
:doc:`Freestyle </render/freestyle/index>`
:doc:`Freestyle rendering </render/freestyle/introduction>`
:doc:`GPU Rendering </render/cycles/gpu_rendering>`
:doc:`GPU accelerated rendering </render/cycles/gpu_rendering>`
:doc:`GPU rendering </render/cycles/gpu_rendering>`
:doc:`General Baking </physics/baking>`
:doc:`General Settings </render/lights/light_object>`
:doc:`Glossary </glossary/index>`
:doc:`Grab </modeling/meshes/uv/tools/grab>`
:doc:`Grab </sculpt_paint/sculpting/tools/grab>`
:doc:`Grab </sculpt_paint/sculpting/tools/smooth>`
:doc:`Graph Editor </editors/graph_editor/index>`
:doc:`Graph Editor </editors/graph_editor/introduction>`
:doc:`Graph Editor chapter </editors/graph_editor/fcurves/index>`
:doc:`Grease Pencil </editors/dope_sheet/grease_pencil>`
:doc:`Grease Pencil </grease_pencil/index>`
:doc:`Grease Pencil </grease_pencil/introduction>`
:doc:`Grease Pencil </grease_pencil/primitives>`
:doc:`Grease Pencil </grease_pencil/properties/index>`
:doc:`Grease Pencil Edit Mode </grease_pencil/selecting>`
:doc:`Grease Pencil Lines </grease_pencil/index>`
:doc:`Grease Pencil Menu </grease_pencil/modes/edit/grease_pencil_menu>`
:doc:`Grease Pencil Modifiers </grease_pencil/modifiers/index>`
:doc:`Grease Pencil material </grease_pencil/materials/introduction>`
:doc:`Grease Pencil object </grease_pencil/index>`
:doc:`Grease Pencil object's </grease_pencil/index>`
:doc:`Guides </grease_pencil/modes/draw/guides>`
:doc:`Hair </physics/particles/hair/index>`
:doc:`Hair Shape </physics/particles/hair/shape>`
:doc:`Hair curves </physics/particles/hair/shape>`
:doc:`Here </render/materials/legacy_textures/types/blend>`
:doc:`Here </render/materials/legacy_textures/types/clouds>`
:doc:`Here </render/materials/legacy_textures/types/distorted_noise>`
:doc:`Here </render/materials/legacy_textures/types/magic>`
:doc:`Here </render/materials/legacy_textures/types/marble>`
:doc:`Here </render/materials/legacy_textures/types/musgrave>`
:doc:`Here </render/materials/legacy_textures/types/noise>`
:doc:`Here </render/materials/legacy_textures/types/stucci>`
:doc:`Here </render/materials/legacy_textures/types/voronoi>`
:doc:`Here </render/materials/legacy_textures/types/wood>`
:doc:`Hinge's </physics/rigid_body/constraints/types/hinge>`
:doc:`Hook Modifier </modeling/modifiers/deform/hooks>`
:doc:`Hooks </modeling/modifiers/deform/hooks>`
:doc:`ID Mask Node </compositing/types/converter/id_mask>`
:doc:`ID mask </compositing/types/converter/id_mask>`
:doc:`ID masked </compositing/types/converter/id_mask>`
:doc:`IK Solver </animation/constraints/tracking/ik_solver>`
:doc:`IK Solver constraint </animation/constraints/tracking/ik_solver>`
:doc:`IK solver </animation/armatures/posing/bone_constraints/inverse_kinematics/introduction>`
:doc:`Image </editors/image/introduction>`
:doc:`Image </render/shader_nodes/textures/image>`
:doc:`Image Editor </editors/image/introduction>`
:doc:`Image Input node </compositing/types/input/image>`
:doc:`Image Strip </video_editing/sequencer/strips/movie_image>`
:doc:`Image Strips </video_editing/sequencer/strips/movie_image>`
:doc:`Image Texture node </render/shader_nodes/textures/image>`
:doc:`Image Textures </render/materials/legacy_textures/types/image_movie>`
:doc:`Image node </compositing/types/input/render_layers>`
:doc:`Import/Export </files/import_export>`
:doc:`Indirect Lighting </render/eevee/render_settings/indirect_lighting>`
:doc:`Inflate </sculpt_paint/sculpting/tools/inflate>`
:doc:`Info Editor </editors/info_editor>`
:doc:`Input Device </getting_started/configuration/hardware>`
:doc:`Input Preference </editors/preferences/input>`
:doc:`Input Preferences </editors/preferences/input>`
:doc:`Instancing Vertex emitter </scene_layout/object/properties/instancing/verts>`
:doc:`Instancing Vertices </scene_layout/object/properties/instancing/verts>`
:doc:`Interface Searching </interface/controls/templates/operator_search>`
:doc:`Interpolation </grease_pencil/animation/interpolation>`
:doc:`Inverse Kinematics constraint </animation/constraints/tracking/ik_solver>`
:doc:`Keyboard and Mouse </getting_started/configuration/hardware>`
:doc:`Keyed </physics/particles/emitter/physics/keyed>`
:doc:`Keyframe </animation/keyframes/index>`
:doc:`Keyframes </animation/keyframes/index>`
:doc:`Keyframes </animation/keyframes/introduction>`
:doc:`Keying Node </compositing/types/matte/keying>`
:doc:`Keying Screen Node </compositing/types/matte/keying_screen>`
:doc:`Keying Set </animation/keyframes/keying_sets>`
:doc:`Keys (Shape Keys) </animation/shape_keys/introduction>`
:doc:`Laplacian Smooth Modifier </modeling/modifiers/deform/laplacian_smooth>`
:doc:`Lattice </animation/lattice>`
:doc:`Lattice Deform </modeling/modifiers/deform/lattice>`
:doc:`Lattice Edit Mode </animation/lattice>`
:doc:`Lattice Modifier </modeling/modifiers/deform/lattice>`
:doc:`Lattice modifier </modeling/modifiers/deform/lattice>`
:doc:`Lattices </modeling/modifiers/deform/lattice>`
:doc:`Launching from the terminal </advanced/command_line/launch/linux>`
:doc:`Layer Properties </grease_pencil/properties/layers>`
:doc:`Layers </grease_pencil/properties/layers>`
:doc:`Library </files/linked_libraries/index>`
:doc:`Library Overrides </files/linked_libraries/library_overrides>`
:doc:`Library and Data System </files/index>`
:doc:`Light </render/lights/light_object>`
:doc:`Light Falloff </render/shader_nodes/color/light_falloff>`
:doc:`Light Paths </render/cycles/render_settings/light_paths>`
:doc:`Light Probe </render/eevee/light_probes/index>`
:doc:`Light Probe </render/eevee/light_probes/introduction>`
:doc:`Light Threshold </render/eevee/render_settings/shadows>`
:doc:`Light settings </render/lights/light_object>`
:doc:`Limit Location constraint </animation/constraints/transform/limit_location>`
:doc:`Line Style </render/freestyle/introduction>`
:doc:`Linked Libraries </files/linked_libraries/index>`
:doc:`Linked libraries </files/linked_libraries/index>`
:doc:`Linux </getting_started/installing/linux>`
:doc:`Local Camera </editors/3dview/sidebar>`
:doc:`Lock Track Constraint </animation/constraints/tracking/locked_track>`
:doc:`Locked Track Constraint </animation/constraints/tracking/locked_track>`
:doc:`Locked Track constraint </animation/constraints/tracking/locked_track>`
:doc:`Locked Track one </animation/constraints/tracking/locked_track>`
:doc:`Manipulation in 3D Space </scene_layout/object/editing/transform/introduction>`
:doc:`Manual </index>`
:doc:`Map Value </compositing/types/vector/map_value>`
:doc:`Mapped the UVs </modeling/meshes/uv/unwrapping/index>`
:doc:`Mapping </render/shader_nodes/vector/mapping>`
:doc:`Markers </animation/markers>`
:doc:`Markers page </animation/markers>`
:doc:`Mask </compositing/types/input/mask>`
:doc:`Mask </movie_clip/masking/introduction>`
:doc:`Mask Node </compositing/types/input/mask>`
:doc:`Mask data-block </movie_clip/masking/index>`
:doc:`Mask panel </sculpt_paint/texture_paint/tool_settings/mask>`
:doc:`Masking </movie_clip/masking/index>`
:doc:`Masks </grease_pencil/properties/masks>`
:doc:`Material </render/materials/index>`
:doc:`Material </render/materials/introduction>`
:doc:`Material </render/shader_nodes/output/material>`
:doc:`Material Displacement </render/materials/components/displacement>`
:doc:`Material Output </render/shader_nodes/output/material>`
:doc:`Material assignment </render/materials/assignment>`
:doc:`Material properties </editors/properties_editor>`
:doc:`Materials </render/shader_nodes/shader/index>`
:doc:`Math </compositing/types/converter/math>`
:doc:`Math Node </compositing/types/converter/math>`
:doc:`Menu Search </interface/controls/templates/operator_search>`
:doc:`Mesh </modeling/meshes/introduction>`
:doc:`Mesh </modeling/meshes/properties/object_data>`
:doc:`Mesh Cache </modeling/modifiers/modify/mesh_cache>`
:doc:`Mesh Cache modifier </modeling/modifiers/modify/mesh_cache>`
:doc:`Mesh Edit Mode </modeling/meshes/selecting/index>`
:doc:`Mesh Primitive </modeling/meshes/primitives>`
:doc:`Mesh Primitives </modeling/meshes/primitives>`
:doc:`Mesh Retopology </modeling/meshes/retopology>`
:doc:`Mesh Sequence Cache modifier </modeling/modifiers/modify/mesh_sequence_cache>`
:doc:`Mesh Sequence Cache modifiers </modeling/modifiers/modify/mesh_sequence_cache>`
:doc:`Mesh snapping </editors/3dview/controls/snapping>`
:doc:`Meta Primitives </modeling/metas/primitives>`
:doc:`Meta Strips </video_editing/sequencer/meta>`
:doc:`Meta-Rigs </addons/rigging/rigify/metarigs>`
:doc:`Metaball </modeling/metas/introduction>`
:doc:`Metaball </modeling/metas/properties>`
:doc:`Metadata </render/output/metadata>`
:doc:`Mirror </modeling/meshes/editing/mesh/mirror>`
:doc:`Mirror </modeling/modifiers/generate/mirror>`
:doc:`Mirror Modifier </modeling/modifiers/generate/mirror>`
:doc:`Mirroring in Object Mode </scene_layout/object/editing/mirror>`
:doc:`Mix Node </compositing/types/color/mix>`
:doc:`Mix Node </render/shader_nodes/shader/mix>`
:doc:`Mix compositing node </compositing/types/color/mix>`
:doc:`Mix shader </render/shader_nodes/shader/mix>`
:doc:`Modeling </modeling/introduction>`
:doc:`Modeling chapter </modeling/index>`
:doc:`Modifier </modeling/modifiers/generate/solidify>`
:doc:`Modifiers </editors/graph_editor/fcurves/modifiers>`
:doc:`Modifiers </grease_pencil/modifiers/introduction>`
:doc:`Modifiers </modeling/modifiers/index>`
:doc:`Modifiers </modeling/modifiers/introduction>`
:doc:`Motion Blur </render/eevee/render_settings/motion_blur>`
:doc:`Motion Paths </animation/motion_paths>`
:doc:`Motion Tracking </movie_clip/index>`
:doc:`Motion Tracking </movie_clip/tracking/index>`
:doc:`Motor's </physics/rigid_body/constraints/types/motor>`
:doc:`Move </scene_layout/object/editing/transform/move>`
:doc:`Move, Rotate, Scale Basics </modeling/meshes/editing/mesh/transform/basic>`
:doc:`Movie Clip </editors/clip/introduction>`
:doc:`Movie Clip Editor </editors/clip/index>`
:doc:`Movie Clip Editor </movie_clip/masking/index>`
:doc:`Movie Clips </editors/clip/introduction>`
:doc:`Multi-View </render/output/stereoscopy/index>`
:doc:`Multiframe </grease_pencil/multiframe>`
:doc:`Multiresolution </modeling/modifiers/generate/multiresolution>`
:doc:`Multiresolution Modifier </modeling/modifiers/generate/multiresolution>`
:doc:`NLA </editors/nla/introduction>`
:doc:`NLA Editor </editors/nla/index>`
:doc:`NLA Editor </editors/nla/properties_modifiers>`
:doc:`NLA editor </editors/nla/index>`
:doc:`NURBS curve selection </modeling/curves/selecting>`
:doc:`Newtonian Physics </physics/particles/emitter/physics/newtonian>`
:doc:`Node </interface/controls/nodes/index>`
:doc:`Node Tree </render/shader_nodes/groups>`
:doc:`Nodes </interface/controls/nodes/index>`
:doc:`Nodes Support </render/eevee/materials/nodes_support>`
:doc:`Normal </modeling/meshes/editing/mesh/normals>`
:doc:`Normal Map </render/shader_nodes/vector/normal_map>`
:doc:`Normals </modeling/meshes/editing/mesh/normals>`
:doc:`OBJ </addons/import_export/scene_obj>`
:doc:`OSL </render/shader_nodes/osl>`
:doc:`Object </scene_layout/object/index>`
:doc:`Object </scene_layout/object/introduction>`
:doc:`Object </scene_layout/object/properties/index>`
:doc:`Object Constraints </animation/constraints/index>`
:doc:`Object Gizmo </editors/3dview/display/gizmo>`
:doc:`Object Mode </editors/3dview/modes>`
:doc:`Object Mode </scene_layout/object/index>`
:doc:`Object Mode </scene_layout/object/selecting>`
:doc:`Object Mode </scene_layout/object/tools/toolbar>`
:doc:`Object Origin </scene_layout/object/origin>`
:doc:`Object Type Visibility </editors/3dview/display/visibility>`
:doc:`Object Types </scene_layout/object/types>`
:doc:`Object Visual Effects </grease_pencil/visual_effects/index>`
:doc:`Object and Edit Mode Pivot </editors/3dview/controls/pivot_point/index>`
:doc:`Object section </scene_layout/object/index>`
:doc:`Ocean Modifier </modeling/modifiers/physics/ocean>`
:doc:`Onion Skinning </grease_pencil/properties/onion_skinning>`
:doc:`Open Shading Language </render/shader_nodes/osl>`
:doc:`Operator Search </interface/controls/templates/operator_search>`
:doc:`Orientation </editors/3dview/controls/orientation>`
:doc:`Orientations menu </editors/3dview/controls/orientation>`
:doc:`Origin of the object </scene_layout/object/origin>`
:doc:`Other ways to reduce noise </render/cycles/optimizations/reducing_noise>`
:doc:`Outliner </editors/outliner/editing>`
:doc:`Outliner </editors/outliner/index>`
:doc:`Outliner editor </editors/outliner/introduction>`
:doc:`Output </render/output/index>`
:doc:`Output Options </render/output/settings>`
:doc:`Overlays </editors/3dview/display/overlays>`
:doc:`Paint Curve </sculpt_paint/brush/stroke>`
:doc:`Paint and Sculpt Modes </sculpt_paint/index>`
:doc:`Painting Falloff </sculpt_paint/brush/falloff>`
:doc:`Palette </sculpt_paint/index>`
:doc:`Parameter Editor </render/freestyle/parameter_editor/index>`
:doc:`Parent Objects </scene_layout/object/editing/parent>`
:doc:`Parent/Constrain Objects to Bones </scene_layout/object/editing/parent>`
:doc:`Particle </physics/particles/index>`
:doc:`Particle </physics/particles/introduction>`
:doc:`Particle Cache </physics/particles/emitter/cache>`
:doc:`Particle Edit Mode </physics/particles/mode>`
:doc:`Particle Instance Modifier </modeling/modifiers/physics/particle_instance>`
:doc:`Particle Physics </physics/particles/emitter/physics/index>`
:doc:`Particle Visualization </physics/particles/emitter/render>`
:doc:`Particles </physics/particles/index>`
:doc:`Particles </physics/particles/introduction>`
:doc:`Particles System </physics/particles/index>`
:doc:`Path Constraint </animation/constraints/relationship/follow_path>`
:doc:`Physical Simulation </physics/introduction>`
:doc:`Physics </physics/index>`
:doc:`Physics Settings </physics/particles/emitter/physics/index>`
:doc:`Physics chapter </physics/forces/gravity>`
:doc:`Pinch </modeling/meshes/uv/tools/pinch>`
:doc:`Pivot Point </editors/3dview/controls/pivot_point/index>`
:doc:`Pivot Points </editors/3dview/controls/pivot_point/index>`
:doc:`Pivot points </editors/3dview/controls/pivot_point/index>`
:doc:`Plane Track Deform node </compositing/types/distort/plane_track_deform>`
:doc:`Pose Library </animation/armatures/properties/pose_library>`
:doc:`Pose Library Editing </animation/armatures/posing/editing/pose_library>`
:doc:`Pose Library Properties </animation/armatures/properties/pose_library>`
:doc:`Pose Library system </animation/armatures/properties/pose_library>`
:doc:`Pose Mode </animation/armatures/posing/index>`
:doc:`Pose Mode </animation/armatures/posing/selecting>`
:doc:`Positioning Guide </addons/rigging/rigify/bone_positioning>`
:doc:`Preferences </editors/preferences/addons>`
:doc:`Preferences </editors/preferences/editing>`
:doc:`Preferences </editors/preferences/file_paths>`
:doc:`Preferences </editors/preferences/index>`
:doc:`Preferences </editors/preferences/input>`
:doc:`Preferences </editors/preferences/interface>`
:doc:`Preferences </editors/preferences/keymap>`
:doc:`Preferences </editors/preferences/themes>`
:doc:`Preferences editor </editors/preferences/navigation>`
:doc:`Principled BSDF </render/shader_nodes/shader/principled>`
:doc:`Principled Hair </render/shader_nodes/shader/hair_principled>`
:doc:`Principled Volume </render/shader_nodes/shader/volume_principled>`
:doc:`Principled Volume shader </render/shader_nodes/shader/volume_principled>`
:doc:`Properties </editors/properties_editor>`
:doc:`Properties </scene_layout/object/properties/transforms>`
:doc:`Proportional Edit </editors/3dview/controls/proportional_editing>`
:doc:`Proportional Editing </editors/3dview/controls/proportional_editing>`
:doc:`Proportional Editing in 3D </editors/3dview/controls/proportional_editing>`
:doc:`Proxies </files/linked_libraries/library_proxies>`
:doc:`Push/Pull </modeling/meshes/editing/mesh/transform/push_pull>`
:doc:`Python Console </editors/python_console>`
:doc:`Python Scripting </render/freestyle/python>`
:doc:`Python Security </advanced/scripting/security>`
:doc:`Python scripting </render/freestyle/python>`
:doc:`Python scripts </editors/preferences/addons>`
:doc:`Randomize Transform </scene_layout/object/editing/transform/randomize>`
:doc:`Read more about Annotations </interface/annotate_tool>`
:doc:`Read more about Blender's Data System </files/index>`
:doc:`Read more about Grease Pencil </grease_pencil/index>`
:doc:`Read more about Undo and Redo options </interface/undo_redo>`
:doc:`Read more about the Outliner </editors/outliner/index>`
:doc:`Read more about the Transform Gizmo </editors/3dview/display/gizmo>`
:doc:`Recalculate Normals </modeling/meshes/editing/mesh/normals>`
:doc:`Recovering your lost work </troubleshooting/recover>`
:doc:`Reducing Noise </render/cycles/optimizations/reducing_noise>`
:doc:`Relax </modeling/meshes/uv/tools/relax>`
:doc:`Remesh modifier </modeling/modifiers/generate/remesh>`
:doc:`Render </physics/particles/emitter/render>`
:doc:`Render </render/shader_nodes/index>`
:doc:`Render Bake </render/cycles/baking>`
:doc:`Render Layers </compositing/types/input/render_layers>`
:doc:`Render Layers </render/layers/index>`
:doc:`Render Layers </render/layers/layers>`
:doc:`Render Layers node </compositing/types/input/render_layers>`
:doc:`Render Output </render/output/settings>`
:doc:`Render Pass </render/layers/passes>`
:doc:`Render Passes </render/layers/passes>`
:doc:`Render mode </physics/particles/emitter/render>`
:doc:`Rendering </render/introduction>`
:doc:`Rendering Animations </render/output/animation>`
:doc:`Rendering audio </render/output/audio/introduction>`
:doc:`Rig Types </addons/rigging/rigify/rig_types/index>`
:doc:`Rigid Bodies </physics/rigid_body/index>`
:doc:`Rigid Body World </physics/rigid_body/world>`
:doc:`Rip </modeling/meshes/uv/tools/rip>`
:doc:`Rotate </scene_layout/object/editing/transform/rotate>`
:doc:`Sampling </render/cycles/render_settings/sampling>`
:doc:`Scale </compositing/types/distort/scale>`
:doc:`Scale </scene_layout/object/editing/transform/scale>`
:doc:`Scale node </compositing/types/distort/scale>`
:doc:`Scene </scene_layout/scene/index>`
:doc:`Scene </scene_layout/scene/introduction>`
:doc:`Scene </scene_layout/scene/properties>`
:doc:`Scene Level Motion Blur </render/cycles/render_settings/motion_blur>`
:doc:`Scene Strips </video_editing/sequencer/strips/scene>`
:doc:`Screw </modeling/meshes/editing/edge/screw>`
:doc:`Screw Modifier </modeling/modifiers/generate/screw>`
:doc:`Sculpt Mode </grease_pencil/modes/sculpting/introduction>`
:doc:`Sculpt Mode </sculpt_paint/sculpting/index>`
:doc:`Sculpt Mode </sculpt_paint/sculpting/introduction>`
:doc:`Sculpting </sculpt_paint/sculpting/introduction>`
:doc:`Select All by Trait </modeling/meshes/selecting/all_by_trait>`
:doc:`Selecting UVs </editors/uv/selecting>`
:doc:`Selecting UVs </modeling/meshes/uv/editing>`
:doc:`Selecting in the 3D Viewport </editors/3dview/selecting>`
:doc:`Selection Mode </modeling/meshes/selecting/introduction>`
:doc:`Sequence Editor </video_editing/introduction>`
:doc:`Sequence Strip </video_editing/sequencer/strips/index>`
:doc:`Sequencer Display </video_editing/preview/introduction>`
:doc:`Set Alpha Node </compositing/types/converter/set_alpha>`
:doc:`Set Strength </modeling/meshes/editing/mesh/normals>`
:doc:`Shade Smooth and Flat </scene_layout/object/editing/shading>`
:doc:`Shader Editor </editors/shader_editor>`
:doc:`Shader Nodes </render/shader_nodes/index>`
:doc:`Shader to RGB </render/shader_nodes/converter/shader_to_rgb>`
:doc:`Shaders </render/shader_nodes/shader/index>`
:doc:`Shading popover </editors/3dview/display/shading>`
:doc:`Shape Key </animation/shape_keys/index>`
:doc:`Shape Key </editors/dope_sheet/shape_key>`
:doc:`Shape Keys </animation/shape_keys/index>`
:doc:`Shape Keys panel </animation/shape_keys/shape_keys_panel>`
:doc:`Shape keys </animation/shape_keys/index>`
:doc:`Shaped Bones </animation/armatures/bones/properties/display>`
:doc:`Shear </modeling/meshes/editing/mesh/transform/shear>`
:doc:`Shrinkwrap </animation/constraints/relationship/shrinkwrap>`
:doc:`Shrinkwrap Constraint </animation/constraints/relationship/shrinkwrap>`
:doc:`Shrinkwrap Modifier </modeling/modifiers/deform/shrinkwrap>`
:doc:`Sidebar </interface/controls/nodes/sidebar>`
:doc:`Sidebar Panels </editors/3dview/sidebar>`
:doc:`Simulations </physics/introduction>`
:doc:`Skin Modifier </modeling/modifiers/generate/skin>`
:doc:`Skinning Mesh Objects </animation/armatures/skinning/introduction>`
:doc:`Smooth Modifier </modeling/modifiers/deform/smooth>`
:doc:`Snap Menu </editors/3dview/controls/snapping>`
:doc:`Snapping in 3D </editors/3dview/controls/snapping>`
:doc:`Soft Bodies </physics/soft_body/index>`
:doc:`Soft Body </physics/soft_body/index>`
:doc:`Solidify Modifier </modeling/modifiers/generate/solidify>`
:doc:`Sounds </render/output/audio/speaker>`
:doc:`Speaker </render/output/audio/speaker>`
:doc:`Splash Screen </interface/splash>`
:doc:`Spline IK </animation/constraints/tracking/spline_ik>`
:doc:`Status Bar </interface/window_system/status_bar>`
:doc:`Strip Proxy and Cache properties </video_editing/sequencer/properties/proxy_cache>`
:doc:`Stroke </sculpt_paint/brush/stroke>`
:doc:`Stroke Menu </grease_pencil/modes/edit/stroke_menu>`
:doc:`Stroke Placement </grease_pencil/modes/draw/stroke_placement>`
:doc:`Strokes </grease_pencil/properties/strokes>`
:doc:`Structure </modeling/metas/structure>`
:doc:`Subdivide </modeling/meshes/editing/edge/subdivide>`
:doc:`Subdivision </modeling/modifiers/generate/subdivision_surface>`
:doc:`Subdivision Surface </modeling/modifiers/generate/subdivision_surface>`
:doc:`Subdivision Surface Modifier </modeling/modifiers/generate/subdivision_surface>`
:doc:`Subdivision Surface modifiers </modeling/modifiers/generate/subdivision_surface>`
:doc:`Subdivision Surfaces </modeling/modifiers/generate/subdivision_surface>`
:doc:`Surface </modeling/surfaces/introduction>`
:doc:`Surface </modeling/surfaces/properties/index>`
:doc:`Surface Edit Mode </modeling/surfaces/selecting>`
:doc:`Surfaces </modeling/surfaces/introduction>`
:doc:`Surfaces Primitives </modeling/surfaces/primitives>`
:doc:`Switch View node </compositing/types/converter/switch_view>`
:doc:`System Console </advanced/command_line/introduction>`
:doc:`System Preferences </editors/preferences/system>`
:doc:`System tab </editors/preferences/system>`
:doc:`Text </editors/text_editor>`
:doc:`Text </modeling/texts/introduction>`
:doc:`Text </modeling/texts/properties>`
:doc:`Text Edit Mode </modeling/texts/selecting>`
:doc:`Text Editor </editors/text_editor>`
:doc:`Text Object </modeling/texts/index>`
:doc:`Text strips </video_editing/sequencer/strips/text>`
:doc:`Texture </render/materials/legacy_textures/index>`
:doc:`Texture </render/materials/legacy_textures/introduction>`
:doc:`Texture </sculpt_paint/brush/texture>`
:doc:`Texture Coordinate Node </render/shader_nodes/input/texture_coordinate>`
:doc:`Texture Coordinate node </render/shader_nodes/input/texture_coordinate>`
:doc:`Texture Node Editor </editors/texture_node/index>`
:doc:`Texture Paint </sculpt_paint/texture_paint/introduction>`
:doc:`Texture Paint Mode </sculpt_paint/texture_paint/index>`
:doc:`Texture color </render/workbench/color>`
:doc:`Texture nodes </render/shader_nodes/textures/index>`
:doc:`Textures </render/shader_nodes/textures/index>`
:doc:`Texturing </editors/uv/introduction>`
:doc:`The multi-view workflow </render/output/stereoscopy/index>`
:doc:`Time node </compositing/types/input/time>`
:doc:`Timeline </editors/timeline>`
:doc:`To Sphere </modeling/meshes/editing/mesh/transform/to_sphere>`
:doc:`Toggles the Camera View </editors/3dview/navigate/camera_view>`
:doc:`Toggles the Projection </editors/3dview/navigate/projections>`
:doc:`Tone Map Node </compositing/types/color/tone_map>`
:doc:`Toolbar </grease_pencil/modes/draw/tools>`
:doc:`Toolbar </grease_pencil/modes/edit/tools>`
:doc:`Tools </editors/3dview/toolbar/index>`
:doc:`Tooltip </getting_started/help>`
:doc:`Topbar </interface/window_system/topbar>`
:doc:`Track To Constraint </animation/constraints/tracking/track_to>`
:doc:`Track To constraint </animation/constraints/tracking/track_to>`
:doc:`Tracking Axis </scene_layout/object/properties/relations>`
:doc:`Transfer Mesh Data Operator </scene_layout/object/editing/relations/transfer_mesh_data>`
:doc:`Transform </scene_layout/object/editing/transform/introduction>`
:doc:`Transform Control </scene_layout/object/editing/transform/control/index>`
:doc:`Transform Orientation </editors/3dview/controls/orientation>`
:doc:`Transform Orientations </editors/3dview/controls/orientation>`
:doc:`Transform panel </modeling/curves/editing/transform_panel>`
:doc:`Transformation Orientations </editors/3dview/controls/orientation>`
:doc:`Transformation constraint </animation/constraints/transform/transformation>`
:doc:`Transformations (translation/scale/rotation) </scene_layout/object/editing/transform/introduction>`
:doc:`Transformations </modeling/meshes/editing/mesh/transform/index>`
:doc:`Transformations </scene_layout/object/editing/transform/index>`
:doc:`Transparent BSDF </render/shader_nodes/shader/transparent>`
:doc:`Transparent BSDFs are given special treatment </render/cycles/render_settings/light_paths>`
:doc:`Triangulate modifier </modeling/modifiers/generate/triangulate>`
:doc:`UDIM </modeling/meshes/uv/workflows/udims>`
:doc:`UV Map node </render/shader_nodes/input/uv_map>`
:doc:`UV Seams </modeling/meshes/uv/unwrapping/seams>`
:doc:`UV Unwrapping </modeling/meshes/uv/unwrapping/index>`
:doc:`UV Warp </modeling/modifiers/modify/uv_warp>`
:doc:`UV editor </editors/texture_node/introduction>`
:doc:`UVs </modeling/meshes/uv/index>`
:doc:`Unwrapping Meshes </modeling/meshes/uv/unwrapping/index>`
:doc:`Unwrapping Tools </modeling/meshes/editing/uv>`
:doc:`Use the Armature Modifier on entire Mesh </animation/armatures/skinning/parenting>`
:doc:`User Interface </interface/index>`
:doc:`Using Vertex Group </sculpt_paint/weight_paint/usage>`
:doc:`VFX </movie_clip/index>`
:doc:`VR Scene Inspection add-on </addons/3d_view/vr_scene_inspection>`
:doc:`VSE </video_editing/index>`
:doc:`Vector Displacement </render/shader_nodes/vector/vector_displacement>`
:doc:`Vector Nodes </render/shader_nodes/vector/index>`
:doc:`Vertex Colors </sculpt_paint/vertex_paint/index>`
:doc:`Vertex Group </modeling/meshes/properties/vertex_groups/index>`
:doc:`Vertex Group </modeling/meshes/properties/vertex_groups/vertex_groups>`
:doc:`Vertex Groups </modeling/meshes/properties/vertex_groups/index>`
:doc:`Vertex Groups </modeling/meshes/properties/vertex_groups/introduction>`
:doc:`Vertex Groups </physics/particles/emitter/vertex_groups>`
:doc:`Vertex Mode </grease_pencil/modes/vertex_paint/introduction>`
:doc:`Vertex Paint </sculpt_paint/vertex_paint/index>`
:doc:`Vertex Paint </sculpt_paint/vertex_paint/introduction>`
:doc:`Vertex Paint Brush </grease_pencil/modes/vertex_paint/tool_settings/brush>`
:doc:`Vertex Paint Mode </sculpt_paint/vertex_paint/index>`
:doc:`Vertex Weight Proximity </modeling/modifiers/modify/weight_proximity>`
:doc:`Video Editing </video_editing/index>`
:doc:`Video Output </render/output/file_formats>`
:doc:`Video Sequence Editor </video_editing/index>`
:doc:`Video Sequence editor </video_editing/index>`
:doc:`Video Sequencer </video_editing/index>`
:doc:`Video Sequencer </video_editing/sequencer/index>`
:doc:`View Layer </scene_layout/view_layers/index>`
:doc:`View Layers </render/layers/index>`
:doc:`View Perspective </editors/3dview/navigate/projections>`
:doc:`Viewer Node </compositing/types/output/viewer>`
:doc:`Viewport Display </interface/controls/templates/curve>`
:doc:`Viewport Overlays </editors/3dview/display/overlays>`
:doc:`Visualization </physics/particles/emitter/render>`
:doc:`Volume </modeling/volumes/introduction>`
:doc:`Volume Absorption </render/shader_nodes/shader/volume_absorption>`
:doc:`Volume Render Settings </render/cycles/render_settings/volumes>`
:doc:`Volume Scatter </render/shader_nodes/shader/volume_scatter>`
:doc:`Volume Shading </render/shader_nodes/shader/volume_principled>`
:doc:`Volumes </modeling/volumes/index>`
:doc:`Wave </modeling/modifiers/deform/wave>`
:doc:`Weight Normals Modifier </modeling/modifiers/modify/weighted_normal>`
:doc:`Weight Paint </modeling/meshes/properties/vertex_groups/vertex_groups>`
:doc:`Weight Paint </sculpt_paint/weight_paint/introduction>`
:doc:`Weight Paint Mode </grease_pencil/modes/weight_paint/index>`
:doc:`Weight Paint Mode </grease_pencil/modes/weight_paint/introduction>`
:doc:`Weight Paint Mode </sculpt_paint/weight_paint/index>`
:doc:`Weight Painting </sculpt_paint/weight_paint/index>`
:doc:`Weighted Normals </modeling/modifiers/modify/weighted_normal>`
:doc:`Weighted Normals modifier </modeling/modifiers/modify/weighted_normal>`
:doc:`White Noise Texture </render/shader_nodes/textures/white_noise>`
:doc:`Window Manager </interface/window_system/introduction>`
:doc:`Windows </getting_started/installing/windows>`
:doc:`Workbench </render/workbench/index>`
:doc:`Workspace </interface/window_system/workspaces>`
:doc:`Workspaces </interface/window_system/workspaces>`
:doc:`World </render/lights/world>`
:doc:`World </render/shader_nodes/output/world>`
:doc:`actions </animation/actions>`
:doc:`add-on </addons/import_export/mesh_uv_layout>`
:doc:`add-ons </editors/preferences/addons>`
:doc:`aligned view </editors/3dview/navigate/align>`
:doc:`animated </animation/index>`
:doc:`animation chapter </animation/index>`
:doc:`animation curves </editors/graph_editor/fcurves/introduction>`
:doc:`annotation tool </interface/annotate_tool>`
:doc:`area </interface/window_system/areas>`
:doc:`arguments </advanced/command_line/arguments>`
:doc:`armature section </animation/armatures/index>`
:doc:`armatures editing section </animation/armatures/bones/editing/index>`
:doc:`armatures section </animation/armatures/bones/editing/introduction>`
:doc:`as instructed </about/contribute/build/index>`
:doc:`assigned </render/materials/assignment>`
:doc:`axis locking </scene_layout/object/editing/transform/control/axis_locking>`
:doc:`axis locking page </scene_layout/object/editing/transform/control/axis_locking>`
:doc:`bake </physics/particles/emitter/cache>`
:doc:`baked </physics/baking>`
:doc:`bendy bone </animation/armatures/bones/properties/bendy_bones>`
:doc:`bone page </animation/armatures/bones/index>`
:doc:`brush </grease_pencil/modes/draw/tool_settings/index>`
:doc:`brushes </sculpt_paint/brush/index>`
:doc:`camera settings </render/cameras>`
:doc:`cameras </render/cameras>`
:doc:`children </physics/particles/emitter/children>`
:doc:`children </scene_layout/object/editing/parent>`
:doc:`cloth simulation </sculpt_paint/sculpting/tools/cloth>`
:doc:`collection hierarchy </scene_layout/collections/index>`
:doc:`collection instance </scene_layout/object/properties/instancing/collection>`
:doc:`collections </scene_layout/collections/introduction>`
:doc:`collision physics </physics/collision>`
:doc:`color </render/workbench/color>`
:doc:`color transform </render/color_management>`
:doc:`command line </advanced/command_line/index>`
:doc:`community </getting_started/about/community>`
:doc:`composited </compositing/index>`
:doc:`compositing </compositing/index>`
:doc:`compositing </compositing/introduction>`
:doc:`configuration directories </advanced/blender_directory_layout>`
:doc:`constraint stack </animation/constraints/interface/stack>`
:doc:`constraints pages </animation/constraints/index>`
:doc:`controlled </physics/fluid/type/domain/field_weights>`
:doc:`converted to/from meshes </scene_layout/object/editing/convert>`
:doc:`core options </render/freestyle/render>`
:doc:`curve widget </interface/controls/templates/curve>`
:doc:`curves </modeling/curves/introduction>`
:doc:`data-block </files/data_blocks>`
:doc:`data-block previews </files/blend/previews>`
:doc:`data-blocks </files/data_blocks>`
:doc:`directory layout </advanced/blender_directory_layout>`
:doc:`displacement </render/materials/components/displacement>`
:doc:`driven </animation/drivers/index>`
:doc:`driver </animation/drivers/index>`
:doc:`duplicated </scene_layout/object/editing/duplicate_linked>`
:doc:`edit them </modeling/meshes/uv/editing>`
:doc:`editing pages </animation/armatures/bones/editing/transform>`
:doc:`editing tools </modeling/index>`
:doc:`effects </video_editing/sequencer/strips/effects/index>`
:doc:`emitted </physics/particles/emitter/index>`
:doc:`empty object </modeling/empties>`
:doc:`exporters </files/import_export>`
:doc:`extrude </modeling/curves/properties/geometry>`
:doc:`extruded </modeling/meshes/editing/edge/extrude_edges>`
:doc:`extruding a curve </modeling/curves/properties/geometry>`
:doc:`extruding a profile along a path </modeling/curves/properties/geometry>`
:doc:`extrusion tools </modeling/curves/properties/geometry>`
:doc:`face loop </modeling/meshes/structure>`
:doc:`face shading </modeling/meshes/editing/face/shading>`
:doc:`fluid simulation cache </physics/fluid/type/domain/cache>`
:doc:`follow a curve </modeling/modifiers/deform/curve>`
:doc:`force fields </physics/forces/force_fields/index>`
:doc:`format </render/output/file_formats>`
:doc:`format that is supported by Blender </render/output/settings>`
:doc:`free and open source </getting_started/about/license>`
:doc:`from faces </scene_layout/object/properties/instancing/faces>`
:doc:`from particles </physics/particles/introduction>`
:doc:`general visibility </scene_layout/object/properties/visibility>`
:doc:`generic wrapper </addons/import_export/node_shaders_info>`
:doc:`gizmos </editors/3dview/display/gizmo>`
:doc:`glTF </addons/import_export/scene_gltf2>`
:doc:`glossary </glossary/index>`
:doc:`header </animation/constraints/interface/header>`
:doc:`here </advanced/appendices/rotations>`
:doc:`here </compositing/types/color/mix>`
:doc:`here </files/media/video_formats>`
:doc:`here </interface/keymap/blender_default>`
:doc:`here </interface/keymap/industry_compatible>`
:doc:`here </modeling/meshes/editing/edge/edge_data>`
:doc:`here </modeling/meshes/properties/vertex_groups/vertex_groups>`
:doc:`here </scene_layout/object/editing/duplicate>`
:doc:`hidden </scene_layout/object/editing/show_hide>`
:doc:`hook </modeling/modifiers/deform/hooks>`
:doc:`image feature tracking component </movie_clip/tracking/clip/introduction>`
:doc:`image formats </files/media/image_formats>`
:doc:`image sequence </video_editing/sequencer/strips/movie_image>`
:doc:`importing an Alembic file </files/import_export/alembic>`
:doc:`instance </scene_layout/object/properties/instancing/index>`
:doc:`instanced </scene_layout/object/properties/instancing/index>`
:doc:`instancing from faces </scene_layout/object/properties/instancing/faces>`
:doc:`interface section </interface/selecting>`
:doc:`interior forces </physics/soft_body/forces/interior>`
:doc:`inverse kinematic </animation/armatures/posing/bone_constraints/inverse_kinematics/introduction>`
:doc:`keyframe </animation/keyframes/index>`
:doc:`keyframe </animation/keyframes/introduction>`
:doc:`keyframed </animation/keyframes/index>`
:doc:`keyframes </animation/keyframes/introduction>`
:doc:`keymap </editors/preferences/keymap>`
:doc:`keymap </interface/keymap/blender_default>`
:doc:`keymap preferences </editors/preferences/keymap>`
:doc:`lattice </animation/lattice>`
:doc:`layers </grease_pencil/properties/layers>`
:doc:`layers and passes </render/layers/index>`
:doc:`light object </render/lights/light_object>`
:doc:`lighting </render/workbench/lighting>`
:doc:`lights </render/lights/index>`
:doc:`limitations </render/eevee/limitations>`
:doc:`line style </render/freestyle/parameter_editor/line_style/introduction>`
:doc:`link/append </files/linked_libraries/index>`
:doc:`linked </files/linked_libraries/index>`
:doc:`linked libraries </files/linked_libraries/index>`
:doc:`locked </scene_layout/object/editing/transform/control/axis_locking>`
:doc:`manually flip the normals </modeling/meshes/editing/mesh/normals>`
:doc:`masking </sculpt_paint/sculpting/tools/mask>`
:doc:`material </grease_pencil/materials/introduction>`
:doc:`material </physics/fluid/material>`
:doc:`material nodes </render/shader_nodes/index>`
:doc:`materials </render/materials/index>`
:doc:`median </editors/3dview/controls/pivot_point/median_point>`
:doc:`mesh </modeling/meshes/editing/introduction>`
:doc:`mesh </modeling/meshes/index>`
:doc:`mesh counterpart </modeling/meshes/tools/spin>`
:doc:`mesh data layer </modeling/meshes/editing/mesh/normals>`
:doc:`mesh editing </modeling/meshes/editing/introduction>`
:doc:`mesh editing </modeling/meshes/editing/mesh/mirror>`
:doc:`mesh section </scene_layout/object/editing/transform/control/index>`
:doc:`mesh vertices </modeling/meshes/editing/mesh/mirror>`
:doc:`meshes </modeling/meshes/selecting/index>`
:doc:`mode </editors/3dview/modes>`
:doc:`modes </editors/3dview/modes>`
:doc:`modified </video_editing/sequencer/editing>`
:doc:`modifier </editors/graph_editor/fcurves/modifiers>`
:doc:`modifier </modeling/modifiers/index>`
:doc:`modifier </modeling/modifiers/modify/data_transfer>`
:doc:`modifiers </editors/graph_editor/fcurves/modifiers>`
:doc:`modifiers </grease_pencil/modifiers/index>`
:doc:`modifiers </modeling/modifiers/introduction>`
:doc:`motion tracking </movie_clip/index>`
:doc:`navigate </editors/3dview/navigate/index>`
:doc:`node </render/shader_nodes/shader/specular_bsdf>`
:doc:`node editor </interface/controls/nodes/index>`
:doc:`nodes </interface/controls/nodes/index>`
:doc:`numeric transformation </scene_layout/object/editing/transform/control/numeric_input>`
:doc:`object origin </scene_layout/object/origin>`
:doc:`object skinning </scene_layout/object/editing/parent>`
:doc:`objects </scene_layout/object/editing/transform/introduction>`
:doc:`operator </scene_layout/object/editing/relations/transfer_mesh_data>`
:doc:`options </render/workbench/options>`
:doc:`origin </scene_layout/object/origin>`
:doc:`output </render/output/index>`
:doc:`overlays </editors/3dview/display/overlays>`
:doc:`overridden </files/linked_libraries/library_overrides>`
:doc:`override </files/linked_libraries/library_overrides>`
:doc:`painting modes </sculpt_paint/brush/introduction>`
:doc:`parameter editor </render/freestyle/parameter_editor/index>`
:doc:`parent </scene_layout/object/editing/parent>`
:doc:`parenting </scene_layout/object/editing/parent>`
:doc:`particle system </physics/particles/emitter/render>`
:doc:`passes </render/layers/passes>`
:doc:`physics simulations </physics/index>`
:doc:`pinned </physics/cloth/settings/shape>`
:doc:`pivot point </editors/3dview/controls/pivot_point/index>`
:doc:`pivot point page </editors/3dview/controls/pivot_point/index>`
:doc:`pose </animation/armatures/posing/index>`
:doc:`pose library </animation/armatures/properties/pose_library>`
:doc:`pose library feature </animation/armatures/properties/pose_library>`
:doc:`poses </animation/armatures/posing/index>`
:doc:`posing </animation/armatures/posing/index>`
:doc:`posing part </animation/armatures/posing/selecting>`
:doc:`previous pages </animation/armatures/index>`
:doc:`primitive shape </modeling/metas/primitives>`
:doc:`procedural texture nodes </render/shader_nodes/textures/index>`
:doc:`properties </interface/controls/nodes/sidebar>`
:doc:`recover </troubleshooting/recover>`
:doc:`relative shape keys </animation/shape_keys/index>`
:doc:`render pass </render/layers/passes>`
:doc:`render passes </render/layers/passes>`
:doc:`rendering </render/index>`
:doc:`rendering </render/output/index>`
:doc:`rendering camera </render/cameras>`
:doc:`rendering to videos </render/output/file_formats>`
:doc:`rotate </compositing/types/distort/rotate>`
:doc:`sculpting </sculpt_paint/sculpting/index>`
:doc:`seams </modeling/meshes/uv/unwrapping/seams>`
:doc:`selected </modeling/curves/selecting>`
:doc:`selected </video_editing/sequencer/selecting>`
:doc:`selecting in the 3D Viewport </scene_layout/object/selecting>`
:doc:`selection </scene_layout/object/selecting>`
:doc:`settings </render/materials/settings>`
:doc:`several modes </editors/3dview/modes>`
:doc:`shader </grease_pencil/materials/grease_pencil_shader>`
:doc:`shader nodes </render/shader_nodes/index>`
:doc:`shader nodes manual </render/shader_nodes/shader/index>`
:doc:`shading </editors/3dview/display/shading>`
:doc:`shading nodes </render/shader_nodes/introduction>`
:doc:`shape key </animation/shape_keys/index>`
:doc:`shape key </animation/shape_keys/introduction>`
:doc:`shape keys </animation/shape_keys/index>`
:doc:`shape keys </animation/shape_keys/introduction>`
:doc:`skin </animation/armatures/skinning/index>`
:doc:`skinned </animation/armatures/skinning/index>`
:doc:`skinning pages </animation/armatures/skinning/index>`
:doc:`skinning part </animation/armatures/skinning/index>`
:doc:`skinning section </animation/armatures/skinning/index>`
:doc:`snap </editors/3dview/controls/snapping>`
:doc:`snap tool </editors/3dview/controls/snapping>`
:doc:`snapping </editors/3dview/controls/snapping>`
:doc:`snapping tools </editors/3dview/controls/snapping>`
:doc:`soft bodies </physics/soft_body/index>`
:doc:`splitting the area </interface/window_system/areas>`
:doc:`standard selection </scene_layout/object/selecting>`
:doc:`standard text editing shortcuts </interface/keymap/introduction>`
:doc:`startup file </getting_started/configuration/defaults>`
:doc:`startup scene </editors/3dview/startup_scene>`
:doc:`structure </modeling/metas/structure>`
:doc:`surface </modeling/surfaces/index>`
:doc:`surface </render/materials/components/surface>`
:doc:`surface shader </render/materials/components/surface>`
:doc:`tabs and panels </interface/window_system/tabs_panels>`
:doc:`text object </modeling/texts/index>`
:doc:`texture data-block </render/materials/legacy_textures/introduction>`
:doc:`this page </files/linked_libraries/index>`
:doc:`this page </physics/soft_body/settings/index>`
:doc:`tool </editors/3dview/toolbar/index>`
:doc:`tool </sculpt_paint/sculpting/tools/index>`
:doc:`tracking or masking </movie_clip/index>`
:doc:`transform gizmos </editors/3dview/display/gizmo>`
:doc:`transform orientation </editors/3dview/controls/orientation>`
:doc:`translate </compositing/types/distort/translate>`
:doc:`troubleshooting </troubleshooting/index>`
:doc:`unwrapped </modeling/meshes/uv/unwrapping/introduction>`
:doc:`user interface </interface/window_system/areas>`
:doc:`vertex group </modeling/meshes/properties/vertex_groups/index>`
:doc:`vertex groups </modeling/meshes/properties/vertex_groups/index>`
:doc:`vertex/edge selection </modeling/meshes/selecting/introduction>`
:doc:`video formats </files/media/video_formats>`
:doc:`viewport overlay </editors/3dview/display/overlays>`
:doc:`visual effects </grease_pencil/modifiers/index>`
:doc:`volume </render/materials/components/volume>`
:doc:`volume shader </render/materials/components/volume>`
:doc:`workspace </interface/window_system/workspaces>`
:guilabel:`2D Painting Only`
:guilabel:`Closest Interpolation Only`
:guilabel:`Complex Mode`
:guilabel:`Compositor Only`
:guilabel:`Cycles Only`
:guilabel:`Eevee Only`
:guilabel:`Fire or Smoke Only`
:guilabel:`Gas Only`
:guilabel:`Grid Display Only`
:guilabel:`Gridlines Only`
:guilabel:`Liquids Only`
:guilabel:`OpenVDB Only`
:guilabel:`Sculpt Mode Only`
:guilabel:`Simple Mode`
:guilabel:`Simulation FLIP Only`
:guilabel:`Streamlines or Needle Only`
:kbd:`'`
:kbd:`0`
:kbd:`1-9`
:kbd:`1`
:kbd:`2`
:kbd:`3`
:kbd:`9`
:kbd:`;`
:kbd:`=`
:kbd:`A`
:kbd:`AccentGrave`
:kbd:`Alt-0`
:kbd:`Alt-1`
:kbd:`Alt-9`
:kbd:`Alt-A`
:kbd:`Alt-B`
:kbd:`Alt-Backspace`
:kbd:`Alt-C`
:kbd:`Alt-D`
:kbd:`Alt-Down`
:kbd:`Alt-E`
:kbd:`Alt-F1`
:kbd:`Alt-F`
:kbd:`Alt-G`
:kbd:`Alt-H`
:kbd:`Alt-I`
:kbd:`Alt-J`
:kbd:`Alt-K`
:kbd:`Alt-LMB`
:kbd:`Alt-L`
:kbd:`Alt-Left`
:kbd:`Alt-MMB`
:kbd:`Alt-M`
:kbd:`Alt-Minus`
:kbd:`Alt-N`
:kbd:`Alt-O`
:kbd:`Alt-P`
:kbd:`Alt-PageDown`
:kbd:`Alt-PageUp`
:kbd:`Alt-Period`
:kbd:`Alt-RMB`
:kbd:`Alt-R`
:kbd:`Alt-Right`
:kbd:`Alt-S`
:kbd:`Alt-Slash`
:kbd:`Alt-Spacebar`
:kbd:`Alt-T`
:kbd:`Alt-Up`
:kbd:`Alt-V`
:kbd:`Alt-W`
:kbd:`Alt-Wheel`
:kbd:`Alt-X`
:kbd:`Alt`
:kbd:`B`
:kbd:`Backslash`
:kbd:`Backspace`
:kbd:`C`
:kbd:`Cmd-Comma`
:kbd:`Cmd`
:kbd:`Comma`
:kbd:`Ctrl-0`
:kbd:`Ctrl-1`
:kbd:`Ctrl-2`
:kbd:`Ctrl-3`
:kbd:`Ctrl-5`
:kbd:`Ctrl-=`
:kbd:`Ctrl-A`
:kbd:`Ctrl-AccentGrave`
:kbd:`Ctrl-Alt-0`
:kbd:`Ctrl-Alt-A`
:kbd:`Ctrl-Alt-B`
:kbd:`Ctrl-Alt-C`
:kbd:`Ctrl-Alt-D`
:kbd:`Ctrl-Alt-E`
:kbd:`Ctrl-Alt-G`
:kbd:`Ctrl-Alt-H`
:kbd:`Ctrl-Alt-LMB`
:kbd:`Ctrl-Alt-MMB`
:kbd:`Ctrl-Alt-Minus`
:kbd:`Ctrl-Alt-Numpad0`
:kbd:`Ctrl-Alt-P`
:kbd:`Ctrl-Alt-Q`
:kbd:`Ctrl-Alt-R`
:kbd:`Ctrl-Alt-S`
:kbd:`Ctrl-Alt-Slash`
:kbd:`Ctrl-Alt-Spacebar`
:kbd:`Ctrl-Alt-T`
:kbd:`Ctrl-Alt-V`
:kbd:`Ctrl-Alt-W`
:kbd:`Ctrl-Alt-Wheel`
:kbd:`Ctrl-Alt-X`
:kbd:`Ctrl-Alt`
:kbd:`Ctrl-B`
:kbd:`Ctrl-Backspace`
:kbd:`Ctrl-C`
:kbd:`Ctrl-D`
:kbd:`Ctrl-Delete`
:kbd:`Ctrl-Down`
:kbd:`Ctrl-E`
:kbd:`Ctrl-End`
:kbd:`Ctrl-F11`
:kbd:`Ctrl-F12`
:kbd:`Ctrl-F2`
:kbd:`Ctrl-F`
:kbd:`Ctrl-G`
:kbd:`Ctrl-H`
:kbd:`Ctrl-Home`
:kbd:`Ctrl-I`
:kbd:`Ctrl-J`
:kbd:`Ctrl-LMB`
:kbd:`Ctrl-L`
:kbd:`Ctrl-Left`
:kbd:`Ctrl-MMB`
:kbd:`Ctrl-M`
:kbd:`Ctrl-Minus`
:kbd:`Ctrl-N`
:kbd:`Ctrl-Numpad0`
:kbd:`Ctrl-Numpad1`
:kbd:`Ctrl-Numpad2`
:kbd:`Ctrl-Numpad3`
:kbd:`Ctrl-Numpad4`
:kbd:`Ctrl-Numpad6`
:kbd:`Ctrl-Numpad7`
:kbd:`Ctrl-Numpad8`
:kbd:`Ctrl-NumpadAsterisk`
:kbd:`Ctrl-NumpadMinus`
:kbd:`Ctrl-NumpadPeriod`
:kbd:`Ctrl-NumpadPlus`
:kbd:`Ctrl-NumpadSlash`
:kbd:`Ctrl-O`
:kbd:`Ctrl-P 1`
:kbd:`Ctrl-P 2`
:kbd:`Ctrl-P`
:kbd:`Ctrl-PageDown`
:kbd:`Ctrl-PageUp`
:kbd:`Ctrl-Period`
:kbd:`Ctrl-Q`
:kbd:`Ctrl-RMB`
:kbd:`Ctrl-R`
:kbd:`Ctrl-Return`
:kbd:`Ctrl-Right`
:kbd:`Ctrl-S`
:kbd:`Ctrl-Slash`
:kbd:`Ctrl-Spacebar`
:kbd:`Ctrl-T`
:kbd:`Ctrl-Tab`
:kbd:`Ctrl-Up`
:kbd:`Ctrl-V`
:kbd:`Ctrl-W`
:kbd:`Ctrl-WheelDown`
:kbd:`Ctrl-WheelUp`
:kbd:`Ctrl-Wheel`
:kbd:`Ctrl-X`
:kbd:`Ctrl-Z`
:kbd:`Ctrl-[`
:kbd:`Ctrl-]`
:kbd:`Ctrl`
:kbd:`D`
:kbd:`Delete`
:kbd:`Down`
:kbd:`E R`
:kbd:`E S`
:kbd:`E`
:kbd:`End`
:kbd:`Equals`
:kbd:`Esc`
:kbd:`F10`
:kbd:`F11`
:kbd:`F12`
:kbd:`F1`
:kbd:`F2`
:kbd:`F3`
:kbd:`F4`
:kbd:`F5`
:kbd:`F6`
:kbd:`F8`
:kbd:`F9`
:kbd:`F`
:kbd:`G 1`
:kbd:`G X Minus 1`
:kbd:`G X Minus 3`
:kbd:`G Z Z 0`
:kbd:`G`
:kbd:`H`
:kbd:`Home`
:kbd:`I`
:kbd:`J`
:kbd:`K`
:kbd:`LMB`
:kbd:`L`
:kbd:`Left`
:kbd:`MMB`
:kbd:`M`
:kbd:`Menu`
:kbd:`Minus 3`
:kbd:`Minus`
:kbd:`NDOFMenu`
:kbd:`N`
:kbd:`Numpad0`
:kbd:`Numpad1`
:kbd:`Numpad2`
:kbd:`Numpad3`
:kbd:`Numpad4`
:kbd:`Numpad5`
:kbd:`Numpad6`
:kbd:`Numpad7`
:kbd:`Numpad8`
:kbd:`Numpad9`
:kbd:`NumpadAsterisk`
:kbd:`NumpadDelete`
:kbd:`NumpadMinus`
:kbd:`NumpadPeriod`
:kbd:`NumpadPlus`
:kbd:`NumpadSlash`
:kbd:`OSKey-R`
:kbd:`OSKey`
:kbd:`O`
:kbd:`P`
:kbd:`PageDown`
:kbd:`PageUp`
:kbd:`Pen`
:kbd:`Period`
:kbd:`Q`
:kbd:`R N`
:kbd:`R R`
:kbd:`R X 9 0`
:kbd:`R Y Y`
:kbd:`RMB`
:kbd:`R`
:kbd:`Return`
:kbd:`Right`
:kbd:`S 2`
:kbd:`S Period 5`
:kbd:`S X 0`
:kbd:`S Y 0`
:kbd:`S`
:kbd:`Shift-'`
:kbd:`Shift-0`
:kbd:`Shift-9`
:kbd:`Shift-;`
:kbd:`Shift-=`
:kbd:`Shift-A`
:kbd:`Shift-AccentGrave`
:kbd:`Shift-Alt-0`
:kbd:`Shift-Alt-8`
:kbd:`Shift-Alt-9`
:kbd:`Shift-Alt-=`
:kbd:`Shift-Alt-A`
:kbd:`Shift-Alt-Comma`
:kbd:`Shift-Alt-D`
:kbd:`Shift-Alt-G`
:kbd:`Shift-Alt-I`
:kbd:`Shift-Alt-LMB`
:kbd:`Shift-Alt-L`
:kbd:`Shift-Alt-Left`
:kbd:`Shift-Alt-O`
:kbd:`Shift-Alt-Period`
:kbd:`Shift-Alt-R`
:kbd:`Shift-Alt-Right`
:kbd:`Shift-Alt-S`
:kbd:`Shift-Alt-T`
:kbd:`Shift-Alt-Wheel`
:kbd:`Shift-Alt`
:kbd:`Shift-B`
:kbd:`Shift-Backspace`
:kbd:`Shift-C`
:kbd:`Shift-Ctrl-8`
:kbd:`Shift-Ctrl-=`
:kbd:`Shift-Ctrl-A`
:kbd:`Shift-Ctrl-Alt-0`
:kbd:`Shift-Ctrl-Alt-1`
:kbd:`Shift-Ctrl-Alt-8`
:kbd:`Shift-Ctrl-Alt-=`
:kbd:`Shift-Ctrl-Alt-C`
:kbd:`Shift-Ctrl-Alt-G`
:kbd:`Shift-Ctrl-Alt-I`
:kbd:`Shift-Ctrl-Alt-Left`
:kbd:`Shift-Ctrl-Alt-Right`
:kbd:`Shift-Ctrl-Alt-S`
:kbd:`Shift-Ctrl-B`
:kbd:`Shift-Ctrl-C`
:kbd:`Shift-Ctrl-Comma`
:kbd:`Shift-Ctrl-Down`
:kbd:`Shift-Ctrl-E`
:kbd:`Shift-Ctrl-End`
:kbd:`Shift-Ctrl-G`
:kbd:`Shift-Ctrl-Home`
:kbd:`Shift-Ctrl-J`
:kbd:`Shift-Ctrl-LMB`
:kbd:`Shift-Ctrl-L`
:kbd:`Shift-Ctrl-Left`
:kbd:`Shift-Ctrl-MMB`
:kbd:`Shift-Ctrl-M`
:kbd:`Shift-Ctrl-Minus`
:kbd:`Shift-Ctrl-N`
:kbd:`Shift-Ctrl-NumpadAsterisk`
:kbd:`Shift-Ctrl-NumpadMinus`
:kbd:`Shift-Ctrl-NumpadPlus`
:kbd:`Shift-Ctrl-NumpadSlash`
:kbd:`Shift-Ctrl-O`
:kbd:`Shift-Ctrl-Period`
:kbd:`Shift-Ctrl-RMB`
:kbd:`Shift-Ctrl-R`
:kbd:`Shift-Ctrl-Right`
:kbd:`Shift-Ctrl-S`
:kbd:`Shift-Ctrl-Slash`
:kbd:`Shift-Ctrl-Spacebar`
:kbd:`Shift-Ctrl-T`
:kbd:`Shift-Ctrl-Tab`
:kbd:`Shift-Ctrl-Up`
:kbd:`Shift-Ctrl-V`
:kbd:`Shift-Ctrl-W`
:kbd:`Shift-Ctrl-X`
:kbd:`Shift-Ctrl-Z`
:kbd:`Shift-Ctrl`
:kbd:`Shift-D`
:kbd:`Shift-Delete`
:kbd:`Shift-Down`
:kbd:`Shift-E`
:kbd:`Shift-End`
:kbd:`Shift-F11`
:kbd:`Shift-F12`
:kbd:`Shift-F`
:kbd:`Shift-G 1`
:kbd:`Shift-G 2`
:kbd:`Shift-G`
:kbd:`Shift-H`
:kbd:`Shift-Home`
:kbd:`Shift-I`
:kbd:`Shift-K`
:kbd:`Shift-LMB`
:kbd:`Shift-L`
:kbd:`Shift-Left`
:kbd:`Shift-MMB`
:kbd:`Shift-M`
:kbd:`Shift-N`
:kbd:`Shift-Numpad2`
:kbd:`Shift-Numpad4`
:kbd:`Shift-Numpad6`
:kbd:`Shift-Numpad8`
:kbd:`Shift-NumpadSlash`
:kbd:`Shift-O`
:kbd:`Shift-P`
:kbd:`Shift-PageDown`
:kbd:`Shift-PageUp`
:kbd:`Shift-Q`
:kbd:`Shift-RMB`
:kbd:`Shift-R`
:kbd:`Shift-Return`
:kbd:`Shift-Right`
:kbd:`Shift-S`
:kbd:`Shift-Spacebar`
:kbd:`Shift-T`
:kbd:`Shift-Tab`
:kbd:`Shift-Up`
:kbd:`Shift-V`
:kbd:`Shift-W`
:kbd:`Shift-Wheel`
:kbd:`Shift-X`
:kbd:`Shift-Y`
:kbd:`Shift-Z`
:kbd:`Shift-[`
:kbd:`Shift-]`
:kbd:`Shift`
:kbd:`Slash`
:kbd:`Spacebar D`
:kbd:`Spacebar M`
:kbd:`Spacebar T`
:kbd:`Spacebar`
:kbd:`T`
:kbd:`Tab 1`
:kbd:`Tab`
:kbd:`U`
:kbd:`Up`
:kbd:`V`
:kbd:`W`
:kbd:`WheelDown`
:kbd:`WheelUp`
:kbd:`Wheel`
:kbd:`X`
:kbd:`Y`
:kbd:`Z`
:kbd:`[`
:kbd:`]`
:math:`((420 + 180) modulo 360) - 180 = 60 - ...`
:math:`(0 + 0 + 0) / 3 = 0.0`
:math:`(1 + 0 + 0 + 0) / 4 = 0.25`
:math:`(1 + 0 + 0) / 3 = 0.333`
:math:`(1 + 0) / 2 = 0.5`
:math:`(A.x * B.x, A.y * B.y, A.z * B.z)`
:math:`(A.x / B.x, A.y / B.y, A.z / B.z)`
:math:`(radius - x)^3`
:math:`0.25`
:math:`0.5`
:math:`0.75`
:math:`0`
:math:`1.55`
:math:`100 × (1 - 0.1) × (1 - 0.43) × (1 - 0.03)`
:math:`1`
:math:`2^{steps -1}`
:math:`50 × (1.0 - 0.5) = 25`
:math:`50 × (1.0 - 0.75) = 12.5`
:math:`RandomFactor`
:math:`[0, 1]`
:math:`a`
:math:`b`
:math:`displacement = texture_value - Midlevel`
:math:`e^{-8x^2/ radius^2}`
:math:`eumelanin = Melanin*(1.0-MelaninRedness)`
:math:`pheomelanin = Melanin*MelaninRedness`
:math:`radius = sqrt(16 × v)`
:math:`randomFactor = 1.0 + 2.0*(Random - 0.5) * RandomColor`
:math:`randomFactor`
:math:`result = mix(previous, previous (+-*) value, influence)`
:math:`result = previous * (value / default) ^ {influence}`
:math:`result = previous + (value - default) * {influence}`
:math:`result = previous + value * influence`
:math:`round(x × n - 0.5) / (n - 1)`
:math:`s`
:math:`sin(2 × pi/ 4) = sin(pi/ 2) = +1.0`
:math:`sin(pi/ 2) = 1.0`
:math:`specular = ((ior - 1)/(ior + 1))^2 / 0.08`
:math:`specular = ((ior - 1)/(ior + 1))^2`
:math:`vertex_offset = displacement × Strength`
:math:`y = -0.5 + 0.6x`
:math:`y = 0.0 + 0.6x`
:math:`y = a + bx`
:math:`y`
:menuselection:`--> (Deform, ...)`
:menuselection:`--> (Locked, ...)`
:menuselection:`--> (Multiply Vertex Group by Envelope, ...)`
:menuselection:`--> Mesh --> Circle`
:menuselection:`... --> Show/Hide`
:menuselection:`3D Viewport --> Add --> Bolt`
:menuselection:`3D Viewport --> Add --> Camera`
:menuselection:`3D Viewport --> Add --> Curve --> Curve Simplify`
:menuselection:`3D Viewport --> Add --> Curve --> Sapling Tree Gen`
:menuselection:`3D Viewport --> Add --> Curve menu`
:menuselection:`3D Viewport --> Add --> Curve`
:menuselection:`3D Viewport --> Add --> Image --> Images as Planes`
:menuselection:`3D Viewport --> Add --> Light menu --> 3 Point Lights`
:menuselection:`3D Viewport --> Add --> Light menu`
:menuselection:`3D Viewport --> Add --> Lights`
:menuselection:`3D Viewport --> Add --> Mesh --> Discombobulator`
:menuselection:`3D Viewport --> Add --> Mesh --> Monkey`
:menuselection:`3D Viewport --> Add --> Mesh menu`
:menuselection:`3D Viewport --> Add --> Mesh`
:menuselection:`3D Viewport --> Add menu --> Armature`
:menuselection:`3D Viewport --> Curve Context Menu`
:menuselection:`3D Viewport --> Edit Mode Context Menu --> Relax`
:menuselection:`3D Viewport --> Object menu --> Quick Effects`
:menuselection:`3D Viewport --> Operator`
:menuselection:`3D Viewport --> Search`
:menuselection:`3D Viewport --> Sidebar --> Animate tab`
:menuselection:`3D Viewport --> Sidebar --> Blenderkit`
:menuselection:`3D Viewport --> Sidebar --> Color Palette or Weight Palette`
:menuselection:`3D Viewport --> Sidebar --> Create tab`
:menuselection:`3D Viewport --> Sidebar --> Create`
:menuselection:`3D Viewport --> Sidebar --> Edit tab`
:menuselection:`3D Viewport --> Sidebar --> Grease Pencil`
:menuselection:`3D Viewport --> Sidebar --> Item --> Camera Rig`
:menuselection:`3D Viewport --> Sidebar --> Item tab`
:menuselection:`3D Viewport --> Sidebar --> Transform`
:menuselection:`3D Viewport --> Sidebar --> VR tab`
:menuselection:`3D Viewport --> Sidebar --> View tab`
:menuselection:`3D Viewport --> Sidebar`
:menuselection:`3D Viewport --> Text`
:menuselection:`3D Viewport --> Tools --> Line Tool`
:menuselection:`3D Viewport --> Tools panel`
:menuselection:`3D Viewport --> View --> Viewport Render Animation`
:menuselection:`3D Viewport --> View --> Viewport Render Image`
:menuselection:`3D Viewport --> View --> Viewport Render Keyframes`
:menuselection:`3D Viewport --> Viewport Overlays --> Curve Edit Mode`
:menuselection:`3D Viewport Edit Mode --> Sidebar --> Edit tab`
:menuselection:`3D Viewport Edit Mode --> context menu`
:menuselection:`3D Viewport Header --> Select Mode`
:menuselection:`3D Viewport Object/Edit Modes --> context menu`
:menuselection:`3D Viewport Pose Mode --> Sidebar --> Create tab`
:menuselection:`Add --> Action Strip`
:menuselection:`Add --> Add Meta-Strips`
:menuselection:`Add --> Armature --> Single Bone`
:menuselection:`Add --> Armature`
:menuselection:`Add --> Camera --> Dolly Camera Rig, Crane Camera Rig or 2D Camera Rig`
:menuselection:`Add --> Camera`
:menuselection:`Add --> Collection Instance`
:menuselection:`Add --> Curve`
:menuselection:`Add --> Distort --> Scale`
:menuselection:`Add --> Effect --> Speed Control`
:menuselection:`Add --> Fades`
:menuselection:`Add --> Force Field`
:menuselection:`Add --> Grease Pencil`
:menuselection:`Add --> Group`
:menuselection:`Add --> Input --> Texture`
:menuselection:`Add --> Input`
:menuselection:`Add --> Mesh`
:menuselection:`Add --> Metaball`
:menuselection:`Add --> Node`
:menuselection:`Add --> Remove Meta-Strips`
:menuselection:`Add --> Sound Clip`
:menuselection:`Add --> Text`
:menuselection:`Add --> Texture`
:menuselection:`Add --> Transition`
:menuselection:`Add`
:menuselection:`Adjust --> Compositing --> Opacity`
:menuselection:`Animation --> Group by NLA Track`
:menuselection:`Applications --> Utilities`
:menuselection:`Apply --> Apply Pose As Rest Pose`
:menuselection:`Armature --> Bone Roll --> Recalculate`
:menuselection:`Armature --> Bone Roll --> Set`
:menuselection:`Armature --> Bone Settings --> ...`
:menuselection:`Armature --> Bone Settings --> Disable a Setting`
:menuselection:`Armature --> Bone Settings --> Enable a Setting`
:menuselection:`Armature --> Bone Settings --> Toggle a Setting`
:menuselection:`Armature --> Change Armature Layers`
:menuselection:`Armature --> Change Bone Layers`
:menuselection:`Armature --> Custom Properties`
:menuselection:`Armature --> Delete --> Bones`
:menuselection:`Armature --> Delete --> Dissolve`
:menuselection:`Armature --> Duplicate`
:menuselection:`Armature --> Extrude`
:menuselection:`Armature --> Fill Between Joints`
:menuselection:`Armature --> Inverse Kinematics`
:menuselection:`Armature --> Motion Paths`
:menuselection:`Armature --> Move Bone To Layer`
:menuselection:`Armature --> Names --> AutoName Left/Right, Front/Back, Top/Bottom`
:menuselection:`Armature --> Names --> Flip Names`
:menuselection:`Armature --> Names`
:menuselection:`Armature --> Parent --> Clear Parent...`
:menuselection:`Armature --> Parent --> Make Parent...`
:menuselection:`Armature --> Parent`
:menuselection:`Armature --> Separate Bones`
:menuselection:`Armature --> Separate`
:menuselection:`Armature --> Skeleton`
:menuselection:`Armature --> Split`
:menuselection:`Armature --> Subdivide`
:menuselection:`Armature --> Switch Direction`
:menuselection:`Armature --> Symmetrize`
:menuselection:`Armature --> Transform --> Align Bones`
:menuselection:`Armature --> Transform --> Scale Envelope Distance`
:menuselection:`Armature --> Transform --> Scale Radius`
:menuselection:`Armature --> Viewport Display`
:menuselection:`Armature tab --> Display panel`
:menuselection:`Bone --> Bendy Bones`
:menuselection:`Bone --> Custom Properties`
:menuselection:`Bone --> Deform`
:menuselection:`Bone --> Inverse Kinematics`
:menuselection:`Bone --> Relations`
:menuselection:`Bone --> Transform`
:menuselection:`Bone --> Viewport Display`
:menuselection:`Bone tab --> Viewport Display panel`
:menuselection:`Camera --> Viewport Display`
:menuselection:`Channel --> Extrapolation Mode`
:menuselection:`Clip --> Proxy --> Rebuild Proxy and Timecode indices`
:menuselection:`Clip Editor --> Tools --> Solve --> Refine Solution`
:menuselection:`Clone --> Download ZIP`
:menuselection:`Collapse Edges & Faces`
:menuselection:`Context Menu --> Laplacian Smooth`
:menuselection:`Context Menu --> Merge by Distance`
:menuselection:`Context Menu --> Merge`
:menuselection:`Context Menu --> Relax`
:menuselection:`Context Menu --> Set Goal Weight`
:menuselection:`Context Menu --> Smooth`
:menuselection:`Context Menu --> Subdivide`
:menuselection:`Context menu --> Add All/Single to Keying Set`
:menuselection:`Context menu --> Add Driver`
:menuselection:`Context menu --> Copy As New Driver`
:menuselection:`Context menu --> Copy Driver`
:menuselection:`Context menu --> Delete Driver(s)`
:menuselection:`Context menu --> Delete Single Driver`
:menuselection:`Context menu --> Edit Driver`
:menuselection:`Context menu --> ID Data --> Make Local`
:menuselection:`Context menu --> Online Manual`
:menuselection:`Context menu --> Open Drivers Editor`
:menuselection:`Context menu --> Paste Driver`
:menuselection:`Control Points --> Clear Tilt`
:menuselection:`Control Points --> Tilt`
:menuselection:`Curve --> Add Duplicate`
:menuselection:`Curve --> Clean Up --> Decimate Curve`
:menuselection:`Curve --> Control Points --> Hooks`
:menuselection:`Curve --> Control Points --> Make Vertex Parent`
:menuselection:`Curve --> Control Points --> Recalculate Handles`
:menuselection:`Curve --> Control Points --> Set Handle Type`
:menuselection:`Curve --> Control Points --> Smooth Curve Radius`
:menuselection:`Curve --> Control Points --> Smooth Curve Tilt`
:menuselection:`Curve --> Control Points --> Smooth Curve Weight`
:menuselection:`Curve --> Control Points --> Smooth`
:menuselection:`Curve --> Delete...`
:menuselection:`Curve --> Extrude Curve and Move`
:menuselection:`Curve --> Make Segment`
:menuselection:`Curve --> Mirror`
:menuselection:`Curve --> Segments --> Subdivide`
:menuselection:`Curve --> Segments --> Switch Direction`
:menuselection:`Curve --> Separate`
:menuselection:`Curve --> Set Spline Type`
:menuselection:`Curve --> Show/Hide`
:menuselection:`Curve --> Snap`
:menuselection:`Curve --> Spin`
:menuselection:`Curve --> Split`
:menuselection:`Curve --> Toggle Cyclic`
:menuselection:`Curve --> Transform --> Radius`
:menuselection:`Curve --> Transform`
:menuselection:`Display & Shading --> Viewport Overlays --> Normals`
:menuselection:`Display & Shading Menu --> Viewport Overlay --> Developer --> Indices`
:menuselection:`Dope Sheet and Graph editors --> Channel --> Simplify F-Curves`
:menuselection:`Drawing Planes`
:menuselection:`Edge --> Bevel Edges`
:menuselection:`Edge --> Bridge Edge Loops`
:menuselection:`Edge --> Edge Bevel Weight`
:menuselection:`Edge --> Edge Crease`
:menuselection:`Edge --> Edge Slide`
:menuselection:`Edge --> Extrude Edges`
:menuselection:`Edge --> Loop Cut and Slide`
:menuselection:`Edge --> Mark Freestyle Edge`
:menuselection:`Edge --> Mark Seam/Clear Seam`
:menuselection:`Edge --> Mark Sharp/Clear Sharp`
:menuselection:`Edge --> Mark/Clear Seam`
:menuselection:`Edge --> Offset Edge Slide`
:menuselection:`Edge --> Rotate Edge CW / Rotate Edge CCW`
:menuselection:`Edge --> Screw`
:menuselection:`Edge --> Subdivide Edge-Ring`
:menuselection:`Edge --> Subdivide`
:menuselection:`Edge --> Un-Subdivide`
:menuselection:`Edge Loops`
:menuselection:`Edit --> Adjust Last Operation...`
:menuselection:`Edit --> Batch Rename`
:menuselection:`Edit --> Duplicate`
:menuselection:`Edit --> Interface --> Translation`
:menuselection:`Edit --> Linked Duplicate`
:menuselection:`Edit --> Make Single User`
:menuselection:`Edit --> Menu Search`
:menuselection:`Edit --> Operator Search`
:menuselection:`Edit --> Preferences...`
:menuselection:`Edit --> Redo`
:menuselection:`Edit --> Remove Empty Animation Data`
:menuselection:`Edit --> Rename Active Item`
:menuselection:`Edit --> Repeat History...`
:menuselection:`Edit --> Repeat Last`
:menuselection:`Edit --> Start Editing Stashed Action`
:menuselection:`Edit --> Start Tweaking Strips Action`
:menuselection:`Edit --> Text to 3D Object`
:menuselection:`Edit --> Tweaking Strips Action`
:menuselection:`Edit --> Undo History`
:menuselection:`Edit --> Undo`
:menuselection:`Face --> Beautify Faces`
:menuselection:`Face --> Face Data --> Rotate UVs/Reverse UVs`
:menuselection:`Face --> Fill`
:menuselection:`Face --> Grid Fill`
:menuselection:`Face --> Inset Faces`
:menuselection:`Face --> Intersect (Boolean)`
:menuselection:`Face --> Intersect (Knife)`
:menuselection:`Face --> Reverse UVs`
:menuselection:`Face --> Rotate UVs`
:menuselection:`Face --> Shade Flat`
:menuselection:`Face --> Shade Smooth`
:menuselection:`Face --> Solidify Faces`
:menuselection:`Face --> Triangles to Quads`
:menuselection:`Face --> Triangulate Faces`
:menuselection:`Face --> Weld Edges into Faces`
:menuselection:`Face --> Wireframe`
:menuselection:`Face Data --> Mark Freestyle Face`
:menuselection:`Face Sets --> Face Set from Edit Mode Selection`
:menuselection:`Face Sets --> Face Set from Masked`
:menuselection:`Face Sets --> Face Set from Visible`
:menuselection:`Face Sets --> Grow/Shrink Face Sets`
:menuselection:`Face Sets --> Init Face Sets`
:menuselection:`Face Sets --> Invert Visible Face Sets`
:menuselection:`Face Sets --> Randomize Colors`
:menuselection:`Face Sets --> Show All Face Sets`
:menuselection:`Faces --> Poke Faces`
:menuselection:`File --> Data Previews --> Batch Clear Previews`
:menuselection:`File --> Data Previews --> Batch Generate Previews`
:menuselection:`File --> Data Previews --> Clear Data-blocks Previews`
:menuselection:`File --> Data Previews --> Refresh Data-blocks Previews`
:menuselection:`File --> Defaults --> Load Factory Settings`
:menuselection:`File --> Defaults --> Save Startup File`
:menuselection:`File --> Defaults`
:menuselection:`File --> Demo Mode (Setup)`
:menuselection:`File --> Demo Mode (Start)`
:menuselection:`File --> Demo menu`
:menuselection:`File --> Export --> Cameras & Markers (.py)`
:menuselection:`File --> Export --> Paper Model (.pdf/.svg)`
:menuselection:`File --> Export --> Pointcache (.pc2)`
:menuselection:`File --> Export`
:menuselection:`File --> External Data --> Automatically Pack Into .blend`
:menuselection:`File --> External Data --> Pack All Into .blend`
:menuselection:`File --> External Data --> Unpack All Into Files`
:menuselection:`File --> External Data`
:menuselection:`File --> Import --> Images as Planes`
:menuselection:`File --> Import --> Scalable Vector Graphics (.svg)`
:menuselection:`File --> Import Palettes`
:menuselection:`File --> Import/Export --> AutoCAD DXF`
:menuselection:`File --> Import/Export --> FBX (.fbx)`
:menuselection:`File --> Import/Export --> Lightwave Point Cache (.mdd)`
:menuselection:`File --> Import/Export --> Motion Capture (.bvh)`
:menuselection:`File --> Import/Export --> Nuke (.chan)`
:menuselection:`File --> Import/Export --> Nuke(*.chan)`
:menuselection:`File --> Import/Export --> Stanford (.ply)`
:menuselection:`File --> Import/Export --> Stl (.stl)`
:menuselection:`File --> Import/Export --> Wavefront (.obj)`
:menuselection:`File --> Import/Export --> X3D Extensible 3D (.x3d/.wrl)`
:menuselection:`File --> Import/Export --> glTF 2.0 (.glb, .gltf)`
:menuselection:`File --> Import`
:menuselection:`File --> Link/Append Link`
:menuselection:`File --> Link/Append`
:menuselection:`File --> Link`
:menuselection:`File --> New --> 2D Animation`
:menuselection:`File --> New`
:menuselection:`File --> Open Recent`
:menuselection:`File --> Open...`
:menuselection:`File --> Recover --> Auto Save...`
:menuselection:`File --> Recover --> Last Session`
:menuselection:`File --> Save As...`
:menuselection:`File --> Save Copy...`
:menuselection:`File --> Save`
:menuselection:`Go to Parent Node Tree`
:menuselection:`Grease Pencil --> Active Layer`
:menuselection:`Grease Pencil --> Animation`
:menuselection:`Grease Pencil --> Clean Up --> Boundary Strokes, Boundary Strokes All Frames`
:menuselection:`Grease Pencil --> Clean Up --> Delete Duplicated Frames`
:menuselection:`Grease Pencil --> Clean Up --> Delete Loose Points`
:menuselection:`Grease Pencil --> Clean Up --> Merge by Distance`
:menuselection:`Grease Pencil --> Clean Up --> Reproject Strokes`
:menuselection:`Grease Pencil --> Copy`
:menuselection:`Grease Pencil --> Delete`
:menuselection:`Grease Pencil --> Duplicate`
:menuselection:`Grease Pencil --> Interpolation`
:menuselection:`Grease Pencil --> Mirror`
:menuselection:`Grease Pencil --> Paste by Layer`
:menuselection:`Grease Pencil --> Paste`
:menuselection:`Grease Pencil --> Separate Strokes`
:menuselection:`Grease Pencil --> Snap`
:menuselection:`Grease Pencil --> Split`
:menuselection:`Grease Pencil --> Transform --> Move, Rotate, Scale`
:menuselection:`Grease Pencil --> Transform`
:menuselection:`Group --> Make Group`
:menuselection:`Group --> Ungroup`
:menuselection:`Guides`
:menuselection:`Hair Info --> Random`
:menuselection:`Header --> Add menu`
:menuselection:`Header --> Overlays --> Mesh Analysis`
:menuselection:`Header --> Transform Orientations`
:menuselection:`Header --> UV`
:menuselection:`Help --> Operator Cheat Sheet`
:menuselection:`Help --> Save System Info`
:menuselection:`Image --> Open`
:menuselection:`Image --> Pack Image`
:menuselection:`Image --> Save As...`
:menuselection:`Image --> Save Image`
:menuselection:`Image Editor --> Image --> Save`
:menuselection:`Image Editor, 3D View Paint Modes --> Color Palette or Weight Palette panel`
:menuselection:`Image editor --> Sidebar --> Color Palette`
:menuselection:`Image`
:menuselection:`Include --> Custom Properties`
:menuselection:`Install...`
:menuselection:`Interface --> Display --> Python Tooltips`
:menuselection:`Key --> Add F-Curve Modifier`
:menuselection:`Key --> Bake Curve`
:menuselection:`Key --> Bake Sound to F-Curves`
:menuselection:`Key --> Clean Channels`
:menuselection:`Key --> Clean Keyframes`
:menuselection:`Key --> Copy Keyframes`
:menuselection:`Key --> Decimate (Allowed Change)`
:menuselection:`Key --> Decimate (Ratio)`
:menuselection:`Key --> Delete Keyframes`
:menuselection:`Key --> Duplicate`
:menuselection:`Key --> Easing Mode`
:menuselection:`Key --> Easing Type`
:menuselection:`Key --> Handle Type`
:menuselection:`Key --> Insert Keyframes`
:menuselection:`Key --> Interpolation Mode`
:menuselection:`Key --> Jump to keyframes`
:menuselection:`Key --> Keyframe Type`
:menuselection:`Key --> Mirror`
:menuselection:`Key --> Paste Keyframes`
:menuselection:`Key --> Sample Keyframes`
:menuselection:`Key --> Smooth Keys`
:menuselection:`Key --> Snap`
:menuselection:`Key --> Transform`
:menuselection:`Marker --> Add Marker`
:menuselection:`Marker --> Bind Camera to Markers`
:menuselection:`Marker --> Delete Marker`
:menuselection:`Marker --> Duplicate Marker to Scene...`
:menuselection:`Marker --> Duplicate Marker`
:menuselection:`Marker --> Jump to Next/Previous Marker`
:menuselection:`Marker --> Make Markers Local`
:menuselection:`Marker --> Move Marker`
:menuselection:`Marker --> Rename Marker`
:menuselection:`Marker --> Show Pose Markers`
:menuselection:`Mask --> Animation`
:menuselection:`Mask --> Box Mask`
:menuselection:`Mask --> Clear Feather Weight`
:menuselection:`Mask --> Delete`
:menuselection:`Mask --> Dirty Mask`
:menuselection:`Mask --> Expand Mask by Curvature`
:menuselection:`Mask --> Expand Mask by Topology`
:menuselection:`Mask --> Invert Mask`
:menuselection:`Mask --> Lasso Mask`
:menuselection:`Mask --> Mask Extract`
:menuselection:`Mask --> Mask Filters`
:menuselection:`Mask --> Mask Slice`
:menuselection:`Mask --> Recalculate Handles`
:menuselection:`Mask --> Set Handle Type`
:menuselection:`Mask --> Show/Hide`
:menuselection:`Mask --> Switch Direction`
:menuselection:`Mask --> Toggle Cyclic`
:menuselection:`Mask --> Transform`
:menuselection:`Mask`
:menuselection:`Material --> Material Slots`
:menuselection:`Material --> Settings --> Displacement`
:menuselection:`Material --> Settings --> Pass Index`
:menuselection:`Material --> Settings`
:menuselection:`Material Properties --> Settings`
:menuselection:`Menu Search --> Pick Shortest Path`
:menuselection:`Mesh --> Bisect`
:menuselection:`Mesh --> Clean up --> Decimate Geometry`
:menuselection:`Mesh --> Clean up --> Degenerate Dissolve`
:menuselection:`Mesh --> Clean up --> Delete Loose`
:menuselection:`Mesh --> Clean up --> Fill Holes`
:menuselection:`Mesh --> Clean up --> Make Planar Faces`
:menuselection:`Mesh --> Clean up --> Split Concave Faces`
:menuselection:`Mesh --> Clean up --> Split Non-Planar Faces`
:menuselection:`Mesh --> Convex Hull`
:menuselection:`Mesh --> Cursor --> Selection`
:menuselection:`Mesh --> Delete --> Collapse Edges & Faces`
:menuselection:`Mesh --> Delete --> Dissolve Edges`
:menuselection:`Mesh --> Delete --> Dissolve Faces`
:menuselection:`Mesh --> Delete --> Dissolve Vertices`
:menuselection:`Mesh --> Delete --> Edge Loops`
:menuselection:`Mesh --> Delete --> Limited Dissolve`
:menuselection:`Mesh --> Delete`
:menuselection:`Mesh --> Duplicate`
:menuselection:`Mesh --> Extrude --> Extrude Faces Along Normals`
:menuselection:`Mesh --> Extrude --> Extrude Manifold`
:menuselection:`Mesh --> Extrude --> Extrude Repeat`
:menuselection:`Mesh --> Extrude --> Individual Faces`
:menuselection:`Mesh --> Extrude`
:menuselection:`Mesh --> Face --> Extrude Faces`
:menuselection:`Mesh --> Knife Project`
:menuselection:`Mesh --> Merge`
:menuselection:`Mesh --> Mirror`
:menuselection:`Mesh --> Normals --> Average`
:menuselection:`Mesh --> Normals --> Copy Vectors`
:menuselection:`Mesh --> Normals --> Flip`
:menuselection:`Mesh --> Normals --> Merge`
:menuselection:`Mesh --> Normals --> Paste Vectors`
:menuselection:`Mesh --> Normals --> Point to Target`
:menuselection:`Mesh --> Normals --> Recalculate Inside`
:menuselection:`Mesh --> Normals --> Recalculate Outside`
:menuselection:`Mesh --> Normals --> Reset Vectors`
:menuselection:`Mesh --> Normals --> Rotate`
:menuselection:`Mesh --> Normals --> Select by Face Strength`
:menuselection:`Mesh --> Normals --> Set Face Strength`
:menuselection:`Mesh --> Normals --> Set from Faces`
:menuselection:`Mesh --> Normals --> Smooth Vectors`
:menuselection:`Mesh --> Normals --> Split`
:menuselection:`Mesh --> Normals`
:menuselection:`Mesh --> Separate`
:menuselection:`Mesh --> Shading`
:menuselection:`Mesh --> Snap to Symmetry`
:menuselection:`Mesh --> Snap`
:menuselection:`Mesh --> Sort Elements...`
:menuselection:`Mesh --> Split --> Faces & Edges by Vertices`
:menuselection:`Mesh --> Split --> Faces by Edges`
:menuselection:`Mesh --> Split --> Selection`
:menuselection:`Mesh --> Split`
:menuselection:`Mesh --> Symmetrize`
:menuselection:`Mesh --> Transform --> Move, Rotate, Scale`
:menuselection:`Mesh --> Transform --> Randomize`
:menuselection:`Mesh --> Transform --> Shrink Fatten`
:menuselection:`Mesh --> Transform --> Skin Resize`
:menuselection:`Mesh --> Transform --> To Sphere`
:menuselection:`Mesh --> Unfold`
:menuselection:`Mesh --> Vertices --> Relax`
:menuselection:`Mesh data --> Vertex and face numbers`
:menuselection:`Metaball tab --> Active Element panel --> Type`
:menuselection:`Modifier --> Subdivision Surface`
:menuselection:`Movie Clip Editor --> Properties --> Lens`
:menuselection:`Movie Clip Editor --> Properties --> Stabilization --> 2D Stabilization --> Interpolate`
:menuselection:`Movie Clip Editor --> Properties --> Stabilization --> 2D Stabilization`
:menuselection:`Movie Clip Editor --> Sidebar region --> Objects`
:menuselection:`Movie Clip Editor --> Toolbar --> Solve --> Solve Camera Motion`
:menuselection:`Node --> Copy`
:menuselection:`Node --> Cut Links`
:menuselection:`Node --> Duplicate`
:menuselection:`Node --> Edit Group`
:menuselection:`Node --> Group Insert`
:menuselection:`Node --> Join in new Frame`
:menuselection:`Node --> Make Group`
:menuselection:`Node --> Move, Rotate, Resize`
:menuselection:`Node --> Paste`
:menuselection:`Node --> Remove from Frame`
:menuselection:`Node --> Toggle Node Mute`
:menuselection:`Object --> Animation --> Bake Mesh to Grease Pencil...`
:menuselection:`Object --> Animation --> Clear Keyframes...`
:menuselection:`Object --> Animation --> Delete Keyframes...`
:menuselection:`Object --> Animation --> Insert Keyframe...`
:menuselection:`Object --> Apply --> Location / Rotation / Scale / Rotation & Scale`
:menuselection:`Object --> Apply --> Location / Rotation / Scale to Deltas`
:menuselection:`Object --> Apply --> Make Instances Real`
:menuselection:`Object --> Apply --> Visual Geometry to Mesh`
:menuselection:`Object --> Apply --> Visual Transform`
:menuselection:`Object --> Clean Up --> Clean Vertex Group Weights`
:menuselection:`Object --> Clean Up --> Limit Total Vertex Groups`
:menuselection:`Object --> Clean Up --> Remove Unused Material Slots`
:menuselection:`Object --> Clear --> Location / Scale / Rotation / Origin`
:menuselection:`Object --> Clear --> Origin`
:menuselection:`Object --> Collection`
:menuselection:`Object --> Constraint --> Add Constraint (with Targets)`
:menuselection:`Object --> Constraint --> Clear Object Constraints`
:menuselection:`Object --> Constraint --> Copy Constraints to Selected Objects`
:menuselection:`Object --> Convert To --> Curve`
:menuselection:`Object --> Convert To --> Mesh`
:menuselection:`Object --> Convert To --> Path, Bézier Curve, Polygon Curve`
:menuselection:`Object --> Convert to --> Grease Pencil from Curve/Mesh`
:menuselection:`Object --> Delete Globally`
:menuselection:`Object --> Delete`
:menuselection:`Object --> Duplicate Linked`
:menuselection:`Object --> Duplicate Objects`
:menuselection:`Object --> Join Objects`
:menuselection:`Object --> Join`
:menuselection:`Object --> Make Links`
:menuselection:`Object --> Parent --> Object`
:menuselection:`Object --> Parent`
:menuselection:`Object --> Quick Effects`
:menuselection:`Object --> Relations --> Make Library Overrides...`
:menuselection:`Object --> Relations --> Make Local...`
:menuselection:`Object --> Relations --> Make Proxy...`
:menuselection:`Object --> Relations --> Make Single User`
:menuselection:`Object --> Relations --> Transfer Mesh Data Layout`
:menuselection:`Object --> Relations --> Transfer Mesh Data`
:menuselection:`Object --> Rigid Body`
:menuselection:`Object --> Set Origin`
:menuselection:`Object --> Shade Flat`
:menuselection:`Object --> Shade Smooth`
:menuselection:`Object --> Show/Hide`
:menuselection:`Object --> Snap`
:menuselection:`Object --> Track`
:menuselection:`Object --> Transform --> Align Objects`
:menuselection:`Object --> Transform --> Align to Transform Orientation`
:menuselection:`Object --> Transform --> Move/Scale Texture Space`
:menuselection:`Object --> Transform --> Randomize Transform`
:menuselection:`Object --> Transform --> Scale/Move Texture Space`
:menuselection:`Object -> Collection`
:menuselection:`Object Data --> Custom Parallax`
:menuselection:`Object Data --> Probe`
:menuselection:`Object Data --> Shape Keys`
:menuselection:`Object Data --> Viewport Display`
:menuselection:`Object Data tab --> Layers`
:menuselection:`Object Data tab --> Vertex Groups`
:menuselection:`Object Properties --> Visibility`
:menuselection:`Object menu --> Make Links... --> Transfer UV Layouts`
:menuselection:`Object tab --> Collections panel`
:menuselection:`Object tab --> Collections`
:menuselection:`Object/Mesh --> Mirror`
:menuselection:`Object/Mesh --> Transform --> Push/Pull`
:menuselection:`Object/Mesh/Curve/Surface --> Transform --> Bend`
:menuselection:`Object/Mesh/Curve/Surface --> Transform --> Move`
:menuselection:`Object/Mesh/Curve/Surface --> Transform --> Rotate`
:menuselection:`Object/Mesh/Curve/Surface --> Transform --> Scale`
:menuselection:`Object/Mesh/Curve/Surface --> Transform --> Shear`
:menuselection:`Object/Mesh/Curve/Surface --> Transform --> Warp`
:menuselection:`Object/Object type --> Snap`
:menuselection:`Object/Pose --> Animation --> Bake Action...`
:menuselection:`Object/Pose --> Parent --> Armature Deform`
:menuselection:`Paint Mask`
:menuselection:`Paint`
:menuselection:`Particle --> Mirror`
:menuselection:`Particle --> Rekey`
:menuselection:`Particle --> Show/Hide`
:menuselection:`Particle --> Subdivide`
:menuselection:`Particle --> Unify Length`
:menuselection:`Particle System --> Cache`
:menuselection:`Particle System --> Children --> Clumping`
:menuselection:`Particle System --> Children --> Kink`
:menuselection:`Particle System --> Children --> Roughness`
:menuselection:`Particle System --> Children`
:menuselection:`Particle System --> Display`
:menuselection:`Particle System --> Emission --> Source`
:menuselection:`Particle System --> Emission`
:menuselection:`Particle System --> Field Weights`
:menuselection:`Particle System --> Force Fields Settings`
:menuselection:`Particle System --> Hair Dynamics --> Structure`
:menuselection:`Particle System --> Hair Dynamics --> Volume`
:menuselection:`Particle System --> Hair Dynamics`
:menuselection:`Particle System --> Hair Shape`
:menuselection:`Particle System --> Particle System`
:menuselection:`Particle System --> Physics --> Advanced`
:menuselection:`Particle System --> Physics --> Battle`
:menuselection:`Particle System --> Physics --> Boid Brain`
:menuselection:`Particle System --> Physics --> Deflection`
:menuselection:`Particle System --> Physics --> Forces`
:menuselection:`Particle System --> Physics --> Integration`
:menuselection:`Particle System --> Physics --> Misc`
:menuselection:`Particle System --> Physics --> Movement`
:menuselection:`Particle System --> Physics --> Relations`
:menuselection:`Particle System --> Physics --> Springs`
:menuselection:`Particle System --> Physics`
:menuselection:`Particle System --> Render --> Collection --> Use Count`
:menuselection:`Particle System --> Render --> Collection`
:menuselection:`Particle System --> Render --> Extra`
:menuselection:`Particle System --> Render --> Object`
:menuselection:`Particle System --> Render --> Timing`
:menuselection:`Particle System --> Render`
:menuselection:`Particle System --> Rotation --> Angular Velocity`
:menuselection:`Particle System --> Rotation`
:menuselection:`Particle System --> Velocity`
:menuselection:`Particle System --> Vertex Groups`
:menuselection:`Particle System --> Viewport Display`
:menuselection:`Physics --> Cloth --> Collision`
:menuselection:`Physics --> Cloth --> Field Weights`
:menuselection:`Physics --> Cloth --> Physical Properties`
:menuselection:`Physics --> Cloth --> Property Weights`
:menuselection:`Physics --> Cloth --> Shape`
:menuselection:`Physics --> Cloth Cache`
:menuselection:`Physics --> Cloth`
:menuselection:`Physics --> Collision`
:menuselection:`Physics --> Dynamic Paint --> Cache`
:menuselection:`Physics --> Dynamic Paint --> Effects`
:menuselection:`Physics --> Dynamic Paint --> Initial Color`
:menuselection:`Physics --> Dynamic Paint --> Output`
:menuselection:`Physics --> Dynamic Paint --> Source`
:menuselection:`Physics --> Dynamic Paint --> Surface`
:menuselection:`Physics --> Dynamic Paint --> Velocity`
:menuselection:`Physics --> Dynamic Paint --> Waves`
:menuselection:`Physics --> Dynamic Paint`
:menuselection:`Physics --> Fluid --> Adaptive Domain`
:menuselection:`Physics --> Fluid --> Cache`
:menuselection:`Physics --> Fluid --> Diffusion`
:menuselection:`Physics --> Fluid --> Guides`
:menuselection:`Physics --> Fluid --> Noise`
:menuselection:`Physics --> Fluid --> Settings --> Border Collisions`
:menuselection:`Physics --> Fluid --> Settings --> Fire`
:menuselection:`Physics --> Fluid --> Settings --> Liquid`
:menuselection:`Physics --> Fluid --> Settings --> Smoke`
:menuselection:`Physics --> Fluid --> Settings --> Texture`
:menuselection:`Physics --> Fluid --> Settings`
:menuselection:`Physics --> Force Field`
:menuselection:`Physics --> Force Fields`
:menuselection:`Physics --> Rigid Body --> Collisions`
:menuselection:`Physics --> Rigid Body --> Dynamics`
:menuselection:`Physics --> Rigid Body --> Settings`
:menuselection:`Physics --> Rigid Body Constraint`
:menuselection:`Physics --> Rigid Body`
:menuselection:`Physics --> Soft Body --> Cache`
:menuselection:`Physics --> Soft Body --> Edges`
:menuselection:`Physics --> Soft Body --> Field Weights`
:menuselection:`Physics --> Soft Body --> Goal`
:menuselection:`Physics --> Soft Body --> Self Collision`
:menuselection:`Physics --> Soft Body --> Solver`
:menuselection:`Physics --> Soft Body`
:menuselection:`Pivot Point --> 3D Cursor`
:menuselection:`Pivot Point --> Active Element`
:menuselection:`Pivot Point --> Bounding Box Center`
:menuselection:`Pivot Point --> Individual Origins`
:menuselection:`Pivot Point --> Median Point`
:menuselection:`Pivot Point`
:menuselection:`Point --> Extrude Points`
:menuselection:`Point --> Merge Points`
:menuselection:`Point --> Smooth Points`
:menuselection:`Pose --> Apply`
:menuselection:`Pose --> Bone Groups --> ...`
:menuselection:`Pose --> Bone Groups`
:menuselection:`Pose --> Clear Transform`
:menuselection:`Pose --> Copy Pose`
:menuselection:`Pose --> Flip Quats`
:menuselection:`Pose --> In-Betweens --> Pose Breakdowner`
:menuselection:`Pose --> In-Betweens --> Push Pose from Breakdown`
:menuselection:`Pose --> In-Betweens --> Push Pose from Rest Pose`
:menuselection:`Pose --> In-Betweens --> Relax Pose to Breakdown`
:menuselection:`Pose --> In-Betweens --> Relax Pose to Rest Pose`
:menuselection:`Pose --> Motion Paths`
:menuselection:`Pose --> Move Bone To Layer`
:menuselection:`Pose --> Paste Pose Flipped`
:menuselection:`Pose --> Paste Pose`
:menuselection:`Pose --> Pose Library --> Add Pose`
:menuselection:`Pose --> Pose Library --> Browse Poses`
:menuselection:`Pose --> Pose Library --> Remove Pose`
:menuselection:`Pose --> Pose Library --> Rename Pose`
:menuselection:`Pose --> Pose Library`
:menuselection:`Pose --> Propagate`
:menuselection:`Pose --> Scale Envelope Distance`
:menuselection:`Pose --> Transform`
:menuselection:`Preferences --> Add-on tab`
:menuselection:`Preferences --> Add-ons --> Install...`
:menuselection:`Preferences --> Add-ons --> Render --> Freestyle SVG Exporter`
:menuselection:`Preferences --> File Paths`
:menuselection:`Preferences --> Input --> Emulate 3 Button Mouse`
:menuselection:`Preferences --> Input --> Keyboard --> Emulate Numpad`
:menuselection:`Preferences --> Input --> Mouse --> Emulate 3 Button Mouse`
:menuselection:`Preferences --> Interface --> Display`
:menuselection:`Preferences --> Keymaps --> Spacebar Action`
:menuselection:`Preferences --> Save & Load --> Auto Run Python Scripts`
:menuselection:`Preferences --> Save & Load --> Blender Files`
:menuselection:`Preferences --> System --> Compute Device Panel`
:menuselection:`Preferences --> System --> Cycles Render Devices`
:menuselection:`Preferences --> System --> Memory & Limits --> Undo Steps`
:menuselection:`Preferences --> System --> Memory & Limits`
:menuselection:`Preferences --> Viewport --> Selection`
:menuselection:`Preferences --> Viewport`
:menuselection:`Properties --> Armature --> Bone Groups`
:menuselection:`Properties --> Armature --> Inverse Kinematics`
:menuselection:`Properties --> Armature --> Motion Paths`
:menuselection:`Properties --> Armature --> Selection Sets`
:menuselection:`Properties --> Armature --> Viewport Display`
:menuselection:`Properties --> Armature tab`
:menuselection:`Properties --> Armature, Bone`
:menuselection:`Properties --> Bone --> Deform --> Envelope --> Distance`
:menuselection:`Properties --> Bone --> Deform --> Radius Section`
:menuselection:`Properties --> Bone --> Deform Panel`
:menuselection:`Properties --> Bone --> Inverse Kinematics`
:menuselection:`Properties --> Bone --> Viewport Display`
:menuselection:`Properties --> Bone Properties`
:menuselection:`Properties --> Bone`
:menuselection:`Properties --> Bones --> Relations`
:menuselection:`Properties --> Camera --> Depth of Field`
:menuselection:`Properties --> Camera`
:menuselection:`Properties --> Compatibility`
:menuselection:`Properties --> Constraint tab`
:menuselection:`Properties --> Curve --> Active Spline`
:menuselection:`Properties --> Font --> Font`
:menuselection:`Properties --> Font --> Geometry`
:menuselection:`Properties --> Font --> Paragraph`
:menuselection:`Properties --> Font --> Text Boxes`
:menuselection:`Properties --> Light tab`
:menuselection:`Properties --> Light`
:menuselection:`Properties --> Material --> Freestyle Line`
:menuselection:`Properties --> Material --> Settings`
:menuselection:`Properties --> Material --> Viewport Display`
:menuselection:`Properties --> Material`
:menuselection:`Properties --> Materials --> Material Library VX`
:menuselection:`Properties --> Materials --> Specials`
:menuselection:`Properties --> Materials`
:menuselection:`Properties --> Mesh --> Paper Model Islands`
:menuselection:`Properties --> Mesh tab --> Shape Keys`
:menuselection:`Properties --> Metaball --> Active Element`
:menuselection:`Properties --> Metaball`
:menuselection:`Properties --> Modifiers tab --> Armature Modifier --> Header`
:menuselection:`Properties --> Modifiers`
:menuselection:`Properties --> Object --> Viewport Display`
:menuselection:`Properties --> Object Buttons`
:menuselection:`Properties --> Object Data --> Empty`
:menuselection:`Properties --> Object Data --> Geometry Data --> Clear Sculpt-Mask Data`
:menuselection:`Properties --> Object Data --> Normals`
:menuselection:`Properties --> Object Data --> Remesh`
:menuselection:`Properties --> Object Data --> Shape Keys Specials`
:menuselection:`Properties --> Object Data --> Texture Space`
:menuselection:`Properties --> Object Properties --> Instancing --> Collection`
:menuselection:`Properties --> Object Properties --> Instancing`
:menuselection:`Properties --> Object Properties --> Motion Blur`
:menuselection:`Properties --> Object Properties --> Motion Paths`
:menuselection:`Properties --> Object Properties --> Pose Library`
:menuselection:`Properties --> Object Properties --> Relations --> Pass Index`
:menuselection:`Properties --> Object Properties --> Relations`
:menuselection:`Properties --> Object Properties --> Shading`
:menuselection:`Properties --> Object Properties --> Transform --> Delta Transforms`
:menuselection:`Properties --> Object Properties --> Transform`
:menuselection:`Properties --> Object Properties --> Viewport Display`
:menuselection:`Properties --> Object Properties --> Visibility`
:menuselection:`Properties --> Output --> Encoding`
:menuselection:`Properties --> Output --> Output`
:menuselection:`Properties --> Output --> Post Processing`
:menuselection:`Properties --> Particles tab`
:menuselection:`Properties --> Physics -- Fluid --> Field Weights`
:menuselection:`Properties --> Physics --> Fluid --> Collections`
:menuselection:`Properties --> Physics --> Rigid Body`
:menuselection:`Properties --> Physics`
:menuselection:`Properties --> Render --> Color Management`
:menuselection:`Properties --> Render --> Device`
:menuselection:`Properties --> Render --> Film --> Transparent`
:menuselection:`Properties --> Render --> Freestyle SVG Export`
:menuselection:`Properties --> Render --> Freestyle`
:menuselection:`Properties --> Render --> Lighting`
:menuselection:`Properties --> Render --> Options`
:menuselection:`Properties --> Render --> Performance`
:menuselection:`Properties --> Render --> Sampling --> Render Samples`
:menuselection:`Properties --> Render --> Sampling`
:menuselection:`Properties --> Render --> Volumetrics`
:menuselection:`Properties --> Render tab`
:menuselection:`Properties --> Scene --> 3D-Coat Settings`
:menuselection:`Properties --> Scene --> Audio`
:menuselection:`Properties --> Scene --> Blend Info panel`
:menuselection:`Properties --> Scene --> Gravity`
:menuselection:`Properties --> Scene --> Keying Sets + Active Keying Set`
:menuselection:`Properties --> Scene --> Keying Sets`
:menuselection:`Properties --> Scene --> Python Console Menu`
:menuselection:`Properties --> Scene --> Rigid Body World`
:menuselection:`Properties --> Scene --> Scene`
:menuselection:`Properties --> Scene --> Units`
:menuselection:`Properties --> Scene --> View Layer`
:menuselection:`Properties --> Text --> Shape`
:menuselection:`Properties --> View Layer --> Freestyle Line Set`
:menuselection:`Properties --> View Layer --> Freestyle Line Style`
:menuselection:`Properties --> View Layer --> Freestyle`
:menuselection:`Properties --> View Layers --> Freestyle Line Style SVG Export`
:menuselection:`Properties --> View Layers`
:menuselection:`Properties --> Visual Effects`
:menuselection:`Properties --> World --> Sun Position panel`
:menuselection:`Properties --> World --> Viewport Display`
:menuselection:`Properties --> World tab`
:menuselection:`Proportional Editing`
:menuselection:`Python Console --> Header --> Icon Viewer`
:menuselection:`Recalculate Roll --> Global +Y Axis`
:menuselection:`Recalculate Roll --> Global -Z Axis`
:menuselection:`Render --> Ambient Occlusion`
:menuselection:`Render --> Bake`
:menuselection:`Render --> Bloom`
:menuselection:`Render --> Color`
:menuselection:`Render --> Depth of Field`
:menuselection:`Render --> Dimensions`
:menuselection:`Render --> Engine --> POV-Ray 3.7`
:menuselection:`Render --> Film`
:menuselection:`Render --> Grease Pencil`
:menuselection:`Render --> Hair`
:menuselection:`Render --> Indirect Lighting`
:menuselection:`Render --> Light Paths`
:menuselection:`Render --> Motion Blur`
:menuselection:`Render --> Performance panel`
:menuselection:`Render --> Performance`
:menuselection:`Render --> Sampling`
:menuselection:`Render --> Screen Space Reflections`
:menuselection:`Render --> Shadows`
:menuselection:`Render --> Simplify`
:menuselection:`Render --> Subdivision`
:menuselection:`Render --> Subsurface Scattering`
:menuselection:`Render --> Volumes`
:menuselection:`Render Layer --> Passes`
:menuselection:`Render Layers --> Denoising`
:menuselection:`Render`
:menuselection:`Run this program in compatibility mode`
:menuselection:`Scene --> Active Keying Set`
:menuselection:`Scene --> Gravity`
:menuselection:`Scene --> Keying Set`
:menuselection:`Scene --> Rigid Body World --> Cache`
:menuselection:`Scene --> Rigid Body World --> Field Weights`
:menuselection:`Scene --> Rigid Body World`
:menuselection:`Scene --> View Layers --> Passes`
:menuselection:`Sculpt --> Rebuild BVH`
:menuselection:`Sculpt --> Set Pivot`
:menuselection:`Sculpt`
:menuselection:`Select --> (De)select First`
:menuselection:`Select --> (De)select Last`
:menuselection:`Select --> All`
:menuselection:`Select --> Alternated`
:menuselection:`Select --> Box Select`
:menuselection:`Select --> Checker Deselect`
:menuselection:`Select --> Circle Select`
:menuselection:`Select --> Control Point Row`
:menuselection:`Select --> Edge Loop`
:menuselection:`Select --> First/Last`
:menuselection:`Select --> Flip Active`
:menuselection:`Select --> Grouped`
:menuselection:`Select --> Invert`
:menuselection:`Select --> Linked Faces`
:menuselection:`Select --> Linked UVs`
:menuselection:`Select --> Linked`
:menuselection:`Select --> Mirror Selection`
:menuselection:`Select --> Mirror`
:menuselection:`Select --> More/Less`
:menuselection:`Select --> None`
:menuselection:`Select --> Roots / Tips`
:menuselection:`Select --> Select Active Camera`
:menuselection:`Select --> Select All by Trait --> Faces by Sides`
:menuselection:`Select --> Select All by Trait --> Interior Faces`
:menuselection:`Select --> Select All by Trait --> Loose Geometry`
:menuselection:`Select --> Select All by Trait --> Non-Manifold`
:menuselection:`Select --> Select All by Trait --> Ungrouped Vertices`
:menuselection:`Select --> Select All by Type`
:menuselection:`Select --> Select Grouped`
:menuselection:`Select --> Select Linked --> Linked`
:menuselection:`Select --> Select Linked --> Shortest Path`
:menuselection:`Select --> Select Linked`
:menuselection:`Select --> Select Loops --> Edge Loops`
:menuselection:`Select --> Select Loops --> Edge Rings`
:menuselection:`Select --> Select Loops --> Select Boundary Loop`
:menuselection:`Select --> Select Loops --> Select Loop Inner-Region`
:menuselection:`Select --> Select More/Less --> Less`
:menuselection:`Select --> Select More/Less --> More`
:menuselection:`Select --> Select More/Less --> Next Active`
:menuselection:`Select --> Select More/Less --> Previous Active`
:menuselection:`Select --> Select More/Less`
:menuselection:`Select --> Select Next`
:menuselection:`Select --> Select Pattern...`
:menuselection:`Select --> Select Previous`
:menuselection:`Select --> Select Random`
:menuselection:`Select --> Select Sharp Edges`
:menuselection:`Select --> Select Similar`
:menuselection:`Select --> Side of Active`
:menuselection:`Select --> Similar --> Face Regions`
:menuselection:`Select --> Similar`
:menuselection:`Select --> Vertex Color`
:menuselection:`Shader Editor --> Sidebar --> Options`
:menuselection:`Shader Editor --> Sidebar --> Settings`
:menuselection:`Sidebar --> Animation tab`
:menuselection:`Sidebar --> Create --> Ivy Generator panel`
:menuselection:`Sidebar --> Create tab`
:menuselection:`Sidebar --> Edit tab`
:menuselection:`Sidebar --> Edited Action`
:menuselection:`Sidebar --> Image --> UDIM Tiles`
:menuselection:`Sidebar --> Item --> Properties --> Add/Remove Crypto Layer`
:menuselection:`Sidebar --> Item --> Properties`
:menuselection:`Sidebar --> Modifiers`
:menuselection:`Sidebar --> Strip --> Active Strip`
:menuselection:`Sidebar --> Tool --> Brush Settings --> Cursor`
:menuselection:`Sidebar --> Tool --> Brush Settings`
:menuselection:`Sidebar --> Tool --> Dyntopo`
:menuselection:`Sidebar --> Tool --> Options --> Auto Merge`
:menuselection:`Sidebar --> Tool --> Options --> Relative Mirror`
:menuselection:`Sidebar --> Tool --> Options --> X-Axis Mirror`
:menuselection:`Sidebar --> Tool --> Options`
:menuselection:`Sidebar --> Tool --> Pose Options --> Auto IK`
:menuselection:`Sidebar --> Tool --> Remesh`
:menuselection:`Sidebar --> Tool tab --> Options panel`
:menuselection:`Sidebar --> Tools --> Active Tool`
:menuselection:`Sidebar --> Tools --> Brushes`
:menuselection:`Sidebar --> Tools --> Tiling`
:menuselection:`Sidebar --> Transform`
:menuselection:`Sidebar --> View --> Annotations`
:menuselection:`Sidebar --> View --> Quad View`
:menuselection:`Sidebar --> View tab --> Turnaround Camera`
:menuselection:`Sidebar Region --> Tool --> Options`
:menuselection:`Sidebar Region --> Tool`
:menuselection:`Sidebar region --> Active Keyframe panel`
:menuselection:`Sidebar region --> Animations --> Action Clip`
:menuselection:`Sidebar region --> Cursor`
:menuselection:`Sidebar region --> Drivers`
:menuselection:`Sidebar region --> F-Curve --> Active F-Curve`
:menuselection:`Sidebar region --> F-Curve --> Active Keyframe`
:menuselection:`Sidebar region --> Item`
:menuselection:`Sidebar region --> Modifiers --> Modifiers`
:menuselection:`Sidebar region --> Node --> Interface`
:menuselection:`Sidebar region --> Options`
:menuselection:`Sidebar region --> Proxy & Timecode --> Cache Settings`
:menuselection:`Sidebar region --> Proxy & Timecode --> Proxy Settings`
:menuselection:`Sidebar region --> Proxy & Timecode --> Strip Proxy & Timecode`
:menuselection:`Sidebar region --> Strip --> Adjust`
:menuselection:`Sidebar region --> Strip --> Source`
:menuselection:`Sidebar region --> Strip --> Time`
:menuselection:`Sidebar region --> Tool --> Pose Options`
:menuselection:`Sidebar region --> Tool`
:menuselection:`Sidebar region --> Transform --> Edge Bevel Weight`
:menuselection:`Sidebar region --> Transform --> Edge Crease`
:menuselection:`Sidebar region --> Transform panel --> Type`
:menuselection:`Sidebar region --> Transform`
:menuselection:`Sidebar region --> Vertex Weights`
:menuselection:`Sidebar region --> View --> 3D Cursor`
:menuselection:`Sidebar region --> View`
:menuselection:`Snap --> Cursor To Selected`
:menuselection:`Snap`
:menuselection:`Snapping --> Snap to`
:menuselection:`Snapping --> Snap with`
:menuselection:`Specials --> New Shape from Mix`
:menuselection:`Strip --> Deinterlace Movies`
:menuselection:`Strip --> Delete`
:menuselection:`Strip --> Duplicate Strips`
:menuselection:`Strip --> Effect Strip --> Change Effect Type`
:menuselection:`Strip --> Effect Strip --> Reassign Inputs`
:menuselection:`Strip --> Effect Strip --> Swap Inputs`
:menuselection:`Strip --> Hold Split`
:menuselection:`Strip --> Inputs --> Change Paths/Files`
:menuselection:`Strip --> Rebuild Proxy and Timecode indices`
:menuselection:`Strip --> Separate Images`
:menuselection:`Strip --> Set Render Size`
:menuselection:`Strip --> Split`
:menuselection:`Strip --> Transform --> Clear Strips Offset`
:menuselection:`Strip --> Transform --> Insert Gaps`
:menuselection:`Strip --> Transform --> Move/Extend from Current Frame`
:menuselection:`Strip --> Transform --> Move`
:menuselection:`Strip --> Transform --> Slip Strip Contents`
:menuselection:`Strip --> Transform --> Snap Strips to the Current Frame`
:menuselection:`Strip --> Transform --> Swap Strips`
:menuselection:`Stroke --> Animation --> Delete Active Keyframe (Active Layer)`
:menuselection:`Stroke --> Animation --> Delete Active Keyframes (All Layers)`
:menuselection:`Stroke --> Animation --> Duplicate Active Keyframe (Active Layer)`
:menuselection:`Stroke --> Animation --> Duplicate Active Keyframe (All Layers)`
:menuselection:`Stroke --> Animation --> Insert Blank Keyframe (Active Layer)`
:menuselection:`Stroke --> Animation --> Insert Blank Keyframe (All Layers)`
:menuselection:`Stroke --> Animation --> Interpolate --> Interpolate`
:menuselection:`Stroke --> Animation --> Interpolate --> Sequence`
:menuselection:`Stroke --> Arrange Strokes`
:menuselection:`Stroke --> Assign Material`
:menuselection:`Stroke --> Close`
:menuselection:`Stroke --> Join --> Join, Join and Copy`
:menuselection:`Stroke --> Move to Layer`
:menuselection:`Stroke --> Reset Fill Transform`
:menuselection:`Stroke --> Scale Stroke Thickness`
:menuselection:`Stroke --> Set as Active Material`
:menuselection:`Stroke --> Simplify`
:menuselection:`Stroke --> Subdivide`
:menuselection:`Stroke --> Switch Direction`
:menuselection:`Stroke --> Toggle Caps`
:menuselection:`Stroke --> Toggle Cyclic`
:menuselection:`Stroke --> Trim`
:menuselection:`Stroke Placement`
:menuselection:`Surface --> Add Duplicate`
:menuselection:`Surface --> Cleanup`
:menuselection:`Surface --> Control Points --> Hooks`
:menuselection:`Surface --> Control Points --> Make Vertex Parent`
:menuselection:`Surface --> Control Points --> Smooth`
:menuselection:`Surface --> Delete`
:menuselection:`Surface --> Extrude Curve and Move`
:menuselection:`Surface --> Make Segment`
:menuselection:`Surface --> Segments --> Subdivide`
:menuselection:`Surface --> Segments --> Switch Direction`
:menuselection:`Surface --> Separate`
:menuselection:`Surface --> Set Spline Type`
:menuselection:`Surface --> Spin`
:menuselection:`Surface --> Split`
:menuselection:`Surface --> Toggle Cyclic`
:menuselection:`Surface --> Transform`
:menuselection:`System Settings --> Window Management --> Window Behavior --> Window Actions`
:menuselection:`Templates --> Python --> Driver Functions`
:menuselection:`Text Editor --> Dev Tab --> Icon Viewer`
:menuselection:`Text Editor --> Sidebar --> Dev tab`
:menuselection:`Text Editor --> Sidebar --> Edit Operator`
:menuselection:`Text Editor --> Sidebar --> Icon Viewer`
:menuselection:`Text Editor --> Sidebar`
:menuselection:`Text Editor --> Templates --> Open Shading Language`
:menuselection:`Text Editor --> Templates --> Python`
:menuselection:`Texture --> Influence`
:menuselection:`Timeline --> View --> Only Selected Channels`
:menuselection:`Toggle Bone Options --> Locked`
:menuselection:`Tool --> Active Tool`
:menuselection:`Tool Settings --> Brush --> Topology Rake`
:menuselection:`Tool Settings --> Brush Settings --> Cursor`
:menuselection:`Tool Settings --> Eraser`
:menuselection:`Tool Settings --> Mode`
:menuselection:`Tool Settings --> Remesh`
:menuselection:`Tool tab --> Display panel`
:menuselection:`Tool tab --> Options panel`
:menuselection:`Toolbar --> Arc`
:menuselection:`Toolbar --> Bend/Shear`
:menuselection:`Toolbar --> Blade`
:menuselection:`Toolbar --> Blob`
:menuselection:`Toolbar --> Boundary`
:menuselection:`Toolbar --> Box Trim`
:menuselection:`Toolbar --> Box`
:menuselection:`Toolbar --> Circle`
:menuselection:`Toolbar --> Clay Strips`
:menuselection:`Toolbar --> Clay Thumb`
:menuselection:`Toolbar --> Clay`
:menuselection:`Toolbar --> Cloth Filter`
:menuselection:`Toolbar --> Cloth`
:menuselection:`Toolbar --> Crease`
:menuselection:`Toolbar --> Curve`
:menuselection:`Toolbar --> Cutter`
:menuselection:`Toolbar --> Draw Face Sets`
:menuselection:`Toolbar --> Draw Sharp`
:menuselection:`Toolbar --> Draw`
:menuselection:`Toolbar --> Edit Face Set`
:menuselection:`Toolbar --> Elastic Deform`
:menuselection:`Toolbar --> Erase`
:menuselection:`Toolbar --> Extrude Manifold`
:menuselection:`Toolbar --> Extrude Region --> Extrude Along Normals`
:menuselection:`Toolbar --> Extrude Region --> Extrude Individual`
:menuselection:`Toolbar --> Extrude Region`
:menuselection:`Toolbar --> Extrude`
:menuselection:`Toolbar --> Eyedropper`
:menuselection:`Toolbar --> Fill`
:menuselection:`Toolbar --> Flatten`
:menuselection:`Toolbar --> Grab`
:menuselection:`Toolbar --> In-Betweens Tools --> Push`
:menuselection:`Toolbar --> In-Betweens Tools --> Relax`
:menuselection:`Toolbar --> Inflate`
:menuselection:`Toolbar --> Inset Faces`
:menuselection:`Toolbar --> Knife --> Bisect`
:menuselection:`Toolbar --> Knife`
:menuselection:`Toolbar --> Lasso Trim`
:menuselection:`Toolbar --> Layer`
:menuselection:`Toolbar --> Line Project`
:menuselection:`Toolbar --> Line`
:menuselection:`Toolbar --> Loop Cut`
:menuselection:`Toolbar --> Mask`
:menuselection:`Toolbar --> Measure`
:menuselection:`Toolbar --> Mesh Filter`
:menuselection:`Toolbar --> Move, Rotate, Scale, Transform`
:menuselection:`Toolbar --> Move, Rotate, Scale`
:menuselection:`Toolbar --> Move`
:menuselection:`Toolbar --> Multiplane Scrape`
:menuselection:`Toolbar --> Nudge`
:menuselection:`Toolbar --> Options`
:menuselection:`Toolbar --> Pinch`
:menuselection:`Toolbar --> Poly Build`
:menuselection:`Toolbar --> Polyline`
:menuselection:`Toolbar --> Pose`
:menuselection:`Toolbar --> Radius`
:menuselection:`Toolbar --> Relax`
:menuselection:`Toolbar --> Rip`
:menuselection:`Toolbar --> Rotate`
:menuselection:`Toolbar --> Scale --> Scale Cage`
:menuselection:`Toolbar --> Scale`
:menuselection:`Toolbar --> Scrape`
:menuselection:`Toolbar --> Shear`
:menuselection:`Toolbar --> Shrink/Fatten`
:menuselection:`Toolbar --> Shrink/Flatten --> Push/Pull`
:menuselection:`Toolbar --> Simplify`
:menuselection:`Toolbar --> Slide Relax`
:menuselection:`Toolbar --> Smooth`
:menuselection:`Toolbar --> Snake Hook`
:menuselection:`Toolbar --> Solve --> Orientation --> Set Origin`
:menuselection:`Toolbar --> Spin`
:menuselection:`Toolbar --> Thumb`
:menuselection:`Toolbar --> Tilt`
:menuselection:`Toolbar --> Tint`
:menuselection:`Toolbar --> Tool --> Symmetry`
:menuselection:`Toolbar --> Transform`
:menuselection:`Toolbar region --> In-Betweens Tools --> Breakdowner`
:menuselection:`Toolbar`
:menuselection:`Topbar --> Blender --> System --> Clean-up Space-data`
:menuselection:`Topbar --> Blender --> System --> Debug Menu`
:menuselection:`Topbar --> Blender --> System --> Memory Statistics`
:menuselection:`Topbar --> Blender --> System --> Redraw Timer`
:menuselection:`Topbar --> Blender --> System --> Reload Scripts`
:menuselection:`Topbar --> File --> Import/Export`
:menuselection:`Topbar --> File menu`
:menuselection:`Topbar --> Render --> View Animation`
:menuselection:`Topbar --> Scene`
:menuselection:`Track --> Copy Tracks`
:menuselection:`Track --> Paste Tracks`
:menuselection:`UV --> Align`
:menuselection:`UV --> Average Island Scale`
:menuselection:`UV --> Copy Mirrored UV Coordinates`
:menuselection:`UV --> Cube Projection`
:menuselection:`UV --> Cylinder Projection`
:menuselection:`UV --> Export UV Layout`
:menuselection:`UV --> Follow Active Quads`
:menuselection:`UV --> Lightmap Pack`
:menuselection:`UV --> Mark/Clear Seam`
:menuselection:`UV --> Merge`
:menuselection:`UV --> Minimize Stretch`
:menuselection:`UV --> Mirror`
:menuselection:`UV --> Pack Islands`
:menuselection:`UV --> Pin/Unpin`
:menuselection:`UV --> Project from View (Bounds)`
:menuselection:`UV --> Project from View`
:menuselection:`UV --> Proportional Editing`
:menuselection:`UV --> Reset`
:menuselection:`UV --> Seams from Islands`
:menuselection:`UV --> Show/Hide Faces`
:menuselection:`UV --> Smart UV Project`
:menuselection:`UV --> Snap`
:menuselection:`UV --> Sphere Projection`
:menuselection:`UV --> Split`
:menuselection:`UV --> Stitch`
:menuselection:`UV --> Transform`
:menuselection:`UV --> Unwrap`
:menuselection:`UV Editor --> UV --> Export UV Layout`
:menuselection:`UV Editor --> UV and Edit Mode menus`
:menuselection:`UVs`
:menuselection:`Vertex --> Bevel Edges`
:menuselection:`Vertex --> Bevel Vertices`
:menuselection:`Vertex --> Blend from Shape`
:menuselection:`Vertex --> Connect Vertex Pairs`
:menuselection:`Vertex --> Connect Vertex Path`
:menuselection:`Vertex --> Extrude Vertices`
:menuselection:`Vertex --> Hooks`
:menuselection:`Vertex --> Make Vertex Parent`
:menuselection:`Vertex --> Merge by Distance`
:menuselection:`Vertex --> New Edge/Face from Vertices`
:menuselection:`Vertex --> Propagate to Shapes`
:menuselection:`Vertex --> Rip Vertices and Extend`
:menuselection:`Vertex --> Rip Vertices and Fill`
:menuselection:`Vertex --> Rip Vertices`
:menuselection:`Vertex --> Slide Vertices`
:menuselection:`Vertex --> Smooth Vertices`
:menuselection:`Vertex --> Vertex Groups`
:menuselection:`Vertex Selection`
:menuselection:`View --> Adjust Last Operation`
:menuselection:`View --> Align View`
:menuselection:`View --> Area --> Duplicate Area into new Window`
:menuselection:`View --> Area --> Toggle Fullscreen Area`
:menuselection:`View --> Area --> Toggle Maximize Area`
:menuselection:`View --> Area --> Toggle Quad View`
:menuselection:`View --> Cameras --> Active Camera`
:menuselection:`View --> Cameras --> Frame Camera Bounds`
:menuselection:`View --> Cameras --> Set Active Object as Camera`
:menuselection:`View --> Frame All`
:menuselection:`View --> Frame Selected`
:menuselection:`View --> Local View --> Remove from Local View`
:menuselection:`View --> Local View --> Toggle Local View`
:menuselection:`View --> Navigation --> Fly Navigation`
:menuselection:`View --> Navigation --> Orbit`
:menuselection:`View --> Navigation --> Pan`
:menuselection:`View --> Navigation --> Roll`
:menuselection:`View --> Navigation --> Walk Navigation`
:menuselection:`View --> Navigation --> Zoom In/Out`
:menuselection:`View --> Navigation --> Zoom Region...`
:menuselection:`View --> Navigation`
:menuselection:`View --> Perspective/Orthographic`
:menuselection:`View --> Show Curve Extremes`
:menuselection:`View --> Show F-Curves`
:menuselection:`View --> Show Markers`
:menuselection:`View --> View Properties...`
:menuselection:`View --> View Regions --> Clear Render Region`
:menuselection:`View --> View Regions --> Clipping Region...`
:menuselection:`View --> View Regions --> Render Region...`
:menuselection:`View Layers --> Layer`
:menuselection:`Viewport Gizmos --> Object Gizmos`
:menuselection:`Viewport Overlays -- Sculpt --> Mask`
:menuselection:`W --> CCEN`
:menuselection:`Weights --> Generate Weights`
:menuselection:`Weights --> Invert`
:menuselection:`Weights --> Locks`
:menuselection:`Weights --> Normalize All`
:menuselection:`Weights --> Normalize`
:menuselection:`Weights --> Smooth`
:menuselection:`Weights`
:menuselection:`Window --> Toggle System Console`
:menuselection:`World --> Ambient Occlusion`
:menuselection:`World --> Mist Pass`
:menuselection:`World --> Ray Visibility`
:menuselection:`World --> Settings`
:menuselection:`World --> Surface`
:menuselection:`World --> Volume`
:menuselection:`node editor --> Sidebar --> Trees`
:menuselection:`node editor --> Sidebar`
:menuselection:`node editors --> Add --> Template`
:menuselection:`node editors --> Add --> Templates`
:menuselection:`node editors --> Sidebar --> Arrange tab`
:menuselection:`☰`
:mod:`Freestyle python module <blender_api:freestyle>`
:mod:`blender_api:bpy.context`
:mod:`blender_api:bpy.ops`
:mod:`blender_api:bpy.props.IntProperty`
:mod:`blender_api:bpy.props`
:mod:`blender_api:bpy`
:mod:`blender_api:mathutils.geometry`
:mod:`blender_api:mathutils`
:ref:`2D Cursor <graph_editor-2d-cursor>`
:ref:`3D cursor <editors-3dview-3d_cursor>`
:ref:`3dview-fly-walk`
:ref:`3dview-multi-object-mode`
:ref:`3dview-nav-zoom-region`
:ref:`Action <bpy.types.Action>`
:ref:`Action <dopesheet-action-action>`
:ref:`Action or NLA Editor <actions-workflow>`
:ref:`Add Hook <bpy.ops.object.hook_add_selob>`
:ref:`Adjust Last Operation <ui-undo-redo-adjust-last-operation>`
:ref:`Advanced Brush Settings <sculpt-tool-settings-brush-settings-advanced>`
:ref:`Aligned Inherit Scale <bone-relations-inherit-settings>`
:ref:`Animating Cameras <bpy.ops.marker.camera_bind>`
:ref:`Animation <grease-pencil-animation-tools-interpolation>`
:ref:`Animation Player <render-output-animation_player>`
:ref:`Animation player <prefs-file_paths-animation_player>`
:ref:`Animation player <render-output-animation_player>`
:ref:`Annotate <tool-annotate>`
:ref:`Anti-Aliasing Threshold <bpy.types.SceneGpencil.antialias_threshold>`
:ref:`Apply <bpy.ops.object.transform_apply>`
:ref:`Applying <bpy.ops.object.transform_apply>`
:ref:`Arc <tool-grease-pencil-draw-arc>`
:ref:`Armature Layers <bpy.types.Armature.layers>`
:ref:`Armature Modifier <bpy.types.ArmatureModifier>`
:ref:`Armatures <armatures-index>`
:ref:`Audio Output <render-output-video-encoding-audio>`
:ref:`Audio Panel <data-scenes-audio>`
:ref:`Audio Preferences <prefs-system-sound>`
:ref:`Auto Depth <prefs-auto-depth>`
:ref:`Auto Handle Smoothing <graph_editor-auto-handle-smoothing>`
:ref:`Auto Normalize <weight-painting-auto-normalize>`
:ref:`Auto Run Python Scripts <prefs-auto-execution>`
:ref:`Auto Save <troubleshooting-file-recovery>`
:ref:`Auto Save Preferences <prefs-auto-save>`
:ref:`Auto Saves <troubleshooting-file-recovery>`
:ref:`Auto Smooth <auto-smooth>`
:ref:`Auto-Keyframing <animation-editors-timeline-autokeyframe>`
:ref:`Auto-Perspective Preference <prefs-interface-auto-perspective>`
:ref:`Background Set <scene-background-set>`
:ref:`Bake <physics-bake>`
:ref:`Batch Rename tool <bpy.ops.wm.batch_rename>`
:ref:`Bendy Bones <bendy-bones>`
:ref:`Bevel <bpy.types.Curve.bevel>`
:ref:`Bevel <tool-mesh-bevel>`
:ref:`Bevel Depth <bpy.types.Curve.bevel_depth>`
:ref:`Bevel Resolution <bpy.types.Curve.bevel_resolution>`
:ref:`Bevel Weights <bpy.ops.transform.edge_bevelweight>`
:ref:`Bisect <tool-mesh-bisect>`
:ref:`Blade <tool-blade>`
:ref:`Blend Modes <bpy.types.Material.blend_method>`
:ref:`Blending <bpy.types.AnimData.action_blend_type>`
:ref:`Blending Mode <bpy.types.Material.blend_method>`
:ref:`Bone Envelopes <armature-bones-envelope>`
:ref:`Bounds <bpy.types.Object.show_bounds>`
:ref:`Box <tool-grease-pencil-draw-box>`
:ref:`Box Select <tool-select-box>`
:ref:`Bridge Edge Loops <modeling-meshes-editing-bridge-edge-loops>`
:ref:`Brush <grease-pencil-draw-brushes>`
:ref:`Brush Display <sculpt-paint-brush-display>`
:ref:`Brushes panel <grease-pencil-draw-common-options>`
:ref:`Bézier Handles <editors-graph-fcurves-settings-handles>`
:ref:`Bézier curves <curve-bezier-handle-type>`
:ref:`Bézier curves <curve-bezier>`
:ref:`Calculate To Frame <calc-physics-bake-to-frame>`
:ref:`Camera Parent Lock <prefs-camera-parent-lock>`
:ref:`Checker Deselect <bpy.ops.mesh.select_nth>`
:ref:`Child Of <bpy.types.ChildOfConstraint>`
:ref:`Circle <tool-grease-pencil-draw-circle>`
:ref:`Circle Select <tool-select-circle>`
:ref:`Clamp setting <render-cycles-integrator-clamp-samples>`
:ref:`Clear <bpy.ops.object.*clear>`
:ref:`Clear Parent Inverse <bpy.ops.object.parent_clear>`
:ref:`Clip Display <clip-editor-clip-display-label>`
:ref:`Collections in the Outliner <editors-outliner-editing-collections>`
:ref:`Color <grease-pencil-draw-color>`
:ref:`Color Palette <ui-color-palette>`
:ref:`Color management <render-post-color-management>`
:ref:`Command Line Launching <command_line-launch-index>`
:ref:`Common Image Settings <editors-image-image-settings-common>`
:ref:`Common Object Options <object-common-options>`
:ref:`Common Options <spline-common-options>`
:ref:`Common Settings section <force-field-common-settings>`
:ref:`Communicating <contribute-contact>`
:ref:`Compress file <files-blend-compress>`
:ref:`Constraints <constraints-index>`
:ref:`Containers <files-video-containers>`
:ref:`Contribute to this Manual <about-user-contribute>`
:ref:`Copy As New Driver <drivers-copy-as-new>`
:ref:`Crease <modeling-edges-crease-subdivision>`
:ref:`Create Face <modeling-mesh-make-face-edge-dissolve>`
:ref:`Curve <tool-grease-pencil-draw-curve>`
:ref:`Curve Edit Mode <curve-toolbar-index>`
:ref:`Curve widget <ui-curve-widget>`
:ref:`Custom Properties <files-data_blocks-custom-properties>`
:ref:`Custom Weight Paint Range <prefs-system-weight>`
:ref:`Cutter <tool-grease-pencil-draw-cutter>`
:ref:`Cycle-Aware Keying <timeline-keying>`
:ref:`Data ID <ui-data-id>`
:ref:`Data ID menu <ui-data-id>`
:ref:`Data-Block <ui-data-block>`
:ref:`Data-Block Menu <ui-data-block>`
:ref:`Data-Block menu <ui-data-block>`
:ref:`Data-block menu <ui-data-block>`
:ref:`Debug Value <bpy.ops.wm.debug_menu>`
:ref:`Defocus node <bpy.types.CompositorNodeDefocus>`
:ref:`Delta Transform <bpy.types.Object.delta>`
:ref:`Delta Transformations <bpy.types.Object.delta>`
:ref:`Depth Troubleshooting <troubleshooting-depth>`
:ref:`Developer Extras <prefs-interface-dev-extras>`
:ref:`Directory Layout <blender-directory-layout>`
:ref:`Displace modifier <bpy.types.DisplaceModifier>`
:ref:`Display <sculpt-paint-brush-display>`
:ref:`Dissolved <bpy.ops.mesh.dissolve>`
:ref:`Distributed Memory Across Devices <prefs-system-cycles-distributive-memory>`
:ref:`Draw <bpy.ops.curve.draw>`
:ref:`Draw <tool-grease-pencil-draw-draw>`
:ref:`Driver Variables <drivers-variables-rotation-modes>`
:ref:`Drivers <animation-drivers-index>`
:ref:`Duplicating <modeling_surface_editing_duplicating>`
:ref:`Dyntopo <bpy.types.Brush.topology_rake_factor>`
:ref:`Edge Creases <bpy.ops.transform.edge_crease>`
:ref:`Edge Creases <modifiers-generate-subsurf-creases>`
:ref:`Edge Loop Selection <bpy.ops.mesh.loop_multi_select>`
:ref:`Edge Loops <bpy.ops.mesh.loop_multi_select>`
:ref:`Edge Rings <modeling-meshes-selecting-edge-rings>`
:ref:`Edge Slide <tool-mesh-edge_slide>`
:ref:`Edge Slide tool <modeling-meshes-editing-edge-slide>`
:ref:`Edge bevel weight <modeling-edges-bevel-weight>`
:ref:`Edit Mode <modeling-meshes-editing-vertices-shape-keys>`
:ref:`Edit Texture Space <modeling_transform_edit-texture-space>`
:ref:`Editing Armatures: Naming conventions <armature-editing-naming-conventions>`
:ref:`Editing Markers <animation-markers-editing>`
:ref:`Encoding Panel <render-output-video-encoding-panel>`
:ref:`Envelope Multiply <armature-bones-envelope>`
:ref:`Erase <tool-grease-pencil-draw-erase>`
:ref:`Experimental Feature Set <cycles-experimental-features>`
:ref:`Extending Blender with Python <scripting-index>`
:ref:`Extrapolation <bpy.types.AnimData.action_extrapolation>`
:ref:`Extrapolation <editors-graph-fcurves-settings-extrapolation>`
:ref:`Extrude <modeling-curves-extrude>`
:ref:`Extrude Individual <tool-mesh-extrude_individual>`
:ref:`Extrude Region <tool-mesh-extrude_region>`
:ref:`Extrude To Cursor <tool-mesh-extrude_cursor>`
:ref:`Eyedropper <tool-grease-pencil-draw-eyedropper>`
:ref:`F-curve Extrapolation <editors-graph-fcurves-settings-extrapolation>`
:ref:`Face Loop Selection <modeling-meshes-selecting-face-loops>`
:ref:`Face Loops <modeling-meshes-selecting-face-loops>`
:ref:`Face Map <bpy.types.FaceMaps>`
:ref:`Face Selection Masking <bpy.types.Mesh.use_paint_mask>`
:ref:`Face Set <sculpting-editing-facesets>`
:ref:`Face Sets <sculpting-editing-facesets>`
:ref:`Face-Map <bpy.types.FaceMaps>`
:ref:`Fill <modeling-meshes-editing-fill>`
:ref:`Fill <tool-grease-pencil-draw-fill>`
:ref:`Filter Glossy <render-cycles-integrator-filter-glossy>`
:ref:`Final <bpy.types.FluidDomainSettings.cache_type>`
:ref:`Flow Object <bpy.types.FluidFlowSettings.flow_type>`
:ref:`Fly/Walk Navigation <3dview-fly-walk>`
:ref:`Fly/walk Navigation <3dview-fly-walk>`
:ref:`Follow Path <curve-path-animation>`
:ref:`Frame Overlay <bpy.types.SequenceEditor.show_overlay>`
:ref:`Free Bake <free-physics-bake>`
:ref:`Freestyle Face Marks <bpy.ops.mesh.mark_freestyle_face>`
:ref:`Freestyle Renders <bpy.types.Freestyle>`
:ref:`From Instancer <cycles-nodes-input-texture-coordinate-from-instancer>`
:ref:`Generated Image <image-generated>`
:ref:`Generated UV Properties <properties-texture-space>`
:ref:`Generated UVs <properties-texture-space>`
:ref:`Getting Started <about-getting-started>`
:ref:`Gizmo Preferences <prefs-viewport-gizmo-size>`
:ref:`Global/Local <modeling-mesh-transform-panel>`
:ref:`Glossy Filter <render-cycles-integrator-filter-glossy>`
:ref:`Goal Weight <curves-weight>`
:ref:`Goal Weight <surface-goal-weight>`
:ref:`Graphics Tablet <hardware-tablet>`
:ref:`Grease Pencil Draw <gpencil_draw-toolbar-index>`
:ref:`Grease Pencil Edit <gpencil_edit-toolbar-index>`
:ref:`Grease Pencil Sculpting <gpencil_sculpt-toolbar-index>`
:ref:`Grease Pencil Weight Paint <gpencil_weight_paint-toolbar-index>`
:ref:`Grid Fill <modeling-meshes-editing-grid-fill>`
:ref:`HMD <hardware-head-mounted-displays>`
:ref:`Hair Dynamics <hair-dynamics>`
:ref:`Halos <particle-halo>`
:ref:`Handle <editors-graph-fcurves-settings-handles>`
:ref:`Handles & Interpolation Display <keyframe-handle-display>`
:ref:`Head-Mounted Displays (HMD) <hardware-head-mounted-displays>`
:ref:`Heat Buoyancy <bpy.types.FluidDomainSettings.beta>`
:ref:`Hold Offset <sequencer-duration-hard>`
:ref:`Holdout Collections <bpy.ops.outliner.collection_holdout_set>`
:ref:`How to install it <translations-fuzzy-strings>`
:ref:`IK bones <bone-constraints-inverse-kinematics>`
:ref:`Image <bpy.types.Object.empty_image>`
:ref:`Increment Snap <transform-snap-element>`
:ref:`Influence <bpy.types.constraint.influence>`
:ref:`Initial Temperature <bpy.types.FluidFlowSettings.temperature>`
:ref:`Inset Faces <tool-mesh-inset_faces>`
:ref:`Interface <prefs-interface-color-picker-type>`
:ref:`Interpolation <editors-graph-fcurves-settings-interpolation>`
:ref:`Interpolation Mode <editors-graph-fcurves-settings-interpolation>`
:ref:`Invalid Selection, Disable Anti-Aliasing <troubleshooting-3dview-invalid-selection>`
:ref:`Inverse Kinematics <bone-constraints-inverse-kinematics>`
:ref:`Joining objects <object-join>`
:ref:`Keying popover <timeline-keying>`
:ref:`Keymap Editor <prefs-input-keymap-editor>`
:ref:`Knife <tool-mesh-knife>`
:ref:`LOCAL directory <blender-directory-layout>`
:ref:`Layers <bpy.types.Armature.layers>`
:ref:`Light Paths <render-cycles-integrator-light-paths>`
:ref:`Light Portals <render-cycles-lights-area-portals>`
:ref:`Limitations <eevee-limitations-ao>`
:ref:`Limitations <eevee-limitations-dof>`
:ref:`Limitations <eevee-limitations-materials>`
:ref:`Limitations <eevee-limitations-reflections>`
:ref:`Limitations <eevee-limitations-shadows>`
:ref:`Limitations <eevee-limitations-sss>`
:ref:`Limitations <eevee-limitations-volumetrics>`
:ref:`Line <tool-grease-pencil-draw-line>`
:ref:`Linking to a Scene <data-system-linked-libraries-make-link>`
:ref:`List View <ui-list-view>`
:ref:`List view <ui-list-view>`
:ref:`Live Unwrap <bpy.types.SpaceUVEditor.use_live_unwrap>`
:ref:`Live Unwrap <bpy.types.ToolSettings.use_edge_path_live_unwrap>`
:ref:`Load UI <file-load-ui>`
:ref:`Lock Camera to View <3dview-lock-camera-to-view>`
:ref:`Lock Relative <weight-painting-auto-normalize>`
:ref:`Loop Cut <tool-mesh-loop_cut>`
:ref:`Loop Cut and Slide <bpy.ops.mesh.loopcut_slide>`
:ref:`Loop Cut and Slide Options <modeling-meshes-editing-edge-loopcut-slide-options>`
:ref:`Manual Index <genindex>`
:ref:`Mask <dope-sheet-mask>`
:ref:`Mask Feathers <mask-feather>`
:ref:`Mask Mode <dope-sheet-mask>`
:ref:`Masked <sculpt-mask-menu>`
:ref:`Masked Geometry <sculpt-mask-menu>`
:ref:`Masks <sculpt-mask-menu>`
:ref:`MatCap <render-workbench-matcap>`
:ref:`Material Preview <3dview-material-preview>`
:ref:`Material Slot <material-slots>`
:ref:`Measure <tool-measure>`
:ref:`Menus <ui-header-menu>`
:ref:`Mesh Display Viewport Overlays panel <mesh-display-normals>`
:ref:`Mesh Edit Mode <mesh-toolbar-index>`
:ref:`Mesh Smoothing <modeling-meshes-editing-normals-shading>`
:ref:`Mesh Symmetry <modeling_meshes_tools-settings_mirror>`
:ref:`Metaball Edit Mode <meta-toolbar-index>`
:ref:`Mirror Vertex Group <bpy.ops.object.vertex_group_mirror>`
:ref:`Mirroring a Selection <fig-mesh-duplicating-mirror-selection>`
:ref:`Mist section <render-cycles-integrator-world-mist>`
:ref:`Modifiers Interface <bpy.types.Modifier.show>`
:ref:`Modular <bpy.types.FluidDomainSettings.cache_type>`
:ref:`Movie Clip Editor Proxy settings <clip-editor-proxy>`
:ref:`Multi-Paint <weight-painting-auto-normalize>`
:ref:`NDOF device <hardware-ndof>`
:ref:`NLA blending <bpy.types.AnimData.action_blend_type>`
:ref:`NURBS <curve-nurbs>`
:ref:`NURBS Curves <modeling-curve-order>`
:ref:`NURBS Splines <curve-nurbs>`
:ref:`NURBS curves <curve-nurbs>`
:ref:`Naming bones <armature-editing-naming-bones>`
:ref:`Navigation Gizmo <navigation-gizmo>`
:ref:`No Caustics <render-cycles-integrator-no-caustics>`
:ref:`Normal <bpy.types.FluidFlowSettings.velocity_normal>`
:ref:`Normal Properties <modeling_meshes_editing_normals_properties>`
:ref:`Normalize All <bpy.ops.object.vertex_group_normalize_all>`
:ref:`Normals <modeling-meshes-structure-normals>`
:ref:`Notes section <shader-white-noise-notes>`
:ref:`Object <movie-clip-tracking-properties-object>`
:ref:`Object Color <bpy.types.Object.color>`
:ref:`Object Modifiers <modifiers-index>`
:ref:`Object Parent <object-parenting>`
:ref:`Object Selector <ui-data-id>`
:ref:`Objects <object-common-options>`
:ref:`Offset Edge Loop Cut <bpy.ops.mesh.offset_edge_loops_slide>`
:ref:`Ogg container <files-video-containers>`
:ref:`Opacity <bpy.types.GPencilLayer.opacity>`
:ref:`Open <files-blend-open>`
:ref:`Operator Preset <ui-presets>`
:ref:`Operator Search <bpy.ops.wm.search_operator>`
:ref:`OptiX <render-cycles-gpu-optix>`
:ref:`Orbit <bpy.ops.view3d.view_orbit>`
:ref:`Orbit Style Preference <prefs-input-orbit-style>`
:ref:`Origins <bpy.types.ToolSettings.use_transform_data_origin>`
:ref:`Outliner <bpy.ops.outliner.orphans_purge>`
:ref:`Outliner <editors-outliner-editing-collections>`
:ref:`Paint Mask <sculpt-mask-menu>`
:ref:`Panels <ui-panels>`
:ref:`Pans the 3D Viewport <bpy.ops.view3d.view_pan>`
:ref:`Parent Inverse matrix <parent-inverse-matrix>`
:ref:`Parent Particles <bpy.types.ParticleSettings.use_parent_particles>`
:ref:`Particle Radius <bpy.types.FluidDomainSettings.particle_radius>`
:ref:`Particle Radius <bpy.types.FluidDomainSettings.resolution_max>`
:ref:`Paste Driver Variables <drivers-variables>`
:ref:`Path Animation panel <curve-path-animation>`
:ref:`Path/Curve-Deform <curve-shape-path-curve-deform>`
:ref:`Pie Menu on Drag <keymap-pref-py_menu_on_drag>`
:ref:`Pie menu settings <prefs-pie-menu>`
:ref:`Pixel Coordinates <bpy.types.SpaceUVEditor.show_pixel_coords>`
:ref:`Poly Build <tool-mesh-poly-build>`
:ref:`Polyline <tool-grease-pencil-draw-polyline>`
:ref:`Preference <editors_preferences_input_ndof>`
:ref:`Preferences <prefs-editing-duplicate-data>`
:ref:`Preferences <prefs-menu>`
:ref:`Preferences <prefs-system-sound>`
:ref:`Presets <ui-presets>`
:ref:`Projection Painting <painting-texture-index>`
:ref:`Proportional Editing <3dview-transform-control-proportional-edit-falloff>`
:ref:`Protected <data-system-datablock-fake-user>`
:ref:`Proxy <object-proxy>`
:ref:`Proxy Render Size <proxy-render-size>`
:ref:`Push Down Action <bpy.ops.nla.action_pushdown>`
:ref:`Push/Pull <tool-transform-push_pull>`
:ref:`Python <scripting-index>`
:ref:`Quick Liquid and Quick Smoke <bpy.ops.object.quick>`
:ref:`Quick Set Up Process <splash-quick-start>`
:ref:`Radius <modeling-curve-radius>`
:ref:`Randomize <tool-mesh-smooth>`
:ref:`Randomize Transform <bpy.ops.object.randomize_transform>`
:ref:`Redo Panel <ui-undo-redo-adjust-last-operation>`
:ref:`Reducing Noise <render-cycles-reducing-noise-clamp-samples>`
:ref:`Refraction limitations <eevee-limitations-refraction>`
:ref:`Refresh All <bpy.ops.sequencer.refresh_all>`
:ref:`Relations panel <bone-relations-bone-group>`
:ref:`Relations panel <bone-relations-parenting>`
:ref:`Relative Paths <files-blend-relative_paths>`
:ref:`Release Guide <about-contribute-guides-release>`
:ref:`Rename tool <tools_rename-active>`
:ref:`Render Dimensions Panel <render-tab-dimensions>`
:ref:`Render Region <editors-3dview-navigate-render-region>`
:ref:`Render Regions <editors-3dview-navigate-render-region>`
:ref:`Render perspective <camera-lens-type>`
:ref:`Rendered <3dview-rendered>`
:ref:`Resolution Divisions <bpy.types.FluidDomainSettings.resolution_max>`
:ref:`Resolution Divisions<bpy.types.FluidDomainSettings.resolution_max>`
:ref:`Restrictions <editors-outliner-interface-restriction_columns>`
:ref:`Rip <bpy.ops.mesh.rip_move>`
:ref:`Rip Edge <tool-mesh-rip_edge>`
:ref:`Rip Region <tool-mesh-rip_region>`
:ref:`Roll <tool-bone-role>`
:ref:`Rotation Channel Modes <drivers-variables-rotation-modes>`
:ref:`Rotation Mode <rotation-modes>`
:ref:`Run Script button <editors-text-run-script>`
:ref:`Safe Areas <camera-safe-areas>`
:ref:`Save & Load <prefs-save-load>`
:ref:`Save <files-blend-save>`
:ref:`Save As... <files-blend-save>`
:ref:`Save Buffers <render_properties_save-buffers>`
:ref:`Saves <files-blend-save>`
:ref:`Scale Cage <tool-scale-cage>`
:ref:`Scale Transform <bpy.ops.transform.resize>`
:ref:`Scene Audio <data-scenes-audio>`
:ref:`Scene Units <bpy.types.UnitSettings>`
:ref:`Select <tool-select-tweak>`
:ref:`Select Box <tool-select-box>`
:ref:`Select Circle <tool-select-circle>`
:ref:`Select Edge Loops <bpy.ops.mesh.loop_multi_select>`
:ref:`Select Grouped <bpy.ops.object.select_grouped>`
:ref:`Select Lasso <tool-select-lasso>`
:ref:`Select Linked <bpy.ops.mesh.select_linked>`
:ref:`Select Non-Manifold <bpy.ops.mesh.select_non_manifold>`
:ref:`Select Random <bpy.ops.mesh.select_random>`
:ref:`Select Shortest Path <bpy.ops.mesh.shortest_path_select>`
:ref:`Select Similar <bpy.ops.mesh.select_similar>`
:ref:`Select With Mouse Button <keymap-blender_default-prefs-select_with>`
:ref:`Selection Mode <bpy.types.ToolSettings.uv_select_mode>`
:ref:`Selection Modes <bpy.types.ToolSettings.mesh_select_mode>`
:ref:`Self-Collision <physics-softbody-settings-self-collision>`
:ref:`Set Origin <bpy.ops.object.origin_set>`
:ref:`Set Origin to Geometry <bpy.ops.object.origin_set>`
:ref:`Shader AOV <render-cycles-passes-aov>`
:ref:`Shader Script <bpy.types.ShaderNodeScript>`
:ref:`Shape Key Editor <dope-sheet-shape-key>`
:ref:`Shape Keys <animation-shape_keys-index>`
:ref:`Sharp Edges <bpy.ops.mesh.mark_sharp>`
:ref:`Shear <tool-transform-shear>`
:ref:`Shortest Path <bpy.ops.mesh.shortest_path_select>`
:ref:`Shrink/Flatten <tool-mesh-shrink-fatten>`
:ref:`Sidebar <ui-region-sidebar>`
:ref:`Simple Expression <drivers-simple-expressions>`
:ref:`Simple Expressions <drivers-simple-expressions>`
:ref:`Simple UVs <bpy.ops.paint.add_simple_uvs>`
:ref:`Small Caps Scale setting <modeling-text-character-underline>`
:ref:`Smooth <tool-mesh-smooth>`
:ref:`Smooth Normals <bpy.ops.object.shade_smooth>`
:ref:`Smooth Shading <bpy.ops.object.shade_smooth>`
:ref:`Smooth Shading <modeling-meshes-editing-normals-shading>`
:ref:`Smooth tool <bpy.ops.mesh.vertices_smooth>`
:ref:`Snap Element <transform-snap-element>`
:ref:`Soft Body Edges <physics-softbody-settings-aerodynamics>`
:ref:`Soft Body Edges settings <physics-softbody-settings-edges>`
:ref:`Soft Body Goal settings <physics-softbody-settings-goal>`
:ref:`Soft Body Solver settings <physics-softbody-settings-solver>`
:ref:`Solve Camera Motion <editors-movie-clip-tracking-clip-solve-motion>`
:ref:`Solve object Motion <editors-movie-clip-tracking-clip-solve-motion>`
:ref:`Sort Mesh Elements <mesh-edit-sort-elements>`
:ref:`Sound Crossfade <bpy.ops.sequencer.crossfade_sounds>`
:ref:`Spacebar Action <keymap-blender_default-spacebar_action>`
:ref:`Specials <ui-specials-menu>`
:ref:`Spin <tool-mesh-spin>`
:ref:`Spin Duplicate <tool-mesh-spin>`
:ref:`Splash Screen <splash>`
:ref:`Stabilize Stroke <grease-pencil-draw-brushes-stabilizer>`
:ref:`Startup File <startup-file>`
:ref:`State Colors <animation-state-colors>`
:ref:`Sticky Selection Mode <bpy.types.SpaceUVEditor.sticky_select_mode>`
:ref:`Stretch To <constraints-stretch-to-volume-preservation>`
:ref:`Strip Proxies <bpy.types.SequenceProxy>`
:ref:`Subdivide <bpy.ops.mesh.subdivide>`
:ref:`Submit Patches <contribute-patch_submit>`
:ref:`Subsurface Translucency <bpy.types.Material.use_sss_translucency>`
:ref:`Surface Edit Mode <surface-toolbar-index>`
:ref:`Surface editing <bpy.ops.curve.spin>`
:ref:`Swing and X/Y/Z Twist <drivers-variables-rotation-modes>`
:ref:`Switch Direction <modeling_surfaces_editing_segments_switch-direction>`
:ref:`Sync Selection <bpy.types.ToolSettings.use_uv_select_sync>`
:ref:`System Preferences <editors_preferences_cycles>`
:ref:`Texture Mask <bpy.types.BrushTextureSlot.mask>`
:ref:`Texture Space <properties-texture-space>`
:ref:`Texture Spaces <properties-texture-space>`
:ref:`The Subset Option <bpy.ops.object.vertex_group_levels>`
:ref:`The Subset Option <sculpt-paint_weight-paint_editing_subset>`
:ref:`Tilt <modeling-curve-tilt>`
:ref:`Timeline Keyframe Control <animation-editors-timeline-autokeyframe>`
:ref:`Timeline editor header <animation-editors-timeline-headercontrols>`
:ref:`Tint <tool-grease-pencil-draw-tint>`
:ref:`To Sphere <tool-transform-to_sphere>`
:ref:`To Sphere Transform <bpy.ops.transform.tosphere>`
:ref:`Toolbar <ui-region-toolbar>`
:ref:`Tracking Axis <bpy.types.Object.track_axis>`
:ref:`Transform Cache Constraint <bpy.types.TransformCacheConstraint>`
:ref:`Transform Snapping <transform-snap>`
:ref:`Translation Preferences <prefs-interface-translation>`
:ref:`Triangulate <bpy.ops.mesh.quads_convert_to_tris>`
:ref:`Troubleshooting Depth Buffer Glitches <troubleshooting-depth>`
:ref:`Tweak <tool-select-tweak>`
:ref:`UV Editor <editors-uv-index>`
:ref:`UV Mapping <editors-uv-index>`
:ref:`UV Mapping section <editors-uv-index>`
:ref:`UV maps list <uv-maps-panel>`
:ref:`UV texturing <editors-uv-index>`
:ref:`Unpack <pack-unpack-data>`
:ref:`Upres Factor <bpy.types.FluidDomainSettings.mesh_scale>`
:ref:`Velocity Source<bpy.types.FluidDomainSettings.guide_source>`
:ref:`Vertex Slide <tool-mesh-vertex-slide>`
:ref:`Vertex Weight Edit modifier <modeling-modifiers-weight-edit-influence-mask-options>`
:ref:`Vertex Weight modifiers <bpy.types.VertexWeightEditModifier>`
:ref:`Vertex merging <vertex-merging>`
:ref:`View Animation <topbar-render-view_animation>`
:ref:`View Dolly <3dview-nav-zoom-dolly>`
:ref:`View Layer Properties <render-layers-denoising-optix>`
:ref:`View Menu <dope-sheet-view-menu>`
:ref:`Viewport Overlays <3dview-overlay-grease-pencil>`
:ref:`Viewport Renders <bpy.ops.render.opengl>`
:ref:`Viewport denoising <render-cycles-settings-viewport-denoising>`
:ref:`Visibility properties <grease_pencil-object-visibility>`
:ref:`Visibility properties <render-cycles-object-settings-visibility>`
:ref:`Volume Limitation <eevee-limitations-volumetrics>`
:ref:`Vorticity <bpy.types.FluidDomainSettings.vorticity>`
:ref:`Walk/Fly Navigation <3dview-fly-walk>`
:ref:`Weight <clip-tracking-weight>`
:ref:`Weight <curves-weight>`
:ref:`Whole Character keying set <whole-character-keying-set>`
:ref:`Workspace controls <workspaces-controls>`
:ref:`World tab <render-cycles-integrator-world-mist>`
:ref:`X-Axis Mirror Pose Mode <bpy.types.Pose.use_mirror_x>`
:ref:`X-ray <3dview-shading-xray>`
:ref:`Zoom to Mouse Position <prefs-zoom-mouse-pos>`
:ref:`Zooms the 3D Viewport <editors_3dview_navigation_zoom>`
:ref:`active clip <scene-active-clip>`
:ref:`active object <object-active>`
:ref:`add-ons section <addons-io>`
:ref:`affects light paths somewhat differently <render-cycles-light-paths-transparency>`
:ref:`animate <bpy.ops.anim.keyframe_insert>`
:ref:`animation player <render-output-animation_player>`
:ref:`animation-shapekeys-relative-vs-absolute`
:ref:`animation-state-colors`
:ref:`any type of node <tab-node-tree-types>`
:ref:`application template <app_templates>`
:ref:`armature-bone-roll`
:ref:`as in the 3D Viewport <3dview-view-clip>`
:ref:`auto-bones naming <armature-editing-naming-bones>`
:ref:`automatic Bézier handles <editors-graph-fcurves-settings-handles>`
:ref:`automatic curve handles <editors-graph-fcurves-settings-handles>`
:ref:`bevel weight <modeling-edges-bevel-weight>`
:ref:`blender-chat`
:ref:`blender-directory-layout`
:ref:`bone envelopes <armature-bones-envelope>`
:ref:`bone locking <animation_armatures_bones_locking>`
:ref:`bone page <armature-bone-influence>`
:ref:`bone-relations-parenting`
:ref:`box selection <tool-select-box>`
:ref:`bpy.ops.armature.bone_layers`
:ref:`bpy.ops.armature.flip_names`
:ref:`bpy.ops.curve.select_row`
:ref:`bpy.ops.mesh.dissolve_faces`
:ref:`bpy.ops.mesh.extrude_edges_move`
:ref:`bpy.ops.mesh.extrude_vertices_move`
:ref:`bpy.ops.mesh.loopcut_slide`
:ref:`bpy.ops.mesh.remove_doubles`
:ref:`bpy.ops.node.read_viewlayers`
:ref:`bpy.ops.object.duplicates_make_real`
:ref:`bpy.ops.object.make_single_user`
:ref:`bpy.ops.object.select_linked`
:ref:`bpy.ops.screen.screen_full_area`
:ref:`bpy.ops.sculpt.face_set_edit`
:ref:`bpy.ops.uv.cube_project`
:ref:`bpy.ops.uv.cylinder_project`
:ref:`bpy.ops.uv.follow_active_quads`
:ref:`bpy.ops.uv.lightmap_pack`
:ref:`bpy.ops.uv.smart_project`
:ref:`bpy.ops.uv.sphere_project`
:ref:`bpy.ops.uv.unwrap`
:ref:`bpy.ops.view3d.edit_mesh_extrude_move_normal`
:ref:`bpy.ops.view3d.edit_mesh_extrude_move_shrink_fatten`
:ref:`bpy.ops.wm.search_menu`
:ref:`bpy.types.Armature.use_mirror_x`
:ref:`bpy.types.UnitSettings`
:ref:`chains of bones <armature-bone-chain>`
:ref:`children <object-parenting>`
:ref:`circle selection <tool-select-circle>`
:ref:`clipping distance <camera-clipping>`
:ref:`clipping range <3dview-view-clip>`
:ref:`collision physics <physics-collision-soft-bodt-cloth>`
:ref:`color picker widget <ui-color-picker>`
:ref:`color ramp <ui-color-ramp-widget>`
:ref:`command-line arguments <command_line-args>`
:ref:`command_line-args`
:ref:`command_line-launch-index`
:ref:`common constraint properties <bpy.types.constraint.influence>`
:ref:`common constraint properties <rigging-constraints-interface-common-space>`
:ref:`common constraint properties <rigging-constraints-interface-common-target>`
:ref:`common masking options <modifiers-common-options-masking>`
:ref:`configured in the preferences <prefs-lights-studio>`
:ref:`configuring peripherals <hardware-ndof>`
:ref:`contact <contribute-contact>`
:ref:`context menu <editors-outliner-editing-context_menu>`
:ref:`converting meshes to curves <bpy.ops.object.convert>`
:ref:`crease <modeling-edges-crease-subdivision>`
:ref:`curve <ui-curve-widget>`
:ref:`curve-bezier`
:ref:`curve-convert-type`
:ref:`curve-nurbs`
:ref:`curves <modeling-curves-extrude>`
:ref:`curves <modeling-curves-make-segment>`
:ref:`curves <modeling-curves-subdivision>`
:ref:`curves <modeling-curves-toggle-cyclic>`
:ref:`custom normals <modeling_meshes_normals_custom>`
:ref:`custom set of data <modeling-modifiers-generate-skin-data>`
:ref:`custom split normals <modeling_meshes_normals_custom>`
:ref:`data ID <ui-data-id>`
:ref:`data-block <ui-data-block>`
:ref:`data-block menu <ui-data-block>`
:ref:`data-block menus <ui-data-block>`
:ref:`data-block type <data-system-datablock-types>`
:ref:`data-blocks types <data-system-datablock-types>`
:ref:`data-scenes-props-units`
:ref:`data-system-datablock-make-single-user`
:ref:`default keymap preferences <keymap-blender_default-prefs>`
:ref:`delete <bpy.ops.armature.delete>`
:ref:`delta transform <bpy.types.Object.delta>`
:ref:`delta transforms <bpy.types.Object.delta>`
:ref:`denoiser <render-cycles-settings-viewport-denoising>`
:ref:`denoising <render-cycles-settings-viewport-denoising>`
:ref:`driver namespace example <driver-namespace>`
:ref:`easing mode <editors-graph-fcurves-settings-easing>`
:ref:`easings <editors-graph-fcurves-settings-easing>`
:ref:`edge loop selection <bpy.ops.mesh.loop_multi_select>`
:ref:`edge loops <modeling-mesh-structure-edge-loops>`
:ref:`edited <properties-texture-space-editing>`
:ref:`editing <meta-ball-editing>`
:ref:`editors-3dview-index`
:ref:`editors-graph-fcurves-settings-handles`
:ref:`editors-graph-fcurves-settings-interpolation`
:ref:`editors-sequencer-index`
:ref:`envelopes <armature-bones-envelope>`
:ref:`example <fig-sequencer-strips-effects-add>`
:ref:`exported <bpy.ops.sequencer.export_subtitles>`
:ref:`exterior forces <physics-softbody-forces-exterior-aerodynamics>`
:ref:`exterior forces <physics-softbody-forces-exterior-goal>`
:ref:`extrapolation <editors-graph-fcurves-settings-extrapolation>`
:ref:`eyedropper <ui-eyedropper>`
:ref:`families <meta-ball-object-families>`
:ref:`family <meta-ball-object-families>`
:ref:`fig-collision-soft-plane`
:ref:`fig-constraints-transformation-extrapolate`
:ref:`fig-curves-editing-open-close`
:ref:`fig-curves-extrude-taper-curve`
:ref:`fig-curves-extrude-taper1`
:ref:`fig-curves-extrude-taper2`
:ref:`fig-curves-extrude-taper3`
:ref:`fig-dope-sheet-action`
:ref:`fig-interface-redo-last-edit-mode`
:ref:`fig-interface-redo-last-object-mode`
:ref:`fig-interpolation-type`
:ref:`fig-mesh-basics-add-one`
:ref:`fig-mesh-deform-mirror-cursor`
:ref:`fig-mesh-deform-mirror-origins`
:ref:`fig-mesh-deform-to-sphere-monkey`
:ref:`fig-mesh-screw-angle`
:ref:`fig-mesh-screw-circle`
:ref:`fig-mesh-screw-clock`
:ref:`fig-mesh-screw-duplicate`
:ref:`fig-mesh-screw-error-info`
:ref:`fig-mesh-screw-error-popup`
:ref:`fig-mesh-screw-generated-mesh`
:ref:`fig-mesh-screw-interactive-panel`
:ref:`fig-mesh-screw-profile`
:ref:`fig-mesh-screw-ramp`
:ref:`fig-mesh-screw-spindle`
:ref:`fig-mesh-screw-spring`
:ref:`fig-mesh-screw-start-mesh`
:ref:`fig-mesh-screw-start`
:ref:`fig-mesh-screw-transform-panel`
:ref:`fig-mesh-screw-wood`
:ref:`fig-mesh-select-advanced-loop-ring`
:ref:`fig-mesh-select-intro-selection-modes`
:ref:`fig-mesh-spin-glass-top`
:ref:`fig-mesh-spin-glass`
:ref:`fig-mesh-spin-profile`
:ref:`fig-mesh-topo-loop`
:ref:`fig-meta-ball-base`
:ref:`fig-meta-ball-example`
:ref:`fig-meta-ball-scale`
:ref:`fig-meta-intro-underlying`
:ref:`fig-modifiers-panel-layout`
:ref:`fig-particle-child-kink`
:ref:`fig-rig-bone-active-tip`
:ref:`fig-rig-bone-connected-root`
:ref:`fig-rig-bone-disconnected-tip`
:ref:`fig-rig-bone-duplication`
:ref:`fig-rig-bone-intro-bbone`
:ref:`fig-rig-bone-intro-same`
:ref:`fig-rig-bone-mirror`
:ref:`fig-rig-bone-select-deselect`
:ref:`fig-rig-bones-extrusion`
:ref:`fig-rig-pose-edit-scale`
:ref:`fig-rig-properties-switch`
:ref:`fig-softbody-collision-plane1`
:ref:`fig-softbody-collision-plane2`
:ref:`fig-softbody-force-interior-bending`
:ref:`fig-softbody-force-interior-connection`
:ref:`fig-softbody-force-interior-no-bending`
:ref:`fig-softbody-force-interior-stiff`
:ref:`fig-softbody-force-interior-with`
:ref:`fig-softbody-force-interior-without`
:ref:`fig-surface-edit-extruding`
:ref:`fig-surface-edit-join-complete`
:ref:`fig-surface-edit-join-ready`
:ref:`fig-surface-edit-select-point`
:ref:`fig-surface-edit-select-row`
:ref:`fig-surface-intro-order`
:ref:`fig-surface-intro-surface`
:ref:`fig-surface-intro-weight`
:ref:`fig-troubleshooting-file-browser`
:ref:`fig-view3d-median-point-edit-mode`
:ref:`fig-view3d-median-point-object-mode`
:ref:`fig-view3d-mode-select`
:ref:`fig-view3d-parent-bone-parent-child`
:ref:`fig-view3d-parent-bone-parent-relative`
:ref:`fig-view3d-parent-bone-parent`
:ref:`fig-view3d-parent-scene-no`
:ref:`files-blend-relative_paths`
:ref:`files-data_blocks-custom-properties`
:ref:`files-linked_libraries-known_limitations-compression`
:ref:`files-media-index`
:ref:`filter <editors-outliner-interface-filter>`
:ref:`graph-preview-range`
:ref:`graph-view-menu`
:ref:`graph_editor-view-properties`
:ref:`gravity <bpy.types.Sculpt.gravity>`
:ref:`grease-pencil-draw-common-options`
:ref:`grease-pencil-modifier-influence-filters`
:ref:`handle type <editors-graph-fcurves-settings-handles>`
:ref:`hardware-ndof`
:ref:`headers <ui-region-header>`
:ref:`help-menu`
:ref:`here <bpy.types.Mesh.use_mirror_topology>`
:ref:`here <curve-switch-direction>`
:ref:`hide and reveal <curves-show-hide>`
:ref:`how to combine shape keys and drivers <shapekey-driver-example>`
:ref:`iTaSC IK Solver <rigging-armatures_posing_bone-constraints_ik_model_itasc>`
:ref:`image formats <files-media-image_formats>`
:ref:`image-formats-open-sequence`
:ref:`image-generated`
:ref:`increasing the radius <modeling-curve-radius>`
:ref:`influence <meta-ball-editing-negative-influence>`
:ref:`interpolation algorithm <bpy.types.Spline.tilt_interpolation>`
:ref:`interpolation mode <editors-graph-fcurves-settings-interpolation>`
:ref:`inverse kinematics feature <bone-constraints-inverse-kinematics>`
:ref:`join <bpy.ops.object.join>`
:ref:`keyframe-type`
:ref:`keymap-customize`
:ref:`lasso selection <tool-select-lasso>`
:ref:`later page <bone-constraints-inverse-kinematics>`
:ref:`layer samples <render-cycles-integrator-layer-samples>`
:ref:`left/right <armature-editing-naming-conventions>`
:ref:`limitations <eevee-limitations-volumetrics>`
:ref:`link <data-system-linked-libraries-make-link>`
:ref:`list <ui-list-view>`
:ref:`list view <ui-list-view>`
:ref:`lists <ui-list-view>`
:ref:`loaded in the preferences <prefs-lights-matcaps>`
:ref:`local, system and user paths <blender-directory-layout>`
:ref:`locks pie menu <bpy.ops.object.vertex_group_lock>`
:ref:`marked as sharp <bpy.ops.mesh.mark_sharp>`
:ref:`material indices <bi-multiple-materials>`
:ref:`material slot <material-slots>`
:ref:`material slots <material-slots>`
:ref:`mesh counterpart <bpy.ops.mesh.decimate>`
:ref:`mesh-faces-tristoquads`
:ref:`mesh-unsubdivide`
:ref:`meta family <meta-ball-object-families>`
:ref:`modeling-mesh-analysis`
:ref:`modeling-mesh-make-face-edge-dissolve`
:ref:`modeling-meshes-editing-fill`
:ref:`modeling-text-character`
:ref:`modeling_meshes_normals_custom`
:ref:`modeling_modifiers_deform_shrinkwrap_methods`
:ref:`modifier stack <modifier-stack>`
:ref:`modifiers-generate-subsurf-creases`
:ref:`more details see here <render-cycles-reducing-noise-glass-and-transp-shadows>`
:ref:`naming conventions <armature-editing-naming-conventions>`
:ref:`object setting <render-cycles-settings-object-motion-blur>`
:ref:`object-convert-to`
:ref:`object-data <properties-data-tabs>`
:ref:`object-proxy`
:ref:`object-show-hide`
:ref:`objects types <objects-types>`
:ref:`offsetting nodes <editors-nodes-usage-auto-offset>`
:ref:`pack islands operator <editors-uv-editing-layout-pack_islands>`
:ref:`pack or unpack external Data <pack-unpack-data>`
:ref:`pack-unpack-data`
:ref:`paint mask <sculpt-mask-menu>`
:ref:`painting-sculpting-index`
:ref:`painting-weight-index`
:ref:`panoramic camera <cycles-panoramic-camera>`
:ref:`parenting <bpy.ops.object.parent_set>`
:ref:`passes <render-cycles-passes>`
:ref:`per-light override <bpy.types.Light.cutoff_distance>`
:ref:`performed manually <bpy.ops.mesh.edge_split>`
:ref:`physics-cloth-introduction-springs`
:ref:`pinned <bpy.ops.uv.pin>`
:ref:`pivot-point-index`
:ref:`plane track <clip-tracking-plane>`
:ref:`pose marker <marker-pose-add>`
:ref:`prefs-auto-execution`
:ref:`prefs-file-paths`
:ref:`prefs-index`
:ref:`prefs-interface-translation`
:ref:`prefs-menu`
:ref:`prefs-save-load`
:ref:`preset <ui-presets>`
:ref:`previews <file_browser-previews>`
:ref:`properties switching/enabling/disabling <armature-bone-properties>`
:ref:`properties-material-viewport-display`
:ref:`properties-object-viewport-display`
:ref:`proxies <object-proxy>`
:ref:`ray visibility <cycles-ray-visibility>`
:ref:`recently <other-file-open-options>`
:ref:`refresh <bpy.ops.sequencer.refresh_all>`
:ref:`region <render-output-dimensions-region>`
:ref:`relations page <bone-relations-parenting>`
:ref:`relative file path <files-blend-relative_paths>`
:ref:`relative shape keys mix additively <animation-shapekeys-relative-vs-absolute>`
:ref:`render output path <render-tab-output>`
:ref:`render pass <render-cycles-passes>`
:ref:`render-cycles-gpu-optix`
:ref:`render-cycles-integrator-world-settings`
:ref:`render-cycles-reducing-noise-mis`
:ref:`render-materials-settings-viewport-display`
:ref:`render-output-postprocess`
:ref:`render-tab-dimensions`
:ref:`rendered shading <view3d-viewport-shading>`
:ref:`rendering animation <command_line-render>`
:ref:`resolution <bpy.types.Curve.resolution_u>`
:ref:`resolution <bpy.types.Curve.resolution_v>`
:ref:`rigged <animation-rigging>`
:ref:`roll rotation <armature-bone-roll>`
:ref:`row <modeling-surfaces-rows-grids>`
:ref:`save <files-blend-save>`
:ref:`saving images <bpy.types.ImageFormatSettings>`
:ref:`scale transformation <bpy.ops.transform.resize>`
:ref:`scaled <bpy.ops.transform.resize>`
:ref:`scene dicing rate <cycles-subdivision-rate>`
:ref:`scene settings <data-scenes-audio>`
:ref:`scene settings <data-scenes-props-units>`
:ref:`scene's active camera<scene-camera>`
:ref:`scene-wide bounce settings <cycles-bounces>`
:ref:`scripting <scripting-index>`
:ref:`sculpt-mask-menu`
:ref:`sculpt_mask_clear-data`
:ref:`selecting <object-select-menu>`
:ref:`selection states <object-active>`
:ref:`sequencer-edit-change`
:ref:`shape <bpy.types.Curve.dimensions>`
:ref:`sharp edges <modeling_meshes_normals_sharp_edge>`
:ref:`simplify panel <render-cycles-settings-scene-simplify>`
:ref:`smooth shading <modeling-meshes-editing-normals-shading>`
:ref:`snap tools <bpy.ops.view3d.snap>`
:ref:`splash`
:ref:`split normals <auto-smooth>`
:ref:`stack <modifier-stack>`
:ref:`strip option <sequencer-sound-waveform>`
:ref:`tab-view3d-modes`
:ref:`temp-dir`
:ref:`text editing <ui-text-editing>`
:ref:`their documentation <bpy.ops.object.make_single_user>`
:ref:`this section <render-layers>`
:ref:`tilt <modeling-curve-tilt>`
:ref:`timeline-playback`
:ref:`timeline-view-menu`
:ref:`tool-annotate`
:ref:`tool-mesh-extrude_individual`
:ref:`tool-select-circle`
:ref:`topbar-app_menu`
:ref:`topbar-render`
:ref:`trackball rotation <view3d-transform-trackball>`
:ref:`transform-numeric-input-advanced`
:ref:`transform-numeric-input-simple`
:ref:`transformations <bpy.ops.object.transform_apply>`
:ref:`trivially cyclic curves <bpy.types.FModifierCycles>`
:ref:`troubleshooting-gpu-index`
:ref:`ui-color-palette`
:ref:`ui-color-picker`
:ref:`ui-color-ramp-widget`
:ref:`ui-curve-widget`
:ref:`ui-data-block`
:ref:`ui-data-id`
:ref:`ui-direction-button`
:ref:`ui-eyedropper`
:ref:`ui-list-view`
:ref:`ui-operator-buttons`
:ref:`ui-undo-redo-adjust-last-operation`
:ref:`underline settings <modeling-text-character-underline>`
:ref:`unit system <data-scenes-props-units>`
:ref:`uv-image-rotate-reverse-uvs`
:ref:`uv-maps-panel`
:ref:`value <animation-shapekey-relative-value>`
:ref:`vertex snapping <transform-snap-element>`
:ref:`video codec <files-video-codecs>`
:ref:`view3d-transform-plane-lock`
:ref:`view3d-viewport-shading`
:ref:`weight <curves_structure_nurbs_weight>`
:ref:`weight <modeling-surfaces-weight>`
:ref:`weight-painting-bones`
:ref:`wireframe <3dview-shading-rendered>`
:ref:`x-ray <3dview-shading-xray>`
:ref:`zoom level <editors_3dview_navigation_zoom>`
:sup:`-1`
:sup:`-2`
:sup:`-3`
:sup:`-5`
:sup:`-6`
:sup:`0`
:sup:`1/e`
:sup:`15`
:sup:`24`
:sup:`2`
:sup:`3`
:sup:`4`
:sup:`5`
:sup:`e`
:sup:`p`
:sup:`power`
:sup:`th`
:sup:`®`
:sup:`™`
:term:`Aliasing`
:term:`Alpha <Alpha Channel>`
:term:`Alpha Channel`
:term:`Ambient Light`
:term:`Anti-Aliasing`
:term:`Armature`
:term:`Axis Angle`
:term:`Axis`
:term:`BVH`
:term:`Bake <Baking>`
:term:`Baking`
:term:`Bit Depth`
:term:`Blend Modes`
:term:`Bone`
:term:`Bones <Bone>`
:term:`Bounce <Light Bounces>`
:term:`Bounding Box`
:term:`Bump Mapping`
:term:`Bézier`
:term:`B‑frames <Frame Types>`
:term:`Camera Projections <Projection>`
:term:`Caustics`
:term:`Child`
:term:`Clamp`
:term:`Color Blend Modes`
:term:`Color Space`
:term:`Color Spaces <Color Space>`
:term:`Concave Face`
:term:`Constraining <Constraint>`
:term:`Constraints <Constraint>`
:term:`Curve`
:term:`Cyclic`
:term:`DOF`
:term:`Data User`
:term:`Depth of Field`
:term:`Display Referenced`
:term:`Edge`
:term:`Edges <Edge>`
:term:`Elastic`
:term:`Empty`
:term:`Euler Rotation`
:term:`Euler`
:term:`F-Curves <F-Curve>`
:term:`Face Loop`
:term:`Face`
:term:`Faces <Face>`
:term:`Fake User`
:term:`Field of View <Field of View>`
:term:`Field of View`
:term:`Fireflies`
:term:`Focal Length <Focal Length>`
:term:`Focal Length`
:term:`Forward Kinematics`
:term:`Gamma`
:term:`Gimbal Lock`
:term:`Gimbal`
:term:`Glossy Map`
:term:`HDRI`
:term:`Head`
:term:`IOR`
:term:`Index of Refraction`
:term:`Interpolation`
:term:`Inverse Kinematics`
:term:`Keyframe`
:term:`Keyframes <Keyframe>`
:term:`Keyframing`
:term:`Lattice`
:term:`Local Space`
:term:`Luminance`
:term:`Manifold`
:term:`Mask`
:term:`MatCap`
:term:`Matte`
:term:`Mesh`
:term:`Micropolygons`
:term:`Mip-maps <Mip-map>`
:term:`Motion Blur`
:term:`Multisampling`
:term:`N-gon`
:term:`N-gons <N-gon>`
:term:`NDOF`
:term:`NURBS`
:term:`Non-manifold`
:term:`Normal Mapping`
:term:`Normal's <Normal>`
:term:`Normal`
:term:`Normals <Normal>`
:term:`Object Origin`
:term:`Object`
:term:`Objects <Object>`
:term:`Octahedron`
:term:`OpenGL`
:term:`Overscan`
:term:`Parent`
:term:`Parenting`
:term:`Pivot Point`
:term:`Pixel <Pixel>`
:term:`Point clouds <Point Cloud>`
:term:`Poles <Pole>`
:term:`Pose Mode`
:term:`Posing`
:term:`Premultiplied Alpha`
:term:`Primaries`
:term:`Proxy`
:term:`Quad`
:term:`Quads <Quad>`
:term:`Quaternion`
:term:`Radiosity`
:term:`Ray Tracing`
:term:`Real User`
:term:`Rig`
:term:`Roll Angle`
:term:`Roll`
:term:`Rolling Shutter`
:term:`Roughness Map`
:term:`Scanline`
:term:`Scene Referenced`
:term:`Seed`
:term:`Straight Alpha`
:term:`Subdivision Surface`
:term:`Swing`
:term:`Tail`
:term:`Tessellation`
:term:`Texture Space`
:term:`Texture`
:term:`Timecode`
:term:`Topology`
:term:`Triangle`
:term:`Twist <Swing>`
:term:`UV Map`
:term:`Vertex Group`
:term:`Vertex`
:term:`Vertices <Vertex>`
:term:`Vertices`
:term:`Voxel`
:term:`Voxels <Voxel>`
:term:`Walk Cycle`
:term:`Weight Painting`
:term:`White Point`
:term:`World Space`
:term:`Z-buffer`
:term:`data users <Data User>`
:term:`objects <Object>`
:term:`poles <Pole>`
:term:`space <Color Space>`
:term:`transform <Transform>`            
            '''
            # data = "Constraints are a way to control an object's properties (e.g. its location, rotation, scale), using either plain static values (like the :doc:`\"limit\" ones </animation/constraints/transform/limit_location>`), or another object, called \"target\" (like e.g. the :doc:`\"copy\" ones </animation/constraints/transform/copy_location>`)."
            # data = "`#blender-coders <https://blender.chat/channel/blender-coders>`__ For developers to discuss Blender development."
            # data = "Sun Beams is a 2D effect for simulating the effect of bright light getting scattered in a medium `(Crepuscular Rays) <https://en.wikipedia.org/wiki/Crepuscular_rays>`__. This phenomenon can be created by renderers, but full volumetric lighting is a rather arduous approach and takes a long time to render."
            # data = ":doc:`Transformations (translation/scale/rotation) </scene_layout/object/editing/transform/introduction>` in *Object Mode* and *Edit Mode* (as well as extrusions in *Edit Mode*) can be locked to a particular axis relative to the current :doc:`transform orientation </editors/3dview/controls/orientation>`. By locking a transformation to a particular axis you are restricting transformations to a single dimension."
            # data= "Applies :term:`Anti-Aliasing` to avoid artifacts at sharp edges or areas with a high contrast."
            # data = ":menuselection:`Armature --> Names --> AutoName Left/Right, Front/Back, Top/Bottom`"
            # data = "There is no way of automatically creating a twisting effect where a dampened rotation is inherited up the chain. Consider using :doc:`Bendy Bones </animation/armatures/bones/properties/bendy_bones>` instead."
            # data = ":ref:`Auto-Perspective Preference <prefs-interface-auto-perspective>`"
            # data = ":menuselection:`Object --> Animation --> Bake Mesh to Grease Pencil...`"
            # data = "Boolean (0=False, 1=True)"
            # data = "Slider (0=Free Lips!, 1=Lips Sealed...)"
            data = '''
:ref:`fig-constraints-transformation-extrapolate`
:ref:`pivot-point-index`
:ref:`tab-view3d-modes`
:ref:`temp-dir`
:ref:`bpy.ops.uv.sphere_project`
:ref:`bpy.ops.uv.unwrap`
:doc:`/compositing/types/color/index`
:doc:`/compositing/types/distort/plane_track_deform`
:doc:`/compositing/types/input/rgb`
:doc:`/copyright`            
'''
            data = '''
``!=``
``####``
``#``
``#blender-coders``
``#cos(frame)``
``#declare``
``#docs``
``#fmod(frame, 24) / 24``
``#frame / 20.0``
``#frame``
``#include``
``#sin(frame)``
``$XDG_CONFIG_HOME``
``'``
``'locale' is not under version control``
``(LW)POLYGON``
``(LW)POLYLINE``
``(X)``
``(``
``(origin, vertex_coordinates)``
``(sin( )*4)``
``**``
``*-0001.jpg``
``*-0002.jpg``
``*-0003.jpg``
``*.avi``
``*.blend1``
``*.blend2``
``*.blend``
``*.jpg``
``*.png``
``*Mirror*``
``*``
``+<frame>``
``+C``
``+WT2``
``+WT``
``+``
``+q11``
``+q1``
``,.?!:;``
``,``
``--``
``--addons``
``--app-template``
``--background``
``--cycles-device CPU``
``--cycles-print-stats``
``--debug-all``
``--debug-cycles``
``--debug-depsgraph-build``
``--debug-depsgraph-eval``
``--debug-depsgraph-no-threads``
``--debug-depsgraph-pretty``
``--debug-depsgraph-tag``
``--debug-depsgraph-time``
``--debug-depsgraph-uuid``
``--debug-depsgraph``
``--debug-events``
``--debug-exit-on-error``
``--debug-ffmpeg``
``--debug-fpe``
``--debug-freestyle``
``--debug-ghost``
``--debug-gpu-force-workarounds``
``--debug-gpu-shaders``
``--debug-gpu``
``--debug-gpumem``
``--debug-handlers``
``--debug-io``
``--debug-jobs``
``--debug-libmv``
``--debug-memory``
``--debug-python``
``--debug-value``
``--debug-wm``
``--debug-xr-time``
``--debug-xr``
``--debug``
``--disable-abort-handler``
``--disable-autoexec``
``--disable-crash-handler``
``--enable-autoexec``
``--enable-event-simulate``
``--engine``
``--env-system-datafiles``
``--env-system-python``
``--env-system-scripts``
``--factory-startup --debug-all``
``--factory-startup``
``--frame-end``
``--frame-jump``
``--frame-start``
``--help``
``--log \"*,^wm.operator.*\"``
``--log \"wm.*\"``
``--log-file``
``--log-level``
``--log-show-backtrace``
``--log-show-basename``
``--log-show-timestamp``
``--log``
``--no-native-pixels``
``--no-window-focus``
``--python-console``
``--python-exit-code``
``--python-expr``
``--python-text``
``--python-use-system-env``
``--python``
``--render-anim``
``--render-format``
``--render-frame 1``
``--render-frame``
``--render-output``
``--scene``
``--start-console``
``--threads``
``--use-extension``
``--verbose``
``--version``
``--window-border``
``--window-fullscreen``
``--window-geometry``
``--window-maximized``
``-<frame>``
``-D``
``-E CYCLES``
``-E help``
``-E``
``-F OPEN_EXR``
``-F``
``-M``
``-P``
``-R``
``-S``
``-W``
``-Y``
``-``
``-a``
``-b``
``-ba``
``-con``
``-d``
``-e``
``-f -2``
``-f 10``
``-f``
``-h``
``-j``
``-m \"message\"``
``-m``
``-noaudio``
``-o /project/renders/frame_#####``
``-o``
``-p``
``-r``
``-s 10 -e 500``
``-s``
``-setaudio``
``-t 2``
``-t``
``-v``
``-w``
``-x``
``-y``
``.*``
``.*rabbit.*``
``... is not a valid Win32 application.``
``...@bone_name``
``...``
``..``
``./Blender.app/Contents/MacOS/Blender``
``./autosave/ ...``
``./config/ ...``
``./config/bookmarks.txt``
``./config/recent-files.txt``
``./config/startup.blend``
``./config/userpref.blend``
``./config/{APP_TEMPLATE_ID}/startup.blend``
``./config/{APP_TEMPLATE_ID}/userpref.blend``
``./datafiles/ ...``
``./datafiles/locale/{language}/``
``./python/ ...``
``./resources/theme/js/version_switch.js``
``./scripts/ ...``
``./scripts/addons/*.py``
``./scripts/addons/modules/*.py``
``./scripts/addons_contrib/*.py``
``./scripts/addons_contrib/modules/*.py``
``./scripts/modules/*.py``
``./scripts/presets/interface_theme/``
``./scripts/presets/{preset}/*.py``
``./scripts/startup/*.py``
``./scripts/templates_osl/*.osl``
``./scripts/templates_py/*.py``
``.001``
``.MTL``
``.``
``.app``
``.avi``
``.bashrc``
``.bat``
``.bin``
``.blend1``
``.blend2``
``.blend``
``.bmp``
``.btx``
``.bw``
``.cin``
``.dae``
``.dpx``
``.dv``
``.dvd``
``.eps``
``.exr``
``.flv``
``.gif``
``.glb``
``.gltf``
``.hdr``
``.html``
``.inc``
``.j2c``
``.jp2``
``.jpeg``
``.jpg``
``.mdd``
``.mkv``
``.mov``
``.mp4``
``.mpeg``
``.mpg``
``.ogg``
``.ogv``
``.osl``
``.oso``
``.pc2``
``.pdb``
``.png``
``.po``
``.py``
``.pyd``
``.rgb``
``.rst``
``.sab``
``.sat``
``.sgi``
``.sh``
``.so``
``.srt``
``.svg``
``.svn``
``.tga``
``.tif``
``.tiff``
``.uni``
``.vdb``
``.velocities``
``.vob``
``.webm``
``.xxxx``
``.xyz``
``.zip``
``//``
``//render/my-anim-``
``//render_####``
``//render_0001.png``
``//render_``
``/?``
``/EXIT``
``/``
``/branches``
``/fr``
``/tmp/``
``/tmp``
``/usr/lib/X11/fonts``
``/usr/lib/fonts``
``/usr/local/cuda/include/host_config.h``
``/usr/local/share``
``/usr/local``
``/usr/share/local``
``0 + (cos(frame / 8) * 4)``
``0 + (sin(frame / 8) * 4)``
``0 +``
``0.1``
``0.8``
``0001.jpg``
``0``
``1.0``
``10/5+4``
``1000``
``1000x500``
``1001``
``1002``
``1010``
``1011``
``10``
``10km``
``16:9``
``16``
``1:1``
``1``
``1cm``
``1m 3mm``
``1m, 3mm``
``2 / Width``
``2 /``
``2.285m``
``2.2mm + 5' / 3\" - 2yards``
``20 /``
``210-group``
``21:9``
``23cm``
``256×256``
``2``
``2ft``
``2m 28.5cm``
``3*2``
``3001``
``3DFACE``
``3DSOLID``
``3ft/0.5km``
``4 / Narrowness``
``43756265_xxxxxx_yy.bphys``
``43756265``
``47``
``4:3``
``5 × 60 × 30 = 9000``
``500``
``6``
``7200.jpg``
``9000 / 1.25 = 7200 = 5 × 60 × 24``
``::::``
``:``
``:abbr:`
``:kbd:`
``:linenos:``
``:menuselection:`
``:term:`
``:term:``
``<-->``
``<->``
``<=``
``<Matrix>``
``<``
``<addon(s)>``
``<bool>``
``<code>``
``<engine>``
``<expression>``
``<extra>``
``<file(s)>``
``<filename>``
``<format>``
``<fps-base>``
``<fps>``
``<frame>``
``<frames>``
``<h>``
``<instance_node>``
``<level>``
``<lines>``
``<match>``
``<name>``
``<node>``
``<options>``
``<path of original footage>/BL_proxy/<clip name>``
``<path>``
``<polylist>``
``<sx>``
``<sy>``
``<template>``
``<threads>``
``<value>``
``<verbose>``
``<vertices>``
``<w>``
``==``
``=``
``>=``
``>>>``
``>``
``@CTRL``
``@DEF``
``@MCH``
``@``
``ACIS``
``ARC``
``AUTO``
``AVIJPEG``
``AVIRAW``
``AVI``
``A``
``Accuracy``
``Aim``
``Antialias_Threshold=n.n``
``BEZIER``
``BLENDER_SYSTEM_DATAFILES``
``BLENDER_SYSTEM_PYTHON``
``BLENDER_SYSTEM_SCRIPTS``
``BLOCK``
``BMP``
``BODY``
``B``
``Blender.app``
``Blosc``
``C:\\blender_docs\\build\\html``
``C:\\blender_docs``
``CINEON``
``CIRCLE``
``COLOR``
``COM``
``CPU``
``CTRL``
``CUBE.001``
``CUDA+CPU``
``CUDA``
``CYCLES_CUDA_EXTRA_CFLAGS``
``C``
``ChainPredicateIterator``
``ChainSilhouetteIterator``
``Cmd``
``Ctrl Shift C``
``Ctrl``
``Cube.001``
``Cube.location.x``
``Cube``
``D. -3.0000 (3.0000) Global``
``DDS``
``DEF-``
``DEF``
``DPX``
``DWAA``
``D``
``DensityUP1D``
``DoubleSided``
``Dynamic_1``
``ELLIPSE``
``EPS``
``EXR``
``E``
``Euler(...)``
``FC0``
``FFCC00``
``FS_floral_brush.png``
``False``
``File.py``
``G.debug_value``
``GROUPS``
``G``
``Ge2Kwy5EGE0``
``H.264``
``HDR``
``HELIX``
``HH:MM:SS.FF``
``ID``
``INSERT(ATTRIB+XDATA)``
``INSERT``
``IRIS``
``IRIZ``
``Interface0D``
``Interface1D``
``JACK``
``JP2``
``JPEG``
``KHR_draco_mesh_compression``
``KHR_lights_punctual``
``KHR_materials_clearcoat``
``KHR_materials_pbrSpecularGlossiness``
``KHR_materials_transmission``
``KHR_materials_unlit``
``KHR_mesh_quantization``
``KHR_texture_transform``
``LAYER_frozen``
``LAYER_locked``
``LAYER_on``
``LAYER``
``LIGHT``
``LINE``
``LOCAL, SYSTEM``
``LOCAL, USER, SYSTEM``
``LOCAL, USER``
``LWPOLYLINE``
``Length2DBP1D``
``Living Room``
``MCH-``
``MCH``
``MESH``
``MPEG H.264``
``MPEG``
``MTEXT``
``M``
``MajorControl``
``MajorRadius``
``Makefile``
``Matrix(...)``
``MaxGradient``
``MetaPlane``
``MetaThing.001``
``MetaThing.round``
``MetaThing``
``MinorControl``
``MinorRadius``
``MyCache_xxxxxx_yy.bphys``
``NULL``
``NUMBER``
``Not a valid font``
``OPENAL``
``OPENCL+CPU``
``OPENCL``
``OPEN_EXR_MULTILAYER``
``OPEN_EXR``
``OPTIX``
``ORG-``
``ORG``
``O``
``Occlusion``
``OpenEXR``
``Operator``
``Operators.bidirectional_chain()``
``Operators.chain(), Operators.bidirectional_chain()``
``Operators.chain()``
``Operators.create()``
``Operators.recursiveSplit()``
``Operators.select()``
``Operators.sequentialSplit()``
``Operators.sequential_split(), Operators.recursive_split()``
``Operators.sort()``
``PATH``
``PIZ``
``PLANESURFACE``
``PLAY``
``PNG``
``POINT``
``POLYFACE``
``POLYLINE``
``POLYMESH``
``PXR24``
``PYTHONPATH``
``ProfilCreate.py``
``QuantitativeInvisibilityUP1D``
``Quaternion(...)``
``Quicktime``
``RAWTGA``
``README``
``REGION``
``RENDER``
``RGB``
``RLE``
``ROT``
``RRGGBB``
``R``
``Radius used``
``Read prefs: {DIR}/userpref.blend``
``Resolution does not match``
``Retina``
``SCALE``
``SDL``
``SOLID``
``STYLE``
``SURFACE``
``SVG``
``S``
``Set as default``
``Super``
``TEMP``
``TEXT``
``TGA``
``TIFF``
``TMP_DIR``
``TMP``
``T``
``Targa``
``Too few selections to merge``
``True``
``Tutorials``
``TypeError: an integer is required (got type str)``
``UVMap``
``VIEW``
``VPORT``
``Vector(...)``
``Vertex count after removing doubles``
``ViewEdgeIterator``
``ViewEdge``
``WAV``
``WGT-``
``Wavelength``
``Widgets``
``Windows-Key``
``XYZ``
``X``
``ZIPS``
``ZIP``
``Zip``
``[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]``
``[1, 2, 3, 4, 5, 6]``
``[1, 2, 3]``
``[1.0, 2.0, 3.0]``
``[327, 47]``
``[47]``
``[Vector(...), Vector(...), ...]``
``[[1, 2, 3], [4, 5], [6]]``
``[\"Agent\"]``
``[\"prop_name\"]``
``\"Agent\"``
``\"You have to select a string of connected vertices too\"``
``\"``
``\"fr\": \"Fran&ccedil;ais\",``
``\"fr\": \"Français\"``
``\\``
``\\build\\html\\index.html``
``\\n``
``^``
``__call__``
``__init__.py``
``_page<number>.svg``
``_sep``
``_socket.py``
``_socket.pyd``
``_socket``
``` -- Links to an entry in the :doc:`
``abs``
``absorption()``
``acos``
``addons/``
``addons_contrib``
``addons``
``ambient_occlusion()``
``and``
``angle_y``
``anim_cycles``
``anim_render``
``anim_screen_switch``
``anim_time_max``
``anim_time_min``
``animation_##_test.png``
``animation_01_test.png``
``ashikhmin_shirley(N, T, ax, ay)``
``ashikhmin_velvet(N, roughness)``
``asin``
``atan2``
``atan``
``avi``
``background()``
``background{}``
``basic.copy_chain``
``basic.pivot``
``basic.raw_copy``
``basic.super_copy``
``bin``
``bind_mat``
``bl*er``
``bl_idname``
``bl_info``
``bl_label``
``bl_math``
``blendcache_[filename]``
``blender -E help``
``blender -d``
``blender -r``
``blender-v{VERSION}-release``
``blender.crash.txt``
``blender_debug_gpu.cmd``
``blender_debug_gpu_workaround.cmd``
``blender_debug_log.cmd``
``blender_debug_log.txt``
``blender_docs``
``blender_factory_startup.cmd``
``blender_oculus``
``blender``
``blogger``
``bpy.``
``bpy.app.debug = True``
``bpy.app.driver_namespace``
``bpy.app.handlers.load_factory_preferences_post``
``bpy.app.handlers.load_factory_startup_post``
``bpy.app``
``bpy.context.active_object``
``bpy.context.mode``
``bpy.context.object``
``bpy.context.scene.frame_current``
``bpy.context.scene``
``bpy.context.selected_objects``
``bpy.context``
``bpy.data``
``bpy.types.Window.event_simulate``
``bpy``
``bssrdf_cubic(N, radius, texture_blur, sharpness)``
``bssrdf_gaussian(N, radius, texture_blur)``
``build/html/contents_quicky.html``
``build/html/index.html``
``build/html``
``build``
``camera_for_shot_ZXY_36x24.chan``
``cartoon.py``
``cd C:\\blender_docs``
``cd``
``ceil``
``ch``
``change_placeholders.sh``
``chapter_subsection_sub-subsection_id.png``
``circle icon``
``clamp``
``cm``
``cmd``
``color_picking``
``color``
``colors.inc``
``conf.py: blender_version``
``conf.py``
``config``
``context.scene``
``context``
``cos``
``cube.001``
``cube.``
``cube?``
``cube``
``curved-POLYLINE``
``cycles/``
``dam``
``data_path``
``data``
``default_byte``
``default_float``
``default_sequencer``
``default``
``deg``
``degrees``
``demo.py``
``density``
``dev``
``developer.blender.org``
``diffuse(N)``
``diffuse_ramp(N, colors[8])``
``diffuse_toon(N, size, smooth)``
``dir()``
``directory_name/``
``disp_####.exr``
``display_render``
``dm``
``dot icon``
``emission()``
``execute()``
``exp``
``exr``
``extras``
``fabs``
``faces.super_face``
``file.blend``
``file_01.blend``
``file_02.blend``
``file``
``filename + frame number + .extension``
``float``
``floor``
``fmod``
``foam_####.exr``
``forearm``
``found bundled python: {DIR}``
``fr``
``frame/8``
``frame``
``ft``
``fur``
``g``
``geom:curve_intercept``
``geom:curve_tangent_normal``
``geom:curve_thickness``
``geom:dupli_generated``
``geom:dupli_uv``
``geom:generated``
``geom:is_curve``
``geom:name``
``geom:numpolyvertices``
``geom:polyvertices``
``geom:trianglevertices``
``geom:uv``
``getattribute()``
``getmessage(\"trace\", ..)``
``getmessage``
``glTF Settings``
``glossy_toon(N, size, smooth)``
``hair_reflection(N, roughnessu, roughnessv, T, offset)``
``hair_transmission(N, roughnessu, roughnessv, T, offset)``
``held_object``
``henyey_greenstein(g)``
``highlighted``
``hm``
``holdout()``
``horizontal line icon``
``hour:minute:second``
``html``
``https://developer.blender.org``
``https://svn.blender.org/svnroot/bf-manual/trunk/blender_docs``
``https://www.youtube.com/watch?v=Ge2Kwy5EGE0``
``image0001.png``
``image_##_test.png``
``image_01_test.png``
``in``
``index.rst``
``injected,held_object``
``injected``
``int``
``interface_splash_current.png``
``interface_undo-redo_last.png``
``interface_undo-redo_repeat-history-menu.png``
``introduction.rst``
``island_abbreviation: edge_number``
``jpeg``
``jpg``
``kConstantScope``
``kFacevaryingScope``
``kUniformScope``
``kUnknownScope``
``kVaryingScope``
``kVertexScope``
``km``
``layername_3Dfaces``
``lerp``
``limbs.simple_tentacle``
``limbs.super_finger``
``limbs.super_limb``
``limbs.super_palm``
``living room``
``locale/fr/LC_MESSAGES/getting_started/about_blender/introduction.po``
``locale/fr``
``locale``
``location.x``
``location[0]``
``log``
``m``
``make modifiers``
``make.bat``
``make``
``manual/getting_started/about_blender/introduction.rst``
``manual/images``
``manual``
``master``
``material:index``
``materials/``
``math``
``max``
``meter``
``meters``
``mi``
``microfacet_beckmann(N, roughness)``
``microfacet_beckmann_aniso(N, T, ax, ay)``
``microfacet_beckmann_refraction(N, roughness, ior)``
``microfacet_ggx(N, roughness)``
``microfacet_ggx_aniso(N, T, ax, ay)``
``microfacet_ggx_refraction(N, roughness, ior)``
``mil``
``min``
``mm``
``mode='RENDER'``
``mode``
``modules/``
``modules``
``mov``
``mp3``
``msgstr``
``my_app_template``
``my_scripts``
``name_frame_index.bphys``
``name``
``new_length = real_length / speed_factor``
``no icon``
``non-highlighted``
``normal_####.exr``
``not``
``object.show_name``
``object:index``
``object:location``
``object:random``
``or``
``oren_nayar(N, roughness)``
``particle:age``
``particle:angular_velocity``
``particle:index``
``particle:lifetime``
``particle:location``
``particle:size``
``particle:velocity``
``path:ray_length``
``phong_ramp(N, exponent, colors[8])``
``pi``
``pip3``
``pip``
``png``
``pot``
``pov/inc/mcr/ini``
``pow``
``presets/``
``presets``
``principled_hair(N, absorption, roughness, radial_roughness, coat, offset, IOR)``
``print()``
``quit.blend``
``rad_def.inc``
``rad_def``
``radians``
``reflection(N)``
``refraction(N, ior)``
``register()``
``register``
``render``
``rendering/``
``requirements.txt``
``resolution_x``
``resources/versions.json``
``rest_mat``
``rig_ui.py``
``rig_ui``
``root``
``rotation_x``
``rotation_y``
``rotation_z``
``round``
``rst``
``scene_linear``
``scripts``
``search_path``
``section_1.rst``
``section_2.rst``
``self.location.x``
``self``
``setmessage``
``sin(frame/8)``
``sin(x)/x``
``sin``
``sky_sphere{}``
``smoothstep``
``sphere_sweep``
``spines.super_spine``
``splash.png``
``sqrt(2)``
``sqrt``
``square(frame)``
``st``
``startup.blend``
``startup/``
``startup``
``svn add /path/to/file``
``svn rm /path/to/file``
``svn status``
``svn update``
``svn``
``sys.argv``
``sys.path``
``sys.stdin``
``system-info.txt``
``tan``
``targa``
``temperature``
``test-######.png``
``test-000001.png``
``test.blend``
``test.crash.txt``
``test_blender_file.blend``
``texture {}``
``todo``
``top -o %MEM``
``top -o MEM``
``total``
``trace(point pos, vector dir, ...)``
``translucent(N)``
``transparent()``
``trunc``
``turntable.blend``
``ui_template_list diff``
``um``
``unregister()``
``unregister``
``userpref.blend``
``v``
``var all_langs = {..};``
``volumes.rst``
``weight = 1``
``wm.call_menu_pie``
``wm.call_menu``
``wm.call_panel``
``wm.context_``
``wm.context_cycle_enum``
``wm.context_menu_enum``
``wm.context_modal_mouse``
``wm.context_pie_enum``
``wm.context_scale_float``
``wm.context_toggle_enum``
``wm.context_toggle``
``wm.operators.*``
``wm.set_stereo_3d``
``x``
``yd``
``{BLENDER_SYSTEM_SCRIPTS}/startup/bl_app_templates_system``
``{BLENDER_USER_SCRIPTS}/startup/bl_app_templates_user``
``{base path}/{file name}{frame number}.{extension}``
``|BLENDER_VERSION|``
``|``
``~/.blender/|BLENDER_VERSION|/config/startup.blend``
``~/blender_docs/build/html``
``~/blender_docs/toos_maintenance``
``~/blender_docs``
``~/software``
``~``            
'''
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
            data = "`#docs <https://blender.chat/channel/docs>`__ For discussion related to Blender's documentation."
            data_lines = data.split('\n')
            for text_line in data_lines:
                is_debug = ('animation/armatures' in text_line)
                if is_debug:
                    print('DEBUG')

                for p, ref_type in find_pat_list:
                    if ref_type is RefType.ARCH_BRACKET:
                        found_items = cm.getTextWithinBrackets('(', ')', text_line, is_include_bracket=False)
                    else:
                        found_items = [i for i in p.findall(text_line) if i]
                    if not found_items:
                        continue

                    print(f'{p.pattern}')
                    print(found_items)

                    # k = f'{f}:{p}'
                    for item in found_items:
                        is_tupple = isinstance(item, tuple)
                        if is_tupple:
                            v, k, _ = item
                            if not v:
                                v = ref_type.value
                        else:
                            v = ""
                            k = item

                        # v = ref_type
                        entry = {k: v}
                        print(f'ADD: {entry}')
                        found_dict.update(entry)
            # print(found_dict)
            new_dict_sorted = OrderedDict(list(sorted(list(found_dict.items()))))
            self.setWriting(False)
            return new_dict_sorted

        def performActualFindSpecialTerms():
            found_dict = {}
            file_list = self.getListOfFiles()
            for f in file_list:
                data = self.poFileToDataBlock(f)
                data_lines = data.split('\n')
                print('-' * 30)
                print(f'File:{f}')
                for text_line in data_lines:
                    # is_debug = ("#today" in text_line)
                    # if not is_debug:
                    #     continue
                    for p, ref_type in find_pat_list:
                        if not p.pattern:
                            found_items = cm.getTextWithinBrackets('(', ')', text_line, is_include_bracket=False)
                        else:
                            found_items = [i for i in p.findall(text_line) if i]
                        if not found_items:
                            continue

                        if p.pattern:
                            print(f'{p.pattern}')
                        else:
                            print(f'( .. )')
                        print(found_items)
                        k = f'{f}:{p}'
                        for item in found_items:
                            is_tupple = isinstance(item, tuple)
                            # is_str = isinstance(item, str)
                            if is_tupple:
                                v, k, _ = item
                                if not v:
                                    v = ref_type.value
                            else:
                                v = ""
                                k = item

                            # v = ref_type
                            entry = {k: v}
                            print(f'ADD: {entry}')
                            found_dict.update(entry)
            # print(found_dict)
            new_dict_sorted = OrderedDict(list(sorted(list(found_dict.items()))))
            print(f'new_dict_sorted: {new_dict_sorted}')
            self.setWriting(True)
            return new_dict_sorted

        def writeSortedDict (found_dict: dict):
            # return
            sorted_list = list(found_dict.items())
            sorted_list.sort()
            sorted_dict = OrderedDict(sorted_list)
            if TESTING:
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
            sorted_by_length = list(sorted(found_dict.items(), key=lambda x: len(x[0]), reverse=True))
            for k, v in sorted_by_length:

                ref_type = RefType.getRef(v)

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

                might_have_link = (is_doc or is_ref or is_term or is_mod or is_ga)

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

                print(f'k:{k}, v:{v}')
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
                    abbr, word = m[0]
                    current_tran = tf.isInDict(abbr)
                    if not current_tran:
                        print(f'<IS ABBR>')
                        self.translate_word_into_dict(abbr, tf, tran_dict)
                        self.translate_word_into_dict(word, tf, tran_dict)
                    print(f'</IS ABBR>')
                elif might_have_link:
                    found_list = cm.findInvert(cm.REF_LINK, k)
                    translating_list=[]
                    for k, v in found_list.items():
                        loc, word = v
                        if is_ref or is_doc:
                            print(f'CHECKING:{ref_type} {k}, {v}')
                            stripped_word = word.strip()
                            is_link = is_ref and re.search(r'^\w+([\-\.]\w+){1,}$', stripped_word)
                            is_doc_link = is_doc and re.search(r'^(\/\w+)+$', stripped_word)
                            # is_possible_link = re.compile('('
                            #     r'(\w+[\.\_])+\w+(\((\w+(\,\s\w+)*\))?)|'       # Operators.bidirectional_chain(one), ashikhmin_shirley(N, T, ax, ay)
                            #     r'[\/]?\w+([\_\/]\w+)*(\.\w{3,5})?|'            # animation_01_test.png, camera_for_shot_ZXY_36x24.chan
                            #     r'\_{2}\w|'
                            #     r'\w+\:\w+(\_\w+)|'                             # particle:angular_velocity, particle:location
                            # ')')
                            #
                            # is_valid_ga = is_ga and (re.search(r'(\w+\s)+', stripped_word) is not None)
                            # is_ignore = (is_link or is_doc_link or not is_valid_ga)
                            is_ignore = (is_link or is_doc_link)
                            if is_ignore:
                                print(f'Debug:{ref_type} {k}, {v} => is_link: {is_ignore} link IGNORED')
                            else:
                                print(f'CHECKING:{ref_type} {k}, {v} VALID')
                                translating_list.append(word)
                        else:
                            translating_list.append(word)
                    for word in translating_list:
                        self.translate_word_into_dict(word, tf, tran_dict)
                else:
                    print(f'<ANYTHING ELSE>')
                    # is_ref = not ((ref_type == RefType.GA) or (ref_type == RefType.TEXT))
                    # word_dict = cm.findInvert(cm.REF_PART, k)
                    self.translate_word_into_dict(k, tf, tran_dict, is_translating_ref=True)
                    print(f'</ANYTHING ELSE>')
            return tran_dict

        if TESTING:
            found_text_dict = testFindText()
        else:
            found_text_dict = performActualFindSpecialTerms()
        sorted_list = list(sorted(list(found_text_dict.items()), key=lambda x: len(x[0]), reverse=True))
        new_found_text_dict = OrderedDict(sorted_list)
        translated_dict = translateTheFoundDict(new_found_text_dict)
        writeSortedDict(translated_dict)
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
parser.add_argument("-D", "--debug", dest="debugging", help="Print out messages as processing.", action='store_const', const=True)
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
