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
from argparse import ArgumentParser

#from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile
from pprint import pprint as pp
from collections import OrderedDict, defaultdict

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

class UpdateVIPO:
    from_vipo_path="/Users/hoangduytran/blender_manual/gui/2.80/po/vi.po"
    to_blender_pot_path="/Users/hoangduytran/blender_gui/blender.pot"

    def __init__(self):
        self.sorted_po_cat = None
        self.from_vipo = None
        self.to_vipo = None
        self.is_dry_run = False

    def setVars(self, from_vipo, to_vipo, is_dry_run):
        self.from_vipo = (from_vipo if (from_vipo is not None) else UpdateVIPO.from_vipo_path)
        self.to_vipo = (to_vipo if (to_vipo is not None) else UpdateVIPO.to_blender_pot_path)
        self.is_dry_run = (True if is_dry_run else False)

    def loadFiles(self):
        self.po_cat = c.load_po(self.from_vipo)
        self.pot_cat = c.load_po(self.to_vipo)

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
            print("poCatToDic:", k, v)
            if not is_same_key:
                lower_entry = {lower_k:v}
                po_cat_dic.update(lower_entry)

        return po_cat_dic


    def binarySearch(self, sorted_list, po_entry, is_lcase=False):
        '''
        :arg
        '''
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
        po_cat_dict = self.poCatToDic(self.po_cat)
        print("po_cat_dict")
        pp(po_cat_dict)

        po_pot_dict = self.poCatToDic(self.pot_cat)
        print("po_pot_dict")
        pp(po_pot_dict)

        ignore_list ={
            ("Volume", "Sound"):"Âm Lượng",
            ("volume", "sound"):"Âm Lượng",
            ("Volume", ""):"Thể Tích",
            ("volume", ""):"Thể Tích",
            #("",""):"",
        }

        changed = False
        for index, item in enumerate(po_pot_dict.items()):
            if index == 0:
                continue

            k, v = item
            is_ignore = (k in ignore_list)
            if is_ignore:
                ignore_value = ignore_list[k]
                v.string = ignore_value
                print("Ignoring item:", k, v.string)
                continue

            print("run:", k, v)

            is_in_old_dict = (k in po_cat_dict)
            if not is_in_old_dict:
                print("NEW ENTRY k:[{}], v:[{}]".format(k, v))
                continue

            old_dict_entry = po_cat_dict[k]

            old_dict_entry_msgid = old_dict_entry.id
            old_dict_entry_msgstr = old_dict_entry.string
            is_fuzzy = old_dict_entry.fuzzy

            has_translation = (old_dict_entry_msgstr is not None) and (len(old_dict_entry_msgstr) > 0)
            if not has_translation:
                print("IGNORED No translation k:[{}], v:[{}]".format(k, v))

            v.string = old_dict_entry_msgstr
            if is_fuzzy:
                v.flags.add('fuzzy')

            print("Updating k[{}], v:[{}], fuzzy:[{}]".format(k,v, is_fuzzy))
            changed = True

        if (changed and not self.is_dry_run):
            new_po_file = "/Users/hoangduytran/new_vi_0001.po"
            print("Saving content of new pot_cat to:{}".format(new_po_file))
            #self.dump_po(new_po_file, self.pot_cat)
            c.dump_po(new_po_file, self.pot_cat)

        print("Transferred translations from:", self.from_vipo, "to:", self.to_vipo, "is_dry_run:", self.is_dry_run)

parser = ArgumentParser("UpdateVIPO, transfer translations from a vi.po file to another")
parser.add_argument("-f", "--from_file", dest="from_file", help="Source file, where translations are taken from.")
parser.add_argument("-t", "--to_file", dest="to_file", help="Target file, where translations in from_file will be copied to.")
parser.add_argument("-r", "--dry_run", dest="dry_run", help="Run in testing mode. Do not write changes out.", action='store_const', const=True)
args = parser.parse_args()

x = UpdateVIPO()
x.setVars(args.from_file, args.to_file, args.dry_run)
x.run()
