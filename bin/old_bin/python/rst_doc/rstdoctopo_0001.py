#!/usr/bin/env python3

"""
Loading the RST file then use the RST structure to identify the subtitles
This file is run with the code in

    /home/htran/.local/lib/python3.6/site-packages/docutils/core.py

and all code in

    /home/htran/bin/python/*

must have PYTHONPATH set in the .bashrc

PYTHONPATH=/home/htran/bin/python/rst_doc:/home/htran/bin/python/base:/home/htran/bin/python/algorithm:/home/htran/bin/python/event:/home/htran/bin/python//PO

and run with command:

cd $BLENDER_MAN_EN; make clean; make gettext

"""

import sys
sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
sys.path.append("/home/htran/bin/python")

import re
import os
import io
import json

from sphinx_intl import catalog as c
from PO.common import Common as cm
from babel.messages import pofile

#from podocument import Document
class RSTToPo:
    default_man_path="/home/htran/blender_documentations/blender_docs/manual"
    default_po_path="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
    instance = None

    @classmethod
    def getInstance(self):
        if (instance == None):
            instance = RSTToPo()

        return instance

    def __init__(self):
        self.document = None
        self.doc_path = None
        self.po_path = None

        self.dic_file="/home/htran/menuselection_new_dictionary_sorted_translated_0001.json"
        self.dic_list={}
        self.dic_list_updated=False

        self.file_name_printed = False
        self.new_text = None

    def setVars(self, document):
        self.document = str(document)


    def writeDictionary(self, dict_list=None, file_name=None):
        try:
            file_path = (self.dic_file if (file_name == None) else file_name)
            dic = (self.dic_list if (dict_list == None) else dict_list)
            #print("Length of write dictionary:{}".format(len(dic)))
            #print("dictionary:{}".format(dic))
            print("writeDictionary:{}".format(file_path))
            with open(file_path, 'w', newline='\n', encoding='utf8') as out_file:
                json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
                out_file.close()
        except Exception as e:
            print("Exception writeDictionary Length of read dictionary:{}".format(len(self.dic_list)))
            raise e


    def readDictionary(self, file_name=None):
        try:
            file_path = (self.dic_file if (file_name == None) else file_name)
            print("readDictionary:{}".format(file_path))
            with open(file_path) as in_file:
                self.dic_list = json.load(in_file)
                in_file.close()
        except Exception as e:
            print("Exception readDictionary Length of read dictionary:{}".format(len(self.dic_list)))
            raise e

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


    def getDocPath(self, text):
        doc_path = re.compile(r"(<document source=\"{}/)(.*)(\.rst\">)".format(RSTToPo.default_man_path))

        m  = doc_path.match(text)
        is_found = (m != None)
        if (is_found):
            g = m.groups(0)
            return g[1]
        else:
            return None


    def getByKeyword(self, keyword, text):
        #<title>Import</title>
        pattern = r"<{}[^>]*>([^\.\!<]+)</{}>".format(keyword, keyword)
        titles = re.compile(pattern)
        m  = titles.findall(text)
        is_found = (m != None)
        if (is_found):
            return m
        else:
            return None


    def printMessageEntry(self, m, extra_message=None):
        if (extra_message != None):
            print("{}".format(extra_message))
        print("msgid: [{}]".format(m.id))
        print("msgstr:[{}]".format(m.string))


    def duplicateMSGIDToUntranslatedMSGSTR(self, po_path, po_cat, title_list):
        is_empty = (title_list == None or len(title_list) < 1)
        if (is_empty):
            return False

        is_dirty = False
        is_displayed_filename = False
        for index, m in enumerate(po_cat):

            id_text = m.id
            #print("msgid: {}".format(id_text))

            is_numeric = cm.isNumber(id_text)

            is_title = (id_text in title_list)
            is_ignore = cm.isIgnored(id_text)


            is_bypass = (not is_title or is_ignore or is_numeric)
            if (is_bypass):
                continue

            msgstr = str(m.string)

            word_list = msgstr.split("--")

            is_translated = len(word_list) > 1
            english_text = None
            vietnamese_text = None

            if (not is_translated):
                english_text = id_text
                vietnamese_text = None
                if (not english_text in self.dic_list):
                    inconsistent = (re.search(" - ", msgstr) != None)
                    if (inconsistent):
                        replace_text = re.sub(" - ", " -- ", msgstr)
                    else:
                        if (len(msgstr) > 0):
                            replace_text = "{} -- {}".format(msgstr, id_text)
                        else:
                            replace_text = "-- {}".format(id_text)
                else:
                    english_text = "({})".format(english_text)
                    vietnamese_text = self.dic_list[english_text]
                    replace_text = "{} -- {}".format(vietnamese_text, english_text)
            else:
                english_text = "({})".format(id_text)
                if (not english_text in self.dic_list):
                    self.printMessageEntry(m, extra_message="NOT IN DICT, ignored!")
                    continue
                else:
                    english_text = "{}".format(id_text)
                    vietnamese_text = self.dic_list[english_text]
                    replace_text = "{} -- {}".format(vietnamese_text, english_text)
                    print("replace_text:[{}]".format(replace_text))

            is_already_done = (replace_text == m.string)
            if (is_already_done):
                print("DONE!")
                continue


            self.printMessageEntry(m, extra_message="FROM:")
            m.string = replace_text
            self.printMessageEntry(m, extra_message="CHANGED TO:")
            is_dirty = True

        if (is_dirty):
            #print("GET OUT:{}".format(po_path)); return
            self.dump_po(po_path, po_cat)

    def dump_po(self, filename, catalog):
        print("dump_po - writting to:{}".format(filename))
        print("-" * 80)
        return
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        with io.open(filename, 'wb') as f:
            pofile.write_po(f, catalog, width=0)

    def translatingSubtitlesUsingDictionary(self, po_doc, po_path, title_list):
        is_empty = (title_list == None or len(title_list) < 1)
        if (is_empty):
            return False

        is_dirty = False
        for index, m in enumerate(po_doc):

            id_text = m.id
            #print("msgid: {}".format(id_text))

            is_numeric = cm.isNumber(id_text)
            is_title = (id_text in title_list)
            is_ignore = cm.isIgnored(id_text)

            is_bypass = (not is_title or is_ignore or is_numeric)
            if (is_bypass):
                continue

            msgstr = str(m.string)
            word_list = msgstr.split("-- ")

            english_text = None
            vietnamese_text = None
            existing_vietnamese_text = None

            is_not_done = (len(word_list) == 1)
            is_not_translated = (len(word_list) > 1) and (len(word_list[0].strip()) == 0)
            is_translated = (len(word_list) > 1) and (len(word_list[0].strip()) > 0)

            is_valid = (is_not_done or is_not_translated or is_translated)
            if (not is_valid):
                print("something is NOT RIGHT here:{}".word_list)
                return


            english_text = id_text
            if (not english_text in self.dic_list):
                if (is_not_done):
                    replace_text = "-- {}".format(id_text)
                else:
                    if (is_translated):
                        vietnamese_text = word_list[0].strip()
                        english_text = "({})".format(word_list[1].strip())
                        if (not english_text in self.dic_list):
                            self.dic_list.update({english_text:vietnamese_text})
                            self.dic_list_updated = True
                            print("\"{}\": \"{}\",".format(english_text, vietnamese_text))
                    continue
            else:
                english_text = "({})".format(english_text)
                vietnamese_text = self.dic_list[english_text]

            has_vietnamese_text = (vietnamese_text != None) and (len(vietnamese_text) > 0)
            if (has_vietnamese_text):
                replace_text = "{} -- {}".format(vietnamese_text, english_text)
            else:
                if (is_translated):
                    existing_vietnamese_text = word_list[0]
                    replace_text = "{} -- {}".format(existing_vietnamese_text, english_text)

            is_already_done = (replace_text == msgstr)
            if (is_already_done):
                self.printMessageEntry(m, extra_message="Already DONE, ignored!")
                return

            self.printMessageEntry(m, extra_message="FROM:")
            m.string = replace_text
            self.printMessageEntry(m, extra_message="CHANGED TO:")
            is_dirty = True

        if (is_dirty):
            #print("GET OUT:{}".format(po_path)); return
            self.dump_po(po_path, po_cat)



    def ProcessRSTDoc(self):
        #self.readDictionary()
        #print(self.dic_list)
        ##exit(0)

        kw = ['title', 'field_name', 'term', 'strong', 'rubric']
        doc_path = self.getDocPath(self.document)

        #print(self.text)
        #p = re.compile(self.pattern)
        #t = re.sub("\n", " ", self.text)
        #r'<title[^>]*>([^<]+)</title>'
        #print("{}".format(m[0]))
        l = []
        for k in kw:
            result = self.getByKeyword(k, self.document)
            if (result != None):
                l.extend(result)

        #s = set(l)
        #s1 = sorted(s)
        #l = list(s1)
        #print("doc_path:{}, keywords: {}".format(doc_path, l))

        po_file = "{}.po".format(doc_path)
        po_path = os.path.join(RSTToPo.default_po_path, po_file)
        if (os.path.exists(po_path)):
            #print("File is there: {}".format(po_path))

            po_doc = c.load_po(po_path)
            self.translatingSubtitlesUsingDictionary(po_doc, po_path, l)
            #self.duplicateMSGIDToUntranslatedMSGSTR(po_path, po_doc, l)

            #po_doc = Document(po_path)
            #po_doc.loadPOText()
            #po_doc.duplicateMSGIDToUntranslatedMSGSTR(l)

        else:
            print("File is NOT there: {}".format(po_path))

        #if (self.dic_list_updated):
            #self.writeDictionary()
            #self.dic_list_updated = False

