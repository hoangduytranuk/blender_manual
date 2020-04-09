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

import json
from sphinx_intl import catalog as c
#from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile
from pprint import pprint as pp
from collections import OrderedDict, defaultdict
from argparse import ArgumentParser

DEBUG = True

def _(*args, **kwargs):
    global DEBUG
    if DEBUG:
        print(args, kwargs)
        print('-' * 30)

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
    to_blender_pot_path="/Users/hoangduytran/po/po/vi.po"
    default_out_file = "/Users/hoangduytran/new_vi.po"
    default_dic_path = "/Users/hoangduytran/blender_manual/ref_dict_0001.json"

    def __init__(self):
        self.po_cat = None
        self.pot_cat = None
        self.sorted_po_cat = None
        self.from_file = None
        self.to_file = None
        self.out_file = None
        self.dry_run = False
        self.json_dic = None


    def writeJSONDic(self, dict_list=None, file_name=None):
        try:
            file_path = file_name
            dic = dict_list

            with open(file_path, 'w', newline='\n', encoding='utf8') as out_file:
                json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

        except Exception as e:
            _("Exception writeDictionary Length of read dictionary:{}".format(len(dic)))
            raise e

    def loadJSONDic(self, file_name=None):
        local_dic = None
        try:
            file_path = file_name
            dic = None
            with open(file_path) as in_file:
                dic = json.load(in_file)

        except Exception as e:
            _("Exception readDictionary Length of read dictionary:")
            _(e)
            raise e

        return dic


    def loadFiles(self):
        self.po_cat = c.load_po(self.from_file)

        if self.update_dic:
            self.json_dic = self.loadJSONDic(self.to_file)
        else:
            self.pot_cat = c.load_po(self.to_file)
            self.sorted_po_cat = None

    def setVars(self, from_file, to_file, out_file, dry_run, update_dic):
        self.update_dic = (True if update_dic else False)

        valid = (from_file is not None) and (os.path.isfile(from_file))
        self.from_file = (from_file if valid else UpdateVIPO.from_vipo_path)

        valid = (to_file is not None) and (os.path.isfile(to_file))

        if self.update_dic:
            self.to_file = (to_file if valid else UpdateVIPO.default_dic_path)
        else:
            self.to_file = (to_file if valid else UpdateVIPO.to_blender_pot_path)

        if not self.update_dic:
            valid = (out_file is not None)
            self.out_file = (out_file if valid else UpdateVIPO.default_out_file)

        self.dry_run = (True if dry_run else False)


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
            #k = (m.id, context)
            k = m.id
            v = m
            entry={k:v}
            po_cat_dic.update(entry)

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


    def updatePOtoDIC(self):
        changed = False
        po_cat_dict = self.poCatToDic(self.po_cat)

        ignore_list=[
            "Volume"
        ]

        for k, v in po_cat_dict.items():
            is_ignore = (k in ignore_list) or (len(k) < 2) 
            if is_ignore:
                print(f'in ignore list or len < 2 => IGNORED: {k}, {v}')
                continue

            v_string = v.string # this is the translation

            has_string = (len(v_string) > 0)
            if not has_string:
                print(f'No Translation IGNORED: {k}, {v_string}')
                continue

            is_same = (k.lower() == v_string.lower())
            if is_same:
                print(f'Identical IGNORED: {k}, {v_string}')
                continue

            is_in_old_dict = (k in self.json_dic)
            if not is_in_old_dict:
                entry={k: v_string}
                print(f'UPDATING NEW ENTRY {entry}')                
                self.json_dic.update(entry)
                changed = True
            else:
                old_v = self.json_dic[k]
                is_diff = (old_v != v_string)
                if is_diff:
                    entry={k: v_string}
                    print(f'UPDATING DIFF ENTRY {entry}')                
                    self.json_dic.update(entry)
                    changed = True
                else:
                    print(f'Already in the current dic, so IGNORED: {k}, {v_string}')


        if changed:
            if self.dry_run:
                test_file = "/Users/hoangduytran/test_file.json"
                print(f'DRY_RUN: changed content IS SAVING to:{test_file}')
                self.writeJSONDic(self.json_dic, test_file) 
            else:
                #new_po_file = "/Users/hoangduytran/new_vi.po"
                print(f'Saving content of changed dictionary to:{self.to_file}')
                self.writeJSONDic(self.json_dic, self.to_file) 

    def updatePOtoPO(self):

        po_cat_dict = self.poCatToDic(self.po_cat)
        po_pot_dict = self.poCatToDic(self.pot_cat)
            # print("po_pot_dict")
            # pp(po_pot_dict)

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



        if (changed):
            if self.dry_run:
                print(f'DRY_RUN: changed content IS NOT SAVED to:{self.out_file}')
            else:
                #new_po_file = "/Users/hoangduytran/new_vi.po"
                print(f'Saving content of new pot_cat to:{self.out_file}')
                c.dump_po(self.out_file, self.pot_cat, line_width=99)


    def run(self):

        self.loadFiles()
        if self.update_dic:
            self.updatePOtoDIC()
        else:
            self.updatePOtoPO()


parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-f", "--from_file", dest="from_file", help="PO files from which translations are taken.")
parser.add_argument("-t", "--to_file", dest="to_file", help="PO files to which translations are transfered to.")
parser.add_argument("-o", "--output_file", dest="output_file", help="The file contains the merged output. DO NOT write to to_file parameter.")
parser.add_argument("-r", "--dry_run", dest="dry_run", help="Test run, do not write changes.", action='store_const', const=True)
parser.add_argument("-D", "--dic", dest="update_dic", help="Update dictionary. 'From file' is the PO file where entries are taken from, 'To file' is the target JSON dictionary.", action='store_const', const=True)

args = parser.parse_args()

x = UpdateVIPO();
x.setVars(
    args.from_file,
    args.to_file,
    args.output_file,
    args.dry_run,
    args.update_dic
    )

x.run()
