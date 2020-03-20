#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Apache License, Version 2.0

# This script is to reduce tedious steps involved when updating PO files.
# It helps replacing generated placeholders string in your PO files, especially
# when updating PO files, automatically inserting name of author and revision time,
# which should save you some times.
# Recommend to copy this to your $HOME/bin directory and add executable flag (chmod u+x),
# then use it with the directory of your local repository (svn or git), ie.
# 		$HOME/bin/change_placeholders.py -d $BLENDER_MAN_EN -t 1d
# 		$HOME/bin/change_placeholders.py -f $BLENDER_MAN_EN/locale/vi/LC_MESSAGES/index.po
# Windows users can try to install Linux on Windows following this guide (https://docs.microsoft.com/en-us/windows/wsl/install-win10)
# Author: Hoang Duy Tran <hoangduytran1960@gmail.com>
# Revision Date: 2020-02-02 09:59+0000
#
import os
import re
import locale
import datetime
from time import gmtime, strftime, time
from pytz import timezone
from argparse import ArgumentParser
from subprocess import PIPE, Popen, run
from math import fabs
from pprint import pprint as pp
from sphinx_intl import catalog as c
from babel.messages import pofile
import enum

#Leave the variables here to make them obvious and easier to change
YOUR_NAME = "Hoang Duy Tran"
YOUR_EMAIL = "hoangduytran1960@gmail.com"
YOUR_ID = "{} <{}>".format(YOUR_NAME, YOUR_EMAIL)
YOUR_TRANSLATION_TEAM = "London, UK <{}>".format(YOUR_EMAIL)
YOUR_LANGUAGE_CODE = "vi"
TIME_ZONE='Europe/London' # this value can be optained using the code 'import pytz; for entry in pytz.all_timezones(); print(entry)'

#header default values, for internal uses only
default_first_author = "FIRST AUTHOR"
default_mail_address = "MAIL@ADDRESS"
default_year = ", YEAR."

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
            ext = os.path.splitext(filename)[1]
            is_valid = filename.lower().endswith(self.search_extension.lower())
            if (is_valid):
                entry=os.path.join(self.dirpath, filename)
                self.result.append(entry)

    def getModificationTime(self, name):
        path = os.path.join(self.dirpath, name)
        return os.path.getmtime(path)

    def getListSorted(self, key_function=None, is_reversed=False):
        #print("getListSorted:", self.result)
        sorted_list = sorted(self.result, key=key_function, reverse=is_reversed)
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
                data = f.read();
            return data
        except Exception as e:
            print("ERROR reading file:", file_name)
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
                callback.setVars(dirpath, dirnames, filenames)
                callback.run()

#  def __init__(self, locale=None, domain=None, header_comment=DEFAULT_HEADER,
#                  project=None, version=None, copyright_holder=None,
#                  msgid_bugs_address=None, creation_date=None,
#                  revision_date=None, last_translator=None, language_team=None,
#                  charset=None, fuzzy=True):

# from babel.dates import UTC
# created = datetime(1990, 4, 1, 15, 30, tzinfo=UTC)
# revised = datetime(1990, 8, 3, 12, 0, tzinfo=UTC)
#  >>> catalog = Catalog(locale='de_DE', project='Foobar', version='1.0',
#     ...                   creation_date=created, revision_date=revised,
#     ...                   last_translator='John Doe <jd@example.com>',
#     ...                   language_team='de_DE <de@example.com>')

