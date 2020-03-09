#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""

import sys
#sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
#sys.path.append("/home/htran/bin/python/PO")
#sys.path.append("/home/htran/bin")
#print("sys.path:", sys.path)
#exit(0)
import re
import os
import io
from sphinx_intl import catalog as c

#from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile
from pprint import pprint as pp
from collections import OrderedDict, defaultdict
from argparse import ArgumentParser

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

class CopyVIPOTrans:
    def __init__(self):
        self.from_file = None
        self.to_file = None
        self.dry_run = False

    def setVars(self, from_file, to_file, dry_run):
        self.from_file = from_file
        self.to_file = to_file
        self.dry_run = (True if dry_run else False)



    def loadFiles(self):
        valid_from_file = (self.from_file is not None) and (os.path.isfile(self.from_file))
        valid_to_file = (self.to_file is not None) and (os.path.isfile(self.to_file))
        valid = (valid_from_file and valid_to_file)
        if not valid:
            print("Source file:", self.from_file, "and/or Target File:", self.to_file, "is NOT VALID or doesn't exists, or cann't be accessed.")
            return

        self.from_po_cat = c.load_po(self.from_file)
        self.to_po_cat = c.load_po(self.to_file)

    def poCatToList(self, po_cat):
        l=[]
        for index, m in enumerate(po_cat):
            context = m.context
            #print("context:{}".format(context))
            k = m.id
            v = m
            l.append((k, context, v))
        return l

    def poCatToDic(self, po_cat):
        po_cat_dic = defaultdict(OrderedDict)
        for index, m in enumerate(po_cat):
            context = (m.context if m.context else "")
            #print("context:{}".format(context))
            k = (m.id, context)
            lower_k = (m.id.lower(), context.lower())

            is_same_key = (k == lower_k)

            v = m
            entry={k:v}
            po_cat_dic.update(entry)
            #print("poCatToDic:", k, v)
            if not is_same_key:
                lower_entry = {lower_k:v}
                po_cat_dic.update(lower_entry)

        return po_cat_dic


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


    def run(self):
        self.loadFiles()
        from_po_dict = self.poCatToDic(self.from_po_cat)
        to_po_dict = self.poCatToDic(self.to_po_cat)

        changed = False
        change_list={}
        for index, item in enumerate(to_po_dict.items()):
            if index == 0:
                continue

            k, to_v = item
            is_in_from = (k in from_po_dict)
            if not is_in_from:
                print("Entry doesn't exist in from source:")
                print(k)
                continue

            from_v:Message = from_po_dict[k]
            from_v_tran = from_v.string
            to_v_tran = to_v.string

            is_same = (from_v_tran == to_v_tran)
            if is_same:
                continue

            print("transfering translation:")
            print("from:", from_v_tran)
            print("replacing:", to_v_tran)

            to_v.string = from_v_tran
            entry={k:to_v}
            change_list.update(entry)
            # changed = True

        is_changed = (len(change_list) > 0)
        if not is_changed:
            print("Nothing to be updated.")
            return

        for k, v in change_list.items():
            to_po_dict[k] = v
            changed = True

        if (changed and not self.dry_run):
            print("Saving content of new pot_cat to:{}".format(self.to_file))
            #self.dump_po(self.to_file, self.to_po_cat)


parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-f", "--from_file", dest="from_file", help="File to copy the translations from.")
parser.add_argument("-t", "--to_file", dest="to_file", help="File where the translations will be replaced.")
parser.add_argument("-r", "--dry", dest="dryrun", help="Testing before commiting data, overwriting the target file", action='store_const', const=True)

args = parser.parse_args()

x = CopyVIPOTrans()
x.setVars(args.from_file, args.to_file, args.dryrun)
x.run()
