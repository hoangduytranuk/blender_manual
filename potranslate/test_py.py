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

    def cleanDict(self):
        from observer import LocationObserver
        def isInOrig(ref_txt, source_list):
            for src_txt in source_list:
                ref_txt = ref_txt.lower()
                src_txt = src_txt.lower()
                is_same = (src_txt in ref_txt)
                if is_same:
                    return True
            return False

        def getListOfUnrefText(txt, source_list=None, is_target=False):
            output_list=[]
            ref_list = RefList(msg=txt, keep_orig=False, tf=tf)
            count = ref_list.findPattern(df.pattern_list, txt)

            obs = LocationObserver(txt)
            if not is_target:
                for loc, mm in ref_list.items():
                    obs.markLocAsUsed(loc)
            else:
                for loc, mm in RefList.items():
                    ref_txt = mm.txt
                    is_in_orig = isInOrig(ref_txt, source_list)
                    if is_in_orig:
                        obs.markLocAsUsed(loc)

            unparsed_dict = obs.getUnmarkedPartsAsDict()
            for loc, mm in unparsed_dict.items():
                txt = mm.txt
                output_list.append(txt)

            return output_list

        tf = TranslationFinder()
        home_dir = os.environ['BLENDER_GITHUB']
        sent_struct_file = os.path.join(home_dir, "ref_dict_0006_0003.json")
        ss_dict = self.loadData(sent_struct_file, is_lower=False)
        for k, v in ss_dict.items():
            en_list = getListOfUnrefText(k)
            vi_list = getListOfUnrefText(v)
            print('*' * 80)
            print(f'k: {k}')
            print(f'EN: {en_list}')
            print('-' * 40)
            print(f'v: {v}')
            print(f'VI: {vi_list}')
            print('*' * 80)

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
                # "X Axis, Y Axis, Z Axis",
                # "X Rotation, Z Rotation",
                # "X, Y, Z Axis",
                # "X, Y, Z Plane",
                # "X/Y Flip",
                # "X/Y/Z Angle",
                # "X/Y/Z Axis",
                # "X/Y/Z Min, Max",
                # "X/Y/Z Source Axis",
                # "Your API Key",
                # "Your First Armature",
                # "Your computer accidentally turns off in the middle of rendering your movie!",
                # "Z- (Down), Y-, X-, Z+ (Up), Y+, X+",
                # "Zip",
                # "Zoom :kbd:`Alt-V` :kbd:`V`",
                # "Zoom :kbd:`Ctrl-MMB`, :kbd:`Wheel`",
                # "Zoom :kbd:`Wheel`",
                # "Zoom In (plus magnifying glass icon)",
                # "Zoom In / Zoom Out",
                # "Zoom In/Out :kbd:`Wheel`",
                # "Zoom Out (minus magnifying glass icon)",
                # "\\+ Non-Grouped Keyframes",
                # "`(De)select First/Last`_",
                # "`2.66 <https://www.blender.org/download/releases/2-66>`__ -- February 2013:",
                # "`2.67 <https://www.blender.org/download/releases/2-67>`__ -- May 2013:",
                # "`2.68 <https://www.blender.org/download/releases/2-68>`__ -- July 2013:",
                # "`2.69 <https://www.blender.org/download/releases/2-69>`__ -- October 2013:",
                # "`2.70 <https://www.blender.org/download/releases/2-70>`__ -- March 2014:",
                # "`2.71 <https://www.blender.org/download/releases/2-71>`__ -- June 2014:",
                # "`2.72 <https://www.blender.org/download/releases/2-72>`__ -- October 2014:",
                # "`2.73 <https://www.blender.org/download/releases/2-73/>`__ -- January 2015:",
                # "`2.74 <https://www.blender.org/download/releases/2-74/>`__ -- March 2015:",
                # "`2.75 <https://www.blender.org/download/releases/2-75/>`__ -- July 2015:",
                # "`2.76 <https://www.blender.org/download/releases/2-76/>`__ -- November 2015:",
                # "`2.77 <https://www.blender.org/download/releases/2-77/>`__ -- March 2016:",
                # "`2.78 <https://www.blender.org/download/releases/2-78/>`__ -- September 2016:",
                # "`2.79 <https://www.blender.org/download/releases/2-79/>`__ -- September 2017:",
                # "`2.80 <https://www.blender.org/download/releases/2-80>`__ -- July 2019:",
                # "`2.81 <https://www.blender.org/download/releases/2-81/>`__ -- November 2019:",
                # "`2.82 <https://www.blender.org/download/releases/2-82/>`__ -- February 2020:",
                # "`2.83 <https://www.blender.org/download/releases/2-83/>`__ -- June 2020:",
                # "`2.90 <https://www.blender.org/download/releases/2-90/>`__ -- August 2020:",
                # "`2.91 <https://www.blender.org/download/releases/2-91/>`__ -- November 2020:",
                # "`2.92 <https://www.blender.org/download/releases/2-92/>`__ -- February 2021:",
                # "`2.93 <https://www.blender.org/download/releases/2-93/>`__ -- June 2021:",
                # "`Cessen's Rigify Extensions <https://github.com/cessen/cessen_rigify_ext>`__",
                # "`Daily Builds <https://builder.blender.org/download>`__",
                # "`Developer Community <https://devtalk.blender.org>`__",
                "`Docutils reStructuredText Reference <https://docutils.sourceforge.io/rst.html>`__",
                # "`Edge Loops`_",
                # "`Edge Ring`_",
                # "`Experimental Rigs by Alexander Gavrilov <https://github.com/angavrilov/angavrilov-rigs>`__",
                # "`Face Loops`_",
                # "`Long-term Support <https://www.blender.org/download/lts/>`__",
                # "`Python API Reference <https://docs.blender.org/api/current/>`__",
                # "`QT rle / QT Animation <https://en.wikipedia.org/wiki/QuickTime_Animation>`__",
                # "`Report a Bug <https://developer.blender.org/maniphest/task/edit/form/1/>`__",
                # "`Select All by Trait`_",
                # "`Select Control Point Row`_",
                # "`Select Next/Previous`_",
                # "`Shortest Path`_",
                # "`Sphinx RST Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__",
                # "`Stable Release <https://www.blender.org/download/>`__",
                # "`Support <https://www.blender.org/support>`__",
                # "`Tutorials <https://www.blender.org/support/tutorials>`__",
                # "`User Communities <https://www.blender.org/community/>`__",
                # "``+C``: Continue an interrupted render",
                # "``+WT``: Limit the number of threads used",
                # "``-D``: Hide image while rendering",
                # "``/EXIT``: Close POV-Ray after rendering the image",
                # "``bpy.context.object`` or ``bpy.context.active_object``",
                # "``bpy.context.selected_objects``",
                # "``color_picking``",
                # "``faces.super_face``",
                # "``file.blend``",
                # "``found bundled python: {DIR}``",
                # "``id`` (integer)",
                # "``injected`` (special)",
                # "``normal`` (vector)",
                # "``rotation`` (vector)",
                # "``scene_linear``",
                # "glTF 2.0",
                # "macOS -- Other GPU",
                # "sRGB",
                # "tap",
                # "tinyCAD Mesh Tools",
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
        # self.cleanDict()
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
