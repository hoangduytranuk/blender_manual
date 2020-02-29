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
from pprint import pprint as pp
from sphinx_intl import catalog as c
from babel.messages import pofile
import enum

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
        #print("getListSorted:", self.result)
        #pp(self.result)
        #print("before sorted getListSorted")

        sorted_list = sorted(self.result, key=key_function, reverse=is_reversed)
        #pp(sorted_list)
        #print("after sorted getListSorted")
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
            print("ERROR write data:", data)
            print("ERROR write file:", file_name)
            raise e

    def readTextFile(self, file_name):
        data=None
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                data = f.read()
            return data
        except Exception as e:
            print("ERROR reading file:", file_name, e)
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
                # print("calling back with:", dirpath, dirnames, filenames)
                callback.setVars(dirpath, dirnames, filenames)
                callback.run()

class FindFilesHasPattern:

    def __init__(self):
        self.basic_io = BasicIO()
        self.found_lines_dic = {}

    def setVars(self, find_pattern, find_po, find_rst, find_py, case_sensitive, before_lines, after_lines):
        self.find_po = (True if find_po else False)
        self.find_rst = (True if find_rst else False)
        self.find_py = (True if find_py else False)
        self.case_sensitive = (True if case_sensitive else False)

        flag = (re.I if not self.case_sensitive else 0)
        self.find_pattern = re.compile(r'{}'.format(find_pattern), flags=flag)
        self.from_line = (int(before_lines) if before_lines else -1)
        self.to_line = (int(after_lines) if after_lines else -1)

    def find(self):
        po_dir = os.environ['BLENDER_MAN_VI']
        if po_dir:
            po_dir = os.path.join(po_dir, "LC_MESSAGES")
            print("po_dir:", po_dir)

        rst_dir = os.environ['BLENDER_MAN_EN']
        if rst_dir:
            rst_dir = os.path.join(rst_dir, "manual")
            print("rst_dir:", rst_dir)

        py_dir = os.environ['LOCAL_PYTHON_3']
        if py_dir:
            print("py_dir:", py_dir)
        
        po_file_list=None
        rst_file_list=None
        py_file_list=None
        search_file_list=[]

        if (self.find_po):
            po_file_list = self.getFileList(po_dir, "po")
            #print("po_file_list")
            ##pp(po_file_list)
            search_file_list.extend(po_file_list)            

        if (self.find_rst):
            rst_file_list = self.getFileList(rst_dir, "rst")
            #print("rst_file_list")
            ##pp(rst_file_list)
            search_file_list.extend(rst_file_list)

        if (self.find_py):
            py_file_list = self.getFileList(py_dir, "py")
            #print("py_file_list")
            ##pp(py_file_list)
            search_file_list.extend(py_file_list)
        
        has_file = (len(search_file_list) > 0)
        if not has_file:
            print("No files to search! Terminate.")
            return

        # print("SEARCHING:")
        for f in search_file_list:
            #print(f)
            try:
                # print("searching in:", f, "for", self.find_pattern)
                self.findPatternInFile(f)
            except Exception as e:
                print("Exception:", e, " file:", f)                
    
    def listingRange(self, data_list, found_index):
        has_from_line = (self.from_line >= 0)
        has_to_line = (self.to_line >= 0)
        
        max_lines = len(data_list)
        if has_from_line:
            min_range = [0, found_index - self.from_line]
            from_line = max(min_range)
            #print("from_line", from_line)
        else:
            from_line = found_index

        if has_to_line:
            max_range = [found_index + self.to_line + 1, max_lines]
            to_line = min(max_range)
            #print("to_line", to_line)
        else:
            max_range = [found_index + 1, max_lines]
            to_line = min(max_range)

        #print("found_index", found_index, "from_line", from_line, "to_line", to_line)
        for index in range(from_line, to_line):
            text_line = data_list[index]
            entry = {index: text_line}
            self.found_lines_dic.update(entry)
            #print(index, text_line)


    def reportFind(self, data):
        data_list = data.split('\n')
        
        for line_no, data_line in enumerate(data_list):
            is_found = (self.find_pattern.search(data_line) != None)
            if is_found:
                #print(line_no, data_line)
                self.listingRange(data_list, line_no)
        
        has_result = (len(self.found_lines_dic) > 0)
        if has_result:
            pp(self.found_lines_dic)

    def findPatternInFile(self, file_path):
        data = self.basic_io.readTextFile(file_path)

        # flag = (re.I if self.case_sensitive else 0)

        #found_list = re.findall(self.find_pattern, data, flags=flag)
        found_list = self.find_pattern.findall(data)
        is_found = (len(found_list) > 0)
        if is_found:
            #pp(found_list)
            self.reportFind(data)
            print("Found in:", file_path)
            print("-" * 80)

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
        # print("Hoang Duy Tran")
        self.find()


parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-p", "--pattern", dest="find_pattern", help="Pattern to find.")
parser.add_argument("-o", "--po", dest="find_po", help="Find in $BLENDER_MAN_VI/LC_MESSAGES.", action='store_const', const=True)
parser.add_argument("-r", "--rst", dest="find_rst", help="Find in $BLENDER_MAN_EN/manual.", action='store_const', const=True)
parser.add_argument("-y", "--py", dest="find_py", help="Find in $LOCAL_PYTHON_3.", action='store_const', const=True)
parser.add_argument("-c", "--case", dest="case_sensitive", help="Find with case sensitive.", action='store_const', const=True)
parser.add_argument("-A", "--after", dest="after_lines", help="Listing this number of lines AFTER the found lines as well.")
parser.add_argument("-B", "--before", dest="before_lines", help="Listing this number of line BEFORE the found lines as well.")

args = parser.parse_args()

x = FindFilesHasPattern()
x.setVars(args.find_pattern, args.find_po, args.find_rst, args.find_py, args.case_sensitive, args.before_lines, args.after_lines)
x.run()