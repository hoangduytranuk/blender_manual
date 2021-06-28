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

        if not text_list:
            t_list = [
                "i.e. a set of close keyframes with linear interpolation",
                # "i.e. a set of detected feature edges",
                # "i.e. above/below the curve",
                # "i.e. all *Generate*, some *Modify* and some *Simulate* modifiers cannot come before the *Multiresolution* one",
                # "i.e. all F-curves for a bone, instead of per F-curve",
                # "i.e. also behaving like polylines",
                # "i.e. angle between faces forming that edge",
                # "i.e. animate",
                # "i.e. as if both object's origins were at the same place",
                # "i.e. as it was transformed in the *Pose Mode*",
                # "i.e. behaving like polylines",
                # "i.e. between the two light gray lines",
                # "i.e. blend-files when loading a complete Blender setting",
                # "i.e. bones deform points in their neighborhood",
                # "i.e. bones deform vertices in their neighborhood",
                # "i.e. changes occur slowly at the beginning and at the end",
                # "i.e. current frame",
                # "i.e. do not turn on *Dynamic*",
                # "i.e. do not turn on Dynamic",
                # "i.e. edges between two selected faces",
                # "i.e. fire or smoke or both",
                # "i.e. first child and parent",
                # "i.e. foam",
                # "i.e. following the selected feature from frame to frame",
                # "i.e. from more complex to simpler",
                # "i.e. from simpler to more complex",
                # "i.e. grids and particles",
                # "i.e. hiding/unhiding in one mode affects the other mode too",
                # "i.e. how many times the process is repeated",
                # "i.e. identical in all directions",
                # "i.e. if you had a ``forearm`` bone selected when you copied the pose, the ``forearm`` bone of the current posed armature will get its pose when you paste it -- and if there is no such named bone, nothing will happen...",
                # "i.e. if you make a parallelepiped out of a cube by modifying its dimensions in *Object Mode*, you will still have a cube-shaped bone...",
                # "i.e. if you set *Start* to 1, you will really see the frame 1 as starting point of the paths...",
                # "i.e. ignoring existing overrides on data-blocks properties",
                # "i.e. including all scenes",
                # "i.e. independently from the armature transformations in *Object Mode*",
                # "i.e. invert negative ones",
                # "i.e. it cannot be edited anymore from the Action/Graph Editors, unless you enter \"Tweak Mode\" on the corresponding strips later",
                # "i.e. it is as if the other metas were \"included\" or joined into the base one",
                # "i.e. it is bilaterally symmetrical",
                # "i.e. it is expected to give reproducible results across several import/export cycles",
                # "i.e. it just snaps to the B-value like an extreme exponential transition",
                # "i.e. it will bake all steps that can be baked individually with the :ref:`Modular <bpy.types.FluidDomainSettings.cache_type>` cache type at once",
                # "i.e. it will be \"played\" reversed...",
                # "i.e. its default pivot point, when it is the only selected one",
                # "i.e. less long thin triangles",
                # "i.e. let the object give the particle a starting speed",
                # "i.e. let the surface normal give the particle a starting speed",
                # "i.e. link and override overrides from another library file, etc.",
                # "i.e. location, rotation or scale",
                # "i.e. making action cyclic",
                # "i.e. mesh, particles, noise",
                # "i.e. modifier has no effect",
                # "i.e. move objects or deform geometry",
                # "i.e. multiple F-curves of the same type",
                # "i.e. normal bone posing",
                # "i.e. normal maps",
                # "i.e. object data-blocks",
                # "i.e. one object",
                # "i.e. one or two...",
                # "i.e. only the paths of keyed bones at a given frame get a yellow dot at this frame",
                # "i.e. parallel to Z",
                # "i.e. parent relationships",
                # "i.e. parent's",
                # "i.e. particles whose keypoints are hidden",
                # "i.e. perpendicular to the original curve plane",
                # "i.e. reverses the weight values of this group",
                # "i.e. right-angled triangles sharing their hypotenuses",
                # "i.e. sentences can have their own lines",
                # "i.e. set rotation to dynamic/constant",
                # "i.e. shape keys and modifiers",
                # "i.e. shorter strokes finish earlier",
                # "i.e. shorter strokes start later",
                # "i.e. straight down a camera or light",
                # "i.e. tangent to the curve at the owner's position",
                # "i.e. that is, have no active action, drivers, and NLA tracks or strips",
                # "i.e. the Rest Pose/Base Rig",
                # "i.e. the UV map",
                # "i.e. the adjacent points will be directly linked, joined, once the intermediary ones are deleted",
                # "i.e. the adjacent rows will be directly linked, joined, once the intermediary ones are deleted",
                # "i.e. the bone will be of the color of the bottommost valid state",
                # "i.e. the chain's transformations above the bone",
                # "i.e. the control points following or preceding the selected ones along the curve",
                # "i.e. the current reference only",
                # "i.e. the direction perpendicular to the tangent line",
                # "i.e. the distance before this constraint is applied",
                # "i.e. the global stamp switch setting",
                # "i.e. the mesh is this times bigger than the base simulation",
                # "i.e. the modification of one bone does not affect the others",
                # "i.e. the owner just gets the properties defined at frame 0 of the linked action...",
                # "i.e. the particle simulation is this times bigger than the base simulation",
                # "i.e. the rotation around the Y axis of the bone",
                # "i.e. the selection *must* define a valid loop, see below",
                # "i.e. the start point will become the end one, and *vice versa*",
                # "i.e. the start point will become the end one, and vice versa",
                # "i.e. the unconnected edges of a mesh",
                # "i.e. the vertex is kept at its original position",
                # "i.e. the world surface shader defined for the scene",
                # "i.e. their root will become their tip, and vice versa",
                # "i.e. they keep a constant rotation relatively to their parent",
                # "i.e. they will move proportionally relative to the location of the selected element",
                # "i.e. they will never \"go outside\" of a stroke or \"jump\" to another stroke in the same object",
                # "i.e. this avoids having the second *Armature* modifier deform the result of the first one...",
                # "i.e. time between strokes drawing",
                # "i.e. to \"paint\" them",
                # "i.e. to a specific object, or to a specific material/light/etc.",
                # "i.e. transforming a parent bone will not affect its children",
                # "i.e. two, three or four",
                # "i.e. unlink the underlying F-curve data-block from this action data-block",
                # "i.e. unlinked to the result of the spin extrusion",
                # "i.e. using the *Keep Offset* option while parenting",
                # "i.e. video games!",
                # "i.e. when it is enabled, the \"positive\" side will be kept, instead of the \"negative\" one",
                # "i.e. when some linked-in objects may have previously been used to develop a set of reusable assets",
                # "i.e. will be applied last",
                # "i.e. with non-uniform scaling",
                # "i.e. with suffixes like \".R\", \".right\", \".L\", etc.",
                # "i.e. without a Display Manager",
                # "i.e. you can't use it e.g. to animate the colors of a material in the Properties...",
                # "i.e. you cannot delete both U and V rows at the same time",
                # "i.e. you copy only selected bones' pose",
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
