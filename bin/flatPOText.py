#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""

import sys
sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
sys.path.append("/home/htran/bin/python/PO")
sys.path.append("/home/htran/bin")

import re
import os
import io

from sphinx_intl import catalog as c
from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile

class FlatPOText:

    def __init__(self):
        self.po_path="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"

    def dump_po(self, filename, catalog):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        with io.open(filename, 'wb') as f:
            pofile.write_po(f, catalog, width=0)

    def getPOFileList(self):
        po_file_list=[]
        for dirpath, dirnames, filenames in os.walk(self.po_path):
            for filename in filenames:
                po_file = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(po_file)
                #basename = relpath(base, self.po_path)
                is_po_file = (ext == ".po")
                #print("po_file:{}, extension:{}, is_po_file:{}".format(po_file, ext, is_po_file))
                if (is_po_file):
                    po_file_list.append(po_file)

        return sorted(po_file_list)

    def printMessageEntry(self, m, extra_message=None):
        print("msgid: [{}]".format(m.id))
        print("msgstr:[{}]".format(m.string))
        if (extra_message != None):
            print("{}".format(extra_message))


    def run(self):
        #exit(0)
        self.po_file_list = self.getPOFileList()
        for po_file in self.po_file_list:
            po_doc = c.load_po(po_file)
            #po_file = "/home/htran/test_vi.po"
            self.dump_po(po_file, po_doc)

x = FlatPOText()
x.run()
