#!/usr/bin/env python3
# Apache License, Version 2.0
# <pep8 compliant>
# This script is to used to find out PO files that no longer have the RST corresponding instance.
# and printout the 'svn rm --force <filename>', so they can be captured to a file and run at
# user's pleasure. This script assumes the existence of 'addons' directory under the locale/ path.
# Last-Updater: Hoang Duy Tran <hoangduytran1960@googlemail.com>
# Last-Updated: 2018-12-08 21:33+0000

"""
This tool checks for unused locale files,
printing out the command to remove them (if any).
"""

import os
import sys
import re

class ListPathEvent:
    """
        This is the base body of file listing event handler, based on the java's ActionEvent pattern.
        It only holds mainly the data passing in by the listPath function
            1. dirpath : current path of a file
            2. dirnames : all the directory names under the dirpath
            3. filenames : only the filename part under the dirpath
    """
    def __init__(self):
        """
        Initialise the class, setting all variables to None
        """
        self.dirpath : str = None
        self.dirnames : list = None
        self.filenames : list = None
        self.root_path : str = None

    def setVars(self, root_path, dirpath : str, dirnames : list, filenames : list):
        """
        :param dirpath: see above
        :param dirnames: see above
        :param filenames: see above
        :return: None
        """
        self.dirpath = dirpath
        self.dirnames = dirnames
        self.filenames = filenames
        self.root_path = root_path

    def run(self):
        """
        Any inherited instance must implement this routine
        to extract a desired result out of the data provided in
        provided variables
        :return: None
        """
        pass


class findParentDir(ListPathEvent):
    """
    An instance of implementation of the ListPathEvent
    Search for a directory name and return the parent directory of search_path
    Calling it by x = findParentDir(".svn")
    get result by x.result
    return the part BEFORE the ".svn", ie. <locale_dir> (ROOT_DIR/locale/fr)
    """
    def __init__(self, search_path : str):
        """
        Initialise the class
        :param search_path: The path to be searched in the dirnames provided
        """
        self.search_path : str = search_path
        self.result : str = None
        self.lock_result : bool = False

    def run(self):
        valid : bool = ((self.dirnames != None) and (self.search_path in self.dirnames))
        if (valid and (not self.lock_result)):
            self.result = self.dirpath+os.sep
            self.lock_result = True


class findFileByExtension(ListPathEvent):
    """
    An instance of implementation of the ListPathEvent
    Find all files with matching extenion input
    Calling it by x = findFileByExtension("rst")
    return the list of all files matching the provided extension
    """

    def __init__(self, search_extension : str):
        """
        Initialise the class with the search_extension
        :param search_extension:
        """
        self.search_extension : str = search_extension
        self.result : list = []

    def run(self):
        for filename in self.filenames:
            ext : str = os.path.splitext(filename)[1]
            is_valid : bool = ext.lower().endswith(self.search_extension)
            if (is_valid):
                entry : str =os.path.join(self.dirpath, filename)
                self.result.append(entry)

class findFileByExtensionRelative(ListPathEvent):
    """
    An instance of implementation of the ListPathEvent
    Find all files with matching extenion
    Calling it by x = findFileByExtension("rst")
    return the list of all files matching the provided extension, with relative paths
    """

    def __init__(self, search_extension : str):
        """
        Initialise the class, setting all variables to input parameters

        :param root_dir: The directory where
        :param search_extension:
        """
        self.search_extension : str = search_extension
        self.result : list = []

    def run(self):
        excluded_len : int = len(self.root_path)
        for filename in self.filenames:
            ext : str = os.path.splitext(filename)[1]
            valid : bool = ext.lower().endswith(self.search_extension)
            if (valid):
                entry : str =os.path.join(self.dirpath, filename)
                rel_path : str = entry[excluded_len:]
                self.result.append(rel_path)

class findFileByName(ListPathEvent):
    """
    An instance of implementation of the ListPathEvent
    Find all files with the same name in all subdirectories
    Calling it by x = findFileByName("index.po")
    Get result by x.result
    return the list of all matching the provided name in all subdirectories

    """

    def __init__(self, search_name : str):
        """
        Initialise the class, setting all variables to input parameters

        :param search_name: The filename to be searched
        """
        self.search_name : str = search_name
        self.result : list = []

        # is_found : bool = (filename.lower() == self.search_name.lower())
        self.p: Pattern = re.compile(self.search_name)

    def run(self):
        """
        This part could be improved using regular expression if there is a need, as:

        p : Pattern = re.compile(search_name)
        m : Match = p.match(filename)
        is_found : bool = (m != None)

        :return: None
        """
        for filename in self.filenames:
            m: Match = self.p.match(filename)
            is_found: bool = (m != None)
            if (is_found):
                entry : str = os.path.join(self.dirpath, filename)
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

