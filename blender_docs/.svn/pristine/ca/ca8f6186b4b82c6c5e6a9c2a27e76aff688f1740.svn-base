#!/usr/bin/env python3
# Apache License, Version 2.0
# <pep8 compliant>
# This script is to used to find out PO files that no longer have the RST corresponding instance.
# and printout the 'svn rm --force <filename>', so they can be captured to a file and run at
# user's pleasure. This script assumes the existence of 'addons' directory under the locale/ path.
# Last-Updater: Hoang Duy Tran <hoangduytran1960@googlemail.com>
# Last-Updated: 2018-11-22 15:12+0000

"""
This tool checks for unused locale files,
printing out the command to remove them (if any).
"""

import os
import sys

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
        l=[]
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
        valid = ((self.dirnames != None) and (self.search_path in self.dirnames))
        if (valid):
            self.result = self.dirpath+os.sep
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
        self.search_extension = search_extension
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

    def __init__(self, root_dir, search_extension):
        self.search_extension = search_extension
        self.root_dir = root_dir
        self.result = []

    def run(self):
        excluded_len = len(self.root_dir)
        for filename in self.filenames:
            ext = os.path.splitext(filename)[1]
            valid = ext.lower().endswith(self.search_extension)
            if (valid):
                entry=os.path.join(self.dirpath, filename)
                rel_path = entry[excluded_len:]
                self.result.append(rel_path)

# -----------------------------------------------------------------------------
# findFileByName
# An instance of implementation of the ListPathEvent
# Find all files with the same name in all subdirectories
# Calling it by x = findFileByName("index.po")
# Get result by x.result
# return the list of all matching the provided name in all subdirectories
#
class findFileByName(ListPathEvent):

    def __init__(self, search_name):
        self.search_name = search_name
        self.result = []

    def run(self):
        for filename in self.filenames:
            is_found = (filename.lower() == self.search_name.lower())
            if (is_found):
                entry=os.path.join(self.dirpath, filename)
                self.result.append(entry)


# if you want to operate on a subdir, e.g: "render"
SUBDIR = ""
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.normpath(os.path.join(CURRENT_DIR, ".."))
RST_DIR = os.path.join(ROOT_DIR, "manual", SUBDIR)
LOCALE_DIR = os.path.join(ROOT_DIR, "locale")
SHELL_EXT = (".bat" if (sys.platform == "win32") else ".sh")
COMMENT_FLAG = ("rem" if (sys.platform == "win32") else "#")
HOME_DIR=os.path.expanduser("~")

#some default constants
DOT="."
PO=".po"
RST=".rst"
SVN=".svn"
REMOVAL_SCRIPT_NAME="remove_po_files{}".format(SHELL_EXT)
REMOVAL_SCRIPT_PATH=os.path.join(HOME_DIR, REMOVAL_SCRIPT_NAME)

#print("REMOVAL_SCRIPT_PATH {}".format(REMOVAL_SCRIPT_PATH))
#exit(1)
#Use this to find the parent path to the directory where '.po' files reside
#This is potentially made the code goes wrong if the 'addons' directory is changed to something else
PO_FIND_DIR="addons"
#print("CURRENT_DIR: {}\nROOT_DIR: {}\nRST_DIR: {}\nLOCALE_DIR: {}".format(CURRENT_DIR, ROOT_DIR, RST_DIR, LOCALE_DIR))

# -----------------------------------------------------------------------------
# print_title
# Print out a string to the standard output,
# with uppercase and double underline matching the length of input string
#
def print_title(title, underline="="):
    print(f"\n{title.upper()}\n{len(title) * underline}")


# -----------------------------------------------------------------------------
# Common Utilities
# base function to list path based on the condition and actions defined in the run routine of the callback function
# remember the callback function must be an instance of ListPathEvent, so your function must inherit that
def listPath(path, callback):
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath.startswith(DOT):
            continue

        valid_function = ((not callback is None) and (isinstance(callback, ListPathEvent)))
        if (valid_function):
            callback.setVars(dirpath, dirnames, filenames)
            callback.run()


# -----------------------------------------------------------------------------
# changeExtension
# swap the existing extension with a new one
def changeExtension(entry, to_ext):
    r_index = entry.rfind(DOT)
    new_entry = entry[:r_index]+to_ext
    return new_entry


def writeFile(file_name, text):
    try:
        with open(file_name, "w+") as f:
            f.write(text)
            f.close()
    except Exception as e:
        print("Error: " + str(e))
        exit(1)

def writeExecutableShellScript(executable_entry_list, exec_directory):
    text_for_entries = os.linesep.join(executable_entry_list)
    cd_exec_dir_text = "cd {}{}".format(exec_directory, os.linesep)
    cd_return_dir = "cd {}{}".format(ROOT_DIR, os.linesep)
    writing_text = "{} Run this script to remove spurious PO files that should no longer be there.{}{}{}{}{}".\
        format(COMMENT_FLAG, os.linesep, cd_exec_dir_text, text_for_entries, os.linesep, cd_return_dir)
    writeFile(REMOVAL_SCRIPT_PATH, writing_text)


# -----------------------------------------------------------------------------
# Locale Checks
def warn_locale():
    """
    Check for stale PO files.
    """
    find_by_dir=findParentDir(SVN)
    listPath(LOCALE_DIR, find_by_dir)
    if (not find_by_dir.result):
        raise Exception("Unable to find SVN directory.")

    locale_dir = find_by_dir.result
    find_by_dir = findParentDir(PO_FIND_DIR)
    listPath(locale_dir, find_by_dir)
    po_dir = find_by_dir.result

    len_local_dir = len(locale_dir)
    po_dir_patch_part = po_dir[len_local_dir:]


    find_po_files = findFileByExtensionRelative(po_dir, PO)
    listPath(LOCALE_DIR, find_po_files)
    po_file_list = sorted(find_po_files.result)

    unfound_unique_po_list=[]
    for po_file in po_file_list:
        rst_file = changeExtension(po_file, ".rst")
        rst_entry = os.path.join(RST_DIR, rst_file)
        is_file_existed = os.path.exists(rst_entry)
        if (not is_file_existed):
            po_unfound_entry = "svn rm --force {}".format(os.path.join(po_dir_patch_part, po_file))
            if (not po_unfound_entry in unfound_unique_po_list):
                unfound_unique_po_list.append(po_unfound_entry)

    if (len(unfound_unique_po_list) > 0):
        print_title("Found SVN entries should no longer exists and can be removed:")
        writeExecutableShellScript(unfound_unique_po_list, locale_dir)
        print("Please execute this script: {}".format(REMOVAL_SCRIPT_PATH))

def main():
    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)

    warn_locale()


if __name__ == "__main__":
    main()
