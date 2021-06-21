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
                "quad only",
                # "quaternion is normalized",
                # "rabbit",
                # "randomly",
                # "rating system performs",
                # "rays",
                # "re-textured",
                # "real-world",
                # "recently",
                # "register an extension prefix",
                # "regrouping",
                # "relations page",
                # "relative file path",
                # "remarks",
                # "rendered shading",
                # "rendering animation",
                # "rendering camera",
                # "rendering to videos",
                # "resets",
                # "retinal rivalry areas",
                # "reversed order",
                # "ribbon",
                # "right within the UI controls",
                # "rings of influence",
                # "ripple edit",
                # "roll rotation",
                # "roofs",
                # "root bone",
                # "root handle",
                # "root of the bone",
                # "rotation pivot point",
                # "sRGB Color Space",
                # "same thing",
                # "same-named pose",
                # "scale transformation",
                # "scaled",
                # "scene dicing rate",
                # "scene linear",
                # "scene settings",
                # "scene's active camera",
                # "scene-wide bounce settings",
                # "screw hardware example.blend",
                # "screw spring example.blend",
                # "sculpt_mask_clear-data",
                # "sea level",
                # "see example blend-file",
                # "see the example on GitHub",
                # "see this",
                # "sees",
                # "selecting in the 3D View",
                # "selection ring",
                # "several independent websites",
                # "several modes",
                # "shader socket",
                # "shading nodes",
                # "shallow link",
                # "shared",
                # "sid",
                # "side suffix",
                # "side views",
                # "simplify panel",
                # "sin(x)/x",
                # "single precision",
                # "single scattering",
                # "single-user",
                # "skinned",
                # "skinning pages",
                # "skinning section",
                # "slow motion",
                # "small dot and grayed out",
                # "smaller than",
                # "smart",
                # "smooth fan",
                # "snap tool",
                # "snap tools",
                # "snapping tools",
                # "soft limit",
                # "solar",
                # "solids",
                # "solved camera motion",
                # "solved object motion",
                # "specular to diffuse",
                # "specular to specular",
                # "spinal",
                # "spiral methodology",
                # "splitting the area",
                # "squarish",
                # "standard normal meshes",
                # "standard selection",
                # "standard text editing shortcuts",
                # "start joint",
                # "stashed",
                # "stashing",
                # "statistically",
                # "stepping effect",
                # "stitching",
                # "stronger",
                # "sub-grids",
                # "sub-quad",
                # "sudo nano /etc/paths",
                # "supported platforms",
                # "surface curves",
                # "surface shader",
                # "svn add /path/to/file",
                # "svn rm /path/to/file",
                # "swept",
                # "symmetrical names",
                # "tabs and panels",
                # "take them back",
                # "taper curve",
                # "target field",
                # "target weight",
                # "tex",
                # "texel",
                # "texture data-block",
                # "texture-space coordinates",
                # "textured brush pack",
                # "th",
                # "the generic coding of moving pictures and associated audio information",
                # "the resources",
                # "their documentation",
                # "this Pixar paper",
                # "this blend",
                # "this picture",
                # "this post",
                # "this section",
                # "tip bone",
                # "tip handle",
                # "too close",
                # "tool-annotate",
                # "top -o %MEM",
                # "top -o MEM",
                # "topbar-app_menu",
                # "topbar-render",
                # "trackers",
                # "tracking or masking",
                # "traditional",
                # "transform center",
                # "transform gizmos",
                # "transform precision/snap",
                # "translucent(N)",
                # "transverse Mercator",
                # "tris, quads & n-gons",
                # "trivially cyclic curves",
                # "true time",
                # "turning",
                # "two new bones",
                # "ui-eyedropper",
                # "ui_template_list diff",
                # "um's",
                # "unbunch",
                # "unconnected",
                # "underline settings",
                # "unit line thickness",
                # "units per frame",
                # "unlinked",
                # "unselectable",
                # "unwrapped",
                # "upward",
                # "upward-most",
                # "vertex snapping",
                # "vertex/edge selection",
                # "visually",
                # "volume objects",
                # "volume shader",
                # "wake",
                # "walking",
                # "wall-thickness",
                # "walls",
                # "wave factor",
                # "wear",
                # "weight = 1",
                # "weight groups",
                # "weight maps",
                # "weighted",
                # "wet paint",
                # "wetmap",
                # "which are not already parented",
                # "while panicked",
                # "white ring",
                # "whitespace",
                # "whole bones",
                # "wire removal",
                # "yadif",
                # "zero level",
                # "zero weights/radii",
                # "zoom level",
                # "{base path}/{file name}{frame number}.{extension}"
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
        tf.writeBackupDict()

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


