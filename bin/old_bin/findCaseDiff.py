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

from sphinx_intl import catalog as c
from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile
from pprint import pprint as pp

class Comparator(object):

    def setItem(a, b):
        self.a=a
        self.b=b
        os.

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

class FindCaseDiff:
    from_vipo_path="/home/htran/blender_documentations/new_po/vi.po"

    def __init__(self):
        self.po_cat = c.load_po(FindCaseDiff.from_vipo_path)
        self.sorted_po_cat = None

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


    def countWordWithTitleCase(self, s):
        s_list = re.findall(r'(\w+)|(\W+)', s)
        count=0
        list_upper_word=[]
        for w in s_list:
            is_upper_word = (w.istitle() or w.isupper())
            count = (count + 1) if (is_upper_word) else (count)
            if (is_upper_word):
                list_upper_word.append(w)
        return count, list_upper_word

    def run(self):
        changed = False
        for index, pot_entry in enumerate(self.po_cat):
            is_first_entry = (index == 0)
            if (is_first_entry):
                continue

            k = pot_entry.id
            s = pot_entry.string

            k_count, k_w_list = self.countWordWithTitleCase(k)
            s_count, s_w_list = self.countWordWithTitleCase(s)
            is_report = (s_count < k_count)

            if (is_report):
                #print("Find possible undercased instance: ")
                print("msgid \"{}\"".format(k))
                pp(k_w_list)
                print("msgstr \"{}\"".format(s))
                pp(s_w_list)
                print("--")

        if (changed):
            new_po_file = "/home/htran/new_vi.po"
            print("Saving content of new pot_cat to:{}".format(new_po_file))
            self.dump_po(new_po_file, self.pot_cat)


x = FindCaseDiff();
x.run()
