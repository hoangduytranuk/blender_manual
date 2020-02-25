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
    from_vipo_path="/home/htran/blender_documentations/new_po/vi.po"
    to_blender_pot_path="/home/htran/blender_documentations/blender.pot"

    def __init__(self):
        self.po_cat = c.load_po(UpdateVIPO.from_vipo_path)
        self.pot_cat = c.load_po(UpdateVIPO.to_blender_pot_path)
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
        #po_dic = self.poCatToList(self.po_cat)
        #self.sorted_po_cat = sorted(po_dic, key = lambda x: "{}{}".format(x[0], x[1]))
        #self.sorted_lower_po_cat = sorted(po_dic, key = lambda x: "{}{}".format(x[0].lower(), x[1]))

        po_cat_dict = self.poCatToDic(self.po_cat)
        print("po_cat_dict")
        pp(po_cat_dict)

        po_pot_dict = self.poCatToDic(self.pot_cat)
        print("po_pot_dict")
        pp(po_pot_dict)

        #pp(self.sorted_po_cat)
        #exit(0)
        changed = False
        for k, v in po_pot_dict.items():
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

        #for index, pot_entry in enumerate(self.pot_cat):
            #is_first_entry = (index == 0)
            #if (is_first_entry):
                #continue

            ##print("id:{}, is_fuzzy:{}".format(po_entry.id, po_entry.fuzzy))

            ##if (po_entry.fuzzy):
                ##exit(0)
            ##else:
                ##continue

            #k = pot_entry.id
            #found_entry = self.binarySearch(self.sorted_po_cat, pot_entry)
            #is_in = isinstance(found_entry, Message)

            #if (not is_in):
                #print("Find in lower case list: ", k)
                #found_entry = self.binarySearch(self.sorted_lower_po_cat, pot_entry, is_lcase=True)
                #is_in = isinstance(found_entry, Message)
                #if (not is_in):
                    #print("Not Found, NEW: {}".format(k))
                    #continue

            ##print("pot_entry:", pot_entry.id)
            ##print("Found entry:", found_entry.id)
            ##k, c, po_value = self.sorted_po_cat[po_value_index]
            ##po_value = found_entry
            #pot_entry.string = found_entry.string
            #changed = True

            ##print("is po_entry a Message:{}".format(isinstance(po_entry, Message)))
            ##exit(0)
            ##is_fuzzy = ('fuzzy' in po_entry.flags)
            #if (found_entry.fuzzy):
                #pot_entry.flags.add('fuzzy')

            #print("pot_entry.id:{}, pot_entry.string:{}, pot_entry.fuzzy:{}".format(pot_entry.id, pot_entry.string, pot_entry.fuzzy))
            #print("--"*5)

        if (changed):
            new_po_file = "/home/htran/new_vi.po"
            print("Saving content of new pot_cat to:{}".format(new_po_file))
            self.dump_po(new_po_file, self.pot_cat)


x = UpdateVIPO();
x.run()
