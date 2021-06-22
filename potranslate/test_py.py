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
                "\"closest\" can be a bit ambiguous",
                # "\"moving\"",
                # "\"radial\" falloff",
                # "\"small\" joint",
                # "#cos(frame)",
                # "#frame / 20.0",
                # "#python",
                # "#sin(frame)",
                # "(Crepuscular Rays)",
                # "(Deform, ...)",
                # "(Locked, ...)",
                # "(Min + Max)/2",
                # "(Multiply Vertex Group by Envelope, ...)",
                # "(X)",
                # "(origin, vertex_coordinates)",
                # "(sin( )*4)",
                # "**not** applicable for most data-blocks which have no file reference",
                # "**not** by a newline",
                # "*Center*",
                # "*Expected* \\*",
                # "*Mirror*",
                # "*Scripted Expression*",
                # "*confirm on release*",
                # "*i* × *s* + *o*",
                # "*undo*",
                # "*x*\\ :sup:`e` + *y*\\ :sup:`e` + *z*\\ :sup:`e`",
                # "+WT",
                # "+WT2",
                # "+q1",
                # "+q11",
                # "--log \"*undo*\"",
                # "-E CYCLES",
                # "-f -2",
                # "-f 10",
                # "-s 10 -e 500",
                # "-t 2",
                # "./datafiles/ ...",
                # "./python/ ...",
                # "1 - alpha",
                # "1.0, 0.707 = sqrt(0.5), 0.354 = sqrt(2)/4, and 0.25",
                # "16-bit",
                # "1m 3mm",
                # "1m, 3mm",
                # "2.2mm + 5' / 3\" - 2yards",
                # "20 °C",
                # "2m 28.5cm",
                # "32-bit",
                # "4 × 8 bits",
                # "5.969 - 0.215\\beta_{N} + 2.532\\beta_{N}^{2} -\n10.73\\beta_{N}^{3} + 5.574\\beta_{N}^{4} + 0.245\\beta_{N}^{5}\\right",
                # "8-bit",
                # ":doc:`operator </scene_layout/object/editing/link_transfer/transfer_mesh_data>` or :doc:`modifier </modeling/modifiers/modify/data_transfer>`",
                # ":kbd:`Ctrl-LMB` drag",
                # ":kbd:`Ctrl`",
                # ":kbd:`G` to move",
                # ":kbd:`NumpadMinus` -- eight times",
                # ":kbd:`Shift-'` to replace existing links",
                # ":kbd:`Shift-LMB` drag",
                # ":kbd:`Wheel`",
                # ":kbd:`Z` key",
                # ":menuselection:`Add --> Armature`",
                # ":menuselection:`Armature --> Viewport Display` panel",
                # ":menuselection:`File --> New`",
                # ":menuselection:`Key --> Keyframe Type`",
                # ":menuselection:`Properties --> Bone --> Deform Panel`",
                # ":menuselection:`UV Editor --> UV --> Export UV Layout`",
                # ":ref:`Developer Extras <prefs-interface-dev-extras>` only",
                # ":term:`Fireflies`",
                # ":term:`IOR`",
                # "@CTRL",
                # "@DEF",
                # "Agent",
                # "Axon D",
                # "COR",
                # "CUDA+CPU",
                # "Collada, ...",
                # "Copy Grease Pencil Effects",
                # "CoreAudio",
                # "Ctrl Shift C",
                # "Current POV syntax is closer to C than Python, so anything that follows two slash character (``//``) is a comment.",
                # "Curve Edit",
                # "Curve Editing",
                # "DCI-P3",
                # "DEF",
                # "DEF-",
                # "DV",
                # "Dealga McArdle",
                # "Define Overrides",
                # "DensityUP1D",
                # "Disables selection for the collection in all view layers -- affects 3D Viewport -- chaining.",
                # "Disables the collection from being rendered in all view layers -- affects render -- chaining.",
                # "Disables the collection in all view layers -- affects 3D Viewport -- chaining.",
                # "DolphinDream",
                # "E.g. depending on the rest position of your elbow, it may be from (0 to 160) or from (-45 to 135).",
                # "E.g. explaining how mesh smoothing algorithms work is unnecessary, but the blending types of a Mix node do need a mathematical explanation.",
                # "Enabling previews adds 65536 bytes to the size of each blend-file (unless it is compressed).",
                # "Eoan, Focal",
                # "Excludes the collection from the current view layer -- affects both 3D Viewport and render -- non-chaining.",
                # "Expected",
                # "FFmpeg -b:v",
                # "Fades",
                # "Fig. :ref:`fig-meta-ball-example`",
                # "Fig. :ref:`fig-softbody-collision-plane1`",
                # "Fig. :ref:`fig-softbody-collision-plane2`",
                # "Fweeb",
                # "GEO",
                # "HS + V",
                # "HV + S",
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
            print(output)
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


