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


class FindFuzzy:
    from_vipo_path="/home/htran/blender_documentations/new_po/vi.po"
    output_file="/home/htran/replaced_vi.po"

    def setVars(self, input_file=None):
        self.input_file=(FindFuzzy.from_vipo_path if (input_file == None) else input_file)

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

            is_fuzzy = (po_entry.fuzzy)
            if (not is_fuzzy):
                continue

            self.printMSGID(k)
            self.printMSGSTR(s)
            self.printSeparator()


parser = ArgumentParser()
##parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
#parser.add_argument("-c", "--ctx", dest="msgctxt", help="Context of the message")
#parser.add_argument("-i", "--id", dest="msgid", help="ID of the message")
#parser.add_argument("-s", "--str", dest="msgstr", help="Translation of the message")
#parser.add_argument("-r", "--rep", dest="rep_txt", help="Replace text for MSGSTR")
#parser.add_argument("-I", "--Insen", dest="insensitive", help="Find case insensitive MODE", action='store_true', default=False)
##parser.add_argument("-R", "--REPLACE", dest="Action_Replace", help="Action to replace MSGSTR entry with entered text", action='store_const', const=True)
parser.add_argument("-f", "--file", dest="input_file", help="Input PO file")

args = parser.parse_args()

x = FindFuzzy();
x.setVars(args.input_file)
x.run()
