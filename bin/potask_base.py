#!/usr/bin/python3
#cython: language_level=3

import sys
import os
import re
blend_man_path = os.environ['BLENDER_GITHUB']
bin_path = os.path.join(blend_man_path, '/bin')
sys.path.append(bin_path)

from definition import Definitions as df
from utils import dd

import json


def writeJSONDic(dict_list=None, file_name=None):
    try:
        if not file_name:
            return

        if not dict_list:
            return

        with open(file_name, 'w+', newline='\n', encoding='utf8') as out_file:
            json.dump(dict_list, out_file, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))
    except Exception as e:
        df.LOG(f'{e}; Length of read dictionary:{len(dict_list)}', error=True)
        raise e


def loadJSONDic(file_name=None):
    return_dic = {}
    try:
        if not file_name:
            dd(f'loadJSONDic - file_name is None.')
            return return_dic

        if not os.path.isfile(file_name):
            dd(f'loadJSONDic - file_name:{file_name} cannot be found!')
            return return_dic

        dic = {}
        with open(file_name) as in_file:
            # dic = json.load(in_file, object_pairs_hook=NoCaseDict)
            return_dic = json.load(in_file)
    except Exception as e:
        df.LOG(f'{e}; Exception occurs while performing loadJSONDic({file_name})', error=True)

    return return_dic

LINE_SEP="@@"
START_WORD_SYMBOLS = re.compile(r'^\W+')
END_WORD_SYMBOLS = re.compile(r'\W+$')
DOT_SPACES = re.compile(r'^[\s\.]+$')

class POResultRecord(object):
    def __init__(self, line_no, msgid, msgstr):
        self.line_no = line_no
        self.msgid = msgid
        self.msgstr = msgstr

    def __repr__(self):
        self.msgid = ("" if not self.msgid else self.msgid)
        self.msgstr = ("" if not self.msgstr else self.msgstr)
        txt = f'[{self.line_no}]; msgid:"{self.msgid}"; msgstr:"{self.msgstr}"'
        return txt

class POTaskBase(list):
    def __init__(self,
                 input_file=None,
                 output_to_file=None,
                 translation_file=None,
                 validate_file=None,
                 pattern=None,
                 negate_pattern=None,
                 pattern_id=None,
                 negate_pattern_id=None,
                 is_case_sensitive=None,
                 is_msgid=None,
                 is_msgstr=None,
                 is_display_msgid=None,
                 is_display_msgstr=None,
                 count_number_of_lines=None,
                 filter_ignored=None,
                 clear_po_comment=None,
                 search_extensions=None,
                 set_translation_fuzzy=None,
                 apply_case_matching_orig_txt=None
                 ):
        self.po_path = input_file
        self.opo_path = output_to_file
        self.tran_file = translation_file
        self.validate_file = validate_file
        self.default_working = os.environ['BLENDER_GIT_PO_FILE']
        self.pattern = (r'%s' % (pattern))
        self.negate_pattern = (r'%s' % (negate_pattern))
        self.pattern = (r'%s' % (pattern) if pattern else None)
        self.negate_pattern = (r'%s' % (negate_pattern) if negate_pattern else None)
        self.apply_case_matching_orig_txt = (True if apply_case_matching_orig_txt else False)

        self.pattern_id = (r'%s' % (pattern_id) if pattern_id else None)
        self.negate_pattern_id = (r'%s' % (negate_pattern_id) if negate_pattern_id else None)

        self.is_case_sensitive = (True if is_case_sensitive else False)
        self.is_msgid = (True if is_msgid else False)
        self.is_msgstr = (True if is_msgstr else False)
        self.is_display_msgid = (True if is_display_msgid else False)
        self.is_display_msgstr = (True if is_display_msgstr else False)
        self.count_number_of_lines = (True if count_number_of_lines else False)
        self.filter_ignored = (True if filter_ignored else False)
        self.clear_po_comment = (True if clear_po_comment else False)
        self.set_translation_fuzzy = (True if set_translation_fuzzy else False)
        self.result = []
        self.line_count=0

        self.pattern_line_no = re.compile(r"\[\d+\]:\s", flags=re.I)
        self.pattern_msgstr = re.compile(r"msgstr:\s", flags=re.I)
        self.pattern_msgid = re.compile(r"msgid:\s", flags=re.I)

        self.search_extensions = None
        if search_extensions:
            self.search_extensions = [x for x in search_extensions.split('|')]


    def setFiles(self):
        has_file = bool(self.po_path)
        if not has_file:
            self.po_path = self.default_working

        has_file = os.path.exists(self.po_path)
        if not has_file:
            msg = f'File: {self.po_path} doesn\'t exist, choose a different path please.'
            raise RuntimeError(msg)

        can_read_file = (os.path.isfile(self.po_path))
        if not can_read_file:
            msg = f'File: [{self.po_path}] cannot be read. Must provide a readable PO file.'
            raise RuntimeError(msg)

    def getNoneAlphaPart(self, msg, is_start=True):
        if not msg:
            return ""

        non_alnum_part = ""
        if is_start:
            non_alpha = START_WORD_SYMBOLS.search(msg)
        else:
            non_alpha = END_WORD_SYMBOLS.search(msg)

        if non_alpha:
            non_alnum_part = non_alpha.group(0)
        return non_alnum_part

    def outputToFile(self, path, data):
        try:
            writeJSONDic(data, path)
        except Exception as e:
            raise RuntimeError(e)

    def convertDataToDict(self, data=None):
        def sort_record(r: POResultRecord):
            return r.line_no

        result_dict={}
        r : POResultRecord = None

        working_data = (data if data else self)
        sorted_data = list(sorted(working_data, key=sort_record, reverse=False))
        for r in sorted_data:
            k = r.msgid
            v = r.msgstr
            dict_entry={k: v}
            result_dict.update(dict_entry)
        return result_dict

    def showResult(self):
        has_records = (len(self) > 0)
        if not has_records:
            msg = f'Either NOTHING is found.'
            print(msg)
            return

        has_output_file = bool(self.opo_path)
        if has_output_file:
            output_dict = self.convertDataToDict()
            self.outputToFile(self.opo_path, output_dict)
        else:
            for rec in self:
                print(rec)

        if self.count_number_of_lines:
            self.line_count = len(self)
            msg = f'{self.line_count} records is found!'
            print(msg)

    def performTask(self):
        pass

# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po

