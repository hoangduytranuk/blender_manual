#!/usr/bin/python3
import sys
sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
sys.path.append("/home/htran/bin/python")

import os
from argparse import ArgumentParser
from PO.common import Common as cm
from sphinx_intl import catalog as c
from pprint import pprint as pp

class DiffVIPO:
    def __init__(self):
        pass

    def setVars(self, from_file, to_file):
        cm.assertFileExist(from_file)
        cm.assertFileExist(to_file)

        self.from_file = from_file
        self.to_file = to_file

    def binarySearch(self, sorted_list, po_entry):
        #found_item = Algo.binarySearch(self.block_list, msgid_entry, cmp=self.compareMSGID)

        lo = 0
        hi = len(sorted_list)
        mid = -1
        while (lo < hi):
            mid = (lo + hi) // 2
            kc, m = sorted_list[mid]
            po_entry_k = "{}{}".format(po_entry.id, po_entry.context)
            #print("ss_list_entry:{} <=> po_entry_msg:{}\n".format(ss_list_entry, po_entry_msg))
            if (kc == po_entry_k):
                return mid
            elif (kc < po_entry_k):
                #print("lo = mid + 1")
                lo = mid + 1
            else:
                #print("hi = mid")
                hi = mid
        return -1


    def dicToList(self, po_data):
        new_list = []
        for m in po_data:
            if (m.fuzzy): continue
            k = m.id
            c_t = m.context
            key="{}{}".format(k, c_t)
            new_list.append((key, m))
        return new_list

    def run(self):
        from_po_doc=c.load_po(self.from_file)
        print("From: {}; Loaded:{}".format(self.from_file, len(from_po_doc)))

        to_po_doc=c.load_po(self.to_file)
        print("To: {}; Loaded:{}".format(self.to_file, len(to_po_doc)))

        from_po_list = self.dicToList(from_po_doc)
        sorted_from_dic = sorted(from_po_list)

        #pp(sorted_from_dic)
        for m in to_po_doc:
            found_index = self.binarySearch(sorted_from_dic, m)
            is_found = (found_index >= 0)
            if (not is_found):
                if (m.context and len(m.context) > 0):
                    print("to_po_doc, INSERTED: id=[{}], context=[{}]".format(m.id, m.context))
                else:
                    print("to_po_doc, INSERTED: id=[{}]".format(m.id))
                print("")
                continue

        to_po_list = self.dicToList(to_po_doc)
        sorted_to_dic = sorted(to_po_list)
        for m in from_po_doc:
            found_index = self.binarySearch(sorted_to_dic, m)
            is_found = (found_index >= 0)
            if (not is_found):
                if (m.context and len(m.context) > 0):
                    print("from_po_doc, DELETED: id=[{}], context=[{}]".format(m.id, m.context))
                else:
                    print("from_po_doc, DELETED: id=[{}]".format(m.id))
                print("")
                continue







parser = ArgumentParser()
parser.add_argument("-f", "--from", dest="from_file", help="From PO file")
parser.add_argument("-t", "--to", dest="to_file", help="To PO file")
args = parser.parse_args()

x = DiffVIPO()
x.setVars(args.from_file, args.to_file)
x.run()
