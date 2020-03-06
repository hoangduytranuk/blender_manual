#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""

import sys
#sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
sys.path.append('/home/htran/bin/python/base')
sys.path.append('/home/htran/bin/python/PO')
sys.path.append('/home/htran/bin/python/event')
sys.path.append('/home/htran/bin/python/algorithm')

sys.path.append("/home/htran/bin")
#print("sys.path:", sys.path)
#exit(0)
import re
import os
import io

from argparse import ArgumentParser
from sphinx_intl import catalog as c
from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile
from pprint import pprint as pp
from pobase import POBasic

class Comparator(object):

    def setItem(a, b):
        self.a=a
        self.b=b

    def compare(self, a, b):
        pass

    def __eq__ (self):
        return (self.compare(self.a, self.b) == 0)

    def __lt__ (self):
        return (self.compare(self.a, self.b) < 0)

    def __gt__ (self, a, b):
        return (self.compare(self.a, self.b) > 0)



class POCaseComp(Comparator):
    def compare(self, a, b):
        pass

class UpdateTranslationFiles:
    from_vipo_path="/home/htran/blender_documentations/new_po/vi.po"
    to_blender_pot_path="/home/htran/blender_documentations/blender.pot"
    translation_default_dir="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"

    def __init__(self):
        self.po_cat = c.load_po(UpdateTranslationFiles.from_vipo_path)
        self.pot_cat = c.load_po(UpdateTranslationFiles.to_blender_pot_path)
        self.sorted_po_cat = None
        self.po_dir = UpdateTranslationFiles.translation_default_dir

    def setPODir(self, new_dir):
        is_valid = (new_dir != None) and (os.path.isfile(new_dir))
        if (is_valid):
            self.po_dir = new_dir
        print("Using translation directory:")
        print(self.po_dir)

    def poCatToList(self, po_cat):
        l=[]
        for index, m in enumerate(po_cat):
            context = m.context
            #print("context:{}".format(context))
            k = m.id
            v = m
            l.append((k, context, v))
        return l

    def binarySearch(self, sorted_list, po_entry, is_lcase=False):
        #found_item = Algo.binarySearch(self.block_list, msgid_entry, cmp=self.compareMSGID)
        is_debug = False
        is_debug_on = False
        ss_list = sorted_list
        lo = 0
        hi = len(ss_list)
        mid = -1
        while (lo < hi):
            mid = (lo + hi) // 2
            k, c, v = ss_list[mid]

            is_debug = (po_entry.id == "Random seed")
            if (not is_lcase):
                ss_list_entry = "{}{}".format(k,c)
                po_entry_msg = "{}{}".format(po_entry.id, po_entry.context)
                ss_list_entry_id = k
                po_entry_msg_id = po_entry.id
            else:
                ss_list_entry = "{}{}".format(k.lower(),c)
                po_entry_msg = "{}{}".format(po_entry.id.lower(), po_entry.context)
                ss_list_entry_id = k.lower()
                po_entry_msg_id = po_entry.id.lower()

            is_equal = (ss_list_entry == po_entry_msg) or (ss_list_entry_id == po_entry_msg_id)
            if (is_debug):
                print("ss_list_entry:", ss_list_entry)
                print("po_entry_msg:", po_entry_msg)
                print("is_equal:", is_equal)

            if (is_equal):
                return v
            elif (ss_list_entry < po_entry_msg):
                #print("lo = mid + 1")
                lo = mid + 1
            else:
                #print("hi = mid")
                hi = mid
        #print("Not found")
        #exit(0)
        return -1


    def dump_po(self, filename, catalog):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        with io.open(filename, 'wb') as f:
            pofile.write_po(f, catalog, width=4096)


    def dealWithEntry(self, found_entry, target_entry):
                #print("is po_entry a Message:{}".format(isinstance(po_entry, Message)))
                #exit(0)
                #is_fuzzy = ('fuzzy' in po_entry.flags)
        print("dealing with target_entry:", target_entry.id)
        print("using found_entry:", found_entry.string)


        #if (found_entry.fuzzy):
            #pot_entry.flags.add('fuzzy')

        #print("pot_entry.id:{}, pot_entry.string:{}, pot_entry.fuzzy:{}".format(pot_entry.id, pot_entry.string, pot_entry.fuzzy))
        print("--"*5)
        return False


    def run(self):
        po_dic = self.poCatToList(self.po_cat)
        self.sorted_po_cat = sorted(po_dic, key = lambda x: "{}{}".format(x[0], x[1]))
        self.sorted_lower_po_cat = sorted(po_dic, key = lambda x: "{}{}".format(x[0].lower(), x[1]))

        getter = POBasic(self.po_dir, False)
        po_dir_list = getter.getSortedPOFileList()

        #pp(po_dir_list)

        #exit(0)
        trans_cat = None
        #pp(self.sorted_po_cat)
        #exit(0)
        changed = False
        for file_index, trans_path in enumerate(po_dir_list):
            print("File:", trans_path)
            print("-"*80)
            trans_cat = c.load_po(UpdateTranslationFiles.to_blender_pot_path)
            for index, pot_entry in enumerate(trans_cat):
                is_first_entry = (index == 0)
                if (is_first_entry):
                    continue

                #print("id:{}, is_fuzzy:{}".format(po_entry.id, po_entry.fuzzy))

                #if (po_entry.fuzzy):
                    #exit(0)
                #else:
                    #continue

                k = pot_entry.id
                found_entry = self.binarySearch(self.sorted_po_cat, pot_entry)
                is_in = isinstance(found_entry, Message)

                if (not is_in):
                    #print("Find in lower case list: ", k)
                    found_entry = self.binarySearch(self.sorted_lower_po_cat, pot_entry, is_lcase=True)
                    is_in = isinstance(found_entry, Message)
                    if (not is_in):
                        #print("Not Found, NEW: {}".format(k))
                        continue


                changed = self.dealWithEntry(found_entry, pot_entry)

            if (changed):
                new_po_file = "/home/htran/new_vi.po"
                print("Saving content of new pot_cat to:{}".format(new_po_file))
                self.dump_po(new_po_file, trans_cat)


parser = ArgumentParser()
parser.add_argument("-p", "--po", dest="po_dir", help="The PO directory from which PO files are to be changed.")
#parser.add_argument("-v", "--vipo", dest="vi_po_path", help="The path of vi.po directory to which translation are taken from")
args = parser.parse_args()

#print("args: {}".format(args))

x = UpdateTranslationFiles();
x.setPODir(args.po_dir)
x.run()
