#!/usr/bin/python3
import sys
sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
sys.path.append("/home/htran/bin/python")

from argparse import ArgumentParser
from bs4 import BeautifulSoup, BeautifulStoneSoup
#from difflib import SequenceMatcher as SM
#from fuzzywuzzy import fuzz as FZ
#import numpy as np
from Levenshtein import distance as DS

import html
#from html.parser import HTMLParser
#import requests
#import webbrowser
import os
import json
import re
import binascii
from codecs import encode

from docutils.utils.smartquotes import smartchars
from PO.common import Common as cm
from base.basefileio import BaseFileIO as bio
from sphinx_intl import catalog as c
from pprint import pprint as pp
from html.parser import HTMLParser
from queue import Queue as Q

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)


class ParseRST():

   #Initializing lists
    def __init__(self):
        self.input_file = None
        self.term_list = []
        self.global_term_list=[]
        self.global_temp_dic={}
        self.soup = None
        self.source_path = None
        self.srt_data_list = []
        self.po_path = None
        self.po_doc = None

        self.dic_file="/home/htran/menuselection_new_dictionary_sorted_translated_00017_test.json"
        self.older_dic_file="/home/htran/menuselection_new_dictionary_sorted_translated_00016_test.json"
        self.doc_root_dir="/home/htran/blender_documentations/blender_docs/manual/"
        self.doc_po_dir="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"

        self.dic_list={}
        self.dic_list_loaded=False
        self.dic_new_list=[]
        self.dic_new_list_loaded = False
        self.dic_list_updated=False

        self.older_dic_list={}

        self.lsStartTags = list()
        self.lsEndTags = list()
        self.lsStartEndTags = list()
        self.lsComments = list()

        self.translated_list=[]

        self.transtable = {
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",

       }


    def setVars(self, input_file : str):
        self.input_file = input_file

   #HTML Parser Methods
    def handle_starttag(self, startTag, attrs):
        self.lsStartTags.append(startTag)

    def handle_endtag(self, endTag):
        self.lsEndTags.append(endTag)

    def handle_startendtag(self,startendTag, attrs):
        self.lsStartEndTags.append(startendTag)

    def handle_comment(self,data):
        self.lsComments.append(data)

    def writeFile(self, data):
        with open(self.input_file, 'w') as f:
            f.write(data)

    def parse_title(self, elem):
        if (not elem.name == "title"):
            return

        for lit in elem.find_all('literal'):
            if (len(lit.text) > 0):
                lit.replaceWith("``{}``".format(lit.text))

        self.term_list.append(elem.text.strip())


    def parse_term(self, elem):
        if (not elem.name == "term"):
            return

        #dic=[
            #"name",
            #"frame",
            #"frames",
            #"path",
            #"engine",
            #"format",
            #"threads",
            #"bool",
            #"file(s)",
            #"sy",
            #"fps-base",
            #"expression",
            #"sx",
            #"fps",
            #"w",
            #"h",
            #"options",
            #"filename",
            #"value",
            #"verbose",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",
            ##"",

             #]

        #prob_file="/home/htran/blender_documentations/blender_docs/build/rstdoc/advanced/command_line/arguments.html"
        #is_special_transform = (self.input_file == prob_file)

        #print("parse_term - elem:[{}]".format(elem))
        #for kbd in elem.find_all('literal', {'classes': 'kbd'}):
            #kbd.replaceWith(":kbd:`{}`".format(kbd.text))
            #self.term_list.append(kbd.text)

        #print("PARSING REF:", elem)
        for ref in elem.find_all('reference'):
            ref_uri_tag="refuri"
            has_refuri = ref.has_attr(ref_uri_tag)
            ref_uri_text = None
            if (has_refuri):
                ref_uri_text = ref.get(ref_uri_tag)
                ref_uri_text = ref_uri_text.replace("#dview", "3dview")

            for i_line in ref.find_all('inline', {'classes':'std std-ref'}):
                has_ref_uri_text = (ref_uri_text != None)
                i_line.replaceWith(":ref:")
                #if (has_ref_uri_text):
                    ##ref_uri_text = ref_uri_text.replace("", "genindex")
                    #i_line.replaceWith(":ref:`{} <{}>`".format(i_line.text, ref_uri_text))
                #else:
                    #i_line.replaceWith(":ref:`{}`".format(i_line.text))

            for i_line in ref.find_all('inline', {'classes':'doc'}):
                has_ref_uri_text = (ref_uri_text != None)
                if (has_ref_uri_text):
                    #ref_uri_text = ref_uri_text.replace("", "/glossary/index")
                    i_line.replaceWith(":doc:`{} <{}>`".format(i_line.text, ref_uri_text))
                else:
                    i_line.replaceWith(":doc:`{}`".format(i_line.text))


        for emp in elem.find_all('emphasis'):
            emp.replaceWith("*{}*".format(emp.text))

        for abr in elem.find_all('abbreviation'):
            expl_attr='explanation'
            expl_text=None
            if (abr.has_attr(expl_attr)):
                expl_text = abr.get(expl_attr)

            has_expl_text = (expl_text != None)
            if (has_expl_text):
                abr.replaceWith(":abbr:`{} ({})`".format(abr.text, expl_text))
            else:
                abr.replaceWith(":abbr:`{}".format(abr.text))

        kbd = elem.find_all('literal', {'classes' : 'kbd'})
        for k in kbd:
            k.replaceWith(":kbd:`{}`".format(k.text))

        is_literal = False
        for lit in elem.find_all('literal'):

            if (is_special_transform):
                for tag in dic:
                    for tt in elem.find_all(tag):
                        #print("found tt:[{}]".format(tag))
                        tt.replaceWith("<{}>".format(tag))

            l_class = lit.get('classes')
            is_kbd = (l_class == 'kbd')
            #kbd has already been handled
            if (is_kbd): continue

            #print("parse_term - lit:[{}]".format(lit))
            lit.replaceWith("``{}``".format(lit.text))


                #found_elem = elem.find(classes="kbd")
                #is_classes = (found_elem != None)
                #if (is_classes):
                    #found_elem.replaceWith(":kbd:`{}`".format(lit.text))
                #elif (lit.text.startswith("<") and lit.text.endswith(">")):
                    #lit.replaceWith("``{}``".format(lit.text))
                #elif (len(lit.text) > 0):
                    #lit.replaceWith("``{}``".format(lit.text))
                #is_literal = True

                #self.term_list.append(lit.text)
                #print("{}; classes=kbd:{}".format(lit, found_elem))

        for ref in elem.find_all('reference'):
            ref_uri='refuri'
            ref_name = 'name'

            refuri = None
            name = None

            if (ref.has_attr(ref_uri)):
                refuri = "{}".format(ref[ref_uri])

            if (ref.has_attr(ref_name)):
                name = "{}".format(ref['name'])

            has_both = (refuri != None) and (name != None)
            if (has_both):
                new_text = "`{} <{}>`__".format(name, refuri)
                ref.replaceWith(new_text)


        text_data = elem.text
        if (is_literal):
            found_entries = [s for s in self.srt_data_list if s.startswith(text_data)]
            #print("looking for:{}".format(text_data))
            #print("found_entries:{}".format(found_entries))
            is_found = (found_entries != None) and (len(found_entries) > 0)
            if (is_found):
                text_data = found_entries[0]
                #print("text_data:{}".format(text_data))

        self.term_list.append(text_data.strip())
        #print("parse_term parsed elem:{}".format(text_data))


    def parse_field_name_for_field_body(self, elem):
        if (not elem.name == "field_name"): return

    def parse_paragraph_for_field_body(self, elem):
        if (not elem.name == "paragraph"): return

    def elem_parse_image(self, p):
        img = p.find_all('image')
        for img_elem in img:
            alt_tag = 'alt'
            has_image_alt = (img_elem.has_attr(alt_tag))
            image_alt_text = None
            if (has_image_alt):
                image_alt_text = img_elem.get(alt_tag)
            if (has_image_alt):
                img_elem.replaceWith("|{}|".format(image_alt_text))

    def elem_parse_kbd(self, p):
        kbd = p.find_all('literal', {'classes' : 'kbd'})
        for k in kbd:
            k.replaceWith(":kbd:`{}`".format(k.text))

    def elem_parse_menu(self, p):
        men = p.find_all('inline', {'classes' : 'menuselection'})
        for m in men:
            rawtext = "{}".format(m['rawtext'])
            rawtext = html.unescape(rawtext)
            m.replaceWith(rawtext)
            #print("rawtext:{}".format(rawtext))

    def elem_parse_literal(self, p):
        lit = p.find_all('literal')
        for l in lit:
            is_xref_py_mod = l.has_attr("classes") and (l['classes'] == "xref py py-mod")
            is_xref_py_class = l.has_attr("classes") and (l['classes'] == "xref py py-class")
            if (is_xref_py_mod):
                l.replaceWith(":mod:`{}`".format(l.text))
            elif (is_xref_py_class):
                l.replaceWith(":class:`{}`".format(l.text))
            else:
                ss = str(l.text)
                #print("SUB:{}".format(ss))
                #print("type(l):{}".format(type(l)))
                l_class = l.get('classes')
                is_kbd = (l_class == 'kbd')
                #pp(att_list)
                #print("attrib list(l):{}".format(get_attribute_list(l)))
                #print("dir(l):{}".format(dir(l)))

                #kbd has already been handled
                if (not is_kbd):
                    l.replaceWith("``{}``".format(l.text))

    def elem_parse_refs(self, p):
        #debug_cond = "The new bone is parented and connected to the bone"
        #is_debug = (debug_cond in str(p))
        #if (is_debug):
            #print("DEBUG:", p)

        refs = p.find_all('reference')
        for ref in refs:
            ref_uri ='refuri'
            ref_id = 'refid'
            is_internal = ref.has_attr("internal") and (ref['internal'] == "True")
            is_internal_with_refid = (is_internal) and ref.has_attr(ref_id)
            is_not_interal = ref.has_attr("name") and (not cm.isEmpty(ref[ref_uri]))
            if (is_internal):
                has_ref_uri = ref.has_attr(ref_uri) and ref[ref_uri].startswith("#")
                if (has_ref_uri):
                    refuri = ref[ref_uri]
                    refuri = refuri.replace("#", "")
                    ref_text = ref.text
                    has_text = (not cm.isEmpty(ref_text))
                    ref.replaceWith(":ref:")
                    #if (has_text):
                        #ref.replaceWith(":ref:`{} <{}>`".format(ref.text, refuri))
                    #else:
                        #ref.replaceWith(":ref:`{}`".format(refuri))
                elif (is_internal_with_refid):
                    ref_id = ref[ref_id]
                    ref.replaceWith(":ref:`{}`".format(ref_id))
                else:
                    docs = ref.find_all('inline', {'classes' : 'doc'})
                    for doc in docs:
                        doc.replaceWith(":doc:`{}".format(ref.text)) # has to wait for fuzzy search

            elif (is_not_interal):
                refuri = ref[ref_uri]
                ref.replaceWith("`{} <{}>`__ ".format(ref.text, refuri))
                #ref.replaceWith(":ref:`{} {}`".format(ref.text, refuri))
            #else:
                #if (is_debug):
                    #print("HERE:", ref)


    def elem_parse_emphasis(self, p):
        emphas = p.find_all('emphasis')
        for em in emphas:
            em.replaceWith("*{}*".format(em.text))

    def elem_parse_strong(self, p):
        strongs = p.find_all('strong')
        for s in strongs:
            s.replaceWith("**{}**".format(s.text))

    def parse_paragraph_base(self, p):
        self.elem_parse_image(p)
        self.elem_parse_kbd(p)
        self.elem_parse_menu(p)
        self.elem_parse_literal(p)
        self.elem_parse_refs(p)
        self.elem_parse_emphasis(p)
        self.elem_parse_strong(p)
        self.term_list.append(p.text)

    def parse_note(self, elem):
        if (not elem.name == "note"): return

        para = elem.find_all('paragraph')
        for index, p in enumerate(para):
            is_first_para = (index == 0)
            if (is_first_para):
                print("routed NOTE:", p)
                self.only_take_heading_item(p)

    def only_take_heading_item(self, p):
        is_ending_with_symbols=(cm.ENDING_WITH_PUNCTUATIONS.search(p.text) != None)
        if (not is_ending_with_symbols):
            #print("p:[{}]; is_ending_with_symbols:{}".format(p.text, is_ending_with_symbols))
            self.parse_paragraph_base(p)
            self.term_list.append(p.text)

    def parse_bullet_list(self, elem):
        if (not elem.name == "bullet_list"): return

        #print("parse_bullet_list:", elem)

        list_items = elem.find_all('list_item')
        for index, lst in enumerate(list_items):
            para = lst.find_all('paragraph')
            for p in para:
                #print("found PARA:[{}]".format(p))
                is_note_child = (p.parent.name == 'note')
                if (is_note_child):
                    is_first_para = (index == 0)
                    if (is_first_para):
                        print("routed NOTE:", p)
                        self.only_take_heading_item(p)
                else:
                    #print("routed HERE:", p)
                    #self.only_take_heading_item(p)
                    self.parse_paragraph_base(p)


    def parse_field_list(self, elem):
        if (not elem.name == "field_list"): return

        for f in elem.find_all('field'):
            for f_name in f.find_all('field_name'):
                self.term_list.append(f_name.text)

            for f_body in f.find_all('field_body'):
                para = f_body.find_all('paragraph')
                for p in para:
                    self.parse_paragraph_base(p)
                    p_text = html.unescape(p.text)
                    self.term_list.append(p_text)
                    #print("para.text:[{}]".format(p.text))

    def parse_literal(self, elem):
        if (not elem.name == "paragraph"): return
        for kbd in elem.find_all('literal', {'classes': 'kbd'}):
            kbd.replaceWith(":kbd:`{}`".format(kbd.text))

    def parse_rubric(self, elem):
        if (not elem.name == "rubric"): return
        self.term_list.append(elem.text)

    def parse_strong(self, elem):
        if (not elem.name == "strong"): return
        parent = elem.parent
        parent_name = parent.name
        #print("parent_name:{}".format(parent_name))
        is_parent_paragraph = (parent_name == 'paragraph')

        if (is_parent_paragraph): return

        print("parse_strong elem:{}".format(elem))
        self.term_list.append(elem.text)

    def getSourceDataAsList(self):
        tag = self.soup.document
        self.source_path = tag['source']
        r = bio()
        data_text = r.readFile(self.source_path)
        self.srt_data_list = data_text.split("\n")
        for index, item in enumerate(self.srt_data_list):
            self.srt_data_list[index] = item.strip()


    def loadPOData(self):
        tag = self.soup.document
        self.source_path = tag['source']
        root_len = len(self.doc_root_dir)
        common_part = self.source_path[root_len:]
        po_part = common_part.replace(".rst", ".po")
        self.po_path = os.path.join(self.doc_po_dir, po_part)
        is_file_there = (os.path.isfile(self.po_path))
        print("self.po_path:{}; is_file_there:{}".format(self.po_path, is_file_there))
        self.po_doc = c.load_po(self.po_path)

    def searchPOData(self, msgid):
        message = None
        is_in_po = (msgid in self.po_doc)
        if (is_in_po):
            message = self.po_doc[msgid]
        return [message, is_in_po]

    def cleanMSGSTR(self, msgstr):
        word_list = msgstr.split("--")


    def searchPODataForValue(self, msgid):
        print("searchPODataForValue:{}".format(msgid))
        print("-" * 50)
        value = None
        if (msgid in self.po_doc):
            message = self.po_doc[msgid]
            value = message.string
            #print("message:{}; trans:{}".format(message, value))
            possible_translated_entry = " -- {}".format(msgid)
            value = value.replace(possible_translated_entry, "")
            possible_translated_entry = "-- {}".format(msgid)
            value = value.replace(possible_translated_entry, "")
            #print("exiting value:{}".format(value))
        return value

    def createWordOnlySearchPattern(self, msgid):
        search_word_list = cm.WORD_SEP.findall(msgid)
        search_pat_list = []
        for word in search_word_list:
            search_pat_list.append("{}.*".format(word))
        search_pattern = "".join(search_pat_list)
        return re.compile(r"{}".format(search_pattern))

    def fuzzySearchPOData(self, msgid):
        print("-" * 50)
        print("fuzzySearchPOData:{}".format(msgid))
        print("-" * 80)


        #p = self.createWordOnlySearchPattern(msgid)
        possible_match=[]
        for m in self.po_doc:
            mid = m.id
            mstr = m.string
            if (len(mid) < 1):
                continue

            mstr = m.string.strip()
            mstr = ("" if (mid == mstr) else mstr)

            dist = DS(msgid, mid)
            #is_menu_selection = ("menuselection" in msgid)
            #is_too_far = (not is_menu_selection) and (dist > 150)
            is_too_far = (dist > 50)
            if (is_too_far):
                #print("fuzzySearchPOData mid:[{}], dist:{}, is_too_far:[{}]".format(mid, dist, is_too_far))
                continue

            #possible_match.append((dist, mid, mstr))
            is_a_subset = (msgid in mid)
            if (is_a_subset):
                possible_match.append((-dist, mid, mstr))
            else:
                #dist = FZ.token_set_ratio(msgid, mid)
                possible_match.append((dist, mid, mstr))

        #sorted_possible_match = sorted(possible_match.items(), key=lambda kv: kv[1], reverse=True)
        #sorted_possible_match = sorted(possible_match.items(), key=lambda kv: kv[1], reverse=False)
        sorted_possible_match = sorted(possible_match)
        for match in sorted_possible_match:
            print("fuzzySearchPOData sorted_possible_match:[{}]".format(match))

        if (len(sorted_possible_match) > 0):
            dist, mid, mstr = (sorted_possible_match[0])
            print("fuzzySearchPOData candidate:[{}], distance:[{}]".format(mid, dist))
            print("=" * 50)
            return [True, mid, mstr]

        print("=" * 50)
        return [False, None, None]

    def fuzzyWordSearchPOData(self, msgid):
        print("-" * 50)
        print("fuzzyWordSearchPOData:{}".format(msgid))
        print("-" * 50)


        p = self.createWordOnlySearchPattern(msgid)
        possible_match=[]
        for m in self.po_doc:
            mid = m.id
            if (len(mid) < 1):
                continue

            mstr = m.string.strip()
            mstr = ("" if (mid == mstr) else mstr)
            match = p.search(mid)
            if (match != None):
                dist = DS(msgid, mid)
                #is_menu_selection = ("menuselection" in msgid)
                #is_too_far = (not is_menu_selection) and (dist > 150)
                is_too_far = (dist > 150)
                if (is_too_far):
                    print("fuzzyWordSearchPOData mid:[{}], dist:{}, is_too_far:[{}]".format(mid, dist, is_too_far))
                    continue

                possible_match.append((dist, mid, mstr))
                #if (msgid in mid):
                    ##possible_match.append((dist - 10, mid, mstr))
                #else:
                    ##dist = FZ.token_set_ratio(msgid, mid)
                    #possible_match.append((dist, mid, mstr))

        #sorted_possible_match = sorted(possible_match.items(), key=lambda kv: kv[1], reverse=True)
        #sorted_possible_match = sorted(possible_match.items(), key=lambda kv: kv[1], reverse=False)
        sorted_possible_match = sorted(possible_match)
        for match in sorted_possible_match:
            print("fuzzyWordSearchPOData sorted_possible_match:[{}]".format(match))

        if (len(sorted_possible_match) > 0):
            dist, mid, mstr = (sorted_possible_match[0])
            print("fuzzyWordSearchPOData candidate:[{}], distance:[{}]".format(mid, dist))
            print("=" * 50)
            return [True, mid, mstr]

        print("=" * 50)
        return [False, None, None]


    def fuzzySearchRSTData(self, msgid):
        print("-" * 50)
        print("fuzzySearchRSTData:{}".format(msgid))
        print("-" * 50)
        possible_match={}

        p = self.createWordOnlySearchPattern(msgid)
        possible_match=[]
        for m in self.srt_data_list:
            mid = m.strip()
            mstr = ""
            match = p.search(mid)
            if (match != None):
                dist = DS(msgid, mid)
                if (msgid in mid):
                    possible_match.append((dist - 10, mid, mstr))
                else:
                    #dist = FZ.token_set_ratio(msgid, mid)
                    possible_match.append((dist, mid, mstr))

        #sorted_possible_match = sorted(possible_match.items(), key=lambda kv: kv[1], reverse=True)
        #sorted_possible_match = sorted(possible_match.items(), key=lambda kv: kv[1], reverse=False)
        sorted_possible_match = sorted(possible_match)
        print("fuzzySearchRSTData sorted_possible_match:[{}]".format(sorted_possible_match))
        if (len(sorted_possible_match) > 0):
            dist, mid, mstr = (sorted_possible_match[0])
            print("fuzzySearchRSTData candidate:[{}], distance:[{}]".format(mid, dist))
            print("=" * 50)
            return [True, mid, mstr]

        print("=" * 50)
        return [False, None, None]


    def removeFromDic(self, text_line):
        is_in_dic = (text_line in self.dic_list)
        if (not is_in_dic): return
        self.dic_list.pop(text_line)
        print("REMOVED FROM DIC:{}".format(text_line))

    def bracketMenuSelection(self, text_line):
        m = cm.MNUSEL.findall(text_line)
        tt = m[0]
        ll = tt.split("-->")

        tt = text_line
        for w in ll:
            w = w.strip()
            wrp = "({})".format(w)
            if (tt.find(wrp) < 0):
                tt = (tt.replace(w, wrp))
        return tt

    def includeEnglishInBrackets(self, text_line):
        pattern = r"\(([^\)]*)\)"
        word_list = re.findall(pattern, text_line);
        has_list = (len(word_list) > 0)

        if (not has_list):
            return text_line

        new_word_list = []
        for w in word_list:
            new_word = "-- {}".format(w)
            new_word_list.append((w, new_word))

        new_text = str(text_line)
        for w, n_w in new_word_list:
            new_text = new_text.replace(w, n_w)
        return new_text

    def fixValueAsMenuSelection(self, k):
        is_menu_selection = (k.find("menuselection") >= 0)
        if (is_menu_selection):
            v = self.bracketMenuSelection(k)
            #print("is_menu_selection:{}".format(v))
        else:
            v = ""
        return v

    def fixValueAsAbbreviation(self, k):
        is_abbreviation = (k.find(":abbr:") >= 0)
        if (is_abbreviation):
            print("{}; is_abbreviation:{}".format(k, is_abbreviation))
            v = self.includeEnglishInBrackets(k)
        else:
            v = ""
        return v

    def removeKeyboardInTranslationIfNeeded(self, text_line):
        p= re.compile(r":kbd:`.*`")
        p1=re.compile(r":kbd:`(?P<key>[\w\d]+)|(?P<modifier>(Enter|Ctrl|Alt|Shift|Home|Insert|PageUp|PageDown|Delete)+[-+](?P=key))*`")
        pex_vn_part=re.compile(r"(NCT)|(NCP)|(NCG)|(LMB)|(MMB)|(RMB)|(Numpad)|(Wheel)|(OS)")
        pdel=re.compile(r"(\.)|(,)|(;)|(and)|(or)|(--)")

        is_remove_pattern = False
        for text_line in t_list:
            found_string = ""
            has_trans=(text_line.find(" -- ") > 1)
            if (has_trans):
                text_line = text_line.split(" -- ")[0]
            m = p.search(text_line)
            if (m != None):
                is_remove_pattern = True
                print("Any Pattern:[{}]".format(m.group(0)))
                found_string=m.group(0)
                n=pex_vn_part.search(found_string)
                if (n != None):
                    print("Exclude Pattern:[{}]".format(n.group(0)))
                    is_remove_pattern = False

            print("Text line before remove:[{}]".format(text_line))
            if (is_remove_pattern):
                text_line = text_line.replace(found_string, "").strip()
                print("Text line after removed:[{}]".format(text_line))

    def getSortedPOData(self, po_doc):
        #unfound_list=["DLS", "SDLS", "Weight", "iTaSC", "iTaSC Solver"]
        #unfound_list=["DLS", "SDLS", "Weight", "iTaSC", "iTaSC Solver"]
        data_list=[]
        for m in po_doc:
            k = m.id
            v = m.string
            data_list.append((k,v))
            #if (k in unfound_list):
                #print("list: k=[{}]; v=[{}]".format(k, v))

        sorted_data_list = sorted(data_list)
        return sorted_data_list

    def unHTMLText_0001(self, text):
        """
        Parameter:  String (unicode or bytes).
        Returns:    The `text`, with each instance of "..." translated to
                    an ellipsis character.

        Example input:  Huh...?
        Example output: Huh&#8230;?
        """
        dic={
            smartchars.ellipsis:"\\.\\.\\.",
            smartchars.apostrophe:"'",
            "+":"\\+",
            "“":"\"",
            "”":"\"",
            "⏮":"|first|",
            "⏭":"|last|",
            "⏪︎":"|previous|",
            "⏩︎":"|next|",
            "◀":"|rewind|",
            "▶":"|play|",
            "⏸":"|pause|",
            "–":"--",
            #"":"",
            #"":"",
             }
        for k,v in dic.items():
            #print("{} -> {} - text before:[{}]".format(k, v, text))
            text = text.replace(k, v)
            #print("{} -> {} - text after:[{}]".format(k, v, text))
        #text = text.replace(smartchars.ellipsis, "...")
        return text

    def unHTMLText_0002(self, text):
        """
        Parameter:  String (unicode or bytes).
        Returns:    The `text`, with each instance of "..." translated to
                    an ellipsis character.

        Example input:  Huh...?
        Example output: Huh&#8230;?
        """

        dic={
            smartchars.ellipsis:"...",
            smartchars.apostrophe:"'",
            "\\+":"+",
            "“":"\\\"",
            "”":"\\\"",
            #"":"",
            "⏮":"|first|",
            "⏭":"|last|",
            "⏪︎":"|previous|",
            "⏩︎":"|next|",
            "◀":"|rewind|",
            "▶":"|play|",
            "⏸":"|pause|",
            "–":"--",
             }

        for k,v in dic.items():
            text = text.replace(k, v)
        return text

        text = text.replace(smartchars.ellipsis, "...")
        text = text.replace(smartchars.apostrophe, "'")

        #text = text.replace(smartchars.ellipsis, "...")
        return text

    def translateKeyBoard(self, k):
        has_keyboard_def = (cm.KEYBOARD_DEF.search(k) != None)
        if (not has_keyboard_def):
            return k

        has_translatable_def = (cm.SPECIAL_DEF.search(k))
        if (not has_translatable_def):
            return k

        new_k = cm.translateKeyboardDef(k)
        return new_k

    def getDocPath(self, text):
        doc_path = re.compile(r"(<document source=\"{}/)(.*)(\.rst\">)".format(RSTToPo.default_man_path))

        m  = doc_path.match(text)
        is_found = (m != None)
        if (is_found):
            g = m.groups(0)

            return g[1]
        else:
            return None

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

    def writeDictionary(self, d_list=None, file_name=None):
        file_path = (self.dic_file if (file_name == None) else file_name)
        dic = (self.dic_list if (d_list == None) else d_list)
        try:
            #print("Length of write dictionary:{}".format(len(dic)))
            #print("dictionary:{}".format(dic))
            print("writeDictionary:{}, size:{}".format(file_path, len(dic)))
            #return
            with open(file_path, 'w', newline='\n', encoding='utf8') as out_file:
                json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
                out_file.close()
        except Exception as e:
            print("Exception writeDictionary".format(file_path))
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

    def parseOneFile(self):
        print("parseOneFile")
        html_data = None
        with open(self.input_file) as fp:
            self.soup = BeautifulSoup(fp, "html.parser")
        self.getSourceDataAsList()
        try:
            self.loadPOData()
        except Exception as e:
            print("ERROR: Unable to load PO file :{}".format(self.po_path))
            print("       as indicated from:{}".format(self.source_path))
            print("       Exception:{}".format(e))
            print("~" * 80)
            return

        sorted_po_data = self.getSortedPOData(self.po_doc)

        #kw = ['title', 'term', 'field_list', 'strong', 'rubric', 'note', 'bullet_list']
        kw = ['title', 'term']
        for k in kw:
            for elem in self.soup.find_all(k):
                self.parse_title(elem)
                self.parse_term(elem)
                #self.parse_field_list(elem)
                #self.parse_rubric(elem)
                #self.parse_strong(elem)
                #self.parse_note(elem)
                #self.parse_bullet_list(elem)

        #sorted_term_list = sorted(list(set(self.term_list)))
        sorted_term_list = self.term_list
        msgid, msgstr = None, None

        pp(sorted_term_list)
        print("Getout")
        exit(0)

        for term in sorted_term_list:
            term = term.strip()
            is_ignore = False
            is_found = False

            msgid = self.unHTMLText_0001(term)
            a_msgid, msgstr = self.binSearch(sorted_po_data, msgid)
            is_found = (msgstr != None)

            #is_found, msgid, msgstr = self.fuzzySearchPOData(term)
            if (not is_found):
                msgid = self.unHTMLText_0002(term)
                msgid = self.removeNewLine(msgid)
                a_msgid, msgstr = self.binSearch(sorted_po_data, msgid)
                is_found = (msgstr != None)
                if (not is_found):
                    a_msgid, msgstr = self.binSearch(sorted_po_data, msgid, is_fuzzy=True)
                    is_found = (msgstr != None)
                    if (not is_found):
                        print("ERROR! Unable to find:[{}]".format(msgid))
                        continue
                    else:
                        msgid = a_msgid

                #is_found, msgid, msgstr = self.fuzzySearchRSTData(term)
                #if (not is_found):

            if (is_found):
                is_ignore = cm.isIgnored(msgid)

            is_doc_path = cm.isDocPath(msgid)
            is_number = cm.isNumber(msgid)
            is_option = (cm.getOption(msgid) != None)
            is_non_alpha_numeric = (cm.isNonAlphaNumeric(msgid))
            is_ignoreable_keyboard = cm.isRemovableKeyboardDef(msgid)

            is_bypass = (is_ignore or is_number or is_option or is_non_alpha_numeric or is_doc_path or is_ignoreable_keyboard)
            if (is_bypass):
                print("Ignored:{}".format(msgid))
                print("is_ignore:{}; is_number:{}; is_option:{}; is_non_alpha_numeric:{}; is_doc_path:{}; is_ignoreable_keyboard:{}".format(is_ignore , is_number , is_option , is_non_alpha_numeric, is_doc_path, is_ignoreable_keyboard))
                #self.removeFromDic("{}".format(msgid))
            else:
                k = msgid
                v = msgstr
                trans_sep = "--"
                has_trans = (not "menuselection" in v) and (trans_sep in v)
                if (has_trans):
                    word_list = v.split(trans_sep)
                    v = word_list[0].strip()

                #v = self.searchPODataForValue(k)
                #print("k=[{}], v=[{}]".format(k, v))
                if (cm.isEmpty(v) or (k == v)):
                    menu_fix = self.fixValueAsMenuSelection(k)
                    bracket_abbrev = self.fixValueAsAbbreviation(k)

                    menu_empty = (cm.isEmpty(menu_fix))
                    bracket_abbrev_empty = (cm.isEmpty(bracket_abbrev))
                    is_both_empty = (menu_empty and bracket_abbrev_empty)
                    has_both = not (menu_empty or bracket_abbrev_empty)
                    v = ""
                    if (not is_both_empty):
                        v = (menu_fix if (bracket_abbrev_empty) else bracket_abbrev)

                    if (has_both):
                        print("ERROR: has both menu and abbreviation")
                        print("menu:{}".format(menu_fix))
                        print("bracket_abbrev:{}".format(bracket_abbrev))
                        exit(1)

                is_kbd = (':kbd:' in k)
                is_abbrev = (':abbr:' in k)
                is_doc = (':doc:' in k)
                is_ref = (':ref:' in k)

                is_copy_k_to_v = (is_kbd or is_abbrev or is_doc or is_ref) and (cm.isEmpty(v))
                if (is_copy_k_to_v):
                    v = self.translateKeyBoard(k)

                #self.global_temp_dic.update({
                    #'key': k,
                    #'value':v
                    #})
                self.global_temp_dic.update({k:v})
                print("[{}] -- [{}]".format(k, v))
                #self.global_term_list.append(term)
                #global_temp_dic.update = sorted(self.global_temp_dic.update, key=lambda k: k['value'])
        #self.global_temp_dic = sorted(self.global_temp_dic.items())
        #pp(self.global_temp_dic)
        self.term_list.clear()

    def parseAllFiles(self):
        #if (not self.dic_list_loaded):
            #self.dic_list = self.readDictionary()
            #self.dic_list_loaded = True

        root_dir="/home/htran/blender_documentations/blender_docs/build/rstdoc"
        the_file_list = self.getFileList(root_dir, ".html")
        for rst_file in the_file_list:
            self.setVars(rst_file)
            self.parseOneFile()
            print("{}".format(rst_file))
            print("=" * 80)

        #for k, v in self.global_temp_dic.items():
            #if (v.startswith("-- ")):
                #print("{} {}".format(k, v))
            #else:
                #print("{} -- {}".format(k, v))
        #sorted_term_list = sorted(list(set(self.global_term_list)))
        #for term in sorted_term_list:
            #k="({})".format(term)
            #v=self.searchPODataForValue(term)
            #if (v == None):
                #is_menu_selection = (k.find("menuselection") >= 0)
                #if (is_menu_selection):
                    #v = self.bracketMenuSelection(term)
                    #print("is_menu_selection:{}".format(v))
                #else:
                    #v=""
            #self.dic_list.update({k:v})
            #self.dic_list_updated=True
            #print("Added to dic:{}".format(k))

        #if (self.dic_list_updated):
            ##print("{}".format(self.dic_list))
            #self.writeDictionary()
        #sorted_term_list = self.global_temp_dic
        #self.writeDictionary(d_list=sorted_term_list)

    def mergeDictionary(self):
        #from_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_0027.json"
        #from_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_0001_test.json"
        #from_dic = "/home/htran/20190507_2002_parse_rst_merge_NOT_Updating_merging.json"
        from_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_0006_test.json"
        to_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_0005_test.json"
        #to_dic = self.dic_file

        from_dic_list={}
        to_dic_list={}
        #to_dic_list = self.dic_list

        #readDictionary(self, d_list=None, file_name=None, flag_to_set=None):
        #writeDictionary(self, d_list=None, file_name=None):
        from_dic_list = self.readDictionary(d_list=from_dic_list, file_name=from_dic)
        to_dic_list = self.readDictionary(d_list=to_dic_list, file_name=to_dic)

        to_dic_changed = False
        for fk, fv in from_dic_list.items():
            #tv = to_dic_list[fk].strip()
            is_update_to = (not fk in to_dic_list)
            #is_update_to = False
            #is_fk_in_to_dic = (fk in to_dic_list)
            #if (is_fk_in_to_dic):
                #tv = to_dic_list[fk].strip()
                #tv_has_translation = (len(tv) > 0)
                #is_update_to = (not tv_has_translation) and (fv != fk)

                #is_update_to = can_update_from_fv
            ##else:
                ##is_update_to = True

            if (is_update_to):
                print("Updating: fk:[{}], fv:[{}]".format(fk, fv))
                to_dic_list.update({fk : fv})
                to_dic_changed = True
            else:
                print("NOT Updating: fk:[{}], fv:[{}]".format(fk, fv))

        sorted_term_list = sorted(to_dic_list)
        if (to_dic_changed):
            print("to dic:{}; size:{}".format(to_dic, len(to_dic_list)))
            #self.writeDictionary()
            #self.writeDictionary(d_list=to_dic_list, file_name=to_dic)
            #pass


    def fuzzySearchInDic(self, word, dic_list):
        print("fuzzySearchInDic - word:[{}]".format(word))
        candidate_list=[]
        for dic_word, trans in dic_list:

            if (len(dic_word) == 0): continue

            dist = DS(word, dic_word)
            #if (word in dic_word):
                #dist = dist-10
            is_acceptable = (dist <= 50)
            if (is_acceptable):
                trans = dic_list[dic_word]
                if (trans != None) and (len(trans) > 0):
                    candidate_list.append((dist, dic_word, trans))
                else:
                    trans=""

        has_trans = (len(candidate_list) > 0)
        if (not has_trans):
            print("getLocalTranslation - Unable to locate TRANSLATION for [{}]".format(word))
            return None

        sorted_possible_match = sorted(candidate_list)
        pp(sorted_possible_match)
        print("getLocalTranslation - Possible Match")
        dist, candidate, trans = sorted_possible_match[0]
        print("getLocalTranslation - word:[{}]; chosen candidate [{}]; trans:[{}]; dist:[{}]".format(word, candidate, trans, dist))
        print("=" * 20)
        return trans

    def searchTransWithCaseVariations(self, dic_list, word):
        list_of_variations=[]
        list_of_variations.append(word.title())
        list_of_variations.append(word.lower())
        list_of_variations.append(word.upper())
        print("searchTransWithCaseVariations:")
        pp(list_of_variations)
        for try_word in list_of_variations:
            trans = self.binSearch(dic_list, try_word)
            if (trans != None):
                print("searchTransWithCaseVariations, found:[{}]".format(trans))
                return trans
        return None

    def matchTransCase(self, word, trans):
        new_trans = trans
        if (word.isupper()):
            new_trans = trans.upper()

        if (word.istitle()):
            new_trans = trans.title()

        if (word.islower()):
            new_trans = trans.lower()

        return new_trans

    def removeNewLine(self, s1):
        return s1.replace("\n", " ")

    def debugDiff(self, s1, s2):
        print("s1:[{}]".format(s1))
        print("s2:[{}]".format(s2))

        s1_length=len(s1)
        s2_length=len(s2)
        length = min(s1_length, s2_length)
        for i in range(0, length):
            s1_c = s1[i]
            s2_c = s2[i]
            is_equal = (s1_c == s2_c)
            range_size=5
            if (not is_equal):
                print("debugDiff:[{}]: s1_c=[{}]; s2_c=[{}]".format(i, s1_c, s2_c))
                start_index = (i-range_size if (i > range_size) else 0)
                end_index = (i+range_size if (i < length-(range_size+1)) else length-1)
                s1_s = s1[start_index:end_index]
                s2_s = s2[start_index:end_index]
                print("debugDiff:[{}]: s1_s=[{}]; s2_s=[{}]".format(i, s1_s, s2_s))

    def binSearch(self, sorted_list , item_to_find, is_fuzzy=False):
        #print("sorted_list: {}, len:{}".format(sorted_list, len(sorted_list)))
        lo  = 0
        hi  = len(sorted_list)
        mid = -1
        #find_word_list=re.findall(r"([^\W]+)")
        while (lo < hi):
            mid  = (lo + hi) // 2
            lst, trans = sorted_list[mid]
            find = item_to_find
            #find = item_to_find.lower()
            #lst = lst.lower()
            #print("binSearch - lo:{}; hi:{}; mid:{} lst:[{}]; find:[{}]".format(lo, hi, mid, lst, find))
            #print("mid:{}, item_on_sorted_list: {}".format(mid, item_on_sorted_list))
            #dist=DS(lst, find)
            #print("({}):find:[{}] --> candidate:[{}]".format(dist, find, lst))
            is_found = (lst == find)

            is_fuzzy_search = ((not is_found) and (is_fuzzy == True))
            if (is_fuzzy_search):
                word_list = cm.WORD_SEP.findall(item_to_find)
                pattern_of_item_to_find = ".*".join(word_list)
                is_found = (re.search(pattern_of_item_to_find, lst) != None)

                #self.debugDiff(lst, item_to_find)
                #html_hex_string = item_to_find.encode("utf-8").hex()
                #po_hex_string = lst.encode("utf-8").hex()
                #is_hex_found = (html_hex_string == po_hex_string)
                #print("html    :[{}]".format(item_to_find))
                #print("html-hex:[{}]".format(html_hex_string))
                #print("po      :[{}]".format(lst))
                #print("po-hex  :[{}]".format(po_hex_string))
                #print("is_hex_found:{}".format(is_hex_found))


            if (is_found):
                if (is_fuzzy_search):
                    return [lst, trans]
                else:
                    return [item_to_find, trans]
            elif (lst < find):
                lo = mid + 1  # range in the higher part
            else:
                hi = mid  # range in the lower part
        return [None, None]

    def getTranslation(self, dic_list, word):
        if (len(word.strip()) == 0):
            return [False, None]

        print("=" * 20)
        print("getLocalTranslation word:[{}]".format(word))

        trans=None
        try_word = word.strip()

        trans = self.binSearch(self.translated_list, try_word)
        if (trans != None):
            print("getTranslation self.translated_list, found:[{}]".format(trans))
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        trans = self.binSearch(dic_list, try_word)
        if (trans != None):
            print("getTranslation dic_list, found:[{}]".format(trans))
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        is_multiple_n = (word.lower().endswith("s")) and (len(word) > 3)
        is_multiple_e = (word.lower().endswith("es")) and (len(word) > 3)
        is_multiple_y = (word.lower().endswith("ies")) and (len(word) > 4)
        is_multiple = (is_multiple_n or is_multiple_e or is_multiple_y)
        if (is_multiple):

            if (is_multiple_y):
                try_word = "{}y".format(word[:-3])
            else:
                try_word = word[:-1]

            print("is_multiple: searching for [{}]; using:[{}]".format(word, try_word))
            #trans = self.searchTransWithCaseVariations(dic_list, try_word)
            trans = self.binSearch(dic_list, try_word)
            if (trans == None):
                trans = self.fuzzySearchInDic(try_word, dic_list)

        is_found = (trans != None) and (len(trans) > 0)
        if (is_found):
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        is_past_tense = (word.lower().endswith("ed"))
        if (is_past_tense):
            try_word = "{}".format(word[:-2])
            print("is_past_tense: searching for [{}]; using:[{}]".format(word, try_word))
            #trans = self.searchTransWithCaseVariations(dic_list, try_word)
            trans = self.binSearch(dic_list, try_word)
            is_found = (trans != None) and (len(trans) > 0)
            if (is_found):
                trans = self.matchTransCase(word, trans)
                return [True, trans]

        if (word in dic_list):
            trans = dic_list[word]
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        #trans = self.searchTransWithCaseVariations(dic_list, word)
        trans = self.binSearch(dic_list, try_word)
        if (trans != None):
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        if (word.endswith("e")):
            try_word = "{}ing".format(word[:-1])
        else:
            try_word = "{}ing".format(word)
        #trans = self.searchTransWithCaseVariations(dic_list, try_word)
        trans = self.binSearch(dic_list, try_word)
        is_found = (trans != None) and (len(trans) > 0)
        if (is_found):
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        try_word = "{}ion".format(word)
        #trans = self.searchTransWithCaseVariations(dic_list, try_word)
        trans = self.binSearch(dic_list, try_word)
        if (trans != None):
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        trans = self.fuzzySearchInDic(word, dic_list)
        is_found = (trans != None) and (len(trans) > 0)
        if (is_found):
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        is_noun = (word.lower().endswith("ion"))
        is_adjective = (word.lower().endswith("ive"))
        is_present_continuing = (word.endswith("ing"))
        is_special_case = (is_noun or is_adjective or is_present_continuing)
        if (is_special_case):
            try_word = word[:-3]
            trans = self.binSearch(dic_list, try_word)
            #trans = self.searchTransWithCaseVariations(dic_list, try_word)
            if (trans == None):
                trans = self.fuzzySearchInDic(try_word, dic_list)

        is_found = (trans != None) and (len(trans) > 0)
        if (is_found):
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        is_adverb = (word.lower().endswith("ionally"))
        if (is_adverb):
            try_word = word[:-4]
            #trans = self.searchTransWithCaseVariations(dic_list, try_word)
            trans = self.binSearch(dic_list, try_word)
            if (trans == None):
                trans = self.fuzzySearchInDic(try_word, dic_list)

        is_found = (trans != None) and (len(trans) > 0)
        if (is_found):
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        is_adverb = (word.lower().endswith("ly"))
        if (is_adverb):
            try_word = "{}e".format(word[:-2])
            #trans = self.searchTransWithCaseVariations(dic_list, try_word)
            trans = self.binSearch(dic_list, try_word)
            if (trans == None):
                trans = self.fuzzySearchInDic(try_word, dic_list)

        is_found = (trans != None) and (len(trans) > 0)
        if (is_found):
            trans = self.matchTransCase(word, trans)
            return [True, trans]

        return [False, word]


    def attempToLocateTranslation(self, sorted_dic, word_list):
        trans_list=[]
        failed_count=0
        num_word = len(word_list)

        print("attempToLocateTranslation:")
        pp(word_list)

        for word in word_list:
            if (len(word) == 0):
                continue

            is_single = (len(word) == 1)
            if (is_single):
                trans_list.append((word, word))
                continue

            is_percent = (word.startswith("%"))
            if (is_percent):
                trans_list.append((word, word))
                continue

            is_ignore = cm.isIgnored(word)
            is_number = cm.isNumber(word)
            is_option = (cm.getOption(word) != None)
            is_non_alpha_numeric = (cm.isNonAlphaNumeric(word))
            is_bypass = (is_ignore or is_number or is_option or is_non_alpha_numeric)
            if (is_bypass):
                trans_list.append((word, word))
                continue

            is_possessive = (word.endswith("'s"))
            if (is_possessive):
                word = word.split("'")[0]

            has_translation, trans = self.getTranslation(sorted_dic, word)
            if (not has_translation):
                print("No translation for:[{}]".format(word))
                trans_list.append((word, word))
                failed_count += 1
                continue

            if (len(trans) > 0):
                if (is_possessive):
                    trans = "của {}".format(trans)
                trans_list.append((word, trans))
                self.translated_list.append((word, trans))
                self.translated_list = sorted(self.translated_list)
                print("Word:[{}]; Translation:[{}]".format(word.lower(), trans))
            else:
                failed_count += 1
                trans_list.append((word, word))
        pp("translation, failed_count:{}".format(failed_count))
        pp(trans_list)
        return [num_word, failed_count, trans_list]

    def testWord(self, sorted_dic, test_word):
        trans = self.binSearch(sorted_dic, test_word)
        print("self.binSearch test_word:{}; trans:{}".format(test_word, trans))

        for index, item in enumerate(sorted_dic):
            k,v = item
            if (k.lower().startswith(test_word)):
                print(index, k, v)

        print("test_word:{}; trans:{}".format(test_word, trans))

        exit(0)

    def testWordList(self, sorted_dic, test_word_list):
        for test_word in test_word_list:
            trans = self.binSearch(sorted_dic, test_word)
            print("self.binSearch test_word:{}; trans:{}".format(test_word, trans))

            for index, item in enumerate(sorted_dic):
                k,v = item
                if (k.lower().startswith(test_word)):
                    print(index, k, v)
            print("test_word:{}; trans:{}".format(test_word, trans))
            print("-" * 20)
        exit(0)

    def lowerCaseList(self, dic_list):
        new_dic = {}
        for k,v in dic_list.items():
            new_dic.update({k.lower():v})
        return new_dic

    def loadPODic(self):
        dic_list={}
        po_dic = "/home/htran/blender_documentations/new_po/vi.po"
        po_data = c.load_po(po_dic)
        for m in po_data:
            if (m.fuzzy): continue
            k = m.id
            v = m.string
            dic_list.update({k:v})
        return dic_list

    def separateDic(self, sorted_dic):
        none_trans = {}
        trans = {}
        for fk, fv in sorted_dic.items():
            is_empty = (len(fk) == 0)
            if (is_empty): continue

            is_needed_translation = (len(fv) == 0)
            if (is_needed_translation):
                none_trans.update({fk : fv})
            else:
                trans.update({fk : fv})
        return [none_trans, trans]


    def getWordList(self, text_line):
        #print("getWordList:\n", text_line)
        #print("-" * 5)
        s2 = re.sub(r"((:kbd:)|(:ref:)|(:doc:)|(:abbr:)|(:menuselection:)|(:class:))", "", text_line, flags=re.I)
        print("removed kbd|ref|doc..\n", s2)

        s1 = re.sub(r"(<[^>]*>)", "", s2)
        print("removed <link>:\n", s1)

        s2 = re.sub(r"(%[\d]{0,2}[sfdi]+)", "", s1, flags=re.I)
        print("removed printf flags:\n", s2)

        s1 = re.sub(r"(\(\))|([_]+)", "", s2, flags=re.I)
        print("removed brackets:\n", s1)

        ##|(\`[^\`]*\`)
        #if (is_simple):
            #tt = re.sub(r"[\,\.\:\;\"\'\`\(\)]+", "", s1)
            #word_list = re.findall(r"[^\s]+", tt)
        #else:
            #word_list = re.findall(r"[^\W]+", s1)

        #word_list = re.findall(r"(\w -']+)", s1)
        word_list = re.findall(r"[^\W]+", s1)
        word_list.sort(key=len, reverse=True)
        filtered = []
        for w in word_list:
            if (len(w) < 2):
                continue
            filtered.append(w.strip())
        word_list = filtered
        return word_list

    def getLineTranslation(self, sorted_dic, text_line):
        trans = self.binSearch(self.translated_list, text_line)
        is_found = (trans != None) and (len(trans) > 0)
        if (is_found):
            return [True, trans]

        trans = self.binSearch(sorted_dic, text_line)
        is_found = (trans != None) and (len(trans) > 0)
        if (is_found):
            return [True, trans]
        return [False, text_line]

    def selfFillTranslation(self):
        from_dic_list={}
        to_dic_list={}

        from_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_0007_test.json"
        to_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_00013_test.json"

        #from_dic_list = self.readDictionary(d_list=from_dic_list, file_name=to_dic)

        from_dic_list = self.readDictionary(d_list=from_dic_list, file_name=from_dic)
        to_dic_list = self.readDictionary(d_list=to_dic_list, file_name=to_dic)

        from_non_trans, from_sorted_dic = self.separateDic(from_dic_list)
        to_non_trans, to_sorted_dic = self.separateDic(from_dic_list)

        #print("non_trans len:{}; sorted_dic len:{}".format(len(non_trans), len(sorted_dic)))
        #po_dic_list = self.loadPODic()

        #z = po_dic_list.copy()
        #z.update(from_dic_list)
        #z.update(self.transtable)
        #self.writeDictionary(d_list=z, file_name=to_dic)
        #exit(0)

        #from_dic_list = {**from_dic_list, **self.transtable}
        #dic_list = from_dic_list.items()
        #tran_list = self.transtable.items()
        #from_dic_list = (dic_list + tran_list)
        from_sorted_dic = self.lowerCaseList(from_sorted_dic)
        #lower_po = self.lowerCaseList(po_dic_list)
        #lower_local = self.lowerCaseList(self.transtable)

        #z = lower_po.copy()
        #z.update(lower_from)
        #z.update(lower_local)
        #sorted_dic = sorted(z.items())
        from_sorted_dic = sorted(from_sorted_dic.items())
        #self.testWord(sorted_dic, "Delete")
        #non_trans = non_trans.items()

        #print("dictionary len after merged:{}".format(len(sorted_dic)))

        #sp_syms = re.compile(r"[:;\*,\.]+")
        dic_changed = False
        for index, item in enumerate(to_non_trans.items()):
            fk, fv = item
            is_empty = (len(fk) == 0)
            if (is_empty): continue

            is_needed_translation = (len(fv) == 0)
            if (not is_needed_translation): continue

            #fk = sp_syms.sub(fk, "")

            print("~" * 50)
            print("fk:[{}]; fv:[{}]".format(fk, fv))

            is_found, trans = self.getLineTranslation(from_sorted_dic, fk)
            if (is_found):
                fv = trans
                self.translated_list.append((fk, fv))
                to_dic_list.update({fk : fv})
                dic_changed = True
                print("whole line - index:[{}] Updating: fk:[{}], fv:[{}]".format(index, fk, fv))
                continue


            word_list = self.getWordList(fk)
            num_word, failed_count, trans_list = self.attempToLocateTranslation(from_sorted_dic, word_list)
            is_found = (trans_list != None) and (len(trans_list) > 0)
            if (is_found):
                fv = str(fk)
                for word, trans in trans_list:
                    fv = fv.replace(word, trans, 1)

                #reversed_list = reversed(trans_list)
                #reversed_list = trans_list
                #fv = " ".join(reversed_list)
                fv = "?{}".format(fv)
                print("index:[{}] Updating: fk:[{}], fv:[{}]".format(index, fk, fv))
                to_dic_list.update({fk : fv})
                dic_changed = True
            print("~" * 50)

        if (dic_changed):
            print("empty line_count:{}; dic:{}; size:{}".format(len(to_non_trans), to_dic, len(to_dic_list)))
            #self.writeDictionary(d_list=to_dic_list, file_name=to_dic)

    def diffDic(self):
        from_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_00011_test.json"
        to_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_00012_test.json"

        from_dic_data = self.readDictionary(file_name=from_dic)
        to_dic_data = self.readDictionary(file_name=to_dic)

        from_data_list = []
        for k,v in from_dic_data.items():
            from_data_list.append((k,v))

        sorted_po = sorted(from_data_list)
        update_count=0
        for k,v in to_dic_data.items():
            kk, trans = self.binSearch(sorted_po, k)
            is_diff = (not cm.isEmpty(v)) and (not cm.isEmpty(trans)) and (v != trans)

            if (not is_diff):
                continue

            to_dic_data.update({k:trans})
            update_count += 1
            print("diff: k=[{}]; from trans:[{}] USING to v=[{}]; ".format(k, v, trans))
            #print("mergeDicChanges - {} update:{}; [{}] -> [{}]".format(update_count, k, v, trans))

        is_dirty = (update_count > 0)
        if (is_dirty):
            print("update_count:{}; dic:{}; update_count:{}".format(update_count, to_dic, len(to_dic_data)))
            #self.writeDictionary(d_list=to_dic_data, file_name=to_dic)


    def mergeDicChanges(self):
        #from_po = "/home/htran/blender_documentations/new_po/vi.po"
        #from_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_0007_test.json"
        from_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_00014_test.json"
        to_dic = "/home/htran/menuselection_new_dictionary_sorted_translated_00015_test.json"

        #po_data = c.load_po(from_po)
        #print("Loaded po:{}; len:{}".format(from_po, len(po_data)))

        from_dic_data = self.readDictionary(file_name=from_dic)
        to_dic_data = self.readDictionary(file_name=to_dic)

        #po = {}
        #for m in po:
            #if (m.fuzzy):
                #continue
            #k=m.id
            #v=m.string
            #po.update({k:v})

        #sorted_po = sorted(self.lowerCaseList(po))
        #print("Loaded sorted_po:{}; len:{}".format(from_po, len(sorted_po)))

        from_data_list = []
        for k,v in from_dic_data.items():
            from_data_list.append((k,v))

        sorted_po = sorted(from_data_list)
        update_count=0
        for k,v in to_dic_data.items():
            kk, trans = self.binSearch(sorted_po, k)
            #is_update = (cm.isEmpty(v)) and (not cm.isEmpty(trans) and (trans != v))
            is_update = (not cm.isEmpty(trans) and (trans != v))

            if (not is_update):
                continue

            to_dic_data.update({k:trans})
            update_count += 1
            print("mergeDicChanges - {} update:{}; [{}] -> [{}]".format(update_count, k, v, trans))


        is_dirty = (update_count > 0)
        if (is_dirty):
            print("update_count:{}; dic:{}; update_count:{}".format(update_count, to_dic, len(to_dic_data)))
            self.writeDictionary(d_list=to_dic_data, file_name=to_dic)


    def run(self):
        if (self.input_file == None):
            self.parseAllFiles()
        else:
            self.parseOneFile()

        #self.mergeDictionary()
        #self.selfFillTranslation()
        #self.mergeDicChanges()
        #self.diffDic()

parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
#parser.add_argument("-i", "--inplace", dest="write_inplace", \
                    #help="Write out the changes to the original file. \
                    #NOTE: Not Recommended! DANGEROUS: Use it at your own peril.", \
                    #action='store_true')
parser.add_argument("-f", "--file", dest="input_file", help="Input rst file.")
args = parser.parse_args()

x = ParseRST()
x.setVars(args.input_file)
x.run()
#x.parseAllFiles()
#x.mergeDictionary()
#x.parseOneFile()

'''
-------------------------
     <title>
      Single Image
     </title>
-------------------
ignore instance from Tables
eg:
<table classes="colwidths-given valign" ids="id2 tab-view3d-modes" names="tab-view3d-modes">
    <title>
     Blender’s Modes
    </title>
-----------------
     <thead>
      <row>
       <entry><paragraph>Icon</paragraph></entry>
       <entry><paragraph>Name</paragraph></entry>
       <entry><paragraph>Details</paragraph></entry>
      </row>
     </thead>
-------------------------
     <term>
      Image
     </term>

        <term>
         New
         <literal>
          +
         </literal>
        </term>
-------------------------
   <bullet_list bullet="-">

    <list_item>
     <paragraph>
      <reference internal="True" refuri="">
       <inline classes="doc">
        Toggles the Projection
       </inline>
      </reference>
     </paragraph>
    </list_item>
    msgid ":doc:`Toggles the Projection </editors/3dview/navigate/projections>`"

    <list_item>
     <paragraph>
      <reference internal="True" refuri="">
       <inline classes="doc">
        Toggles the Camera View
       </inline>
      </reference>
     </paragraph>
    </list_item>
    msgid ":doc:`Toggles the Camera View </editors/3dview/navigate/camera_view>`"

    <list_item>
     <paragraph>
      <reference name="Pans the 3D Viewport" refuri="Panning">
       Pans the 3D Viewport
      </reference>
      <target ids="['pans-the-3d-viewport']" names="['pans the 3d viewport']" refuri="Panning">
      </target>
     </paragraph>
    </list_item>

    <list_item>
     <paragraph>
      <reference name="Zooms the 3D Viewport" refuri="Zooming">
       Zooms the 3D Viewport
      </reference>
      <target ids="['zooms-the-3d-viewport']" names="['zooms the 3d viewport']" refuri="Zooming">
      </target>
     </paragraph>
    </list_item>
    msgid "`Zooms the 3D Viewport <Zooming>`_"

   </bullet_list>
-------------------------

  <admonition classes="refbox">
    <title>
     Reference
    </title>
-------------------------

    <field_list>

     <field>
      <field_name>Mode</field_name>
      <field_body>
       <paragraph>All modes</paragraph>
      </field_body>
     </field>

     <field>
      <field_name>Menu</field_name>
      <field_body>
      msgid "Menu"

       <paragraph>
        <inline classes="menuselection" rawtext=":menuselection:`View --&gt; Navigation --&gt; Orbit`">
         View ‣ Navigation ‣ Orbit
        </inline>
       </paragraph>
      </field_body>
     </field>
    msgid ":menuselection:`View --> Navigation --> Orbit`"

     <field>
      <field_name>
       Hotkey
      </field_name>
      msgid "Hotkey"

      <field_body>
       <paragraph>
        <literal classes="kbd">
         MMB
        </literal>
        ,
        <literal classes="kbd">
         Numpad2
        </literal>
        ,
        <literal classes="kbd">
         Numpad4
        </literal>
        ,
        <literal classes="kbd">
         Numpad6
        </literal>
        ,
        <literal classes="kbd">
         Numpad8
        </literal>
        ,
        <literal classes="kbd">
         Ctrl-Alt-Wheel
        </literal>
        ,
        <literal classes="kbd">
         Shift-Alt-Wheel
        </literal>
       </paragraph>
      </field_body>
     </field>
    msgid ""
    ":kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, "
    ":kbd:`Numpad8`, :kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`"

    </field_list>
   </admonition>

-------------------------------------
   <note>
    <paragraph>
     Hotkeys
    </paragraph>
    <paragraph>
     Remember that most hotkeys affect the
     <strong>
      active
     </strong>
     area (the one that has focus),
so check that the mouse cursor is in the area you want to work in before you use the hotkeys.
    </paragraph>
   </note>

#the first instance of paragraph is THE TITLE??? - if there are one or more instances of paragraph belows
msgid "Hotkeys"

-------------------------------------

   <seealso>
    <bullet_list bullet="-">
     <list_item>
      <paragraph>
       <reference internal="True" refuri="#prefs-input-orbit-style">
        <inline classes="std std-ref">Orbit Style Preference</inline>
       </reference>
      </paragraph>
     </list_item>

     <list_item>
      <paragraph>
       <reference internal="True" refuri="#prefs-interface-auto-perspective">
        <inline classes="std std-ref">
         Auto-Perspective Preference
        </inline>
       </reference>
      </paragraph>
     </list_item>

    </bullet_list>
   </seealso>

msgid ":ref:`Orbit Style Preference <prefs-input-orbit-style>`"
msgid ":ref:`Auto-Perspective Preference <prefs-interface-auto-perspective>`"
-------------------------------------

<hint>
    <paragraph>
     If You Get Lost
    </paragraph>
    <paragraph>
     If you get lost in 3D space, which is not uncommon, two hotkeys will help you:
     <literal classes="kbd">
      Home
     </literal>
     changes the view so that you can see all objects
     <inline classes="menuselection" rawtext=":menuselection:`View --&gt; Frame All`">
      View ‣ Frame All
     </inline>
     ,
while
     <literal classes="kbd">
      NumpadPeriod
     </literal>
     zooms the view to the currently selected objects
when in perspective mode
     <inline classes="menuselection" rawtext=":menuselection:`View --&gt; Frame Selected`">
      View ‣ Frame Selected
     </inline>
     .
    </paragraph>

msgid ""
"If you get lost in 3D space, which is not uncommon, two hotkeys will help"
" you: :kbd:`Home` changes the view so that you can see all objects "
":menuselection:`View --> Frame All`, while :kbd:`NumpadPeriod` zooms the "
"view to the currently selected objects when in perspective mode "
":menuselection:`View --> Frame Selected`."

   </hint>
-------------------------------------
<rubric ids="bpy-types-cyclesrendersettings-texture-limit bpy-types-rendersettings-simplify-subdivision" names="bpy.types.cyclesrendersettings.texture_limit bpy.types.rendersettings.simplify_subdivision">
   Common Settings
  </rubric>
  msgid "Common Settings"
-------------------------------------
<admonition classes="refbox" names="tham\ chiếu\ --\ reference">
    <title>
     Tham Chiếu -- Reference
    </title>
    <field_list>
     <field>
      <field_name>
       Trình Đơn -- Menu
      </field_name>
      <field_body>
       <paragraph>
        <inline classes="menuselection" rawtext=":menuselection:`Cộng Thêm (Add)`">
         Cộng Thêm (Add)
        </inline>
       </paragraph>
      </field_body>
     </field>
     <field>
      <field_name>
       Phím Tắt -- Hotkey
      </field_name>
      <field_body>
       <paragraph>
        <literal classes="kbd">
         Shift-A
        </literal>
       </paragraph>
      </field_body>
     </field>
    </field_list>
   </admonition>

msgid "Reference"
msgstr "Tham Chiếu -- Reference"

msgid "Menu"
msgstr "Trình Đơn -- Menu"

msgid "Hotkey"
msgstr "Phím Tắt -- Hotkey"

msgid ":kbd:`Shift-A`"
msgstr ":kbd:`Shift-A`"

-------------------------------------
'''
