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
import langdetect
import json

from sphinx_intl import catalog as c
from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile

class RewordingMSGSTR:
    def __init__(self):
        self.po_path="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
        self.pattern=r":menuselection:`[\w ][^`]*`"
        #self.dic_file="/home/htran/menuselection_dictionary.json"
        self.dic_file="/home/htran/menuselection_new_dictionary_sorted_translated_0001.json"
        self.dic_list={}

        self.file_name_printed = False
        self.new_text = None

    def dump_po(self, filename, catalog):
        print("dump_po - writting to:{}".format(filename))
        print("-" * 80)
        #return
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

    def getReplaceText(self, m):
        replace = m.id
        is_subtitle = (m.string.find(" -- ") >= 0)
        if (is_subtitle):
            replace = " -- {}".format(m.id)
        return replace

    def printMessageEntry(self, m, extra_message=None):
        if (extra_message != None):
            print("{}".format(extra_message))
        print("msgid: [{}]".format(m.id))
        print("msgstr:[{}]".format(m.string))


    def storeWordList(self, data_list):
        for d in data_list:
            is_already_in = (d in self.dic_list)
            if (not is_already_in):
                self.dic_list.update({d:0})
            else:
                v = self.dic_list[d] + 1
                self.dic_list.update({d:v})

    def writeDictionary(self, dict_list=None, file_name=None):
        file_path = (self.dic_file if (file_name == None) else file_name)
        dic = (self.dic_list if (dict_list == None) else dict_list)
        #print("Length of write dictionary:{}".format(len(dic)))
        #print("dictionary:{}".format(dic))
        with open(file_path, 'w', newline='\n') as out_file:
            json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

    def readDictionary(self, file_name=None):
        file_path = (self.dic_file if (file_name == None) else file_name)
        with open(file_path) as in_file:
            self.dic_list = json.load(in_file)
        #print("Length of read dictionary:{}".format(len(self.dic_list)))

    def printFileNameOnce(self, file_name, extra_message=None):
        if (self.file_name_printed):
            return
        if (extra_message == None):
            msg = "{}".format(file_name)
        else:
            msg = "{}; {}".format(extra_message, file_name)

        print(msg)
        print("." * 80)
        self.file_name_printed = True

    def resetFileNamePrinted(self):
        self.file_name_printed = False

    def getNewText(self, old_text, trans_text):
        p=re.findall(r":menuselection:`(.*)`", old_text)
        if (len(p) == 0):
            return None

        #local_dic={}
        #print("p[0]:[{}]".format(p[0]))
        word_list = p[0].split("-->")
        #print("word_list:{}".format(word_list))
        for index, text in enumerate(word_list):
            is_already_done = (len(trans_text.split("()")) > 2)
            #print("trans_text:{}; is_already_done:{};".format(trans_text, is_already_done))
            if (is_already_done):
                return None

            text = text.strip()
            test_bracketed_text = "\({}\)".format(text)
            test_text = ":menuselection:`[\w ]+{}.*".format(test_bracketed_text)
            is_already_done = (re.search(test_text, trans_text) != None)

            #print("test_text:{}; trans_text:{}; is_already_done:{}".format(test_text, trans_text, is_already_done))
            if (is_already_done):
                #print("ALREADY DONE:{}".format(trans_text))
                return None

            is_empty_text = (len(text) == 0)
            if (is_empty_text):
                continue

            bracketed_text = "({})".format(text)
            if (bracketed_text not in self.dic_list):
                print("ADDING TO DICTIONARY:[{}]".format(bracketed_text))
                self.dic_list.update({bracketed_text:""})

            translation = self.dic_list[bracketed_text]
            #print("Looking:[{}]; translation:[{}]".format(bracketed_text, translation))

            is_translation_empty = (len(translation) == 0)
            if (is_translation_empty):
                bracketed_text = "{}".format(text)
                #print("Translation is EMPTY:[{}]".format(bracketed_text))
            else:
                bracketed_text = "{} {}".format(translation, bracketed_text)
                #print("Translation is NOT EMPTY:[{}]".format(bracketed_text))

            word_list[index] = bracketed_text

        #self.storeWordList(word_list)
        #print("END LOOP - word_list:{}".format(word_list))
        new_text = " --> ".join(word_list)

        new_text = ":menuselection:`{}`".format(new_text)
        #print("getNewText() new_text=[{}]".format(new_text))
        #self.storeWordList(word_list)
        return new_text


    def rewordMessage(self, m, p, file_name):
        self.printMessageEntry(m, extra_message="Possible!")
        new_id = str(m.id)
        new_msgstr = str(m.string)
        new_text = None
        print("Processing file:{}".format(file_name))
        for match in p.finditer(m.id):
            old_sub_text = match.group()
            #print("match.start:{}, match.group:{}".format(match.start(), match.group()))
            new_sub_text = self.getNewText(old_sub_text, m.string)
            is_already_done = (new_sub_text == None)
            if (is_already_done):
                print("ALREADY DONE, ignore!")
                self.printMessageEntry(m, extra_message="ALREADY DONE, ignore!")
                self.printFileNameOnce(file_name)
                return None

            is_msgstr_empty = (len(m.string) == 0)
            is_msgstr_same_as_msgid = (m.string == m.id)
            is_using_msgstr = (not (is_msgstr_empty or is_msgstr_same_as_msgid))
            if (is_using_msgstr):
                new_msgstr = new_msgstr.replace(old_sub_text, new_sub_text, 1)
                new_text = new_msgstr
                print("USING MSGSTR")
                #self.printFileNameOnce(file_name, extra_message="POSSIBLE DIRTY")
            else:
                new_id = new_id.replace(old_sub_text, new_sub_text, 1)
                new_text = new_id
                #print("USING MSGID")
                #self.printFileNameOnce(file_name, extra_message="POSSIBLE DIRTY")
        return new_text


    def rewordingMSGSTR(self, doc, file_name):
        is_dirty = False
        self.resetFileNamePrinted()
        possible_p = re.compile(r":menuselection:\`[^\`]*\`");
        possible_msgstr_p = re.compile(r":menuselection:\`([^\`\(\)]*)\`");

        p = re.compile(self.pattern)
        for index, m in enumerate(doc):
            is_first_item = (index == 0)
            if (is_first_item):
                continue

            is_possible = (possible_p.search(m.id) != None)
            if (not is_possible):
                continue


            is_possible = (possible_msgstr_p.search(m.string) != None)
            if (not is_possible):
                continue

            #self.printMessageEntry(m, extra_message="POSSIBLE!")
            new_text = self.rewordMessage(m, possible_msgstr_p, file_name)
            print("new_text:[{}]".format(new_text))

            is_the_same = (m.string == new_text)
            if (is_the_same):
                self.printFileNameOnce(file_name, extra_message="SHOULD BE IGNORED")
                continue

            #is_dirty = (not is_the_same)
            is_already_done = (new_text == None)
            if (not is_already_done):
                self.printMessageEntry(m, extra_message="CHANGED FROM:")
                m.string = new_text
                self.printMessageEntry(m, extra_message="CHANGED TO:")
                is_dirty = True
                print("-" * 20)

        if (is_dirty):
            #self.printFileNameOnce(file_name)
            #file_name="/home/htran/test_vi.po"
            self.dump_po(file_name, doc)

    def run(self):
        #exit(0)
        self.readDictionary()
        #for k,v in self.dic_list.items():
            #print("K=[{}] V=[{}]".format(k, v))
        #exit(0)
        self.po_file_list = self.getPOFileList()
        for po_file in self.po_file_list:
            po_doc = c.load_po(po_file)
            self.rewordingMSGSTR(po_doc, po_file)
        self.writeDictionary()

    def copyTranslationFromVIPOToDictOnFile(self):
        vipo_file="/home/htran/blender_documentations/new_po/vi.po"
        dict_file="/home/htran/menuselection_dictionary_sorted_translated.json"
        new_dict_file="/home/htran/menuselection_new_dictionary_sorted_translated.json"

        vipo_doc = c.load_po(vipo_file)
        local_vipo_dict = {}
        for index, m in enumerate(vipo_doc):
            if (index == 0):
                continue

            k = m.id
            v = m.string
            local_vipo_dict.update({k:v})

        self.readDictionary(file_name = dict_file)
        print("len of vipo_dic:{}".format(len(local_vipo_dict)))
        print("len of json_dic:{}".format(len(self.dic_list)))

        new_dict_list={}
        for k,v in self.dic_list.items():
            new_dict_list.update({k:v})
            #print("json k:[{}] json v:[{}]".format(k, v))
            can_find_definition = (len(v) == 0)
            if (not can_find_definition):
                continue

            #kk = re.search("\((.*)\)", k)
            #key = kk[0]
            trans = None
            key = k.strip("()")
            if (not key in local_vipo_dict):
                print("NOT IN VIPO DIC:[{}]".format(key))
                key_word_list = (key.split(" "))
                print("key_word_list:{}".format(key_word_list))
                trans_word_list = []
                for word in key_word_list:
                    if (not word in local_vipo_dict):
                        trans_word_list.append(word)
                    else:
                        trans = local_vipo_dict[word]
                        trans_word_list.append(trans)
                trans = " ".join(trans_word_list)
                if (trans == key):
                    continue
            else:
                trans = local_vipo_dict[key]

            has_translation = (len(trans) > 0)
            if (has_translation):
                k = "({})".format(key)
                #print("key:[{}]; value:[{}]".format(k, trans))
                new_dict_list.update({k:trans})
            else:
                print("key:[{}]; NO TRANSLATION".format(key))

        self.writeDictionary(dict_list=new_dict_list, file_name=new_dict_file)
        #print(new_dict_list)

x = RewordingMSGSTR()
x.run()
#x.copyTranslationFromVIPOToDictOnFile()
