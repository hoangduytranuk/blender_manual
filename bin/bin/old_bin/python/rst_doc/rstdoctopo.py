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

lock = threading.RLock()

DEBUG=True
dic_file="/home/htran/menuselection_new_dictionary_sorted_translated_0027.json"
dic_new_file="/home/htran/menuselection_new_dictionary_sorted_0001.json"
dic_list={}
dic_list_loaded=False
dic_new_list=[]
dic_new_list_loaded = False
dic_list_updated=False
count=0

#from podocument import Document
class RSTToPo:
    default_man_path="/home/htran/blender_documentations/blender_docs/manual"
    default_po_path="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
    #"/home/htran/menuselection_new_dictionary_sorted_translated_0024.json"

    def __init__(self):
        pass

    def setVars(self, document):

        self.doc_path = None
        self.po_path = None

        self.file_name_printed = False
        self.new_text = None
        self.orig_document = document
        self.document = str(document)

    def writeTextFile(self, file_name, text):
        try:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, "w") as f:
                f.write(text);
                f.close()
        except Exception as e:
            print("Exception writeTextFile:{}".format(file_name))
            raise e


    def getDocPath(self, text):
        doc_path = re.compile(r"(<document source=\"{}/)(.*)(\.rst\">)".format(RSTToPo.default_man_path))

        m  = doc_path.match(text)
        is_found = (m != None)
        if (is_found):
            g = m.groups(0)

            return g[1]
        else:
            return None


    def printMessageEntry(self, m, extra_message=None):
        if (extra_message != None):
            print("{}".format(extra_message))
        print("msgid: [{}]".format(m.id))
        print("msgstr:[{}]".format(m.string))

    def ProcessRSTDoc(self):
        global DEBUG

        kw = ['title', 'field_name', 'term', 'strong', 'rubric']
        doc_path = self.getDocPath(self.document)

        rst_output_path = "/home/htran/blender_documentations/blender_docs/build/rstdoc/{}.rst".format(doc_path)

        if (DEBUG):
            print("Writting RST formatted document [{}]".format(rst_output_path))
            DEBUG=False

        self.writeTextFile(rst_output_path, self.document)
        return

rstpoto_instance = RSTToPo()
