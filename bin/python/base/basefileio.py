#!/usr/bin/python3 -d
from common import Common
import os
import re
#import copy
import os.path
#import hashlib

import datetime
#from time import gmtime, strftime
from pytz import timezone
#from enum import Enum
#from bisect import bisect_left

# -----------------------------------------------------------------------------
# ListPathEvent
# This is the base body of file listing event handler, based on the java's ActionEvent pattern.
# It only holds mainly the data passing in by the listPath function
#   1. dirpath : current path of a file
#   2. dirnames : all the directory names under the dirpath
#   3. filenames : only the filename part under the dirpath
# 3 parts must be combined in order to form the whole absolute path to a filename
#
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
# findParentDir
# An instance of implementation of the ListPathEvent
# Search for a directory name and return the parent directory of search_path
# Calling it by x = findParentDir(".svn")
# get result by x.result
# return the part BEFORE the ".svn", ie. <locale_dir> (ROOT_DIR/locale/fr)
#
class findParentDir(ListPathEvent):

    def __init__(self, search_path):
        self.search_path = search_path
        self.result = None

    def run(self):
        valid = ((self.dirnames != None)
                 and (self.search_path in self.dirnames))

        if (valid):
            self.result = os.path.join(self.dirpath, os.sep)
            #print("self.result: {}, dirnames: {}".format(self.result, self.dirnames))
            return


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
            ext = os.path.splitext(filename)[1]
            is_valid = ext.lower().endswith(self.search_extension)
            if (is_valid):
                entry=os.path.join(self.dirpath, filename)
                self.result.append(entry)
                #print("entry:{}".format(entry))

# -----------------------------------------------------------------------------
# findFileByExtensionRelative
# An instance of implementation of the ListPathEvent
# Find all files with matching extenion
# Calling it by x = findFileByExtension("rst")
# return the list of all files matching the provided extension, with relative paths
#
class findFileByExtensionRelative(ListPathEvent):

    def __init__(self, root_dir , search_extension):
        self.search_extension = search_extension
        self.root_dir = root_dir
        self.result = []

    def run(self):
        excluded_len = len(self.root_dir)
        for filename in self.filenames:
            ext  = os.path.splitext(filename)[1]
            valid = ext.lower().endswith(self.search_extension)
            if (valid):
                entry=os.path.join(self.dirpath, filename)
                rel_path = entry[excluded_len:]
                is_leading_with_path_sep = rel_path.startswith(os.sep)
                is_root_dir_relative = (self.root_dir != os.sep)
                is_remove_leading_slash = (is_leading_with_path_sep and is_root_dir_relative)

                if (is_remove_leading_slash):
                    rel_path = rel_path.lstrip(os.sep)
                self.result.append(rel_path)

# -----------------------------------------------------------------------------
# To test, just run a source ~/.bash_profile to update your current terminal.

# Side note about the colors: The colors are preceded by an escape sequence \e and defined by a color value, composed of [style;color+m] and wrapped in an escaped [] sequence. eg.

# red = \[\e[0;31m\]
# bold red (style 1) = \[\e[1;31m\]
# clear coloring = \[\e[0m\]
# findFileByName
# An instance of implementation of the ListPathEvent
# Find all files with the same name in all subdirectories
# Calling it by x = findFileByName("index.po")
# Get result by x.result
# return the list of all matching the provided name in all subdirectories
#
class findFileByName(ListPathEvent):

    def __init__(self, search_name ):
        self.search_name= search_name
        self.result = []

    def run(self):
        for filename in self.filenames:
            is_found  = (filename.lower() == self.search_name.lower())
            if (is_found):
                entry=os.path.join(self.dirpath, filename)
                self.result.append(entry)


class BaseFileIO():

    def writeListToFile(self, file_name, text_list):
        with open(file_name, "w+") as f:
            for (index, text_line) in enumerate(text_list):
                f.write(text_line)
                f.write(os.linesep)
            f.close()

    def writeTextToFile(self, file_name, text):
        with open(file_name, "w+") as f:
            f.write(text)
            f.close()

    def readTextFileAsList(self, file_name):
        line_list=None
        with open(file_name) as f:
            line_list = f.readlines();
            return line_list
        return None

    def readFile(self, file_name):
        with open(file_name) as f:
            read_text = f.read();
            f.close()
            return read_text
        return None

    def getTimeNow(self) -> str:
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        loc_dt=local_time.localize(datetime.datetime.now())
        formatted_dt=loc_dt.strftime(fmt)
        return formatted_dt

    def listDirModiTimeSorted(self, folder) -> list:
        def getmtime(name):
            path = os.path.join(folder, name)
            return os.path.getmtime(path)

        return sorted(os.listdir(folder), key=getmtime, reverse=True)

    # -----------------------------------------------------------------------------
    # Common Utilities
    # base function to list path based on the condition and actions defined in the run routine of the callback function
    # remember the callback function must be an instance of ListPathEvent, so your function must inherit that
    def listDir(self, from_path : str, callback : object):
        for dirpath, dirnames, filenames in os.walk(str(from_path)):
            if dirpath.startswith(Common.DOT):
                continue

            valid_function = ((not callback is None) and (isinstance(callback, ListPathEvent)))
            if (valid_function):
                callback.setVars(dirpath, dirnames, filenames)
                callback.run()
