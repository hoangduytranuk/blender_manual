#!/usr/bin/env python3
#cython: language_level=3
import re
import os
import json
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



    def test_translate_0001(self, text_list=None):
        from paragraph import Paragraph as PR
        from sentence import StructRecogniser as SR

        if not text_list:
            t_list = [
                "**not** the orientation, which is always perpendicular to the face",
                # "**not** the orientation",
                # "Center",
                # "Scripted Expression",
                # "confirm on release",
                # "3 boxes with dashed outline",
                # "operator",
                # ":kbd:`LMB` drag",
                # ":kbd:`LMB` or the :kbd:`Pen` tip",
                # ":kbd:`Shift-LMB` on the chain icon to the right",
                # ":kbd:`Shift-Spacebar` for play",
                # ":kbd:`Shift` extends, :kbd:`Ctrl` expands",
                # "Add",
                # "Armature",
                # "File",
                # "Key",
                # "Movie Clip Editor",
                # "UV Editor",
                # "Developer Extras",
                # "Fireflies",
                # "IOR",
                # "NDOF",
                # "Object Origin",
                # "Pixel",
                # "see also",
                # "A Render Layer could be substituted for the Image layer, and the",
                # "A typical method to create the fake depth-shaded image is by using a linear blend texture for all objects in the scene or by using the",
                # "Add Constraint",
                # "Add Constraint (with Targets)",
                # "Affects all selection modes.",
                # "Agent",
                # "Alembic",
                # "All these formats support compression which can be important when rendering out animations.",
                # "Appears in the :ref:`bpy.ops.screen.redo_last` panel.",
                # "Attribute Combine",
                # "Attribute Combine XYZ Node",
                # "Attribute Convert",
                # "Attribute Curve Map",
                # "Attribute Remove",
                # "Attribute Separate",
                # "Attribute Separate XYZ Node",
                # "Attribute Transfer",
                # "Attribute Vector Rotate Node",
                # "Automatically Pack Resources",
                # "Average Tracks",
                # "Axon D",
                # "BSDF (Bidirectional Scattering Distribution Function)",
                # "BSDF (Bidirectional scattering distribution function)",
                # "BSSRDF (Bidirectional subsurface scattering distribution function)",
                # "Blender 2.78",
                # "Blender Development, general information and helpful links.",
                # "Blender goes Open Source, 1st Blender Conference.",
                # "Blue minus Luminance",
                # "Box outline",
                # "Bézier curve icon",
                # "CAD",
                # "Computer-Aided Design",
                # "Computer-Generated Imagery",
                # "Central Processing Unit",
                # "Compute Unified Device Architecture",
                # "Cameras & Markers (.py)",
                # "Clemens Barth et al. --",
                # "Collada, ...",
                # "Collection Properties",
                # "Continuing our previous example, imagine that, having initially laid the box flat on the tabletop, you now cut it into smaller pieces, somehow stretch and/or shrink those pieces, and then arrange them in some way upon a photograph that is also lying on that tabletop.",
                # "Copy Grease Pencil Effects",
                # "Copy Modifiers",
                # "Copy UV Maps",
                # "CoreAudio",
                # "Corner Rounding",
                # "Courant–Friedrichs–Lewy",
                # "Crease Threshold",
                # "Ctrl Shift C",
                # "Current POV syntax is closer to C than Python, so anything that follows two slash character",
                # "Curve Edit",
                # "Curve to Mesh",
            ]
        else:
            t_list = text_list

        tf = TranslationFinder()
        for t in t_list:
            pr = PR(t, translation_engine=tf)
            # pr.translateAsIs()
            pr.translateSplitUp()
            # output = pr.getTranslation()
            output = pr.getTextAndTranslation()
            df.LOG(output)

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

    def run(self):
        # self.test_0001()
        # import cProfile
        # self.findRefText()
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