#Use this to find the parent path to the directory where '.po' files reside
#This is potentially made the code goes wrong if the 'addons' directory is changed to something else
PO_FIND_DIR="addons"
#print("CURRENT_DIR: {}\nROOT_DIR: {}\nRST_DIR: {}\nLOCALE_DIR: {}".format(CURRENT_DIR, ROOT_DIR, RST_DIR, LOCALE_DIR))

def print_title(title, underline="="):
    """
    Print out a string to the standard output,
    with uppercase and double underline matching the length of input string

    :param title: The string tile
    :param underline: The character for underlinning line
    :return: None
    """
    print(f"\n{title.upper()}\n{len(title) * underline}")


def listPath(path : str, callback : object):
    """
    Base function to list path based on the condition and actions defined in the run routine of the callback function
    remember the callback function must be an instance of ListPathEvent, so your function must inherit that

    :param path: The path to be listed
    :param callback: The callback function which will be executed under os.walk(path)
    :return: None
    """
    for dirpath, dirnames, filenames in os.walk(path):
        if dirpath.startswith(DOT):
            continue

        valid_function : bool = ((not callback is None) and (isinstance(callback, ListPathEvent)))
        if (valid_function):
            callback.setVars(path, dirpath, dirnames, filenames)
            callback.run()


def changeExtension(entry : str, to_ext : str):
    """
    Change a filename with an extension to another, if a file extension exists. If not,
    the new extension WON'T be attached.
    :param entry: The filename entry expecting to have an extension
    :param to_ext: The extension to change to
    :return: A filename with new extension if the file already has an extension
    """
    new_entry = entry
    r_index : int = entry.rfind(DOT)
    has_dot : boot = (r_index >= 0)
    if (has_dot):
        new_entry = entry[:r_index]+to_ext
    return new_entry


def writeFile(file_name : str, text : str):
    """
    Write the text content to a file with the name provided

    :param file_name: the name of the file to be written to (included path)
    :param text: The text with content to be written
    :return: None
    """
    try:
        with open(file_name, "w+") as f:
            f.write(text)
            f.close()
    except Exception as e:
        print("Error: " + str(e))
        exit(1)

def writeExecutableShellScript(executable_entry_list : list, exec_directory : str):
    """
    Write a shell script that can be executed from shell/command line environment.
    :param executable_entry_list: The list of commands including parameters to be executed
    :param exec_directory: The directory where the above commands are to be executed from
    :return: None
    """
    text_for_entries : str = os.linesep.join(executable_entry_list)
    cd_exec_dir_text : str = "cd {}{}".format(exec_directory, os.linesep)
    writing_text : str = "{} Run this script to remove spurious PO files that should no longer be there.{}{}{}{}".\
        format(COMMENT_FLAG, os.linesep, cd_exec_dir_text, text_for_entries, os.linesep)
    writeFile(REMOVAL_SCRIPT_PATH, writing_text)


# -----------------------------------------------------------------------------
# Locale Checks
def warn_locale():
    """
    Check for stale of PO files to see if the corresponding RST entry exists.
    If not, list non-exist entries into a file and instruct users to execute that script file
    to remove unwanted entries.

    If no entries are found (ie. for every PO files there exists a corresponding RST entry) then
    NO message and no script file are produced.
    """
    find_by_dir=findParentDir(SVN)
    listPath(LOCALE_DIR, find_by_dir)
    if (not find_by_dir.result):
        raise Exception("Unable to find SVN directory.")

    locale_dir = find_by_dir.result
    find_by_dir = findParentDir(PO_FIND_DIR)
    listPath(locale_dir, find_by_dir)
    po_dir = find_by_dir.result

    """
    Example how to use findFileByName using regular expression, listing out all index.po files
    
    f_name = findFileByName("ind.*\.po")
    listPath(po_dir, f_name)
    result = f_name.result
    print("result:{}".format(result))    
    """

    len_local_dir = len(locale_dir)
    po_dir_patch_part = po_dir[len_local_dir:]

    find_po_files = findFileByExtensionRelative(PO)
    listPath(po_dir, find_po_files)
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
