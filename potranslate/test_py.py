#!/usr/bin/env python3
#cython: language_level=3
import re
import os
import json
import time
from collections import OrderedDict, defaultdict

import datetime
import math
from collections import deque
from difflib import SequenceMatcher as SM
from pprint import pprint as PP
# import html
import subprocess as sub

import ignore
from translation_finder import TranslationFinder
from ignore import Ignore as IG
from fuzzywuzzy import fuzz

from sphinx_intl import catalog as c
from pytz import timezone
from common import Common as cm, dd, pp
from matcher import MatcherRecord
from definition import Definitions as df, RefType, TranslationState
from reflist import RefList
import inspect as INP
import copy as CP
import cProfile


def readJSON(file_path):
    with open(file_path) as in_file:
        dic = json.load(in_file, object_pairs_hook=OrderedDict)
    return dic

def writeJSON(file_path, data):
    with open(file_path, 'w+', newline='\n', encoding='utf8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))

class test(object):

    def resort_dictionary(self):
        home_dir = os.environ['BLENDER_GITHUB']
        from_file = os.path.join(home_dir, 'ref_dict_0006_0003.json')
        to_file = os.path.join(home_dir, 'ref_dict_0006_0002.json')

        to_dic = readJSON(from_file)

        sorting = sorted(list(to_dic.items()), key=lambda x: x[0].lower())
        new_dic = OrderedDict(sorting)

        for t_k, t_v in to_dic.items():
            entry = {t_k: t_v}
            new_dic.update(entry)

        sorting = sorted(list(new_dic.items()), key=lambda x: x[0].lower())
        new_dic = OrderedDict(sorting)

        writeJSON(to_file, new_dic)

    # def grepPOTFindPath(self, txt):
    #     ref_dict_list, obs = cm.getRefDictList(txt)
    #     for entry in ref_dict_list:
    #         df.LOG(entry)
    #     return ref_dict_list

    def findRefText(selfI):
        from reflist import RefList
        from ignore import Ignore as ig
        def addDict(txt):
            selected_list.update({txt.strip(): ""})

        def printRef(mm):
            # print(mm.type)
            txt = mm.getSubText()
            if not txt:
                txt = mm.getMainText()
            txt = (df.FILLER_CHAR_PATTERN.sub("", txt))


            is_math = (mm.type == RefType.MATH)
            is_keyboard = (mm.type == RefType.KBD)
            is_ignore = (is_keyboard or is_math)
            if is_ignore:
                return

            is_ignore = ig.isIgnored(txt)
            if is_ignore:
                print(f'IGNORED: [{txt}]')
                return

            entry=None
            has_ref_link = (df.REF_LINK.search(txt) is not None)
            has_menu_sep = (df.MENU_SEP.search(txt) is not None)
            if has_ref_link:
                found_dict = cm.findInvert(df.REF_LINK, txt, is_reversed=True)
                for sub_loc, sub_mm in found_dict.items():
                    sub_txt = sub_mm.getMainText()
                    is_in_dict = (sub_txt in dict)
                    if not is_in_dict:
                        addDict(sub_txt)
            elif has_menu_sep:
                word_list = cm.findInvert(df.MENU_SEP, txt, is_reversed=True)
                for loc, mnu_item_mm in word_list.items():
                    sub_txt: str = mnu_item_mm.txt
                    left, mid, right = cm.getTextWithin(sub_txt)
                    is_in_dict = (mid in dict)
                    if not is_in_dict:
                        addDict(sub_txt)
            else:
                is_in_dict = (txt in dict)
                if not is_in_dict:
                    addDict(txt)

        def filterOneLine(m):
            id = m.id
            if not id:
                return

            # print(id)
            ref = RefList(msg= id, tf=tf)
            ref.findPattern(df.pattern_list, id)
            for loc, mm in ref.items():
                printRef(mm)

        selected_list = {}
        tf = TranslationFinder()
        dict = tf.getDict()
        home = os.environ['BLENDER_MAN_EN']
        file_name = 'build/gettext/blender_manual.pot'
        file_path = os.path.join(home, file_name)
        data = c.load_po(file_path)
        data_list = [x for x in data]
        for m in data_list:
            filterOneLine(m)

        home = os.environ['HOME']
        output_file = os.path.join(home, "untran.json")
        cm.writeJSONDic(selected_list, output_file)

    def findUnknownRefs(self):
        home = os.environ['BLENDER_MAN_EN']
        file_name = 'build/gettext/blender_manual.pot'
        file_path = os.path.join(home, file_name)

        tf = TranslationFinder()
        backup_dict = tf.backup_dic_list
        data = c.load_po(file_path)
        for m in data:
            id = m.id
            ref = RefList(msg=id, tf=tf)
            ref.parseMessage()
            ref.translate()
        tf.writeBackupDict()

    def test_0001(self):
        word = r'[\w_\-]+'
        word_space = r'[\w\-_\s]+'
        word_any = r'.*[\w\W]+.*(?<!\s)'
        # ending = r'(\s|$)?'
        embpart_terminator = r'(\s|\b|$)?'
        # embpart_terminator = ''
        ending = r'(\W\b|$)?'
        leading = r'\s?'

        # ast_quote_txt = r'([\*]+)(\w[^\*]+\w)([\*]+)'
        any_part_txt = r'(%s)' % (word_any)
        not_emb_part = r'(the|a|an)'
        not_eq_part = r'%s(?!(%s)\w+)%s' % (leading, not_emb_part, ending)
        ending_emb_part = r'ion'
        ending_part = r'%s(%s%s)%s' % (leading, word, ending_emb_part, ending)

        final_pat = r'%s%s' % (not_eq_part, ending_part)
        simplified_pat = final_pat.replace('\\s?\\s?', '\\s?')
        simplified_pat = simplified_pat.replace('\\s?( )\\s?', '\\s?')

        simplified_pat = r'(\w+)\s?(\w+(ion))'
        pat = re.compile(simplified_pat, flags=re.I)

        t = "**not** the orientation"
        m = pat.search(t)
        print(m)

    def test_translate_0001(self, text_list=None):
        from paragraph import Paragraph as PR
        from sentence import StructRecogniser as SR

        if not text_list:
            t_list = [
                "and by extension, the Material Preview mode",
                # "and hence take it \"away\" from its \"keyed position\"",
                # "and the *Offset* value described below, too",
                # "and use *Object Transform*",
                # "and/or the :ref:`context menu <editors-outliner-editing-context_menu>`",
                # "and/or the `context menu`_, see below",
                # "antonioya",
                # "any number 0 or greater, nominal value is 1.0",
                # "any number greater than 0, nominal value is 1.0",
                # "any number, the nominal value is 0",
                # "applies to *Plane*, *Circle* and *Grid*",
                # "as for *Less*, all linked points are always selected, and of course, *More* cannot add any",
                # "as usual, :kbd:`LMB` to select, :kbd:`RMB` to deselect",
                # "as usual, cancel the move with :kbd:`RMB`, or :kbd:`Esc`",
                # "as well as helping to keep the animation of related objects together in the NLA editor for instance",
                # "as well as helping to keep the animation of related objects together in the NLA for instance",
                # "as with texture baking",
                # "as you can see it in the *Transform* panel, in the 3D Viewport's Sidebar",
                # "assign, select...",
                # "assuming *Preserve Volume* is enabled",
                # "assuming the mesh has a uniform density",
                # "at 0.5, it gives a *Minkowski 1/2*",
                # "at 4.0, it gives a *Minkowski 4*, at 10.0, a *Chebychev*",
                # "at frame 200",
                # "at frame 65",
                # "at the top left side",
                # "at the top/bottom of the editor area",
                # "at the upper left corner",
                # "atomic, van der Waals or as specified in the custom data file [predefined]",
                # "attempting to load a library built for a different version of Python, or loading a 32-bit library on a 64-bit system",
                # "audio strips can still be loaded normally",
                # "author's Github repository",
                # "auto/fixed, and number",
                # "automatic curve handles",
                # "available from the context menu, *Vertices*, *Edges* and *Faces* menus",
                # "available in distortion mode only",
                # "available in reconstruction mode only",
                # "axis locking page",
            ]
        else:
            t_list = text_list

        s_time = time.perf_counter()
        tf = TranslationFinder()
        out_put_list=[]
        for t in t_list:
            pr = PR(t, translation_engine=tf)
            pr.translateAsIs()
            # pr.translateSplitUp()
            output = pr.getTextAndTranslation()
            out_put_list.append(output)

        e_time = time.perf_counter()
        p_time = (e_time - s_time)
        print(f'p_time:{p_time}')
        for o in out_put_list:
            print(o)

        # tf.writeBackupDict()

    def run(self):
        # self.test_0001()
        # import cProfile
        # self.findRefText()
        # self.findUnknownRefs()
        self.resort_dictionary()
        self.test_translate_0001()


x = test()
# cProfile.run('x.run()', 'test_profile.dat')
#
# import pstats
# from pstats import SortKey
#
# with open('output_time.txt', 'w') as f:
#     p = pstats.Stats('test_profile.dat', stream=f)
#     p.sort_stats('time').print_stats()
#
# with open('output_calls.txt', 'w') as f:
#     p = pstats.Stats('test_profile.dat', stream=f)
#     p.sort_stats('calls').print_stats()

x.run()


