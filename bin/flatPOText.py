#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')

import os
import io
from argparse import ArgumentParser
from sphinx_intl import catalog as c
from babel.messages import pofile

class FlatPOText:

    def __init__(self, file_path, to_file, is_sorted):
        # self.po_path = "/Users/hoangduytran/blender_docs/locale/vi/LC_MESSAGES"
        self.po_path = file_path
        self.to_path = to_file
        self.is_sorted = (True if is_sorted else False)

    # def dump_po(self, filename, catalog):
    #     dirname = os.path.dirname(filename)
    #     if not os.path.exists(dirname):
    #         os.makedirs(dirname)
    #
    #     # Because babel automatically encode strings, file should be open as binary mode.
    #     with io.open(filename, 'wb') as f:
    #         pofile.write_po(f, catalog, width=0)

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
        if extra_message is not None:
            print("{}".format(extra_message))


    def run(self):
        data = c.load_po(self.po_path)
        out_path = (self.to_path if self.to_path else self.po_path)
        if data:
            if out_path == self.po_path:
                msg = 'Do you want to overwrite existing file(Y/n)?'
                confirm = input(msg)
                is_yes = (confirm.lower() == 'y')
                if not is_yes:
                    exit(0)
            
            c.dump_po(out_path, data, line_width=4069, sort_output=self.is_sorted)

        # #exit(0)
        # self.po_file_list = self.getPOFileList()
        # for po_file in self.po_file_list:
        #     po_doc = c.load_po(po_file)
        #     #po_file = "/home/htran/test_vi.po"
        #     self.dump_po(po_file, po_doc)

parser = ArgumentParser()
parser.add_argument("-f", "--from_file", dest="from_file", help="PO files to process.")
parser.add_argument("-t", "--to_file", dest="to_file", help="Output changes to this PO file.")
parser.add_argument("-s", "--sort_by_id", dest="sort_by_id", help="Sort the output PO file by msgid.", action='store_const', const=True)
args = parser.parse_args()

x = FlatPOText(args.from_file, args.to_file, args.sort_by_id)
x.run()