class ChangePlaceHolder:

    CONVERT_M = 60
    CONVERT_H = CONVERT_M * 60
    CONVERT_D = CONVERT_H * 24
    CONVERT_W = CONVERT_D * 7

    def __init__(self):       

        self.PO_MSGID_MSGSTR = re.compile(r'msgid.*\nmsgstr', re.MULTILINE)
        self.RE_COMMENTED_LINE= r'^#~.*$'
        self.TIME_INPUT_PATTERN=re.compile(r'[\d]+[smhdw]')

        self.basic_io = BasicIO()

        self.specific_dir = None
        self.specific_file = None
        self.specific_time = False

    def setVars(self, specific_file: str, specific_dir, dir_force_mode, dry_run, list_dir_only, specific_time, change_modi_time):
        self.specific_file = specific_file
        has_file = (self.specific_file is not None)
        if has_file:
            is_file_there = os.path.isfile(self.specific_file)
            if not is_file_there:
                raise Exception("File provided:", self.specific_file, " is NOT accessible. Aborted!")

        self.specific_dir = specific_dir
        has_dir = (self.specific_dir is not None)
        if has_dir:
            is_dir_there = os.path.isdir(self.specific_dir)
            if not is_dir_there:
                raise Exception("Path for directory provided: ", self.specific_dir, " is NOT accessible. Aborted!")

        self.dry_run: bool = (True if dry_run else False)
        self.list_dir_only: bool = (True if list_dir_only else False)
        self.dir_force_mode = (True if dir_force_mode else False)

        self.specific_time = self.specificTimeToSeconds(specific_time)
        self.modi_time = (True if change_modi_time else False)

    def isPOFile(self, file_name):
        data = self.basic_io.readTextFile(file_name)
        has_msgid_msgstr = (self.PO_MSGID_MSGSTR.search(data) is not None)
        return has_msgid_msgstr

    def specificTimeToSeconds(self, period_string):
        # accepted format
        # 10s (10 seconds),
        # 5m (5 minutes)
        # 1h (1 hour),
        # 2d (2 days)
        valid = (period_string is not None) and (len(period_string) > 0)
        if not valid:
            return -1

        try:
            unit_part = period_string[-1]  # s|h|d
            digit_part = period_string[:-1]  # 10 etc..
            digits = int(digit_part)
            digits = fabs(digits)
        except Exception as e:
            print(e)
            print("Input data is invalid:", period_string)
            print("Unable to convert input [{}] into number of seconds".format(period_string))
            raise Exception("Period must be: digits + 's|h|d|w' (seconds|minutes|hours|days|week), e.g. 30s, 5m, 2h, 1d, 1w etc..")

        multiplier = 1
        if unit_part == "m":
            multiplier = ChangePlaceHolder.CONVERT_M
        elif unit_part == "h":
            multiplier = ChangePlaceHolder.CONVERT_H
        elif unit_part == "d":
            multiplier = ChangePlaceHolder.CONVERT_D
        elif unit_part == "w":
            multiplier = ChangePlaceHolder.CONVERT_W

        period_in_seconds = digits * multiplier
        return period_in_seconds

    def getTimeNow(self):
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        loc_dt=local_time.localize(datetime.datetime.now())
        formatted_dt=loc_dt.strftime(fmt)
        return formatted_dt

    def shellCommandRun(self, command):
        # print("shellCommandRun: [{}]".format(command))
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        return result.stdout

    def findChangedFiles(self, directory):
        valid_dir = (directory is not None) and (len(directory) > 0) and (os.path.isdir(directory))
        if not valid_dir:
            raise Exception("Invalid {}, Halted!".format(directory))

        git_dir = os.path.join(directory, ".git")
        svn_dir = os.path.join(directory, ".svn")

        has_git = os.path.isdir(git_dir)
        has_svn = os.path.isdir(svn_dir)

        git_cmd = "git status | grep \'modified\' | awk \'{ print $2 }\' | grep \".po$\""
        svn_cmd = "svn status | grep \'^[MA]\' | awk \'{ print $2 }\' | grep \".po$\""
        # normal_cmd = "find {} -name \"*.po\" -mtime -1 -print".format(directory)  # files modified last 24 hours
        # normal_cmd = "find {} -name \"*.po\" -mtime -100 -print".format(directory)  # files modified last 1 days

        if self.dir_force_mode:
            has_git = False
            has_svn = False
        
        file_list=[]
        msg = ""
        if has_git:
            msg = "has_git"
            output = self.shellCommandRun(git_cmd)
            file_list = output.split()
        elif has_svn:
            msg = "has_svn"
            output = self.shellCommandRun(svn_cmd)
            file_list = output.split()
        else:
            msg = "other"
            file_list = self.getLatestPOFiles(self.specific_dir)

        return file_list


    def removeCommentedLineInSingleFile(self, file_name):
        home_dir = os.environ['HOME']
        temp_file_name = "temp_file.po"
        tempfile= os.path.join(home_dir, temp_file_name)

        grep_cmd = "grep \"{}\" {}".format(self.RE_COMMENTED_LINE, file_name)
        not_comment_cmd = "grep -v \"{}\" {} > {}".format(self.RE_COMMENTED_LINE, file_name, tempfile)
        move_tempfile_to_origin_cmd = "mv {} {}".format(tempfile, file_name)

        exclude_lines=self.shellCommandRun(grep_cmd)
        is_empty = (len(exclude_lines.strip()) == 0)
        if not is_empty:
            print("Removing commented lines:")
            pp(exclude_lines)
            if self.dry_run:
                return
            self.shellCommandRun(not_comment_cmd)
            self.shellCommandRun(move_tempfile_to_origin_cmd)

    def removeCommentedLineInAllFiles(self, file_list):
        normal_cmd = "find . -name \"*.po\" -print"
        output = self.shellCommandRun(normal_cmd)
        file_list = output.split()
        for f in file_list:
            self.removeCommentedLineInSingleFile(f)

    def getLatestPOFiles(self, directory):
        mod_file_list = []
        valid = (directory is not None) and (len(directory) > 0) and os.path.isdir(directory)
        if not valid:
            return mod_file_list

        modi_file_callback = findFileByExtension(".po")
        self.basic_io.listDir(directory, modi_file_callback)
        mod_file_list = modi_file_callback.getListSortedModified(self.specific_time)

        return mod_file_list


    def replaceAndReport(self, changed_file):

        # these lines are taken from /Library/Python/3.7/site-packages/babel/messages/catalog.py
        # put here for references
        #
        # self.domain = domain
        # self.locale = locale
        # self._header_comment = header_comment
        # self._messages = OrderedDict()

        # self.project = project or 'PROJECT'
        # self.version = version or 'VERSION'
        # self.copyright_holder = copyright_holder or 'ORGANIZATION'
        # self.msgid_bugs_address = msgid_bugs_address or 'EMAIL@ADDRESS'

        # self.last_translator = last_translator or 'FULL NAME <EMAIL@ADDRESS>'
        # """Name and email address of the last translator."""
        # self.language_team = language_team or 'LANGUAGE <LL@li.org>'
        # """Name and email address of the language team."""

        # self.charset = charset or 'utf-8'

        # if creation_date is None:
        #   creation_date = datetime.now(LOCALTZ)
        # elif isinstance(creation_date, datetime) and not creation_date.tzinfo:
        #   creation_date = creation_date.replace(tzinfo=LOCALTZ)
        # self.creation_date = creation_date
        # if revision_date is None:
        #   revision_date = 'YEAR-MO-DA HO:MI+ZONE'
        # elif isinstance(revision_date, datetime) and not revision_date.tzinfo:
        #   revision_date = revision_date.replace(tzinfo=LOCALTZ)
        # self.revision_date = revision_date
        # self.fuzzy = fuzzy

        # self.obsolete = OrderedDict()  # Dictionary of obsolete messages
        # self._num_plurals = None
        # self._plural_expr = None

        cat_changed = False
        header_changed = False
        in_po_cat = c.load_po(changed_file)

        local_time=timezone(TIME_ZONE)
        time_now =local_time.localize(datetime.datetime.now())        
        if self.modi_time:
            change_time = time_now.strftime('%Y-%m-%d %H:%M%z')
            print("PO-Revision-Date:", change_time)
            in_po_cat.revision_date = time_now
            cat_changed = True

        is_you_last_translator = (YOUR_ID in in_po_cat.last_translator)
        if not is_you_last_translator:
            print("Last-Translator:", YOUR_ID)
            in_po_cat.last_translator=YOUR_ID
            cat_changed = True

        is_language_team_already_set = (YOUR_TRANSLATION_TEAM in in_po_cat.language_team)
        if not is_language_team_already_set:
            print("Language-Team:", YOUR_TRANSLATION_TEAM)
            in_po_cat.language_team=YOUR_TRANSLATION_TEAM
            cat_changed = True

        header = in_po_cat._get_header_comment()

        is_you_already_first_author = (YOUR_NAME in header) and (default_first_author not in header)
        if not is_you_already_first_author:
            print("FIRST AUTHOR <EMAIL@ADDRESS>", YOUR_ID)
            header = header.replace(default_first_author, YOUR_NAME)        
            header = header.replace(default_mail_address, YOUR_EMAIL)

            is_year_set = (header.find(default_year) < 0)
            if not is_year_set:
                year = time_now.strftime('%Y')
                print(default_year, year)
                actual_year = ", {}.".format(year)
                header = header.replace(default_year, actual_year)
            header_changed = True        
            in_po_cat.header_comment = header

        changed = (cat_changed or header_changed)
        if changed:
            if self.dry_run:
                print("Processing file:", changed_file)
                print("-" * 80)
            else:
                #self.basic_io.writeTextFile(changed_file, data)
                c.dump_po(changed_file, in_po_cat)
                print("Wrote changes to:", changed_file)

    def replaceAllChangedFiles(self, file_list):
        valid = (file_list is not None) and (len(file_list) > 0)
        if not valid:
            return

        for f in file_list:
            # print("Processing file:", f)
            self.removeCommentedLineInSingleFile(f)
            self.replaceAndReport(f)
            #print("-" * 80)

    def listFile(self, file_name):
        print("file:", file_name)
        print("-" * 80)
        data = self.basic_io.readTextFile(file_name)
        print(data)
        print("-" * 80)

    def run(self):

        has_specific_file = (self.specific_file is not None) and \
                  (len(self.specific_file) > 0) and \
                    os.path.isfile(self.specific_file)

        use_specific_file = has_specific_file and self.isPOFile(self.specific_file)
        if use_specific_file:
            if self.list_dir_only:
                self.listFile(self.specific_file)
                return
            self.removeCommentedLineInSingleFile(self.specific_file)
            self.replaceAndReport(self.specific_file)
        else:
            os.chdir(self.specific_dir)
            # cwd = os.getcwd()

            file_list = self.findChangedFiles(self.specific_dir)
            if self.list_dir_only:
                for f in file_list:
                    self.listFile(f)
                return

            self.replaceAllChangedFiles(file_list)

parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-f", "--file", dest="specific_file", help="Perform replacements on a specific file")
parser.add_argument("-d", "--dir", dest="specific_dir", help="Directory where changed files are searched for replacements")
parser.add_argument("-D", "--Dir", dest="specific_dir_force", help="Directory where changed files are searched for replacements, FORCE mode", action='store_const', const=True)
parser.add_argument("-r", "--dry", dest="dry_run", help="Listing out possible changes but do not commit changes", action='store_const', const=True)
parser.add_argument("-l", "--list", dest="list_dir_only", help="Listing files out only, do not perform any operations", action='store_const', const=True)
parser.add_argument("-m", "--mod_time", dest="change_modified_time", help="Change modification time to time of the system now. Default False, to avoid overwriting previously stamped time.", action='store_const', const=True)
parser.add_argument("-t", "--mtime", dest="modified_time_period", help="Time period to search for file's modified times. Acceptable format: digits + 's|m|h|d|w' (seconds|minutes|hours|days|weeks), e.g. 30s, 5m, 2h, 1d, 1w. Only used for free searching, not for git or svn status. This should only be used with searching a non 'svn' or non 'git' directories.")
args = parser.parse_args()

x = ChangePlaceHolder()
x.setVars(  args.specific_file, 
            args.specific_dir, 
            args.specific_dir_force,
            args.dry_run, 
            args.list_dir_only, 
            args.modified_time_period, 
            args.change_modified_time
            )
x.run()
