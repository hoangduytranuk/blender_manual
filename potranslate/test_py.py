#!/usr/bin/python3
#cython: language_level=3
# -*- coding: utf-8 -*-
# import sys
# print(sys.path)
# exit(0)
# sys.path.append('/Users/hoangduytran/Dev/tran/blender_manual/potranslate')

import re
import os
import json
import time
from collections import OrderedDict, defaultdict
from translation_finder import TranslationFinder
from sphinx_intl import catalog as c
from common import Common as cm
from utils import dd, pp
from matcher import MatcherRecord
from definition import Definitions as df, RefType, TranslationState
from reflist import RefList
import inspect as INP
import cProfile, pstats, io
from ignore import Ignore as ig
from string_utils import StringUtils as st
from pattern_utils import PatternUtils as pu
from enum import Enum
from case_action_list import CaseActionList, CaseAction, CaseRecord
from babel.messages import Catalog, Message
from pprint import pprint as pp
from bracket import RefAndBracketsParser as PSER
from observer import LocationObserver

# cd ../blender_docs
# pip3 install --user -r requirements.txt 
# pip3 --user install --upgrade pip
# sudo pip3 install --upgrade pip
# pip3 install --user urlextract fuzzywuzzy python-Levenshtein

class ProblemRecord:
    def __init__(self, funct_name=None, key=None, msg=None, new_msgid=None, new_msgstr=None, remove_key=None):
        self.funct_name=funct_name
        self.key = key
        self.msg: Message = msg
        self.remove_key = remove_key
        self.new_msgid = new_msgid
        self.new_msgstr = new_msgstr

    def __repr__(self):
        msg = f'funct_name:[{self.funct_name}()]\nold_msgid[{self.msg.id}]\nnew_msgid:[{self.new_msgid}]\n'
        msg += f'old_msgstr[{self.msg.string}]\nnew_msgstr:[{self.new_msgstr}]\n'
        has_remove_key = (self.remove_key is not None)
        if has_remove_key:
            msg += f'remove_key:[{self.remove_key}]\n'
        has_context = (self.msg.context is not None)
        if has_context:
            msg += f'context:[{self.msg.context}]\n\n'
        else:
            msg += f'\n'
        return msg

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
    def __init__(self):
        home = os.environ['HOME']
        self.home = os.path.join(home, 'Dev/tran')


    def readFile(self, file_name):
        with open(file_name, 'r') as f:
            data_lines = f.read().splitlines()
        return data_lines

    def writeFile(self, file_name, data):
        data_list = [(x + '\n') for x in data]
        with open(file_name, 'w+') as f:
            f.writelines(data_list)

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
        # from googletrans import Translator
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
                # "``anim_time_max`` -- Maximum number of seconds to show the animation for (in case the end frame is very high for no reason).",
                '"Bone" is "Bone.003" \'s parent. Therefore, "Bone.003" \'s root is the same as the tip of "Bone". Since "Bone" is still selected, its tip is selected. Thus the root of "Bone.003" remains selected.'
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

    def test_get_partial(self):
        msg = 'scene and view layer settings'
        msg = 'volume'
        cx = 'nothing'
        tf = TranslationFinder()
        # result = tf.getDict().getBestMatchPartial(msg)
        result = tf.getDict().get(msg, ctx=cx)
        result_msg = f'looking for: {msg}, context:{cx}; result: {result}'
        # if not bool(result):
        #     result_msg = f'Looking for:{msg}\nFound nothing!'
        # else:
        #     (matching_ratio, (full_key, full_value)) = result
        #     result_msg = f'Looking for:{msg};\ngot msgid:{full_key}\ngot msgstr:{full_value}\nmatching ratio:{matching_ratio}'
        print(result_msg)

    def flatText(self):
        home = os.environ['HOME']
        ofile = os.path.join(home, 'flat_txt.log')
        t = '''
        "Một ví dụ: Nếu bạn đã tạo một nguyên liệu mà bạn muốn sử dụng với các yếu"
" tố đầu vào khác biệt, ví dụ: màu khuếch tán: nhựa màu đỏ, nhựa màu xanh "
"lá cây, thì bạn có thể tạo các nguyên liệu riêng biệt bằng nút "
":abbr:`Biến Thành Đơn Người Dùng (Make Single User)` cho mỗi màu khác "
"biệt, với bản sao của phần cây mô tả vật liệu nhựa. Nếu bạn muốn chỉnh "
"sửa nguyên liệu, thì bạn cần phải chỉnh sửa lại Toàn bộ các nguyên liệu. "
"Một Phương Pháp tốt hơn để tái sử dụng là tạo các nhóm nút, chỉ cho lộ ra"
" các tham số đầu vào (ví dụ: :abbr:`màu khuếch tán (diffuse color)`)"
        '''
        t1 = t.replace('"\n"', '').strip()
        with open(ofile, 'w+') as f:
            f.write(t1)
        print(t1)
        exit(0)

    def testString(self):
        class TestingCase(list):
            def __init__(self):
                self.line = 'This is line'

        def map_func(item):
            mm: MatcherRecord = None
            (loc, mm) = item
            if (map_func.start == -1):
                word = mm.txt.upper()
            else:
                word = mm.txt.title()
            mm.txt = word
            (map_func.start, map_func.end) = loc
            return word

        (map_func.start, map_func.end) = (-1, -1)


        s1 = "Alternate script path :abbr:`nhất định phải (must)` , matching the Default Layout with subdirs: startup, add-ons & modules (Requires restart)"
        s2 = "nó :abbr:`nhất định phải (must)` có cái tên này để blender nhận ra nó"
        s3 = "a single Instance string"
        s1_tran = 'đường dẫn cho tập Lệnh thay thế :abbr:`nhất định phải (must)` khớp với bố Trí Mặc Định với các thư mục nhánh: startup, add-ons & modules (đòi hỏi phải Khởi Động Lại)'

        s1 = "*Material* modifier alters the base property with a new one taken from a given range mapped on the current material under the stroke"
        s1_tran = "Bộ điều chỉnh :abbr:`*Nguyên vật liệu* (*Material*)` cảnh báo :abbr:`tính chất nền (base property)` bằng một cái mới được lấy từ một phạm vi đã cho ánh xạ trên nguyên vật liệu hiện tại, dưới nét vẽ"

        # s1 = "*Mirror*"
        # s1_tran = ":abbr:`Phản Chiếu Đối Xứng (Mirror*"

        new_txt = CaseActionList.matchCase(s1, s1_tran)
        print(f'[{new_txt}]')


    def fix_abbr(self):
        from babel.messages.catalog import Message
        home_dir = os.environ['HOME']
        po_path = os.path.join(home_dir, 'Dev/tran/blender_docs/locale/vi/LC_MESSAGES/blender_manual.po')
        out_path = os.path.join(home_dir, 'blender_manual_0001.po')

        msg_data = c.load_po(po_path)
        m: Message
        changed = False
        # GA_REF_PART = re.compile(r'([^:])(abbr:\`([^\(\)]+)\s\(([^\(\)]+))(\W+)?', re.I)
        GA_REF_PART = re.compile(r':abbr:\`([^\(\)]+)\s\(([^\(\)]+)', re.I)
        for index, m in enumerate(msg_data):
            is_first = (index == 0)
            if is_first:
                continue

            msgid = m.id
            msgstr = m.string

            strip_symbs = '"\'*'
            found_dict = pu.patternMatchAll(GA_REF_PART, msgstr)
            is_found = bool(found_dict)
            count = 0
            if is_found:
                mm: MatcherRecord = None
                is_printed_msg = False
                for (loc, mm) in found_dict.items():
                    (s, e) = loc
                    has_ending = (msgstr[e:e+2] == ')`')
                    if has_ending:
                        continue

                    if not is_printed_msg:
                        print(f'msgid:[{msgid}]')
                        print(f'msgstr:[{msgstr}]')
                        is_printed_msg = True

                    pp(mm.getSubEntriesAsList())
                    count += 1
                if bool(count):
                    print('----------\n\n')

        if changed:
            c.dump_po(out_path, msg_data)

    def fix_file(self):
        from babel.messages.catalog import Message
        home_dir = os.environ['HOME']
        # po_path = os.path.join(home_dir, 'Dev/tran/blender_docs/locale/vi/LC_MESSAGES/blender_manual.po')
        po_path = os.path.join(home_dir, 'blender_manual_0001.po')
        out_path = os.path.join(home_dir, 'blender_manual_0002.po')

        msg_data = c.load_po(po_path)
        m: Message
        changed = False
        pat = re.compile(r'[]')
        for index, m in enumerate(msg_data):
            is_first = (index == 0)
            if is_first:
                continue

            msgid = m.id
            msgstr = m.string
            print(f'msgid:[{msgid}]\nmsgstr:[{msgstr}]\n\n')

    def fixpo(self):
        def findOne(pattern, id, str):
            total_match_list = []
            match_list = pattern.findall(msgid)
            total_match_list.extend(match_list)

            match_list = pattern.findall(msgstr)
            total_match_list.extend(match_list)
            return total_match_list

        from babel.messages.catalog import Message
        home_dir = os.environ['HOME']
        # po_path = os.path.join(home_dir, 'Dev/tran/blender_docs/locale/vi/LC_MESSAGES/blender_manual.po')
        po_path = os.path.join(home_dir, 'blender_manual_0006.po')
        out_path = os.path.join(home_dir, 'blender_manual_0007.po')

        data = c.load_po(po_path)
        GA_SINGLE = re.compile(r'(?!:)\`(?!\s)[^\`]+\S\`__')
        GA_DOUBLE = re.compile(r'\`{2}[^\`]+?\`{2}(?<!\(\s)')
        SINGLE_QUOTE = re.compile(r'\'+(?![\s\,\`]|ll|[tsd]\s)[^\']+\'+(?<!\(\s)')
        DOUBLE_QUOTE = re.compile(r'\"+(?![\s\,\`])[^"]+\"+(?<!\(\s)') ## r'(?<!\\")(")(\S[^\"]+\S)(")'
        AST = re.compile(r'\*+(?![\s\,\`])[^*]+\*+(?<!\(\s)')
        REF_GENERIC = re.compile(r':\w+:(?!:)\`(?!\s)[^\`]+\S\`')
        # ignoring math,
        REF_CONTENT_WITH_LINK_SPLITTER = re.compile(r'([^\<\>]+)\s(\<[^\<\>]+\>)')
        # for term, doc, ref, ga_single(`txt`__) -- ignore if no link, format :...:`vn_txt (en_txt) <link>`(__)

        MENU_SELECTION = re.compile(r':menuselection:\`([^`]+)(\s[\-]{2}>\s([^`]+))*\`')
        MENU_TXT_SPLITTER = re.compile(r'\s[\-]{2}>\s')

        ABBR_SPLITER = re.compile(r':abbr:\`([^`]+)\s\(([^<>]+)\)\`')
        GUI_LABEL_SPLITER = re.compile(r':guilabel:\`([^`]+)\`')
        GA_DOUBLE_SPLITTER = re.compile(r'[\`]{2}([^`]+)[\`]{2}') # note brackets (txt), leanding --|\+|\*|\(|\'|\.|\/,\d+, leave translations on right (*trans*), breakup punctuations
        pattern_list = [GA_SINGLE, GA_DOUBLE, SINGLE_QUOTE, DOUBLE_QUOTE, AST, REF_GENERIC]
        total_match_list=[]
        for m in data:
            msgid = m.id
            msgstr = m.string
            for pat in pattern_list:
                match_list = findOne(pat, msgid, msgstr)
                total_match_list.extend(match_list)

        for text in total_match_list:
            print(text)
            abbr_dict = pu.patternMatchAll(ABBR_SPLITER, text)
            is_abbr = bool(abbr_dict)
            if is_abbr:
                pp(abbr_dict)

            # menu_dict = pu.patternMatchAll(MENU_SELECTION, text)
            # is_menu = bool(menu_dict)
            # if is_menu:
            #     for (loc, mm) in menu_dict.items():
            #         print(f'menu_dict component start:')
            #         sub_list = mm.getSubEntriesAsList()
            #         (loc0, txt0) = sub_list[0]
            #         (loc1, txt1) = sub_list[1]
            #         text_components = pu.findInvert(MENU_TXT_SPLITTER, txt1)
            #         pp(text_components)
            #         print(f'menu_dict component end:-------')
        exit(0)
        # c.dump_po(out_path, data, line_width=4096)

    def testRefList(self):
        home = os.environ['HOME']

        test_file = os.path.join(home, 'cor_0006.po')
        data = c.load_po(test_file)
        collector=[]
        # tf = TranslationFinder()
        for m in data:
            msgid = m.id
            if not bool(msgid):
                continue

            msgstr = m.string

            ref_list = PSER.parseMsgAndBrackets(msgid, is_ref_only=False)
            if ref_list:
                print('MSGSTR: ------')
                print(msgstr)
                print(ref_list)
                print('END: ------\n\n')
            # # collector.extend(ref_list)
            # # if is_debug:
            # #     exit(0)
        mm: MatcherRecord = None
        # for ref_list in collector:
        #     pp(ref_list)

    def debug_po(self):
        home = os.environ['HOME']
        in_file = os.path.join(home, 'test_dict_0001.po')
        out_file = os.path.join(home, 'test_debug_0001.po')
        data = c.load_po(in_file)
        c.dump_po(out_file, data, line_width=4096)

    def testenum(self):
        pass

    def find_terms(self):
        home = os.environ['HOME']
        in_file = os.path.join(home, 'cor_0005.po')
        out_file = os.path.join(home, 'cor_0006.po')
        pat = re.compile(r'[^:]term:`[^\`]`')
        changed = False
        data = c.load_po(in_file)
        # found_data = list(map(find_invalid_term, data))

    def cleanRepeat(self):
        home = os.environ['HOME']
        file_path = os.path.join(home, 'blender_manual_0002.po')
        out_path = os.path.join(home, 'blender_manual_0002_0001.po')
        data = c.load_po(file_path)
        is_changed = False
        for m in data:
            msgid = m.id
            msgstr = m.string
            formatted_same = f'{msgid} ({msgid})'
            is_same = (msgid == msgstr) or (msgstr == formatted_same)
            if is_same:
                m.string = ""
                is_changed = True
        if is_changed:
            c.dump_po(out_path, data)

    def test_ref(self):
        msgstr_pattern = re.compile(r'([\*\"\']+)?\`([^\`\<\>\(\)]+)\s[-]{2}\s([^\`\<\>\(\)]+)(\s\<[^\`\<\>]+\>)?\`[_]+([\*\"\']+)?')
        t = "\"`Trang của Đề Án -- Project Page <https://developer.blender.org/project/profile/53/>`__\""
        l = pu.patternMatchAll(msgstr_pattern, t)
        mm: MatcherRecord = None
        for (loc, mm) in l.items():
            sub_list = mm.getSubEntriesAsList()
            (oloc, otxt) = sub_list[0]
            (oloc, otxt) = sub_list[1]
            (oloc, otxt) = sub_list[2]
        # match = msgstr_pattern.search(t)
        # print(match)

    def checkOldRef(self):

        pat_txt = r'([\*\"\']+)([^\*\"\']+)([\*\"\']+)\s\(([^\(\)]+)\)'
        p = re.compile(pat_txt)

        p = re.compile(r'([\"]+)((?:[\w])[^\"]+(?:[\w]))([\"]+)')
        t =  "To transition the audience from one scene or shot to\" another, a common technique is to \"fade to black\". As its name implies, the scene fades to a black screen. You can also \"fade to white\" or whatever color you wish, but black is a good neutral color that is easy on the eyes and intellectually \"resets\" the viewer's mind. The node tree below shows how to do this using the Set Alpha node."
        m = p.search(t)
        print(m)

    def cleanBrackets(self):
        def dealWithOneLine(txt: str):
            ref_list = PSER(txt)
            (new_loc, new_txt) = ref_list.getTextStrippedNonAlpha()
            is_diff = (new_txt != txt)
            if is_diff:
                return new_txt
            else:
                return None

        home = os.environ['HOME']
        file_path = os.path.join(home, 'cor_0012.po')
        out_path = os.path.join(home, 'cor_0013.po')
        data = c.load_po(file_path)
        is_changed = False
        braket_pattern_only = re.compile(r'^[\(\)\[\]\<\>]+$')
        bracket_set = re.compile(r'^((\(\))|(\[\])|(\<\>))$')
        dot_ending = re.compile(r'[\.\,\!\:\s]+$')
        eg_ie_start = re.compile(r'^((e\.g\.)|(i\.e\.))\s', re.I)
        ending_abbrev = re.compile(r'((e\.g\.)|(i\.e\.)|(etc\.)|(v\.\v\.))$')
        all_symbols = re.compile(r'^(\W+)$')
        operation_list = []
        for (key, m) in data._messages.items():
            has_context = not (m.context is None)
            if has_context:
                is_debug = True

            msgid = m.id
            msgstr = m.string

            # is_debug = ('RGB float' in msgid)
            # if is_debug:
            #     is_debug = True

            new_msgid = dealWithOneLine(msgid)
            new_msgstr = dealWithOneLine(msgstr)
            is_valid = (bool(new_msgid) or bool(msgstr))
            if not is_valid:
                continue

            new_msgid = (new_msgid if (new_msgid is not None) else msgid)
            new_msgstr = (new_msgstr if (new_msgstr is not None) else msgstr)

            # (self, funct_name=None, key=None, msg=None, new_msgid=None, new_msgstr=None, remove_key=None):
            r = ProblemRecord(
                funct_name='cleanBrackets',
                key=msgid,
                msg=m,
                new_msgid=new_msgid,
                new_msgstr=new_msgstr,
                remove_key=msgid,
            )
            operation_list.append(r)
            print(r)

        r: ProblemRecord = None
        for r in operation_list:
            key = (r.remove_key if bool(r.remove_key) else r.msg.id)
            del data[key]
            is_changed = True

        for r in operation_list:
            r.msg.string = r.new_msgstr
            r.msg.id = r.new_msgid
            data[r.new_msgstr] = r.msg
            is_changed = True

        if is_changed:
            c.dump_po(out_path, data, line_width=4096, sort_output=True)

    def fix_blender_man(self):
        home = os.environ['BLENDER_MAN_VI']
        home = os.path.join(home, 'LC_MESSAGES')
        file_path = os.path.join(home, 'blender_manual.po')
        out_path = os.path.join(home, '20220302_blender_manual.po')
        data = c.load_po(file_path)
        is_changed = False
        for m in data:
            msgid = m.id
            is_emtpy = not bool(msgid)
            if is_emtpy:
                continue

            ref_list = PSER(msgid)
            ref_list.parseMessage(is_ref_only=True, pattern_list=df.pattern_list, is_reverse=False, include_brackets=True)
            unmarked = ref_list.local_obs.getUnmarkedPartsAsDict()
            msgstr = m.string


    def test_sent(self):
        def getTextOnly(entry):
            mm: MatcherRecord = None
            (loc, mm) = entry
            return mm.txt

        home = os.environ['HOME']
        file_path = os.path.join(home, 'cor_0013.po')
        out_path = os.path.join(home, 'cor_0014.po')
        data = c.load_po(file_path)
        is_changed = False
        m: Message = None
        operation_list = []
        for m in data:
            msgid = m.id
            is_empty_id = len(msgid) == 0
            if is_empty_id:
                continue

            ref_list = PSER(msgid)
            msgid_list = list(ref_list.getBreakupSentenceList().items())
            is_broken_up = (len(msgid_list) > 1)
            if not is_broken_up:
                continue

            # print(f'orig: [{msgid}]')
            # print(msgid_list)

            msgstr = m.string
            is_empty_str = len(msgstr) == 0
            if is_empty_str:
                continue

            orig_msg = f'ORIG:\n---\nmsgid "{msgid}"\nmsgstr "{msgstr}"\n---\n'
            print(orig_msg)
            ref_list = PSER(msgstr)
            msgstr_list = list(ref_list.getBreakupSentenceList().items())
            # print(msgstr_list)
            # print('-' * 80)

            id_len = len(msgid_list)
            str_len = len(msgstr_list)
            can_map = (id_len == str_len)
            if not can_map:
                print('ERROR: entry is not MAPPABLE')
                print('x' * 80)
                msgid_txt_list = list(map(getTextOnly, msgid_list))
                msgstr_txt_list = list(map(getTextOnly, msgstr_list))
                pp(msgid_txt_list)
                print('-' * 80)
                pp(msgstr_txt_list)
                print('x' * 80)
            else:
                for i in range(0, id_len):
                    (loc, mm_id) = msgid_list[i]
                    (loc, mm_str) = msgstr_list[i]
                    new_msgid = mm_id.txt
                    new_msgstr = mm_str.txt
                    # (self, funct_name=None, key=None, msg=None, new_msgid=None, new_msgstr=None, remove_key=None):
                    r = ProblemRecord(
                        funct_name='breakupSentence',
                        key=msgid,
                        msg=m,
                        new_msgid=new_msgid,
                        new_msgstr=new_msgstr,
                        remove_key=msgid,
                    )
                    operation_list.append(r)
                    msg = f'msgid "{new_msgid}"\n'
                    msg += f'msgstr "{new_msgstr}"\n\n'
                    print(msg)

    def test_grep(self):

        home = os.environ['HOME']
        file_path = os.path.join(home, 'test_0001.log')
        with open(file_path, 'r') as f:
            data_list = f.readlines()

        pat_txt = r'\w+\.\s[a-z]'
        p = re.compile(pat_txt)
        for l in data_list:
            match_list = p.findall(l)
            if len(match_list) > 0:
                print(match_list)

    def abbrev(self):
        def removeIfExcluded(entry):
            excluded_word_list = removeIfExcluded.excluded_word_list
            mm: MatcherRecord = None
            (loc, mm) = entry
            excluded_test = [(mm.txt in exword) for exword in excluded_word_list]
            is_excluded = (True in excluded_test)
            if is_excluded:
                is_excluded = True
            return not is_excluded

        def getTextOnly(entry):
            mm: MatcherRecord = None
            (loc, mm) = entry
            return mm.txt

        def getAllTitleCasedWords(text_dict_list: dict, excluded_word_list: list):
            def update_location_with_orig(entry):
                orig_loc = update_location_with_orig.orig_loc
                mm: MatcherRecord = None
                (loc, mm) = entry
                (os, oe) = orig_loc
                (cs, ce) = loc
                ns = (os + cs)
                ne = ns + (ce - cs)
                new_loc = (ns, ne)
                mm.updateMasterLoc(ns, ne)
                return (new_loc, mm)

            mm: MatcherRecord = None
            word_dict={}
            word_list=[]
            for (loc, mm) in text_dict_list.items():
                txt = mm.txt
                titled_word_dict = pu.patternMatchAll(TITLE_CASED, txt)
                has_word = (len(titled_word_dict) > 0)
                if not has_word:
                    continue

                update_location_with_orig.orig_loc = loc
                updated_list = list(map(update_location_with_orig, titled_word_dict.items()))
                titled_word_dict = OrderedDict(updated_list)
                is_check_exclusion = (excluded_word_list is not None)
                if is_check_exclusion:
                    removeIfExcluded.excluded_word_list = excluded_word_list
                    included_word_list = list(filter(removeIfExcluded, titled_word_dict.items()))
                    titled_word_dict = OrderedDict(included_word_list)
                txt_only_list = list(map(getTextOnly, titled_word_dict.items()))
                word_dict.update(titled_word_dict)
                word_list.extend(txt_only_list)
            return word_dict, word_list

        def processOneString(txt: str, excluded_word_list: list):
            ref_list = PSER(txt)
            ref_list.parseMessage(is_ref_only=True, pattern_list=df.pattern_list, include_brackets=True, is_reverse=False)
            obs = ref_list.local_obs
            text_dict = obs.getUnmarkedPartsAsDict(reversing=False)
            titled_dict, titled_txt_list = getAllTitleCasedWords(text_dict, excluded_word_list)
            return titled_dict, titled_txt_list, ref_list

        ending_punct = r'([\,\.!]+$)'
        ENDING_WITH_PUNCT = re.compile(ending_punct)
        home = os.environ['HOME']
        file_path = os.path.join(home, 'cor_0013.po')
        out_path = os.path.join(home, 'cor_0013_02.po')
        data = c.load_po(file_path)
        is_changed = False
        m: Message = None
        operation_list = []
        vn_uppercase_letters = u'ĂÂÁẮẤÀẰẦẢẲẨÃẴẪẠẶẬĐÊÉẾÈỀẺỂẼỄẸỆÍÌỈĨỊÔƠÓỐỚÒỒỜỎỔỞÕỖỠỌỘỢƯÚỨÙỪỦỬŨỮỤỰÝỲỶỸỴA-Z\d'
        title_case_txt = r'(?:[%s][^\s\!\:\,]+)(\s(?:[%s][^\s\!\:\,]+))*' % (vn_uppercase_letters, vn_uppercase_letters)
        TITLE_CASED = re.compile(title_case_txt, re.UNICODE)

        sep = f'-' * 80
        sep1 = f'*' * 80
        changed = False
        for m in data:
            can_print_orig_txt = False
            msgid = m.id
            is_empty_id = len(msgid) == 0
            if is_empty_id:
                continue

            msgstr = m.string
            new_msgstr = str(msgstr)

            is_debug = ('Confirm, %s: Cancel' in msgid)
            if is_debug:
                is_debug = True

            msgstr_titled_dict, msgstr_titled_txt_list, str_reflist = processOneString(msgstr, None)
            str_reflist_txt_only = list(map(getTextOnly, str_reflist.items()))
            msgid_titled_dict, msgid_titled_txt_list, id_reflist = processOneString(msgid, str_reflist_txt_only)


            has_id = len(msgstr_titled_dict) > 0
            if not has_id:
                continue

            pair_list = []
            mid: MatcherRecord = None
            mstr: MatcherRecord = None
            mid_list = list(msgid_titled_dict.items())
            mstr_list = list(msgstr_titled_dict.items())
            can_print_orig_txt = (len(mid_list) > 0)
            if not can_print_orig_txt:
                continue

            for i, (id_loc, mid) in enumerate(mid_list):
                try:
                    (str_loc, mstr) = mstr_list[i]
                    id_txt = mid.txt
                    str_txt = mstr.txt
                    # is_ignore = (id_txt == msgid) or (id_txt == str_txt)
                    is_ignore = (id_txt == str_txt)
                    if is_ignore:
                        continue

                    pair_entry = ((id_loc, mid.txt), (str_loc, mstr.txt))
                    pair_list.append(pair_entry)
                except Exception as e:
                    pass

            if can_print_orig_txt:
                msg = f'\n\nmsgid "{msgid}"\nmsgstr "{msgstr}"\n'
                print(msg)
                can_print_orig_txt = False

            can_pair = len(pair_list) > 0
            if can_pair:
                # sorted_pair_list = list(sorted(pair_list, reverse=False, key=pairListSortByLoc))
                replace_list = []
                for ((id_loc, mid_txt), (str_loc, mstr_txt)) in pair_list:
                    mid_txt = ENDING_WITH_PUNCT.sub('', mid_txt)
                    match = ENDING_WITH_PUNCT.search(mstr_txt)
                    if match:
                        match_txt = match.group(0)
                        (s_s, s_e) = str_loc
                        s_e -= len(match_txt)
                        str_loc = (s_s, s_e)

                    is_ast = (df.AST_QUOTE.search(mid_txt) is not None)
                    if is_ast:
                        mid_txt = mid_txt[1:-1]
                        (s_s, s_e) = str_loc
                        str_loc = (s_s+1, s_e-1)
                        new_txt = f'\\":abbr:`{mstr_txt} ({mid_txt})`\\"'
                    else:
                        new_txt = f':abbr:`{mstr_txt} ({mid_txt})`'
                    print(new_txt)
                    entry = (str_loc, new_txt)
                    replace_list.append(entry)
                    # print(new_txt)

                replace_list.sort(reverse=True)
                for (str_loc, new_txt) in replace_list:
                    new_msgstr = cm.jointText(new_msgstr, new_txt, str_loc)

                m.string = new_msgstr
                changed = True
            else:
                msg = 'UNABLE TO MAP:'
                print(msg)
                pp(msgid_titled_txt_list)
                pp(msgstr_titled_txt_list)
            print(sep1)

        if changed:
            c.dump_po(out_path, data, line_width=4096, sort_output=True)

    def correctRef(self):
        class MatcherExtractRecord():
            def __init__(self, mm: MatcherRecord):
                sub_list = mm.getSubEntriesAsList()
                sub_list_len = len(sub_list)
                has_type = (sub_list_len > 5)
                (self.oloc, self.orig_txt) = sub_list[0]
                if has_type:
                    (self.type_loc, self.ref_type) = sub_list[1]
                    (self.ref_txt_with_link_loc, self.ref_txt_with_link) = sub_list[2]
                    (self.ref_txt_loc, self.ref_txt) = sub_list[3]
                    (self.ref_link_loc, self.ref_link) = sub_list[4]
                    (self.ref_link_txt_loc, self.ref_link_txt) = sub_list[5]
                else:
                    (self.ref_txt_with_link_loc, self.ref_txt_with_link) = sub_list[1]
                    (self.ref_txt_loc, self.ref_txt) = sub_list[2]
                    (self.ref_link_loc, self.ref_link) = sub_list[3]
                    (self.ref_link_txt_loc, self.ref_link_txt) = sub_list[4]

        def getMMTextAndLink(mm: MatcherRecord):
            sub_list = mm.getSubEntriesAsList()
            sub_list_len = len(sub_list)
            has_type = (sub_list_len > 5)
            if (sub_list_len < 5 or sub_list_len > 6):
                raise RuntimeError(f'WRONG SUBLIST_LENGTH,\n{sub_list}\n\n')

            mmxrec = MatcherExtractRecord(mm)
            return mmxrec

        def matchingRefIDAndStr(str_entry):
            str_mm: MatcherRecord = None
            (str_loc, str_mm) = str_entry
            id_ref_txt = matchingRefIDAndStr.id_ref_txt
            str_mmxrec: MatcherExtractRecord = getMMTextAndLink(str_mm)
            str_ref_txt = str_mmxrec.ref_txt
            is_match = (id_ref_txt in str_ref_txt)
            return is_match

        def pairing(id_match_entry):
            mm: MatcherRecord = None
            str_match_dict = pairing.str_match_dict
            id_match_dict = pairing.id_match_dict
            (loc, mm) = id_match_entry
            id_mmexrec = getMMTextAndLink(mm)

            matchingRefIDAndStr.id_ref_txt = id_mmexrec.ref_txt
            matching_str_list = list(filter(matchingRefIDAndStr, str_match_dict.items()))
            has_match = (bool(matching_str_list) and (len(matching_str_list) > 0))
            if not has_match:
                entry_with_wrong_text_and_can_replace = (len(id_match_dict) == 1) and (len(str_match_dict) == 1)
                if not entry_with_wrong_text_and_can_replace:
                    return (None, None)
                else:
                    try:
                        (str_loc, str_mm) = list(str_match_dict.items())[0]
                        str_mmxrec = MatcherExtractRecord(str_mm)
                        return (id_mmexrec, str_mmxrec)
                    except Exception as e:
                        return (None, None)
            else:
                (str_loc, str_mm) = matching_str_list[0]
                str_mmxrec = MatcherExtractRecord(str_mm)
                return (id_mmexrec, str_mmxrec)

        def sortWorkingPair(pair_entry):
            id_mmexrec: MatcherExtractRecord = None
            str_mmxrec: MatcherExtractRecord = None
            (id_mmexrec, str_mmxrec) = pair_entry
            return (id_mmexrec.oloc[0])

        pat_txt = r'\s[\'\"\(]([^\'\"\(\)]+)$'
        PAT = re.compile(r'(:\w+:)?[\`](((?!\s)[^\`\<\>]+)(\s<([^\`\<\>]+)>))[\`]', re.I)
        BRACKET = re.compile(r'[\(]([^\(\)]+)[\)]', re.I)

        home = os.environ['HOME']
        file_path = os.path.join(home, 'blender_manual_0003_0007.po')
        out_path = os.path.join(home, 'blender_manual_0003_0008.po')
        data = c.load_po(file_path)
        m: Message = None
        sep1 = f'*' * 80
        sep2 = f'-' * 80
        changed = False
        for index, m in enumerate(data):
            msgid = m.id
            is_empty = len(msgid) == 0
            if is_empty:
                continue

            is_debug = ('World Scale UV' in msgid)
            if is_debug:
                is_debug = True

            msgstr = m.string
            id_match_dict = pu.patternMatchAll(PAT, msgid)
            is_found = (id_match_dict is not None) and (len(id_match_dict) > 0)
            if not is_found:
                continue

            str_match_dict = pu.patternMatchAll(PAT, msgstr)
            is_found = (str_match_dict is not None) and (len(str_match_dict) > 0)
            if not is_found:
                continue

            new_msgstr = str(msgstr)
            pairing.str_match_dict = str_match_dict
            pairing.id_match_dict = id_match_dict
            paired_list = list(map(pairing, id_match_dict.items()))
            is_found = (len(paired_list) > 0)
            if not is_found:
                msg = f'NOT MATCH:\n'
                msg += f'[{id_match_dict}]\n[{str_match_dict}]\n\n'
                pp(msg)
            else:
                working_pair = [(x, y) for (x, y) in paired_list if bool(x) and bool(y)]
                working_pair.sort(key=sortWorkingPair, reverse=True)
                id_mmexrec: MatcherExtractRecord = None
                str_mmxrec: MatcherExtractRecord = None
                replace_list = []
                for (id_mmexrec, str_mmxrec) in working_pair:
                    is_diff = (id_mmexrec.ref_link_txt != str_mmxrec.ref_link_txt)
                    if is_diff:
                        entry = (str_mmxrec.ref_link_loc, id_mmexrec.ref_link)
                        replace_list.append(entry)

                    is_id_ref_txt_already_in_str_ref_txt = (id_mmexrec.ref_txt in str_mmxrec.ref_txt) or \
                                                           (str_mmxrec.ref_txt == id_mmexrec.ref_txt)
                    if is_id_ref_txt_already_in_str_ref_txt:
                        continue

                    bracket_match = pu.patternMatchAll(BRACKET, str_mmxrec.ref_txt)
                    has_braket_match = bool(bracket_match) and len(bracket_match) > 0
                    if not has_braket_match:
                        continue

                    bracket_match_item: MatcherRecord = None
                    bracket_match_list = list(bracket_match.items())
                    (brk_loc, bracket_match_item) = bracket_match_list[0]
                    brk_sub_list = bracket_match_item.getSubEntriesAsList()
                    (brk_txt_loc, bracket_match_txt) = brk_sub_list[1]

                    new_str_ref_txt = cm.jointText(str_mmxrec.ref_txt, id_mmexrec.ref_txt, brk_txt_loc)
                    str_mmxrec.ref_txt = new_str_ref_txt
                    entry = (str_mmxrec.ref_txt_loc, str_mmxrec.ref_txt)
                    replace_list.append(entry)

                replace_list.sort(reverse=True)
                for (loc, replace_txt) in replace_list:
                    new_msgstr = cm.jointText(new_msgstr, replace_txt, loc)
                    m.string = new_msgstr
                    changed = True

                is_changed = (msgstr != new_msgstr)
                if is_changed:
                    print(f'REPLACED:\n old_msgstr:[{msgstr}]\n\nnew_msgstr:[{new_msgstr}]\n\n\n')

        is_writing_changes = (changed and bool(out_path))
        if is_writing_changes:
            c.dump_po(out_path, data, line_width=4096)


    def test_pattern(self):
        from itertools import groupby
        # single_quote_txt = r'(?:\s)\'([^\'\\]+)\''
        # single_quote_txt_absolute = r'^%s$' % (single_quote_txt)
        # SNG_QUOTE = re.compile(single_quote_txt)

        # t = "it's about my chart's colour but 'should find this' "
        # m = SNG_QUOTE.findall(t)
        # print(m)
        p = re.compile(r'\s?((?!\s)[A-z\d\s]+)(?<!\s)\s?') # for characters only, without refs
        t = "To create a sphere with 2D surfaces, " \
            "its the same principle as with a 2D circle. " \
            "You will note that the four different weights needed for creating a sphere " \
            "(1.0, 0.707 = sqrt(0.5), 0.354 = sqrt(2)/4, " \
            "and 0.25)."
        l = p.findall(t)
        print(l)

    def removeIfNotRepeatable(self, non_repeat_list):
        def cleanIfNonRepeat(m: Message):
            mid = m.id
            is_clean_tran = (mid in non_repeat_list)
            if is_clean_tran:
                m.string = ""
                return True
            else:
                return False

        def cleanIfSingleRefAndTranDoesntMatch(m: Message):
            mid = m.id
            has_id = (bool(mid) and len(mid) > 0)
            if not has_id:
                return False

            mstr = m.string
            has_str = (bool(mstr) and len(mstr) > 0)
            if not has_str:
                return False

            id_ref_list = PSER(mid)
            id_ref_list.parseMessage(is_ref_only=True, pattern_list=df.no_bracket_pattern_list, include_brackets=True, is_reverse=False)
            has_ref = (bool(id_ref_list) and len(id_ref_list) > 0)
            if not has_ref:
                return False

            has_one_ref = len(id_ref_list) == 1
            if not has_one_ref:
                return False

            idref_list = list(id_ref_list.items())
            first_ref: MatcherRecord = None
            (first_ref_loc, first_ref) = idref_list[0]
            is_consider_type = (first_ref.type in df.complex_pattern_type_list)
            if not is_consider_type:
                return False

            id_obs = id_ref_list.local_obs
            id_left = id_obs.getLeft()
            id_right = id_obs.getRight()
            (id_mid_loc, id_mid) = id_obs.getMid()
            no_left = not bool(id_left)
            no_right = not bool(id_right)
            ref_starts_at_zero = (id_mid_loc[0] == 0)
            ref_ends_at_end = (id_mid_loc[1] == len(mid))

            valid = (no_left and no_right and ref_starts_at_zero and ref_ends_at_end)
            if not valid:
                return False

            is_debug = ('``position``' in mid)
            if is_debug:
                is_debug = True

            id_txt_list = df.CHARACTERS.findall(mid)
            str_txt_list = df.CHARACTERS.findall(mstr)
            test_matching_list = [(id_word in str_txt_list) for id_word in id_txt_list]
            is_matched = not (False in test_matching_list)
            if not is_matched:
                m.string = ""
                m.flags.clear()
                return True
            else:
                return False

        def updateMessage(m: Message):
            mid = m.id
            valid = bool(mid)
            if not valid:
                return False

            mstr = m.string
            has_tran = bool(mstr)
            if not has_tran:
                return False

            return cleanIfSingleRefAndTranDoesntMatch(m)
            # return cleanIfNonRepeat(m)

        home = self.home
        man_po = os.path.join(home, 'blender_manual_0003_0014.po')
        man_po_out = os.path.join(home, 'blender_manual_0003_0015.po')
        data = c.load_po(man_po)
        result_id_cleaned = list(filter(updateMessage, data))
        result_id_cleaned.sort()

        m: Message = None
        for m in result_id_cleaned:
            mid = m.id
            mstr = m.string
            msg = f'REMOVE:\nmid: {mid}\nmstr: {mstr}\n\n'
            print(msg)


        is_changed = len(result_id_cleaned) > 0
        if is_changed:
            c.dump_po(man_po_out, data, line_width=4096)

        # print('CLEANED')
        # pp(result_id_cleaned)
        #
        # for mid in result_id_cleaned:
        #     m = data[mid]
        #     print(f'NEW STR:[{m.string}]')
        # print('CLEANED', len(result_id_cleaned))

    def cleanRefOnlyTran(self):
        home = self.home
        ignore_file = os.path.join(home, 'ignore.log')
        ignore_list = self.readFile(ignore_file)
        self.removeIfNotRepeatable(ignore_list)

    def fixGlossaryEntriesMakeEnGoesFirst(self):
        def bracket_to_square_bracket(txt: str):
            new_txt = txt.replace('(', '[')
            new_txt = new_txt.replace(')', ']')
            return new_txt

        def isInLocation(loc_entry):
            check_string = isInLocation.check_string
            (location_txt, line_no) = loc_entry
            is_in = (check_string in location_txt)
            if is_in:
                is_in = True
            return is_in

        def fixCurrentWrong(m: Message, mid: str, mstr:str):
            has_tran = bool(mstr)
            if not has_tran:
                new_tran = f'{mid} ()'
            else:
                is_title = ('Glossary' == mid)
                mid = bracket_to_square_bracket(mid)
                en_part = f'({mid})'

                vn_part = (mstr.replace(en_part, '').strip())
                vn_part = bracket_to_square_bracket(vn_part)
                new_tran = (f'{mid} ({vn_part})' if not is_title else f'{vn_part} ({mid})')

            msg = f'old:[{mstr}]\nnew:[{new_tran}]\n\n'
            print(msg)
            m.string = new_tran
            return mid

        def transferFromOldFile(m: Message, mid: str, mstr: str):
            try:
                old_ref_m: Message = old_ref_data[mid]
                old_str = old_ref_m.string
                msg = f'"{mid}"\nold_mstr "{old_str}"\n current_mstr "{mstr}"\n\n'
                print(msg)
                m.string = old_str
            except Exception as e:
                msg = f'NOT found in old_ref_data:\n msgid "{mid}"'
                print(msg)
            return m

        def recomposeGlossaryIndex(m: Message):
            mid = m.id
            valid = bool(mid)
            if not valid:
                return None

            is_title = (mid in title_list)
            if not is_title:
                return None

            check_string = 'manual/glossary/index'
            locations = m.locations
            isInLocation.check_string = check_string
            is_in_list = list(filter(isInLocation, locations))
            is_index = bool(is_in_list) and len(is_in_list) > 0
            if not is_index:
                return None

            mstr = m.string
            m = fixCurrentWrong(m, mid, mstr)
            # m = transferFromOldFile(m, mid, mstr)
            return m

        def reworkCurrentTitles(m: Message):
            mid = m.id
            valid = bool(mid)
            if not valid:
                return None

            is_title = (mid in title_list)
            if not is_title:
                return None

            has_brackets = (df.ARCH_BRAKET_MULTI.search(mid) is not None)
            if not has_brackets:
                return None

            mstr = m.string
            title_repeated = f'({mid})'
            is_repeated = (title_repeated in mstr)
            if not is_repeated:
                return None

            vn_part = mstr.replace(title_repeated, "").strip()
            new_mid = bracket_to_square_bracket(mid)
            new_mstr = bracket_to_square_bracket(vn_part)

            new_mstr = f'{new_mstr} ({new_mid})'
            m.string = new_mstr
            print(f'msgid "{mid}"')
            print(f'msgstr "{mstr}"')
            print(f'new_mstr "{new_mstr}"')
            print('x' * 30)

            # m = fixCurrentWrong(m, mid, mstr)
            # m = transferFromOldFile(m, mid, mstr)
            return m

        def cleanUnmatchedRefs(m: Message):
            def isMatch(entry):
                def id_in_str(id_word):
                    str_word_list = id_in_str.str_word_list
                    return (id_word in str_word_list)

                str_mm: MatcherRecord = None
                (str_loc, str_mm) = entry
                id_mm: MatcherRecord = isMatch.id_mm

                # is_debug = ('new_length = real_length' in id_mm.txt)
                # if is_debug:
                #     is_debug = True

                id_txt = id_mm.txt.lower()
                str_txt = str_mm.txt.lower()

                id_word_list = df.CHARACTERS.findall(id_txt)
                str_word_list = df.CHARACTERS.findall(str_txt)
                id_in_str.str_word_list = str_word_list

                is_id_in_str_condition_list = list(map(id_in_str, id_word_list))
                is_matched = not (False in is_id_in_str_condition_list)
                # if is_matched:
                #     msg = f'matched:\nid_mm:{id_mm}\nstr_mm:{str_mm}\nmatched----'
                #     print(msg)
                return is_matched

            def pairing(entry):
                mm: MatcherRecord = None
                str_ref_list = pairing.str_ref_list
                (loc, id_mm) = entry

                isMatch.id_mm = id_mm
                str_ref_matched_list = list(filter(isMatch, str_ref_list.items()))
                is_matched = (bool(str_ref_matched_list) and len(str_ref_matched_list) > 0)
                if not is_matched:
                    entry_return = (id_mm, None)
                else:
                    first_str_matched = str_ref_matched_list[0]
                    entry_return = (id_mm, first_str_matched)
                return entry_return

            mid = m.id
            mstr = m.string

            has_tran = (bool(mstr) and len(mstr) > 0)
            if not has_tran:
                return None

            id_ref_list = PSER(mid)
            id_ref_list.parseMessage(is_ref_only=True, pattern_list=df.no_bracket_pattern_list, include_brackets=True, is_reverse=False)
            has_ref = (bool(id_ref_list) and len(id_ref_list) > 0)
            if not has_ref:
                return None

            str_ref_list = PSER(mstr)
            str_ref_list.parseMessage(is_ref_only=True, pattern_list=df.no_bracket_pattern_list, include_brackets=True, is_reverse=False)
            has_str_ref = (bool(str_ref_list) and len(str_ref_list) > 0)
            if not has_str_ref:
                return None

            pairing.str_ref_list = str_ref_list
            paired_list = list(map(pairing, id_ref_list.items()))
            unmatched_list = [id_mm for (id_mm, str_mm) in paired_list if (str_mm is None)]
            is_unmatched = (bool(unmatched_list) and len(unmatched_list) > 0)
            if is_unmatched:
                print('UNMATCHED')
                print('x' * 80)
                locations = m.locations
                pp(locations)
                print(f'msgid "{mid}"')
                print(f'msgstr "{mstr}"')
                print('x' * 30)
                pp(unmatched_list)
                print('x' * 30)
                # m.string = ""
            return m

        def updateMessage(m: Message):
            return reworkCurrentTitles(m)
            # return recomposeGlossaryIndex(m)
            # return cleanUnmatchedRefs(m)

        home = self.home
        ref_from_old_file = os.path.join(home, 'blender_manual_0003_0012.po')

        input_file = os.path.join(home, 'blender_manual_0003_0015.po')
        output_file = os.path.join(home, 'blender_manual_0003_0016.po')
        title_file = os.path.join(home, 'keep.log')
        title_list = self.readFile(title_file)

        data = c.load_po(input_file)
        old_ref_data = c.load_po(ref_from_old_file)

        result_list = list(map(updateMessage, data))
        result_list = [x for x in result_list if bool(x)]
        is_changed = len(result_list) > 0
        # is_changed = False
        if is_changed:
            c.dump_po(output_file, data, line_width=4096)

    def duplicateIdInTitles(self):

        def adjustCase(m: Message):
            mid: str = m.id
            mstr: str = m.string

            new_mstr = cm.matchCase(mid, mstr)
            valid = (new_mstr.lower() == mstr.lower())
            if not valid:
                msg = f'mstr:{mstr}\n{new_mstr}\n\n'
                raise RuntimeError(msg)

            is_changed = (mstr != new_mstr)
            if is_changed:
                m.string = new_mstr
                msg = f'mid:{mid}\nold_mstr:{mstr}\nnew_mstr:{new_mstr}\n\n'
                print(msg)

            return m

        def updateMessage(m: Message):
            title_list = updateMessage.title_list
            mid = m.id
            is_in_title_list = (mid in title_list)
            if not is_in_title_list:
                return None

            mstr = m.string
            has_translation = bool(mstr)
            if not has_translation:
                return None

            repeat_orig = f'({mid})'
            repeat_orig_lower = repeat_orig.lower()
            mstr_lower = mstr.lower()
            index_of_orig = mstr_lower.find(repeat_orig_lower)
            is_repeated = (index_of_orig > 0)
            if not is_repeated:
                return None

            # new_m = repeatOriginal(m)
            new_m = adjustCase(m)
            return new_m

        home = self.home
        input_file = os.path.join(home, 'blender_manual_0003_0019.po')
        output_file = os.path.join(home, 'blender_manual_0003_0020.po')
        title_file = os.path.join(home, 'keep.log')
        title_list = self.readFile(title_file)

        data = c.load_po(input_file)
        updateMessage.title_list = title_list

        result_list = list(map(updateMessage, data))
        result_list = [x for x in result_list if bool(x)]
        is_changed = len(result_list) > 0
        is_changed = False
        if is_changed:
            c.dump_po(output_file, data, line_width=4096)

    def correctBrackets(self):
        def correctBracketIfhasInternalBrackets(entry):
            mstr = correctBracketIfhasInternalBrackets.mstr

            loc: (int, int) = entry[0]
            text_within = entry[1]
            match_dict = pu.patternMatchAll(df.ARCH_BRAKET_MULTI, text_within)
            has_internal_bracket = (len(match_dict) > 0)
            if not has_internal_bracket:
                return False

            (new_txt_within, left_count) = re.subn(r'\(', '[', text_within)
            (new_txt_within, right_count) = re.subn(r'\)', ']', new_txt_within)
            is_changed = (left_count > 0) or (right_count > 0)
            if is_changed:
                is_changed = True
            return is_changed

        def count_percent_repeat(mid_word):
            mstr_word_list = count_percent_repeat.mstr_word_list
            mid_word_percent = count_percent_repeat.mid_word_percent
            is_repeated = (mid_word in mstr_word_list)
            mstr_word_percent = (100 / len(mstr_word_list))
            return (mstr_word_percent if is_repeated else 0)

        def checkRepeatedWordCount(msg: Message):
            mid = msg.id
            is_empty = not bool(mid)
            if is_empty:
                return False

            mstr = msg.string
            is_empty = not bool(mstr)
            if is_empty:
                return False

            mid_word_list = df.CHARACTERS.findall(mid)
            mstr_word_list = df.CHARACTERS.findall(mstr)

            mid_word_percent = (100 / len(mid_word_list))
            count_percent_repeat.mstr_word_list = mstr_word_list
            count_percent_repeat.mid_word_percent = mid_word_percent

            repeated_count_list = list(map(count_percent_repeat, mid_word_list))
            total_repeat = sum(repeated_count_list)
            is_changed = (total_repeat > 75)
            if is_changed:
                num_word_mstr = len(mstr_word_list)
                have_thang_in_it = ('Tháng' in mstr)

                can_blank_out = (num_word_mstr > 15) and not have_thang_in_it

                if can_blank_out:
                    error_msg = f'BLANKING: mid:{mid}\nmstr:{mstr}\ntotal_repeat:{total_repeat}\n\n'
                    print(error_msg)
                    msg.string = ""
                    is_changed = True
                else:
                    error_msg = f'not BLANKING: mid:{mid}\nmstr:{mstr}\ntotal_repeat:{total_repeat}\n\n'
                    print(error_msg)
                    is_changed = False
            return is_changed

        def update_matched_record(entry):
            mid = update_matched_record.mid
            mstr = update_matched_record.mstr
            PAT = update_matched_record.PAT

            old_mstr = str(mstr)
            loc: (int, int) = entry[0]
            mm: MatcherRecord = entry[1]

            match = pu.patternMatchAll(PAT, mid)
            is_id_the_same = (len(match) > 0)
            if is_id_the_same:
                has_origin_in_mstr = (mid.lower() in mstr.lower())
                if has_origin_in_mstr:
                    form1 = f'({mid})'
                    form2 = f'{mid}'
                    mstr = mstr.replace(form1, "")
                    mstr = mstr.replace(form2, "")

                new_str = mstr
                ending_with_dot = (mid.endswith('.') and not mid.endswith('...'))
                if ending_with_dot:
                    new_str = mstr[:-1]

                if ending_with_dot:
                    new_str = f'{new_str}.'
                else:
                    new_str = f'{new_str} ({mid})'
            else:
                sub_list = mm.getSubEntriesAsList()
                (mstr_front_loc, mstr_front_txt) = sub_list[1]
                (mstr_back_loc, mstr_back_txt) = sub_list[2]

                ending_with_dot = (mid.endswith('.') and not mid.endswith('...'))
                if ending_with_dot:
                    back_txt = mstr_back_txt[-1]
                    new_str = f'{mstr_front_txt}.'
                else:
                    back_txt = re.sub('\(', '[', mid)
                    back_txt = re.sub('\)', ']', mid)
                    new_str = f'{mstr_front_txt} ({mid})'
            mm.translation = new_str
            report_msg = f'id:{mid}\nold_str:{old_mstr}\nnew_str:{new_str}\n\n'
            print(report_msg)
            return True

        def processUpdateMatchedRecord(msg: Message):
            mid = msg.id
            mstr = msg.string

            have_thang_in_it = ('Tháng' in mstr)
            match = pu.patternMatchAll(PAT, mstr)
            is_found = (len(match) > 0) and not (have_thang_in_it)
            if not is_found:
                return False

            match_list = list(match.items())
            match_list.sort(reverse=True)

            update_matched_record.mid = mid
            update_matched_record.mstr = mstr
            update_matched_record.PAT = PAT
            result_list = list(filter(update_matched_record, match_list))
            is_fuzzy = msg.fuzzy
            if not is_fuzzy:
                msg.flags.add('fuzzy')
                is_fuzzy = msg.fuzzy
                debug = True

            is_changed = True
            return is_changed

        def updateMessage(msg: Message):
            mid = msg.id
            is_empty = not bool(mid)
            if is_empty:
                return False

            mstr = msg.string
            repeated_end_dot = f' {mid}.'
            is_in_mstr = (repeated_end_dot.lower() in mstr.lower())
            if is_in_mstr:
                report_msg = f'{mid}\n{mstr}\n\n'
                print(report_msg)
                new_mstr = (mstr.replace(repeated_end_dot, ""))
                msg.string = new_mstr
            is_changed = True
            return is_changed

        home = self.home
        input_file = os.path.join(home, 'blender_manual_0003_0019.po')
        output_file = os.path.join(home, 'blender_manual_0003_0020.po')

        leading_string = r'See :doc:`Here <([^<>]+)>`\.'
        pat_txt = r'^%s$' % (leading_string)
        pat_txt = r'(.+)\s[-]{2}\s(.+)'
        PAT = re.compile(pat_txt)

        data = c.load_po(input_file)
        result_list = list(map(updateMessage, data))
        result_list = [x for x in result_list if bool(x)]
        is_changed = (True in result_list)
        is_changed = False
        if is_changed:
            c.dump_po(output_file, data, line_width=4096)

    def test_pat(self):

        msgid = "Should I Translate\\.\\.\\. ?"
        msgstr = "Tôi có nên dịch hay không\\.\\.\\. ? (Should I Translate\\.\\.\\. ?). But this part should."

        p = re.compile(r'(?=(\s+|^)) ([A-Z]+)(?=(\b+|$))', re.UNICODE)
        msgid = "AutoCAD DXF"
        msgstr = ":abbr:`DXF (Drawing Interchange Format: Định Dạng Trao Đổi Họa Bản)` của AutoCAD (AutoCAD DXF)"

        m = p.search(msgid)
        print(m)

        # l1 = ['Những', 'Thay', 'Đổi', 'Lớn', 'Hơn', '(Bigger', 'Changes)']
        # l2 = l1[1:]
        # l3 = msgstr.split()
        # l4 = l3[1:]
        # print(l2)
        # def1 = '\\.\\.\\.'
        # def2 = '...'
        # rep1 = f"{'$' * len(def1)}"
        # rep2 = f"{'$' * len(def2)}"
        # rep_mstr = msgstr.replace(def1, rep1)
        # single_escaped_dot = re.escape(r'.')
        # double_escaped_dot = re.escape(r'\.')
        # escaped_dots = r'((%s)|(%s))' % (single_escaped_dot, double_escaped_dot)
        # full_stop_pat_txt1 = r'(?=\S)(\.)(?=(\s|$))'
        # full_stop_pat_txt2 = r'(?=\S)(\\\.)(?=(\s|$))'
        # try:
        #     FULL_STOP1 = re.compile(full_stop_pat_txt1)
        #     FULL_STOP2 = re.compile(full_stop_pat_txt2)
        #     m1 = pu.patternMatchAll(FULL_STOP1, msgstr)
        #     m2 = pu.patternMatchAll(FULL_STOP2, msgstr)
        #     print('m1:', m1.keys())
        #     # print('m2:', m2)
        #
        #     # loc_list = list(m1.keys())
        #     #
        #     # actual_loc_list=[]
        #     # start = 0
        #     # for (x, y) in loc_list:
        #     #     new_loc = (y, y+1)
        #     #     actual_loc_list.append(new_loc)
        #     # obs = LocationObserver(msgstr)
        #     # obs.markLocListAsUsed(actual_loc_list)
        #     # sen_dict = obs.getUnmarkedPartsAsDict(reversing=False)
        #     # print(sen_dict)
        #     # m2 = pu.patternMatchAll(FULL_STOP, msgstr)
        #     # m = FULL_STOP.split(msgid)
        #     # print(m1)
        #     # print(m2)
        # except Exception as e:
        #     print(e)
        # p = re.compile(r'\d+')
        # t = '123 456 7890 1234'
        # pos = 0
        # endpos = len(t)
        # for m in p.finditer(t, pos=pos, endpos=endpos):
        #     d = dir(m)
        #     g = m.groups()
        #     g = m.group()
        #     l = m.span()
        #     print(m)

    def printRefs(self):
        def getRefOneLine(line: str):
            ref_list = PSER(line)
            ref_list.parseMessage(is_ref_only=True, is_reverse=False, pattern_list=df.no_bracket_pattern_list, include_brackets=False)
            return ref_list

        def extractBracket(txt: str):

            bracket = df.ARCH_BRAKET_SINGLE.search(txt)
            no_bracket_part = df.ARCH_BRAKET_SINGLE.sub("", txt)
            bracket_part = bracket.group(1)
            abbrev_entry = f":abbr:`{no_bracket_part.strip()}({bracket_part.strip()})`"
            return [abbrev_entry]

        def extractLink(txt: str):
            link = df.REF_LINK.search(txt)
            no_link_part = df.REF_LINK.sub("", txt)
            abbrev_entry = extractBracket(no_link_part)
            return [abbrev_entry]

        def getTran(txt: str):
            tran = tf.isInDict(txt.strip())
            has_tran = (tran is not None)
            if has_tran:
                tran = extractAbbr(tran)
                abbrev_entry = f":abbr:`{tran} ({txt.strip()})`"
            else:
                abbrev_entry = f":abbr:`({txt.strip()})`"
            return abbrev_entry

        def rmKeyBoard(txt: str):
            match = pu.patternMatchAll(df.REF_GENERIC, txt)
            has_match = (len(match) > 0)
            if not has_match:
                return txt

            has_keyboard_test = [(mm.type == RefType.KBD) for (loc, mm) in match.items()]
            has_keyboard = (True in has_keyboard_test)
            if not has_keyboard:
                return txt

            has_keyboard_test = [loc for (loc, mm) in match.items() if (mm.type == RefType.KBD)]
            has_keyboard_test.sort(reverse=True)

            new_txt = str(txt)
            for loc in has_keyboard_test:
                new_txt = cm.jointText(new_txt, "", loc)

            return new_txt

        def extract_menu(txt: str):
            out_put_list = []
            txt_list = txt.split('-->')
            for txt_item in txt_list:
                bracket = df.ARCH_BRAKET_SINGLE.search(txt)
                has_bracket = (bracket is not None)
                if has_bracket:
                    abbrev_entry = extractBracket(txt_item)
                    out_put_list.extend(abbrev_entry)
                else:
                    abbrev_entry = getTran(txt_item)
                    out_put_list.append(abbrev_entry)
            return out_put_list

        def extractGuiLabel(txt: str):
            find_dict = pu.patternMatchAll(df.GUI_LABEL_PARSER, txt)
            found = len(find_dict) > 0
            if found:
                dict_list = list(find_dict.items())
                dict_list.sort(reverse=True)
                new_txt = str(txt)
                for (loc, mm) in dict_list:
                    sub_list = mm.getSubEntriesAsList()
                    (sub_loc, sub_txt) = sub_list[1]
                    new_txt = cm.jointText(new_txt, sub_txt, loc)
                return new_txt
            else:
                return txt

        def extractAbbr(txt: str):
            abbr_dict = pu.patternMatchAll(df.ABBREV_PATTERN_PARSER, txt)
            has_abbr = len(abbr_dict) > 0
            if has_abbr:
                abbr_dict_list = list(abbr_dict.items())
                abbr_dict_list.sort(reverse=True)
                new_txt = str(txt)
                for (loc, mm) in abbr_dict_list:
                    sub_list = mm.getSubEntriesAsList()
                    (sub_loc, txt) = sub_list[1]
                    abbrev_orig_rec, abbrev_part, exp_part = cm.extractAbbr(txt)
                    new_txt = cm.jointText(new_txt, abbrev_part, loc)
                return new_txt
            else:
                return txt

        def getAndMakeRef(m: Message):
            def makeDictEntry(txt: str):
                match = df.ARCH_BRAKET_SINGLE.search(txt)
                if match:
                    key = match.group(1)
                    entry = (key, txt)
                    return entry
                else:
                    return (None, None)

            def rmLocInTxt(loc_list: list, txt: str):
                loc_list.sort(reverse=True)
                new_txt = str(txt)
                for loc in loc_list:
                    new_txt = cm.jointText(new_txt, "", loc)
                return new_txt

            mid = m.id
            is_empty = len(mid) == 0
            if is_empty:
                return []

            mstr = m.string

            abbr_dict = pu.patternMatchAll(df.ABBREV_PATTERN_PARSER, mstr)
            has_abbr = len(abbr_dict) > 0
            if has_abbr:
                mstr = extractAbbr(mstr)
                has_abbr = True

            is_debug = ('AutoCAD DXF' in mid)
            if is_debug:
                # mid = extractGuiLabel(mid)
                # mstr = extractGuiLabel(mstr)
                is_debug = True

            mid = rmKeyBoard(mid)
            mstr = rmKeyBoard(mid)

            print_list = []
            global_ref_list = OrderedDict()
            ref_list = getRefOneLine(mid)
            global_ref_list.update(ref_list)

            ref_list = getRefOneLine(mstr)
            global_ref_list.update(ref_list)
            has_ref = len(ref_list) > 0
            processed_ref_loc = {}
            has_keyboard = False
            for (loc, mm) in global_ref_list.items():
                try:
                    type = mm.type
                    sub_list = mm.getSubEntriesAsList()
                    try:
                        (loc, txt) = sub_list[1]
                        txt = df.REF_LINK.sub("", txt)
                        txt = txt.strip()
                        is_menu =  ('-->' in txt)
                        if is_menu:
                            try:
                                (loc, txt) = sub_list[2]
                            except Exception as e:
                                (loc, txt) = sub_list[1]
                            txt = txt.strip()
                            output_list = extract_menu(txt)
                            print_list.extend(output_list)
                            entry = {loc: ""}
                            processed_ref_loc.update(entry)
                        else:
                            bracket = df.ARCH_BRAKET_SINGLE.search(txt)
                            has_bracket = (bracket is not None)
                            if has_bracket:
                                try:
                                    output_list = extractBracket(txt)
                                    print_list.extend(output_list)
                                    entry = {loc: ""}
                                    processed_ref_loc.update(entry)
                                except Exception as e:
                                    print(f'abbrev_entry! {e}')
                            else:
                                try:
                                    abbrev_entry = getTran(txt)
                                    print_list.append(abbrev_entry)
                                    entry = {loc: ""}
                                    processed_ref_loc.update(entry)
                                except Exception as e:
                                    print(f'abbrev_entry! {e}')
                                has_bracket = False
                    except Exception as e:
                        (loc, txt) = sub_list[0]
                except Exception as e:
                    print_list.append(mm.txt)

            repeat_format1 = f'({mid.lower()})'
            repeat_format2 = f'{mid.lower()}'
            mstr_lower = mstr.lower()

            i1 = mstr_lower.find(repeat_format1)
            i2 = mstr_lower.find(repeat_format2)

            is_repeated1 = (i1 >= 0)
            is_repeated2 = (i2 >= 0)
            is_repeated = (is_repeated1 or is_repeated2)

            if not is_repeated:
                return []

            mstr = extractGuiLabel(mstr)

            if is_repeated1:
                left = mstr[:i1]
                right = mstr[i1 + len(repeat_format1):]
                vn_part = left + right
            elif is_repeated2:
                left = mstr[:i2]
                right = mstr[i2 + len(repeat_format2):]
                vn_part = left + right

            vn_part = vn_part.strip()
            vn_part = df.REF_LINK.sub("", vn_part)
            bracket = df.ARCH_BRAKET_SINGLE.search(vn_part)
            is_bracketed = (bracket is not None)
            if is_bracketed:
                vn_part = bracket.group(1)

            abbrev_line = f':abbr:`{vn_part} ({mid})`'
            print_list.append(abbrev_line)
            new_abbrev_line = f'\\"{abbrev_line}\\"'
            print_list.append(new_abbrev_line)

            has_data = len(print_list) > 0
            if not has_data:
                return
            else:
                dict_list = list(map(makeDictEntry, print_list))
                dict_list = [(x, y) for (x, y) in dict_list if (x is not None)]
                dict_list.sort()
                for (x, y) in dict_list:
                    print(y)

        home = self.home
        dict_file = os.path.join(home, 'cor_0014.po')
        input_file = os.path.join(home, 'blender_manual_0003_0019.po')
        output_file = os.path.join(home, 'blender_manual_0003_0020.po')
        tf = TranslationFinder()
        data = c.load_po(input_file)
        result_list = list(map(getAndMakeRef, data))

    def sort_by_field(self):
        def makeDictEntry(txt: str):
            match = df.ARCH_BRAKET_SINGLE.search(txt)
            if match:
                key = match.group(1)
                entry = (key, txt)
                return entry
            else:
                return (None, None)

        home = self.home
        in_file = os.path.join(home, 'work.log')
        with open(in_file, "r") as f:
            data = f.read()
        data_list = data.split('\n')
        dict_list = list(map(makeDictEntry, data_list))
        dict_list = [(x, y) for (x, y) in dict_list if (x is not None)]
        dict_list.sort()
        for (x, y) in dict_list:
            print(y)

    def sudoku(self):
        def possible(x, y, n):
            for col in range(9):
                cell = grid[y][col]
                sub_row = grid[y][col:]
                is_filled = (cell == n)
                if is_filled:
                    return False
            for row in range(9):
                cell = grid[row][x]
                sub_row = grid[row][x:]
                is_filled = (cell == n)
                if is_filled:
                    return False
            x0 = (x // 3) * 3
            y0 = (y // 3) * 3
            for col in range(0, 3):
                for row in range(0, 3):
                    cel_y = y0+col
                    cel_x = x0+row
                    cell = grid[cel_y][cel_x]
                    sub_row = grid[cel_y][cel_x:]
                    is_filled = (cell == n)
                    if is_filled:
                        return False
            return True

        def solve():
            for col in range(9):
                for row in range(9):
                    cell = grid[col][row]
                    sub_row = grid[col][row:]
                    is_not_filled = (cell == 0)
                    if is_not_filled:
                        for n in range(1, 10):
                            is_pos = possible(col, row, n)
                            if is_pos:
                                sub_row = grid[col][row:]
                                is_pos = possible(col, row, n)
                                grid[col][row] = n
                                solve()
                                grid[col][row] = 0
                        return
            # pp(grid)


        # grid=[
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        # ]
        grid = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 3, 5, 0, 0, 0, 0, 4, 0],
            [0, 0, 8, 0, 9, 4, 0, 3, 6],

            [6, 0, 0, 0, 7, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 9, 4, 5, 0],
            [0, 0, 0, 0, 0, 8, 0, 0, 0],

            [0, 0, 9, 0, 0, 0, 7, 0, 0],
            [0, 0, 0, 7, 0, 0, 2, 0, 0],
            [4, 0, 3, 0, 0, 2, 0, 0, 0],
        ]
        solve()

    def tranRefs(self):
        from datetime import datetime, date
        from collections import OrderedDict
        from refs.ref_base import RefBase
        from refs.ref_menu import RefMenu
        from refs.ref_abbr import RefAbbr
        from refs.ref_keyboard import RefKeyboard
        from refs.ref_guilabel import RefGUILabel
        from refs.ref_with_link import RefWithLink
        from refs.ref_term import RefTerm
        from refs.ref_with_external_link import RefWithExternalLink
        from refs.ref_with_internal_link import RefWithInternalLink
        from refs.ref_single_quote import RefSingleQuote
        from refs.ref_ast import RefAST
        from refs.ref_ga_only import RefGA
        from refs.ref_ga_with_bracket import RefGAWithBrackets


        def translateRefs(m: Message):
            def insertRefHandler(ref_handler: RefBase):
                new_txt = translateRefs.new_txt
                handler = ref_handler(new_txt, tf=tf)
                pat = handler.getPattern()
                dict_list = pu.patternMatchAll(pat, mid)
                has_patterns = len(dict_list) > 0
                if not has_patterns:
                    return None

                loc_list = list(dict_list.keys())
                handler.obs = insertRefHandler.obs
                handler.obs.markLocListAsUsed(loc_list)

                dict_list = list(dict_list.items())
                dict_list.sort(reverse=True)
                handler.extend(dict_list)
                return handler

            def translate_handler(ref_handler: RefBase):
                ref_handler.obs = translateRefs.obs
                ref_handler.translateAll()
                translate_handler.global_untran_list.extend(ref_handler.need_tran_list)
                return ref_handler

            mid = m.id
            has_id = len(mid) > 0
            if not has_id:
                return None

            mstr = m.string
            has_tran = len(mstr) > 0
            if has_tran:
                return None

            is_debug = ('["Agent"]' in mid)
            if is_debug:
                is_debug = True

            # always the global mid text has already been updated,
            # each ref handler would generate it's own locations,
            # after previous handler has updated the message
            new_txt = str(mid)
            global_obs: LocationObserver = LocationObserver(mid)
            translateRefs.obs: LocationObserver = global_obs
            insertRefHandler.obs: LocationObserver = global_obs
            translateRefs.new_txt = new_txt

            handler_list_raw = list(map(insertRefHandler, ref_handler_list))
            handler_list = [handler for handler in handler_list_raw if (handler is not None)]
            has_handlers = len(handler_list) > 0
            if not has_handlers:
                return None

            translate_handler.global_untran_list = global_untran_list
            handler_list = list(map(translate_handler, handler_list))

            ref_list = [x for y in handler_list for x in y]


            for (loc, mm) in ref_list:
                is_translated = (mm.translation is not None)
                if not is_translated:
                    continue

                sub_list = mm.getSubEntriesAsList()
                (oloc, otxt) = sub_list[0]
                tran_txt = mm.translation
                new_txt = cm.jointText(new_txt, tran_txt, oloc)



            is_changed = (new_txt != mid)
            if not is_changed:
                return None

            report_msg = f'\nmid:{mid}\nnew_mstr:{new_txt}\n\n'
            print(report_msg)
            m.string = new_txt
            is_debug = True
            return m

        ref_handler_list = [RefMenu]
        ref_handler_list = [RefGAWithBrackets]
        global_untran_list=[]
        home = self.home
        dict_file = os.path.join(home, 'cor_0014.po')
        input_file = os.path.join(home, 'blender_manual_0003_0019.po')
        output_file = os.path.join(home, 'blender_manual_0003_0020.po')
        untran_dic_file = os.path.join(home, '20220408_untran.po')
        tf = TranslationFinder()
        data = c.load_po(input_file)

        translateRefs.ref_handler_list = ref_handler_list
        result_list = list(map(translateRefs, data))

        is_translated_list = [(mm is not None) for mm in result_list]
        is_changed = (True in is_translated_list)
        is_writing_changes = (is_changed and output_file is not None)
        has_untran = len(global_untran_list) > 0
        if has_untran:
            global_untran_list = list(set(global_untran_list))
            global_untran_list.sort()

            # use dict to filter out same text different case entries
            lcase_dict = OrderedDict()
            for txt in global_untran_list:
                entry = {txt.lower(): txt}
                lcase_dict.update(entry)
            global_untran_list = list(lcase_dict.values())

            today_date = datetime.now()
            untran_catalog = Catalog(project='Translate Blender Man',
                        version='1.0',
                        creation_date=today_date,
                        revision_date=today_date,
                        language_team="UK <hoangduytran1960@gmail.com>",
                        locale="vi",
                        last_translator="Hoang Duy Tran <hoangduytran1960@gmail.com>")
            for txt in global_untran_list:
                txt = txt.strip()
                untran_catalog.add(txt)
            c.dump_po(untran_dic_file, untran_catalog, line_width=4096)

        if is_writing_changes:
            print(f'writing changes to {output_file}')
            # c.dump_po(output_file, data, line_width=4096)

    def tranRefDriver(self):
        from refs.ref_driver import RefDriver
        driver = RefDriver()
        driver.executeDriver()

    def run(self):
        self.tranRefDriver()
        # self.sudoku()
        # self.sort_by_field()
        # self.printRefs()
        # self.tranRefs()
        # self.test_pat()
        # self.correctBrackets()
        # self.duplicateIdInTitles() ###
        # self.fixGlossaryEntriesMakeEnGoesFirst()
        # self.cleanRefOnlyTran()
        # self.correctRef()
        # self.abbrev()
        # self.test_grep()
        # self.test_sent()
        # self.fix_blender_man()
        # self.test_pattern()
        # self.cleanBrackets()
        # self.checkOldRef()
        # self.test_ref()
        # self.cleanRepeat()
        # self.find_terms()
        # self.testenum()
        # self.correct_ref()
        # self.debug_po()©
        # self.testRefList()
        # self.fixpo()
        # self.fix_file()
        # self.fix_abbr()
        # self.testString()
        # self.flatText()
        # self.cleanDict()
        # self.test_0001()
        # import cProfile
        # self.findRefText()
        # self.findUnknownRefs()
        # self.resort_dictionary()
        # self.test_translate_0001()
        # self.cleanSS()+
        # self.translate_backup_dict()
        # self.translate_backup_dict_using_google()
        # self.test_code_0001()
        # self.test_brk_pat()
        # self.cleanKritaPOFile()
        # self.correct_snippet_seq()
        # self.printEmptyPOLines()
        # self.test_pattern()
        # self.test_get_partial()
        # self.debugSphinxBuild_MakeGettext()

# /Users/hoangduytran/Dev/tran/blender_docs
# sphinx-build -M gettext "./manual" "build" -j auto -D language='en'

# from sphinx.cmd.build import main
#
# if __name__ == '__main__':
#     sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
#     sys.exit(main())

x = test()
# # cProfile.run('x.run()', 'test_profile.dat')
# #
# # import pstats
# # from pstats import SortKey
# #
# # with open('output_time.txt', 'w') as f:
# #     p = pstats.Stats('test_profile.dat', stream=f)
# #     p.sort_stats('time').print_stats()
# #
# # with open('output_calls.txt', 'w') as f:
# #     p = pstats.Stats('test_profile.dat', stream=f)
# #     p.sort_stats('calls').print_stats()
#
x.run()

