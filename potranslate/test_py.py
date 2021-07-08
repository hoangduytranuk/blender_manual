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
                # "\"Bone size\" scaling example.",
                # "\"Focus Pull\"",
                # "(De)select All :kbd:`A`",
                # "*Curve Map* variations.",
                # "*nn* - Theme Color Set",
                # "-X/-Y/-Z/X/Y/Z Rotation",
                # "16-bit Half Float",
                # "1D",
                # "2D",
                # "2D Curve Boolean",
                # "2D Full Canvas",
                # "2D Traditional Animation",
                # "2D Vector",
                # "3D",
                # "3D Function Surface by Buerbaum Martin (Pontiac), Elod Csirmaz",
                # "3D Print Toolbox",
                "3D Rigs (Dolly & Crane)",
                # "3D Viewport Header Widget",
                # "3D Viewport Hotkeys",
                # "3D Viewport Keys",
                # "3D Viewport Pie Menus",
                # "3D graphics",
                # "3D-Coat Applink",
                # "4D",
                # ":abbr:`BSDF (Bidirectional Scattering Distribution Function)` shader",
                # ":abbr:`DLS (Damped Least Square)`",
                # ":abbr:`IES (Illuminating Engineering Society)` Texture",
                # ":abbr:`SDLS (Selective Damped Least Square)`",
                # ":doc:`Armature </animation/armatures/index>`",
                # ":doc:`Collection Instance </scene_layout/object/properties/instancing/collection>`",
                # ":doc:`Curve </modeling/curves/introduction>`",
                # ":doc:`Empty </modeling/empties>`",
                # ":doc:`Extrude Along Normals </modeling/meshes/editing/face/extrude_faces_normal>`",
                # ":doc:`Extrude Manifold </modeling/meshes/tools/extrude_manifold>`",
                # ":doc:`Force Field </physics/forces/force_fields/index>`",
                # ":doc:`Glossary </glossary/index>`",
                # ":doc:`Grab </modeling/meshes/uv/tools/grab>`",
                # ":doc:`Grab </modeling/meshes/uv/uv_sculpt>`",
                # ":doc:`Grease Pencil </grease_pencil/primitives>`",
                # ":doc:`Light </render/lights/light_object>`",
                # ":doc:`Light Probe </render/eevee/light_probes/introduction>`",
                # ":doc:`Manual </index>`",
                # ":doc:`Mesh </modeling/meshes/introduction>`",
                # ":doc:`Metaball </modeling/metas/introduction>`",
                # ":doc:`Move </scene_layout/object/editing/transform/move>` :kbd:`G`",
                # ":doc:`Pinch </modeling/meshes/uv/tools/pinch>`",
                # ":doc:`Pinch </modeling/meshes/uv/uv_sculpt>`",
                # ":doc:`Push/Pull </modeling/meshes/editing/mesh/transform/push_pull>`",
                # ":doc:`Relax </modeling/meshes/uv/tools/relax>`",
                # ":doc:`Relax </modeling/meshes/uv/uv_sculpt>`",
                # ":doc:`Rip </modeling/meshes/uv/tools/rip>`",
                # ":doc:`Rotate </scene_layout/object/editing/transform/rotate>` :kbd:`R`",
                # ":doc:`Scale </scene_layout/object/editing/transform/scale>` :kbd:`S`",
                # ":doc:`Select All by Trait </modeling/meshes/selecting/all_by_trait>`",
                # ":doc:`Shear </modeling/meshes/editing/mesh/transform/shear>` :kbd:`Shift-Ctrl-Alt-S`",
                # ":doc:`Speaker </render/output/audio/speaker>`",
                # ":doc:`Surface </modeling/surfaces/introduction>`",
                # ":doc:`Text </modeling/texts/introduction>`",
                # ":doc:`To Sphere </modeling/meshes/editing/mesh/transform/to_sphere>` :kbd:`Shift-Alt-S`",
                # ":doc:`Volume </modeling/volumes/introduction>`",
                # ":kbd:`AccentGrave`",
                # ":kbd:`G`",
                # ":kbd:`LMB`",
                # ":kbd:`MMB`",
                # ":kbd:`Numpad0` to :kbd:`Numpad9`, :kbd:`NumpadPlus`",
                # ":kbd:`OSKey`",
                # ":kbd:`OSKey` (also known as the ``Windows-Key``, ``Cmd`` or ``Super``)",
                # ":kbd:`RMB`",
                # ":kbd:`Shift`, :kbd:`Ctrl`, :kbd:`Alt`",
                # ":kbd:`Wheel`",
                # ":ref:`Add Cone <tool-add-cone>`",
                # ":ref:`Add Cube <tool-add-cube>`",
                # ":ref:`Add Cylinder <tool-add-cylinder>`",
                # ":ref:`Add Ico Sphere <tool-add-icosphere>`",
                # ":ref:`Add UV Sphere <tool-add-cylinder>`",
                # ":ref:`Annotate <tool-annotate>`",
                # ":ref:`Arc <tool-grease-pencil-draw-arc>`",
                # ":ref:`Armatures <armatures-index>`",
                # ":ref:`Bevel <tool-mesh-bevel>`",
                # ":ref:`Bisect <tool-mesh-bisect>`",
                # ":ref:`Blade <tool-blade>`",
                # ":ref:`Box <tool-grease-pencil-draw-box>`",
                # ":ref:`Box Select <tool-select-box>` :kbd:`B`",
                # ":ref:`Checker Deselect <bpy.ops.mesh.select_nth>`",
                # ":ref:`Checker Deselect <modeling-selecting-checker_deselect>`",
                # ":ref:`Circle <tool-grease-pencil-draw-circle>`",
                # ":ref:`Circle Select <tool-select-circle>` :kbd:`C`",
                # ":ref:`Constraints <constraints-index>`",
                # ":ref:`Curve <tool-grease-pencil-draw-curve>`",
                # ":ref:`Cutter <tool-grease-pencil-draw-cutter>`",
                # ":ref:`Draw <bpy.ops.curve.draw>`",
                # ":ref:`Draw <tool-grease-pencil-draw-draw>`",
                # ":ref:`Drivers <animation-drivers-index>`",
                # ":ref:`Edge Loops <bpy.ops.mesh.loop_multi_select>`",
                # ":ref:`Edge Rings <modeling-meshes-selecting-edge-rings>`",
                # ":ref:`Edge Slide <tool-mesh-edge_slide>`",
                # ":ref:`Erase <tool-grease-pencil-draw-erase>`",
                # ":ref:`Extrude <modeling-curves-extrude>`",
                # ":ref:`Extrude Individual <tool-mesh-extrude_individual>`",
                # ":ref:`Extrude Region <tool-mesh-extrude_region>`",
                # ":ref:`Extrude To Cursor <tool-mesh-extrude_cursor>`",
                # ":ref:`Eyedropper <tool-grease-pencil-draw-eyedropper>`",
                # ":ref:`Face Loops <modeling-meshes-selecting-face-loops>`",
                # ":ref:`Fill <tool-grease-pencil-draw-fill>`",
                # ":ref:`Image <bpy.types.Object.empty_image>`",
                # ":ref:`Inset Faces <tool-mesh-inset_faces>`",
                # ":ref:`Interpolate <tool-grease-pencil-draw-interpolate>` :kbd:`Ctrl-E`",
                # ":ref:`Knife <tool-mesh-knife>`",
                # ":ref:`Line <tool-grease-pencil-draw-line>`",
                # ":ref:`Loop Cut <tool-mesh-loop_cut>`",
                # ":ref:`Manual Index <genindex>`",
                # ":ref:`Measure <tool-measure>`",
                # ":ref:`Object Modifiers <modifiers-index>`",
                # ":ref:`Offset Edge Loop Cut <bpy.ops.mesh.offset_edge_loops_slide>`",
                # ":ref:`Poly Build <tool-mesh-poly-build>`",
                # ":ref:`Polyline <tool-grease-pencil-draw-polyline>`",
                # ":ref:`Push/Pull <tool-transform-push_pull>`",
                # ":ref:`Radius <modeling-curve-radius>`",
                # ":ref:`Randomize <tool-mesh-smooth>`",
                # ":ref:`Rip Edge <tool-mesh-rip_edge>`",
                # ":ref:`Rip Region <tool-mesh-rip_region>`",
                # ":ref:`Roll <tool-bone-role>`",
                # ":ref:`Scale Cage <tool-scale-cage>`",
                # ":ref:`Select <tool-select-tweak>`",
                # ":ref:`Select Box <tool-select-box>`",
                # ":ref:`Select Circle <tool-select-circle>`",
                # ":ref:`Select Lasso <tool-select-lasso>`",
                # ":ref:`Select Linked <bpy.ops.mesh.select_linked>`",
                # ":ref:`Select Random <bpy.ops.mesh.select_random>`",
                # ":ref:`Select Similar <bpy.ops.mesh.select_similar>` :kbd:`Shift-G`",
                # ":ref:`Shape Keys <animation-shape_keys-index>`",
                # ":ref:`Shear <tool-transform-shear>`",
                # ":ref:`Shortest Path <bpy.ops.mesh.shortest_path_select>`",
                # ":ref:`Shrink/Flatten <tool-mesh-shrink-fatten>`",
                # ":ref:`Smooth <tool-mesh-smooth>`",
                # ":ref:`Spin <tool-mesh-spin>`",
                # ":ref:`Spin Duplicate <tool-mesh-spin>`",
                # ":ref:`Tilt <modeling-curve-tilt>`",
                # ":ref:`Tint <tool-grease-pencil-draw-tint>`",
                # ":ref:`To Sphere <tool-transform-to_sphere>`",
                # ":ref:`Tweak <tool-select-tweak>`",
                # ":ref:`Vertex Slide <tool-mesh-vertex-slide>`",
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
        # self.cleanSS()

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
