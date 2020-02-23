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
import threading


from sphinx_intl import catalog as c
from PO.common import Common as cm
from babel.messages import pofile
from random import randint
from time import sleep

#from podocument import Document
class RSTToPo:
    default_man_path="/home/htran/blender_documentations/blender_docs/manual"
    default_po_path="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
    #"/home/htran/menuselection_new_dictionary_sorted_translated_0024.json"

    def __init__(self):
        self.DEBUG=True
        self.dic_file="/home/htran/menuselection_new_dictionary_sorted_translated_0027.json"
        self.dic_new_file="/home/htran/menuselection_new_dictionary_sorted_0001.json"
        self.dic_list={}
        self.dic_list_loaded=False
        self.dic_new_list=[]
        self.dic_new_list_loaded = False
        self.dic_list_updated=False
        self.count=0

        self.the_file_list=[]

        self.doc_path = None
        self.po_path = None

        self.file_name_printed = False
        self.new_text = None
        self.orig_document = None
        self.document = None
        self.pattern_list = []
        self.kw = ['title', 'field_name', 'term', 'strong', 'rubric']

    def setupPattern(self):

        for k in self.kw:
            pattern_0001 = r"<{}[^>]*>([^\.\!<]+)</{}>".format(k, k)
            p = re.compile(pattern_0001)
            self.pattern_list.append(p)

            pattern_0002 = r"<{}[^>]*>([^\.\!<]+)*<".format(k)
            p = re.compile(pattern_0002)
            self.pattern_list.append(p)

    #def dump_po(self, filename, catalog):
        #print("dump_po - writting to:{}".format(filename))
        #print("-" * 80)
        #if (self.DEBUG): return
        #dirname = os.path.dirname(filename)
        #if not os.path.exists(dirname):
            #os.makedirs(dirname)

        ## Because babel automatically encode strings, file should be open as binary mode.
        #with io.open(filename, 'wb') as f:
            #pofile.write_po(f, catalog, width=0)

    def getFileList(self, root_dir, extension):
        file_list=[]
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                the_file = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(the_file)
                #basename = relpath(base, self.po_path)
                #print("ext:{}".format(ext))
                #exit(0)
                is_the_file = (ext.lower() == extension.lower())
                if (is_the_file):
                    file_list.append(the_file)

        return sorted(file_list)

    def setVars(self, document):
        pass

    def writeDictionary(self, d_list=None, file_name=None):
        file_path = (self.dic_file if (file_name == None) else file_name)
        dic = (self.dic_list if (d_list == None) else d_list)
        try:
            #print("Length of write dictionary:{}".format(len(dic)))
            #print("dictionary:{}".format(dic))
            print("writeDictionary:{}, size:{}".format(file_path, len(dic)))
            #if (DEBUG): return
            with open(file_path, 'w', newline='\n', encoding='utf8') as out_file:
                json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
                out_file.close()
        except Exception as e:
            print("Exception writeDictionary".format(file_path))
            raise e


    def readTextFile(self, file_name):
        read_text = None
        try:
            print("readTextFile:{}".format(file_name))
            with open(file_name) as f:
                #print("start readTextFile:{}".format(file_name))
                read_text = f.read();
                #print("readTextFile closing:{}".format(file_name))
                return read_text
        except Exception as e:
            print("Exception readTextFile:{}".format(file_name))
            raise e

    def writeTextFile(self, file_name, text):
        try:
            print("writeTextFile:{}".format(file_name))
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, "w") as f:
                f.write(text);
                f.close()
        except Exception as e:
            print("Exception writeTextFile:{}".format(file_name))
            raise e

    def readDictionary(self, d_list=None, file_name=None, flag_to_set=None):

        file_path = (self.dic_file if (file_name == None) else file_name)
        dic = (self.dic_list if (d_list == None) else d_list)

        try:
            print("readDictionary:{}, current size:{}".format(file_path, len(dic)))
            with open(file_path) as in_file:
                dic = json.load(in_file)
                print("Loaded:{}".format(len(dic)))
                flag_to_set = (len(dic) > 0)
                in_file.close()
            return dic
        except Exception as e:
            print("Exception readDictionary:{}".format(file_path))
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


    def getByKeyword(self, text):
        #<title>Import</title>
        result_list=[]
        for p in self.pattern_list:
            m  = p.findall(text)

            is_found_m = (m != None)
            if (is_found_m):
                result_list= result_list + m

        unique_set = set(result_list)
        result_list = list(unique_set)
        result_list = sorted(result_list)
        return result_list


    def printMessageEntry(self, m, extra_message=None):
        if (extra_message != None):
            print("{}".format(extra_message))
        print("msgid: [{}]".format(m.id))
        print("msgstr:[{}]".format(m.string))


    #def duplicateMSGIDToUntranslatedMSGSTR(self, po_path, po_cat, title_list):
        #is_empty = (title_list == None or len(title_list) < 1)
        #if (is_empty):
            #return False

        #is_dirty = False
        #self.resetFileNamePrinted()
        #for index, m in enumerate(po_cat):

            #id_text = m.id
            #msgstr = m.string
            ##print("msgid: {}".format(id_text))

            #is_numeric = cm.isNumber(id_text)

            #is_title = (id_text in title_list)
            #is_ignore = cm.isIgnored(id_text)

            #is_bypass = (not is_title) or is_ignore or is_numeric
            #if (is_bypass):
                #continue

            #en = m.id
            #dic_en = "({})".format(en)


            #if (dic_en not in self.dic_list):
                #word_list = msgstr.split("--")
                #has_trans = (len(word_list) > 1) and (len(word_list[0].strip()) > 0)
                #if (has_trans):
                    #vn = word_list[0].strip()
                    #en = id_text
                    #replace_text = "{} -- {}".format(vn, en)
                #else:
                    #replace_text = "-- {}".format(id_text)
            #else:
                #dic_vn = self.dic_list[dic_en]
                #replace_text = "{} -- {}".format(dic_vn, en)

            ##print("duplicateMSGIDToUntranslatedMSGSTR")
            ###print(self.dic_list)

            #is_already_done = (replace_text == msgstr)
            #if (is_already_done):
                #continue

            #self.printMessageEntry(m, extra_message="FROM:")
            #m.string = replace_text
            #is_dirty = True
            #self.printMessageEntry(m, extra_message="CHANGED TO:")

        #if (is_dirty):
            ##print("GET OUT:{}".format(po_path)); return
            #self.dump_po(po_path, po_cat)

    #def translatingSubtitlesUsingDictionary(self, po_doc, po_path, title_list):
        #is_empty = (title_list == None or len(title_list) < 1)
        #if (is_empty):
            #return False

        #is_dirty = False
        #for index, m in enumerate(po_doc):

            #id_text = m.id
            ##print("msgid: {}".format(id_text))

            #is_numeric = cm.isNumber(id_text)
            #is_title = (id_text in title_list)
            #is_ignore = cm.isIgnored(id_text)

            #is_bypass = (not is_title or is_ignore or is_numeric)
            #if (is_bypass):
                #continue

            #msgstr = str(m.string)
            #word_list = msgstr.split("-- ")

            #english_text = None
            #vietnamese_text = None
            #existing_vietnamese_text = None

            #is_not_done = (len(word_list) == 1)
            #is_not_translated = (len(word_list) > 1) and (len(word_list[0].strip()) == 0)
            #is_translated = (len(word_list) > 1) and (len(word_list[0].strip()) > 0)

            #is_valid = (is_not_done or is_not_translated or is_translated)
            #if (not is_valid):
                #print("something is NOT RIGHT here:{}".word_list)
                #return

            #english_text = id_text
            #if (not english_text in self.dic_list):
                #if (is_not_done):
                    #replace_text = "-- {}".format(id_text)
                #else:
                    #if (is_translated):
                        #vietnamese_text = word_list[0].strip()
                        #english_text = "({})".format(word_list[1].strip())
                        #if (not english_text in self.dic_list):
                            #self.dic_list.update({english_text:vietnamese_text})
                            #self.dic_list_updated = True
                            #print("\"{}\": \"{}\",".format(english_text, vietnamese_text))
                    #continue
            #else:
                #english_text = "({})".format(english_text)
                #vietnamese_text = self.dic_list[english_text]

            #has_vietnamese_text = (vietnamese_text != None) and (len(vietnamese_text) > 0)
            #if (has_vietnamese_text):
                #replace_text = "{} -- {}".format(vietnamese_text, english_text)
            #else:
                #if (is_translated):
                    #existing_vietnamese_text = word_list[0]
                    #replace_text = "{} -- {}".format(existing_vietnamese_text, english_text)

            #is_already_done = (replace_text == msgstr)
            #if (is_already_done):
                #self.printMessageEntry(m, extra_message="Already DONE, ignored!")
                #return

            #self.printMessageEntry(m, extra_message="FROM:")
            #m.string = replace_text
            #self.printMessageEntry(m, extra_message="CHANGED TO:")
            #is_dirty = True

        #if (is_dirty):
            ##print("GET OUT:{}".format(po_path)); return
            #self.dump_po(po_path, po_cat)


    def getUntranslatedSubtitleToDictionary(self, po_doc, po_path, title_list):
        #print("Running (getUntranslatedSubtitleToDictionary)!")
        #return
        is_empty = (title_list == None or len(title_list) < 1)
        if (is_empty):
            return False

        for index, m in enumerate(po_doc):

            id_text = m.id
            #print("msgid: {}".format(id_text))

            is_numeric = cm.isNumber(id_text)
            is_title = (id_text in title_list)
            is_ignore = cm.isIgnored(id_text)

            is_bypass = (not is_title or is_ignore or is_numeric)
            if (is_bypass):
                continue

            english_text = id_text
            vietnamese_text = ""

            english_text = "({})".format(english_text)
            #print("{}:self dictionary".format(self.dic_list))
            #if (not english_text in self.dic_list):
                #self.printFileNameOnce(po_path)
                #print("\"{}\": \"\",".format(english_text))
                ##dic_new_list.update({english_text:vietnamese_text})
                ##self.dic_new_list.append(id_text)
                ##self.dic_list_updated = True


    def ProcessRSTDoc(self):
        #print(dic_file)

        doc_path = self.getDocPath(self.document)

        l = []
        result = self.getByKeyword(self.document)
        if (result != None):
            l.extend(result)
            l = sorted(l)

        print("{}".format(doc_path))
        print("{}".format(l))
        print("-" * 50)
        return

        po_file = "{}.po".format(doc_path)
        po_path = os.path.join(RSTToPo.default_po_path, po_file)
        #print("Processing: {}".format(po_path))
        if (os.path.exists(po_path)):
            ##print("File is there: {}".format(po_path))

            po_doc = c.load_po(po_path)
            ##self.translatingSubtitlesUsingDictionary(po_doc, po_path, l)
            ##self.duplicateMSGIDToUntranslatedMSGSTR(po_path, po_doc, l)
            self.getUntranslatedSubtitleToDictionary(po_doc, po_path, l)
            ##po_doc = Document(po_path)
            ##po_doc.loadPOText()
            ##po_doc.duplicateMSGIDToUntranslatedMSGSTR(l)
            #self.resetFileNamePrinted()

        else:
            print("File is NOT there: {}".format(po_path))

        ##print("dic_new_list:")
        #print("=" * 80)
        #dic_new_list = sorted(dic_new_list)
        #for x in dic_new_list:
            #line = "'({})\': '',".format(x)
            #cmd = "echo \"{}\" >> {}".format(line, dic_new_file)
            #os.system(cmd)
        #print("=" * 80)
        ##if (dic_list_updated):
            ####self.writeDictionary()
            ##self.writeDictionary(d_list=dic_new_list, file_name=dic_new_file)
            ##self.dic_list_updated = False

    def run(self):
        if (not self.dic_list_loaded):
            self.dic_list = self.readDictionary(flag_to_set=self.dic_list_loaded)
            self.dic_list_loaded = True

        self.setupPattern()
        #self.readDictionary()
        #for k,v in self.dic_list.items():
            #print("K=[{}] V=[{}]".format(k, v))
        #exit(0)
        root_dir="/home/htran/blender_documentations/blender_docs/build/rstdoc"
        self.the_file_list = self.getFileList(root_dir, ".rst")
        for rst_file in self.the_file_list:
            self.document = self.readTextFile(rst_file)
            print("{}".format(self.document))
            print("{}".format(rst_file))
            print("=" * 80)
            self.ProcessRSTDoc()

        if (self.dic_list_updated):
            print("{}".format(self.dic_new_list))
        #self.writeDictionary()

rstpoto_instance = RSTToPo()
rstpoto_instance.run()

