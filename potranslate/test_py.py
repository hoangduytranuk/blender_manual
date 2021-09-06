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
import cProfile, pstats, io

# cd ../blender_docs
# pip3 install --user -r requirements.txt 
# pip3 --user install --upgrade pip
# sudo pip3 install --upgrade pip
# pip3 install --user urlextract fuzzywuzzy python-Levenshtein

def profile(fnc):

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()

        s = io.StringIO()
        # sortby = 'cumulative'
        sortby = 'ncalls'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

        return retval

    return inner

def readJSON(file_path):
    with open(file_path) as in_file:
        dic = json.load(in_file, object_pairs_hook=OrderedDict)
    return dic

def writeJSON(file_path, data):
    with open(file_path, 'w+', newline='\n', encoding='utf8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))

class test(object):

    def resort_dictionary(self):
        def splitULcase():
            ucase_dict = {}
            lcase_dict = {}
            t_k: str = None
            t_v: str = None
            for t_k, t_v in to_dic.items():
                entry = {t_k: t_v}
                is_lower = t_k.islower()
                if is_lower:
                    lcase_dict.update(entry)
                else:
                    ucase_dict.update(entry)
            return ucase_dict, lcase_dict

        def makeTempLcaseDict(ucase_dict):
            ucase_lower_temp_list = [(x.lower(), y) for x, y in ucase_dict.items()]
            ucase_lower_temp_dict = OrderedDict(ucase_lower_temp_list)
            return ucase_lower_temp_dict

        def getRemoveAndUpdateList(ucase_dict, lcase_dict):
            rm_from_lower_list=[]
            upd_tran_with_lower_list=[]
            for t_k, t_v in ucase_dict.items():
                lcase_t_k = t_k.lower()
                is_in_lower = (lcase_t_k in lcase_dict)
                if not is_in_lower:
                    continue

                lcase_t_v = lcase_dict[lcase_t_k]
                is_same = (lcase_t_v == t_v.lower())
                if is_same:
                    rm_from_lower_list.append(lcase_t_k)
                else:
                    upd_tran_with_lower_list.append(lcase_t_k)

            return rm_from_lower_list, upd_tran_with_lower_list

        def printRemoveList(rm_from_lower_list):
            if not rm_from_lower_list:
                return

            for t_k in rm_from_lower_list:
                print(f'REMOVE: "{t_k}":')

        def printUpdTran(upd_tran_with_lower_list, lcase_list, ucase_lower_temp_dict):
            if not upd_tran_with_lower_list:
                return

            dd(f'*' * 80)
            dd(f'MERGED V:')
            for t_k in upd_tran_with_lower_list:
                lcase_list_v = lcase_list[t_k]
                ucase_list_v = ucase_lower_temp_dict[t_k]
                is_same = (lcase_list_v.lower() == ucase_list_v.lower())
                if is_same:
                    continue

                merged_v = f'{ucase_list_v}/{lcase_list_v}'
                print(f'"{t_k}": "{merged_v}",')

        def updateToNewdict(sorted_list):
            new_dic = OrderedDict()
            for k, v in sorted_list:
                entry = {k: v}
                new_dic.update(entry)
            return new_dic

        def sortLower(item):
            (k, v) = item
            return k.lower()

        home_dir = os.environ['BLENDER_GITHUB']
        from_file = os.path.join(home_dir, 'ref_dict_0006_0003.json')
        to_file = os.path.join(home_dir, 'ref_dict_0006_0002.json')

        to_dic = readJSON(from_file)

        sorted_list = sorted(list(to_dic.items()), key=sortLower)
        new_dict = OrderedDict(sorted_list)
        writeJSON(to_file, new_dict)


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

    def loadData(self, file_path, is_lower=True):
        return_dict = OrderedDict()
        dic = cm.loadJSONDic(file_name=file_path)
        if is_lower:
            data = [(k.lower(), v) for (k, v) in dic.items()]
        else:
            data = list(dic.items())

        data.sort()
        return_dict.update(data)
        return return_dict

    def cleanSS(self):
        def getOrEntries(txt):
            mm: MatcherRecord = None
            any_part = r'([^()`]+)?'
            bracketted_part = r'(\(([^\(\)]+)\))|\`([^\`]+)\`'
            pat_txt = r'%s(%s)%s' % (any_part, bracketted_part, any_part)
            pat = re.compile(pat_txt)
            part_match_dict = cm.patternMatchAll(pat, txt)
            found_parts = []
            for loc, mm in part_match_dict.items():
                txt_loc = mm.getSubLoc()
                txt = mm.getSubText()
                if not txt:
                    txt = mm.getType()
                    txt_loc = mm.getTypeLoc()

                or_list = txt.split('|')
                is_or_list = (len(or_list) > 1)
                if not is_or_list:
                    continue

                entry = (txt_loc, or_list)
                found_parts.append(entry)
            return found_parts

        def composeSubEntries(orig_txt_list, loc, or_list):
            new_line_list = []
            for orig_txt in orig_txt_list:
                for or_clause in or_list:
                    new_line = cm.jointText(orig_txt, or_clause, loc)
                    new_line_list.append(new_line)
            return new_line_list

        def cleanLine(old_line):
            clean_new_k_pat_txt = r'[()`\[\]\^\\]'
            clean_spaces_pat_txt = r'[\s]+'
            clean_spaces_pat = re.compile(clean_spaces_pat_txt)
            clean_new_k_pat = re.compile(clean_new_k_pat_txt)

            has_spaces = ('\\s' in old_line)
            if has_spaces:
                dd('debug')
            new_line = old_line.replace('\\s', ' ')

            new_line = clean_new_k_pat.sub('', new_line)
            new_line = clean_spaces_pat.sub(' ', new_line)
            new_line = new_line.strip()
            return new_line

        rep_keywords = r'(\/?(\d|ED|LD|EX|EQ|NP|NC|MX\d+|\\w|\+|\?|\\d|\\W))'
        re_pat_txt = r'(\$\{)|%s?|(\})' % (rep_keywords)
        pat = re.compile(re_pat_txt)

        home_dir = os.environ['BLENDER_GITHUB']
        sent_struct_file = os.path.join(home_dir, "ref_dict_ss_0001.json")
        ss_dict = self.loadData(sent_struct_file, is_lower=False)
        for k, v in ss_dict.items():
            dd(f'orig:[{k}]')
            new_k = pat.sub("", k)
            is_or = ('|' in new_k)
            if is_or:
                found_or_list = getOrEntries(new_k)
                found_or_list.sort(reverse=True)

                group_of_new_lines=[new_k]
                for loc, or_list in found_or_list:
                    new_group = composeSubEntries(group_of_new_lines, loc, or_list)
                    group_of_new_lines = new_group
            else:
                group_of_new_lines = [new_k]

            cleaned_group = map(cleanLine, group_of_new_lines)
            cleaned_group_list = list(cleaned_group)
            dd('-' * 30)
            pp(cleaned_group_list)
            dd('*' * 30)

    # @profile
    def test_translate_0001(self, text_list=None):
        from paragraph import Paragraph as PR
        from sentence import StructRecogniser as SR
#
        def checkTranslation(orig_txt):
            tran = tf.isInDict(orig_txt)
            return (orig_txt, tran)

        def checkAndRemoveTranslated():
            tran_list = list(map(checkTranslation, t_list))
            remove_list=[]
            keep_list=[]
            for (orig_txt, tran) in tran_list:
                if tran:
                    remove_list.append(orig_txt)
                else:
                    keep_list.append(orig_txt)
            print(f'removed: [{len(remove_list)}]')
            for txt in keep_list:
                msg = f'"{txt}",'
                print(msg)


        if not text_list:
            t_list = [
                # "Syncing Overrides",
                # "System Operators",
                # "System Overrides",
                # "System Requirements",
                # "Tablet API (Windows only)",
                # "Tabs and Text Size",
                # "Tail (Boolean)",
                # "Tail Position (integer)",
                # "Tail X, Y, Z",
                # "Tangential Distortion Coefficients (P1, P2)",
                # "Taper Mode",
                # "Target Attribute",
                # "Target Geometry",
                # "Target Layer",
                # "Target Material",
                # "Target Space & Owner Space",
                # "Target for constraints",
                # "Target/Owner",
                # "Teapot by Anthony D'Agostino",
                # "Tear Boundaries",
                # "Technical Note",
                # "Template Scripts",
                # "Tension Springs",
                # "Terminology",
                # "Text & Search Fields",
                # "Text Auto Complete :kbd:`Tab`",
                # "Text Menu",
                # "Texture Channels",
                # "Texture Distortion Decrease",
                # "Texture Distortion Increase",
                # "Texture Influence",
                # "Texture Mapping Modifier",
                # "Texture Paint Tools",
                # "Texture Resolution",
                # "Texture Resolution (min - max)",
                # "Texture Size in Meters",
                # "Texture channel variations.",
                # "The \"Dancing\" Black Borders",
                # "The Anti-Aliasing node has three properties shown here.",
                # "The Armature Object",
                # "The Big Picture",
                # "The Blender Community",
                # "The Brush",
                # "The Clipping Region",
                # "The Extrapolate principles.",
                # "The Filter node has seven modes, shown here.",
                # "The Mask modifier in Armature mode.",
                # "The Mask modifier in Vertex Group mode.",
                # "The Nvidia OpenGL driver lost connection with the display driver",
                # "The Offset/Power/Slope Formula",
                # "The Process",
                # "The Simple Case",
                # "The Source of the Noise",
                # "The Spring Example",
                # "The Weighting Color Code",
                # "The different Gizmos.",
                # "The effect of corner rounding.",
                # "The image with various alpha and gray-scale values.",
                # "The start!",
                # "The system did not find a solution",
                # "Theme colors",
                # "Thickness :kbd:`D`",
                # "Thickness Clamp",
                # "Thickness Controls",
                # "Thickness Mode :guilabel:`Complex Mode`",
                # "Thickness Modifier",
                # "Thickness, Custom Color",
                # "Third-party glTF Extensions",
                # "This image shows how the Warp transform is influenced by the location of the cursor.",
                # "This image shows the influence of the current view.",
                # "Three Edges",
                # "Tile Offset X, Y, Z",
                # "Tiles X, Y",
                # "Time Panel",
                # "Timesteps Minimum",
                # "Tint Tool",
                # "Tint gradient color sample.",
                # "Tint uniform color sample.",
                # "Tips for Nice Setups",
                # "Tips: Preventing Collapse",
                # "Tissue",
                # "Title Caps",
                # "Title Safe Margins X/Y",
                # "To Sphere :kbd:`Shift-Alt-S`",
                # "Toggle Bold, Italics, Underline, Small Caps",
                # "Toggle Brush Gradient",
                # "Toggle Comments :kbd:`Ctrl-Slash`.",
                # "Toggle Cyclic :kbd:`Alt-C`",
                # "Toggle Gradient",
                # "Toggle Muting :kbd:`H`",
                # "Toggle Pin",
                # "Toggle Preserve State",
                # "Toggle Sequencer/Preview :kbd:`Ctrl-Tab`",
                # "Toggle Stack",
                # "Toggling Interaction Modes",
                # "Tone :guilabel:`Compositor Only`",
                # "Tone Map Modifier",
                # "Tool Selection",
                # "Tool System",
                # "Tool Theme Overrides",
                # "Tool Type :kbd:`Spacebar`",
                # "Tool Type :kbd:`W`, :kbd:`X`",
                # "Toolbar :kbd:`T`",
                # "Tools Settings",
                # "Top Baseline",
                # "Topology Falloff",
                # "Topology Mapping",
                # "Topology Recursive Step",
                # "Torso Bones",
                # "Torus Knot by Anthony D'Agostino",
                # "Torus Knots, by Marius Giurgi (DolphinDream), testscreenings",
                # "Track with Same Color",
                # "Tracking (Aim Lock)",
                # "Tracking Extra Settings",
                # "Transform Controls",
                # "Transform Options",
                # "Transform Strip",
                # "Transformation Gizmos",
                # "Transforming Points",
                # "Translations",
                # "Transmission Depth :guilabel:`Cycles Only`",
                # "Transmission Roughness :guilabel:`Cycles Only`",
                # "Transparency Masks",
                # "Transparent Depth :guilabel:`Cycles Only`",
                # "Transparent Roughness",
                # "Transparent Shadows",
                # "Trapped Air Potential Minimum",
                # "Trapper Air Particle Sampling",
                # "Tree Scale:",
                # "Tri-Lighting",
                # "Triangles by Sjaak-de-Draak",
                # "Tricks",
                # "Trim Strokes End",
                "Twisted Torus by Paulo_Gomes",
                # "Two Adjacent Quad Edges",
                # "Two Opposite Quad Edges",
                # "Two Tri Edges",
                # "Type A, B",
                # "Type A, B, C",
                # "Type Of",
                # "Type of Radii",
                # "Types of Particle Systems",
                # "Typical Scenarios for using Soft Bodies",
                # "UDIM Tile List",
                # "UDIMs",
                # "UV",
                # "UV Offsets",
                # "UV Warp Modifier",
                # "UVs & Texture Space",
                # "UnMeta Strip :kbd:`Ctrl-Alt-G`",
                # "Unconnected Cuts",
                # "Undistorted",
                # "Undo/Redo/History",
                # "Uni Cache",
                # "Unified Selected/Active Colors",
                # "Uniform, Size",
                # "Unindent :kbd:`Shift-Tab`",
                # "Unindent :kbd:`Shift-Tab`.",
                # "Union :kbd:`Ctrl-NumpadPlus`",
            ]
        else:
            t_list = text_list

        s_time = time.perf_counter()
        tf = TranslationFinder()
        out_put_list=[]
        # remove_list=[]
        # dict_list = tf.getDict().original_data_set
        changed=False
        rm_count = 0

        # checkAndRemoveTranslated()
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
            # print(o + ',')
            print(o)

        #     is_here = tf.isInDict(t)
        #     if not is_here:
        #         o = t.replace('"', '\\"')
        #         entry=f'"{o}"'
        #         out_put_list.append(entry)
        #         dd(f'NEED WORKS: [{t}]')
        #     else:
        #         dd(f'DONE: [{t}]')
        #         rm_count += 1
        # if rm_count:
        #     dd(f'removed: [{rm_count}]')

            # without_ie_txt = t.replace('i.e. ', '')
            # is_in = (without_ie_txt in dict_list)
            # if is_in:
            #     without_ie_tran_txt = dict_list[without_ie_txt]
            #
            # if without_ie_tran_txt:
            #     k = 'i.e. ' + t
            #     v = without_ie_tran_txt + ', chẳng hạn'
            #     entry = {t: v}
            #     # remove_list.append(without_ie_txt)
            #     dd(f'UPDATE: [{entry}]')
            #     dict_list.update(entry)
            #     changed = True

            # del dict_list[without_ie_txt]
            # is_in = (without_ie_txt in dict_list)
            # if is_in:
            #     dd(f'unable to DEL:[{without_ie_txt}]')
            # else:
            #     dd(f'NEED WORKS: [{t}]')

        # if changed:
        #     home = os.environ['BLENDER_GITHUB']
        #     temp_path = os.path.join(home, 'new_dict.json')
        #     cm.writeJSONDic(dict_list=dict_list, file_name=temp_path)

        # tf.writeBackupDict()

    def run(self):
        # self.test_0001()
        # import cProfile
        # self.findRefText()
        # self.findUnknownRefs()
        self.resort_dictionary()
        self.test_translate_0001()
        # self.cleanSS()+

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
