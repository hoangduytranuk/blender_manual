#!/usr/bin/python3
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
from common import Common as cm
from utils import dd, pp
from matcher import MatcherRecord
from definition import Definitions as df, RefType, TranslationState
from reflist import RefList
import inspect as INP
import copy as CP
import cProfile, pstats, io
from ignore import Ignore as ig
from string_utils import StringUtils as st
from pattern_utils import PatternUtils as pu

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
                word_list = pu.findInvert(df.MENU_SEP, txt, is_reversed=True)
                for loc, mnu_item_mm in word_list.items():
                    sub_txt: str = mnu_item_mm.txt
                    left, mid, right = st.getTextWithin(sub_txt)
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
            part_match_dict = pu.patternMatchAll(pat, txt)
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

    # /Users/hoangduytran/Dev/tran/blender_manual/ref_dict_backup_0005_0001_working.json
    def translate_backup_dict_using_google(self):
        from googletrans import Translator
        from paragraph import Paragraph as PR

        home_dir = os.environ['BLENDER_GITHUB']
        sent_struct_file = os.path.join(home_dir, "ref_dict_backup_0005_0002_working.json")
        ignore_file = os.path.join(home_dir, "ref_dict_backup_0005_0001_ignore.json")
        ss_dict = self.loadData(sent_struct_file, is_lower=False)
        output_list = []
        output_dict = {}
        ignore_dict = {}
        # dictionary = tf.getDict()
        ts = Translator()
        i = 0
        last = 5
        for k, v in ss_dict.items():
            v = ts.translate(k, dest='vi', src='en')            
            entry = {k: v.text}
            output_dict.update(entry)
            # i += 1
            # if (i > last):
            #     break

        if output_dict:
            out_file = os.path.join(home_dir, "ref_dict_backup_0005_0005_working.json")
            writeJSON(out_file, output_dict)

    def translate_backup_dict(self):
        from paragraph import Paragraph as PR

        tf = TranslationFinder()
        home_dir = os.environ['BLENDER_GITHUB']
        sent_struct_file = os.path.join(home_dir, "ref_dict_backup_0005_0002_working.json")
        ignore_file = os.path.join(home_dir, "ref_dict_backup_0005_0001_ignore.json")
        ss_dict = self.loadData(sent_struct_file, is_lower=False)
        output_list = []
        output_dict = {}
        ignore_dict = {}
        dictionary = tf.getDict()
        for k, v in ss_dict.items():
            # tran = tf.isInDict(k)
            # if not tran:
            #     entry = {k: v}
            #     output_dict.update(entry)
            last_char = k[-1]
            has_dot = (last_char == '.')
            if has_dot:
                k = k[:-1]

            is_ignored = ig.isIgnored(k)
            tran = dictionary.get(k)
            is_in_dict = (tran is not None)
            can_ignore = (is_ignored or is_in_dict)
            if can_ignore:
                entry = {k: v}
                ignore_dict.update(entry)
                continue


            # pr = PR(k, translation_engine=tf)
            # pr.translateAsIs()
            # tran = pr.tl_txt
            # if not tran:
            #     tran = ''

            entry = {k: v}
            output_dict.update(entry)

            # # pr.translateSplitUp()
            # output = pr.getTextAndTranslation()
            # output_list.append(output)

        # for entry in output_list:
        #     print(entry)

        if ignore_dict:
            writeJSON(ignore_file, ignore_dict)

        if output_dict:
            out_file = os.path.join(home_dir, "ref_dict_backup_0005_0004_working.json")
            writeJSON(out_file, output_dict)

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
                # "Disables selection for the collection in all view layers -- affects 3D Viewport -- chaining.",
                # "Disables the collection in all view layers -- affects 3D Viewport -- chaining.",
                # "File:Manual-2.6-Render-Freestyle-PrincetownLinestyle.pdf",
                # "Move this vertex using the shortcut :kbd:`G X Minus 1` and :kbd:`Return`. See Fig. :ref:`fig-mesh-screw-spindle`.",
                # "Mickael Lozac'h et al. -- `Link to publication <https://doi.org/10.1002/ese3.174>`__",
                "``anim_time_max`` -- Maximum number of seconds to show the animation for (in case the end frame is very high for no reason)."
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

    def merge_po(self, from_po, to_po, out_po=None):
        def make_key(msg):
            k = m.id
            k_ctx = m.context
            return (k, k_ctx)

        def make_value(msg):
            v1 = msg.string
            v2 = msg
            return (v1, v2)

        def po_to_dict(po_msg_list):
            new_dict = {}
            for m in po_msg_list:
                key = make_key(m)
                value = make_value(m)
                entry = {key: value}
                new_dict.update(entry)
            return new_dict

        def find_msg(msg_to_find, po_msg_list_to_find_in):
            find_key = make_key(msg_to_find)
            for m in po_msg_list_to_find_in:
                current_key = make_key(m)
                is_found = (current_key == find_key)
                if not is_found:
                    continue

                
            return None
        try:
            # to_po is normally the file with latest changes
            # from_po is normally the file from SVN, with untranslated, but latest strings
            from_po_msg = c.load_po(from_po)
            to_po_msg = c.load_po(to_po)

            for m in from_po_msg:
                from_msgid = m.id

        except Exception as e:
            out_po_txt = (out_po if out_po else "")
            df.LOG(f'ERROR: {e}; from_po:{from_po}, to_po:{to_po}, out_po:{out_po_txt}')

    def test_code_0001(self):
        from gettext_within import GetTextWithin as gt
        t = [
            '(this one text) and this is another (here).',
            '(this one and that one).'
        ]

        for txt in t:
            left, mid, right = gt.getTextWithin(txt)
            print(f'left:{left}')
            print(f'mid:{mid}')
            print(f'right:{right}')
            print('-' * 80)

    def test_brk_pat(self):
        from enum import Enum
        class RefRecStatus(Enum):
            UNKOWN = 0
            REMOVE_LEFT = 1
            REMOVE_RIGHT = 2
            REMOVE_BOTH = 3
            REMOVE = 4
            IGNORE = 5

        def getNoneAlphaPart(msg, is_start=True):
            if not msg:
                return ""

            non_alnum_part = ""
            if is_start:
                non_alpha = df.START_WORD_SYMBOLS.search(msg)
            else:
                non_alpha = df.END_WORD_SYMBOLS.search(msg)

            if non_alpha:
                non_alnum_part = non_alpha.group(0)
            return non_alnum_part

        def getTextWithinWithDiffLoc(msg, to_matcher_record=False):
            # should really taking bracket pairs into account () '' ** "" [] <> etc.. before capture
            left_part = getNoneAlphaPart(msg, is_start=True)
            right_part = getNoneAlphaPart(msg, is_start=False)

            ss = len(left_part)
            ee = (-len(right_part) if right_part else len(msg))
            mid_part = msg[ss:ee]
            length_ee = len(right_part)
            diff_loc = (ss, length_ee)

            main_record: MatcherRecord = None
            if to_matcher_record:
                ls = 0
                le = ss
                ms = le
                me = ms + len(mid_part)
                rs = me
                re = rs + len(right_part)

                main_record = MatcherRecord(s=0, e=len(msg), txt=msg)
                if left_part:
                    main_record.addSubMatch(ls, le, left_part)
                    test_txt = left_part[ls: le]
                else:
                    main_record.addSubMatch(-1, -1, None)
                if mid_part:
                    main_record.addSubMatch(ms, me, mid_part)
                    test_txt = left_part[ms: me]
                else:
                    main_record.addSubMatch(ls, re, msg)
                if right_part:
                    main_record.addSubMatch(rs, re, right_part)
                    test_txt = left_part[rs: re]
                else:
                    main_record.addSubMatch(-1, -1, None)

            return diff_loc, left_part, mid_part, right_part, main_record

        def findTextWithin(msg):
            diff_loc, left_part, mid_part, right_part, main_record = getTextWithinWithDiffLoc(msg)
            return left_part, mid_part, right_part

        def find_brackets(msg: str):
            found_dict = pu.patternMatchAll(all_punct_pattern, msg)
            return found_dict

        def getRefRecStatus(ref_rec: MatcherRecord, orig_msg: str, is_first=True) -> RefRecStatus:
            try:
                ref_type = ref_rec.type
                is_text = (ref_type == RefType.TEXT) or (ref_type == RefType.ARCH_BRACKET)
                # is_ref = (not is_text)

                ref_main_txt = ref_rec.txt
                is_all_non_alpha = non_alpha_only_pattern.search(ref_main_txt)
                s = ref_rec.s
                e = ref_rec.e
                if is_all_non_alpha:
                    return RefRecStatus.REMOVE, (s, e)
                if is_text:
                    state = RefRecStatus.UNKOWN
                    left, mid, right = findTextWithin(ref_main_txt)
                    has_left = bool(left)
                    has_right = bool(right)
                    has_mid = bool(mid) and (non_alpha_only_pattern.search(mid) is None)

                    if has_left and not has_right:
                        is_s_start = (s == 0)
                        if is_s_start:
                            state = RefRecStatus.REMOVE_LEFT
                            s += len(left)
                        else:
                            state = RefRecStatus.IGNORE
                    elif has_left and has_right:
                        if has_mid:
                            state = RefRecStatus.REMOVE_BOTH
                            s += len(left)
                            e -= len(right)
                        else:
                            state = RefRecStatus.REMOVE
                    elif not has_left and has_right:
                        e -= len(right)
                        state = RefRecStatus.REMOVE_RIGHT
                    # not (has_left or has_right)
                else: # is_ref
                    max_length = len(orig_msg)

                return state, (s, e)
            except Exception as e:
                df.LOG(f'{e}: {ref_rec}')
            
        def parseRefList(ref_list: RefList, orig_msg: str):
            try:
                list_len = len(ref_list)
                (first_ref_loc, first_ref_rec) = ref_list[0]
                (last_ref_loc, last_ref_rec) = ref_list[list_len-1]

                is_one_line = (first_ref_loc == last_ref_loc)

                print(f'FIRST: {first_ref_rec}')
                print(f'LAST: {last_ref_rec}')
                first_state, first_loc = getRefRecStatus(first_ref_rec, orig_msg, is_first=True)
                last_state, last_loc = getRefRecStatus(last_ref_rec, orig_msg, is_first=False)

            except Exception as e:
                df.LOG(f'{e}: {ref_list}')

        # get list of brackets in the text line, with location, state = UNKOWN
        # mask off pairs that are (CONSUME)
        #   - (SLINE)(BRK) .. (BRK)(space) (exlcude space)
        #   - (space)(BRK) .. (BRK)(space) (exlcude space)
        #   - (space)(BRK) .. (BRK)(ELINE) (exlcude space)
        #
        # remove if pairs are (REMOVE)
        #   - (SLINE)(BRK) .. (BRK)(ELINE)
        #   - (SLINE|NON-ALPHA+)(BRK) .. (BRK)(ELINE)
        #   - (SLINE)(BRK) .. (BRK)(NON-ALPHA+|ELINE)
        #   - (SLINE, NON-ALPHA+)(ALPHA) (exclude the alpha)
        #   - (ALPHA)(NON-ALPHA+, ELINE) (exclude the alpha)

        punctuation_txt = r'\.\,\!\:'
        brk_same_set_txt = r'\:\`§"\'\*'
        brk_open_set_txt = r'\[\(\<\{'
        brk_close_set_txt = r'\]\)\>\}'
        alpha_only_txt = r'[^%s%s%s%s]' % (brk_open_set_txt, brk_close_set_txt, brk_same_set_txt, punctuation_txt)
        non_alpha_txt = r'[%s%s%s%s]' % (brk_open_set_txt, brk_close_set_txt, brk_same_set_txt, punctuation_txt)
        non_alpha_only_txt = r'^%s$' % (non_alpha_txt)

        brk_full_set = r'%s%s%s' % (brk_same_set_txt, brk_open_set_txt, brk_close_set_txt)
        begin_or_space_txt = r'(^|\s)'
        end_or_space_txt = r'(\s|$)'
        begin_or_space_followed_by_brk_txt = r'%s[%s%s]+' % (begin_or_space_txt, brk_open_set_txt, brk_same_set_txt)
        end_or_space_preceded_by_brk_txt = r'[%s%s]+%s' % (brk_close_set_txt, brk_same_set_txt, end_or_space_txt)

        pat_txt = r'[%s%s%s%s]' % (brk_open_set_txt, brk_close_set_txt, brk_same_set_txt, punctuation_txt)
        all_punct_pattern = re.compile(pat_txt)

        unpackable_txt = r'[%s%s]' % (punctuation_txt, brk_same_set_txt)
        unpackable_txt_only = r'^%s$' % (unpackable_txt)

        punctuation_pat_txt = r'[%s]' % (punctuation_txt)
        punctuation_only_txt = r'^%s$' % (punctuation_pat_txt)

        unpackable_pattern = re.compile(unpackable_txt)
        punctuation_only_pattern = re.compile(punctuation_only_txt)
        non_alpha_only_pattern = re.compile(non_alpha_only_txt)

        look_ahead_space_leading = r'(?\s)'
        look_ahead_space_trailing = r'(?<\s)'

        consume_1_txt = r'%s[%s](%s)+[%s]' % (begin_or_space_txt, brk_open_set_txt, alpha_only_txt, brk_close_set_txt)

        varifying_brk_pattern_txt = r'[%s]+' % (brk_full_set)
        varifying_brk_pattern = re.compile(varifying_brk_pattern_txt)

        test_list = [
            '(Inside bracket) and (another set).',
            "**1.00 -- January 1994:** Blender `in development <https://code.blender.org/2013/12/how-blender-started-twenty-years-ago/>`__ at animation studio NeoGeo.",
            '(this is one bracket line).',
            # 'No brackets at all line.',
            "\"You have to select a string of connected vertices too\".",
            "\"Enabling previews adds 65536 bytes to the size of each blend-file (unless it is compressed).\"",
        ]

        # find_all = df.AST_QUOTE.findall(test_txt)
        # print(find_all)

        for t in test_list:
            ref_dict = RefList(t)
            ref_dict.parseMessage(is_ref_only=False, include_brackets=True)
            ref_list = list(ref_dict.items())
            ref_list.sort()
            parseRefList(ref_list, t)

        # brk_dict = find_brackets(test_txt)
        # print(brk_dict)

    def cleanKritaPOFile(self):
        po_path = os.environ['KRITA_PO_FILE']
        home_dir = os.environ['HOME']
        out_file = os.path.join(home_dir, 'temp_krita.po')

        po_data = c.load_po(po_path)
        changed = False
        for m in po_data:
            is_fuzzy = m.fuzzy
            if is_fuzzy:
                print(type(m.flags))
                m.string = ""
                changed = True
                m.flags.remove('fuzzy')
            print(f'msgid: {m.id}')
            print(f'msgstr: {m.string}')

        if changed:
            c.dump_po(out_file, po_data)

    def correct_snippet_seq(self):
        import plistlib as PL
        import xml.etree.ElementTree as ET

        home_dir = os.environ['HOME']
        atom_home_dir = os.path.join(home_dir, '.atom')

        in_plist_file = os.path.join(atom_home_dir, 'Text Substitutions 2.plist')
        try:
            v1 = v2 = 0
            v1_max = 9999
            v2_max = 9999
            dict_list = {}
            et_file = ET.parse(in_plist_file)
            plist_root = et_file.getroot()
            for array_tag in plist_root.findall('array'):
                for dict_elem in array_tag.findall('dict'):
                    keys = dict_elem.findall('key')
                    strings = dict_elem.findall('string')
                    phrase = strings[0].text
                    short_cut = strings[1].text
                    print(f'[{short_cut}] => [{phrase}]')
                    dict_key = f'{v1:03}_{v2:04}'
                    v1 += 1
                    if v1 > v1_max:
                        v1 = 0
                        v2 += 1
                        if v2 > v2_max:
                            v2 = 0
                    dict_value = (short_cut, phrase)
                    dict_entry = {dict_key: dict_value}
                    dict_list.update(dict_entry)
                    print(dict_entry)

            tab_one = ' '
            tab_two = (tab_one * 2)
            tab_three = (tab_one * 3)

            out_file = os.path.join(home_dir, 'temp_snippets.cson')
            with open(out_file, 'w') as outf:
                for k, v in dict_list.items():
                    prefix_txt, body_txt = v
                    item_key = f"{tab_one}'{k}':"
                    prefix = f"{tab_two}'prefix': '{prefix_txt}:'"
                    body = f"{tab_two}'body': '{body_txt} $1'"
                    line = f'{item_key}\n{prefix}\n{body}\n'
                    outf.write(line)

            print('Finished')
        except Exception as e:
            print(f'Exception: {e}')

        # infile = os.path.join(home_dir, '.atom/snippets.cson')
        # out_file = os.path.join(home_dir, 'temp_snippets.cson')
        # old_lines=[]
        # with open(infile, 'r') as inf:
        #     l = inf.readlines()
        # old_lines = list(l)
        #
        # v1 = 0
        # v1_max = 999
        # v2 = 0
        # v2_max = 9999
        # body_pat_txt = r"'body':"
        # prefix_pat_txt = r"'prefix':"
        # section_pat_txt = r'\d{3}_\d{4}'
        # pat = re.compile(find_pattern, flags=re.I)
        #
        # new_lines=[]
        # for l in old_lines:
        #     is_found = (pat.search(l) is not None)
        #     if not is_found:
        #         new_lines.append(l)
        #         print(f'unfound: {l}')
        #     else:
        #         v1 += 1
        #         if v1 > v1_max:
        #             v1 = 0
        #             v2 += 1
        #             if v2 > v2_max:
        #                 v2 = 0
        #
        #         new_v = f'{v1:03}_{v2:04}'
        #         # print(f'new_v: {new_v}')
        #         new_l = pat.sub(new_v, l)
        #         # print(f'new_l: {new_l}')
        #         new_lines.append(new_l)
        #         # print(f'new_lines:{new_lines}')
        #         # exit(0)
        # # print(new_lines)
        # with open(out_file, 'w') as outf:
        #     outf.writelines(new_lines)

    def printEmptyPOLines(self):
        # po_path = os.environ['KRITA_PO_FILE']
        home_dir = os.environ['HOME']
        po_path = os.path.join(home_dir, 'temp_krita.po')
        
        msg_data = c.load_po(po_path)

        for index, m in enumerate(msg_data):
            is_translated = bool(m.string)
            if is_translated:
                continue

            msgid = m.id
            msg = f'{index + 1}: [{msgid}]'
            print(msg)

    def run(self):
        # self.cleanDict()
        # self.test_0001()
        # import cProfile
        # self.findRefText()
        # self.findUnknownRefs()
        self.resort_dictionary()
        self.test_translate_0001()
        # self.cleanSS()+
        # self.translate_backup_dict()
        # self.translate_backup_dict_using_google()
        # self.test_code_0001()
        # self.test_brk_pat()
        # self.cleanKritaPOFile()
        # self.correct_snippet_seq()
        # self.printEmptyPOLines()


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
