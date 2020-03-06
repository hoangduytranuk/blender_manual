#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""

import sys
#sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
sys.path.append("/home/htran/bin/python/PO")
sys.path.append("/home/htran/bin")
#print("sys.path:", sys.path)
#exit(0)
import re
import os
import io

from sphinx_intl import catalog as cat
from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile
from pprint import pprint as pp
from argparse import ArgumentParser


class FindVIPO:
    from_vipo_path="/home/htran/blender_documentations/new_po/vi.po"
    output_file="/home/htran/replaced_vi.po"

    def setVars(self, msgctx = None, msgid = None, msgstr = None, rep_txt=None, case_insensitive=True, input_file=None, exclude_id=None, exclude_str=None):
        self.msgctx = msgctx
        self.msgid = msgid
        self.msgstr = msgstr
        self.rep_txt = rep_txt
        self.is_replace = (rep_txt != None)
        self.case_insensitive = case_insensitive
        self.input_file=(FindVIPO.from_vipo_path if (input_file == None) else input_file)
        self.exclude_id=exclude_id
        self.exclude_str=exclude_str

        #print("self.input_file:", self.input_file)
        print("self.case_insensitive:", self.case_insensitive)
        #exit(0)

    def printMSGCTXT(self, c):
        print("msgctxt \"{}\"".format(c))

    def printMSGID(self, k):
        print("msgid \"{}\"".format(k))

    def printMSGSTR(self, s):
        print("msgstr \"{}\"".format(s))

    def printSeparator(self):
        print("="*50)

    def replaceMSGSTR(self, find_pattern, replace_pattern, orig_text):
        new_text = orig_text
        if (self.is_replace):
            #new_text = re.sub(find_pattern, replace_pattern, text, count=??)
            new_text = find_pattern.sub(replace_pattern, orig_text)
        return new_text

    def dump_po(self, filename, catalog):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        with io.open(filename, 'wb') as f:
            pofile.write_po(f, catalog, width=4096)

    def run(self):
        c = None
        k = None
        s = None

        find_c = self.msgctx
        find_k = self.msgid
        find_s = self.msgstr
        rep_txt = self.rep_txt
        ex_msgid = self.exclude_id
        ex_msgstr = self.exclude_str

        is_find_context = (find_c != None)
        is_find_msgid = (find_k != None)
        is_find_msgstr = (find_s != None)
        is_replace = (rep_txt != None)
        is_exclude_msgid = (ex_msgid != None)
        is_exclude_msgstr = (ex_msgstr != None)
        msgid_exclude_p = None
        msgstr_exclude_p = None


        is_valid = (is_find_context or is_find_msgid or is_find_msgstr or is_replace)

        if not is_valid:
            return


        context_p = msgid_p = msgstr_p = None
        if (self.case_insensitive):
            if (is_find_context):
                context_p = re.compile(find_c, flags=re.I)
            if (is_find_msgid):
                msgid_p = re.compile(find_k, flags=re.I)
            if (is_find_msgstr):
                msgstr_p = re.compile(find_s, flags=re.I)
            if (is_exclude_msgid):
                msgid_exclude_p = re.compile(ex_msgid, flags=re.I)
            if (is_exclude_msgstr):
                msgstr_exclude_p = re.compile(ex_msgstr, flags=re.I)
        else:
            if (is_find_context):
                context_p = re.compile(find_c)
            if (is_find_msgid):
                msgid_p = re.compile(find_k)
            if (is_find_msgstr):
                msgstr_p = re.compile(find_s)
            if (is_exclude_msgid):
                msgid_exclude_p = re.compile(ex_msgid)
            if (is_exclude_msgstr):
                msgstr_exclude_p = re.compile(ex_msgstr)


        changed = False
        po_cat = cat.load_po(self.input_file)
        for index, po_entry in enumerate(po_cat):
            is_changed = False
            is_first_entry = (index == 0)
            if (is_first_entry):
                continue

            c = po_entry.context
            k = po_entry.id
            s = po_entry.string

            is_found_msgctx = False
            is_found_msgid = False
            is_found_msgstr = False
            is_found_exclude_msgid = False
            is_found_exclude_msgstr = False

            if (is_find_context):
                is_found_msgctx = (c != None) and (len(c) > 0) and (context_p.search(c) != None)

            if (is_find_msgid):
                is_found_msgid = (k != None) and (len(k) > 0) and (msgid_p.search(k) != None)
                if (is_found_msgid):
                    is_found_exclude_msgid = (is_exclude_msgid) and (msgid_exclude_p.search(k) != None)
                    is_found_msgid = (not is_found_exclude_msgid)

            if (is_find_msgstr):
                is_found_msgstr = (s != None) and (len(s) > 0) and (msgstr_p.search(s) != None)
                if (is_found_msgstr):
                    is_found_exclude_msgstr = (is_exclude_msgstr) and (msgstr_exclude_p.search(s) != None)
                    is_found_msgstr = (not is_found_exclude_msgstr)


            #0 0 0

            #0 0 1
            #0 1 0
            #0 1 1

            #1 0 0
            #1 0 1
            #1 1 0

            #1 1 1

            p1 = (not is_find_context and not is_find_msgid and is_find_msgstr) and (is_found_msgstr)
            p2 = (not is_find_context and is_find_msgid and not is_find_msgstr) and (is_found_msgid)
            p3 = (not is_find_context and is_find_msgid and is_find_msgstr) and (is_found_msgid and is_found_msgstr)

            p4 = (is_find_context and not is_find_msgid and not is_find_msgstr) and (is_found_msgctx)
            p5 = (is_find_context and not is_find_msgid and is_find_msgstr) and (is_found_msgctx and is_found_msgstr)
            p6 = (is_find_context and is_find_msgid and not is_find_msgstr) and (is_found_msgctx and is_found_msgid)

            p7 = (is_find_context and is_find_msgid and is_find_msgstr) and (is_found_msgctx and is_found_msgid and is_found_msgstr)

            is_replacing = (is_replace and (p1 or p3 or p5 or p7))
            if (is_replacing):
                old_text = str(s)
                new_text = msgstr_p.sub(rep_txt, s)
                po_entry.string = new_text
                is_changed = (old_text != new_text)
                if (is_changed):
                    s = new_text
                    changed = True


            if (p1):
                self.printMSGSTR(s)
            elif (p2):
                self.printMSGID(k)
            elif (p3):
                self.printMSGID(k)
                self.printMSGSTR(s)
            elif (p4):
                self.printMSGCTXT(c)
            elif (p5):
                self.printMSGCTXT(c)
                self.printMSGSTR(s)
            elif (p6):
                self.printMSGCTXT(c)
                self.printMSGID(k)
            elif (p7):
                self.printMSGCTXT(c)
                self.printMSGID(k)
                self.printMSGSTR(s)

            is_found = (p1 or p2 or p3 or p4 or p5 or p6 or p7)
            if (is_found):
                self.printSeparator()


        if (changed):
            print("Writting changes to:", FindVIPO.output_file)
            self.dump_po(FindVIPO.output_file, po_cat)


parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-c", "--ctx", dest="msgctxt", help="Context of the message")
parser.add_argument("-i", "--id", dest="msgid", help="ID of the message")
parser.add_argument("-s", "--str", dest="msgstr", help="Translation of the message")
parser.add_argument("-r", "--rep", dest="rep_txt", help="Replace text for MSGSTR")
parser.add_argument("-xi", "--exclude_id", dest="exclude_id", help="Exclude all founds in MSGID")
parser.add_argument("-xs", "--exclude_str", dest="exclude_str", help="Exclude all founds in MSGSTR")
parser.add_argument("-I", "--Insen", dest="insensitive", help="Find case insensitive MODE", action='store_true', default=False)
#parser.add_argument("-R", "--REPLACE", dest="Action_Replace", help="Action to replace MSGSTR entry with entered text", action='store_const', const=True)
parser.add_argument("-f", "--file", dest="input_file", help="Input PO file")

args = parser.parse_args()

print(args)

x = FindVIPO();
x.setVars(args.msgctxt, args.msgid, args.msgstr, args.rep_txt, args.insensitive, args.input_file, args.exclude_id, args.exclude_str)
x.run()
