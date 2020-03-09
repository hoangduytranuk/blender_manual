#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""

import os
import io
from argparse import ArgumentParser
from sphinx_intl import catalog as c
from babel.messages import pofile

class FlatPOText:

    def __init__(self, po_path, dry_run):
        self.po_path = po_path
        valid_dir = (po_path is not None) and (os.path.isdir(po_path))
        if not valid_dir:
            raise Exception("Path provided is not valid or inaccessible. Aborted!")

        self.dry_run = (True if dry_run is not None else False)

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
        try:
            self.po_file_list = self.getPOFileList()
            for po_file in self.po_file_list:
                po_doc = c.load_po(po_file)
                if self.dry_run:
                    print("File to be flatted:", po_file)
                else:
                    #self.dump_po(po_file, po_doc)
                    c.dump_po(po_file, po_doc)
        except Exception as e:
            print(e)
            print(po_file)


parser = ArgumentParser()
parser.add_argument("-d", "--dir", dest="po_dir", help="Directory where PO files resided.")
parser.add_argument("-r", "--dry", dest="dry_run", help="Listing out possible changes but do not commit changes", action='store_const', const=True)

args = parser.parse_args()

x = FlatPOText(args.po_dir, args.dry_run)
x.run()
