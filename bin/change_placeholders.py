#!/usr/bin/env python3
import argparse
import os
import sys
import re
import subprocess as SP
from datetime import datetime
import pytz

from pprint import pprint as pp

YOUR_NAME="Hoang Duy Tran"
YOUR_EMAIL="hoangduytran1960@googlemail.com"
YOUR_ORG_CONTACT=YOUR_EMAIL
YOUR_CITY="London"
YOUR_COUNTRY="UK"
YOUR_ID="{} <{}>".format(YOUR_NAME, YOUR_EMAIL)
YOUR_TRANSLATION_TEAM="{}, {} <{}>".format(YOUR_CITY, YOUR_COUNTRY, YOUR_ORG_CONTACT)
YOUR_LANGUAGE_CODE="vi"
RE_COMMENTED_LINE="^#~.*$"


class ChangePlaceHolder:
    def __init__(self):
        self.file_list=[]
        self.file = None
        self.dir = None
        self.dryrun = False
        self.listing = False
        self.time_now = self.getTimeNow()
        self.po_revision_date_value="PO-Revision-Date: {}".format(self.time_now)
        self.pattern_list = {
            "FIRST AUTHOR.*SS>":"{}".format(YOUR_ID),
            "Last-Translator.*>":"Last-Translator: {}".format(YOUR_ID),
            "PO-Revision-Date.*[[:digit:]]\{4\}":self.po_revision_date_value,
            "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE":self.po_revision_date_value,
            "Language-Team:.*>":"Language-Team: {}".format(YOUR_TRANSLATION_TEAM)
        }

        #This is for the language line. This line is required by POEdit, if you're using it for editing PO files.
        #Inserting this line before the MIME-Version.
        re_language_code="Language:.*{}".format(YOUR_LANGUAGE_CODE)
        language_code=r'\"Language: ' + YOUR_LANGUAGE_CODE + r'\\n\"\n'
        self.pattern_insert={
            "\"MIME-Version":"{}\"MIME-Version".format(language_code)
        }


    def __repr__(self):
        try:
            v = (self.file if self.file else "")
            print("self.file:", v)

            v = (self.dir if self.dir else "")
            print("self.dir:", v)

            print("self.dryrun:", self.dryrun)
            print("self.listing:", self.listing)
            print("self.file_list:")
            pp(self.file_list)
        except Exception as e:
            return ""


    def getTimeNow(self):
        tz_london = pytz.timezone('Europe/London')
        datetime_london = datetime.now(tz_london)
        current_time = datetime_london.strftime("%Y-%m-%d %H:%M%z")
        return current_time

    def setVars(self, file=None, dir=None, listing_only=None, dryrun_only=None):
        self.file = file
        self.dir = dir
        self.listing = (listing_only if listing_only is not None else False)
        self.dryrun = (dryrun_only if dryrun_only is not None else False)

    def runShellCommand(self, cmd):
        result_list = None
        try:
            result = SP.run(cmd, shell=True, stdout=SP.PIPE, stderr=SP.STDOUT, universal_newlines=True)
        except SP.CalledProcessError as err:
            print("Error:", err)
        else:
            
            result_list=result.stdout.split()
            # print("result:", result_list)
        return result_list

    def findChangedFiles(self):
        pass

    def run(self):
        print("Hoang Duy Tran")
        cmd = "svn status | grep -e 'po$' | awk '{print $2}'"
        cmd = "git status | grep -e 'modified' | grep  -e 'po$' | awk '{print $2}'"
        result_list = self.runShellCommand(cmd)
        if result_list:
            pp(result_list)

        #stdout, stderr = result.communicate()
        # print("stdout:\n", result.stdout.decode('utf-8'))
        #print("stderr:\n", stderr)
        


parser = argparse.ArgumentParser(description="Processing Arguments for change place holders")

parser.add_argument('-f', dest='file', type=str, help='Peform on a specific file.')
parser.add_argument('-d', dest='dir', type=str, help='Peform on a specific directory.')
parser.add_argument('-l', dest='listing', help='Peform actions by listing only affected files but DO NOT write changes. For Debugging purposes and validate the action.', action='store_true')
parser.add_argument('-r', dest='dryrun', help='Peform actions as if it was running but DO NOT write changes. For Debugging purposes and validate the action.', action='store_true')

args = parser.parse_args()

x = ChangePlaceHolder()
x.setVars(file=args.file, dir=args.dir, listing_only=args.listing, dryrun_only=args.dryrun)
# print(x)
x.run()

